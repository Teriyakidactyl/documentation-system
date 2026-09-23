#!/usr/bin/env python3
r'''---
uid: 45E225
architecture: '<a href="../6%20Software%20Design/2%20%F0%9F%93%96%20Documentation%20Compiler%20Architecture.md" uid="55NHDB">documentation-system:§6.2</a>'
description: >-
  `Read in full and follow when` *a Documentation System corpus may have changed
  or an address must be resolved* `to` **compile derived control state, validate
  durable references, refresh projections and controlled links, or resolve the
  requested address without hand-maintaining derived information**.
quadrant: HowTo
outline:
  topology: linear
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
# 🛠️ Documentation Compiler

Use the Documentation Compiler as the single public entry point for corpus
compilation and address resolution. Its `_compiler` package owns implementation
stages; do not invoke those modules as independent tools.

The current repository filename is retained temporarily as a compatibility
entry point for existing automation. **Documentation Compiler** is the canonical
tool name.

## 1. Compile the corpus

Run the compiler after controlled classification, recognized metadata, numbered
headings, generated-index membership, controlled links, or compiler-owned
projections may have changed.

```text
python3 "4 Tooling/1 🛠️ Navigation Crawler.py" [corpus_root]
```

The positional `corpus_root` path declares which filesystem directory serves
as the corpus root for this compiler job. The designation exists for that job;
it is not stored on or permanently assigned to the directory. When the argument
is omitted, the job declares the root of the Git repository containing this
tool. An explicit path overrides that default.

Each documentation address separately declares its corpus root by directory
name before `:`. For a job selecting a directory named
`documentation-system`, generated addresses therefore begin
`documentation-system:§...`. No second corpus-root designation is configured
or stored in metadata. `§...` without a corpus-root declaration is location notation and is invalid
where a documentation address is required. Renaming the directory
serving as corpus root changes the corpus-root declaration in addresses that
use it; moving that directory beneath a different ancestor without renaming it
does not.

A successful run refreshes deterministic projections and controlled links,
then evaluates structured diagnostics. Errors make the run fail; warnings and
info remain successful unless a future invocation policy explicitly promotes
them.

## 2. Project diagnostics beside source

Use `--annotate` when an editor or agent benefits from diagnostics immediately
beside the offending source.

```text
python3 "4 Tooling/1 🛠️ Navigation Crawler.py" --annotate [corpus_root]
```

The compiler owns comments beginning `ERROR DS`, `WARNING DS`, or `INFO DS` and
removes stale compiler annotations before each normal compile. Do not author
those comments manually.

Use `--diagnostics-json PATH` when another tool needs the same diagnostics as
machine-readable data.

## 3. Resolve an address

Use `--resolve` for read-only address resolution.

```text
python3 "4 Tooling/1 🛠️ Navigation Crawler.py" --resolve documentation-system:§2.1#4.2 [corpus_root]
```

The address must declare the compiler job's corpus root by directory name before
`:`; `--resolve §2.1` is a syntax error because `§2.1` is only location
notation.
Resolution returns JSON for the addressed document, location, or numbered
section without compiling derived state.

## 4. Preserve the architecture boundary

Treat the controlled `architecture` link in this module's metadata as the
normative software-architecture provenance for the tool. Internal `_compiler`
modules inherit that architecture and state only their local responsibility in
ordinary module docstrings.

Requires PyYAML.
'''

from pathlib import Path

from _compiler.cli import main


if __name__ == "__main__":
    main(Path(__file__).resolve())
