"""Own normalized corpus facts, identity, and address derivation.

This module owns stable facts about the controlled corpus. It does not render
indexes, rewrite links, emit diagnostics, or decide presentation policy.
"""

from __future__ import annotations

import os
import re
import secrets
import subprocess
from dataclasses import dataclass
from pathlib import Path

from _capabilities.frontmatter import (
    FrontmatterError,
    add_missing_key,
    module_docstring,
    split as split_frontmatter_text,
)
from _capabilities.markdown import (
    HeadingTarget,
    MarkdownError,
    heading_target as markdown_heading_target,
    numbered_headings as markdown_numbered_headings,
    title_from_body as markdown_title_from_body,
)
from _capabilities.yaml import YamlError, parse_mapping as yaml_parse_mapping
from .convention import ConventionError, convention_for_children, token_from_name


IGNORED_DIRS = {"__pycache__"}
CONTROLLED_SIDEBAND_DIRS = {".research", ".decisions", ".fault"}
SUPPORTED_SUFFIXES = {".md", ".py"}
LOCATION_ORDINAL_RE = re.compile(r"^([0-9]+)(?:\.\s+|\s+)")
ADDRESS_RE = re.compile(
    r"^(?P<corpus_root>[^:\r\n]+):"
    r"(?P<location>§[0-9]+(?:\.[0-9]+)*)"
    r"(?:#(?P<section>[0-9]+(?:\.[0-9]+)*))?$"
)
BARE_CORPUS_ROOT_ADDRESS_RE = re.compile(
    r"^§[0-9]+(?:\.[0-9]+)*(?:#[0-9]+(?:\.[0-9]+)*)?$"
)
UID_ALPHABET = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"
UID_RE = re.compile(r"^[0123456789ABCDEFGHJKMNPQRSTVWXYZ]{6}$")


class OrganizingError(RuntimeError):
    """Raised when the corpus cannot be modeled or organized deterministically."""


@dataclass(frozen=True)
class Artifact:
    path: Path
    kind: str
    metadata: dict
    body: str
    title: str
    description: str
    location: str | None
    ordinal: str | None
    uid: str | None


@dataclass(frozen=True)
class Corpus:
    corpus_root: Path
    artifacts: dict[Path, Artifact]
    locations: dict[str, Path]
    origin: Path
    index_owners: frozenset[Path]
    immediate: dict[Path, frozenset[Path]]
    parents: dict[Path, Path]


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise OrganizingError(f"Can't read {path}: {exc}") from exc


def corpus_path(corpus_root: Path, path: Path) -> str:
    return path.resolve().relative_to(corpus_root.resolve()).as_posix()


def corpus_root_name(corpus_root: Path) -> str:
    name = corpus_root.resolve().name
    if not name:
        raise OrganizingError(f"Corpus root has no directory name: {corpus_root}")
    if ":" in name or "\r" in name or "\n" in name:
        raise OrganizingError(
            f"Corpus root directory name {name!r} cannot be represented in a documentation address"
        )
    return name


