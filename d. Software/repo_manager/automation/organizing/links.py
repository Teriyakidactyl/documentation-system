"""Own UID-controlled link resolution and mechanical href/address rewriting."""

from __future__ import annotations

import os
from pathlib import Path
from urllib.parse import quote

from repo_manager.capabilities.frontmatter import FrontmatterError, module_docstring, replace_module_docstring
from repo_manager.capabilities.html import HtmlAnchor, rewrite_anchors
from repo_manager.capabilities.markdown import transform_prose

from .model import (
    ADDRESS_RE,
    UID_RE,
    OrganizingError,
    Corpus,
    artifact_by_uid,
    heading_target,
    read_text,
    render_address,
    corpus_path,
    walk_files,
)

LINK_TYPE_ATTRIBUTE = "data-ds-link"
ADDRESS_LINK_TYPE = "address"
RELATIVE_PATH_LINK_TYPE = "relative-path"
LINK_TYPES = frozenset({ADDRESS_LINK_TYPE, RELATIVE_PATH_LINK_TYPE})


def relative_link(from_path: Path, to_path: Path) -> str:
    relative = os.path.relpath(to_path, start=from_path.parent)
    return quote(Path(relative).as_posix(), safe="/@")


def relative_display_path(from_path: Path, to_path: Path) -> str:
    relative = os.path.relpath(to_path, start=from_path)
    return Path(relative).as_posix()


def render_control_link(
    owner: Path,
    corpus: Corpus,
    uid: str,
    label: str,
    *,
    link_type: str = ADDRESS_LINK_TYPE,
) -> str:
    if not UID_RE.fullmatch(uid):
        raise OrganizingError(f"{corpus_path(corpus.corpus_root, owner)}: invalid controlled-link uid {uid!r}")
    artifact = artifact_by_uid(corpus).get(uid)
    if artifact is None:
        raise OrganizingError(f"{corpus_path(corpus.corpus_root, owner)}: controlled link names missing uid {uid}")
    if link_type not in LINK_TYPES:
        raise OrganizingError(
            f"{corpus_path(corpus.corpus_root, owner)}: controlled link uid {uid} "
            f"uses unknown link type {link_type!r}"
        )

    href = relative_link(owner, artifact.path)
    if link_type == RELATIVE_PATH_LINK_TYPE:
        display = relative_display_path(owner, artifact.path)
        return (
            f'<a href="{href}" uid="{uid}" '
            f'{LINK_TYPE_ATTRIBUTE}="{RELATIVE_PATH_LINK_TYPE}">{display}</a>'
        )

    match = ADDRESS_RE.fullmatch(label.strip())
    if match is None:
        raise OrganizingError(
            f"{corpus_path(corpus.corpus_root, owner)}: controlled link uid {uid} must display "
            "an address with a corpus-root declaration"
        )
    section = match.group("section")
    heading = heading_target(artifact.body, section, artifact.path) if section else None
    if heading is not None:
        href += "#" + quote(heading.anchor, safe="-._~")
    return f'<a href="{href}" uid="{uid}">{render_address(corpus, artifact, section)}</a>'


def rewrite_markdown_text(text: str, owner: Path, corpus: Corpus) -> tuple[str, int]:
    def rewrite_segment(segment: str) -> tuple[str, int]:
        def render(anchor: HtmlAnchor) -> str | None:
            uid = anchor.attribute("uid")
            if uid is None:
                return None
            link_type = anchor.attribute(LINK_TYPE_ATTRIBUTE) or ADDRESS_LINK_TYPE
            return render_control_link(
                owner,
                corpus,
                uid,
                anchor.text,
                link_type=link_type,
            )

        return rewrite_anchors(segment, render)

    return transform_prose(text, rewrite_segment)


def rewrite_markdown(path: Path, corpus: Corpus) -> int:
    text = read_text(path)
    rewritten, changed = rewrite_markdown_text(text, path, corpus)
    if changed:
        path.write_text(rewritten, encoding="utf-8")
    return changed


def rewrite_python(path: Path, corpus: Corpus) -> int:
    source = read_text(path)
    try:
        parsed = module_docstring(source, str(path))
    except FrontmatterError as exc:
        raise OrganizingError(str(exc)) from exc
    if parsed is None:
        return 0
    body, _ = parsed
    rewritten, changed = rewrite_markdown_text(body, path, corpus)
    if not changed:
        return 0
    try:
        updated = replace_module_docstring(source, rewritten, str(path))
    except FrontmatterError as exc:
        raise OrganizingError(str(exc)) from exc
    path.write_text(updated, encoding="utf-8")
    return changed


def rewrite_control_links(corpus: Corpus) -> int:
    changed = 0
    for path in sorted(walk_files(corpus.corpus_root), key=lambda p: corpus_path(corpus.corpus_root, p).casefold()):
        suffix = path.suffix.lower()
        if suffix == ".md":
            changed += rewrite_markdown(path, corpus)
        elif suffix == ".py":
            changed += rewrite_python(path, corpus)
    return changed
