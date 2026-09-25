#!/usr/bin/env python3
r'''---
uid: N5986D
architecture: '<a href="9%20%F0%9F%93%90%20Architecture/2%20%F0%9F%93%96%20Tooling%20Architecture.md" uid="K7W3P9">documentation-system:§4.9.2</a>'
description: >-
  `Read in full and follow when` *a repository has installed the Documentation
  System but an agent harness cannot discover it under the skill name declared
  by SKILL.md* `to` **project the canonical Documentation System directory into
  each selected harness skill directory with an idempotent symlink**.
quadrant: HowTo
---
# 🛠️ Harness Installer

Use this tool from the Documentation System repository or submodule. The
canonical source directory is the Git repository containing this tool; the
harness-facing symlink name is read from `SKILL.md#name`, for example
`documentation-system`.

The installer never copies the corpus. It creates or validates symlinks so one
canonical working tree is visible through harness-specific skill paths. A real
file or directory already occupying the target name is never overwritten.

By default the host repository is the current working directory and the script
looks for existing `.agents/skills`, `.claude/skills`, and `.github/skills`
directories. Pass `--target PATH` one or more times to select other skill
directories explicitly.

Usage:
    python3 "4 Tooling/Harness Installer.py" [host_root]
    python3 "4 Tooling/Harness Installer.py" --check [host_root]
    python3 "4 Tooling/Harness Installer.py" --remove [host_root]
    python3 "4 Tooling/Harness Installer.py" --target .agents/skills [host_root]

Requires PyYAML.
'''

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover - environmental failure
    raise SystemExit("harness installer requires PyYAML") from exc


KNOWN_SKILL_DIRS = (
    Path(".agents/skills"),
    Path(".claude/skills"),
    Path(".github/skills"),
)


class InstallError(RuntimeError):
    """Raised when a safe harness projection cannot be completed."""


def find_repository_root(script: Path) -> Path:
    try:
        result = subprocess.run(
            ["git", "-C", str(script.resolve().parent), "rev-parse", "--show-toplevel"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise InstallError("Could not determine the containing Git repository root") from exc
    root = Path(result.stdout.strip()).resolve()
    if not root.is_dir():
        raise InstallError(f"Git repository root is not a directory: {root}")
    return root


def skill_name(source_root: Path) -> str:
    path = source_root / "SKILL.md"
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise InstallError(f"{path}: missing YAML frontmatter")
    close = text.find("\n---", 4)
    if close == -1:
        raise InstallError(f"{path}: unclosed YAML frontmatter")
    try:
        metadata = yaml.safe_load(text[4:close])
    except yaml.YAMLError as exc:
        raise InstallError(f"{path}: invalid YAML frontmatter: {exc}") from exc
    if not isinstance(metadata, dict):
        raise InstallError(f"{path}: frontmatter must be a mapping")
    name = metadata.get("name")
    if not isinstance(name, str) or not name.strip():
        raise InstallError(f"{path}: frontmatter.name must be a non-empty string")
    return name.strip()


def discover_targets(host_root: Path, explicit: list[Path]) -> list[Path]:
    if explicit:
        targets = [
            (path if path.is_absolute() else host_root / path).resolve()
            for path in explicit
        ]
    else:
        targets = [
            (host_root / relative).resolve()
            for relative in KNOWN_SKILL_DIRS
            if (host_root / relative).is_dir()
        ]
    if not targets:
        raise InstallError(
            "No harness skill directories detected. Create one of "
            ".agents/skills, .claude/skills, .github/skills, or pass --target PATH."
        )
    return sorted(set(targets), key=lambda path: path.as_posix().casefold())


def expected_target(link: Path, source_root: Path) -> Path:
    relative = os.path.relpath(source_root, start=link.parent)
    return Path(relative)


def status(link: Path, source_root: Path) -> str:
    if not link.exists() and not link.is_symlink():
        return "missing"
    if not link.is_symlink():
        return "conflict"
    try:
        resolved = link.resolve(strict=True)
    except FileNotFoundError:
        return "broken"
    return "correct" if resolved == source_root.resolve() else "wrong-target"


def install(link: Path, source_root: Path) -> str:
    state = status(link, source_root)
    if state == "correct":
        return "already correct"
    if state == "conflict":
        raise InstallError(f"Refusing to replace non-symlink path: {link}")
    if link.is_symlink():
        link.unlink()
    link.parent.mkdir(parents=True, exist_ok=True)
    link.symlink_to(expected_target(link, source_root), target_is_directory=True)
    return "installed" if state == "missing" else "repaired"


def remove(link: Path, source_root: Path) -> str:
    state = status(link, source_root)
    if state == "missing":
        return "already absent"
    if state == "conflict":
        raise InstallError(f"Refusing to remove non-symlink path: {link}")
    if state not in {"correct", "broken", "wrong-target"}:
        raise InstallError(f"Unexpected link state for {link}: {state}")
    link.unlink()
    return "removed"


def main() -> None:
    script = Path(__file__).resolve()
    source_root = find_repository_root(script)
    name = skill_name(source_root)

    args = sys.argv[1:]
    mode = "install"
    explicit: list[Path] = []
    positional: list[str] = []
    i = 0
    while i < len(args):
        arg = args[i]
        if arg == "--check":
            mode = "check"
            i += 1
        elif arg == "--remove":
            mode = "remove"
            i += 1
        elif arg == "--target":
            if i + 1 >= len(args):
                raise InstallError("--target requires a path")
            explicit.append(Path(args[i + 1]))
            i += 2
        elif arg in {"-h", "--help"}:
            print(__doc__.split("---\n", 2)[-1].strip())
            return
        else:
            positional.append(arg)
            i += 1

    if len(positional) > 1:
        raise InstallError("Expected at most one host_root argument")
    host_root = Path(positional[0]).resolve() if positional else Path.cwd().resolve()
    if not host_root.is_dir():
        raise InstallError(f"Host root is not a directory: {host_root}")

    targets = discover_targets(host_root, explicit)
    failures = 0
    for skills_dir in targets:
        link = skills_dir / name
        if mode == "check":
            state = status(link, source_root)
            print(f"{state:12} {link}")
            failures += state != "correct"
        elif mode == "remove":
            print(f"{remove(link, source_root):12} {link}")
        else:
            print(f"{install(link, source_root):12} {link}")

    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    try:
        main()
    except InstallError as exc:
        raise SystemExit(f"harness installer: {exc}") from exc
