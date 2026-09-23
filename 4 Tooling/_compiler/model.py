"""Own normalized corpus facts, metadata adapters, identity, and address derivation.

This module owns stable facts about the controlled corpus. It does not render
indexes, rewrite links, emit diagnostics, or decide presentation policy.
"""

from __future__ import annotations

import ast
import io
import os
import re
import secrets
import subprocess
import tokenize
from dataclasses import dataclass
from pathlib import Path

import yaml

IGNORED_DIRS = {"__pycache__"}
CONTROLLED_SIDEBAND_DIRS = {".research"}
SUPPORTED_SUFFIXES = {".md", ".py"}
LOCATION_ORDINAL_RE = re.compile(r"^([0-9]+)(?:\.\s+|\s+)")
ADDRESS_RE = re.compile(
    r"^(?:(?P<space>[a-z0-9][a-z0-9-]*):)?"
    r"(?P<location>§[0-9]+(?:\.[0-9]+)*)"
    r"(?:#(?P<section>[0-9]+(?:\.[0-9]+)*))?$"
)
UID_ALPHABET = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"
UID_RE = re.compile(r"^[0123456789ABCDEFGHJKMNPQRSTVWXYZ]{6}$")
NUMBERED_HEADING_RE = re.compile(
    r"^(?P<marks>#{2,6})\s+(?P<number>[0-9]+(?:\.[0-9]+)*)"
    r"(?P<trailing>\.)?\s+(?P<title>.+?)\s*$"
)
ADDRESS_SPACE = "documentation-system"


class CompilerError(RuntimeError):
    """Raised when the corpus cannot be modeled or compiled deterministically."""


@dataclass(frozen=True)
class Artifact:
    path: Path
    kind: str
    metadata: dict
    body: str
    title: str
    description: str
    address: str | None
    ordinal: str | None
    uid: str | None


@dataclass(frozen=True)
class HeadingTarget:
    number: str
    level: int
    title: str
    heading: str
    anchor: str
    start: int
    end: int


@dataclass(frozen=True)
class Corpus:
    root: Path
    address_space: str
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
        raise CompilerError(f"Can't read {path}: {exc}") from exc


