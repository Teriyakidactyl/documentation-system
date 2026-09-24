#!/usr/bin/env python3
"""Validate and deterministically format the Semantic Registry Document Element."""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import json
from pathlib import Path
import re
import sys
from typing import Iterable

CORPUS_ROOT = Path(__file__).resolve().parents[4]
TOOLING = CORPUS_ROOT / "4 Tooling"
if str(TOOLING) not in sys.path:
    sys.path.insert(0, str(TOOLING))

from _capabilities.markdown import MarkdownError, fenced_blocks, resolve_section
from _capabilities.yaml import YamlError, parse_mapping

KEY_RE = re.compile(
    r'^(?P<indent> *)(?P<key>"(?:[^"\\]|\\.)*"):(?P<rest>.*?)(?P<ending>\r?\n)?$'
)
ANY_MAPPING_RE = re.compile(r"^(?P<indent> *)(?P<key>[^#][^:]*):(?P<rest>.*)$")

class SemanticRegistryError(ValueError):
    """Raised when a Semantic Registry operation cannot be established."""


@dataclass(frozen=True)
class Diagnostic:
    code: str
    severity: str
    line: int
    message: str


@dataclass(frozen=True)
class RegistryBlock:
    section_start_line: int
    block_start_line: int
    content_start_line: int
    block_end_line: int
    content: str


def _entry_lines(content: str) -> Iterable[tuple[int, re.Match[str]]]:
    for line_number, line in enumerate(content.splitlines(keepends=True), start=1):
        if line.startswith("# Terms:") or not line.strip() or line.lstrip().startswith("#"):
            continue
        match = KEY_RE.match(line)
        if match is not None:
            yield line_number, match


def _line_diagnostics(content: str) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    entries = list(_entry_lines(content))

    for line_number, line in enumerate(content.splitlines(), start=1):
        if "\t" in line:
            diagnostics.append(
                Diagnostic("SR003", "error", line_number, "Semantic Registry indentation must not contain tabs.")
            )
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        quoted = KEY_RE.match(line)
        mapping = ANY_MAPPING_RE.match(line)
        if mapping is not None and quoted is None:
            diagnostics.append(
                Diagnostic(
                    "SR004",
                    "error",
                    line_number,
                    "Semantic Registry mapping keys must be double-quoted reader-visible labels.",
                )
            )
            continue
        if quoted is not None:
            indent = len(quoted.group("indent"))
            if indent % 2:
                diagnostics.append(
                    Diagnostic(
                        "SR005",
                        "error",
                        line_number,
                        f"Semantic Registry indentation is {indent} spaces; use multiples of two.",
                    )
                )

    if not entries:
        diagnostics.append(Diagnostic("SR006", "error", 1, "Semantic Registry contains no mapping entries."))
        return diagnostics

    root_indent = min(len(match.group("indent")) for _, match in entries)
    if root_indent != 2:
        first_root_line = next(
            line_number
            for line_number, match in entries
            if len(match.group("indent")) == root_indent
        )
        diagnostics.append(
            Diagnostic(
                "SR005",
                "error",
                first_root_line,
                f"Root registry entries are indented {root_indent} spaces; use exactly two.",
            )
        )

    previous_indent: int | None = None
    for line_number, match in entries:
        indent = len(match.group("indent"))
        if previous_indent is not None and indent > previous_indent + 2:
            diagnostics.append(
                Diagnostic(
                    "SR005",
                    "error",
                    line_number,
                    f"Semantic Registry indentation jumps from {previous_indent} to {indent} spaces; advance one two-space level at a time.",
                )
            )
        previous_indent = indent

        if indent != root_indent:
            continue
        rest = match.group("rest").strip()
        if not rest.startswith("#") or not rest[1:].strip():
            diagnostics.append(
                Diagnostic(
                    "SR007",
                    "error",
                    line_number,
                    "Each root registry entry must carry a non-empty trailing-comment definition.",
                )
            )

    return diagnostics


def format_content(content: str) -> str:
    """Return the canonical absolute-column representation of one registry block."""
    endings = content.splitlines(keepends=True)
    if not endings:
        raise SemanticRegistryError("Semantic Registry block is empty.")

    body_lines = [line for line in endings if not line.startswith("# Terms:")]
    matches: list[tuple[str, re.Match[str]]] = []
    for line in body_lines:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        match = KEY_RE.match(line)
        if match is not None:
            matches.append((line, match))

    if not matches:
        raise SemanticRegistryError("Semantic Registry contains no double-quoted mapping entries.")

    anchor = max(len(match.group("indent") + match.group("key") + ":") for _, match in matches) + 4
    rendered: list[str] = []
    for line in body_lines:
        match = KEY_RE.match(line)
        if match is None:
            rendered.append(line)
            continue
        prefix = match.group("indent") + match.group("key") + ":"
        rest = match.group("rest").strip()
        ending = match.group("ending") or ""
        if rest:
            rendered.append(prefix + (" " * (anchor - len(prefix))) + rest + ending)
        else:
            rendered.append(prefix + ending)

    terminal = max(
        [len(line.rstrip("\r\n")) for line in rendered if line.strip()]
        + [anchor + len("# Definitions") + 12]
    )
    left_label = "# Terms:"
    left = left_label + " " + ("-" * max(1, anchor - len(left_label) - 2)) + " "
    right_label = "# Definitions "
    header_base = left + right_label
    header = header_base + ("-" * max(1, terminal - len(header_base)))

    newline = "\r\n" if any(line.endswith("\r\n") for line in endings) else "\n"
    return header + newline + "".join(rendered)


