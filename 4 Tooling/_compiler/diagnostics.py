"""Own structured validation findings and their presentation projections."""

from __future__ import annotations

import json
import os
import re
from dataclasses import asdict, dataclass
from enum import Enum
from pathlib import Path

from .links import CONTROL_LINK_RE
from .model import Corpus, python_docstring, read_text, repo_path, walk_files

ADDRESS_TOKEN_RE = re.compile(
    r"(?<![A-Za-z0-9_-])(?:(?:[a-z0-9][a-z0-9-]*):)?"
    r"§[0-9]+(?:\.[0-9]+)*(?:#[0-9]+(?:\.[0-9]+)*)?",
    re.IGNORECASE,
)
ANNOTATION_LINE_RE = re.compile(
    r"^[ \t]*<!-- (?:ERROR|WARNING|INFO) DS[0-9]{3}: .* -->[ \t]*(?:\r?\n)?$",
    re.MULTILINE,
)


class Severity(str, Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass(frozen=True)
class Diagnostic:
    code: str
    severity: Severity
    path: Path
    line: int
    message: str

    def inline_comment(self) -> str:
        message = " ".join(self.message.split())
        return f"<!-- {self.severity.value.upper()} {self.code}: {message} -->"


def clear_inline_annotations(root: Path) -> int:
    changed = 0
    for path in walk_files(root):
        if path.suffix.lower() not in {".md", ".py"}:
            continue
        text = read_text(path)
        cleaned = ANNOTATION_LINE_RE.sub("", text)
        if cleaned != text:
            path.write_text(cleaned, encoding="utf-8")
            changed += 1
    return changed


def _strip_inline_code(line: str) -> str:
    result: list[str] = []
    cursor = 0
    while cursor < len(line):
        tick = line.find("`", cursor)
        if tick == -1:
            result.append(line[cursor:])
            break
        result.append(line[cursor:tick])
        run_end = tick
        while run_end < len(line) and line[run_end] == "`":
            run_end += 1
        delimiter = line[tick:run_end]
        close = line.find(delimiter, run_end)
        if close == -1:
            break
        result.append(" " * (close + len(delimiter) - tick))
        cursor = close + len(delimiter)
    return "".join(result)


def _scan_markdown(text: str, path: Path, base_line: int = 1) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    in_fence = False
    fence_token: str | None = None
    in_comment = False
    for offset, original in enumerate(text.splitlines(), start=0):
        stripped = original.lstrip()
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

        line = original
        if in_comment:
            end = line.find("-->")
            if end == -1:
                continue
            line = line[end + 3 :]
            in_comment = False
        while "<!--" in line:
            start = line.find("<!--")
            end = line.find("-->", start + 4)
            if end == -1:
                line = line[:start]
                in_comment = True
                break
            line = line[:start] + " " * (end + 3 - start) + line[end + 3 :]

        line = CONTROL_LINK_RE.sub(lambda m: " " * len(m.group(0)), line)
        line = _strip_inline_code(line)
        for match in ADDRESS_TOKEN_RE.finditer(line):
            address = match.group(0)
            diagnostics.append(
                Diagnostic(
                    code="DS001",
                    severity=Severity.ERROR,
                    path=path,
                    line=base_line + offset,
                    message=(
                        f"Bare documentation address {address} is location-only and not durable; "
                        "use a UID-controlled link in reader-visible prose."
                    ),
                )
            )
    return diagnostics


def validate_bare_addresses(corpus: Corpus) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    for path in sorted(walk_files(corpus.root), key=lambda p: repo_path(corpus.root, p).casefold()):
        if path.suffix.lower() == ".md":
            diagnostics.extend(_scan_markdown(read_text(path), path))
        elif path.suffix.lower() == ".py":
            parsed = python_docstring(path)
            if parsed is not None:
                doc, start_line = parsed
                diagnostics.extend(_scan_markdown(doc, path, start_line))
    return diagnostics


def validate(corpus: Corpus) -> list[Diagnostic]:
    return validate_bare_addresses(corpus)


def annotate(root: Path, diagnostics: list[Diagnostic]) -> int:
    grouped: dict[Path, list[Diagnostic]] = {}
    for diagnostic in diagnostics:
        grouped.setdefault(diagnostic.path.resolve(), []).append(diagnostic)
    changed = 0
    for path, path_diagnostics in grouped.items():
        source = read_text(path)
        lines = source.splitlines(keepends=True)
        by_line: dict[int, list[Diagnostic]] = {}
        for diagnostic in path_diagnostics:
            by_line.setdefault(diagnostic.line, []).append(diagnostic)
        output: list[str] = []
        for number, line in enumerate(lines, start=1):
            output.append(line)
            for diagnostic in sorted(by_line.get(number, []), key=lambda d: (d.severity.value, d.code)):
                newline = "\n" if line.endswith("\n") else ""
                if not newline:
                    output[-1] = output[-1] + "\n"
                output.append(diagnostic.inline_comment() + "\n")
        rendered = "".join(output)
        if rendered != source:
            path.write_text(rendered, encoding="utf-8")
            changed += 1
    return changed


def _github_escape(value: str, *, property_value: bool = False) -> str:
    value = value.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
    if property_value:
        value = value.replace(":", "%3A").replace(",", "%2C")
    return value


def emit(diagnostics: list[Diagnostic], root: Path) -> None:
    for diagnostic in diagnostics:
        path = repo_path(root, diagnostic.path)
        print(
            f"{diagnostic.severity.value.upper()} {diagnostic.code} "
            f"{path}:{diagnostic.line} {diagnostic.message}"
        )
        if os.getenv("GITHUB_ACTIONS", "").lower() == "true":
            command = {
                Severity.ERROR: "error",
                Severity.WARNING: "warning",
                Severity.INFO: "notice",
            }[diagnostic.severity]
            print(
                f"::{command} file={_github_escape(path, property_value=True)},"
                f"line={diagnostic.line},title={diagnostic.code}::"
                f"{_github_escape(diagnostic.message)}"
            )


def write_json(path: Path, diagnostics: list[Diagnostic], root: Path) -> None:
    payload = {
        "errors": sum(d.severity is Severity.ERROR for d in diagnostics),
        "warnings": sum(d.severity is Severity.WARNING for d in diagnostics),
        "info": sum(d.severity is Severity.INFO for d in diagnostics),
        "diagnostics": [
            {
                **asdict(d),
                "severity": d.severity.value,
                "path": repo_path(root, d.path),
            }
            for d in diagnostics
        ],
    }
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
