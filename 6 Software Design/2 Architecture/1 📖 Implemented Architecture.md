---
uid: 6Q70VZ
description: >-
  `Consult when` *a project, package, service, subsystem, or other implemented
  scope has architectural decisions that future maintainers must recover
  without reverse engineering the code* `to` **establish current architecture
  authority, code-local discovery, scope inheritance, reusable-architecture
  selection, realization evidence, verification obligations, and maintenance
  rules**.
quadrant: Reference
outline:
  topology: tree
  axis: implemented architecture facet
  numbering: hierarchical-decimal
writing-style:
  formality: professional
  tone: clinical/detached
  mode: declarative
  density: compressed/dense
  abstraction: mixed
  redundancy: zero
  signposting: entry-headers only
  register: technical
---

# 📖 Implemented Architecture

An **implemented architecture** is the current durable design authority for an
implemented software scope. It fixes architectural decisions that future
maintainers must preserve or deliberately change without requiring them to
reconstruct those decisions from code shape, tests, conversation history, or
historical ADRs.

An **Architecture Document** is the controlled document that expresses that
architecture. The distinction follows the useful separation made by
[ISO/IEC/IEEE 42010:2022](https://www.iso.org/standard/74393.html) between an
architecture and an architecture description. This repository uses
**Architecture Document** for its concrete document role and does not claim
conformance to ISO/IEC/IEEE 42010 unless separately established.

## 1. Selecting condition

Create durable implemented architecture when several interacting design
decisions constrain future implementation work beyond one local contract.

Strong selecting conditions include:

- responsibilities or invariants span several modules, components, processes, or
  representations;
- future changes must preserve a non-obvious boundary, ownership rule, state
  authority, interaction pattern, or quality property;
- more than one plausible implementation could satisfy the visible behavior but
  only some preserve the intended design;
- reusable Software Design architectures are selected together and their local
  realization must be made explicit;
- agents or maintainers would otherwise need to infer architectural intent from
  implementation clues.

Do not create an Architecture Document merely because a package exists, several
files share a directory, or a design could be described at architectural
abstraction. Local code contracts remain preferable when they completely
express the relevant rule.

## 2. Locality and discovery

### 2.1 Architecture store

Place Architecture Documents in a **`📐 Architecture/` store at the nearest
stable root of the implementation they govern**.

The host repository's organization scheme may add an ordinal, namespace, or
other locator representation to that directory. The semantic store name remains
`📐 Architecture`; its physical representation follows the host's normal
controlled-organization rules.

The store is current authority and participates in normal retrieval. Do not hide
it in a historical, research, or other explicit-retrieval sideband.

### 2.2 Discovery from code

An amnesiac maintainer starting from implementation must be able to locate its
architecture without semantic repository-wide search:

~~~text
start at governed implementation
→ inspect its stable owning root
→ enter that root's 📐 Architecture store
→ select the Architecture Document whose Scope includes the implementation
~~~

A deeper owning root may introduce its own Architecture store when a narrower
scope has independently meaningful architecture. The narrower architecture must
state whether it specializes, replaces, or remains independent of architecture
at an enclosing root.

Do not rely on filename resemblance, import structure, test names, commit
history, or remembered conventions as the only architecture-discovery
mechanism.

### 2.3 Direct provenance

Where the host repository supports controlled metadata, a public or indexed
implementation entry point should carry a direct `architecture` link to the
Architecture Document that governs it.

In the Documentation System, an indexed executable entry point governed by a
formal architecture carries that controlled link. Internal modules inherit the
governing architecture unless a narrower documented scope says otherwise.

The direct link accelerates discovery; the code-local Architecture store
establishes the durable locality convention.

## 3. Authority relationships

### 3.1 Current authority

An Architecture Document states the design that implemented code is expected to
satisfy now. Change it with the implementation when the architecture changes.

Do not use an Architecture Document as a roadmap whose claims are knowingly
unimplemented. Planned architecture belongs in planning material until the
implementation and current architecture authority can move together.

### 3.2 Software Design guidance

Implemented architectures inherit
<a href="../1%20%F0%9F%93%96%20Software%20Design%20Principles.md" uid="M8MDHY">documentation-system:§6.1</a>
and use concern References such as Error Management and Testing to resolve
recurring design problems.

A **reusable architecture** under Software Design fixes one recurring arrangement
for a selecting condition, such as Agent-Facing Errors or Self-Assembling
Verification. An implemented Architecture Document may select such architectures
and then records where and how their obligations are realized.

Do not claim a reusable architecture merely because the implementation
resembles it. Selection means the implementation accepts that architecture's
contract and verification obligations.

### 3.3 Decision provenance

An Architecture Decision Record preserves why an architectural choice was made
at a particular state. It is not current architecture authority.

Use the relationship:

~~~text
Software Design guidance
        ↓ informs
implemented Architecture Document
        ↓ governs
code + verification

ADR
        └── preserves why a consequential choice was made
~~~

A current Architecture Document may link to an ADR when historical rationale is
useful, but current work must not require reconstructing the architecture from a
sequence of ADRs.

## 4. Architecture content

An Architecture Document must establish enough information for a maintainer to
understand and verify the governing design without prescribing irrelevant
boilerplate.

The canonical Architecture Document Form requires six semantic surfaces:

~~~text
Scope
Drivers
Architecture
Realization
Verification
Evolution
~~~

**Scope** identifies the implementation governed and its boundary with
surrounding systems or narrower architectures.

**Drivers** identifies the requirements, constraints, consumers, quality goals,
and selected reusable guidance that materially shape the design.

**Architecture** fixes the responsibilities, ownership, canonical state,
relationships, interactions, invariants, and other structural decisions that
must remain true. Organize this section around the design itself rather than a
universal list of architecture headings.

**Realization** maps architectural concepts to recognizable implementation
boundaries. Name public entry points, modules, packages, schemas, protocols,
stores, processes, or other code structures when those facts let a maintainer
locate the realization directly.

**Verification** states how architectural obligations are proved. Prefer
mechanical checks for mechanically decidable claims and name the independent
contracts or tests that establish behavioral claims.

**Evolution** distinguishes fixed architectural commitments from allowed
variation and states selecting conditions for known extension points or
replacement boundaries.

The Architecture Document Form is:
<a href="../../../2%20Technical%20Writing/3%20Document/1%20Document%20Forms/13%20Architecture%20Document/README.md" uid="T6P28F">documentation-system:§2.3.1.13</a>.

## 5. Completeness without template worship

Architecture design must consider more than the headings that happen to appear
in the final document.

Use recurring Software Design concerns to ask which independent decision domains
matter. Use established architecture lenses, including viewpoints and
cross-cutting perspectives, to look for omitted context, information, runtime,
development, operational, security, performance, resilience, and evolution
concerns.

These are **consideration lenses, not mandatory document sections**.

An irrelevant concern does not need a decorative "not applicable" section.
A consequential omission must be distinguishable from an accidental omission
when a future maintainer could reasonably assume the missing concern changes the
design.

This approach is compatible with the intent of practical architecture methods
such as [arc42](https://arc42.org/documentation/), which emphasizes useful,
maintainable architecture information and docs-as-code while allowing detail to
be tailored to stakeholder need.

## 6. Realization evidence

Architectural authority must have recognizable evidence in the implementation.

Prefer explicit structures when an architecture requires explicit concepts:
typed values, schemas, interfaces, registries, public declarations, stable
module boundaries, dependency rules, or other mechanically recognizable forms.

Do not require arbitrary class names or framework shapes merely to make an
architecture visible. The evidence should arise naturally from the guarantees
the architecture makes.

The governing relationship is:

~~~text
declared architecture
    + recognizable implementation evidence
    + verification
= architectural commitment
~~~

Implementation resemblance without declared authority is not sufficient.

## 7. Maintenance

Change an Architecture Document whenever a code change alters one of its fixed
architectural claims, realization mappings, selected reusable architectures, or
verification obligations.

Preserve stable wording when the implementation changes beneath an unchanged
architectural boundary. Architecture documentation should describe durable
design rather than narrate every refactor.

Create or update an ADR separately when the reason for a consequential
architecture change has a continuing provenance value. Do not turn routine
Architecture Document maintenance into mandatory ADR production.
