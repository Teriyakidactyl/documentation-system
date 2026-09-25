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