def repo_path(root: Path, path: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def find_repository_root(script: Path) -> Path:
    try:
        result = subprocess.run(
            ["git", "-C", str(script.resolve().parent), "rev-parse", "--show-toplevel"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise CompilerError(
            "Cannot determine the containing Git repository root; pass corpus_root explicitly"
        ) from exc
    root = Path(result.stdout.strip()).resolve()
    if not root.is_dir():
        raise CompilerError(f"Git repository root is not a directory: {root}")
    return root


def split_frontmatter(text: str) -> tuple[str, str] | None:
    if not text.startswith("---\n"):
        return None
    close = text.find("\n---", 4)
    if close == -1:
        return None
    fence_end = close + 4
    if fence_end < len(text) and text[fence_end] == "\n":
        fence_end += 1
    return text[4:close], text[fence_end:]


def parse_yaml_mapping(raw: str, owner: Path) -> dict:
    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError as exc:
        raise CompilerError(f"Invalid YAML metadata in {owner}: {exc}") from exc
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise CompilerError(f"{owner}: metadata must be a mapping")
    return data


def title_from_body(body: str, fallback: str) -> str:
    for line in body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def markdown_adapter(path: Path) -> tuple[dict, str, str] | None:
    text = read_text(path)
    split = split_frontmatter(text)
    if split is None:
        return None
    raw, body = split
    metadata = parse_yaml_mapping(raw, path)
    return metadata, body, title_from_body(body, path.stem)


def python_docstring(path: Path) -> tuple[str, int] | None:
    source = read_text(path)
    try:
        tree = ast.parse(source, filename=str(path))
    except SyntaxError as exc:
        raise CompilerError(f"Can't parse Python documentation in {path}: {exc}") from exc
    if not tree.body:
        return None
    first = tree.body[0]
    if not (
        isinstance(first, ast.Expr)
        and isinstance(first.value, ast.Constant)
        and isinstance(first.value.value, str)
    ):
        return None
    return first.value.value, first.value.lineno


def python_adapter(path: Path) -> tuple[dict, str, str] | None:
    parsed = python_docstring(path)
    if parsed is None:
        return None
    doc, _ = parsed
    split = split_frontmatter(doc)
    if split is None:
        return None
    raw, body = split
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
        raise CompilerError(f"{owner}: description must be a non-empty Markdown scalar")
    return clean(value)


def ordinal_from_name(name: str) -> str | None:
    match = LOCATION_ORDINAL_RE.match(name)
    return match.group(1) if match else None


def address_components(root: Path, path: Path) -> list[str]:
    rel = path.resolve().relative_to(root.resolve())
    if any(part in CONTROLLED_SIDEBAND_DIRS for part in rel.parts[:-1]):
        return []
    components: list[str] = []
    for part in rel.parts[:-1]:
        ordinal = ordinal_from_name(part)
        if ordinal is not None:
            components.append(ordinal)
    if path.name != "INDEX.md":
        ordinal = ordinal_from_name(path.name)
        if ordinal is not None:
            components.append(ordinal)
    return components


def address_for(root: Path, path: Path) -> str | None:
    components = address_components(root, path)
    return "§" + ".".join(components) if components else None


def markdown_anchor(heading: str) -> str:
    value = heading.strip().lower()
    value = re.sub(r"<[^>]+>", "", value)
    value = re.sub(r"[^\w\- ]", "", value, flags=re.UNICODE)
    return re.sub(r"\s+", "-", value)


def numbered_headings(body: str) -> list[HeadingTarget]:
    raw: list[tuple[str, int, str, str, str, int]] = []
    in_fence = False
    fence_token: str | None = None
    offset = 0
    for line in body.splitlines(keepends=True):
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
            match = NUMBERED_HEADING_RE.match(line.rstrip("\r\n"))
            if match:
                marks = match.group("marks")
                number = match.group("number")
                title = match.group("title")
                heading = f"{number}{match.group('trailing') or ''} {title}"
                raw.append((number, len(marks), title, heading, markdown_anchor(heading), offset))
        offset += len(line)

    result: list[HeadingTarget] = []
    for index, (number, level, title, heading, anchor, start) in enumerate(raw):
        end = len(body)
        for _, next_level, _, _, _, next_start in raw[index + 1 :]:
            if next_level <= level:
                end = next_start
                break
        result.append(HeadingTarget(number, level, title, heading, anchor, start, end))
    return result


def heading_target(body: str, number: str, owner: Path) -> HeadingTarget:
    matches = [heading for heading in numbered_headings(body) if heading.number == number]
    if not matches:
        raise CompilerError(f"{owner}: no numbered heading resolves #{number}")
    if len(matches) > 1:
        raise CompilerError(f"{owner}: numbered heading #{number} is ambiguous")
    return matches[0]


def parse_address(address: str, address_space: str) -> tuple[str, str | None]:
    match = ADDRESS_RE.fullmatch(address)
    if not match:
        raise CompilerError(f"Invalid address: {address!r}")
    qualifier = match.group("space")
    if qualifier is not None and qualifier != address_space:
        expected = address_space or "<unqualified corpus>"
        raise CompilerError(
            f"Address {address!r} names address space {qualifier!r}; current space is {expected!r}"
        )
    return match.group("location"), match.group("section")


def ignored_directory_name(name: str) -> bool:
    return (
        (name.startswith(".") and name not in CONTROLLED_SIDEBAND_DIRS)
        or name in IGNORED_DIRS
        or name.startswith("old_")
    )


def ignored_path(path: Path, root: Path) -> bool:
    try:
        rel = path.resolve().relative_to(root.resolve())
    except ValueError:
        return True
    return any(ignored_directory_name(part) for part in rel.parts[:-1]) or path.name.startswith("old_")


def walk_files(root: Path):
    for current, dirs, files in os.walk(root, followlinks=False):
        current_path = Path(current)
        dirs[:] = [
            name
            for name in dirs
            if not ignored_directory_name(name) and not (current_path / name).is_symlink()
        ]
        for name in files:
            path = current_path / name
            if path.is_symlink() or ignored_path(path, root):
                continue
            yield path.resolve()


def load_artifacts(root: Path) -> dict[Path, Artifact]:
    artifacts: dict[Path, Artifact] = {}
    addresses: dict[str, Path] = {}
    uids: dict[str, Path] = {}
    for path in sorted(walk_files(root), key=lambda p: repo_path(root, p).casefold()):
        if path.suffix.lower() not in SUPPORTED_SUFFIXES:
            continue
        extracted = extract_metadata(path)
        if extracted is None:
            continue
        metadata, body, title = extracted
        address = address_for(root, path)
        ordinal = None if path.name == "INDEX.md" else ordinal_from_name(path.name)
        uid = metadata.get("uid")
        if uid is not None:
            if not isinstance(uid, str) or not UID_RE.fullmatch(uid):
                raise CompilerError(
                    f"{repo_path(root, path)}: uid must be six Crockford Base32 characters"
                )
            previous_uid = uids.get(uid)
            if previous_uid is not None:
                raise CompilerError(
                    f"Duplicate uid {uid}: {repo_path(root, previous_uid)} and {repo_path(root, path)}"
                )
            uids[uid] = path
        artifact = Artifact(
            path=path,
            kind=path.suffix.lower().lstrip("."),
            metadata=metadata,
            body=body,
            title=title,
            description=description_from_metadata(metadata, path),
            address=address,
            ordinal=ordinal,
            uid=uid,
        )
        if address is not None:
            previous = addresses.get(address)
            if previous is not None:
                raise CompilerError(
                    f"Duplicate address {address}: {repo_path(root, previous) } and {repo_path(root, path)}"
                )
            addresses[address] = path
        artifacts[path] = artifact
    return artifacts


def generate_uid(used: set[str]) -> str:
    while True:
        uid = "".join(secrets.choice(UID_ALPHABET) for _ in range(6))
        if uid not in used:
            return uid


def source_offset(lines: list[str], position: tuple[int, int]) -> int:
    line, column = position
    return sum(len(part) for part in lines[: line - 1]) + column


def add_uid_to_metadata(path: Path, uid: str) -> None:
    source = read_text(path)
    if path.suffix.lower() == ".md":
        if not source.startswith("---\n"):
            raise CompilerError(f"{path}: cannot add uid without Markdown frontmatter")
        path.write_text(source.replace("---\n", f"---\nuid: {uid}\n", 1), encoding="utf-8")
        return

    if path.suffix.lower() != ".py":
        raise CompilerError(f"{path}: cannot add uid to unsupported metadata surface")
    try:
        tree = ast.parse(source, filename=str(path))
    except SyntaxError as exc:
        raise CompilerError(f"Can't parse Python metadata in {path}: {exc}") from exc
    if not tree.body:
        raise CompilerError(f"{path}: cannot find Python module docstring")
    first = tree.body[0]
    if not (
        isinstance(first, ast.Expr)
        and isinstance(first.value, ast.Constant)
        and isinstance(first.value.value, str)
    ):
        raise CompilerError(f"{path}: cannot find Python module docstring")

    token = None
    for candidate in tokenize.generate_tokens(io
.StringIO(source).readline):
        if candidate.type == tokenize.STRING and candidate.start[0] == first.value.lineno:
            token = candidate
            break
    if token is None:
        raise CompilerError(f"{path}: cannot locate Python module docstring token")
    literal = token.string
    marker = "---\n"
    marker_at = literal.find(marker)
    if marker_at == -1:
        raise CompilerError(f"{path}: module docstring metadata must begin with ---")
    insert_at = marker_at + len(marker)
    new_literal = literal[:insert_at] + f"uid: {uid}\n" + literal[insert_at:]
    lines = source.splitlines(keepends=True)
    start = source_offset(lines, token.start)
    end = source_offset(lines, token.end)
    path.write_text(source[:start] + new_literal + source[end:], encoding="utf-8")


def ensure_uids(root: Path) -> int:
    artifacts = load_artifacts(root)
    used = {artifact.uid for artifact in artifacts.values() if artifact.uid is not None}
    created = 0
    for path, artifact in sorted(artifacts.items(), key=lambda pair: repo_path(root, pair[0]).casefold()):
        if artifact.uid is not None:
            continue
        uid = generate_uid(used)
        add_uid_to_metadata(path, uid)
        used.add(uid)
        created += 1
    return created


def location_addresses(root: Path) -> dict[str, Path]:
    result: dict[str, Path] = {}
    for current, dirs, _ in os.walk(root, followlinks=False):
        current_path = Path(current).resolve()
        dirs[:] = [
            name
            for name in dirs
            if not ignored_directory_name(name) and not (current_path / name).is_symlink()
        ]
        if current_path == root.resolve() or ordinal_from_name(current_path.name) is None:
            continue
        rel = current_path.relative_to(root.resolve())
        if any(part in CONTROLLED_SIDEBAND_DIRS for part in rel.parts):
            continue
        ordinals = [ordinal_from_name(part) for part in rel.parts]
        ordinals = [part for part in ordinals if part is not None]
        if not ordinals:
            continue
        address = "§" + ".".join(ordinals)
        previous = result.get(address)
        if previous is not None and previous != current_path:
            raise CompilerError(
                f"Two locations derive {address}: {repo_path(root, previous)} and {repo_path(root, current_path)}"
            )
        result[address] = current_path
    return result


def validate_sibling_ordinals(root: Path) -> None:
    for current, dirs, files in os.walk(root, followlinks=False):
        current_path = Path(current)
        dirs[:] = [
            name
            for name in dirs
            if not ignored_directory_name(name) and not (current_path / name).is_symlink()
        ]
        seen: dict[str, str] = {}
        names = dirs + [
            name for name in files if Path(name).suffix.lower() in SUPPORTED_SUFFIXES and name != "INDEX.md"
        ]
        for name in names:
            ordinal = ordinal_from_name(name)
            if ordinal is None:
                continue
            previous = seen.get(ordinal)
            if previous is not None:
                raise CompilerError(
                    f"Duplicate sibling location ordinal {ordinal} in {repo_path(root, current_path)}: "
                    f"{previous!r} and {name!r}"
                )
            seen[ordinal] = name


def address_depth(address: str) -> int:
    return len(address.removeprefix("§").split("."))


def derive_index(root: Path, artifacts: dict[Path, Artifact]) -> tuple[Path, frozenset[Path], dict[Path, frozenset[Path]], dict[Path, Path]]:
    origin = (root / "README.md").resolve()
    if origin not in artifacts:
        raise CompilerError("Corpus root must contain indexed README.md")
    immediate: dict[Path, set[Path]] = {}
    parents: dict[Path, Path] = {}
    addressed = [artifact for artifact in artifacts.values() if artifact.address is not None]

    root_children = {artifact.path for artifact in addressed if address_depth(artifact.address) == 1}
    if root_children:
        immediate[origin] = root_children
        for child in root_children:
            parents[child] = origin

    for owner in artifacts.values():
        if owner.path.name != "INDEX.md" or owner.address is None:
            continue
        prefix = owner.address + "."
        depth = address_depth(owner.address) + 1
        children = {
            artifact.path
            for artifact in addressed
            if artifact.address.startswith(prefix) and address_depth(artifact.address) == depth
        }
        if children:
            immediate[owner.path] = children
            for child in children:
                previous = parents.get(child)
                if previous is not None and previous != owner.path:
                    raise CompilerError(
                        f"{repo_path(root, child)} derives multiple index parents: "
                        f"{repo_path(root, previous)} and {repo_path(root, owner.path)}"
                    )
                parents[child] = owner.path

    frozen = {owner: frozenset(children) for owner, children in immediate.items()}
    return origin, frozenset(frozen), frozen, parents


def build_corpus(root: Path) -> Corpus:
    root = root.resolve()
    if not root.is_dir():
        raise CompilerError(f"Corpus root is not a directory: {root}")
    validate_sibling_ordinals(root)
    artifacts = load_artifacts(root)
    if not artifacts:
        raise CompilerError(f"No recognized metadata-bearing artifacts beneath {root}")
    locations = location_addresses(root)
    origin, owners, immediate, parents = derive_index(root, artifacts)
    return Corpus(
        root=root,
        address_space=ADDRESS_SPACE,
        artifacts=artifacts,
        locations=locations,
        origin=origin,
        index_owners=owners,
        immediate=immediate,
        parents=parents,
    )


def artifact_by_address(corpus: Corpus) -> dict[str, Artifact]:
    return {a.address: a for a in corpus.artifacts.values() if a.address is not None}


def artifact_by_uid(corpus: Corpus) -> dict[str, Artifact]:
    return {a.uid: a for a in corpus.artifacts.values() if a.uid is not None}


def qualified_address(corpus: Corpus, artifact: Artifact, section: str | None = None) -> str:
    if artifact.address is None:
        raise CompilerError(
            f"{repo_path(corpus.root, artifact.path)}: uid {artifact.uid} has no addressable location"
        )
    address = artifact.address
    address = f"{corpus.address_space}:{address}"
    if section is not None:
        address += f"#{section}"
    return address