def find_repository_root(script: Path) -> Path:
    try:
        result = subprocess.run(
            ["git", "-C", str(script.resolve().parent), "rev-parse", "--show-toplevel"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise OrganizingError(
            "Cannot determine the containing Git repository root; pass corpus_root explicitly"
        ) from exc
    root = Path(result.stdout.strip()).resolve()
    if not root.is_dir():
        raise OrganizingError(f"Git repository root is not a directory: {root}")
    return root


def split_frontmatter(text: str) -> tuple[str, str] | None:
    return split_frontmatter_text(text)


def parse_yaml_mapping(raw: str, owner: Path) -> dict:
    try:
        return yaml_parse_mapping(raw)
    except YamlError as exc:
        raise OrganizingError(f"Invalid YAML metadata in {owner}: {exc}") from exc


def title_from_body(body: str, fallback: str) -> str:
    return markdown_title_from_body(body, fallback)


def python_docstring(path: Path) -> tuple[str, int] | None:
    source = read_text(path)
    try:
        return module_docstring(source, str(path))
    except FrontmatterError as exc:
        raise OrganizingError(str(exc)) from exc


def markdown_adapter(path: Path) -> tuple[dict, str, str] | None:
    text = read_text(path)
    separated = split_frontmatter(text)
    if separated is None:
        return None
    raw, body = separated
    metadata = parse_yaml_mapping(raw, path)
    return metadata, body, title_from_body(body, path.stem)


def python_adapter(path: Path) -> tuple[dict, str, str] | None:
    parsed = python_docstring(path)
    if parsed is None:
        return None
    doc, _ = parsed
    separated = split_frontmatter(doc)
    if separated is None:
        return None
    raw, body = separated
    metadata = parse_yaml_mapping(raw, path)
    return metadata, body, title_from_body(body, path.stem)


def extract_metadata(path: Path) -> tuple[dict, str, str] | None:
    suffix = path.suffix.lower()
    if suffix == ".md":
        return markdown_adapter(path)
    if suffix == ".py":
        return python_adapter(path)
    return None


def clean(text: str) -> str:
    return " ".join(text.split())


def description_from_metadata(metadata: dict, owner: Path) -> str:
    value = metadata.get("description")
    if not isinstance(value, str) or not value.strip():
        raise OrganizingError(f"{owner}: description must be a non-empty Markdown scalar")
    return clean(value)


def ordinal_from_name(name: str) -> str | None:
    match = LOCATION_ORDINAL_RE.match(name)
    return match.group(1) if match else None


def location_components(corpus_root: Path, path: Path) -> list[str]:
    root = corpus_root.resolve()
    resolved = path.resolve()
    rel = resolved.relative_to(root)
    if any(part in CONTROLLED_SIDEBAND_DIRS for part in rel.parts[:-1]):
        return []
    components: list[str] = []
    current = root
    try:
        for part in rel.parts[:-1]:
            convention = convention_for_children(root, current).folders
            token = token_from_name(part, convention)
            if token is not None:
                components.append(token)
            current = current / part
        if resolved.name != "README.md":
            convention = convention_for_children(root, resolved.parent).files
            token = token_from_name(resolved.name, convention)
            if token is not None:
                components.append(token)
    except ConventionError as exc:
        raise OrganizingError(str(exc)) from exc
    return components


def location_for(corpus_root: Path, path: Path) -> str | None:
    if path.name != "README.md":
        try:
            convention = convention_for_children(corpus_root, path.parent).files
            if token_from_name(path.name, convention) is None:
                return None
        except ConventionError as exc:
            raise OrganizingError(str(exc)) from exc
    components = location_components(corpus_root, path)
    return "§" + ".".join(components) if components else None


def numbered_headings(body: str) -> list[HeadingTarget]:
    return markdown_numbered_headings(body)


def heading_target(body: str, number: str, owner: Path) -> HeadingTarget:
    try:
        return markdown_heading_target(body, number)
    except MarkdownError as exc:
        raise OrganizingError(f"{owner}: {exc}") from exc


def parse_address(address: str, corpus_root: Path) -> tuple[str, str | None]:
    match = ADDRESS_RE.fullmatch(address)
    if not match:
        if BARE_CORPUS_ROOT_ADDRESS_RE.fullmatch(address):
            raise OrganizingError(
                f"Bare corpus-root address {address!r} is invalid and unresolvable; "
                "addresses must declare the corpus root before ':'"
            )
        raise OrganizingError(f"Invalid documentation address {address!r}")
    declared_root = match.group("corpus_root")
    expected_root = corpus_root_name(corpus_root)
    if declared_root != expected_root:
        raise OrganizingError(
            f"Address {address!r} declares corpus root {declared_root!r}; "
            f"current corpus root is {expected_root!r}"
        )
    return match.group("location"), match.group("section")


def ignored_directory_name(name: str) -> bool:
    return (
        (name.startswith(".") and name not in CONTROLLED_SIDEBAND_DIRS)
        or name in IGNORED_DIRS
        or name.startswith("old_")
    )


def ignored_path(path: Path, corpus_root: Path) -> bool:
    try:
        rel = path.resolve().relative_to(corpus_root.resolve())
    except ValueError:
        return True
    return any(ignored_directory_name(part) for part in rel.parts[:-1]) or path.name.startswith("old_")


def walk_files(corpus_root: Path):
    for current, dirs, files in os.walk(corpus_root, followlinks=False):
        current_path = Path(current)
        dirs[:] = [
            name
            for name in dirs
            if not ignored_directory_name(name) and not (current_path / name).is_symlink()
        ]
        for name in files:
            path = current_path / name
            if path.is_symlink() or ignored_path(path, corpus_root):
                continue
            yield path.resolve()


def load_artifacts(corpus_root: Path) -> dict[Path, Artifact]:
    artifacts: dict[Path, Artifact] = {}
    artifact_locations: dict[str, Path] = {}
    uids: dict[str, Path] = {}
    for path in sorted(walk_files(corpus_root), key=lambda p: corpus_path(corpus_root, p).casefold()):
        if path.suffix.lower() not in SUPPORTED_SUFFIXES:
            continue
        extracted = extract_metadata(path)
        if extracted is None:
            continue
        metadata, body, title = extracted
        location = location_for(corpus_root, path)
        ordinal = (location.split(".")[-1] if location is not None and path.name != "README.md" else None)
        uid = metadata.get("uid")
        if uid is not None:
            if not isinstance(uid, str) or not UID_RE.fullmatch(uid):
                raise OrganizingError(
                    f"{corpus_path(corpus_root, path)}: uid must be six Crockford Base32 characters"
                )
            previous_uid = uids.get(uid)
            if previous_uid is not None:
                raise OrganizingError(
                    f"Duplicate uid {uid}: {corpus_path(corpus_root, previous_uid)} and {corpus_path(corpus_root, path)}"
                )
            uids[uid] = path
        artifact = Artifact(
            path=path,
            kind=path.suffix.lower().lstrip("."),
            metadata=metadata,
            body=body,
            title=title,
            description=description_from_metadata(metadata, path),
            location=location,
            ordinal=ordinal,
            uid=uid,
        )
        if location is not None:
            previous = artifact_locations.get(location)
            if previous is not None:
                raise OrganizingError(
                    f"Duplicate artifact location {location}: "
                    f"{corpus_path(corpus_root, previous)} and {corpus_path(corpus_root, path)}"
                )
            artifact_locations[location] = path
        artifacts[path] = artifact
    return artifacts


def generate_uid(used: set[str]) -> str:
    while True:
        uid = "".join(secrets.choice(UID_ALPHABET) for _ in range(6))
        if uid not in used:
            return uid



def add_uid_to_metadata(path: Path, uid: str) -> None:
    try:
        add_missing_key(path, "uid", uid)
    except FrontmatterError as exc:
        raise OrganizingError(str(exc)) from exc


def ensure_uids(corpus_root: Path) -> int:
    artifacts = load_artifacts(corpus_root)
    used = {artifact.uid for artifact in artifacts.values() if artifact.uid is not None}
    created = 0
    for path, artifact in sorted(artifacts.items(), key=lambda pair: corpus_path(corpus_root, pair[0]).casefold()):
        if artifact.uid is not None:
            continue
        uid = generate_uid(used)
        add_uid_to_metadata(path, uid)
        used.add(uid)
        created += 1
    return created


def location_addresses(corpus_root: Path) -> dict[str, Path]:
    root = corpus_root.resolve()
    result: dict[str, Path] = {}
    for current, dirs, _ in os.walk(root, followlinks=False):
        current_path = Path(current).resolve()
        dirs[:] = [
            name
            for name in dirs
            if not ignored_directory_name(name) and not (current_path / name).is_symlink()
        ]
        if current_path == root:
            continue
        rel = current_path.relative_to(root)
        if any(part in CONTROLLED_SIDEBAND_DIRS for part in rel.parts):
            continue
        components = location_components(root, current_path / "README.md")
        if not components:
            continue
        location = "§" + ".".join(components)
        previous = result.get(location)
        if previous is not None and previous != current_path:
            raise OrganizingError(
                f"Two locations derive {location}: "
                f"{corpus_path(root, previous)} and {corpus_path(root, current_path)}"
            )
        result[location] = current_path
    return result


def validate_sibling_ordinals(corpus_root: Path) -> None:
    for current, dirs, files in os.walk(corpus_root, followlinks=False):
        current_path = Path(current)
        dirs[:] = [
            name
            for name in dirs
            if not ignored_directory_name(name) and not (current_path / name).is_symlink()
        ]
        seen: dict[str, str] = {}
        names = dirs + [
            name for name in files if Path(name).suffix.lower() in SUPPORTED_SUFFIXES
        ]
        for name in names:
            ordinal = ordinal_from_name(name)
            if ordinal is None:
                continue
            previous = seen.get(ordinal)
            if previous is not None:
                raise OrganizingError(
                    f"Duplicate sibling location ordinal {ordinal} in {corpus_path(corpus_root, current_path)}: "
                    f"{previous!r} and {name!r}"
                )
            seen[ordinal] = name


def location_depth(location: str) -> int:
    return len(location.removeprefix("§").split("."))


def derive_index(corpus_root: Path, artifacts: dict[Path, Artifact]) -> tuple[Path, frozenset[Path], dict[Path, frozenset[Path]], dict[Path, Path]]:
    origin = (corpus_root / "README.md").resolve()
    if origin not in artifacts:
        raise OrganizingError("Corpus root must contain indexed README.md")
    immediate: dict[Path, set[Path]] = {}
    parents: dict[Path, Path] = {}
    located = [artifact for artifact in artifacts.values() if artifact.location is not None]

    root_children = {artifact.path for artifact in located if location_depth(artifact.location) == 1}
    if root_children:
        immediate[origin] = root_children
        for child in root_children:
            parents[child] = origin

    for owner in artifacts.values():
        if owner.path.name != "README.md" or owner.location is None:
            continue
        prefix = owner.location + "."
        depth = location_depth(owner.location) + 1
        children = {
            artifact.path
            for artifact in located
            if artifact.location.startswith(prefix) and location_depth(artifact.location) == depth
        }
        if children:
            immediate[owner.path] = children
            for child in children:
                previous = parents.get(child)
                if previous is not None and previous != owner.path:
                    raise OrganizingError(
                        f"{corpus_path(corpus_root, child)} derives multiple index parents: "
                        f"{corpus_path(corpus_root, previous)} and {corpus_path(corpus_root, owner.path)}"
                    )
                parents[child] = owner.path

    frozen = {owner: frozenset(children) for owner, children in immediate.items()}
    return origin, frozenset(frozen), frozen, parents


def build_corpus(corpus_root: Path) -> Corpus:
    corpus_root = corpus_root.resolve()
    if not corpus_root.is_dir():
        raise OrganizingError(f"Corpus root is not a directory: {corpus_root}")
    corpus_root_name(corpus_root)
    validate_sibling_ordinals(corpus_root)
    artifacts = load_artifacts(corpus_root)
    if not artifacts:
        raise OrganizingError(f"No recognized metadata-bearing artifacts beneath {corpus_root}")
    locations = location_addresses(corpus_root)
    origin, owners, immediate, parents = derive_index(corpus_root, artifacts)
    return Corpus(
        corpus_root=corpus_root,
        artifacts=artifacts,
        locations=locations,
        origin=origin,
        index_owners=owners,
        immediate=immediate,
        parents=parents,
    )


def artifact_by_location(corpus: Corpus) -> dict[str, Artifact]:
    return {a.location: a for a in corpus.artifacts.values() if a.location is not None}


def artifact_by_uid(corpus: Corpus) -> dict[str, Artifact]:
    return {a.uid: a for a in corpus.artifacts.values() if a.uid is not None}


def render_address(corpus: Corpus, artifact: Artifact, section: str | None = None) -> str:
    if artifact.location is None:
        raise OrganizingError(
            f"{corpus_path(corpus.corpus_root, artifact.path)}: uid {artifact.uid} has no addressable location"
        )
    address = f"{corpus_root_name(corpus.corpus_root)}:{artifact.location}"
    if section is not None:
        address += f"#{section}"
    return address
