"""Own Markdown heading structure, section coordinates, fenced blocks, and local renumbering."""

from __future__ import annotations

import re
from dataclasses import dataclass

from markdown_it import MarkdownIt

NUMBERED_HEADING_RE = re.compile(
    r"^(?P<marks>#{2,6})\s+(?P<number>[0-9]+(?:\.[0-9]+)*)"
    r"(?P<trailing>\.)?\s+(?P<title>.+?)\s*$"
)
ATX_HEADING_RE = re.compile(r"^(?P<marks>#{1,6})\s+(?P<title>.+?)\s*$")
NUMBER_PREFIX_RE = re.compile(r"^\d+(?:\.\d+)*\.?\s+")
FENCE_OPEN_RE = re.compile(r"^(?P<indent> {0,3})(?P<marks>`{3,}|~{3,})(?P<info>[^\r\n]*)$")


class MarkdownError(ValueError):
    """Raised when deterministic Markdown structure cannot be established."""


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
class Section:
    selector: str
    number: str | None
    level: int
    title: str
    heading: str
    start_line: int
    content_start_line: int
    end_line: int


@dataclass(frozen=True)
class FencedBlock:
    language: str
    info: str
    fence: str
    start_line: int
    content_start_line: int
    end_line: int
    content: str


@dataclass(frozen=True)
class ParsedHeading:
    line: int
    level: int
    title: str
    inline_types: tuple[str, ...]


_PARSER = MarkdownIt("commonmark").enable(["table", "strikethrough"])


def title_from_body(body: str, fallback: str) -> str:
    for line in body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def anchor(heading: str) -> str:
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
                raw.append((number, len(marks), title, heading, anchor(heading), offset))
        offset += len(line)

    result: list[HeadingTarget] = []
    for index, (number, level, title, heading, heading_anchor, start) in enumerate(raw):
        end = len(body)
        for _, next_level, _, _, _, next_start in raw[index + 1 :]:
            if next_level <= level:
                end = next_start
                break
        result.append(HeadingTarget(number, level, title, heading, heading_anchor, start, end))
    return result


def heading_target(body: str, number: str) -> HeadingTarget:
    matches = [heading for heading in numbered_headings(body) if heading.number == number]
    if not matches:
        raise MarkdownError(f"no numbered heading resolves #{number}")
    if len(matches) > 1:
        raise MarkdownError(f"numbered heading #{number} is ambiguous")
    return matches[0]


def parsed_headings(body: str) -> list[ParsedHeading]:
    """Return parser-backed heading facts without exposing parser token objects."""
    tokens = _PARSER.parse(body)
    result: list[ParsedHeading] = []
    for index, token in enumerate(tokens):
        if token.type != "heading_open" or token.map is None:
            continue
        inline = tokens[index + 1] if index + 1 < len(tokens) else None
        if inline is None or inline.type != "inline":
            raise MarkdownError(f"heading at line {token.map[0] + 1} has no inline content token")
        children = inline.children or []
        result.append(
            ParsedHeading(
                line=token.map[0] + 1,
                level=int(token.tag[1:]),
                title=inline.content,
                inline_types=tuple(child.type for child in children),
            )
        )
    return result


def headings(body: str) -> list[dict]:
    return [
        {"line": item.line, "level": item.level, "title": item.title}
        for item in parsed_headings(body)
    ]



def sections(body: str) -> list[Section]:
    found = headings(body)
    total_lines = len(body.splitlines())
    result: list[Section] = []
    for index, item in enumerate(found):
        level = int(item["level"])
        raw_title = str(item["title"])
        number_match = NUMBER_PREFIX_RE.match(raw_title)
        number = number_match.group(0).strip().rstrip(".") if number_match else None
        title = raw_title[number_match.end():] if number_match else raw_title
        end_line = total_lines
        for candidate in found[index + 1:]:
            if int(candidate["level"]) <= level:
                end_line = int(candidate["line"]) - 1
                break
        result.append(
            Section(
                selector=number or title,
                number=number,
                level=level,
                title=title,
                heading=raw_title,
                start_line=int(item["line"]),
                content_start_line=int(item["line"]) + 1,
                end_line=end_line,
            )
        )
    return result


