---
uid: 55NHDB
description: >-
  `Consult when` *a Documentation Compiler responsibility, dependency,
  validation, or projection is being introduced or materially changed* `to`
  **place the change in the canonical compiler component and preserve one
  deterministic compilation pipeline without parallel sources of truth**.
quadrant: Reference
outline:
  topology: tree
  axis: compiler responsibility
  numbering: hierarchical-decimal
writing-style:
  formality: professional
  tone: clinical/detached
  mode: declarative
  density: compressed/dense
  abstraction: concrete/specific
  redundancy: zero
  signposting: entry-headers only
  register: technical
---

# 📖 Documentation Compiler Architecture

The Documentation Compiler is one controlled tool with one compilation
pipeline. The public Tooling artifact owns invocation and user-facing behavior;
the address-transparent `_compiler` package owns implementation stages.

Do not create an independent assembler, validator executable, projection tool,
or second corpus model when the responsibility belongs to this pipeline.

## 1. Architecture contract

Use one public compiler entry point. Treat `_compiler` as an operational
implementation package rather than a Documentation System location; its modules
carry ordinary Python docstrings and are not independently indexed artifacts.

The controlled entry point carries an `architecture` link to this document.
Internal modules inherit this architecture and state their local responsibility
rather than repeating the governing design principles.

The current repository keeps the historical Navigation Crawler filename only as
an automation-compatibility constraint. **Documentation Compiler** is the
canonical tool and concept name.

## 2. Canonical components

### 2.1 Corpus model

`model.py` owns metadata adapters, normalized `Artifact`, `HeadingTarget`,
and `Corpus` values, UID identity, corpus-root-relative location derivation,
address parsing and rendering, Git repository root discovery, and corpus
construction.

A `Corpus` carries the corpus-root declaration selected for the current
compiler job as its `corpus_root` fact. That fact is job-local runtime state,
not a permanent designation of the filesystem directory. Address rendering declares
the same role in address syntax by using the selected directory's name before
`:`; the `§` location is derived from descendants relative to that directory.
Do not carry a persistent or second corpus-root fact beside the job-local
corpus-root declaration.

Model objects carry facts. They do not compile indexes, rewrite links, emit
diagnostics, or choose presentation policy.

### 2.2 Diagnostics

`diagnostics.py` owns `Diagnostic`, severity, validators, and diagnostic
projections.

Validators report observed violations without silently repairing semantic
content. The same diagnostic may be rendered to the console, GitHub Actions,
machine-readable JSON, or an optional compiler-owned inline annotation.

### 2.3 Index projection

`indexes.py` owns validation and rendering of compiler-owned
`BEGIN index` / `END index` regions.

Indexes derive only from the normalized corpus and filesystem classification;
they do not become another authored topology.

### 2.4 Controlled links

`links.py` owns UID-controlled target resolution and mechanical rewriting of
the current `href` and displayed address.

The UID is authority for target identity within the selected corpus. The
displayed address is a projection of the current corpus-root declaration,
corpus-root-relative location, and optional numbered section. Controlled links
reject a displayed value that omits the corpus-root declaration, but a stale
address may be rewritten after the corpus-root declaration or target location
changes because UID identity remains authoritative.

### 2.5 Compilation engine

`engine.py` owns pass ordering and passes the normalized corpus between
stages. It does not absorb subsystem-specific parsing, validation, rendering,
or presentation behavior.

### 2.6 Command line

`cli.py` owns invocation, exit policy, address-resolution output, selection
of diagnostic projections, and the job-local corpus-root declaration. A
supplied `corpus_root` path declares which directory serves that role for the
job; when omitted, the CLI declares the Git repository root containing the
compiler.

The command line orchestrates compiler behavior; it does not invent a second
corpus-root setting.

## 3. Compilation pipeline

Use this canonical order:

```text
select corpus root
-> clear stale inline diagnostics
-> mint missing UIDs
-> build corpus model
-> compile deterministic projections
-> rebuild corpus model
-> rewrite UID-controlled links
-> rebuild corpus model
-> validate compiled state
-> emit selected diagnostic projections
```

A pass may write only the representation it owns. Rebuild the corpus model
after a pass whose writes can change facts consumed by a later pass.

Future Element projection belongs in the deterministic-projection stage before
controlled-link rewriting so projected controlled links can be refreshed in
their consuming context.

## 4. Diagnostic contract

Use `ERROR`, `WARNING`, and `INFO` as the external severity vocabulary.

- **ERROR** means a valid deterministic result cannot be established and the
  compiler exits unsuccessfully.
- **WARNING** means the compiled corpus is valid but a condition requires
  attention.
- **INFO** records a useful non-failing observation.

Each diagnostic carries a stable code, severity, path, line, and concrete
message. Keep the `Diagnostic` value canonical; console output, GitHub
annotations, JSON, and inline source comments are projections of that value.

Inline annotations are compiler-owned ordinary HTML comments such as:

```markdown

```

A normal compile removes stale compiler-owned diagnostic comments before
validation. `--annotate` projects the current diagnostics beside offending
source for an editor or agent. Do not author those comments manually.

## 5. Dependency rules

Keep dependencies directed from orchestration toward specialized stages and
shared facts:

```text
CLI -> engine -> passes
             -> normalized Corpus
validators -> Diagnostic
presenters -> Diagnostic
```

Share corpus facts through the normalized model rather than hidden mutable
state between passes. Keep cross-artifact invariants in validation when no
single artifact legitimately owns them. Derive addresses from the job-local
corpus-root declaration; do not introduce another authored or computed
corpus-root source of truth.

Do not move compiler behavior onto data objects merely to make those objects
richer. Do not create a class hierarchy that mirrors the module layout.

## 6. Evolution

Add a compiler capability when canonical inputs and declarations determine one
output without contextual interpretation. If producing the output requires
choosing among plausible meanings, reconciling authority, or adapting semantics
to context, keep that work authored.

Add another internal module when a responsibility has an independent reason to
change and a stable boundary. Do not split one function per file for symmetry.

Add another public executable only when the new capability has an independent
lifecycle and cannot remain a pass in this compiler without violating this
architecture.

Do not reserve compiler modules, persistence adapters, or command-line
operations for a possible future capability before a concrete requirement
selects that representation. Preserve candidate designs in the information
store appropriate to their current role rather than making speculative
implementation part of the active architecture.
