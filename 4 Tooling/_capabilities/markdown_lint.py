"""Own the Documentation System's executable Markdown lint policy."""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from pathlib import Path

from .frontmatter import FrontmatterError, load as load_frontmatter
from .markdown import NUMBER_PREFIX_RE, headings

DEFAULT_RULES: dict[str, str] = {
    "MD001": "Heading levels do not skip depth.",
    "MD003": "Use ATX headings.",
    "MD004": "Use dash markers for unordered lists.",
    "MD005": "Keep list indentation consistent at one level.",
    "MD009": "Do not retain trailing spaces.",
    "MD010": "Do not use hard tabs.",
    "MD011": "Reject reversed link syntax.",
    "MD012": "Do not use repeated blank lines.",
    "MD018": "Use one space after an ATX heading marker.",
    "MD019": "Do not use repeated spaces after an ATX heading marker.",
    "MD023": "Headings begin at the left margin.",
    "MD024": "Sibling headings have unique text.",
    "MD027": "Use one space after blockquote markers.",
    "MD029": "Use sequential ordered-list markers.",
    "MD030": "Use canonical spacing after list markers.",
    "MD031": "Surround fenced code blocks with blank lines.",
    "MD032": "Surround lists with blank lines.",
    "MD034": "Do not leave bare URLs in prose.",
    "MD035": "Use one thematic-break representation.",
    "MD037": "Do not pad emphasis markers with spaces.",
    "MD038": "Do not pad code spans with spaces.",
    "MD039": "Do not pad link text with spaces.",
    "MD040": "Give fenced code blocks a language.",
    "MD042": "Do not leave empty link destinations.",
    "MD045": "Give images alt text.",
    "MD046": "Use fenced rather than indented code blocks.",
    "MD047": "End files with one newline.",
    "MD048": "Use backticks for fenced code blocks.",
    "MD049": "Use asterisks for emphasis.",
    "MD050": "Use asterisks for strong emphasis.",
    "MD051": "Local link fragments must resolve.",
    "MD053": "Do not retain unused link/image reference definitions.",
    "MD059": "Use descriptive link text.",
    "MD060": "Use compact GFM table columns.",
    "PML100": "Reject raw HTML elements that GFM treats as unsafe in Markdown.",
}

AUTOFIX_RULES = frozenset({
    "MD001", "MD004", "MD005", "MD009", "MD010", "MD019", "MD023",
    "MD027", "MD029", "MD030", "MD035", "MD037", "MD038", "MD039",
    "MD046", "MD047", "MD048",
})

EMPHASIS_IN_HEADING_RE = re.compile(
    r"(\*\*[^*\n]+\*\*|__[^_\n]+__|(?<!\*)\*[^*\n]+\*(?!\*)|(?<!_)_[^_\n]+_(?!_))"
)


class MarkdownLintError(ValueError):
    """Raised when linting cannot establish a deterministic result."""


@dataclass(frozen=True)
class MarkdownDiagnostic:
    code: str
    line: int
    column: int
    message: str
    fixable: bool
    source: str

    def to_dict(self) -> dict:
        return asdict(self)


def _api():
    try:
        from pymarkdown.api import PyMarkdownApi
    except ImportError as exc:
        raise MarkdownLintError(
            "PyMarkdownLnt is required; install pymarkdownlnt==0.9.40"
        ) from exc

    api = PyMarkdownApi(inherit_logging=True).disable_rule_by_identifier("*")
    for rule_id in DEFAULT_RULES:
        api.enable_rule_by_identifier(rule_id)
    api.enable_extension_by_identifier("markdown-tables")

    settings = {
        "plugins.md003.style": "atx",
        "plugins.md004.style": "dash",
        "plugins.md029.style": "ordered",
        "plugins.md035.style": "---",
        "plugins.md046.style": "fenced",
        "plugins.md048.style": "backtick",
        "plugins.md049.style": "asterisk",
        "plugins.md050.style": "asterisk",
        "plugins.md060.style": "compact",
    }
    for key, value in settings.items():
        api.set_string_property(key, value)
    api.set_boolean_property("plugins.md024.siblings_only", True)
    return api


