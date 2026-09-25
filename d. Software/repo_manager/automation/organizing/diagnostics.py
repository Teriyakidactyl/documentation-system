"""Own structured organization findings and their presentation projections."""

from __future__ import annotations

import json
import os
import re
from dataclasses import asdict, dataclass
from enum import Enum
from pathlib import Path

from repo_manager.capabilities.html import anchors
from .elements import element_instances
from .schemes.ordinal import OrdinalSchemeError, inspect as inspect_ordinal_sequences
from .model import (
    CONTROLLED_SIDEBAND_DIRS,
    UID_RE,
    Corpus,
    artifact_by_uid,
    corpus_path,
    corpus_root_name,
    python_docstring,
    read_text,
    walk_files,
)

BARE_CORPUS_ROOT_ADDRESS_RE = re.compile(
    r"(?<!:)§(?:[0-9]+|[a-z]+)(?:\.(?:[0-9]+|[a-z]+))*(?:#[0-9]+(?:\.[0-9]+)*)?"
)
ANNOTATION_LINE_RE = re.compile(
    r"^[ \t]*<!-- (?:ERROR|WARNING|INFO) DS[0-9]{3}: .* -->[ \t]*(?:\r?\n)?$",
    re.MULTILINE,
)

VERSION_RE = re.compile(r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$")
DRIFT_RANK = {"minor": 1, "major": 2}


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


def clear_inline_annotations(corpus_root: Path) -> int:
    changed = 0
    for path in walk_files(corpus_root):
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


def _scan_markdown(
    text: str,
    path: Path,
    corpus_root: str,
    base_line: int = 1,
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    address_re = re.compile(
        rf"(?P<prefix>^|[^A-Za-z0-9_-])"
        rf"(?P<address>{re.escape(corpus_root)}:§(?:[0-9]+|[a-z]+)(?:\.(?:[0-9]+|[a-z]+))*(?:#[0-9]+(?:\.[0-9]+)*)?)"
    )
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

        chars = list(line)
        for anchor in anchors(line):
            if anchor.attribute("uid") is None:
                continue
            for index in range(anchor.start, anchor.end):
                chars[index] = " "
        line = _strip_inline_code("".join(chars))

        for match in address_re.finditer(line):
            address = match.group("address")
            diagnostics.append(
                Diagnostic(
                    code="DS001",
                    severity=Severity.ERROR,
                    path=path,
                    line=base_line + offset,
                    message=(
                        f"Documentation address {address} appears as plain prose; "
                        "use a UID-controlled link in reader-visible prose."
                    ),
                )
            )

        for match in BARE_CORPUS_ROOT_ADDRESS_RE.finditer(line):
            bare_address = match.group(0)
            diagnostics.append(
                Diagnostic(
                    code="DS004",
                    severity=Severity.ERROR,
                    path=path,
                    line=base_line + offset,
                    message=(
                        f"Bare corpus-root address {bare_address} is invalid and unresolvable; "
                        f"declare the corpus root as {corpus_root}:{bare_address}."
                    ),
                )
            )
    return diagnostics


def validate_address_references(corpus: Corpus) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    root_name = corpus_root_name(corpus.corpus_root)
    for path in sorted(walk_files(corpus.corpus_root), key=lambda p: corpus_path(corpus.corpus_root, p).casefold()):
        rel = path.resolve().relative_to(corpus.corpus_root.resolve())
        if any(part in CONTROLLED_SIDEBAND_DIRS for part in rel.parts[:-1]):
            continue
        if path.suffix.lower() == ".md":
            diagnostics.extend(_scan_markdown(read_text(path), path, root_name))
        elif path.suffix.lower() == ".py":
            parsed = python_docstring(path)
            if parsed is not None:
                doc, start_line = parsed
                diagnostics.extend(_scan_markdown(doc, path, root_name, start_line))
    return diagnostics


def validate_research_reports(corpus: Corpus) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    by_uid = artifact_by_uid(corpus)
    for artifact in sorted(corpus.artifacts.values(), key=lambda a: corpus_path(corpus.corpus_root, a.path).casefold()):
        prompt_uid = artifact.metadata.get("research-prompt")
        if prompt_uid is None:
            continue
        if not isinstance(prompt_uid, str) or not UID_RE.fullmatch(prompt_uid):
            diagnostics.append(
                Diagnostic(
                    code="DS002",
                    severity=Severity.ERROR,
                    path=artifact.path,
                    line=1,
                    message="research-prompt must be a six-character controlled artifact UID",
                )
            )
            continue
        prompt = by_uid.get(prompt_uid)
        if prompt is None:
            diagnostics.append(
                Diagnostic(
                    code="DS002",
                    severity=Severity.ERROR,
                    path=artifact.path,
                    line=1,
                    message=f"research-prompt names missing uid {prompt_uid}",
                )
            )
        else:
            rel = prompt.path.resolve().relative_to(corpus.corpus_root.resolve())
            if ".research" not in rel.parts[:-1] or prompt.path.name != "Prompt.md":
                diagnostics.append(
                    Diagnostic(
                        code="DS002",
                        severity=Severity.ERROR,
                        path=artifact.path,
                        line=1,
                        message=(
                            f"research-prompt uid {prompt_uid} must identify Prompt.md "
                            "inside the controlled .research sideband"
                        ),
                    )
                )

        run = artifact.metadata.get("research-run")
        required = ("executed-at", "model", "version")
        if not isinstance(run, dict) or any(not run.get(key) for key in required):
            diagnostics.append(
                Diagnostic(
                    code="DS003",
                    severity=Severity.ERROR,
                    path=artifact.path,
                    line=1,
                    message=(
                        "research-run must record non-empty executed-at, model, and version "
                        "for every retained research report"
                    ),
                )
            )
    return diagnostics


def _version_tuple(value: object) -> tuple[int, int] | None:
    if not isinstance(value, str):
        return None
    match = VERSION_RE.fullmatch(value)
    if match is None:
        return None
    return int(match.group(1)), int(match.group(2))


def _version_policy(metadata: dict) -> tuple[tuple[int, int] | None, bool, str | None, str | None]:
    version = metadata.get("version")
    if not isinstance(version, dict):
        return None, True, None, None
    current = _version_tuple(version.get("value"))
    info = version.get("info", True)
    warn = version.get("warn")
    error = version.get("error")
    return (
        current,
        info if isinstance(info, bool) else True,
        warn if warn in DRIFT_RANK else None,
        error if error in DRIFT_RANK else None,
    )


def validate_form_versions(corpus: Corpus) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    by_uid = artifact_by_uid(corpus)

    for artifact in sorted(
        corpus.artifacts.values(),
        key=lambda item: corpus_path(corpus.corpus_root, item.path).casefold(),
    ):
        form = artifact.metadata.get("form")
        if form is None:
            continue
        if not isinstance(form, dict):
            diagnostics.append(Diagnostic(
                code="DS006",
                severity=Severity.ERROR,
                path=artifact.path,
                line=1,
                message="form must be a mapping containing path and version",
            ))
            continue

        path_value = form.get("path")
        consumed_value = form.get("version")
        consumed = _version_tuple(consumed_value)
        if not isinstance(path_value, str) or consumed is None:
            diagnostics.append(Diagnostic(
                code="DS006",
                severity=Severity.ERROR,
                path=artifact.path,
                line=1,
                message="form.path must be a controlled-link string and form.version must use major.minor",
            ))
            continue

        found = [anchor for anchor in anchors(path_value) if anchor.attribute("uid") is not None]
        if len(found) != 1:
            diagnostics.append(Diagnostic(
                code="DS006",
                severity=Severity.ERROR,
                path=artifact.path,
                line=1,
                message="form.path must contain exactly one UID-controlled link",
            ))
            continue

        target_uid = found[0].attribute("uid")
        target = by_uid.get(target_uid) if target_uid is not None else None
        if target is None:
            diagnostics.append(Diagnostic(
                code="DS006",
                severity=Severity.ERROR,
                path=artifact.path,
                line=1,
                message=f"form.path names missing uid {target_uid or '<none>'}",
            ))
            continue

        current, info_enabled, warn_at, error_at = _version_policy(target.metadata)
        if current is None:
            diagnostics.append(Diagnostic(
                code="DS006",
                severity=Severity.ERROR,
                path=artifact.path,
                line=1,
                message=f"Form uid {target_uid} must declare version.value as major.minor",
            ))
            continue

        if consumed == current:
            continue
        if consumed > current:
            diagnostics.append(Diagnostic(
                code="DS006",
                severity=Severity.ERROR,
                path=artifact.path,
                line=1,
                message=(
                    f"form.version {consumed_value} is newer than Form uid {target_uid} "
                    f"authority version {current[0]}.{current[1]}"
                ),
            ))
            continue

        drift = "major" if consumed[0] != current[0] else "minor"
        rank = DRIFT_RANK[drift]
        severity: Severity | None = None
        if error_at is not None and rank >= DRIFT_RANK[error_at]:
            severity = Severity.ERROR
        elif warn_at is not None and rank >= DRIFT_RANK[warn_at]:
            severity = Severity.WARNING
        elif info_enabled:
            severity = Severity.INFO

        if severity is not None:
            diagnostics.append(Diagnostic(
                code="DS006",
                severity=severity,
                path=artifact.path,
                line=1,
                message=(
                    f"form.version {consumed_value} has {drift} drift from Form uid {target_uid} "
                    f"version {current[0]}.{current[1]}"
                ),
            ))
    return diagnostics


def validate_element_versions(corpus: Corpus) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    by_uid = artifact_by_uid(corpus)

    for instance in element_instances(corpus):
        element = instance.element
        path_value = element.get("path")
        consumed_value = element.get("version")
        consumed = _version_tuple(consumed_value)

        if not isinstance(path_value, dict):
            diagnostics.append(Diagnostic(
                code="DS007",
                severity=Severity.ERROR,
                path=instance.owner,
                line=1,
                message="element.path must be a mapping containing uid and filepath",
            ))
            continue

        uid = path_value.get("uid")
        filepath = path_value.get("filepath")
        if (
            not isinstance(uid, str)
            or not UID_RE.fullmatch(uid)
            or not isinstance(filepath, str)
            or not filepath
            or consumed is None
        ):
            diagnostics.append(Diagnostic(
                code="DS007",
                severity=Severity.ERROR,
                path=instance.owner,
                line=1,
                message=(
                    "element.path.uid must be a controlled UID, element.path.filepath "
                    "must be non-empty, and element.version must use major.minor"
                ),
            ))
            continue

        renderer = element.get("renderer")
        if renderer is not None:
            if (
                not isinstance(renderer, dict)
                or not isinstance(renderer.get("uid"), str)
                or not UID_RE.fullmatch(renderer["uid"])
                or not isinstance(renderer.get("filepath"), str)
                or not renderer["filepath"]
            ):
                diagnostics.append(Diagnostic(
                    code="DS007",
                    severity=Severity.ERROR,
                    path=instance.owner,
                    line=1,
                    message="element.renderer must contain a controlled uid and non-empty filepath",
                ))
                continue

        target = by_uid.get(uid)
        if target is None:
            # External Element authorities remain valid declarations, but this
            # corpus cannot compare their current contract version.
            continue

        current, info_enabled, warn_at, error_at = _version_policy(target.metadata)
        if current is None:
            diagnostics.append(Diagnostic(
                code="DS007",
                severity=Severity.ERROR,
                path=instance.owner,
                line=1,
                message=f"Element uid {uid} must declare version.value as major.minor",
            ))
            continue

        if consumed == current:
            continue
        if consumed > current:
            diagnostics.append(Diagnostic(
                code="DS007",
                severity=Severity.ERROR,
                path=instance.owner,
                line=1,
                message=(
                    f"element.version {consumed_value} is newer than Element uid {uid} "
                    f"authority version {current[0]}.{current[1]}"
                ),
            ))
            continue

        drift = "major" if consumed[0] != current[0] else "minor"
        rank = DRIFT_RANK[drift]
        severity: Severity | None = None
        if error_at is not None and rank >= DRIFT_RANK[error_at]:
            severity = Severity.ERROR
        elif warn_at is not None and rank >= DRIFT_RANK[warn_at]:
            severity = Severity.WARNING
        elif info_enabled:
            severity = Severity.INFO

        if severity is not None:
            diagnostics.append(Diagnostic(
                code="DS007",
                severity=severity,
                path=instance.owner,
                line=1,
                message=(
                    f"element.version {consumed_value} has {drift} drift from Element uid {uid} "
                    f"version {current[0]}.{current[1]}"
                ),
            ))
    return diagnostics


def validate_ordinal_sequences(corpus: Corpus) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    try:
        sequences = inspect_ordinal_sequences(corpus.corpus_root)
    except OrdinalSchemeError:
        return diagnostics
    for sequence in sequences:
        if sequence.contiguous:
            continue
        owner = corpus.origin
        candidate = (sequence.parent / "README.md").resolve()
        if candidate in corpus.artifacts:
            owner = candidate
        found = ", ".join(str(value) for value, _ in sequence.entries)
        expected = ", ".join(str(value) for value in range(1, len(sequence.entries) + 1))
        parent = "." if sequence.parent == corpus.corpus_root else corpus_path(
            corpus.corpus_root, sequence.parent
        )
        diagnostics.append(
            Diagnostic(
                code="DS005",
                severity=Severity.WARNING,
                path=owner,
                line=1,
                message=(
                    f"Ordinal sequence under {parent} is not contiguous: "
                    f"found [{found}], normalized sequence is [{expected}]."
                ),
            )
        )
    return diagnostics


def validate(corpus: Corpus) -> list[Diagnostic]:
    return (
        validate_address_references(corpus)
        + validate_research_reports(corpus)
        + validate_form_versions(corpus)
        + validate_element_versions(corpus)
        + validate_ordinal_sequences(corpus)
    )


def annotate(corpus_root: Path, diagnostics: list[Diagnostic]) -> int:
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


def emit(diagnostics: list[Diagnostic], corpus_root: Path) -> None:
    for diagnostic in diagnostics:
        path = corpus_path(corpus_root, diagnostic.path)
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


def write_json(path: Path, diagnostics: list[Diagnostic], corpus_root: Path) -> None:
    payload = {
        "errors": sum(d.severity is Severity.ERROR for d in diagnostics),
        "warnings": sum(d.severity is Severity.WARNING for d in diagnostics),
        "info": sum(d.severity is Severity.INFO for d in diagnostics),
        "diagnostics": [
            {
                **asdict(d),
                "severity": d.severity.value,
                "path": corpus_path(corpus_root, d.path),
            }
            for d in diagnostics
        ],
    }
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
