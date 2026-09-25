---
uid: 91ZTQW
description: >-
  `Consult when` *an Architecture Document instance is being authored or
  reviewed for conformance* `to` **confirm its current-authority role,
  code-local placement, Form provenance, required semantic sections, and
  separation from historical decision rationale**.
quadrant: Reference
outline:
  topology: list
  axis: architecture document facet
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

# 📖 Architecture Document

An Architecture Document expresses the current implemented architecture of one
governed software scope. It is current design authority, not a chronological
decision log, implementation transcript, or speculative future-state proposal.

Reusable architectures published under Software Design are not instances of this
Form. They define reusable design contracts; this Form governs the code-local
document that states how an actual implementation is architected.

## 1. Placement and filename

Store the document in the `📐 Architecture/` store at the stable root of the
implementation it governs, following any representation required by the host
repository's organization scheme.

Use:

~~~text
<Subject> Architecture.md
~~~

after any organization-scheme prefix required by the containing corpus.

The H1 is:

~~~markdown
# 📖 <Subject> Architecture
~~~

Name the architectural subject rather than the repository, author, decision
date, or implementation technology unless that technology is itself the
architectural subject.

## 2. Frontmatter

Every Architecture Document carries:

~~~yaml
uid: <Organizing-minted>
form:
  path: '<controlled link to the Architecture Document Form package>'
  version: '<major.minor contract used by this document>'
description: >-
  <routing statement naming the governed implementation and architectural work encounter>
quadrant: Reference
outline:
  topology: tree
  axis: <architecture-specific organizing axis>
  numbering: hierarchical-decimal
writing-style:
  formality: professional
  tone: clinical/detached
  mode: declarative
  density: compressed/dense
  abstraction: concrete/specific | mixed
  redundancy: zero
  signposting: entry-headers only
  register: technical
~~~

The Architecture Document does not require decision-status metadata. Git history
records document changes; ADRs separately preserve decision provenance when
that history has a continuing job.

## 3. Required sections

Use these H2 sections in order:

~~~markdown
## 1. Scope
## 2. Drivers
## 3. Architecture
## 4. Realization
## 5. Verification
## 6. Evolution
~~~

Additional H3 and deeper structure is selected by the architecture itself. Do
not create universal subsections for concerns that are irrelevant to the
governed design.

### 3.1 Scope

Identify the implementation governed by the document and the boundary of that
authority.

State relationships to enclosing or narrower architectures when scopes overlap.
A reader starting from governed code must be able to determine that this
document applies without inferring the answer from implementation resemblance.

### 3.2 Drivers

State only the requirements, constraints, consumers, quality goals, external
conditions, and selected reusable architectures that materially shape the
design.

Drivers explain what the architecture must satisfy now. Historical deliberation
and rejected alternatives belong in ADRs when their rationale must be retained.

### 3.3 Architecture

State the durable design commitments: responsibilities, ownership, canonical
state, relationships, interactions, invariants, boundaries, and other decisions
that future implementation work must preserve or deliberately change.

Organize this section around the governed system. Diagrams, tables, dependency
lists, flows, or other representations are selected only when they communicate a
load-bearing relationship more clearly than prose.

Distinguish fixed architectural commitments from incidental implementation
details.

### 3.4 Realization

Map architectural concepts to recognizable implementation evidence.

Name stable code boundaries such as public entry points, packages, modules,
interfaces, schemas, registries, persistence boundaries, processes, or
configuration surfaces when those mappings let a maintainer locate the
realization directly.

Do not turn Realization into a file inventory. Include an implementation detail
only when it evidences an architectural claim or establishes the place future
changes belong.

### 3.5 Verification

State how architectural obligations are proved and where that evidence can be
executed or inspected.

Separate mechanically decidable conformance from semantic review. Identify
unverified architectural obligations explicitly rather than presenting prose as
proof.

### 3.6 Evolution

State the supported extension points, allowed variation, selecting conditions
for known alternatives, and boundaries that may change independently.

Use this section to prevent current implementation details from being mistaken
for permanent architecture and permanent architecture from being treated as
optional convention.

## 4. Reusable architecture selection

When the implementation selects a reusable Software Design architecture, name
it in Drivers and record the local realization and verification evidence in the
corresponding sections.

A link to a reusable architecture does not replace the local Architecture
Document. The reusable architecture states the general contract; the local
document states where that contract applies and how the implementation realizes
it.

Do not claim conformance based only on resemblance.

## 5. Authority boundary

Keep current architecture in the Architecture Document.

Use ADRs for retained decision rationale, research for retained investigation
evidence, plans for future intended work, tests for executable evidence, and
code for implementation. Link those artifacts when useful without asking any
one of them to substitute for the architecture authority.

An Architecture Document may summarize a driver already owned elsewhere, but
should link to the owning authority instead of copying a changing specification
into architectural prose.

## 6. Completion condition

An Architecture Document is complete when an unfamiliar maintainer can
determine:

- what implementation it governs;
- which forces and reusable designs materially constrain that implementation;
- what architectural commitments must remain true;
- where those commitments are realized in code;
- how they are verified;
- what variation and extension remain intentionally open; and
- where to look for historical rationale if a consequential choice must be
  revisited.

Completeness does not require describing every architecture viewpoint or
software-design concern. It requires enough current authority to prevent
architectural reconstruction from implementation clues.
