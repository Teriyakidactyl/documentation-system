#!/usr/bin/env python3
r'''---
uid: 45E225
description: >-
  `Read in full and follow when` *a Documentation System corpus may have changed
  or an address must be resolved* `to` **validate derived control state, refresh
  index blocks and controlled links, or resolve the requested
  address without hand-maintaining indexes**.
quadrant: HowTo
---
# 🛠️ Navigation Crawler


Run this tool after classification, indexed metadata, numbered headings, or
controlled links may have changed. The filesystem is the authoritative
classification hierarchy. Each indexed artifact contributes one canonical
Markdown `description`; indexes are derived from immediate filesystem children
rather than authored navigation metadata, and traversing successive indexes
provides progressive disclosure.

A location ordinal is read from the beginning of a numbered directory or
numbered artifact name. Both `9 Name` and `9. Name` are accepted. Numbered
directories contribute hierarchical address components. `INDEX.md` represents
its containing location without adding another component. A numbered artifact
adds the terminal component. Unnumbered directories are address-transparent.
A numbered heading extends an address after `#`; `SKILL.md#name` qualifies the
address space when a reference must remain unambiguous outside this corpus.

The crawler currently recognizes YAML frontmatter in Markdown and YAML
frontmatter at the start of a Python module docstring. Dot-prefixed
directories are outside the corpus and are never traversed. Other source
formats can be added as metadata adapters without changing the normalized
model. Every indexed artifact must carry a non-empty `description`. On a normal
compile the crawler mints any missing `uid` as six Crockford Base32 characters;
an existing UID is permanent and duplicates are errors.

`README.md` represents the origin and projects the immediate indexed items at
the crawler root. Each `INDEX.md` with immediate indexed children projects only
those children. The generated choices belong between `<!-- BEGIN index -->` and
`<!-- END index -->`; the marker name is only a generated region
demarcation. Each rendered choice reuses the child's exact
`description`. No authored child list is read.

A controlled link is an HTML anchor carrying `uid`. Authors may write
`<a href="*" uid="5CFFZW">documentation-system:§2.1#4.2</a>`. Every compile
pass uses only the UID to identify the current document, preserves and validates
the optional section number, then rewrites the displayed qualified address and
`href`. Ordinary Markdown links are untouched. The same rule applies in Markdown
frontmatter and inside a Python module docstring. Address semantics are defined by
<a href="../1%20Document%20Control/1%20%F0%9F%9B%A0%EF%B8%8F%20Control%20Documented%20Information.md#3-derive-and-use-addresses" uid="0AQHNH">documentation-system:§1.1#3</a>.

Usage:
    python3 "4 Tooling/1 🛠️ Navigation Crawler.py" [crawler_root]
    python3 "4 Tooling/1 🛠️ Navigation Crawler.py" --resolve documentation-system:§2.1#4.2 [crawler_root]

When `crawler_root` is omitted, the script walks upward to the nearest
`SKILL.md`; its containing directory is the intended root and its `name`
qualifies controlled addresses. This lets the tool live inside the ordinal
Tooling location while still dogfooding the corpus it controls. `--resolve` is
read-only and returns JSON containing the address, UID, description, path, body,
ordinal, and parent index when one exists. A `#` address returns the numbered
heading and the body it governs.

Requires PyYAML.
'''

from __future__ import annotations

import ast
import io
import json
import os
import re
import secrets
import sys
import tokenize
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote

try:
    import yaml
except ImportError as exc:  # pragma: no cover - environmental failure
    raise SystemExit("navigation crawler requires PyYAML") from exc


