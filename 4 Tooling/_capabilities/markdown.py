"""Own Markdown heading structure, section coordinates, and local renumbering."""

from __future__ import annotations

import re
from dataclasses import dataclass

NUMBERED_HEADING_RE = re.compile(
    r"^(?P<marks>#{2,6})\s+(?P<number>[0-9]+(?:\.[0-9]+)*)"
    r"(?P<trailing>\.)?\s+(?P<title>.+?)\s*$"
)
ATX_HEADING_RE = re.compile(r"^(?P<marks>#{1,6})\s+(?P<title>.+?)\s*$")
NUMBER_PREFIX_RE = re.compile(r"^\d+(?:\.\d+)*\.?\s+")


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


def headings(body: str) -> list[dict]:
    result: list[dict] = []
    in_fence = False
    fence_token: str | None = None
    for line_number, line in enumerate(body.splitlines(), start=1):
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            token = stripped[:3]
            if not in_fence:
                in_fence = True
                fence_token = token
            elif token == fence_token:
                in_fence = False
                fence_token = None
            continue
        if in_fence:
            continue
        match = ATX_HEADING_RE.match(line)
        if match:
            result.append(
                {
                    "line": line_number,
                    "level": len(match.group("marks")),
                    "title": match.group("title"),
                }
            )
    return result


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
        if old:
            old_number = old.group(0).strip().rstrip(".")
            mapping[old_number] = number
        output.append(f"{match.group('marks')} {number} {clean_title}{ending}")
        previous_level = level

    return "".join(output), mapping
