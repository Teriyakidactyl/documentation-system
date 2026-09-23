"""Own compiler-generated immediate-child index projections."""

from __future__ import annotations

import os
from pathlib import Path
from urllib.parse import quote

from .model import Artifact, CompilerError, Corpus, corpus_path, read_text, render_address

BEGIN = "<!-- BEGIN index -->"
END = "<!-- END index -->"


def live_marker_offsets(text: str) -> tuple[list[int], list[int]]:
    begins: list[int] = []
    ends: list[int] = []
    in_fence = False
    fence_token: str | None = None
    offset = 0
    for line in text.splitlines(keepends=True):
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            token = stripped[:3]
            if not in_fence:
                in_fence = True
                fence_token = token
            elif token == fence_token:
                in_fence = False
                fence_token = None
        elif not in_fence:
            begin_at = line.find(BEGIN)
            end_at = line.find(END)
            if begin_at != -1:
                begins.append(offset + begin_at)
            if end_at != -1:
                ends.append(offset + end_at)
        offset += len(line)
    return begins, ends


def validate_regions(corpus: Corpus) -> None:
    for path, artifact in corpus.artifacts.items():
        if artifact.kind != "md":
            if path in corpus.index_owners:
                raise CompilerError(
                    f"{corpus_path(corpus.root, path)}: a Python artifact cannot render an index region"
                )
            continue
        begins, ends = live_marker_offsets(read_text(path))
        if path in corpus.index_owners:
            if len(begins) != 1 or len(ends) != 1 or ends[0] < begins[0]:
                raise CompilerError(
                    f"{corpus_path(corpus.root, path)}: index owner must contain exactly one "
                    f"{BEGIN} ... {END} region outside fenced code"
                )
        elif begins or ends:
            raise CompilerError(
                f"{corpus_path(corpus.root, path)}: index region exists but the filesystem "
                "derives no immediate indexed children"
            )


def relative_link(from_path: Path, to_path: Path) -> str:
    relative = os.path.relpath(to_path, start=from_path.parent)
    return quote(Path(relative).as_posix(), safe="/@")


def generated_notice() -> str:
    return (
        "<!-- This block is owned by the Documentation Compiler; run the compiler "
        "whenever indexed information or classification may have changed. -->"
    )


def render_index(corpus: Corpus, owner: Path, children: frozenset[Path]) -> str:
    lines = [generated_notice(), ""]
    ordered = sorted(
        children,
        key=lambda path: (
            tuple(int(part) for part in corpus.artifacts[path].location[1:].split("."))
            if corpus.artifacts[path].location
            else (10**9,),
            corpus_path(corpus.root, path).casefold(),
        ),
    )
    for path in ordered:
        artifact: Artifact = corpus.artifacts[path]
        if artifact.uid is None:
            raise CompilerError(f"{corpus_path(corpus.root, path)}: indexed child has no uid")
        label = render_address(corpus, artifact)
        lines.append(
            f'- <a href="{relative_link(owner, path)}" uid="{artifact.uid}">{label}</a> — {artifact.title}'
        )
        lines.append(f"  - {artifact.description}")
    return "\n".join(lines).rstrip()


def replace_region(path: Path, content: str) -> None:
    text = read_text(path)
    begins, ends = live_marker_offsets(text)
    if len(begins) != 1 or len(ends) != 1:
        raise CompilerError(f"{path}: expected one live index region")
    start = begins[0] + len(BEGIN)
    stop = ends[0]
    replacement = f"{text[:start]}\n{content}\n{text[stop:]}"
    if replacement != text:
        path.write_text(replacement, encoding="utf-8")


def compile_indexes(corpus: Corpus) -> None:
    validate_regions(corpus)
    for owner in sorted(corpus.index_owners, key=lambda p: corpus_path(corpus.root, p).casefold()):
        replace_region(owner, render_index(corpus, owner, corpus.immediate[owner]))
