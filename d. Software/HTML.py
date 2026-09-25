#!/usr/bin/env python3
r'''---
uid: PPVYWD
architecture: '<a href="docs/%F0%9F%93%96%20Software%20Architecture.md" uid="K7W3P9">documentation-system:§d.c.2</a>'
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
python3 "d. Software/HTML.py" inspect PATH
python3 "d. Software/HTML.py" anchors PATH
```

`inspect` emits structural HTML tokens. `anchors` emits simple inline
`<a>text</a>` anchors with parsed attributes. The anchor surface is deliberately
constrained because it is also used by Organizing for controlled-reference
rewriting.
'''

from repo_manager.interfaces.cli.html import main


if __name__ == "__main__":
    main()
