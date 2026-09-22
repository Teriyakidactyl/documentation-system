#!/usr/bin/env python3
r'''---
uid: N5986D
description: >-
  `Read in full and follow when` *a repository has installed the Documentation
  System but an agent harness cannot discover it under the skill name declared
  by SKILL.md* `to` **project the canonical Documentation System directory into
  each selected harness skill directory with an idempotent symlink**.
quadrant: HowTo
---
# 🛠️ Harness Installer

Use this tool from a repository that contains the Documentation System as a
folder or submodule. The canonical folder may carry an ordinal classification
name such as `4 Documentation System`; the harness-facing symlink is named from
`SKILL.md#name`, for example `documentation-system`.

The installer never copies the corpus. It creates or validates symlinks so one
canonical working tree is visible through harness-specific skill paths. A real
file or directory already occupying the target name is never overwritten.

By default the host repository is the current working directory and the script
looks for existing `.agents/skills`, `.claude/skills`, and `.github/skills`
directories. Pass `--target PATH` one or more times to select other skill
directories explicitly.

Usage:
    python3 "4 Tooling/2 🛠️ Harness Installer.py" [host_root]
    python3 "4 Tooling/2 🛠️ Harness Installer.py" --check [host_root]
    python3 "4 Tooling/2 🛠️ Harness Installer.py" --remove [host_root]
    python3 "4 Tooling/2 🛠️ Harness Installer.py" --target .agents/skills [host_root]

Requires PyYAML.
'''

from __future__ import annotations

import os
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


def find_skill_root(script: Path) -> Path:
    for directory in (script.resolve().parent, *script.resolve().parents):
        if (directory / "SKILL.md").is_file():
            return directory
    raise InstallError("Could not find SKILL.md above the installer")


def skill_name(skill_root: Path) -> str:
    path = skill_root / "SKILL.md"
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


def expected_target(link: Path, skill_root: Path) -> Path:
    relative = os.path.relpath(skill_root, start=link.parent)
    return Path(relative)


def status(link: Path, skill_root: Path) -> str:
    if not link.exists() and not link.is_symlink():
        return "missing"
    if not link.is_symlink():
        return "conflict"
    try:
        resolved = link.resolve(strict=True)
    except FileNotFoundError:
        return "broken"
    return "correct" if resolved == skill_root.resolve() else "wrong-target"


def install(link: Path, skill_root: Path) -> str:
    state = status(link, skill_root)
    if state == "correct":
        return "already correct"
    if state == "conflict":
        raise InstallError(f"Refusing to replace non-symlink path: {link}")
    if link.is_symlink():
        link.unlink()
    link.parent.mkdir(parents=True, exist_ok=True)
    link.symlink_to(expected_target(link, skill_root), target_is_directory=True)
    return "installed" if state == "missing" else "repaired"


def remove(link: Path, skill_root: Path) -> str:
    state = status(link, skill_root)
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
    skill_root = find_skill_root(script)
    name = skill_name(skill_root)

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
            state = status(link, skill_root)
            print(f"{state:12} {link}")
            failures += state != "correct"
        elif mode == "remove":
            print(f"{remove(link, skill_root):12} {link}")
        else:
            print(f"{install(link, skill_root):12} {link}")

    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    try:
        main()
    except InstallError as exc:
        raise SystemExit(f"harness installer: {exc}") from exc
