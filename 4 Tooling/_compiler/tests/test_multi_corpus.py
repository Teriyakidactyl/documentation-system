from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

TOOLING = Path(__file__).resolve().parents[2]
if str(TOOLING) not in sys.path:
    sys.path.insert(0, str(TOOLING))

from _compiler.engine import compile_corpus, resolve_address
from _compiler.model import CompilerError


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def origin(uid: str, address_space: str, dependencies: dict[str, str] | None = None) -> str:
    dependency_yaml = ""
    if dependencies:
        dependency_yaml = "corpus-dependencies:\n" + "".join(
            f"  {name}: {path}\n" for name, path in dependencies.items()
        )
    return f"""---
uid: {uid}
address-space: {address_space}
{dependency_yaml}description: >-
  `Consult when` *routing a test concern* `to` **select a test artifact**.
---
# {address_space} Origin

<!-- BEGIN index -->
<!-- END index -->
"""


def artifact(uid: str | None, title: str, extra_frontmatter: str = "") -> str:
    uid_yaml = f"uid: {uid}\n" if uid is not None else ""
    return f"""---
{uid_yaml}{extra_frontmatter}description: >-
  `Consult when` *testing {title}* `to` **resolve {title} deterministically**.
---
# {title}
"""


class MultiCorpusCompilerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)
        self.dependency = self.base / "documentation-system"
        self.project = self.base / "project"

    def tearDown(self) -> None:
        self.temp.cleanup()

    def make_dependency(self, *, address_space: str = "documentation-system") -> None:
        write(self.dependency / "README.md", origin("DOC001", address_space))
        write(self.dependency / "1 External.md", artifact("ABC123", "External"))

    def make_project(
        self,
        *,
        dependencies: dict[str, str] | None = None,
        local_uid: str | None = "ABC123",
        link_label: str | None = "documentation-system:§1",
    ) -> None:
        write(self.project / "README.md", origin("PRJ001", "project", dependencies))
        extra = ""
        if link_label is not None:
            extra = (
                "form: '<a href=\"*\" uid=\"ABC123\">"
                + link_label
                + "</a>'\n"
            )
        write(self.project / "1 Local.md", artifact(local_uid, "Local", extra))

    def snapshot(self, root: Path) -> dict[str, bytes]:
        return {
            path.relative_to(root).as_posix(): path.read_bytes()
            for path in sorted(root.rglob("*"))
            if path.is_file()
        }

    def test_foreign_controlled_link_is_namespace_scoped_and_dependency_is_read_only(self) -> None:
        self.make_dependency()
        self.make_project(
            dependencies={"documentation-system": "../documentation-system"},
            local_uid="ABC123",
        )
        dependency_before = self.snapshot(self.dependency)

        compile_corpus(self.project)

        local = (self.project / "1 Local.md").read_text(encoding="utf-8")
        self.assertIn(
            '<a href="../documentation-system/1%20External.md" uid="ABC123">'
            "documentation-system:§1</a>",
            local,
        )
        self.assertEqual(dependency_before, self.snapshot(self.dependency))

    def test_foreign_address_resolution_uses_declared_dependency(self) -> None:
        self.make_dependency()
        self.make_project(
            dependencies={"documentation-system": "../documentation-system"},
            link_label=None,
        )

        resolved = resolve_address(self.project, "documentation-system:§1")

        self.assertEqual("documentation-system", resolved["address_space"])
        self.assertEqual("ABC123", resolved["uid"])
        self.assertEqual("../documentation-system/1 External.md", resolved["path"])

    def test_undeclared_foreign_namespace_fails_instead_of_searching(self) -> None:
        self.make_dependency()
        self.make_project(dependencies=None)

        with self.assertRaisesRegex(CompilerError, "not.*declared"):
            compile_corpus(self.project)

    def test_dependency_namespace_mismatch_fails_before_local_uid_minting(self) -> None:
        self.make_dependency(address_space="other-system")
        self.make_project(
            dependencies={"documentation-system": "../documentation-system"},
            local_uid=None,
            link_label=None,
        )
        local_path = self.project / "1 Local.md"
        before = local_path.read_text(encoding="utf-8")

        with self.assertRaisesRegex(CompilerError, "declaring address-space"):
            compile_corpus(self.project)

        self.assertEqual(before, local_path.read_text(encoding="utf-8"))

    def test_second_compile_is_idempotent(self) -> None:
        self.make_dependency()
        self.make_project(
            dependencies={"documentation-system": "../documentation-system"},
            local_uid="PRJ123",
        )

        compile_corpus(self.project)
        after_first = self.snapshot(self.project)
        compile_corpus(self.project)

        self.assertEqual(after_first, self.snapshot(self.project))

    def test_dependency_can_move_without_changing_its_logical_addresses(self) -> None:
        self.make_dependency()
        self.make_project(
            dependencies={"documentation-system": "../documentation-system"},
            link_label=None,
        )
        first = resolve_address(self.project, "documentation-system:§1")

        moved = self.base / "governance"
        shutil.move(str(self.dependency), str(moved))
        project_origin = (self.project / "README.md").read_text(encoding="utf-8")
        project_origin = project_origin.replace(
            "../documentation-system", "../governance"
        )
        write(self.project / "README.md", project_origin)
        second = resolve_address(self.project, "documentation-system:§1")

        self.assertEqual(first["address"], second["address"])
        self.assertEqual(first["uid"], second["uid"])
        self.assertEqual("../governance/1 External.md", second["path"])


if __name__ == "__main__":
    unittest.main()
