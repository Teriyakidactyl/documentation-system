"""Orchestrate deterministic compiler passes over the normalized corpus model."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from .diagnostics import Diagnostic, Severity, clear_inline_annotations, validate
from .indexes import compile_indexes
from .links import rewrite_control_links
from .model import (
    CompilerError,
    artifact_by_address,
    build_corpus,
    ensure_uids,
    heading_target,
    repo_path,
    select_corpus,
    split_address,
)


@dataclass(frozen=True)
class CompileResult:
    artifacts: int
    locations: int
    links_refreshed: int
    uids_minted: int
    diagnostics: tuple[Diagnostic, ...]

    @property
    def errors(self) -> int:
        return sum(d.severity is Severity.ERROR for d in self.diagnostics)


def compile_corpus(root: Path) -> CompileResult:
    clear_inline_annotations(root)
    minted = ensure_uids(root)
    corpus = build_corpus(root)
    compile_indexes(corpus)
    corpus = build_corpus(root)
    links = rewrite_control_links(corpus)
    corpus = build_corpus(root)
    diagnostics = tuple(validate(corpus))
    return CompileResult(
        artifacts=len(corpus.artifacts),
        locations=len(corpus.locations),
        links_refreshed=links,
        uids_minted=minted,
        diagnostics=diagnostics,
    )


def resolve_address(root: Path, address: str) -> dict:
    root = root.resolve()
    corpus = build_corpus(root)
    qualifier, location, section = split_address(address)
    target_corpus = select_corpus(corpus, qualifier)
    artifact = artifact_by_address(target_corpus).get(location)
    if artifact is not None:
        parent = target_corpus.parents.get(artifact.path)
        result = {
            "address": address,
            "address_space": target_corpus.address_space,
            "type": "document" if artifact.path.name != "INDEX.md" else "location-index",
            "path": Path(os.path.relpath(artifact.path, start=root)).as_posix(),
            "parent_index": (
                Path(os.path.relpath(parent, start=root)).as_posix() if parent else None
            ),
            "location_ordinal": artifact.ordinal,
            "uid": artifact.uid,
            "title": artifact.title,
            "description": artifact.description,
            "body": artifact.body,
        }
        if section is not None:
            heading = heading_target(artifact.body, section, artifact.path)
            result.update(
                {
                    "section": section,
                    "heading": heading.heading,
                    "body": artifact.body[heading.start : heading.end].rstrip() + "\n",
                }
            )
        return result
    location_path = target_corpus.locations.get(location)
    if location_path is not None and section is None:
        return {
            "address": address,
            "address_space": target_corpus.address_space,
            "type": "location",
            "path": Path(os.path.relpath(location_path, start=root)).as_posix() + "/",
            "index": None,
            "body": None,
        }
    if location_path is not None:
        raise CompilerError(f"{address}: location has no indexed body to resolve #{section}")
    raise CompilerError(f"No indexed document or location resolves from {address}")
