"""Own frontmatter envelope parsing and mutation across supported host files."""

from __future__ import annotations

import ast
import io
import re
import tokenize
from dataclasses import dataclass
from pathlib import Path

from .yaml import YamlError, parse_mapping, serialize as serialize_yaml


class FrontmatterError(ValueError):
    """Raised when a frontmatter surface cannot be parsed or mutated safely."""


@dataclass(frozen=True)
class Frontmatter:
    data: dict
    body: str
    kind: str
    start_line: int


def split(text: str) -> tuple[str, str] | None:
    if not text.startswith("---\n"):
        return None
    close = text.find("\n---", 4)
    if close == -1:
        return None
    fence_end = close + 4
    if fence_end < len(text) and text[fence_end] == "\n":
        fence_end += 1
    return text[4:close], text[fence_end:]


def module_docstring(source: str, owner: str = "<python>") -> tuple[str, int] | None:
    try:
        tree = ast.parse(source, filename=owner)
    except SyntaxError as exc:
        raise FrontmatterError(f"Can't parse Python documentation in {owner}: {exc}") from exc
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


def parse_text(text: str, *, kind: str, owner: str = "<text>") -> Frontmatter | None:
    start_line = 1
    surface = text
    if kind == "py":
        parsed = module_docstring(text, owner)
        if parsed is None:
            return None
        surface, start_line = parsed
    elif kind != "md":
        raise FrontmatterError(f"Unsupported frontmatter host kind {kind!r}")

    separated = split(surface)
    if separated is None:
        return None
    raw, body = separated
    try:
        data = parse_mapping(raw)
    except YamlError as exc:
        raise FrontmatterError(f"Invalid YAML metadata in {owner}: {exc}") from exc
    return Frontmatter(data=data, body=body, kind=kind, start_line=start_line)


def load(path: Path) -> Frontmatter | None:
    kind = path.suffix.lower().lstrip(".")
    try:
        source = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise FrontmatterError(f"Can't read {path}: {exc}") from exc
    return parse_text(source, kind=kind, owner=str(path))


def _source_offset(lines: list[str], position: tuple[int, int]) -> int:
    line, column = position
    return sum(len(part) for part in lines[: line - 1]) + column


def add_missing_key(path: Path, key: str, value: str) -> None:
    try:
        source = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise FrontmatterError(f"Can't read {path}: {exc}") from exc

    entry = serialize_yaml({key: value}).rstrip("\n") + "\n"

    suffix = path.suffix.lower()
    if suffix == ".md":
        if not source.startswith("---\n"):
            raise FrontmatterError(f"{path}: cannot add {key} without Markdown frontmatter")
        updated = source.replace("---\n", "---\n" + entry, 1)
        path.write_text(updated, encoding="utf-8")
        return

    if suffix != ".py":
        raise FrontmatterError(f"{path}: unsupported frontmatter host")

    try:
        tree = ast.parse(source, filename=str(path))
    except SyntaxError as exc:
        raise FrontmatterError(f"Can't parse Python metadata in {path}: {exc}") from exc
    if not tree.body:
        raise FrontmatterError(f"{path}: cannot find Python module docstring")
    first = tree.body[0]
    if not (
        isinstance(first, ast.Expr)
        and isinstance(first.value, ast.Constant)
        and isinstance(first.value.value, str)
    ):
        raise FrontmatterError(f"{path}: cannot find Python module docstring")

    token = None
    for candidate in tokenize.generate_tokens(io.StringIO(source).readline):
        if candidate.type == tokenize.STRING and candidate.start[0] == first.value.lineno:
            token = candidate
            break
    if token is None:
        raise FrontmatterError(f"{path}: cannot locate Python module docstring token")

    literal = token.string
    marker = "---\n"
    marker_at = literal.find(marker)
    if marker_at == -1:
        raise FrontmatterError(f"{path}: module docstring metadata must begin with ---")
    insert_at = marker_at + len(marker)
    new_literal = literal[:insert_at] + entry + literal[insert_at:]
    lines = source.splitlines(keepends=True)
    start = _source_offset(lines, token.start)
    end = _source_offset(lines, token.end)
    path.write_text(source[:start] + new_literal + source[end:], encoding="utf-8")


