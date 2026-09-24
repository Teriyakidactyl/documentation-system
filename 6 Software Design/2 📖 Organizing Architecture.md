---
uid: 55NHDB
description: >-
  `Consult when` *the Organizing tool, an organization scheme, a peer
  representation capability, a validation rule, a projection, or a structural
  refactor is being introduced or materially changed* `to` **place
  responsibility with the owning capability while preserving one normalized
  corpus and one deterministic organization workflow**.
quadrant: Reference
outline:
  topology: tree
  axis: organizing responsibility
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

# 📖 Organizing Architecture

Organizing maintains the correspondence between stable controlled identities,
their organization, and the derived representations through which readers and
tools find them.

The public Organizing tool owns corpus-wide orchestration. Folder, Markdown,
Frontmatter, YAML, and HTML are peer capabilities with independently routable work
encounters. Organizing may call those capabilities when an organization
operation requires their representation knowledge. A dependency does not make
one capability a child of another in Tooling navigation.

## 1. Architecture contract

Keep one normalized corpus model and one public Organizing entry point for
corpus-wide organization operations. Do not create a second corpus model,
parallel link authority, independent index assembler, or filesystem refactorer
that reconstructs organization semantics separately.

Treat `_organizing` as an address-transparent implementation package beneath
the controlled Organizing entry point. Treat `_capabilities` as reusable
representation-level behavior used by Organizing and by independently routable
peer tools.

A peer capability owns its representation semantics. Organizing owns how those
representations participate in one controlled corpus.

## 2. Identity, organization, and locators

Keep durable identity independent from current organization.

```text
uid
 └── identifies controlled artifact
      └── participates in organization scheme
           ├── membership and topology
           ├── representation constraints
           └── locator projection, when the scheme defines one
```

The UID remains authority for artifact identity across moves, renames, and
organization changes.

An **organization scheme** defines how controlled artifacts participate in an
organized structure. A scheme may define membership rules, naming constraints,
relationships, ordering, and a locator notation. Do not require every future
scheme to produce decimal locations merely because the current scheme does.

A **locator** is a current coordinate projected by a scheme. It is not durable
identity. The current ordinal-hierarchy scheme projects filesystem ordinals as
`§` locations and can extend an addressed document with a Markdown-local
numbered section after `#`.

A controlled reference binds durable UID identity to the current physical and
locator projections required by its representation. The UID selects the target;
the organization scheme and local representation determine what should be
displayed and linked now.

## 3. Peer capabilities

### 3.1 Folder

Folder owns filesystem path inspection and collision-safe path mutation. It
does not decide what a path means to a corpus or which ordinal a sibling should
receive.

Organizing supplies an already-decided rename or move plan. Folder verifies the
transaction can be applied without clobbering unrelated paths and performs the
filesystem mutation.

### 3.2 Markdown

Markdown owns Markdown structure: headings, sections, anchors, local heading
numbering, and mechanically decidable Markdown structural validation.

Markdown may return an old-to-new local section mapping after deterministic
normalization. Organizing consumes that mapping when controlled references must
be refreshed. Markdown does not own corpus locations or UIDs.

### 3.3 Frontmatter

Frontmatter owns the metadata envelope carried by a host artifact: locating,
extracting, updating, and preserving the boundary between metadata and body.

Frontmatter consumes YAML for YAML payload semantics. That implementation
dependency does not make YAML subordinate in Tooling navigation.

### 3.4 YAML

YAML owns generic YAML parsing, serialization, and mechanically decidable YAML
validation. It does not know frontmatter, controlled artifacts, UIDs, or
organization schemes.

YAML remains independently routable because pure YAML is a valid work encounter
even when no frontmatter or Documentation System corpus is involved.

### 3.5 HTML

HTML owns generic element, attribute, comment, entity, and constrained anchor
parsing. It does not know that a `uid` attribute is a controlled identity or
that an anchor represents a Documentation System reference.

Markdown may use HTML to understand raw HTML carried by Markdown. Organizing may
use HTML when a controlled representation is encoded as HTML. HTML remains
independently routable because inspecting an HTML fragment or file is a coherent
work encounter without Markdown or corpus semantics.

## 4. Ordinal hierarchy scheme

The currently implemented organization scheme is **ordinal hierarchy**.

Its filesystem representation reads a local numeric ordinal from each numbered
directory or numbered artifact name. The ordinal path beneath the selected
corpus root projects the `§` location.

The scheme owns:

- ordinal syntax and extraction;
- sibling ordinal uniqueness;
- ordinal-sequence inspection;
- deterministic compact resequencing;
- location derivation;
- the relationship between physical hierarchy and `§` location.

