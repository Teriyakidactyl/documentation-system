"""Orchestrate deterministic Organizing passes over the normalized corpus model."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .diagnostics import Diagnostic, Severity, clear_inline_annotations, validate
from .indexes import refresh_indexes
from .links import rewrite_control_links
from .model import (
    OrganizingError,
    artifact_by_location,
    build_corpus,
    corpus_path,
    ensure_uids,
    heading_target,
    parse_address,
)


@dataclass(frozen=True)
class RefreshResult:
    artifacts: int
    locations: int
    links_refreshed: int
    uids_minted: int
    diagnostics: tuple[Diagnostic, ...]

    @property
    def errors(self) -> int:
        return sum(d.severity is Severity.ERROR for d in self.diagnostics)


def refresh_corpus(corpus_root: Path) -> RefreshResult:
    corpus_root = corpus_root.resolve()
    # Establish the selected root and validate modelable canonical state before
    # any Organizing-owned mutation occurs.
    build_corpus(corpus_root)
    clear_inline_annotations(corpus_root)
    minted = ensure_uids(corpus_root)
    corpus = build_corpus(corpus_root)
    refresh_indexes(corpus)
    corpus = build_corpus(corpus_root)
    links = rewrite_control_links(corpus)
    corpus = build_corpus(corpus_root)
    diagnostics = tuple(validate(corpus))
    return RefreshResult(
        artifacts=len(corpus.artifacts),
        locations=len(corpus.locations),
        links_refreshed=links,
        uids_minted=minted,
        diagnostics=diagnostics,
    )


def resolve_address(corpus_root: Path, address: str) -> dict:
    corpus = build_corpus(corpus_root)
    location, section = parse_address(address, corpus.corpus_root)
    artifact = artifact_by_location(corpus).get(location)
    if artifact is not None:
        parent = corpus.parents.get(artifact.path)
        result = {
            "address": address,
            "corpus_root": str(corpus.corpus_root),
            "type": "document" if artifact.path.name != "INDEX.md" else "location-index",
            "path": corpus_path(corpus_root, artifact.path),
            "parent_index": corpus_path(corpus_root, parent) if parent else None,
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
    location_path = corpus.locations.get(location)
    if location_path is not None and section is None:
        return {
            "address": address,
            "corpus_root": str(corpus.corpus_root),
            "type": "location",
            "path": corpus_path(corpus_root, location_path) + "/",
            "index": None,
            "body": None,
        }
    if location_path is not None:
        raise OrganizingError(f"{address}: location has no indexed body to resolve #{section}")
    raise OrganizingError(f"No indexed document or location resolves from {address}")