BEGIN = "<!-- BEGIN index -->"
END = "<!-- END index -->"
IGNORED_DIRS = {"__pycache__"}
SUPPORTED_SUFFIXES = {".md", ".py"}
LOCATION_ORDINAL_RE = re.compile(r"^([0-9]+)(?:\.\s+|\s+)")
ADDRESS_RE = re.compile(
    r"^(?:(?P<space>[a-z0-9][a-z0-9-]*):)?"
    r"(?P<location>§[0-9]+(?:\.[0-9]+)*)"
    r"(?:#(?P<section>[0-9]+(?:\.[0-9]+)*))?$"
)
UID_ALPHABET = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"
UID_RE = re.compile(r"^[0123456789ABCDEFGHJKMNPQRSTVWXYZ]{6}$")
CONTROL_LINK_RE = re.compile(
    r'<a\b(?P<attrs>[^>\n]*?\buid="(?P<uid>[^"]+)"[^>\n]*?)>'
    r'(?P<label>[^<\n]+)</a>'
)
NUMBERED_HEADING_RE = re.compile(
    r"^(?P<marks>#{2,6})\s+(?P<number>[0-9]+(?:\.[0-9]+)*)(?P<trailing>\.)?\s+(?P<title>.+?)\s*$"
)
SKILL_NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")


class CrawlError(RuntimeError):
    """Raised when the corpus cannot compile deterministically."""


@dataclass(frozen=True)
class Item:
    path: Path
    kind: str
    metadata: dict
    body: str
    title: str
    description: str
    address: str | None
    ordinal: str | None
    uid: str | None


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise CrawlError(f"Can't read {path}: {exc}") from exc


