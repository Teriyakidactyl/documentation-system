#!/usr/bin/env python3
r'''---
uid: 45E225
architecture: '<a href="9%20%F0%9F%93%90%20Architecture/1%20%F0%9F%93%96%20Organizing%20Architecture.md" uid="55NHDB">documentation-system:§4.9.1</a>'
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
python3 "4 Tooling/1 🛠️ Navigation Crawler.py" refresh [corpus_root]
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
python3 "4 Tooling/1 🛠️ Navigation Crawler.py" inspect [corpus_root]
```

The current ordinal-hierarchy inspection reports each sibling ordinal sequence,
gaps, the complete compact normalization plan, and unmanaged literal path
references that could make structural renaming unsafe.

## 3. Normalize ordinal structure

Preview normalization first:

```text
python3 "4 Tooling/1 🛠️ Navigation Crawler.py" normalize [corpus_root]
```

The command is dry-run by default. Add `--apply` only after the reported plan
is acceptable:

```text
python3 "4 Tooling/1 🛠️ Navigation Crawler.py" normalize --apply [corpus_root]
```

Organizing refuses the apply operation when it finds literal repository-path
references outside UID-controlled links that it cannot prove safe to migrate.
When the filesystem transaction succeeds, Organizing refreshes indexes,
controlled links, and diagnostics against the new corpus state.

## 4. Resolve a locator

Resolve a current Documentation System locator without refreshing state:

```text
python3 "4 Tooling/1 🛠️ Navigation Crawler.py" resolve documentation-system:§2.1#4.2 [corpus_root]
```

The historical `--resolve ADDRESS` form remains accepted for compatibility.

## 5. Preserve capability boundaries

Treat the controlled `architecture` link in this module as direct provenance
to the code-local current Architecture Document. `_organizing` owns corpus
semantics and orchestration. `_capabilities` owns reusable representation
mechanics.

Requires PyYAML.
'''

from pathlib import Path

from _organizing.cli import main


if __name__ == "__main__":
    main(Path(__file__).resolve())
