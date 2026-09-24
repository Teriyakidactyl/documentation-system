#!/usr/bin/env python3
r'''---
architecture: '<a href="../6%20Software%20Design/2%20%F0%9F%93%96%20Organizing%20Architecture.md" uid="55NHDB">documentation-system:§6.2</a>'
description: >-
  `Read in full and follow when` *HTML elements, attributes, comments, or
  inline anchors must be inspected independently of Markdown or corpus
  semantics* `to` **parse HTML syntax into structured tokens and expose
  constrained anchor facts without assigning higher-level meaning to them**.
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
# 🛠️ HTML

Use HTML for syntax-level inspection. HTML owns elements, attributes, comments,
entities, and constrained anchor parsing. It does not decide that an attribute
such as `uid` represents a controlled identity; Organizing owns that meaning.

```text
python3 "4 Tooling/7 🛠️ HTML.py" inspect PATH
python3 "4 Tooling/7 🛠️ HTML.py" anchors PATH
```

`inspect` emits structural HTML tokens. `anchors` emits simple inline
`<a>text</a>` anchors with parsed attributes. The anchor surface is deliberately
constrained because it is also used by Organizing for controlled-reference
rewriting.
'''

from __future__ import annotations

import argparse
import json
from pathlib import Path

from _capabilities.html import anchors, inspect


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    show = sub.add_parser("inspect")
    show.add_argument("path", type=Path)
    show_anchors = sub.add_parser("anchors")
    show_anchors.add_argument("path", type=Path)
    args = parser.parse_args()

    text = args.path.read_text(encoding="utf-8")
    if args.command == "inspect":
        payload = [item.__dict__ for item in inspect(text)]
    else:
        payload = [
            {
                "start": item.start,
                "end": item.end,
                "attributes": dict(item.attributes),
                "text": item.text,
            }
            for item in anchors(text)
        ]
    print(json.dumps(payload, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