def repo_path(root: Path, path: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def find_crawler_root(script: Path) -> Path:
    for directory in (script.resolve().parent, *script.resolve().parents):
        if (directory / "SKILL.md").is_file():
            return directory
    return script.resolve().parent


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
        raise CrawlError(f"Invalid YAML metadata in {owner}: {exc}") from exc
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise CrawlError(f"{owner}: metadata must be a mapping")
    return data


def address_space_name(root: Path) -> str | None:
    skill = root / "SKILL.md"
    if not skill.is_file():
        return None
    text = read_text(skill)
    split = split_frontmatter(text)
    if split is None:
        raise CrawlError(f"{skill}: SKILL.md must begin with YAML frontmatter")
    raw, _ = split
    metadata = parse_yaml_mapping(raw, skill)
    name = metadata.get("name")
    if not isinstance(name, str) or not SKILL_NAME_RE.fullmatch(name):
        raise CrawlError(
            f"{skill}: skill name must match {SKILL_NAME_RE.pattern!r} to qualify addresses"
        )
    return name


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


def python_adapter(path: Path) -> tuple[dict, str, str] | None:
    text = read_text(path)
    try:
        tree = ast.parse(text, filename=str(path))
    except SyntaxError as exc:
        raise CrawlError(f"Can't parse Python metadata in {path}: {exc}") from exc
    doc = ast.get_docstring(tree, clean=False)
    if not doc:
        return None
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
        raise CrawlError(f"{owner}: description must be a non-empty Markdown scalar")
    return clean(value)

def ordinal_from_name(name: str) -> str | None:
    match = LOCATION_ORDINAL_RE.match(name)
    return match.group(1) if match else None


def address_components(root: Path, path: Path) -> list[str]:
    rel = path.resolve().relative_to(root.resolve())
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


@dataclass(frozen=True)
class HeadingTarget:
    number: str
    level: int
    title: str
    heading: str
    anchor: str
    start: int
    end: int


def markdown_anchor(heading: str) -> str:
    """Render the heading fragment used by common Markdown/GitHub-style renderers."""
    value = heading.strip().lower()
    value = re.sub(r"<[^>]+>", "", value)
    value = re.sub(r"[^\w\- ]", "", value, flags=re.UNICODE)
    value = re.sub(r"\s+", "-", value)
    return value


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
        raise CrawlError(f"{owner}: no numbered heading resolves #{number}")
    if len(matches) > 1:
        raise CrawlError(f"{owner}: numbered heading #{number} is ambiguous")
    return matches[0]


def parse_address(address: str, address_space: str | None) -> tuple[str, str | None]:
    match = ADDRESS_RE.fullmatch(address)
    if not match:
        raise CrawlError(f"Invalid address: {address!r}")
    qualifier = match.group("space")
    if qualifier is not None and qualifier != address_space:
        expected = address_space or "<unqualified corpus>"
        raise CrawlError(
            f"Address {address!r} names address space {qualifier!r}; current space is {expected!r}"
        )
    return match.group("location"), match.group("section")


def ignored_directory_name(name: str) -> bool:
    return name.startswith(".") or name in IGNORED_DIRS or name.startswith("old_")


def ignored_path(path: Path, root: Path) -> bool:
    try:
        rel = path.resolve().relative_to(root.resolve())
    except ValueError:
        return True
    return (
        any(ignored_directory_name(part) for part in rel.parts[:-1])
        or path.name.startswith("old_")
    )


def walk_files(root: Path):
    for current, dirs, files in os.walk(root, followlinks=False):
        current_path = Path(current)
        dirs[:] = [
            name
            for name in dirs
            if not ignored_directory_name(name)
            and not (current_path / name).is_symlink()
        ]
        for name in files:
            path = current_path / name
            if path.is_symlink() or ignored_path(path, root):
                continue
            yield path.resolve()


def load_items(root: Path) -> dict[Path, Item]:
    items: dict[Path, Item] = {}
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
                raise CrawlError(
                    f"{repo_path(root, path)}: uid must be six Crockford Base32 characters"
                )
            previous_uid = uids.get(uid)
            if previous_uid is not None:
                raise CrawlError(
                    f"Duplicate uid {uid}: {repo_path(root, previous_uid)} and "
                    f"{repo_path(root, path)}"
                )
            uids[uid] = path
        item = Item(
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
                raise CrawlError(
                    f"Duplicate address {address}: {repo_path(root, previous)} and "
                    f"{repo_path(root, path)}"
                )
            addresses[address] = path
        items[path] = item
    return items


def generate_uid(used: set[str]) -> str:
    while True:
        uid = "".join(secrets.choice(UID_ALPHABET) for _ in range(6))
        if uid not in used:
            return uid


def add_uid_to_metadata(path: Path, uid: str) -> None:
    source = read_text(path)
    if path.suffix.lower() == ".md":
        if not source.startswith("---\n"):
            raise CrawlError(f"{path}: cannot add uid without Markdown frontmatter")
        path.write_text(
            source.replace("---\n", f"---\nuid: {uid}\n", 1),
            encoding="utf-8",
        )
        return

    if path.suffix.lower() != ".py":
        raise CrawlError(f"{path}: cannot add uid to unsupported metadata surface")
    try:
        tree = ast.parse(source, filename=str(path))
    except SyntaxError as exc:
        raise CrawlError(f"Can't parse Python metadata in {path}: {exc}") from exc
    if not tree.body:
        raise CrawlError(f"{path}: cannot find Python module docstring")
    first = tree.body[0]
    if not (
        isinstance(first, ast.Expr)
        and isinstance(first.value, ast.Constant)
        and isinstance(first.value.value, str)
    ):
        raise CrawlError(f"{path}: cannot find Python module docstring")

    token = None
    for candidate in tokenize.generate_tokens(io.StringIO(source).readline):
        if candidate.type == tokenize.STRING and candidate.start[0] == first.value.lineno:
            token = candidate
            break
    if token is None:
        raise CrawlError(f"{path}: cannot locate Python module docstring token")

    literal = token.string
    marker = "---\n"
    marker_at = literal.find(marker)
    if marker_at == -1:
        raise CrawlError(f"{path}: module docstring metadata must begin with ---")
    insert_at = marker_at + len(marker)
    new_literal = literal[:insert_at] + f"uid: {uid}\n" + literal[insert_at:]
    lines = source.splitlines(keepends=True)
    start = source_offset(lines, token.start)
    end = source_offset(lines, token.end)
    path.write_text(source[:start] + new_literal + source[end:], encoding="utf-8")


def ensure_uids(root: Path) -> int:
    items = load_items(root)
    used = {item.uid for item in items.values() if item.uid is not None}
    created = 0
    for path, item in sorted(
        items.items(), key=lambda pair: repo_path(root, pair[0]).casefold()
    ):
        if item.uid is not None:
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
            if not ignored_directory_name(name)
            and not (current_path / name).is_symlink()
        ]
        if current_path == root.resolve():
            continue
        rel = current_path.relative_to(root.resolve())
        components = [ordinal_from_name(part) for part in rel.parts]
        ordinals = [part for part in components if part is not None]
        if not ordinals:
            continue
        address = "§" + ".".join(ordinals)
        previous = result.get(address)
        if previous is not None and previous != current_path:
            raise CrawlError(
                f"Two locations derive {address}: {repo_path(root, previous)} and "
                f"{repo_path(root, current_path)}"
            )
        result[address] = current_path
    return result


def validate_sibling_ordinals(root: Path) -> None:
    for current, dirs, files in os.walk(root, followlinks=False):
        current_path = Path(current)
        dirs[:] = [
            name
            for name in dirs
            if not ignored_directory_name(name)
            and not (current_path / name).is_symlink()
        ]
        seen: dict[str, str] = {}
        names = dirs + [
            name
            for name in files
            if Path(name).suffix.lower() in SUPPORTED_SUFFIXES and name != "INDEX.md"
        ]
        for name in names:
            ordinal = ordinal_from_name(name)
            if ordinal is None:
                continue
            previous = seen.get(ordinal)
            if previous is not None:
                raise CrawlError(
                    f"Duplicate sibling location ordinal {ordinal} in "
                    f"{repo_path(root, current_path)}: {previous!r} and {name!r}"
                )
            seen[ordinal] = name


def address_depth(address: str) -> int:
    return len(address.removeprefix("§").split("."))


def derived_index(root: Path, items: dict[Path, Item]) -> dict:
    """Derive reader-facing immediate choices from the filesystem address tree."""
    origin = (root / "README.md").resolve()
    if origin not in items:
        raise CrawlError("Crawler root must contain indexed README.md")

    immediate: dict[Path, set[Path]] = {}
    parent_map: dict[Path, Path] = {}

    addressed = [item for item in items.values() if item.address is not None]

    root_children = {item.path for item in addressed if address_depth(item.address) == 1}
    if root_children:
        immediate[origin] = root_children
        for child in root_children:
            parent_map[child] = origin

    for owner in items.values():
        if owner.path.name != "INDEX.md" or owner.address is None:
            continue
        prefix = owner.address + "."
        depth = address_depth(owner.address) + 1
        children = {
            item.path
            for item in addressed
            if item.address.startswith(prefix) and address_depth(item.address) == depth
        }
        if children:
            immediate[owner.path] = children
            for child in children:
                previous = parent_map.get(child)
                if previous is not None and previous != owner.path:
                    raise CrawlError(
                        f"{repo_path(root, child)} derives multiple index parents: "
                        f"{repo_path(root, previous)} and {repo_path(root, owner.path)}"
                    )
                parent_map[child] = owner.path

    return {
        "origin": origin,
        "projection_owners": set(immediate),
        "immediate": immediate,
        "parents": parent_map,
    }

def live_marker_offsets(text: str) -> tuple[list[int], list[int]]:
    """Return BEGIN/END offsets outside fenced Markdown code blocks."""
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


def validate_generated_regions(root: Path, items: dict[Path, Item], projection_owners: set[Path]) -> None:
    for path, item in items.items():
        if item.kind != "md":
            if path in projection_owners:
                raise CrawlError(
                    f"{repo_path(root, path)}: a Python item cannot render an index region"
                )
            continue
        begins, ends = live_marker_offsets(read_text(path))
        if path in projection_owners:
            if len(begins) != 1 or len(ends) != 1 or ends[0] < begins[0]:
                raise CrawlError(
                    f"{repo_path(root, path)}: index owner must contain exactly one "
                    f"{BEGIN} ... {END} region outside fenced code"
                )
        elif begins or ends:
            raise CrawlError(
                f"{repo_path(root, path)}: index region exists but "
                "the filesystem derives no immediate indexed children"
            )


def relative_link(from_path: Path, to_path: Path) -> str:
    relative = os.path.relpath(to_path, start=from_path.parent)
    return quote(Path(relative).as_posix(), safe="/@")


def generated_notice(root: Path, script: Path) -> str:
    return (
        "<!-- This block was created by running `"
        + repo_path(root, script)
        + "`; run it whenever indexed information or classification may have changed. -->"
    )


def render_index(
    root: Path,
    owner: Path,
    children: set[Path],
    items: dict[Path, Item],
    script: Path,
    address_space: str | None,
) -> str:
    lines = [generated_notice(root, script), ""]
    ordered = sorted(
        children,
        key=lambda path: (
            tuple(int(part) for part in items[path].address[1:].split(".")) if items[path].address else (10**9,),
            repo_path(root, path).casefold(),
        ),
    )
    for path in ordered:
        item = items[path]
        if item.uid is None:
            raise CrawlError(f"{repo_path(root, path)}: indexed child has no uid")
        label = (
            f"{address_space}:{item.address}"
            if address_space is not None and item.address is not None
            else item.address or item.title
        )
        lines.append(
            f'- <a href="{relative_link(owner, path)}" uid="{item.uid}">{label}</a> — {item.title}'
        )
        lines.append(f"  - {item.description}")
    return "\n".join(lines).rstrip()


def replace_region(path: Path, content: str) -> None:
    text = read_text(path)
    begins, ends = live_marker_offsets(text)
    if len(begins) != 1 or len(ends) != 1:
        raise CrawlError(f"{path}: expected one live index region")
    start = begins[0] + len(BEGIN)
    stop = ends[0]
    replacement = f"{text[:start]}\n{content}\n{text[stop:]}"
    if replacement != text:
        path.write_text(replacement, encoding="utf-8")


def build_model(root: Path) -> dict:
    root = root.resolve()
    if not root.is_dir():
        raise CrawlError(f"Crawler root is not a directory: {root}")
    validate_sibling_ordinals(root)
    items = load_items(root)
    if not items:
        raise CrawlError(f"No recognized metadata-bearing artifacts beneath {root}")
    locations = location_addresses(root)
    index_model = derived_index(root, items)
    return {
        "root": root,
        "address_space": address_space_name(root),
        "items": items,
        "locations": locations,
        **index_model,
    }


def item_by_address(model: dict) -> dict[str, Item]:
    return {
        item.address: item
        for item in model["items"].values()
        if item.address is not None
    }


def item_by_uid(model: dict) -> dict[str, Item]:
    return {item.uid: item for item in model["items"].values() if item.uid is not None}


def qualified_address(model: dict, item: Item, section: str | None = None) -> str:
    if item.address is None:
        raise CrawlError(
            f"{repo_path(model['root'], item.path)}: uid {item.uid} has no addressable location"
        )
    address = item.address
    if model["address_space"] is not None:
        address = f"{model['address_space']}:{address}"
    if section is not None:
        address += f"#{section}"
    return address


def resolve_target(model: dict, address: str) -> tuple[Item, HeadingTarget | None]:
    location, section = parse_address(address, model["address_space"])
    item = item_by_address(model).get(location)
    if item is None:
        location_path = model["locations"].get(location)
        if location_path is not None:
            raise CrawlError(
                f"{address}: {location} is a location with no indexed body; add INDEX.md before linking to it"
            )
        raise CrawlError(f"No indexed document or location resolves from {address}")
    heading = heading_target(item.body, section, item.path) if section else None
    return item, heading


def render_control_link(root: Path, owner: Path, model: dict, uid: str, label: str) -> str:
    if not UID_RE.fullmatch(uid):
        raise CrawlError(f"{repo_path(root, owner)}: invalid controlled-link uid {uid!r}")
    item = item_by_uid(model).get(uid)
    if item is None:
        raise CrawlError(
            f"{repo_path(root, owner)}: controlled link names missing uid {uid}"
        )
    match = ADDRESS_RE.fullmatch(label.strip())
    if match is None:
        raise CrawlError(
            f"{repo_path(root, owner)}: controlled link uid {uid} must display a documentation address"
        )
    qualifier = match.group("space")
    if qualifier is not None and qualifier != model["address_space"]:
        raise CrawlError(
            f"{repo_path(root, owner)}: controlled link uid {uid} names address space "
            f"{qualifier!r}, not {model['address_space']!r}"
        )
    section = match.group("section")
    heading = heading_target(item.body, section, item.path) if section else None
    href = relative_link(owner, item.path)
    if heading is not None:
        href += "#" + quote(heading.anchor, safe="-._~")
    rendered_label = qualified_address(model, item, section)
    return f'<a href="{href}" uid="{uid}">{rendered_label}</a>'


def rewrite_control_links_in_markdown(
    body: str, root: Path, owner: Path, model: dict
) -> tuple[str, int]:
    changed = 0
    out: list[str] = []
    in_fence = False
    fence_token: str | None = None
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
            out.append(line)
            continue
        if in_fence:
            out.append(line)
            continue

        def replace(match: re.Match[str]) -> str:
            nonlocal changed
            rendered = render_control_link(
                root, owner, model, match.group("uid"), match.group("label")
            )
            if rendered != match.group(0):
                changed += 1
            return rendered

        # Code spans are examples, not live controlled links.
        cursor = 0
        rendered_line: list[str] = []
        while cursor < len(line):
            tick = line.find("`", cursor)
            if tick == -1:
                rendered_line.append(CONTROL_LINK_RE.sub(replace, line[cursor:]))
                break
            rendered_line.append(CONTROL_LINK_RE.sub(replace, line[cursor:tick]))
            run_end = tick
            while run_end < len(line) and line[run_end] == "`":
                run_end += 1
            delimiter = line[tick:run_end]
            close = line.find(delimiter, run_end)
            if close == -1:
                rendered_line.append(line[tick:])
                break
            close_end = close + len(delimiter)
            rendered_line.append(line[tick:close_end])
            cursor = close_end
        out.append("".join(rendered_line))
    return "".join(out), changed


def rewrite_markdown_control_links(path: Path, root: Path, model: dict) -> int:
    text = read_text(path)
    rewritten, changed = rewrite_control_links_in_markdown(text, root, path, model)
    if changed:
        path.write_text(rewritten, encoding="utf-8")
    return changed


def source_offset(lines: list[str], position: tuple[int, int]) -> int:
    line, column = position
    return sum(len(part) for part in lines[: line - 1]) + column


def rewrite_python_control_links(path: Path, root: Path, model: dict) -> int:
    source = read_text(path)
    try:
        tree = ast.parse(source, filename=str(path))
    except SyntaxError as exc:
        raise CrawlError(f"Can't parse Python documentation in {path}: {exc}") from exc
    if not tree.body:
        return 0
    first = tree.body[0]
    if not (
        isinstance(first, ast.Expr)
        and isinstance(first.value, ast.Constant)
        and isinstance(first.value.value, str)
    ):
        return 0

    token = None
    for candidate in tokenize.generate_tokens(io.StringIO(source).readline):
        if candidate.type == tokenize.STRING and candidate.start[0] == first.value.lineno:
            token = candidate
            break
    if token is None:
        return 0

    literal = token.string
    prefix_match = re.match(r"(?i)^([rub]*)", literal)
    prefix = prefix_match.group(1) if prefix_match else ""
    rest = literal[len(prefix) :]
    quote_mark = None
    for candidate_quote in ("'''", '"""'):
        if rest.startswith(candidate_quote) and rest.endswith(candidate_quote):
            quote_mark = candidate_quote
            break
    if quote_mark is None:
        return 0
    body = rest[len(quote_mark) : -len(quote_mark)]
    rewritten, changed = rewrite_control_links_in_markdown(body, root, path, model)
    if not changed:
        return 0
    new_literal = prefix + quote_mark + rewritten + quote_mark
    lines = source.splitlines(keepends=True)
    start = source_offset(lines, token.start)
    end = source_offset(lines, token.end)
    path.write_text(source[:start] + new_literal + source[end:], encoding="utf-8")
    return changed


def rewrite_control_links(root: Path, model: dict) -> int:
    changed = 0
    for path in sorted(walk_files(root), key=lambda p: repo_path(root, p).casefold()):
        suffix = path.suffix.lower()
        if suffix == ".md":
            changed += rewrite_markdown_control_links(path, root, model)
        elif suffix == ".py":
            changed += rewrite_python_control_links(path, root, model)
    return changed


def compile_corpus(root: Path, script: Path) -> tuple[int, int, int, int]:
    minted = ensure_uids(root)
    model = build_model(root)
    validate_generated_regions(root, model["items"], model["projection_owners"])
    for owner in sorted(model["projection_owners"], key=lambda p: repo_path(root, p).casefold()):
        content = render_index(
            root,
            owner,
            model["immediate"][owner],
            model["items"],
            script,
            model["address_space"],
        )
        replace_region(owner, content)
    model = build_model(root)
    links = rewrite_control_links(root, model)
    return len(model["items"]), len(model["locations"]), links, minted


def resolve_address(root: Path, address: str) -> dict:
    model = build_model(root)
    location, section = parse_address(address, model["address_space"])
    by_address = item_by_address(model)
    item = by_address.get(location)
    if item is not None:
        parent = model["parents"].get(item.path)
        result = {
            "address": address,
            "address_space": model["address_space"],
            "type": "document" if item.path.name != "INDEX.md" else "location-index",
            "path": repo_path(root, item.path),
            "parent_index": repo_path(root, parent) if parent else None,
            "location_ordinal": item.ordinal,
            "uid": item.uid,
            "title": item.title,
            "description": item.description,
            "body": item.body,
        }
        if section is not None:
            heading = heading_target(item.body, section, item.path)
            result.update(
                {
                    "section": section,
                    "heading": heading.heading,
                    "body": item.body[heading.start : heading.end].rstrip() + "\n",
                }
            )
        return result
    location_path = model["locations"].get(location)
    if location_path is not None and section is None:
        return {
            "address": address,
            "address_space": model["address_space"],
            "type": "location",
            "path": repo_path(root, location_path) + "/",
            "index": None,
            "body": None,
        }
    if location_path is not None:
        raise CrawlError(f"{address}: location has no indexed body to resolve #{section}")
    raise CrawlError(f"No indexed document or location resolves from {address}")

def usage(script: Path) -> str:
    return (
        f'Usage:\n  python3 "{script.name}" [crawler_root]\n'
        f'  python3 "{script.name}" --resolve documentation-system:§2.1#4.2 [crawler_root]'
    )


def main() -> None:
    script = Path(__file__).resolve()
    args = sys.argv[1:]
    resolve: str | None = None
    positional: list[str] = []
    index = 0
    while index < len(args):
        arg = args[index]
        if arg == "--resolve":
            if index + 1 >= len(args):
                raise CrawlError("--resolve requires an address")
            resolve = args[index + 1]
            index += 2
        elif arg in {"-h", "--help"}:
            print(usage(script))
            return
        else:
            positional.append(arg)
            index += 1
    if len(positional) > 1:
        raise CrawlError(usage(script))
    root = Path(positional[0]).resolve() if positional else find_crawler_root(script)

    if resolve is not None:
        print(json.dumps(resolve_address(root, resolve), indent=2, ensure_ascii=False))
        return

    items, locations, links, minted = compile_corpus(root, script)
    print(
        f"Compiled {items} indexed artifacts across {locations} addressed locations "
        f"beneath {root}; minted {minted} uids and refreshed {links} controlled links"
    )


if __name__ == "__main__":
    try:
        main()
    except CrawlError as exc:
        raise SystemExit(f"navigation crawler: {exc}") from exc