def rule_policy() -> list[dict]:
    policy = [
        {"code": code, "opinion": opinion, "fixable": code in AUTOFIX_RULES}
        for code, opinion in DEFAULT_RULES.items()
    ]
    policy.extend([
        {
            "code": "DSMD001",
            "opinion": "Headings do not contain Markdown emphasis.",
            "fixable": False,
        },
        {
            "code": "DSMD002",
            "opinion": (
                "When hierarchical-decimal numbering is declared, local heading "
                "numbers follow source order and depth."
            ),
            "fixable": False,
        },
    ])
    return policy


def _custom_diagnostics(body: str, metadata: dict) -> list[MarkdownDiagnostic]:
    diagnostics: list[MarkdownDiagnostic] = []
    found = headings(body)
    for item in found:
        if EMPHASIS_IN_HEADING_RE.search(str(item["title"])):
            diagnostics.append(MarkdownDiagnostic(
                "DSMD001", int(item["line"]), 1,
                "Heading contains emphasis; headings use plain text.",
                False, "documentation-system",
            ))

    outline = metadata.get("outline")
    numbering = outline.get("numbering") if isinstance(outline, dict) else None
    if numbering != "hierarchical-decimal":
        return diagnostics

    counters = [0, 0, 0, 0, 0]
    previous_level: int | None = None
    for item in found:
        level = int(item["level"])
        if level == 1:
            counters = [0, 0, 0, 0, 0]
            previous_level = None
            continue
        if previous_level is None and level != 2:
            previous_level = level
            continue
        if previous_level is not None and level > previous_level + 1:
            previous_level = level
            continue
        index = level - 2
        counters[index] += 1
        for deeper in range(index + 1, len(counters)):
            counters[deeper] = 0
        expected = ".".join(str(value) for value in counters[: index + 1])
        match = NUMBER_PREFIX_RE.match(str(item["title"]))
        actual = match.group(0).strip().rstrip(".") if match else None
        if actual != expected:
            diagnostics.append(MarkdownDiagnostic(
                "DSMD002", int(item["line"]), 1,
                f"Expected local heading number {expected}; found {actual or 'none'}.",
                False, "documentation-system",
            ))
        previous_level = level
    return diagnostics


def _parts(path: Path) -> tuple[str, str, dict, int]:
    source = path.read_text(encoding="utf-8")
    try:
        frontmatter = load_frontmatter(path)
    except FrontmatterError as exc:
        raise MarkdownLintError(str(exc)) from exc
    if frontmatter is None:
        return "", source, {}, 0
    body = frontmatter.body
    if not source.endswith(body):
        raise MarkdownLintError(f"{path}: frontmatter did not preserve Markdown body")
    prefix = source[: len(source) - len(body)]
    return prefix, body, frontmatter.data, prefix.count("\n")


def lint_text(body: str, *, metadata: dict | None = None, line_offset: int = 0) -> list[MarkdownDiagnostic]:
    try:
        result = _api().scan_string(body)
    except Exception as exc:
        raise MarkdownLintError(f"PyMarkdown scan failed: {exc}") from exc

    diagnostics = [
        MarkdownDiagnostic(
            failure.rule_id.upper(),
            failure.line_number + line_offset,
            failure.column_number,
            failure.rule_description + (failure.extra_error_information or ""),
            failure.rule_id.upper() in AUTOFIX_RULES,
            "pymarkdown",
        )
        for failure in result.scan_failures
    ]
    for item in _custom_diagnostics(body, metadata or {}):
        diagnostics.append(MarkdownDiagnostic(
            item.code, item.line + line_offset, item.column,
            item.message, item.fixable, item.source,
        ))
    return sorted(diagnostics, key=lambda item: (item.line, item.column, item.code))


def lint_file(path: Path) -> list[MarkdownDiagnostic]:
    _, body, metadata, offset = _parts(path)
    return lint_text(body, metadata=metadata, line_offset=offset)


def fix_file(path: Path) -> tuple[list[MarkdownDiagnostic], bool]:
    prefix, body, metadata, _ = _parts(path)
    try:
        result = _api().fix_string(body)
    except Exception as exc:
        raise MarkdownLintError(f"PyMarkdown fix failed: {exc}") from exc

    rendered = result.fixed_file
    changed = rendered != body
    if changed:
        path.write_text(prefix + rendered, encoding="utf-8")
    return lint_file(path), changed
