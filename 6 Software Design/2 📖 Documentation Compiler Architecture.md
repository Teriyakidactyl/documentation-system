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
and `Corpus` values, UID identity, the compiler-owned address-space name,
address derivation, Git repository root discovery, and corpus construction.

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

The UID is authority for target identity. The rendered address is a projection
of current corpus structure.

### 2.5 Compilation engine

`engine.py` owns pass ordering and passes the normalized corpus between
stages. It does not absorb subsystem-specific parsing, validation, rendering,
or presentation behavior.

### 2.6 Command line

`cli.py` owns invocation, exit policy, address-resolution output, and
selection of diagnostic projections.

The command line orchestrates compiler behavior; it does not own corpus rules.

### 2.7 Validation evidence

When durable validation evidence is implemented, keep receipt semantics and
storage mechanics in separate internal modules.

`receipts.py` owns the validation-evidence domain: validation basis,
schema-valid receipt values, producer kind, typed coverage, canonical
serialization, receipt invariants, and current-versus-stale applicability
semantics. It does not invoke Git or decide command-line presentation.

`git_notes.py` owns the Git persistence adapter: resolve the exact Git object
state for a controlled subject, read and write the selected validation-notes
namespace, and return stored representations to the receipt layer. It does not
decide whether a receipt is semantically admissible and does not make Git object
identity replace Documentation System `uid` identity.

Use Git Notes as the selected persistence mechanism for durable validation
receipts because receipt updates must not mutate the validated artifact merely
to record that validation occurred. Keep the storage namespace and Git commands
behind this adapter.

Do not persist ordinary compiler or lint success on every run. Deterministic
validation remains authoritative by recomputation when it is cheap. A tool
receipt is persisted only when a concrete requirement makes the run itself
valuable evidence, such as expensive execution, environment-specific
provenance, release attestation, or compliance evidence.

A validation-status operation combines applicable durable receipts with
recomputed deterministic checks. It exposes domain states such as current,
stale, findings, uncertain, and not evaluated; it does not project a blanket
`validated: true` fact onto the subject.

## 3. Compilation pipeline

Use this canonical order:

```text
clear stale inline diagnostics
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
             -> validation status
validators -> Diagnostic
receipts -> validation evidence values
git_notes -> receipt persistence
presenters -> Diagnostic
```

Share corpus facts through the normalized model rather than hidden mutable
state between passes. Keep cross-artifact invariants in validation when no
single artifact legitimately owns them.

Keep dependencies directed from receipt semantics toward abstract subject/frame
facts and from the Git adapter toward receipt serialization. `receipts.py`
must not import Git persistence. `git_notes.py` may persist only receipt
representations that have passed receipt validation. The engine coordinates
basis resolution, deterministic rechecks, receipt lookup, and status assembly.

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

Expose future validation-evidence operations through the existing compiler
entry point unless an independent lifecycle is demonstrated. User-facing
commands name Validation concepts such as receipt and status; they do not
require callers to manipulate Git refs, note namespaces, or object identifiers
directly.
