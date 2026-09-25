"""Own deterministic selection and collision-safe filesystem rename transactions.

This capability changes filesystem names only. It does not assign semantic
meaning to a path, choose Documentation System ordinals, or repair references.

`plan_strip_prefix` is deliberately match-driven: a candidate basename is
changed only when the declared regular expression matches from character zero,
and the destination removes exactly the span consumed by that match. An
optional basename glob narrows candidate selection without changing what text is
removed. Non-matching paths are untouched.

Plans may contain files and directories from multiple levels beneath one root.
Application validates the complete plan before mutation, executes deeper sibling
groups before their parents, uses temporary names to avoid in-group collisions,
and rolls completed groups back if a later group fails.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from fnmatch import fnmatchcase
from pathlib import Path


class FolderError(RuntimeError):
    """Raised when a requested path rename transaction is unsafe."""


@dataclass(frozen=True)
class Rename:
    source: Path
    destination: Path


def validate(renames: list[Rename]) -> None:
    if len({item.source for item in renames}) != len(renames):
        raise FolderError("rename plan contains a duplicate source")
    if len({item.destination for item in renames}) != len(renames):
        raise FolderError("rename plan contains a duplicate destination")

    sources = {item.source for item in renames}
    for item in renames:
        if item.source.parent != item.destination.parent:
            raise FolderError("current Folder rename transactions are sibling-only")
        if not item.source.exists():
            raise FolderError(f"rename source does not exist: {item.source}")
        if item.destination.exists() and item.destination not in sources:
            raise FolderError(f"rename destination already exists: {item.destination}")


def plan_strip_prefix(
    root: Path,
    pattern: str,
    *,
    include_files: bool = True,
    include_directories: bool = True,
    name_glob: str | None = None,
) -> list[Rename]:
    """Plan recursive basename-prefix removal for paths whose prefix matches.

    `pattern` is compiled as a regular expression and evaluated with
    `Pattern.match`, so every successful match begins at basename position
    zero. Exactly `basename[:match.end()]` is removed. Text outside that
    consumed prefix is never stripped or normalized.

    `name_glob`, when supplied, is a candidate-selection filter evaluated
    against the complete basename before prefix matching. It never contributes
    characters to the removed span. Files and directories are both candidates
    by default; callers may select only one kind. The root itself and symlinks
    are never renamed.

    The complete plan is validated before it is returned. A matching expression
    that consumes zero characters, consumes the entire basename, creates a
    duplicate destination, or collides with an unmatched existing sibling is
    rejected rather than guessed through.
    """

    root = root.resolve()
    if not root.is_dir():
        raise FolderError(f"strip-prefix root is not a directory: {root}")
    if not include_files and not include_directories:
        raise FolderError("strip-prefix must include files, directories, or both")

    try:
        compiled = re.compile(pattern)
    except re.error as exc:
        raise FolderError(f"invalid strip-prefix regular expression: {exc}") from exc

    plan: list[Rename] = []
    for current, dirs, files in os.walk(root, followlinks=False):
        parent = Path(current).resolve()
        dirs[:] = [
            name
            for name in dirs
            if not (parent / name).is_symlink()
        ]

        candidates: list[str] = []
        if include_directories:
            candidates.extend(dirs)
        if include_files:
            candidates.extend(
                name
                for name in files
                if not (parent / name).is_symlink()
            )

        for name in sorted(candidates, key=str.casefold):
            if name_glob is not None and not fnmatchcase(name, name_glob):
                continue

            match = compiled.match(name)
            if match is None:
                continue
            if match.end() == 0:
                raise FolderError(
                    f"strip-prefix pattern matched zero characters in basename {name!r}"
                )

            remainder = name[match.end() :]
            if not remainder:
                raise FolderError(
                    f"strip-prefix pattern would remove the complete basename {name!r}"
                )

            source = (parent / name).resolve()
            plan.append(Rename(source, source.with_name(remainder)))

    plan.sort(
        key=lambda item: (
            -len(item.source.relative_to(root).parts),
            item.source.as_posix().casefold(),
        )
    )
    validate(plan)
    return plan


def _apply_group(renames: list[Rename]) -> None:
    validate(renames)
    parent = renames[0].source.parent
    temporary: list[tuple[Rename, Path]] = []
    for index, item in enumerate(renames, start=1):
        temp = parent / f".__organizing_move_{index}__{item.source.name}"
        if temp.exists():
            raise FolderError(f"temporary rename path already exists: {temp}")
        temporary.append((item, temp))

    moved_to_temp: list[tuple[Rename, Path]] = []
    completed: list[Rename] = []
    try:
        for item, temp in temporary:
            item.source.rename(temp)
            moved_to_temp.append((item, temp))
        for item, temp in temporary:
            temp.rename(item.destination)
            completed.append(item)
    except OSError as exc:
        for item in reversed(completed):
            if item.destination.exists() and not item.source.exists():
                try:
                    item.destination.rename(item.source)
                except OSError:
                    pass
        for item, temp in reversed(moved_to_temp):
            if temp.exists() and not item.source.exists():
                try:
                    temp.rename(item.source)
                except OSError:
                    pass
        raise FolderError(f"rename transaction failed: {exc}") from exc


def apply(renames: list[Rename]) -> None:
    """Apply one validated rename plan, rolling back prior groups on failure."""

    validate(renames)
    groups: dict[Path, list[Rename]] = {}
    for item in renames:
        groups.setdefault(item.source.parent, []).append(item)

    ordered = [
        groups[parent]
        for parent in sorted(groups, key=lambda path: len(path.parts), reverse=True)
    ]
    completed: list[list[Rename]] = []
    try:
        for group in ordered:
            _apply_group(group)
            completed.append(group)
    except FolderError as exc:
        rollback_error: FolderError | None = None
        for group in reversed(completed):
            reverse = [
                Rename(item.destination, item.source)
                for item in group
            ]
            try:
                _apply_group(reverse)
            except FolderError as rollback_exc:
                rollback_error = rollback_exc
                break
        if rollback_error is not None:
            raise FolderError(
                f"{exc}; rollback also failed: {rollback_error}"
            ) from exc
        raise
