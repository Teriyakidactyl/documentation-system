"""Own inspection and deterministic resequencing for the ordinal-hierarchy scheme."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from repo_manager.capabilities.folder import Rename

from ..model import (
    SUPPORTED_SUFFIXES,
    corpus_path,
    ignored_directory_name,
    ordinal_from_name,
)


class OrdinalSchemeError(ValueError):
    """Raised when an ordinal sequence cannot be normalized deterministically."""


@dataclass(frozen=True)
class OrdinalSequence:
    parent: Path
    entries: tuple[tuple[int, Path], ...]
    missing: tuple[int, ...]

    @property
    def contiguous(self) -> bool:
        return not self.missing and tuple(value for value, _ in self.entries) == tuple(
            range(1, len(self.entries) + 1)
        )


def _renamed(name: str, ordinal: int) -> str:
    current = ordinal_from_name(name)
    if current is None:
        raise OrdinalSchemeError(f"{name!r} has no ordinal prefix")
    prefix = str(current)
    return str(ordinal) + name[len(prefix) :]


def inspect(corpus_root: Path) -> list[OrdinalSequence]:
    root = corpus_root.resolve()
    result: list[OrdinalSequence] = []
    for current, dirs, files in os.walk(root, followlinks=False):
        parent = Path(current).resolve()
        dirs[:] = [
            name
            for name in dirs
            if not ignored_directory_name(name) and not (parent / name).is_symlink()
        ]
        paths = [parent / name for name in dirs]
        paths.extend(
            parent / name
            for name in files
            if Path(name).suffix.lower() in SUPPORTED_SUFFIXES
        )
        numbered = [
            (int(ordinal), path.resolve())
            for path in paths
            if (ordinal := ordinal_from_name(path.name)) is not None
        ]
        if not numbered:
            continue
        numbered.sort(key=lambda item: (item[0], item[1].name.casefold()))
        values = [value for value, _ in numbered]
        if len(values) != len(set(values)):
            duplicates = sorted({value for value in values if values.count(value) > 1})
            raise OrdinalSchemeError(
                f"{corpus_path(root, parent)}: duplicate sibling ordinals {duplicates}"
            )
        expected = set(range(1, len(numbered) + 1))
        missing = tuple(sorted(expected.difference(values)))
        result.append(OrdinalSequence(parent, tuple(numbered), missing))
    return result


def plan_normalization(corpus_root: Path) -> list[Rename]:
    root = corpus_root.resolve()
    plan: list[Rename] = []
    for sequence in inspect(root):
        for desired, (current, path) in enumerate(sequence.entries, start=1):
            if current == desired:
                continue
            destination = path.with_name(_renamed(path.name, desired))
            plan.append(Rename(path, destination))
    return sorted(
        plan,
        key=lambda item: (
            -len(item.source.parent.relative_to(root).parts),
            corpus_path(root, item.source).casefold(),
        ),
    )


def as_dict(corpus_root: Path) -> dict:
    root = corpus_root.resolve()
    sequences = inspect(root)
    plan = plan_normalization(root)
    return {
        "scheme": "ordinal-hierarchy",
        "sequences": [
            {
                "parent": "." if sequence.parent == root else corpus_path(root, sequence.parent),
                "ordinals": [value for value, _ in sequence.entries],
                "missing": list(sequence.missing),
                "contiguous": sequence.contiguous,
            }
            for sequence in sequences
        ],
        "normalization": [
            {
                "from": corpus_path(root, item.source),
                "to": corpus_path(root, item.destination),
            }
            for item in plan
        ],
    }
