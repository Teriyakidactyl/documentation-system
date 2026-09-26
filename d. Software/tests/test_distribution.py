from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SOFTWARE = Path(__file__).resolve().parents[1]
if str(SOFTWARE) not in sys.path:
    sys.path.insert(0, str(SOFTWARE))

from repo_manager.automation.distribution import DistributionError, build_distribution


def git(root: Path, *arguments: str) -> str:
    return subprocess.run(
        ["git", "-C", str(root), *arguments],
        check=True,
        stdout=subprocess.PIPE,
        text=True,
    ).stdout.strip()


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


class DistributionBuildTests(unittest.TestCase):
    def make_repository(self) -> tuple[tempfile.TemporaryDirectory, Path]:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name) / "source repo"
        root.mkdir()
        git(root, "init", "-q")
        git(root, "config", "user.name", "Distribution Test")
        git(root, "config", "user.email", "distribution@example.invalid")

        write(root / "README.md", "consumer root\n")
        write(root / "docs" / "Guide.md", "guide\n")
        write(root / ".github" / "workflow.yml", "source only\n")
        write(root / "visible" / ".folder.json", "{}\n")
        write(root / "visible" / ".private" / "secret.txt", "secret\n")
        write(root / "visible" / "public.txt", "public\n")
        write(root / "untracked.txt", "not in projection\n")

        executable = root / "tool.py"
        write(executable, "#!/usr/bin/env python3\n")
        executable.chmod(0o755)

        git(root, "add", "README.md", "docs", ".github", "visible", "tool.py")
        git(root, "commit", "-qm", "fixture")
        return temp, root

    def test_build_uses_tracked_files_and_omits_dot_prefixed_components(self) -> None:
        temp, root = self.make_repository()
        output = Path(temp.name) / "distribution"

        result = build_distribution(root, output)

        self.assertEqual(git(root, "rev-parse", "HEAD"), result.source_revision)
        self.assertEqual(root.resolve(), result.source_root)
        self.assertEqual(output.resolve(), result.output_root)
        self.assertTrue((output / "README.md").is_file())
        self.assertTrue((output / "docs" / "Guide.md").is_file())
        self.assertTrue((output / "visible" / "public.txt").is_file())
        self.assertFalse((output / ".github").exists())
        self.assertFalse((output / "visible" / ".folder.json").exists())
        self.assertFalse((output / "visible" / ".private").exists())
        self.assertFalse((output / "untracked.txt").exists())
        self.assertNotIn(".github/workflow.yml", result.files)
        self.assertNotIn("visible/.folder.json", result.files)

    def test_build_replaces_output_and_preserves_executable_mode(self) -> None:
        temp, root = self.make_repository()
        output = Path(temp.name) / "distribution"
        build_distribution(root, output)
        write(output / "stale.txt", "stale\n")

        build_distribution(root, output)

        self.assertFalse((output / "stale.txt").exists())
        self.assertTrue(os.access(output / "tool.py", os.X_OK))

    def test_build_refuses_to_replace_source_repository(self) -> None:
        _, root = self.make_repository()
        with self.assertRaisesRegex(DistributionError, "cannot replace"):
            build_distribution(root, root)


if __name__ == "__main__":
    unittest.main()
