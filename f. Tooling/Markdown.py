#!/usr/bin/env python3
r'''---
uid: XS6515
architecture: '<a href="%F0%9F%93%90%20Architecture/%F0%9F%93%96%20Tooling%20Architecture.md" uid="K7W3P9">documentation-system:§f.d.2</a>'
description: >-
  `Read in full and follow when` *Markdown structure must be inspected, linted,
  mechanically corrected, or locally renumbered* `to` **give an agent bounded
  section access, deterministic diagnostics, safe formatting fixes, and stable
  document-local coordinates around authored edits**.
quadrant: HowTo
outline:
  topology: branching
  axis: operation
writing-style:
  formality: professional
  tone: neutral/detached
  mode: imperative
  density: moderate
  abstraction: concrete/specific
  redundancy: zero
  signposting: light
  register: technical
---
# 🛠️ Markdown

Use Markdown as structural perception and deterministic feedback around an
authored edit. The shared capability uses markdown-it-py as its structural
parser and exposes repository-owned heading, section, fenced-block, and source
coordinate values rather than parser-specific tokens. PyMarkdownLnt remains the
separate generic lint-and-fix engine.

The default lint policy is selective: PyMarkdown rules are disabled as a set
and only explicit Documentation System defaults are enabled, so a dependency
upgrade cannot silently add a house opinion. Documentation-System-specific
rules consume the shared structural model when Markdown semantics matter.

```text
python3 "f. Tooling/Markdown.py" headings PATH
python3 "f. Tooling/Markdown.py" sections PATH
python3 "f. Tooling/Markdown.py" get-section PATH SELECTOR
python3 "f. Tooling/Markdown.py" lint PATH
python3 "f. Tooling/Markdown.py" fix PATH
python3 "f. Tooling/Markdown.py" rules
python3 "f. Tooling/Markdown.py" renumber [--write] PATH
```

`lint` is read-only. `fix` applies only deterministic PyMarkdown autofixes; coordinate renumbering
remains an explicit operation because higher-level references may depend on the
old coordinates. Unresolved findings remain for the agent. `rules`
is the executable source of truth for default lint opinions.

The defaults deliberately do not impose line length, forbid HTML, forbid
heading punctuation, or require generic blank lines beneath headings. Those
would conflict with controlled anchors, metamatter placement, or valid
technical-writing forms.

Markdown owns document-local structure and coordinates. Organizing owns how
those coordinates participate in controlled corpus references.

Structural inspection, lint, and fix require the dependencies declared by
Tooling `requirements.txt`. When an import is unavailable, prepare the
repository-local Tooling environment
before retrying; do not install the dependency into the operating system's
Python installation.
'''

from __future__ import annotations

import argparse
import json
from pathlib import Path

from _capabilities.frontmatter import FrontmatterError, load as load_frontmatter
from _capabilities.markdown import MarkdownError, get_section, headings, renumber, sections
from _capabilities.markdown_lint import MarkdownLintError, fix_file, lint_file, rule_policy


def markdown_body(path: Path) -> tuple[str, str]:
    source = path.read_text(encoding="utf-8")
    try:
        frontmatter = load_frontmatter(path)
    except FrontmatterError as exc:
        raise SystemExit(f"markdown: {exc}") from exc
    if frontmatter is None:
        return "", source
    return source[: len(source) - len(frontmatter.body)], frontmatter.body


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    show = sub.add_parser("headings")
    show.add_argument("path", type=Path)
    list_sections = sub.add_parser("sections")
    list_sections.add_argument("path", type=Path)
    get = sub.add_parser("get-section")
    get.add_argument("--no-heading", action="store_true")
    get.add_argument("path", type=Path)
    get.add_argument("selector")
    lint = sub.add_parser("lint")
    lint.add_argument("path", type=Path)
    fix = sub.add_parser("fix")
    fix.add_argument("path", type=Path)
    sub.add_parser("rules")
    number = sub.add_parser("renumber")
    number.add_argument("--write", action="store_true")
    number.add_argument("path", type=Path)
    args = parser.parse_args()

    if args.command == "rules":
        print(json.dumps(rule_policy(), indent=2, ensure_ascii=False))
        return
    if args.command == "lint":
        try:
            diagnostics = lint_file(args.path)
        except MarkdownLintError as exc:
            raise SystemExit(f"markdown: {exc}") from exc
        print(json.dumps({"path": str(args.path), "diagnostics": [item.to_dict() for item in diagnostics]}, indent=2, ensure_ascii=False))
        raise SystemExit(1 if diagnostics else 0)
    if args.command == "fix":
        try:
            diagnostics, changed = fix_file(args.path)
        except MarkdownLintError as exc:
            raise SystemExit(f"markdown: {exc}") from exc
        print(json.dumps({"path": str(args.path), "changed": changed, "diagnostics": [item.to_dict() for item in diagnostics]}, indent=2, ensure_ascii=False))
        raise SystemExit(1 if diagnostics else 0)

    prefix, text = markdown_body(args.path)
    if args.command == "headings":
        print(json.dumps(headings(text), indent=2, ensure_ascii=False))
        return
    if args.command == "sections":
        print(json.dumps([item.__dict__ for item in sections(text)], indent=2, ensure_ascii=False))
        return
    if args.command == "get-section":
        try:
            print(get_section(text, args.selector, include_heading=not args.no_heading), end="")
        except MarkdownError as exc:
            raise SystemExit(f"markdown: {exc}") from exc
        return
    try:
        rendered, mapping = renumber(text)
    except MarkdownError as exc:
        raise SystemExit(f"markdown: {exc}") from exc
    if args.write and rendered != text:
        args.path.write_text(prefix + rendered, encoding="utf-8")
    print(json.dumps({"changed": rendered != text, "mapping": mapping, "written": args.write}, indent=2))


if __name__ == "__main__":
    main()
