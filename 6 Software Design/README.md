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

Software Design exists to guide the authoring and maintenance of **Software
Architecture Specifications** for live software implementations.

Its documents may also be consulted independently for explanation, design
reasoning, or a local implementation decision. That local usefulness is
secondary to their collective purpose: supplying the canonical vocabulary,
decision models, defaults, selecting conditions, reusable designs, completeness
lenses, and verification expectations needed to specify a durable software
architecture without reconstructing those decisions from scratch.

The documents in this section are normative working authority, not a survey of
software-engineering possibilities. They constrain how a Software Architecture
Specification is developed while leaving implementation-specific decisions in
the specification owned by the live codebase.

The purpose is not to eliminate engineering judgment. It is to preserve resolved
design knowledge so the author of a Software Architecture Specification spends
judgment on the decisions that are actually specific to the implementation.

## Working doctrine

### Specify before representing

Resolve the design problem before choosing its implementation representation.

Start with meaning, identity, ownership, invariants, relationships, canonical
state, and required behavior. Choose classes, modules, schemas, serializers,
frameworks, transports, and other representations only after the decisions they
must realize are understood.

Implementation shape is evidence of a design. It is not a reliable substitute
for an explicit design decision.

### Prefer canonical decisions over menus

When several established approaches satisfy the same constraints, Software
Design should state one canonical default rather than present equivalent options
for every implementation to rank again.

A supported alternative needs a concrete selecting condition. The reader should
be able to determine why the default applies or why a different specified
arrangement is required.

Named methodologies, patterns, and schools of design are sources of useful
reasoning. They do not become repository authority merely because they are
recognized in the literature.

### Guide the specification; do not replace it

Software Design supplies reusable specification authority used to write a
Software Architecture Specification.

General specification guidance defines how a recurring design problem is
reasoned about and resolved. A reusable blueprint may go further and fix a
durable arrangement for a recurring selecting condition. Neither artifact is the
architecture specification of a live implementation.

The Software Architecture Specification records the design actually governing
that implementation. It resolves the applicable Software Design concerns,
selects reusable blueprints where their conditions apply, adds
implementation-specific decisions, identifies realization evidence, and states
how the resulting architectural obligations are verified.

A reusable design is not selected merely because code resembles it. The Software
Architecture Specification must explicitly accept the relevant obligations and
state how the implementation realizes and verifies them.

Keep the Software Architecture Specification with the implementation it governs
in the code-local `📐 Architecture` store. Do not use reusable Software Design
documents as substitutes for that live authority.

### Organize around recurring independent decisions

Software Design is organized primarily around recurring design concerns whose
decisions can arise independently across different systems and architectures.

A concern deserves an independently routable location when it:

- recurs across implementations;
- has a stable vocabulary, decision sequence, or set of design choices;
- is consequential enough that getting it wrong changes system behavior or
  maintainability; and
- is non-obvious enough that an unfamiliar maintainer should not be expected to
  reconstruct it from first principles or existing code.

This is why Error Management and Testing are first-class concerns. A maintainer
can encounter either problem without first deciding the rest of a system's
architecture.

### Let the taxonomy grow from demonstrated need

Do not pre-create a complete Software Design hierarchy from a book, framework,
or imagined future architecture.

A topic earns a location when recurring work establishes that it is an
independent decision domain with useful canonical specification. Until then,
leave the taxonomy incomplete rather than create empty categories.

The final shape of Software Design is intentionally not fixed in advance.

### Use architecture lenses for completeness, not navigation

Architecture viewpoints, perspectives, and established design traditions are
tools for finding omissions and testing reasoning.

Use them to ask whether a design has overlooked relevant information, runtime,
development, operational, security, resilience, performance, evolution, or
other concerns. Do not make those lenses the default folder taxonomy unless a
concrete recurring work encounter independently justifies that structure.

Navigation should begin from the problem the maintainer knows they have, not
from prior knowledge of which architectural framework classifies it.

### Design for an amnesiac maintainer

Assume the next agent or maintainer has the repository but none of the
conversation that produced its design.

Consequential decisions must therefore be recoverable from controlled
specification and code-local authority rather than from remembered discussion,
implementation resemblance, commit archaeology, or inference from tests.

