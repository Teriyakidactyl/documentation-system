from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

TOOLING = Path(__file__).resolve().parents[2]
if str(TOOLING) not in sys.path:
    sys.path.insert(0, str(TOOLING))

from _compiler.engine import compile_corpus, resolve_address
from _compiler.model import CompilerError, find_repository_root


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def origin(root_name: str, *, extra_body: str = "", uid: str | None = "ABC123") -> str:
    uid_line = f"uid: {uid}\n" if uid is not None else ""
    return f"""---
{uid_line}description: >-
  `Consult when` *a test corpus is entered* `to` **route through test content**.
---
# {root_name} Origin

{extra_body}
<!-- BEGIN index -->
<!-- END index -->
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
        compile_corpus(root)

        compiled = (root / "README.md").read_text(encoding="utf-8")
        self.assertIn("Project Docs:§1", compiled)

        resolved = resolve_address(root, "Project Docs:§1")
        self.assertEqual("DEF456", resolved["uid"])
        self.assertEqual(str(root.resolve()), resolved["corpus_root"])

    def test_directory_has_corpus_root_role_only_when_declared(self) -> None:
        parent = self.base / "parent"
        nested = parent / "nested"
        write(parent / "README.md", origin("parent"))
        write(nested / "README.md", origin("nested"))
        write(nested / "1 Page.md", page())

        parent_resolution = resolve_address(parent, "parent:§1")
        nested_resolution = resolve_address(nested, "nested:§1")

        self.assertEqual("DEF456", parent_resolution["uid"])
        self.assertEqual("DEF456", nested_resolution["uid"])
        self.assertEqual(str(parent.resolve()), parent_resolution["corpus_root"])
        self.assertEqual(str(nested.resolve()), nested_resolution["corpus_root"])

    def test_location_without_corpus_root_is_not_an_address(self) -> None:
        root = self.make_corpus("project")

        with self.assertRaisesRegex(CompilerError, "must declare the corpus root"):
            resolve_address(root, "§1")

    def test_address_corpus_root_must_match_job_corpus_root(self) -> None:
        root = self.make_corpus("project")

        with self.assertRaisesRegex(CompilerError, "declares corpus root 'other'"):
            resolve_address(root, "other:§1")

    def test_controlled_links_refresh_after_corpus_root_rename(self) -> None:
        root = self.base / "alpha"
        controlled = '<a href="1%20Page.md" uid="DEF456">alpha:§1</a>'
        write(root / "README.md", origin("alpha", extra_body=f"See {controlled}.\n"))
        write(root / "1 Page.md", page())

        compile_corpus(root)
        renamed = self.base / "beta"
        shutil.move(str(root), str(renamed))
        compile_corpus(renamed)

        compiled = (renamed / "README.md").read_text(encoding="utf-8")
        self.assertIn('<a href="1%20Page.md" uid="DEF456">beta:§1</a>', compiled)
        self.assertNotIn(">alpha:§1</a>", compiled)

    def test_reader_visible_address_requires_controlled_link(self) -> None:
        root = self.base / "project"
        write(root / "README.md", origin("project"))
        write(root / "1 Page.md", page(body="See project:§1.\n"))

        result = compile_corpus(root)

        self.assertIn("DS001", {diagnostic.code for diagnostic in result.diagnostics})

    def test_reader_visible_location_without_corpus_root_is_reported(self) -> None:
        root = self.base / "project"
        write(root / "README.md", origin("project"))
        write(root / "1 Page.md", page(body="See §1.\n"))

        result = compile_corpus(root)

        self.assertIn("DS004", {diagnostic.code for diagnostic in result.diagnostics})

    def test_invalid_corpus_root_name_fails_before_uid_minting(self) -> None:
        root = self.make_corpus("bad:root", origin_uid=None)
        before = (root / "README.md").read_text(encoding="utf-8")

        with self.assertRaisesRegex(CompilerError, "cannot be represented"):
            compile_corpus(root)

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
