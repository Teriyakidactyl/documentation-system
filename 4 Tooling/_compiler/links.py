"""Own UID-controlled link resolution and mechanical href/address rewriting."""

from __future__ import annotations

import ast
import io
import re
import tokenize
from pathlib import Path
from urllib.parse import quote

from .indexes import relative_link
from .model import (
    ADDRESS_RE,
    UID_RE,
    CompilerError,
    Corpus,
    artifact_by_uid,
    heading_target,
    qualified_address,
    read_text,
    repo_path,
    source_offset,
    walk_files,
)

CONTROL_LINK_RE = re.compile(
    r'<a\b(?P<attrs>[^>\n]*?\buid="(?P<uid>[^"]+)"[^>\n]*?)>'
    r'(?P<label>[^<\n]+)</a>'
)


def render_control_link(owner: Path, corpus: Corpus, uid: str, label: str) -> str:
    if not UID_RE.fullmatch(uid):
        raise CompilerError(f"{repo_path(corpus.root, owner)}: invalid controlled-link uid {uid!r}")
    artifact = artifact_by_uid(corpus).get(uid)
    if artifact is None:
        raise CompilerError(f"{repo_path(corpus.root, owner)}: controlled link names missing uid {uid}")
    match = ADDRESS_RE.fullmatch(label.strip())
    if match is None:
        raise CompilerError(
            f"{repo_path(corpus.root, owner)}: controlled link uid {uid} must display a documentation address"
        )
    qualifier = match.group("space")
    if qualifier is not None and qualifier != corpus.address_space:
        raise CompilerError(
            f"{repo_path(corpus.root, owner)}: controlled link uid {uid} names address space "
            f"{qualifier!r}, not {corpus.address_space!r}"
        )
    section = match.group("section")
    heading = heading_target(artifact.body, section, artifact.path) if section else None
    href = relative_link(owner, artifact.path)
    if heading is not None:
        href += "#" + quote(heading.anchor, safe="-._~")
    return f'<a href="{href}" uid="{uid}">{qualified_address(corpus, artifact, section)}</a>'


def rewrite_markdown_text(text: str, owner: Path, corpus: Corpus) -> tuple[str, int]:
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

        def replace(match: re.Match[str]) -> str:
            nonlocal changed
            rendered = render_control_link(owner, corpus, match.group("uid"), match.group("label"))
            if rendered != match.group(0):
                changed += 1
            return rendered

        cursor = 0
        rendered_line: list[str] = []
        while cursor < len(line):
            tick = line.find("`", cursor)
            if tick == -1:
                rendered_line.append(CONTROL_LINK_RE.sub(replace, line[cursor:]))
                break
            rendered_line.append(CONTROL_LINK_RE.sub(replace, line[cursor:tick]))
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


def rewrite_markdown(path: Path, corpus: Corpus) -> int:
    text = read_text(path)
    rewritten, changed = rewrite_markdown_text(text, path, corpus)
    if changed:
        path.write_text(rewritten, encoding="utf-8")
    return changed


def rewrite_python(path: Path, corpus: Corpus) -> int:
    source = read_text(path)
    try:
        tree = ast.parse(source, filename=str(path))
    except SyntaxError as exc:
        raise CompilerError(f"Can't parse Python documentation in {path}: {exc}") from exc
    if not tree.body:
        return 0
    first = tree.body[0]
    if not (
        isinstance(first, ast.Expr)
        and isinstance(first.value, ast.Constant)
        and isinstance(first.value.value, str)
    ):
        return 0
    token = None
    for candidate in tokenize.generate_tokens(io.StringIO(source).readline):
        if candidate.type == tokenize.STRING and candidate.start[0] == first.value.lineno:
            token = candidate
            break
    if token is None:
        return 0
    literal = token.string
    prefix_match = re.match(r"(?i)^([rub]*)", literal)
    prefix = prefix_match.group(1) if prefix_match else ""
    rest = literal[len(prefix) :]
    quote_mark = next(
        (q for q in ("'''", '"""') if rest.startswith(q) and rest.endswith(q)),
        None,
    )
    if quote_mark is None:
        return 0
    body = rest[len(quote_mark) : -len(quote_mark)]
    rewritten, changed = rewrite_markdown_text(body, path, corpus)
    if not changed:
        return 0
    new_literal = prefix + quote_mark + rewritten + quote_mark
    lines = source.splitlines(keepends=True)
    start = source_offset(lines, token.start)
    end = source_offset(lines, token.end)
    path.write_text(source[:start] + new_literal + source[end:], encoding="utf-8")
    return changed


def rewrite_control_links(corpus: Corpus) -> int:
    changed = 0
    for path in sorted(walk_files(corpus.root), key=lambda p: repo_path(corpus.root, p).casefold()):
        suffix = path.suffix.lower()
        if suffix == ".md":
            changed += rewrite_markdown(path, corpus)
        elif suffix == ".py":
            changed += rewrite_python(path, corpus)
    return changed