The repository should answer two different questions directly:

~~~text
What specification guidance and reusable designs should I use
to resolve this architectural decision?
    → Software Design

What architecture is this implementation actually required to satisfy?
    → its Software Architecture Specification
~~~

Software Design exists to make the second answer possible without forcing its
author to reinvent the first. When either answer requires reverse engineering,
the documentation system has lost design information.

### Keep current authority separate from decision history

Current specification states what is expected now. Decision records preserve why
a consequential choice was made at a particular point in repository history.

Do not force a maintainer to replay ADRs to discover the current design, and do
not turn current specification into a chronology of rejected alternatives.

Historical reasoning belongs in `.decisions` when retaining that reasoning has
a continuing job. The accepted consequence of a decision belongs in current
authority.

### Require architecture to meet implementation evidence

A declared architecture is not established by prose alone, and code resemblance
does not create architecture authority by itself.

Treat durable architecture as a commitment among three things:

~~~text
declared current architecture
+ recognizable implementation evidence
+ verification
= architectural commitment
~~~

Prefer mechanically recognizable evidence for mechanically decidable claims.
Keep semantic judgment explicit where faithful automation is not possible.

## Working method

Use Software Design to build or revise a Software Architecture Specification:

1. establish the live implementation scope that the specification will govern;
2. identify the recurring design concerns that materially affect that scope;
3. consult the canonical specification for each concern before inventing a local
   convention;
4. apply documented defaults and decision sequences, recording only the resolved
   result that matters to this implementation;
5. select a reusable blueprint only when its selecting conditions and obligations
   actually apply;
6. use architecture viewpoints, perspectives, and other completeness lenses to
   search for consequential concerns that have not yet been resolved;
7. state the implementation-specific responsibilities, boundaries, invariants,
   interactions, and allowed variation that remain after reusable decisions are
   applied;
8. map those architectural claims to recognizable implementation evidence;
9. state how mechanically decidable and semantic obligations will be verified;
   and
10. preserve historical rationale separately when the reason for a consequential
    choice must survive.

A Software Architecture Specification is therefore not a copy of Software Design.
It is the implementation-specific resolution produced by applying Software Design
to one live scope.

## Index
<!--
element:
  path:
    uid: BZJASV
    filepath: 2 Technical Writing/3 Document/2 Document Elements/5 Index/README.md
  version: '2.0'
  renderer:
    uid: 45E225
    filepath: 4 Tooling/1 🛠️ Navigation Crawler.py
-->

### 📖 Software Design Principles

`Consult when` *a software design decision admits several plausible implementations or an existing implementation boundary is being materially changed* `to` **apply the Documentation System's canonical defaults for concepts, ownership, classes, modules, validation, and projections without reopening equivalent alternatives**.

<a href="1%20%F0%9F%93%96%20Software%20Design%20Principles.md" uid="M8MDHY" data-ds-link="relative-path">../1 📖 Software Design Principles.md</a>

### Architecture

`Consult when` *implemented code needs durable architecture authority or an existing architecture must be located, reviewed, or changed* `to` **route between the Implemented Architecture reference and the procedure for designing, recording, colocating, and maintaining that authority**.

<a href="2%20Architecture/README.md" uid="20KRDM" data-ds-link="relative-path">../2 Architecture/README.md</a>

- `1 📖 Implemented Architecture.md`
- `2 🛠️ Design And Record An Implemented Architecture.md`

### Error Management

`Consult when` *software failure behavior must be designed or an established error architecture must be selected* `to` **route between general error management concepts and formal architectures that apply those concepts under recurring consumer constraints**.

<a href="3%20Error%20Management/README.md" uid="TJBYJ1" data-ds-link="relative-path">../3 Error Management/README.md</a>

- `1 📖 Error Management.md`
- `2 Architectures/README.md`

### Testing

`Consult when` *software behavior or architecture requires executable verification, or an established verification architecture must be selected* `to` **route between general testing principles and formal architectures that implement those principles for recurring verification surfaces**.

<a href="4%20Testing/README.md" uid="R0J5KF" data-ds-link="relative-path">../4 Testing/README.md</a>

- `1 📖 Testing.md`
- `2 Architectures/README.md`
