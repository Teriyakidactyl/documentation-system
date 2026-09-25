---
uid: 1SGQXT
description: >-
  `Consult when` *software design must be specified, a recurring design
  concern must be resolved, a reusable design must be selected, or the
  relationship between reusable specification and a live implementation must
  be understood* `to` **apply the canonical Software Design authority,
  preserve established decisions, and route implementation-specific design to
  the code-local architecture that governs it**.
---

# Software Design

Software Design exists to guide the writing and maintenance of **Software
Architecture Specifications** for live software implementations.

A document in this section may also be useful by itself. A reader may consult
one concern to understand a design problem, resolve a local decision, or inspect
an established reusable design. Collectively, however, these documents have one
job: preserve reusable design knowledge so an architecture author can specify a
live implementation without reconstructing established reasoning from code,
conversation history, or first principles.

> [!IMPORTANT]
> **Software Design informs the specification; the Software Architecture
> Specification governs the implementation.**
>
> Reusable guidance and blueprints do not become the architecture of a codebase
> merely because they apply or because the code resembles them. The live
> Software Architecture Specification records what that implementation has
> actually selected, specialized, and committed to.

The section is normative rather than encyclopedic. Its purpose is not to survey
all defensible software-design approaches. It preserves the decisions, concepts,
defaults, reusable arrangements, and completeness lenses that should remain
available when future architecture work begins.

## Terms
<!--
element:
  path:
    uid: BJS5BZ
    filepath: 2 Technical Writing/3 Document/2 Document Elements/1 📖 Glossary.md
  version: '2.0'
-->

| Term | Meaning |
|---|---|
| **Software Specification Guidance** | Canonical reusable guidance that defines how a recurring class of software decisions should be understood and resolved. |
| **Software Specification Blueprint** | Canonical reusable specification that fixes a durable design for a recurring selecting condition. |
| **Software Architecture Specification** | Current codebase-specific specification of the architecture governing a live software implementation. |

## Design stance

> [!IMPORTANT]
> **Write for the amnesia agent.**
>
> Assume the next agent has the repository but none of the conversation that
> produced its design. If a consequential decision can only be recovered by
> interpreting implementation shape, reading commit archaeology, inferring from
> tests, or remembering prior discussion, the repository has lost design
> information.

This stance changes what counts as sufficient design documentation. Code can
demonstrate that an architecture is realized, but code should not be forced to
explain why its boundaries exist, which alternatives were intentionally
excluded, or which obligations future changes must preserve. Those decisions
belong in controlled specification.

The same standard applies to reusable guidance. A future architecture author
should be able to enter Software Design with the problem they are trying to
solve and recover the established decision model without reconstructing the
repository's intellectual history.

> [!IMPORTANT]
> **Organize around recurring independent decisions.**
>
> Software Design is organized primarily around recurring design concerns whose
> decisions can arise independently across different systems and architectures.
> A maintainer should be able to enter through the problem they know they have,
> rather than first translating that problem into an architecture framework,
> viewpoint, or named school of design.

The recognized recurring decision domains are established as first-class routing
locations even when their canonical guidance is not yet mature. An otherwise
empty domain README deliberately terminates routing while naming the class of
decisions that belongs there.

~~~text
Software Design
├── Principles
├── Comments
├── Concurrency
├── Configuration
├── Data Flow
├── Decomposition
├── Error Management
├── Extension
├── Interfaces
├── Naming
├── Performance
└── Testing
~~~

Architecting is cross-domain work rather than another decision domain. Guidance
for composing resolved domain decisions into a Software Architecture
Specification belongs at this root alongside Principles instead of behind a
collector folder.

Architecture viewpoints and perspectives serve a different purpose. Use them as
completeness lenses that expose omissions in an architecture; do not turn them
into the default navigation hierarchy merely because they describe architecture
comprehensively.

Named traditions such as Domain-Driven Design, information hiding, GRASP, Ports
and Adapters, or Viewpoints and Perspectives are sources of tested concepts and
reasoning. They can inform several Software Design concerns without becoming
the repository's taxonomy.

## Preserve resolved judgment

Software Design should reduce repeated reasoning, not multiply choices.

When several established approaches are equivalent for the repository's needs,
preserve a canonical default instead of presenting each future author with the
same menu. When a different arrangement is valid only under particular
conditions, state those selecting conditions so the exception can be recognized
without reopening the entire design problem.