def resolve_section(body: str, selector: str) -> Section:
    matches = [
        section
        for section in sections(body)
        if selector in {section.selector, section.number, section.title, section.heading}
    ]
    if not matches:
        raise MarkdownError(f"no section resolves {selector!r}")
    if len(matches) > 1:
        raise MarkdownError(f"section selector {selector!r} is ambiguous")
    return matches[0]


def get_section(body: str, selector: str, *, include_heading: bool = True) -> str:
    section = resolve_section(body, selector)
    lines = body.splitlines(keepends=True)
    start = section.start_line - 1 if include_heading else section.content_start_line - 1
    return "".join(lines[start:section.end_line])


def fenced_blocks(body: str, *, language: str | None = None) -> list[FencedBlock]:
    """Return parser-backed fenced code blocks with one-based line coordinates."""
    result: list[FencedBlock] = []
    for token in _PARSER.parse(body):
        if token.type != "fence" or token.map is None:
            continue
        info = token.info.strip()
        block_language = info.split(None, 1)[0] if info else ""
        if language is not None and block_language.lower() != language.lower():
            continue
        result.append(
            FencedBlock(
                language=block_language,
                info=info,
                fence=token.markup,
                start_line=token.map[0] + 1,
                content_start_line=token.map[0] + 2,
                end_line=token.map[1],
                content=token.content,
            )
        )
    return result

def transform_prose(text: str, transform) -> tuple[str, int]:
    changed = 0
    out: list[str] = []
    in_fence = False
    fence_token: str | None = None
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
            out.append(line)
            continue
        if in_fence:
            out.append(line)
            continue

        cursor = 0
        rendered_line: list[str] = []
        while cursor < len(line):
            tick = line.find("`", cursor)
            if tick == -1:
                rendered, count = transform(line[cursor:])
                rendered_line.append(rendered)
                changed += count
                break
            rendered, count = transform(line[cursor:tick])
            rendered_line.append(rendered)
            changed += count
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

def renumber(body: str) -> tuple[str, dict[str, str]]:
    lines = body.splitlines(keepends=True)
    counters = [0, 0, 0, 0, 0]
    previous_level: int | None = None
    mapping: dict[str, str] = {}
    output: list[str] = []
    in_fence = False
    fence_token: str | None = None

    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            token = stripped[:3]
            if not in_fence:
                in_fence = True
                fence_token = token
            elif token == fence_token:
                in_fence = False
                fence_token = None
            output.append(line)
            continue
        if in_fence:
            output.append(line)
            continue

        ending = "\n" if line.endswith("\n") else ""
        raw_line = line[:-1] if ending else line
        if raw_line.endswith("\r"):
            raw_line = raw_line[:-1]
            ending = "\r\n" if ending else "\r"
        match = ATX_HEADING_RE.match(raw_line)
        if match is None:
            output.append(line)
            continue

        level = len(match.group("marks"))
        if level == 1:
            output.append(line)
            previous_level = None
            counters = [0, 0, 0, 0, 0]
            continue
        if previous_level is None and level != 2:
            raise MarkdownError(f"numbered outline begins at H{level}; expected H2")
        if previous_level is not None and level > previous_level + 1:
            raise MarkdownError(f"heading depth jumps from H{previous_level} to H{level}")

        index = level - 2
        if any(value == 0 for value in counters[:index]):
            raise MarkdownError(f"H{level} heading has no numbered parent")
        counters[index] += 1
        for deeper in range(index + 1, len(counters)):
            counters[deeper] = 0
        number = ".".join(str(value) for value in counters[: index + 1])

        title = match.group("title")
        old = NUMBER_PREFIX_RE.match(title)
        clean_title = title[old.end() :] if old else title
        punctuation = ""
        if old:
            old_prefix = old.group(0).strip()
            old_number = old_prefix.rstrip(".")
            punctuation = "." if old_prefix.endswith(".") else ""
            mapping[old_number] = number
        output.append(f"{match.group('marks')} {number}{punctuation} {clean_title}{ending}")
        previous_level = level

    return "".join(output), mapping
