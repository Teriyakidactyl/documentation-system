"""Own generic HTML fragment inspection and constrained element rewriting."""

from __future__ import annotations

import re
from dataclasses import dataclass
from html.parser import HTMLParser
from typing import Callable


class HtmlError(ValueError):
    """Raised when an HTML operation cannot be completed deterministically."""


@dataclass(frozen=True)
class HtmlToken:
    kind: str
    line: int
    column: int
    tag: str | None = None
    attributes: tuple[tuple[str, str | None], ...] = ()
    data: str | None = None


@dataclass(frozen=True)
class HtmlAnchor:
    start: int
    end: int
    raw: str
    attributes: tuple[tuple[str, str | None], ...]
    text: str

    def attribute(self, name: str) -> str | None:
        wanted = name.casefold()
        for key, value in self.attributes:
            if key.casefold() == wanted:
                return value
        return None


class _Inspector(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.tokens: list[HtmlToken] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        line, column = self.getpos()
        self.tokens.append(HtmlToken("start", line, column + 1, tag, tuple(attrs)))

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        line, column = self.getpos()
        self.tokens.append(HtmlToken("startend", line, column + 1, tag, tuple(attrs)))

    def handle_endtag(self, tag: str) -> None:
        line, column = self.getpos()
        self.tokens.append(HtmlToken("end", line, column + 1, tag))

    def handle_comment(self, data: str) -> None:
        line, column = self.getpos()
        self.tokens.append(HtmlToken("comment", line, column + 1, data=data))

    def handle_decl(self, decl: str) -> None:
        line, column = self.getpos()
        self.tokens.append(HtmlToken("declaration", line, column + 1, data=decl))

    def handle_entityref(self, name: str) -> None:
        line, column = self.getpos()
        self.tokens.append(HtmlToken("entity", line, column + 1, data=name))

    def handle_charref(self, name: str) -> None:
        line, column = self.getpos()
        self.tokens.append(HtmlToken("charref", line, column + 1, data=name))


def inspect(text: str) -> list[HtmlToken]:
    parser = _Inspector()
    try:
        parser.feed(text)
        parser.close()
    except Exception as exc:
        raise HtmlError(str(exc)) from exc
    return parser.tokens


class _StartTagParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.attributes: tuple[tuple[str, str | None], ...] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if self.attributes is None:
            self.attributes = tuple(attrs)


ANCHOR_RE = re.compile(
    r'<a\b(?P<attrs>[^>\n]*)>(?P<text>[^<\n]*)</a>',
    re.IGNORECASE,
)


def _anchor_from_match(match: re.Match[str]) -> HtmlAnchor:
    raw = match.group(0)
    parser = _StartTagParser()
    try:
        parser.feed(raw)
        parser.close()
    except Exception as exc:
        raise HtmlError(f"Cannot parse anchor: {exc}") from exc
    if parser.attributes is None:
        raise HtmlError("Cannot parse anchor start tag")
    return HtmlAnchor(
        start=match.start(),
        end=match.end(),
        raw=raw,
        attributes=parser.attributes,
        text=match.group("text"),
    )


def anchors(text: str) -> list[HtmlAnchor]:
    return [_anchor_from_match(match) for match in ANCHOR_RE.finditer(text)]


def rewrite_anchors(
    text: str,
    renderer: Callable[[HtmlAnchor], str | None],
) -> tuple[str, int]:
    changed = 0

    def replace(match: re.Match[str]) -> str:
        nonlocal changed
        anchor = _anchor_from_match(match)
        rendered = renderer(anchor)
        if rendered is None or rendered == anchor.raw:
            return anchor.raw
        changed += 1
        return rendered

    return ANCHOR_RE.sub(replace, text), changed

from pathlib import Path
from typing import Any, Mapping
from repo_manager.core import Effects, ExpectedFailure, Failure, Field, InputSchema, Operation, Probe, Result, Source, Verification, invoke, register

OWNER=Source("repo_manager.capabilities.html","d. Software/repo_manager/capabilities/html.py")
CAPABILITY=Source("repo_manager.capabilities.html","d. Software/repo_manager/capabilities/html.py")

def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ExpectedFailure(Failure(
            origin=OWNER,name="READ_FAILED",classification="unreadable",
            subject={"path":str(path)},message=str(exc),
            details={"exception_type":type(exc).__name__},
        )) from exc

def _inspect(inputs: Mapping[str, Any]) -> Result[Any]:
    path=Path(str(inputs["path"]))
    try:
        return Result.success([item.__dict__ for item in inspect(_read(path))])
    except HtmlError as exc:
        raise ExpectedFailure(Failure(
            origin=Source(CAPABILITY.module,CAPABILITY.file,"inspect"),
            name="HTML_ERROR",classification="malformed",subject={"path":str(path)},
            message=str(exc),details={"exception_type":type(exc).__name__},
        )) from exc

def _anchors(inputs: Mapping[str, Any]) -> Result[Any]:
    path=Path(str(inputs["path"]))
    try:
        payload=[{"start":item.start,"end":item.end,"attributes":dict(item.attributes),"text":item.text} for item in anchors(_read(path))]
        return Result.success(payload)
    except HtmlError as exc:
        raise ExpectedFailure(Failure(
            origin=Source(CAPABILITY.module,CAPABILITY.file,"anchors"),
            name="HTML_ERROR",classification="malformed",subject={"path":str(path)},
            message=str(exc),details={"exception_type":type(exc).__name__},
        )) from exc

HTML_INSPECT=register(Operation(
    id="html.inspect",commands=(("html","inspect"),),owner=Source(OWNER.module,OWNER.file,"inspect"),
    input_schema=InputSchema((Field("path","path",example="fixture.html"),)),
    handler=_inspect,effects=Effects(filesystem="read"),
    verification=Verification(probes=(Probe(name="inspect-html",fixture_input="path",fixture_content="<p>Hello</p>\n",fixture_suffix=".html"),)),
))
HTML_ANCHORS=register(Operation(
    id="html.anchors",commands=(("html","anchors"),),owner=Source(OWNER.module,OWNER.file,"anchors"),
    input_schema=InputSchema((Field("path","path",example="fixture.html"),)),
    handler=_anchors,effects=Effects(filesystem="read"),
    verification=Verification(probes=(Probe(name="inspect-anchor",fixture_input="path",fixture_content="<a uid='ABC123' href='x'>Label</a>\n",fixture_suffix=".html"),)),
))