This is not an argument against engineering judgment. It is an argument for
spending judgment where the implementation actually differs instead of spending
it again on choices the repository has already resolved.

Historical rationale and current authority have different jobs. Keep the
current decision in the guidance or specification that owns it. Preserve the
reasoning behind a consequential historical choice separately when that
reasoning still has value. Do not make a future maintainer replay decision
history to discover what governs now.

## Specify meaning before representation

Start with the design facts that must remain true: meaning, identity, ownership,
invariants, relationships, canonical state, required behavior, and consumer
obligations.

Choose classes, modules, schemas, transports, frameworks, serializers,
persistence mechanisms, and other implementation representations after those
facts are understood.

Representation is evidence of design. It is not a substitute for design.

This keeps Software Design from collapsing into pattern selection. A named
pattern can be useful when it accurately realizes an established decision, but
the pattern name does not explain the decision by itself.

## Reuse without confusing reuse with authority

Software Specification Guidance preserves reasoning that should apply across
many implementations. A Software Specification Blueprint goes further by
resolving several related decisions into one reusable durable arrangement.

Neither governs a live codebase merely by existing.

The Software Architecture Specification is where reusable authority becomes a
commitment for one implementation. It records which guidance has been resolved,
which blueprint has been selected when one applies, how reusable decisions were
specialized, and which implementation-specific architectural decisions remain.

Do not infer blueprint selection from implementation resemblance. Similarity
may be evidence worth investigating; it is not authority.

The relationship is:

~~~text
Software Specification Guidance
        ↓ informs

Software Specification Blueprint
        ↓ may be explicitly selected by

Software Architecture Specification
        ↓ governs

live implementation
~~~

The first two belong in reusable Software Design. The third belongs with the
codebase it governs.

## Check completeness without turning completeness into structure

Concern-oriented navigation and architecture completeness solve different
problems.

The section should help an author find a known design problem directly. During
architecture work, broader viewpoints, perspectives, quality concerns, and
other established lenses can then be used to ask what the author has missed.

Use those lenses aggressively for review. Do not assume every lens deserves a
folder, a mandatory document section, or a permanent place in the taxonomy.

The recognized domain surface is intentionally explicit rather than maximal.
It can still evolve when a genuinely new recurring independent decision domain
is established, but a recognized domain remains visible even before detailed
canonical guidance has been authored for it.

## Architectural commitment

A Software Architecture Specification is useful only when it remains connected
to the implementation it governs.

Treat durable architecture as a relationship among declared current
architecture, recognizable implementation evidence, and verification:

~~~text
declared current architecture
+ recognizable implementation evidence
+ verification
= architectural commitment
~~~

The specification should make consequential boundaries and obligations
recoverable without becoming a file inventory. Mechanical claims should prefer
mechanically recognizable evidence and verification. Claims that require human
or agent judgment should remain explicitly semantic rather than being forced
into brittle mechanical checks.

Software Design supplies the reusable knowledge used to reach that commitment.
The live Software Architecture Specification remains the authority for what one
implementation is required to satisfy.

## Index
<!--
element:
  path:
    uid: BZJASV
    filepath: 2 Technical Writing/3 Document/2 Document Elements/5 Index/README.md
  version: '2.0'
  renderer:
    uid: 45E225
    filepath: 4 Tooling/1 Navigation Crawler.py
-->

### 📖 Software Design Principles

`Consult when` *a software design decision admits several plausible implementations or an existing implementation boundary is being materially changed* `to` **apply the Documentation System's canonical defaults for concepts, ownership, classes, modules, validation, and projections without reopening equivalent alternatives**.

<a href="1%20%F0%9F%93%96%20Software%20Design%20Principles.md" uid="M8MDHY" data-ds-link="relative-path">../1 📖 Software Design Principles.md</a>

### Comments

`Consult when` *comments or docstrings must carry software-design information that code alone cannot reliably communicate* `to` **route recurring decisions about what explanatory context belongs with source and what should remain in clearer code or governing specification**.

<a href="2%20Comments/README.md" uid="206929" data-ds-link="relative-path">../2 Comments/README.md</a>

### Concurrency

`Consult when` *work may execute concurrently or asynchronously and independence, ordering, shared state, or coordination must be designed* `to` **route recurring concurrency decisions into canonical Software Design guidance**.

<a href="3%20Concurrency/README.md" uid="MPCB6Y" data-ds-link="relative-path">../3 Concurrency/README.md</a>