A gap such as `1, 2, 4, 5` is diagnosable without guessing semantic meaning.
Normalization may plan `4 -> 3` and shift later peers accordingly. The plan
must be complete before the first rename occurs.

Do not generalize ordinal-only invariants into universal controlled-artifact
rules. A later supported scheme may use names, tags, another notation, or no
positional locator. Add that scheme only when a concrete requirement selects
it.

## 5. Corpus components

### 5.1 Model

Model values carry normalized facts such as controlled artifact identity,
metadata, body, current organization facts, and corpus relationships. They do
not perform filesystem mutation, rewrite references, render indexes, or emit
diagnostics.

### 5.2 Corpus construction

Corpus construction discovers supported controlled artifacts, applies the
selected organization scheme, validates unique identities and coordinates, and
produces the normalized corpus consumed by later passes.

Source-format adapters may call Frontmatter, Markdown, YAML, or HTML. Do not copy
those representation parsers into the corpus model.

### 5.3 Navigation projections

Index projection derives reader navigation from the normalized corpus. An index
is a projection of current organization, never a second authored topology.

### 5.4 Controlled references

Controlled-reference processing owns UID target resolution and mechanical
refresh of physical links and displayed locators.

A stale location is repairable when UID identity remains valid. A missing or
ambiguous UID, invalid locator syntax, or unresolved local section is not
repairable by guessing.

### 5.5 Diagnostics

Each capability evaluates invariants it legitimately owns and returns
structured diagnostics. Organizing collects corpus-wide findings and presents
them consistently.

Keep one diagnostic value with stable code, severity, path, line, and concrete
message. Console output, GitHub Actions annotations, JSON, and optional inline
comments are projections of that value.

## 6. Organizing operations

### 6.1 Refresh

Refresh reconciles deterministic derived state with current canonical sources:

```text
select corpus root
-> clear stale inline diagnostics
-> establish controlled identities
-> build normalized corpus
-> refresh deterministic navigation projections
-> rebuild corpus
-> refresh UID-controlled references
-> rebuild corpus
-> validate organized state
-> emit selected diagnostic projections
```

A pass may write only the representation it owns. Rebuild the corpus after a
write that changes facts consumed by a later pass.

### 6.2 Inspect

Inspect exposes organization facts and violations without changing the corpus.
Use it to debug how paths become locations, identify ordinal gaps, and view the
normalization plan implied by the selected scheme.

### 6.3 Resolve

Resolve maps a supported locator to its current controlled artifact, location,
or local section without refreshing derived state.

### 6.4 Normalize

Normalize plans a deterministic structural refactor of the selected
organization scheme. Dry-run is the default.

Before applying a rename plan:

1. derive the complete old-to-new filesystem and locator mapping;
2. reject duplicate sources, duplicate destinations, or unrelated destination
   collisions;
3. identify unmanaged literal path references that UID-controlled reference
   repair cannot prove safe;
4. stop rather than mutate when an unmanaged dependency remains.

When the plan is safe to apply, Folder performs the collision-safe filesystem
transaction. Organizing then rebuilds the corpus, refreshes navigation and
UID-controlled references, and validates the resulting state.

Normalization does not decide that two concepts should exchange semantic
positions. It only applies an organization change already determined by the
selected scheme or an explicit caller decision.

## 7. Dependency rules

Keep semantic ownership and implementation dependency distinct:

```text
Organizing CLI -> organizing engine
               -> organization scheme
               -> corpus model
               -> indexes
               -> controlled references
               -> diagnostics
               -> Folder
               -> Markdown
               -> Frontmatter -> YAML
               -> HTML
               -> Markdown -> HTML

YAML        <- independently routable
HTML        <- independently routable
Frontmatter <- independently routable
Markdown    <- independently routable
Folder      <- independently routable
```

Share normalized facts through explicit values rather than hidden mutable state.
Do not infer a Tooling hierarchy from the import graph.

## 8. Evolution

Add a deterministic capability when canonical inputs and declarations select
one output without contextual interpretation. Keep semantic choices authored
when several meanings remain plausible.

Add an internal module when a responsibility has an independent reason to
change and a stable boundary. Do not split one function per file for symmetry.

Add another public Tooling artifact when the work encounter is independently
routable and useful without entering Organizing. Do not require an independent
package or release lifecycle merely because a capability deserves a separate
routing surface.

Add another organization scheme only when a real corpus requires behavior the
current scheme cannot represent without distorting its meaning.
