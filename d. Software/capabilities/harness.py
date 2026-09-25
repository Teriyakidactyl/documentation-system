"""Own harness discovery and symlink projection mechanics."""
from __future__ import annotations

import os
import subprocess
from pathlib import Path

from .frontmatter import FrontmatterError, load as load_frontmatter

KNOWN_SKILL_DIRS=(
    Path(".agents/skills"),
    Path(".claude/skills"),
    Path(".github/skills"),
)

class HarnessError(RuntimeError):
    """Raised when a harness projection cannot be evaluated or applied safely."""

InstallError=HarnessError

def find_repository_root(script: Path) -> Path:
    try:
        result=subprocess.run(
            ["git","-C",str(script.resolve().parent),"rev-parse","--show-toplevel"],
            check=True,capture_output=True,text=True,
        )
    except (OSError,subprocess.CalledProcessError) as exc:
        raise HarnessError("Could not determine the containing Git repository root") from exc
    root=Path(result.stdout.strip()).resolve()
    if not root.is_dir():
        raise HarnessError(f"Git repository root is not a directory: {root}")
    return root

def skill_name(source_root: Path) -> str:
    path=source_root/"SKILL.md"
    try:
        frontmatter=load_frontmatter(path)
    except FrontmatterError as exc:
        raise HarnessError(str(exc)) from exc
    if frontmatter is None:
        raise HarnessError(f"{path}: missing YAML frontmatter")
    name=frontmatter.data.get("name")
    if not isinstance(name,str) or not name.strip():
        raise HarnessError(f"{path}: frontmatter.name must be a non-empty string")
    return name.strip()

def discover_targets(host_root: Path, explicit: list[Path]) -> list[Path]:
    if explicit:
        targets=[(path if path.is_absolute() else host_root/path).resolve() for path in explicit]
    else:
        targets=[(host_root/relative).resolve() for relative in KNOWN_SKILL_DIRS if (host_root/relative).is_dir()]
    if not targets:
        raise HarnessError(
            "No harness skill directories detected. Create one of "
            ".agents/skills, .claude/skills, .github/skills, or pass --target PATH."
        )
    return sorted(set(targets),key=lambda path:path.as_posix().casefold())

def expected_target(link: Path, source_root: Path) -> Path:
    return Path(os.path.relpath(source_root,start=link.parent))

def status(link: Path, source_root: Path) -> str:
    if not link.exists() and not link.is_symlink():
        return "missing"
    if not link.is_symlink():
        return "conflict"
    try:
        resolved=link.resolve(strict=True)
    except FileNotFoundError:
        return "broken"
    return "correct" if resolved==source_root.resolve() else "wrong-target"

def install(link: Path, source_root: Path) -> str:
    state=status(link,source_root)
    if state=="correct":
        return "already correct"
    if state=="conflict":
        raise HarnessError(f"Refusing to replace non-symlink path: {link}")
    if link.is_symlink():
        link.unlink()
    link.parent.mkdir(parents=True,exist_ok=True)
    link.symlink_to(expected_target(link,source_root),target_is_directory=True)
    return "installed" if state=="missing" else "repaired"

def remove(link: Path, source_root: Path) -> str:
    state=status(link,source_root)
    if state=="missing":
        return "already absent"
    if state=="conflict":
        raise HarnessError(f"Refusing to remove non-symlink path: {link}")
    if state not in {"correct","broken","wrong-target"}:
        raise HarnessError(f"Unexpected link state for {link}: {state}")
    link.unlink()
    return "removed"