### Configuration

`Consult when` *software behavior depends on selectable runtime or deployment values and their ownership, defaults, precedence, or validation must be designed* `to` **route recurring configuration decisions into canonical Software Design guidance**.

<a href="4%20Configuration/README.md" uid="NB7QP1" data-ds-link="relative-path">../4 Configuration/README.md</a>

### Data Flow

`Consult when` *software must move, transform, retain, or mutate data across responsibilities and the authoritative flow must be designed* `to` **route recurring data-flow decisions about state ownership, transformation, and movement into canonical Software Design guidance**.

<a href="5%20Data%20Flow/README.md" uid="Y8VWBX" data-ds-link="relative-path">../5 Data Flow/README.md</a>

### Decomposition

`Consult when` *software responsibilities must be divided among components, modules, classes, functions, or other implementation boundaries* `to` **route recurring decomposition decisions about responsibility, cohesion, and reusable boundaries into canonical Software Design guidance**.

<a href="6%20Decomposition/README.md" uid="NGMGK7" data-ds-link="relative-path">../6 Decomposition/README.md</a>

### Error Management

`Consult when` *software failure behavior must be designed or an established error architecture must be selected* `to` **route between general error management concepts and formal architectures that apply those concepts under recurring consumer constraints**.

<a href="7%20Error%20Management/README.md" uid="TJBYJ1" data-ds-link="relative-path">../7 Error Management/README.md</a>

- `1 📖 Error Management.md`
- `2 Architectures/README.md`

### Extension

`Consult when` *software must admit future variants or capabilities without destabilizing established responsibilities and contracts* `to` **route recurring extension decisions about variation points, compatibility, and change boundaries into canonical Software Design guidance**.

<a href="8%20Extension/README.md" uid="YDA5G5" data-ds-link="relative-path">../8 Extension/README.md</a>

### Interfaces

`Consult when` *software responsibilities communicate across a boundary and the contract between them must be designed* `to` **route recurring interface decisions about exchanged meaning, compatibility, ownership, and boundary behavior into canonical Software Design guidance**.

<a href="9%20Interfaces/README.md" uid="XF3XK9" data-ds-link="relative-path">../9 Interfaces/README.md</a>

### Naming

`Consult when` *software concepts require stable identifiers whose names must communicate role and meaning across implementation surfaces* `to` **route recurring naming decisions into canonical Software Design guidance**.

<a href="10%20Naming/README.md" uid="MK3ZHA" data-ds-link="relative-path">../10 Naming/README.md</a>

### Performance

`Consult when` *latency, throughput, resource use, scale, or optimization materially constrains software design* `to` **route recurring performance decisions and their evidence requirements into canonical Software Design guidance**.

<a href="11%20Performance/README.md" uid="91PTM0" data-ds-link="relative-path">../11 Performance/README.md</a>

### Testing

`Consult when` *software behavior or architecture requires executable verification, or an established verification architecture must be selected* `to` **route between general testing principles and formal architectures that implement those principles for recurring verification surfaces**.

<a href="12%20Testing/README.md" uid="R0J5KF" data-ds-link="relative-path">../12 Testing/README.md</a>

- `1 📖 Testing.md`
- `2 Architectures/README.md`

### 📖 Implemented Architecture

`Consult when` *a project, package, service, subsystem, or other implemented scope has architectural decisions that future maintainers must recover without reverse engineering the code* `to` **establish current architecture authority, code-local discovery, scope inheritance, reusable-architecture selection, realization evidence, verification obligations, and maintenance rules**.

<a href="13%20%F0%9F%93%96%20Implemented%20Architecture.md" uid="6Q70VZ" data-ds-link="relative-path">../13 📖 Implemented Architecture.md</a>

### 🛠️ Design And Record An Implemented Architecture

`Read in full and follow when` *an implemented scope warrants durable architecture authority or its existing architecture is being materially changed* `to` **derive the architecture from relevant design concerns, place its Architecture Document beside the governed code, connect it to reusable guidance and implementation evidence, and keep the document synchronized with the design it governs**.

<a href="14%20%F0%9F%9B%A0%EF%B8%8F%20Design%20And%20Record%20An%20Implemented%20Architecture.md" uid="0F8SKM" data-ds-link="relative-path">../14 🛠️ Design And Record An Implemented Architecture.md</a>
