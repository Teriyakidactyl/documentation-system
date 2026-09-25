from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

TOOLING = Path(__file__).resolve().parents[1]
if str(TOOLING) not in sys.path:
    sys.path.insert(0, str(TOOLING))

from automation.organizing.engine import refresh_corpus, resolve_address
from automation.organizing.convention import convention_for_children
from automation.organizing.model import OrganizingError, build_corpus, find_repository_root
from automation.organizing.refactor import normalize_conventions


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def origin(
    root_name: str,
    *,
    extra_body: str = "",
    uid: str | None = "ABC123",
    index_level: int = 2,
) -> str:
    uid_line = f"uid: {uid}\n" if uid is not None else ""
    index_marks = "#" * index_level
    return f"""---
{uid_line}description: >-
  `Consult when` *a test corpus is entered* `to` **route through test content**.
---
# {root_name} Origin

{extra_body}
{index_marks} Index
<!--
element:
  path:
    uid: BZJASV
    filepath: system/Index.md
  version: '0.9'
  renderer:
    uid: 45E225
    filepath: system/Renderer.py
-->
"""



def location_readme(name: str, uid: str = "GHJ789") -> str:
    return f"""---
uid: {uid}
description: >-
  `Consult when` *a test location is entered* `to` **route through its immediate children**.
---
# {name}

## Index
<!--
element:
  path:
    uid: BZJASV
    filepath: system/Index.md
  version: '0.9'
  renderer:
    uid: 45E225
    filepath: system/Renderer.py
-->
"""

def page(uid: str = "DEF456", *, body: str = "") -> str:
    return f"""---
uid: {uid}
description: >-
  `Consult when` *a test page is needed* `to` **resolve the test page**.
---
# Test Page

{body}
"""


class FolderConventionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "corpus"
        write(self.root / "README.md", origin("corpus"))

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write_config(self, directory: Path, value: dict) -> None:
        write(directory / ".folder.json", json.dumps(value, indent=2) + "\n")

    def test_config_governs_children_not_its_own_folder_name(self) -> None:
        self.write_config(
            self.root,
            {
                "folders": {"scheme": "alpha", "separator": ". ", "sort": "alphabetical"},
                "files": {"scheme": "decimal", "separator": ". ", "sort": "alphabetical"},
            },
        )
        tooling = self.root / "d. Software"
        write(tooling / "README.md", location_readme("Software"))
        self.write_config(tooling, {"folders": {"scheme": ""}, "files": {"scheme": ""}})
        write(tooling / "8 Guide.md", page(uid="JKM234"))
        write(tooling / "Reference.md", page(uid="QRS456"))
        write(tooling / "9 Architecture" / "README.md", location_readme("Architecture", uid="MNP345"))

        payload = normalize_conventions(self.root, apply=True)
        self.assertTrue(payload["applied"])
        renamed = self.root / "a. Software"
        self.assertTrue(renamed.is_dir())
        self.assertTrue((renamed / "Guide.md").is_file())
        self.assertTrue((renamed / "Reference.md").is_file())
        self.assertTrue((renamed / "Architecture").is_dir())
        self.assertFalse((renamed / "8 Guide.md").exists())
        self.assertFalse((renamed / "9 Architecture").exists())

    def test_controlled_sidebands_are_outside_folder_naming_normalization(self) -> None:
        self.write_config(
            self.root,
            {
                "folders": {"scheme": "alpha", "separator": ". ", "sort": "alphabetical"},
                "files": {"scheme": "decimal", "separator": ". ", "sort": "alphabetical"},
            },
        )
        sideband = self.root / ".research" / "1 Retained.md"
        write(sideband, page(uid="DEF456"))

        normalize_conventions(self.root, apply=True)

        self.assertTrue(sideband.is_file())
        self.assertFalse((self.root / ".research" / "1. Retained.md").exists())

    def test_partial_legacy_and_canonical_prefixes_reconcile(self) -> None:
        self.write_config(
            self.root,
            {
                "folders": {"scheme": "alpha", "separator": ". ", "sort": "alphabetical"},
                "files": {"scheme": "decimal", "separator": ". ", "sort": "alphabetical"},
            },
        )
        write(self.root / "2 Zebra.md", page(uid="DEF456"))
        write(self.root / "1. Alpha.md", page(uid="GHJ789"))

        normalize_conventions(self.root, apply=True)

        self.assertTrue((self.root / "1. Alpha.md").is_file())
        self.assertTrue((self.root / "2. Zebra.md").is_file())

    def test_invalid_prefix_like_form_fails_before_mutation(self) -> None:
        self.write_config(
            self.root,
            {"files": {"scheme": "decimal", "separator": ". ", "sort": "alphabetical"}},
        )
        write(self.root / "1-Bad.md", page(uid="DEF456"))
        before = sorted(path.name for path in self.root.iterdir())

        with self.assertRaisesRegex(OrganizingError, "unrecognized prefix-like form"):
            normalize_conventions(self.root, apply=True)

        self.assertEqual(before, sorted(path.name for path in self.root.iterdir()))

    def test_undeclared_corpus_preserves_legacy_unnumbered_controlled_files(self) -> None:
        write(self.root / "Tool.py", "r'''---\nuid: T00K01\ndescription: test\n---\n# Tool\n'''\n")
        payload = normalize_conventions(self.root, apply=True)
        self.assertFalse(payload["applied"])
        self.assertTrue((self.root / "Tool.py").is_file())


class CorpusRootTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def make_corpus(self, name: str, *, origin_uid: str | None = "ABC123") -> Path:
        root = self.base / name
        write(root / "README.md", origin(name, uid=origin_uid))
        write(root / "1 Page.md", page())
        return root

    def test_selected_directory_name_is_the_corpus_root_declaration(self) -> None:
        root = self.make_corpus("Project Docs")
        refresh_corpus(root)

        compiled = (root / "README.md").read_text(encoding="utf-8")
        self.assertIn("### Test Page", compiled)
        self.assertIn(
            '<a href="1%20Page.md" uid="DEF456" data-ds-link="relative-path">../1 Page.md</a>',
            compiled,
        )

        resolved = resolve_address(root, "Project Docs:§1")
        self.assertEqual("DEF456", resolved["uid"])
        self.assertEqual(str(root.resolve()), resolved["corpus_root"])

    def test_directory_has_corpus_root_role_only_when_declared(self) -> None:
        parent = self.base / "parent"
        nested = parent / "nested"
        write(parent / "README.md", origin("parent"))
        write(nested / "README.md", origin("nested", uid="GHJ789"))
        write(nested / "1 Page.md", page())

        parent_resolution = resolve_address(parent, "parent:§1")
        nested_resolution = resolve_address(nested, "nested:§1")

        self.assertEqual("DEF456", parent_resolution["uid"])
        self.assertEqual("DEF456", nested_resolution["uid"])
        self.assertEqual(str(parent.resolve()), parent_resolution["corpus_root"])
        self.assertEqual(str(nested.resolve()), nested_resolution["corpus_root"])


    def test_numbered_directory_readme_represents_location_and_owns_index(self) -> None:
        root = self.base / "project"
        write(root / "README.md", origin("project"))
        write(root / "1 Section" / "README.md", location_readme("Section"))
        write(root / "1 Section" / "1 Child.md", page(uid="JKM234"))

        refresh_corpus(root)

        root_compiled = (root / "README.md").read_text(encoding="utf-8")
        section_compiled = (root / "1 Section" / "README.md").read_text(encoding="utf-8")
        self.assertIn("### Section", root_compiled)
        self.assertIn(
            '<a href="1%20Section/README.md" uid="GHJ789" data-ds-link="relative-path">'
            "../1 Section/README.md</a>",
            root_compiled,
        )
        self.assertIn("- `1 Child.md`", root_compiled)
        self.assertIn("### Test Page", section_compiled)
        self.assertIn(
            '<a href="1%20Child.md" uid="JKM234" data-ds-link="relative-path">'
            "../1 Child.md</a>",
            section_compiled,
        )
        self.assertIn("version: '2.0'", section_compiled)
        self.assertNotIn("BEGIN index", section_compiled)
        self.assertNotIn("END index", section_compiled)

        resolved = resolve_address(root, "project:§1")
        self.assertEqual("location-representation", resolved["type"])
        self.assertEqual("1 Section/README.md", resolved["path"])
        self.assertEqual("GHJ789", resolved["uid"])

    def test_index_entries_float_one_heading_level_below_index(self) -> None:
        root = self.base / "project"
        write(root / "README.md", origin("project", index_level=4))
        write(root / "1 Page.md", page())

        refresh_corpus(root)

        compiled = (root / "README.md").read_text(encoding="utf-8")
        self.assertIn("#### Index", compiled)
        self.assertIn("##### Test Page", compiled)

    def test_index_h6_fails_preflight_without_mutation(self) -> None:
        root = self.base / "project"
        write(root / "README.md", origin("project", uid=None, index_level=6))
        write(root / "1 Page.md", page())
        before = (root / "README.md").read_text(encoding="utf-8")

        with self.assertRaisesRegex(
            OrganizingError,
            "Index Element at H6 cannot render child headings",
        ):
            refresh_corpus(root)

        self.assertEqual(before, (root / "README.md").read_text(encoding="utf-8"))
        self.assertNotIn("uid:", before.split("---", 2)[1])

    def test_readme_hint_uses_only_downstream_index_members_in_order(self) -> None:
        root = self.base / "project"
        write(root / "README.md", origin("project"))
        write(root / "1 Section" / "README.md", location_readme("Section"))
        write(root / "1 Section" / "2 Second.md", page(uid="MNP345"))
        write(root / "1 Section" / "1 First.md", page(uid="JKM234"))
        write(
            root / "1 Section" / ".research" / "Unindexed.md",
            """---
uid: QRS456
description: >-
  `Consult when` *an unindexed test page exists* `to` **remain outside the Index hint**.
---
# Unindexed
""",
        )

        refresh_corpus(root)

        compiled = (root / "README.md").read_text(encoding="utf-8")
        first = compiled.index("- `1 First.md`")
        second = compiled.index("- `2 Second.md`")
        self.assertLess(first, second)
        self.assertNotIn("Unindexed.md", compiled)

    def test_unnumbered_controlled_python_in_numbered_location_is_unaddressed(self) -> None:
        root = self.base / "project"
        write(root / "README.md", origin("project"))
        section = root / "1 Section"
        write(
            section / "README.md",
            """---
uid: GHJ789
description: >-
  `Consult when` *a test location is entered* `to` **represent the location**.
---
# Section
""",
        )
        tool = section / "Tool.py"
        write(
            tool,
            """r'''---
uid: T00K01
description: >-
  `Consult when` *a test tool is needed* `to` **exercise unnumbered Python control**.
---
# Test Tool
'''
""",
        )

        refresh_corpus(root)

        corpus = build_corpus(root)
        artifact = corpus.artifacts[tool.resolve()]
        self.assertIsNone(artifact.location)
        compiled = (section / "README.md").read_text(encoding="utf-8")
        self.assertNotIn("Test Tool", compiled)

    def test_decisions_sideband_is_controlled_but_unaddressed(self) -> None:
        root = self.make_corpus("project")
        decision = root / ".decisions" / "Decision.md"
        write(
            decision,
            """---
description: >-
  `Read in full when` *a test decision needs review* `to` **preserve its provenance**.
---
# Test Decision
""",
        )

        refresh_corpus(root)

        refreshed = decision.read_text(encoding="utf-8")
        self.assertIn("uid:", refreshed)
        corpus = build_corpus(root)
        artifact = corpus.artifacts[decision.resolve()]
        self.assertIsNone(artifact.location)
        compiled = (root / "README.md").read_text(encoding="utf-8")
        self.assertNotIn("Test Decision", compiled)

    def test_fault_sideband_is_controlled_but_unaddressed(self) -> None:
        root = self.make_corpus("project")
        fault = root / ".fault" / "Fault.md"
        write(
            fault,
            """---
description: >-
  `Read in full when` *a test fault needs review* `to` **preserve its evidence**.
---
# Test Fault
""",
        )

        refresh_corpus(root)

        refreshed = fault.read_text(encoding="utf-8")
        self.assertIn("uid:", refreshed)
        corpus = build_corpus(root)
        artifact = corpus.artifacts[fault.resolve()]
        self.assertIsNone(artifact.location)
        compiled = (root / "README.md").read_text(encoding="utf-8")
        self.assertNotIn("Test Fault", compiled)

    def test_bare_corpus_root_address_is_invalid(self) -> None:
        root = self.make_corpus("project")

        with self.assertRaisesRegex(
            OrganizingError,
            "Bare corpus-root address '§1' is invalid and unresolvable",
        ):
            resolve_address(root, "§1")

    def test_address_corpus_root_must_match_job_corpus_root(self) -> None:
        root = self.make_corpus("project")

        with self.assertRaisesRegex(OrganizingError, "declares corpus root 'other'"):
            resolve_address(root, "other:§1")

    def test_controlled_link_refresh_accepts_html_attribute_variants(self) -> None:
        root = self.base / "project"
        controlled = "<a uid='DEF456' href='stale.md'>project:§1</a>"
        write(root / "README.md", origin("project", extra_body=f"See {controlled}.\n"))
        write(root / "1 Page.md", page())

        refresh_corpus(root)

        compiled = (root / "README.md").read_text(encoding="utf-8")
        self.assertIn('<a href="1%20Page.md" uid="DEF456">project:§1</a>', compiled)

    def test_controlled_links_refresh_after_corpus_root_rename(self) -> None:
        root = self.base / "alpha"
        controlled = '<a href="1%20Page.md" uid="DEF456">alpha:§1</a>'
        write(root / "README.md", origin("alpha", extra_body=f"See {controlled}.\n"))
        write(root / "1 Page.md", page())

        refresh_corpus(root)
        renamed = self.base / "beta"
        shutil.move(str(root), str(renamed))
        refresh_corpus(renamed)

        compiled = (renamed / "README.md").read_text(encoding="utf-8")
        self.assertIn('<a href="1%20Page.md" uid="DEF456">beta:§1</a>', compiled)
        self.assertNotIn(">alpha:§1</a>", compiled)

    def test_form_version_drift_uses_form_policy(self) -> None:
        root = self.base / "project"
        write(root / "README.md", origin("project"))
        write(
            root / "1 Instance.md",
            """---
uid: DEF456
form:
  path: '<a href="2%20Form/README.md" uid="FRM123">project:§2</a>'
  version: '1.1'
description: >-
  `Consult when` *a versioned instance is tested* `to` **exercise Form drift diagnostics**.
---
# Instance
""",
        )
        write(
            root / "2 Form" / "README.md",
            """---
uid: FRM123
version:
  value: '1.2'
  warn: minor
  error: major
description: >-
  `Consult when` *a test Form is needed* `to` **supply version authority**.
---
# Form
""",
        )

        result = refresh_corpus(root)

        drift = [item for item in result.diagnostics if item.code == "DS006"]
        self.assertEqual(1, len(drift))
        self.assertEqual("warning", drift[0].severity.value)
        self.assertIn("minor drift", drift[0].message)

    def test_form_version_info_is_default_and_newer_claim_is_error(self) -> None:
        root = self.base / "project"
        write(root / "README.md", origin("project"))
        write(
            root / "1 Older.md",
            """---
uid: DEF456
form:
  path: '<a href="3%20Form/README.md" uid="FRM123">project:§3</a>'
  version: '1.0'
description: >-
  `Consult when` *default drift behavior is tested* `to` **exercise informational diagnostics**.
---
# Older
""",
        )
        write(
            root / "2 Newer.md",
            """---
uid: GHJ789
form:
  path: '<a href="3%20Form/README.md" uid="FRM123">project:§3</a>'
  version: '1.3'
description: >-
  `Consult when` *impossible provenance is tested* `to` **reject a future Form claim**.
---
# Newer
""",
        )
        write(
            root / "3 Form" / "README.md",
            """---
uid: FRM123
version:
  value: '1.2'
description: >-
  `Consult when` *a test Form is needed* `to` **supply version authority**.
---
# Form
""",
        )

        result = refresh_corpus(root)

        drift = [item for item in result.diagnostics if item.code == "DS006"]
        self.assertEqual(2, len(drift))
        self.assertEqual(
            {"info", "error"},
            {item.severity.value for item in drift},
        )

    def test_static_element_drift_and_filepath_refresh(self) -> None:
        root = self.base / "project"
        write(root / "README.md", origin("project"))
        write(
            root / "1 Instance.md",
            """---
uid: DEF456
description: >-
  `Consult when` *a versioned Element instance is tested* `to` **exercise Element drift diagnostics**.
---
# Instance

## Terms
<!--
element:
  path:
    uid: E1M123
    filepath: stale/Element.md
  version: '1.1'
-->
Body.
""",
        )
        write(
            root / "2 Element.md",
            """---
uid: E1M123
version:
  value: '1.2'
  warn: minor
  error: major
description: >-
  `Consult when` *a test Element is needed* `to` **supply Element version authority**.
---
# Element
""",
        )

        result = refresh_corpus(root)

        rendered = (root / "1 Instance.md").read_text(encoding="utf-8")
        self.assertIn("filepath: 2 Element.md", rendered)
        drift = [item for item in result.diagnostics if item.code == "DS007"]
        self.assertEqual(1, len(drift))
        self.assertEqual("warning", drift[0].severity.value)
        self.assertIn("minor drift", drift[0].message)

    def test_reader_visible_address_requires_controlled_link(self) -> None:
        root = self.base / "project"
        write(root / "README.md", origin("project"))
        write(root / "1 Page.md", page(body="See project:§1.\n"))

        result = refresh_corpus(root)

        self.assertIn("DS001", {diagnostic.code for diagnostic in result.diagnostics})

    def test_reader_visible_bare_corpus_root_address_is_reported(self) -> None:
        root = self.base / "project"
        write(root / "README.md", origin("project"))
        write(root / "1 Page.md", page(body="See §1.\n"))

        result = refresh_corpus(root)

        self.assertIn("DS004", {diagnostic.code for diagnostic in result.diagnostics})
        self.assertTrue(
            any(
                "Bare corpus-root address §1 is invalid and unresolvable"
                in diagnostic.message
                for diagnostic in result.diagnostics
            )
        )

    def test_invalid_corpus_root_name_fails_before_uid_minting(self) -> None:
        root = self.make_corpus("bad:root", origin_uid=None)
        before = (root / "README.md").read_text(encoding="utf-8")

        with self.assertRaisesRegex(OrganizingError, "cannot be represented"):
            refresh_corpus(root)

        self.assertEqual(before, (root / "README.md").read_text(encoding="utf-8"))

    def test_default_corpus_root_is_compiler_git_repository_root(self) -> None:
        root = self.base / "repo-root"
        root.mkdir()
        subprocess.run(["git", "init", "-q", str(root)], check=True)
        script = root / "tools" / "crawler.py"
        write(script, "# test tool\n")

        self.assertEqual(root.resolve(), find_repository_root(script))


if __name__ == "__main__":
    unittest.main()
