#!/usr/bin/env python3
r'''---
uid: 45E225
architecture: '<a href="%F0%9F%93%90%20Architecture/%F0%9F%93%96%20Organizing%20Architecture.md" uid="55NHDB">documentation-system:§d.c.1</a>'
description: >-
  `Read in full and follow when` *a controlled corpus must be refreshed,
  inspected, resolved, or structurally normalized* `to` **maintain stable
  identities, organization-scheme invariants, navigation projections, and
  controlled references through deterministic corpus operations**.
quadrant: HowTo
outline:
  topology: branching
  axis: operation
  numbering: hierarchical-decimal
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
# 🛠️ Organizing

Use Organizing for corpus-wide control operations. Folder, Markdown,
Frontmatter, and YAML remain independently routable peer tools; Organizing
calls their implementation capabilities when a corpus operation needs them.

The historical `Navigation Crawler.py` filename remains an automation-compatibility
constraint. **Organizing** is the canonical tool and concept name.

## 1. Refresh organized state

Run `refresh` after controlled identity, organization, generated navigation,
or controlled references may have changed:

```text
python3 "d. Software/Navigation Crawler.py" refresh [corpus_root]
```

For compatibility, omitting the subcommand still means `refresh`.

Refresh establishes missing UIDs, refreshes structured Element filepaths,
renders dynamic Index Elements, refreshes UID-controlled links, and reports
organization diagnostics. Index rendering uses heading-bounded Element
metamatter rather than generated-region marker comments. Use `--annotate`
or `--diagnostics-json PATH` with `refresh` when another surface needs the
same diagnostics.

## 2. Inspect organization

Use `inspect` to see organization-scheme facts without mutation:

```text
python3 "d. Software/Navigation Crawler.py" inspect [corpus_root]
```

Inspection reports each effective inherited `.folder.json` namespace, the
complete normalization plan, deterministic literal-path migrations, and any
ambiguous references that would block safe mutation.

## 3. Normalize folder conventions

Preview normalization first:

```text
python3 "d. Software/Navigation Crawler.py" normalize [corpus_root]
```

The command is dry-run by default. Add `--apply` only after the reported plan
is acceptable:

```text
python3 "d. Software/Navigation Crawler.py" normalize --apply [corpus_root]
```

For convention-managed corpora, Refresh first executes the complete mutation and
refresh against a temporary copy. The real tree is changed only when staged
normalization, path migration, corpus construction, indexes, controlled links,
and diagnostics are valid. Ambiguous path references fail rather than being
guessed through.

## 4. Resolve a locator

Resolve a current Documentation System locator without refreshing state:

```text
python3 "d. Software/Navigation Crawler.py" resolve documentation-system:§2.1#4.2 [corpus_root]
```

The historical `--resolve ADDRESS` form remains accepted for compatibility.

## 5. Preserve capability boundaries

Treat the controlled `architecture` link in this module as direct provenance
to the code-local current Architecture Document. `automation/organizing`
owns corpus semantics and orchestration. `capabilities` owns reusable
representation mechanics.

Requires PyYAML.
'''

from pathlib import Path

import sys
from repo_manager.interfaces.cli.organizing import main


if __name__ == "__main__":
    argv=list(sys.argv[1:])
    if not argv:
        argv=["refresh"]
    elif argv[0]=="--resolve":
        argv=["resolve",*argv[1:]]
    elif argv[0] not in {"refresh","inspect","resolve","normalize","-h","--help"}:
        argv=["refresh",*argv]
    main(argv)
