"""Own structured Document Element deployment metadata in controlled Markdown."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path

from _capabilities.markdown import HeadingComment, MarkdownError, heading_comments
from _capabilities.yaml import YamlError, parse_mapping, serialize as serialize_yaml
from .model import Artifact, Corpus, OrganizingError, artifact_by_uid, corpus_path, read_text


@dataclass(frozen=True)
class ElementInstance:
    owner: Path
    comment: HeadingComment
    metadata: dict
    element: dict


def instances_for_artifact(artifact: Artifact) -> list[ElementInstance]:
    if artifact.kind != "md":
        return []
    result: list[ElementInstance] = []
    try:
        comments = heading_comments(artifact.body)
    except MarkdownError as exc:
        raise OrganizingError(f"{artifact.path}: {exc}") from exc
    for comment in comments:
        if not comment.content.lstrip().startswith("element:"):
            continue
        try:
            metadata = parse_mapping(comment.content)
        except YamlError as exc:
            raise OrganizingError(
                f"{artifact.path}:{comment.start_line}: element metamatter is not valid YAML: {exc}"
            ) from exc
        element = metadata.get("element")
        if isinstance(element, dict):
            result.append(ElementInstance(artifact.path, comment, metadata, element))
    return result


def element_instances(corpus: Corpus) -> list[ElementInstance]:
    result: list[ElementInstance] = []
    for artifact in sorted(
        corpus.artifacts.values(),
        key=lambda item: corpus_path(corpus.corpus_root, item.path).casefold(),
    ):
        result.extend(instances_for_artifact(artifact))
    return result


def _refresh_locator(locator: object, corpus: Corpus, by_uid: dict[str, Artifact]) -> bool:
    if not isinstance(locator, dict):
        return False
    uid = locator.get("uid")
    if not isinstance(uid, str):
        return False
    target = by_uid.get(uid)
    if target is None:
        return False
    filepath = corpus_path(corpus.corpus_root, target.path)
    if locator.get("filepath") == filepath:
        return False
    locator["filepath"] = filepath
    return True


def refresh_element_filepaths(corpus: Corpus) -> int:
    """Refresh structured Element and Renderer filepaths from durable UIDs."""
    by_uid = artifact_by_uid(corpus)
    changed_files = 0

    for artifact in sorted(
        corpus.artifacts.values(),
        key=lambda item: corpus_path(corpus.corpus_root, item.path).casefold(),
    ):
        instances = instances_for_artifact(artifact)
        replacements: list[tuple[int, int, str]] = []
        for instance in instances:
            metadata = deepcopy(instance.metadata)
            element = metadata["element"]
            changed = _refresh_locator(element.get("path"), corpus, by_uid)
            changed = _refresh_locator(element.get("renderer"), corpus, by_uid) or changed
            if not changed:
                continue
            rendered = serialize_yaml(metadata).rstrip("\n")
            replacements.append(
                (
                    instance.comment.start_line,
                    instance.comment.end_line,
                    f"<!--\n{rendered}\n-->\n",
                )
            )

        if not replacements:
            continue

        source = read_text(artifact.path)
        body = artifact.body
        if not source.endswith(body):
            raise OrganizingError(f"{artifact.path}: Markdown body is not a suffix of source")
        prefix = source[: len(source) - len(body)]
        lines = body.splitlines(keepends=True)
        for start_line, end_line, replacement in sorted(replacements, reverse=True):
            lines[start_line - 1 : end_line] = [replacement]
        rendered_source = prefix + "".join(lines)
        if rendered_source != source:
            artifact.path.write_text(rendered_source, encoding="utf-8")
            changed_files += 1

    return changed_files