def _locate(path: Path, selector: str) -> tuple[str, RegistryBlock]:
    try:
        body = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise SemanticRegistryError(f"Can't read {path}: {exc}") from exc

    try:
        section = resolve_section(body, selector)
    except MarkdownError as exc:
        raise SemanticRegistryError(str(exc)) from exc

    lines = body.splitlines(keepends=True)
    section_text = "".join(lines[section.start_line - 1 : section.end_line])
    try:
        blocks = fenced_blocks(section_text, language="yaml")
    except MarkdownError as exc:
        raise SemanticRegistryError(str(exc)) from exc

    if len(blocks) != 1:
        raise SemanticRegistryError(
            f"Semantic Registry section must contain exactly one fenced yaml block; found {len(blocks)}."
        )
    block = blocks[0]
    base = section.start_line - 1
    return body, RegistryBlock(
        section_start_line=section.start_line,
        block_start_line=base + block.start_line,
        content_start_line=base + block.content_start_line,
        block_end_line=base + block.end_line,
        content=block.content,
    )


def diagnostics(path: Path, selector: str) -> tuple[list[Diagnostic], RegistryBlock]:
    _, block = _locate(path, selector)
    local = _line_diagnostics(block.content)
    try:
        parse_mapping(block.content)
    except YamlError as exc:
        local.append(Diagnostic("SR002", "error", 1, f"Semantic Registry YAML is invalid: {exc}"))

    if not any(item.code in {"SR002", "SR003", "SR004", "SR005", "SR006", "SR007"} for item in local):
        canonical = format_content(block.content)
        if canonical != block.content:
            local.append(
                Diagnostic(
                    "SR008",
                    "error",
                    1,
                    "Semantic Registry is not in canonical absolute-column alignment; run format.",
                )
            )

    offset = block.content_start_line - 1
    return [
        Diagnostic(item.code, item.severity, item.line + offset, item.message)
        for item in local
    ], block


def _replace_block(body: str, block: RegistryBlock, replacement: str) -> str:
    lines = body.splitlines(keepends=True)
    start = block.content_start_line - 1
    end = block.block_end_line - 1
    return "".join(lines[:start]) + replacement + "".join(lines[end:])


def format_document(path: Path, selector: str, *, write: bool = False) -> dict:
    body, block = _locate(path, selector)
    pre = _line_diagnostics(block.content)
    fatal = [item for item in pre if item.severity == "error" and item.code != "SR008"]
    try:
        parse_mapping(block.content)
    except YamlError as exc:
        fatal.append(Diagnostic("SR002", "error", 1, f"Semantic Registry YAML is invalid: {exc}"))
    if fatal:
        raise SemanticRegistryError("; ".join(f"{item.code}: {item.message}" for item in fatal))

    rendered = format_content(block.content)
    try:
        parse_mapping(rendered)
    except YamlError as exc:
        raise SemanticRegistryError(f"Formatted Semantic Registry would not parse as YAML: {exc}") from exc

    changed = rendered != block.content
    if write and changed:
        path.write_text(_replace_block(body, block, rendered), encoding="utf-8")

    return {
        "path": str(path),
        "selector": selector,
        "changed": changed,
        "written": bool(write and changed),
        "content": rendered,
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    check = sub.add_parser("check", help="Validate one Semantic Registry element.")
    check.add_argument("path", type=Path)
    check.add_argument("selector")

    fmt = sub.add_parser("format", help="Render canonical absolute-column alignment.")
    fmt.add_argument("--write", action="store_true")
    fmt.add_argument("path", type=Path)
    fmt.add_argument("selector")
    return parser


def main() -> None:
    args = _parser().parse_args()
    try:
        if args.command == "check":
            found, block = diagnostics(args.path, args.selector)
            payload = {
                "path": str(args.path),
                "selector": args.selector,
                "block": {
                    "start_line": block.block_start_line,
                    "end_line": block.block_end_line,
                },
                "diagnostics": [asdict(item) for item in found],
            }
            print(json.dumps(payload, indent=2, ensure_ascii=False))
            raise SystemExit(1 if any(item.severity == "error" for item in found) else 0)

        result = format_document(args.path, args.selector, write=args.write)
        if args.write:
            print(json.dumps({key: value for key, value in result.items() if key != "content"}, indent=2))
        else:
            print(result["content"], end="")
    except SemanticRegistryError as exc:
        raise SystemExit(f"semantic-registry: {exc}") from exc


if __name__ == "__main__":
    main()
