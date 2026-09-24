"""Own collision-safe sibling path rename transactions."""

from __future__ import annotations

from dataclasses import dataclass
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
    groups: dict[Path, list[Rename]] = {}
    for item in renames:
        groups.setdefault(item.source.parent, []).append(item)
    for parent in sorted(groups, key=lambda path: len(path.parts), reverse=True):
        _apply_group(groups[parent])
