"""Own UID-controlled link resolution and mechanical href/address rewriting."""

from __future__ import annotations

from pathlib import Path
from urllib.parse import quote

from _capabilities.frontmatter import FrontmatterError, module_docstring, replace_module_docstring
from _capabilities.html import HtmlAnchor, rewrite_anchors
from _capabilities.markdown import transform_prose

from .indexes import relative_link
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

def render_control_link(owner: Path, corpus: Corpus, uid: str, label: str) -> str:
    if not UID_RE.fullmatch(uid):
        raise OrganizingError(f"{corpus_path(corpus.corpus_root, owner)}: invalid controlled-link uid {uid!r}")
    artifact = artifact_by_uid(corpus).get(uid)
    if artifact is None:
        raise OrganizingError(f"{corpus_path(corpus.corpus_root, owner)}: controlled link names missing uid {uid}")
    match = ADDRESS_RE.fullmatch(label.strip())
    if match is None:
        raise OrganizingError(
            f"{corpus_path(corpus.corpus_root, owner)}: controlled link uid {uid} must display "
            "an address with a corpus-root declaration"
        )
    section = match.group("section")
    heading = heading_target(artifact.body, section, artifact.path) if section else None
    href = relative_link(owner, artifact.path)
    if heading is not None:
        href += "#" + quote(heading.anchor, safe="-._~")
    return f'<a href="{href}" uid="{uid}">{render_address(corpus, artifact, section)}</a>'


def rewrite_markdown_text(text: str, owner: Path, corpus: Corpus) -> tuple[str, int]:
    def rewrite_segment(segment: str) -> tuple[str, int]:
        def render(anchor: HtmlAnchor) -> str | None:
            uid = anchor.attribute("uid")
            if uid is None:
                return None
            return render_control_link(owner, corpus, uid, anchor.text)

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
