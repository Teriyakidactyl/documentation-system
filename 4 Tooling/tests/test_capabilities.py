from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
import sys

TOOLING = Path(__file__).resolve().parents[1]
if str(TOOLING) not in sys.path:
    sys.path.insert(0, str(TOOLING))

from _capabilities.frontmatter import load as load_frontmatter
from _capabilities.html import anchors, inspect as inspect_html
from _capabilities.markdown import fenced_blocks, get_section, renumber, sections
from _capabilities.markdown_lint import fix_file as fix_markdown, lint_file as lint_markdown, rule_policy
from _capabilities.yaml import parse_mapping
from _organizing.engine import refresh_corpus
from _organizing.model import OrganizingError
from _organizing.refactor import inspect_organization, normalize_ordinals


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def origin() -> str:
    return """---
uid: ABC123
description: >-
  `Consult when` *a test root is entered* `to` **route through test content**.
---
# Root

<!-- BEGIN index -->
<!-- END index -->
"""


def page(uid: str, title: str = "Page") -> str:
    return f"""---
uid: {uid}
description: >-
  `Consult when` *a test page is needed* `to` **resolve the test page**.
---
# {title}
"""


class CapabilityTests(unittest.TestCase):
    def test_yaml_mapping_is_independent(self) -> None:
        self.assertEqual({"a": 1}, parse_mapping("a: 1\n"))

    def test_python_docstring_frontmatter_loads(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "1 Tool.py"
            write(
                path,
                "r'''---\nuid: ABC123\ndescription: test\n---\n# Tool\n'''\n",
            )
            value = load_frontmatter(path)
            self.assertIsNotNone(value)
            self.assertEqual("ABC123", value.data["uid"])
            self.assertEqual("py", value.kind)

    def test_html_inspection_and_anchor_attributes_are_generic(self) -> None:
        source = "<!-- note --><a uid='ABC123' href='x'>Label</a>"
        tokens = inspect_html(source)
        self.assertEqual("comment", tokens[0].kind)
        found = anchors(source)
        self.assertEqual(1, len(found))
        self.assertEqual("ABC123", found[0].attribute("uid"))
        self.assertEqual("x", found[0].attribute("href"))
        self.assertEqual("Label", found[0].text)

    def test_markdown_sections_support_bounded_agent_reads(self) -> None:
        source = "# Title\n\n## 1 First\nA\n\n### 1.1 Child\nB\n\n## 2 Second\nC\n"
        found = sections(source)
        self.assertEqual(["Title", "1", "1.1", "2"], [item.selector for item in found])
        selected = get_section(source, "1")
        self.assertIn("### 1.1 Child", selected)
        self.assertNotIn("## 2 Second", selected)

    def test_markdown_fenced_blocks_expose_bounded_yaml_content(self) -> None:
        source = (
            "# Title\n\n"
            "## Registry\n"
            "```yaml\n"
            "a: 1\n"
            "```\n\n"
            "```text\n"
            "ignored\n"
            "```\n"
        )
        found = fenced_blocks(source, language="yaml")
        self.assertEqual(1, len(found))
        self.assertEqual("yaml", found[0].language)
        self.assertEqual("a: 1\n", found[0].content)
        self.assertEqual(4, found[0].start_line)
        self.assertEqual(6, found[0].end_line)

    def test_markdown_lint_policy_is_selective_and_adds_local_rules(self) -> None:
        codes = {item["code"] for item in rule_policy()}
        self.assertIn("MD001", codes)
        self.assertIn("MD060", codes)
        self.assertIn("PML100", codes)
        self.assertIn("DSMD001", codes)
        self.assertNotIn("MD013", codes)
        self.assertNotIn("MD033", codes)

    def test_markdown_fix_does_not_cross_into_coordinate_renumbering(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "doc.md"
            write(
                path,
                "---\noutline:\n  numbering: hierarchical-decimal\n---\n"
                "# Title\n\n## 9 Wrong\nParagraph with trailing spaces.  \n",
            )
            before = {item.code for item in lint_markdown(path)}
            self.assertIn("DSMD002", before)
            diagnostics, changed = fix_markdown(path)
            self.assertTrue(changed)
            rendered = path.read_text(encoding="utf-8")
            self.assertIn("## 9 Wrong", rendered)
            self.assertNotIn("spaces.  \n", rendered)
            self.assertIn("DSMD002", {item.code for item in diagnostics})

    def test_markdown_renumber_uses_local_coordinates(self) -> None:
        source = (
            "# Title\n\n"
            "## 3.1.2.1 Preconditions\n"
            "### 3.1.2.1.1 Network\n"
            "## 3.1.2.2 Bootstrap\n"
        )
        rendered, mapping = renumber(source)
        self.assertIn("## 1 Preconditions", rendered)
        self.assertIn("### 1.1 Network", rendered)
        self.assertIn("## 2 Bootstrap", rendered)
        self.assertEqual("1", mapping["3.1.2.1"])
        self.assertEqual("1.1", mapping["3.1.2.1.1"])


class OrdinalOrganizationTests(unittest.TestCase):
    def make_root(self) -> tuple[tempfile.TemporaryDirectory, Path]:
        temp = tempfile.TemporaryDirectory()
        root = Path(temp.name) / "corpus"
        write(root / "README.md", origin())
        write(root / "1 One.md", page("DEF456", "One"))
        write(root / "2 Two.md", page("GHJ789", "Two"))
        write(root / "4 Four.md", page("JKM234", "Four"))
        return temp, root

    def test_inspect_reports_gap_and_complete_plan(self) -> None:
        temp, root = self.make_root()
        self.addCleanup(temp.cleanup)
        payload = inspect_organization(root)
        root_sequence = next(item for item in payload["sequences"] if item["parent"] == ".")
        self.assertEqual([1, 2, 4], root_sequence["ordinals"])
        self.assertEqual([3], root_sequence["missing"])
        self.assertIn(
            {"from": "4 Four.md", "to": "3 Four.md"},
            payload["normalization"],
        )

    def test_refresh_reports_gap_as_warning(self) -> None:
        temp, root = self.make_root()
        self.addCleanup(temp.cleanup)
        result = refresh_corpus(root)
        gap = [item for item in result.diagnostics if item.code == "DS005"]
        self.assertEqual(1, len(gap))
        self.assertEqual("warning", gap[0].severity.value)

    def test_normalize_applies_collision_safe_rename(self) -> None:
        temp, root = self.make_root()
        self.addCleanup(temp.cleanup)
        payload = normalize_ordinals(root, apply=True)
        self.assertTrue(payload["applied"])
        self.assertTrue((root / "3 Four.md").exists())
        self.assertFalse((root / "4 Four.md").exists())

    def test_normalize_blocks_unmanaged_literal_paths(self) -> None:
        temp, root = self.make_root()
        self.addCleanup(temp.cleanup)
        write(root / "config.txt", 'target = "4 Four.md"\n')
        payload = normalize_ordinals(root, apply=False)
        self.assertTrue(payload["unmanaged_references"])
        with self.assertRaisesRegex(OrganizingError, "unmanaged literal path references"):
            normalize_ordinals(root, apply=True)


if __name__ == "__main__":
    unittest.main()
