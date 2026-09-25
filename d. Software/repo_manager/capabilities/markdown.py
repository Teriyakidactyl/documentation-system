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


@dataclass(frozen=True)
class HeadingComment:
    section: Section
    start_line: int
    end_line: int
    content: str


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


def heading_comments(body: str) -> list[HeadingComment]:
    """Return HTML comments placed immediately beneath heading lines."""
    lines = body.splitlines(keepends=True)
    result: list[HeadingComment] = []
    for section in sections(body):
        index = section.start_line
        if index >= len(lines) or not lines[index].lstrip().startswith("<!--"):
            continue
        parts: list[str] = []
        end_line: int | None = None
        for candidate in range(index, min(section.end_line, len(lines))):
            parts.append(lines[candidate])
            if "-->" in lines[candidate]:
                end_line = candidate + 1
                break
        if end_line is None:
            raise MarkdownError(
                f"unclosed HTML comment beneath heading at line {section.start_line}"
            )
        raw = "".join(parts)
        start = raw.find("<!--")
        end = raw.find("-->", start + 4)
        if start == -1 or end == -1:
            continue
        result.append(
            HeadingComment(
                section=section,
                start_line=index + 1,
                end_line=end_line,
                content=raw[start + 4 : end].strip(),
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

from pathlib import Path
from typing import Any, Mapping

from repo_manager.capabilities.frontmatter import FrontmatterError, load as load_frontmatter
from repo_manager.capabilities.markdown_lint import MarkdownLintError, fix_file, lint_file, rule_policy
from repo_manager.capabilities.yaml import YamlError
from repo_manager.core import (
    Diagnostic, Effects, ExpectedFailure, Failure, Field, InputSchema, Operation,
    Probe, Result, Severity, Source, Verification, invoke, register,
)

OWNER=Source("repo_manager.capabilities.markdown","d. Software/repo_manager/capabilities/markdown.py")
MARKDOWN=Source("repo_manager.capabilities.markdown","d. Software/repo_manager/capabilities/markdown.py")
LINT=Source("repo_manager.capabilities.markdown_lint","d. Software/repo_manager/capabilities/markdown_lint.py")
FRONTMATTER=Source("repo_manager.capabilities.frontmatter","d. Software/repo_manager/capabilities/frontmatter.py")
YAML=Source("repo_manager.capabilities.yaml","d. Software/repo_manager/capabilities/yaml.py")

def _chain(exc: BaseException):
    current=exc
    while current is not None:
        yield current
        current=current.__cause__

def _expected(exc: BaseException, path: Path, fallback: Source, symbol: str) -> ExpectedFailure:
    chain=list(_chain(exc))
    if any(isinstance(item,YamlError) for item in chain):
        origin=Source(YAML.module,YAML.file,"parse_mapping")
        name="YAML_ERROR"; classification="malformed"
        provenance=("frontmatter.load",)
    elif any(isinstance(item,FrontmatterError) for item in chain):
        origin=Source(FRONTMATTER.module,FRONTMATTER.file,"load")
        name="FRONTMATTER_ERROR"; classification="invalid-frontmatter"
        provenance=()
    elif any(isinstance(item,MarkdownError) for item in chain):
        origin=Source(MARKDOWN.module,MARKDOWN.file,symbol)
        name="MARKDOWN_ERROR"; classification="invalid-markdown"
        provenance=()
    elif any(isinstance(item,MarkdownLintError) for item in chain):
        origin=Source(LINT.module,LINT.file,symbol)
        name="MARKDOWN_LINT_ERROR"; classification="lint-failure"
        provenance=()
    else:
        origin=fallback
        name="READ_FAILED"; classification="unreadable"
        provenance=()
    return ExpectedFailure(Failure(
        origin=origin,name=name,classification=classification,
        subject={"path":str(path)},message=str(exc),
        details={"exception_type":type(exc).__name__},provenance=provenance,
    ))

def _body(path: Path) -> tuple[str,str]:
    try:
        source=path.read_text(encoding="utf-8")
        frontmatter=load_frontmatter(path)
    except (OSError,FrontmatterError) as exc:
        raise _expected(exc,path,OWNER,"load") from exc
    if frontmatter is None:
        return "",source
    if not source.endswith(frontmatter.body):
        raise ExpectedFailure(Failure(
            origin=FRONTMATTER,name="BODY_PRESERVATION_FAILED",
            classification="invalid-frontmatter",subject={"path":str(path)},
            message="frontmatter extraction did not preserve the Markdown body",
        ))
    return source[:len(source)-len(frontmatter.body)],frontmatter.body

def _headings(inputs: Mapping[str,Any]) -> Result[Any]:
    path=Path(str(inputs["path"]))
    _,text=_body(path)
    try:
        return Result.success(headings(text))
    except MarkdownError as exc:
        raise _expected(exc,path,MARKDOWN,"headings") from exc

def _sections(inputs: Mapping[str,Any]) -> Result[Any]:
    path=Path(str(inputs["path"]))
    _,text=_body(path)
    try:
        return Result.success([item.__dict__ for item in sections(text)])
    except MarkdownError as exc:
        raise _expected(exc,path,MARKDOWN,"sections") from exc

def _get_section(inputs: Mapping[str,Any]) -> Result[Any]:
    path=Path(str(inputs["path"]))
    _,text=_body(path)
    try:
        return Result.success(get_section(text,str(inputs["selector"]),include_heading=not bool(inputs["no_heading"])))
    except MarkdownError as exc:
        raise _expected(exc,path,MARKDOWN,"get_section") from exc

def _canonical_diagnostics(path: Path, observed) -> tuple[Diagnostic,...]:
    result=[]
    for item in observed:
        origin=Source(LINT.module,LINT.file,"lint_file")
        result.append(Diagnostic(
            code=item.code,severity=Severity.ERROR,message=item.message,
            subject={"path":str(path),"line":item.line,"column":item.column},
            origin=origin,details={"fixable":item.fixable,"source":item.source},
        ))
    return tuple(result)

def _lint(inputs: Mapping[str,Any]) -> Result[Any]:
    path=Path(str(inputs["path"]))
    try:
        observed=lint_file(path)
    except (MarkdownLintError,FrontmatterError,OSError) as exc:
        raise _expected(exc,path,LINT,"lint_file") from exc
    payload={"path":str(path),"diagnostics":[item.to_dict() for item in observed]}
    return Result.success(payload,diagnostics=_canonical_diagnostics(path,observed))

def _fix(inputs: Mapping[str,Any]) -> Result[Any]:
    path=Path(str(inputs["path"]))
    try:
        observed,changed=fix_file(path)
    except (MarkdownLintError,FrontmatterError,OSError) as exc:
        raise _expected(exc,path,LINT,"fix_file") from exc
    payload={"path":str(path),"changed":changed,"diagnostics":[item.to_dict() for item in observed]}
    return Result.success(payload,diagnostics=_canonical_diagnostics(path,observed))

def _rules(inputs: Mapping[str,Any]) -> Result[Any]:
    return Result.success(rule_policy())

def _renumber(inputs: Mapping[str,Any]) -> Result[Any]:
    path=Path(str(inputs["path"]))
    prefix,text=_body(path)
    try:
        rendered,mapping=renumber(text)
    except MarkdownError as exc:
        raise _expected(exc,path,MARKDOWN,"renumber") from exc
    changed=rendered!=text
    if bool(inputs["write"]) and changed:
        try:
            path.write_text(prefix+rendered,encoding="utf-8")
        except OSError as exc:
            raise _expected(exc,path,OWNER,"renumber") from exc
    return Result.success({"changed":changed,"mapping":mapping,"written":bool(inputs["write"])})

MARKDOWN_HEADINGS=register(Operation(
    id="markdown.headings",commands=(("markdown","headings"),),owner=Source(OWNER.module,OWNER.file,"headings"),
    input_schema=InputSchema((Field("path","path",example="fixture.md"),)),handler=_headings,
    effects=Effects(filesystem="read"),verification=Verification(probes=(
        Probe(name="headings",fixture_input="path",fixture_content="# Title\n\n## 1. First\n\nBody.\n",fixture_suffix=".md"),
    )),
))
MARKDOWN_SECTIONS=register(Operation(
    id="markdown.sections",commands=(("markdown","sections"),),owner=Source(OWNER.module,OWNER.file,"sections"),
    input_schema=InputSchema((Field("path","path",example="fixture.md"),)),handler=_sections,
    effects=Effects(filesystem="read"),verification=Verification(probes=(
        Probe(name="sections",fixture_input="path",fixture_content="# Title\n\n## 1. First\n\nBody.\n",fixture_suffix=".md"),
    )),
))
MARKDOWN_GET_SECTION=register(Operation(
    id="markdown.get-section",commands=(("markdown","get-section"),),owner=Source(OWNER.module,OWNER.file,"get_section"),
    input_schema=InputSchema((
        Field("path","path",example="fixture.md"),
        Field("selector","string",example="1"),
        Field("no_heading","boolean",required=False,default=False),
    )),handler=_get_section,effects=Effects(filesystem="read"),verification=Verification(probes=(
        Probe(name="get-section",inputs={"selector":"1","no_heading":False},fixture_input="path",fixture_content="# Title\n\n## 1. First\n\nBody.\n",fixture_suffix=".md"),
    )),
))
MARKDOWN_LINT=register(Operation(
    id="markdown.lint",commands=(("markdown","lint"),),owner=Source(OWNER.module,OWNER.file,"lint"),
    input_schema=InputSchema((Field("path","path",example="fixture.md"),)),handler=_lint,
    effects=Effects(filesystem="read"),verification=Verification(probes=(
        Probe(name="lint",fixture_input="path",fixture_content="# Title\n\n## First\n\nBody.\n",fixture_suffix=".md"),
    )),
))
MARKDOWN_FIX=register(Operation(
    id="markdown.fix",commands=(("markdown","fix"),),owner=Source(OWNER.module,OWNER.file,"fix"),
    input_schema=InputSchema((Field("path","path",example="fixture.md"),)),handler=_fix,
    effects=Effects(filesystem="write"),verification=Verification(probes=(
        Probe(name="fix",fixture_input="path",fixture_content="# Title  \n\nBody.\n",fixture_suffix=".md"),
    )),
))
MARKDOWN_RULES=register(Operation(
    id="markdown.rules",commands=(("markdown","rules"),),owner=Source(OWNER.module,OWNER.file,"rules"),
    input_schema=InputSchema(),handler=_rules,effects=Effects(),
))
MARKDOWN_RENUMBER=register(Operation(
    id="markdown.renumber",commands=(("markdown","renumber"),),owner=Source(OWNER.module,OWNER.file,"renumber"),
    input_schema=InputSchema((
        Field("path","path",example="fixture.md"),
        Field("write","boolean",required=False,default=False),
    )),handler=_renumber,effects=Effects(filesystem="write"),verification=Verification(probes=(
        Probe(name="renumber-preview",inputs={"write":False},fixture_input="path",fixture_content="# Title\n\n## First\n\nBody.\n",fixture_suffix=".md"),
    )),
))
