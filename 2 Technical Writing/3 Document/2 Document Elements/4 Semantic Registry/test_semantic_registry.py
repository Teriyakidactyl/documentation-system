from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("semantic_registry", HERE / "semantic_registry.py")
assert SPEC is not None and SPEC.loader is not None
semantic_registry = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(semantic_registry)


class SemanticRegistryTests(unittest.TestCase):
    def test_format_uses_one_absolute_definition_anchor(self) -> None:
        source = (
            '# Terms: # Definitions\n'
            '  "Profile": # A named execution configuration.\n'
            '    "Substrate": "Typed Relation Modeling"\n'
            '    "Storage": "Semantic YAML"\n'
            '\n'
            '  "Another Profile": # A second execution configuration.\n'
            '    "Substrate": "Inferential Derivation"\n'
            '    "Inference Level": "Deductive"\n'
        )
        rendered = semantic_registry.format_content(source)
        lines = rendered.splitlines()
        anchor = lines[0].index("# Definitions")
        for line in lines[1:]:
            if not line.strip():
                continue
            match = semantic_registry.KEY_RE.match(line)
            self.assertIsNotNone(match)
            rest = match.group("rest").strip()
            if rest:
                self.assertEqual(anchor, line.index(rest))

    def test_check_requires_root_definition_comment(self) -> None:
        source = (
            '  "Profile":\n'
            '    "Storage": "Semantic YAML"\n'
        )
        codes = {item.code for item in semantic_registry._line_diagnostics(source)}
        self.assertIn("SR007", codes)

    def test_check_requires_double_quoted_keys(self) -> None:
        source = (
            '  Profile: # A named execution configuration.\n'
            '    "Storage": "Semantic YAML"\n'
        )
        codes = {item.code for item in semantic_registry._line_diagnostics(source)}
        self.assertIn("SR004", codes)

    def test_format_document_changes_only_selected_yaml_block(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "doc.md"
            path.write_text(
                "# Title\n\n"
                "## Profiles\n"
                "<!-- element: semantic-registry -->\n\n"
                "```yaml\n"
                '  "Profile": # A named execution configuration.\n'
                '    "Storage": "Semantic YAML"\n'
                "```\n\n"
                "## Other\n"
                "```yaml\n"
                "other: value\n"
                "```\n",
                encoding="utf-8",
            )
            result = semantic_registry.format_document(path, "Profiles", write=True)
            self.assertTrue(result["changed"])
            rendered = path.read_text(encoding="utf-8")
            self.assertIn("# Terms:", rendered)
            self.assertIn("other: value", rendered)

    def test_diagnostics_accept_canonical_registry(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "doc.md"
            canonical = semantic_registry.format_content(
                '  "Profile": # A named execution configuration.\n'
                '    "Storage": "Semantic YAML"\n'
            )
            path.write_text(
                "# Title\n\n## Profiles\n\n```yaml\n" + canonical + "```\n",
                encoding="utf-8",
            )
            found, _ = semantic_registry.diagnostics(path, "Profiles")
            self.assertEqual([], found)


if __name__ == "__main__":
    unittest.main()
