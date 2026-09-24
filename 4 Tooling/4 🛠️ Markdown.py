#!/usr/bin/env python3
r'''---
uid: XS6515
architecture: '<a href="../6%20Software%20Design/2%20%F0%9F%93%96%20Organizing%20Architecture.md" uid="55NHDB">documentation-system:§6.2</a>'
description: >-
  `Read in full and follow when` *Markdown heading structure must be
  inspected or hierarchical heading numbers have drifted* `to` **read the
  structural heading model or deterministically regenerate local heading
  coordinates without treating corpus addresses as heading numbers**.
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

Use `headings` to inspect Markdown structure. Use `renumber` to derive
hierarchical-decimal H2-H6 numbering from heading depth and source order.
Renumbering is dry-run by default; add `--write` to replace the file.

```text
python3 "4 Tooling/4 🛠️ Markdown.py" headings PATH
python3 "4 Tooling/4 🛠️ Markdown.py" renumber [--write] PATH
```

Markdown owns document-local section coordinates. Organizing owns how those
coordinates participate in controlled corpus references.
'''

from __future__ import annotations

import argparse
import json
from pathlib import Path

from _capabilities.markdown import MarkdownError, get_section, headings, renumber, sections
from _capabilities.markdown_lint import MarkdownLintError, fix_file, lint_file, rule_policy


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

    text = args.path.read_text(encoding="utf-8")
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
        args.path.write_text(rendered, encoding="utf-8")
    print(json.dumps({"changed": rendered != text, "mapping": mapping, "written": args.write}, indent=2))


if __name__ == "__main__":
    main()
