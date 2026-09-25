"""Plan and apply deterministic organization refactors without guessing dependencies."""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote

from _capabilities.folder import FolderError, Rename, apply as apply_renames
from _capabilities.html import anchors
from .model import OrganizingError, corpus_path
from .schemes.folder import FolderSchemeError, as_dict as folder_as_dict, plan_normalization as folder_plan_normalization
from .schemes.ordinal import OrdinalSchemeError, as_dict as ordinal_as_dict, plan_normalization as ordinal_plan_normalization


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
        chars = list(text)
        for anchor in anchors(text):
            if anchor.attribute("uid") is None:
                continue
            for index in range(anchor.start, anchor.end):
                if chars[index] != "\n":
                    chars[index] = " "
        text = "".join(chars)
        for line_number, line in enumerate(text.splitlines(), start=1):
            for pattern in ordered_patterns:
                if pattern in line:
                    findings.append(UnmanagedReference(path, line_number, pattern))
    return findings


def _uses_folder_conventions(corpus_root: Path) -> bool:
    root = corpus_root.resolve()
    return any(path.name == ".folder.json" for path in root.rglob(".folder.json"))


def _organization_payload_and_plan(corpus_root: Path) -> tuple[dict, list[Rename]]:
    try:
        if _uses_folder_conventions(corpus_root):
            return folder_as_dict(corpus_root), folder_plan_normalization(corpus_root)
        return ordinal_as_dict(corpus_root), ordinal_plan_normalization(corpus_root)
    except (FolderSchemeError, OrdinalSchemeError) as exc:
        raise OrganizingError(str(exc)) from exc


def inspect_organization(corpus_root: Path) -> dict:
    payload, plan = _organization_payload_and_plan(corpus_root)
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


def normalize_conventions(corpus_root: Path, *, apply: bool = False) -> dict:
    root = corpus_root.resolve()
    payload = inspect_organization(root)
    _, plan = _organization_payload_and_plan(root)
    refs = unmanaged_references(root, plan)
    payload["applied"] = False
    if not apply or not plan:
        return payload
    if refs:
        raise OrganizingError(
            "folder convention normalization is blocked by unmanaged literal path references; "
            "inspect the dry-run report and migrate those references first"
        )
    try:
        apply_renames(plan)
    except FolderError as exc:
        raise OrganizingError(str(exc)) from exc
    payload["applied"] = True
    return payload


# Explicit legacy ordinal operation retained for existing callers and tests.
def normalize_ordinals(corpus_root: Path, *, apply: bool = False) -> dict:
    root = corpus_root.resolve()
    try:
        payload = ordinal_as_dict(root)
        plan = ordinal_plan_normalization(root)
    except OrdinalSchemeError as exc:
        raise OrganizingError(str(exc)) from exc
    refs = unmanaged_references(root, plan)
    payload["unmanaged_references"] = [
        {"path": corpus_path(root, item.path), "line": item.line, "value": item.value}
        for item in refs
    ]
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
