"""Own Organizing-generated immediate-child Index Element projections."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from capabilities.markdown import Section, heading_comments
from capabilities.yaml import YamlError, parse_mapping, serialize as serialize_yaml
from .convention import token_sort_value
from .links import relative_display_path, relative_link
from .model import (
    Artifact,
    Corpus,
    OrganizingError,
    artifact_by_uid,
    corpus_path,
    read_text,
    render_address,
)

INDEX_UID = "BZJASV"
INDEX_RENDERER_UID = "45E225"
INDEX_VERSION = "2.0"
LEGACY_BEGIN = "<!-- BEGIN index -->"
LEGACY_END = "<!-- END index -->"


@dataclass(frozen=True)
class ElementSection:
    section: Section
    metadata: dict


def _element_sections(text: str, uid: str) -> list[ElementSection]:
    found: list[ElementSection] = []
    for comment in heading_comments(text):
        if not comment.content.lstrip().startswith("element:"):
            continue
        try:
            metadata = parse_mapping(comment.content)
        except YamlError as exc:
            raise OrganizingError(
                f"line {comment.section.start_line}: heading metamatter is not valid YAML: {exc}"
            ) from exc

        element = metadata.get("element")
        if isinstance(element, dict):
            path = element.get("path")
            if isinstance(path, dict) and path.get("uid") == uid:
                found.append(ElementSection(comment.section, metadata))
        elif isinstance(element, str) and f'uid="{uid}"' in element:
            found.append(ElementSection(comment.section, metadata))
    return found


def _index_section(path: Path) -> ElementSection:
    text = read_text(path)
    found = _element_sections(text, INDEX_UID)
    if len(found) != 1:
        raise OrganizingError(
            f"{path}: index owner must contain exactly one heading-bounded "
            f"element declaration for uid {INDEX_UID}"
        )
    return found[0]


def _version_value(artifact: Artifact) -> str:
    version = artifact.metadata.get("version")
    if not isinstance(version, dict) or not isinstance(version.get("value"), str):
        raise OrganizingError(
            f"{artifact.path}: versioned Element must declare version.value"
        )
    value = version["value"]
    parts = value.split(".")
    if len(parts) != 2 or any(not part.isdigit() for part in parts):
        raise OrganizingError(
            f"{artifact.path}: version.value must use major.minor"
        )
    return value


def _declared_filepath(metadata: dict, key: str, uid: str) -> str | None:
    element = metadata.get("element")
    if not isinstance(element, dict):
        return None
    value = element.get(key)
    if not isinstance(value, dict) or value.get("uid") != uid:
        return None
    filepath = value.get("filepath")
    return filepath if isinstance(filepath, str) and filepath else None


def _canonical_declaration(corpus: Corpus, current: dict) -> dict:
    by_uid = artifact_by_uid(corpus)
    element = by_uid.get(INDEX_UID)
    renderer = by_uid.get(INDEX_RENDERER_UID)

    if element is not None:
        element_filepath = corpus_path(corpus.corpus_root, element.path)
        supported = _version_value(element)
        if supported != INDEX_VERSION:
            raise OrganizingError(
                f"{element.path}: Index renderer emits {INDEX_VERSION} but Element authority declares {supported}"
            )
    else:
        element_filepath = _declared_filepath(current, "path", INDEX_UID)
        if element_filepath is None:
            raise OrganizingError(
                f"Index Element uid {INDEX_UID} is external to the corpus and its declaration has no filepath"
            )

    if renderer is not None:
        renderer_filepath = corpus_path(corpus.corpus_root, renderer.path)
    else:
        renderer_filepath = _declared_filepath(current, "renderer", INDEX_RENDERER_UID)
        if renderer_filepath is None:
            raise OrganizingError(
                f"Index renderer uid {INDEX_RENDERER_UID} is external to the corpus and its declaration has no filepath"
            )

    return {
        "element": {
            "path": {
                "uid": INDEX_UID,
                "filepath": element_filepath,
            },
            "version": INDEX_VERSION,
            "renderer": {
                "uid": INDEX_RENDERER_UID,
                "filepath": renderer_filepath,
            },
        }
    }


def validate_regions(corpus: Corpus) -> None:
    for path, artifact in corpus.artifacts.items():
        if artifact.kind != "md":
            if path in corpus.index_owners:
                raise OrganizingError(
                    f"{corpus_path(corpus.corpus_root, path)}: a Python artifact cannot render an Index Element"
                )
            continue

        text = read_text(path)
        found = _element_sections(text, INDEX_UID)
        legacy_markers = LEGACY_BEGIN in text or LEGACY_END in text
        if path in corpus.index_owners:
            if len(found) != 1:
                raise OrganizingError(
                    f"{corpus_path(corpus.corpus_root, path)}: index owner must contain exactly one "
                    f"heading-bounded Index Element declaration"
                )
        elif found or legacy_markers:
            raise OrganizingError(
                f"{corpus_path(corpus.corpus_root, path)}: Index Element exists but the filesystem "
                "derives no immediate indexed children"
            )


def _ordered_children(corpus: Corpus, children: frozenset[Path]) -> list[Path]:
    return sorted(
        children,
        key=lambda path: (
            tuple(token_sort_value(part) for part in corpus.artifacts[path].location[1:].split("."))
            if corpus.artifacts[path].location
            else (10**9,),
            corpus_path(corpus.corpus_root, path).casefold(),
        ),
    )


def _hint_label(owner: Path, target: Path) -> str:
    """Render a downstream Index member as a non-link filename/path clue."""
    relative = os.path.relpath(target, start=owner.parent)
    return Path(relative).as_posix()


def render_index(
    corpus: Corpus,
    owner: Path,
    children: frozenset[Path],
    *,
    index_level: int,
) -> str:
    if index_level >= 6:
        raise OrganizingError(
            f"{corpus_path(corpus.corpus_root, owner)}: Index Element at H{index_level} "
            "cannot render child headings; maximum Markdown heading depth is H6"
        )

    lines: list[str] = []
    entry_marks = "#" * (index_level + 1)
    for path in _ordered_children(corpus, children):
        artifact: Artifact = corpus.artifacts[path]
        if artifact.uid is None:
            raise OrganizingError(f"{corpus_path(corpus.corpus_root, path)}: indexed child has no uid")

        lines.append(f"{entry_marks} {artifact.title}")
        lines.append("")
        lines.append(artifact.description)
        lines.append("")
        lines.append(
            f'<a href="{relative_link(owner, path)}" uid="{artifact.uid}" '
            f'data-ds-link="relative-path">{relative_display_path(owner, path)}</a>'
        )

        if path.name == "README.md" and path in corpus.immediate:
            lines.append("")
            for hinted in _ordered_children(corpus, corpus.immediate[path]):
                lines.append(f"- `{_hint_label(path, hinted)}`")

        lines.append("")

    return "\n".join(lines).rstrip()


def _render_section(corpus: Corpus, path: Path, element: ElementSection, content: str) -> str:
    text = read_text(path)
    lines = text.splitlines(keepends=True)
    section = element.section
    heading = lines[section.start_line - 1].rstrip("\r\n")
    declaration = serialize_yaml(_canonical_declaration(corpus, element.metadata)).rstrip("\n")
    rendered = f"{heading}\n<!--\n{declaration}\n-->\n\n{content}\n"
    return "".join(lines[: section.start_line - 1]) + rendered + "".join(lines[section.end_line :])


def preflight_indexes(corpus: Corpus) -> None:
    """Reject invalid Index deployments before any refresh mutation occurs."""
    validate_regions(corpus)
    for owner in sorted(corpus.index_owners, key=lambda p: corpus_path(corpus.corpus_root, p).casefold()):
        element = _index_section(owner)
        if element.section.level >= 6:
            raise OrganizingError(
                f"{corpus_path(corpus.corpus_root, owner)}: Index Element at H{element.section.level} "
                "cannot render child headings; maximum Markdown heading depth is H6"
            )


def refresh_indexes(corpus: Corpus) -> None:
    preflight_indexes(corpus)
    for owner in sorted(corpus.index_owners, key=lambda p: corpus_path(corpus.corpus_root, p).casefold()):
        element = _index_section(owner)
        replacement = _render_section(
            corpus,
            owner,
            element,
            render_index(
                corpus,
                owner,
                corpus.immediate[owner],
                index_level=element.section.level,
            ),
        )
        if replacement != read_text(owner):
            owner.write_text(replacement, encoding="utf-8")