def replace_module_docstring(source: str, new_docstring: str, owner: str = "<python>") -> str:
    try:
        tree = ast.parse(source, filename=owner)
    except SyntaxError as exc:
        raise FrontmatterError(f"Can't parse Python documentation in {owner}: {exc}") from exc
    if not tree.body:
        raise FrontmatterError(f"{owner}: cannot find Python module docstring")
    first = tree.body[0]
    if not (
        isinstance(first, ast.Expr)
        and isinstance(first.value, ast.Constant)
        and isinstance(first.value.value, str)
    ):
        raise FrontmatterError(f"{owner}: cannot find Python module docstring")

    token = None
    for candidate in tokenize.generate_tokens(io.StringIO(source).readline):
        if candidate.type == tokenize.STRING and candidate.start[0] == first.value.lineno:
            token = candidate
            break
    if token is None:
        raise FrontmatterError(f"{owner}: cannot locate Python module docstring token")

    literal = token.string
    prefix_match = re.match(r"(?i)^([rub]*)", literal)
    prefix = prefix_match.group(1) if prefix_match else ""
    rest = literal[len(prefix) :]
    quote_mark = next(
        (mark for mark in ("'''", '"""') if rest.startswith(mark) and rest.endswith(mark)),
        None,
    )
    if quote_mark is None:
        raise FrontmatterError(f"{owner}: unsupported Python module docstring literal")
    new_literal = prefix + quote_mark + new_docstring + quote_mark
    lines = source.splitlines(keepends=True)
    start = _source_offset(lines, token.start)
    end = _source_offset(lines, token.end)
    return source[:start] + new_literal + source[end:]

from pathlib import Path
from typing import Any, Mapping
from repo_manager.capabilities.yaml import YamlError
from repo_manager.core import Effects, ExpectedFailure, Failure, Field, InputSchema, Operation, Probe, Result, Source, Verification, invoke, register

OPERATION_ID="frontmatter.inspect"
OWNER=Source("repo_manager.capabilities.frontmatter","d. Software/repo_manager/capabilities/frontmatter.py","inspect")
FRONTMATTER=Source("repo_manager.capabilities.frontmatter","d. Software/repo_manager/capabilities/frontmatter.py","load")
YAML=Source("repo_manager.capabilities.yaml","d. Software/repo_manager/capabilities/yaml.py","parse_mapping")

def _handler(inputs: Mapping[str, Any]) -> Result[Any]:
    path=Path(str(inputs["path"]))
    try:
        value=load(path)
    except FrontmatterError as exc:
        cause=exc.__cause__
        origin=YAML if isinstance(cause,YamlError) else FRONTMATTER
        raise ExpectedFailure(Failure(
            origin=origin,
            name="YAML_ERROR" if origin is YAML else "FRONTMATTER_ERROR",
            classification="malformed" if origin is YAML else "invalid-frontmatter",
            subject={"path":str(path)},
            message=str(exc),
            details={"exception_type":type(exc).__name__},
            provenance=("frontmatter.load",) if origin is YAML else (),
        )) from exc
    if value is None:
        raise ExpectedFailure(Failure(
            origin=FRONTMATTER,
            name="NO_FRONTMATTER",
            classification="not-found",
            subject={"path":str(path)},
            message="no supported frontmatter surface found",
        ))
    return Result.success({"kind":value.kind,"start_line":value.start_line,"data":value.data})

OPERATION=register(Operation(
    id=OPERATION_ID,
    commands=(("frontmatter","inspect"),),
    owner=OWNER,
    input_schema=InputSchema((Field("path","path",example="fixture.md"),)),
    handler=_handler,
    effects=Effects(filesystem="read"),
    verification=Verification(probes=(
        Probe(name="valid-frontmatter",fixture_input="path",fixture_content="---\nname: example\n---\n# Body\n",fixture_suffix=".md"),
        Probe(name="malformed-frontmatter-yaml",fixture_input="path",fixture_content="---\nname: [\n---\n# Body\n",fixture_suffix=".md",expected_status="failure",expected_failure_origin=YAML.file),
    )),
))
