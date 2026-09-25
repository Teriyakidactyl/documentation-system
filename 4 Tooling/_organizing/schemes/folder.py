"""Plan deterministic .folder.json naming normalization."""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path

from _capabilities.folder import Rename, validate as validate_renames

from ..convention import (
    CONFIG_NAME,
    ConventionError,
    NamespaceConvention,
    canonical_prefix,
    convention_for_children,
    split_prefix,
)
from ..model import (
    SUPPORTED_SUFFIXES,
    corpus_path,
    extract_metadata,
    ignored_directory_name,
)


class FolderSchemeError(ValueError):
    """Raised when folder naming cannot be normalized without guessing."""


@dataclass(frozen=True)
class NamingSequence:
    parent: Path
    kind: str
    scheme: str
    separator: str
    sort: str
    entries: tuple[Path, ...]


def _candidate_files(parent: Path, files: list[str]) -> list[Path]:
    result: list[Path] = []
    for name in files:
        if name in {"README.md", CONFIG_NAME} or name.startswith("."):
            continue
        path = parent / name
        if path.is_symlink() or path.suffix.lower() not in SUPPORTED_SUFFIXES:
            continue
        if extract_metadata(path.resolve()) is not None:
            result.append(path.resolve())
    return result


def _remainder(path: Path, convention: NamespaceConvention) -> tuple[int | None, str]:
    _, value, remainder = split_prefix(path.name, convention)
    if not remainder:
        raise FolderSchemeError(f"{path}: prefix consumes the complete basename")
    # Refuse prefix-like punctuation that is not one of the recognized canonical
    # or legacy forms.  Normalization must not guess whether it is semantic text.
    if value is None and re.match(r"^(?:[0-9]+|[A-Za-z]+)[.)_-]", path.name):
        raise FolderSchemeError(
            f"{path}: basename begins with an unrecognized prefix-like form"
        )
    return value, remainder


def _sort_entries(
    entries: list[Path],
    convention: NamespaceConvention,
) -> list[tuple[Path, str, int | None]]:
    parsed = [(path, *_remainder(path, convention)[::-1]) for path in entries]
    # parsed is (path, remainder, current_value)
    if convention.sort == "alphabetical":
        return sorted(parsed, key=lambda item: (item[1].casefold(), item[0].name.casefold()))
    if convention.sort == "date":
        return sorted(parsed, key=lambda item: (item[0].stat().st_mtime_ns, item[1].casefold()))
    if convention.sort == "size":
        return sorted(parsed, key=lambda item: (item[0].stat().st_size, item[1].casefold()))
    if convention.sort == "numerical":
        keyed = []
        for item in parsed:
            match = re.match(r"^([0-9]+)", item[1])
            if match is None:
                raise FolderSchemeError(
                    f"{item[0]}: numerical sort requires the unprefixed basename to begin with a number"
                )
            keyed.append((int(match.group(1)), item))
        return [item for _, item in sorted(keyed, key=lambda pair: (pair[0], pair[1][1].casefold()))]
    if convention.sort == "none":
        if any(item[2] is None for item in parsed):
            missing = [item[0].name for item in parsed if item[2] is None]
            raise FolderSchemeError(
                "sticky sort requires every managed sibling to have a recognized prefix; "
                f"missing on {missing}"
            )
        values = [item[2] for item in parsed]
        if len(values) != len(set(values)):
            raise FolderSchemeError("sticky sort has duplicate sibling prefix positions")
        return sorted(parsed, key=lambda item: (item[2], item[1].casefold()))
    raise FolderSchemeError(f"unsupported sort {convention.sort!r}")


def _namespace_plan(
    parent: Path,
    entries: list[Path],
    convention: NamespaceConvention,
) -> list[Rename]:
    if convention.scheme == "none" or not entries:
        return []

    if convention.scheme == "":
        plan: list[Rename] = []
        for path in entries:
            _, value, remainder = split_prefix(path.name, convention)
            if value is None:
                _remainder(path, convention)
                continue
            plan.append(Rename(path, path.with_name(remainder)))
        return plan

    ordered = _sort_entries(entries, convention)
    plan = []
    for position, (path, remainder, _) in enumerate(ordered, start=1):
        desired = canonical_prefix(position, convention) + remainder
        if desired != path.name:
            plan.append(Rename(path, path.with_name(desired)))
    return plan


def inspect(corpus_root: Path) -> tuple[list[NamingSequence], list[Rename]]:
    root = corpus_root.resolve()
    sequences: list[NamingSequence] = []
    plan: list[Rename] = []

    try:
        for current, dirs, files in os.walk(root, followlinks=False):
            parent = Path(current).resolve()
            dirs[:] = [
                name
                for name in dirs
                if not ignored_directory_name(name) and not (parent / name).is_symlink()
            ]
            convention = convention_for_children(root, parent)

            folder_entries = [(parent / name).resolve() for name in dirs]
            file_entries = _candidate_files(parent, files)

            for kind, entries, namespace in (
                ("folders", folder_entries, convention.folders),
                ("files", file_entries, convention.files),
            ):
                sequences.append(
                    NamingSequence(
                        parent=parent,
                        kind=kind,
                        scheme=namespace.scheme,
                        separator=namespace.separator,
                        sort=namespace.sort,
                        entries=tuple(entries),
                    )
                )
                plan.extend(_namespace_plan(parent, entries, namespace))
    except ConventionError as exc:
        raise FolderSchemeError(str(exc)) from exc

    plan.sort(
        key=lambda item: (
            -len(item.source.parent.relative_to(root).parts),
            corpus_path(root, item.source).casefold(),
        )
    )
    try:
        validate_renames(plan)
    except Exception as exc:
        raise FolderSchemeError(str(exc)) from exc
    return sequences, plan


def plan_normalization(corpus_root: Path) -> list[Rename]:
    return inspect(corpus_root)[1]


def as_dict(corpus_root: Path) -> dict:
    root = corpus_root.resolve()
    sequences, plan = inspect(root)
    return {
        "scheme": "folder-conventions",
        "sequences": [
            {
                "parent": "." if item.parent == root else corpus_path(root, item.parent),
                "kind": item.kind,
                "prefix_scheme": item.scheme,
                "separator": item.separator,
                "sort": item.sort,
                "entries": [path.name for path in item.entries],
            }
            for item in sequences
        ],
        "normalization": [
            {
                "from": corpus_path(root, item.source),
                "to": corpus_path(root, item.destination),
            }
            for item in plan
        ],
    }
