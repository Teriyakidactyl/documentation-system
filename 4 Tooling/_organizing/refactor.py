"""Plan and apply deterministic organization refactors without guessing dependencies."""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote

from _capabilities.folder import FolderError, Rename, apply as apply_renames

from .links import CONTROL_LINK_RE
from .model import OrganizingError, corpus_path
from .schemes.ordinal import OrdinalSchemeError, as_dict, plan_normalization


@dataclass(frozen=True)
class UnmanagedReference:
    path: Path
    line: int
    value: str


def _text_files(root: Path):
    for current, dirs, files in os.walk(root, followlinks=False):
        parent = Path(current)
        dirs[:] = [
            name
            for name in dirs
            if name != ".git" and not (parent / name).is_symlink()
        ]
        for name in files:
            path = parent / name
            if path.is_symlink():
                continue
            try:
                if path.stat().st_size > 2_000_000:
                    continue
                path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            yield path.resolve()


def unmanaged_references(corpus_root: Path, plan: list[Rename]) -> list[UnmanagedReference]:
    root = corpus_root.resolve()
    patterns: set[str] = set()
    for item in plan:
        relative = corpus_path(root, item.source)
        patterns.add(relative)
        patterns.add(quote(relative, safe="/@"))
    if not patterns:
        return []

    findings: list[UnmanagedReference] = []
    ordered_patterns = sorted(patterns, key=len, reverse=True)
    for path in sorted(_text_files(root), key=lambda item: corpus_path(root, item).casefold()):
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        text = CONTROL_LINK_RE.sub(lambda match: " " * len(match.group(0)), text)
        for line_number, line in enumerate(text.splitlines(), start=1):
            for pattern in ordered_patterns:
                if pattern in line:
                    findings.append(UnmanagedReference(path, line_number, pattern))
    return findings


def inspect_organization(corpus_root: Path) -> dict:
    try:
        payload = as_dict(corpus_root)
    except OrdinalSchemeError as exc:
        raise OrganizingError(str(exc)) from exc
    plan = plan_normalization(corpus_root)
    refs = unmanaged_references(corpus_root, plan)
    payload["unmanaged_references"] = [
        {
            "path": corpus_path(corpus_root.resolve(), item.path),
            "line": item.line,
            "value": item.value,
        }
        for item in refs
    ]
    return payload


def normalize_ordinals(corpus_root: Path, *, apply: bool = False) -> dict:
    root = corpus_root.resolve()
    payload = inspect_organization(root)
    plan = plan_normalization(root)
    refs = unmanaged_references(root, plan)
    payload["applied"] = False
    if not apply or not plan:
        return payload
    if refs:
        raise OrganizingError(
            "ordinal normalization is blocked by unmanaged literal path references; "
            "inspect the dry-run report and migrate those references first"
        )
    try:
        apply_renames(plan)
    except FolderError as exc:
        raise OrganizingError(str(exc)) from exc
    payload["applied"] = True
    return payload
