#!/usr/bin/env python3
r'''---
uid: XS6515
architecture: '<a href="%F0%9F%93%90%20Architecture/%F0%9F%93%96%20Software%20Architecture.md" uid="K7W3P9">documentation-system:§d.g.2</a>'
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
python3 "d. Software/Markdown.py" headings PATH
python3 "d. Software/Markdown.py" sections PATH
python3 "d. Software/Markdown.py" get-section PATH SELECTOR
python3 "d. Software/Markdown.py" lint PATH
python3 "d. Software/Markdown.py" fix PATH
python3 "d. Software/Markdown.py" rules
python3 "d. Software/Markdown.py" renumber [--write] PATH
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
Software `requirements.txt`. When an import is unavailable, prepare the
repository-local Software environment
before retrying; do not install the dependency into the operating system's
Python installation.
'''

from interfaces.cli.markdown import main


if __name__ == "__main__":
    main()
