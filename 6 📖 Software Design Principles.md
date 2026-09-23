---
description: >-
  `Consult when` *a software design decision admits several plausible
  implementations or an existing implementation boundary is being materially
  changed* `to` **apply the Documentation System's canonical defaults for
  concepts, ownership, classes, modules, validation, and projections without
  reopening equivalent alternatives**.
quadrant: Reference
outline:
  topology: list
  axis: design principle
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

# 📖 Software Design Principles

Use these principles as defaults for software design in this repository. They
are optimized for agent consistency rather than for surveying every defensible
architecture.

Prefer one good canonical default over a menu of competing excellent
alternatives. When several established designs satisfy the same constraints,
use the default stated here. Depart from it only when a concrete constraint
makes it materially incorrect, and state that constraint where the exception
is introduced.

Named traditions below are retrieval cues for their established bodies of
knowledge. The local rule is the interpretation this repository adopts when
those traditions permit several reasonable implementations.

## Default decision order

Resolve meaning before representation:

```text
concept
-> identity and lifecycle
-> authority and ownership
-> relationships and invariants
-> canonical state
-> projections
-> implementation representation
```

Do not begin from a Python class, module tree, serializer, provider object, or
consumer view when any earlier decision remains unsettled.

## DDD: Bounded Context

Keep one coherent meaning and rule set for a term inside one model boundary.

**Default.** Reuse a term inside the same bounded context only when it denotes
the same concept. Model distinct meanings separately even when their names
match.

## DDD: Ubiquitous Language

Use one canonical term for one concept inside its bounded context.

**Default.** Code, tests, metadata, and documentation use the same domain term.
Translate vocabulary only at an explicit external boundary.

## DDD: Entity and Value Object

Distinguish persistent identity from value equality.

**Default.** Model an entity only when identity must survive changes to
attributes, placement, representation, or display name. Otherwise prefer a
value representation.

Do not create a class merely because a noun can be named. A class must preserve
identity, value semantics, an invariant, validation, serialization behavior,
substitutable behavior, or useful typed dispatch.

## DDD: Aggregate and Design by Contract

Place each invariant at the narrowest boundary that legitimately owns every fact
required to enforce it.

**Default.** Keep object-local rules with the object, aggregate rules with the
aggregate boundary, cross-object corpus or graph rules in compilation
validation, and external-system rules at the integration boundary.

Do not move a cross-object validation rule onto a model object merely to make
that object richer.

## Parnas: Information Hiding

Hide decisions that can vary independently behind separate boundaries.

**Default.** Separate implementation modules when they have independent reasons
to change. Sharing the same input model is not, by itself, a reason to combine
their behavior.

## GRASP: Information Expert

Place responsibility with the legitimate owner of the information needed to
perform it.

**Default.** Domain objects own domain facts and local invariants. Compiler,
assembler, validation, and projection behavior remain in their corresponding
processing stages unless the domain model itself demonstrates a stronger owner.

## GRASP: High Cohesion and Low Coupling

Keep one reason to change together and minimize knowledge across boundaries.

**Default.** Prefer a small number of cohesive modules over both a monolith and
a proliferation of one-function modules. Split when an independently changing
policy, representation, or compiler pass has become identifiable.

## Behavioral Subtyping

Use inheritance only when substitution preserves the parent's meaning and
contract.

**Default.** Do not use inheritance to share fields or implementation. Use
composition, ownership, containment, or references unless the child is
semantically a kind of the parent and is substitutable everywhere the parent
is accepted.

## Ports and Adapters

Keep provider, protocol, and transport vocabulary at the boundary.

**Default.** Translate external representations into canonical domain terms at
the adapter. Do not let a provider's taxonomy become the domain taxonomy unless
the domain independently adopts the same distinction.

## Common Closure Principle

Treat repeated co-change as evidence for cohesion, subordinate to semantic
ownership.

**Default.** Keep concepts together when they share an invariant, domain
meaning, or durable reason to change. Do not group them merely because one
operation happens to process them in sequence.

## Canonical state and projections

Give each mutable fact one canonical authority.

**Default.** Consumer-specific forms are projections derived from canonical
state:

```text
canonical source -> projection
```

A projection may rearrange, filter, join, or format canonical information, but
does not become independently editable authority. Do not create parallel
canonical models for different consumers.

A deterministic projection may be compiled automatically when its result is a
mechanical function of canonical inputs. If producing the result requires
interpretation, choosing among plausible meanings, reconciling conflicting
authority, or adapting semantics to context, it is authoring rather than
compilation and requires an agent or human decision.

## Modules and lightweight model objects

Use modules to expose independently changing implementation responsibilities.
Use lightweight typed objects to make stable domain facts explicit.

**Default.** Data objects model facts. Compiler passes perform transformations.
Validators evaluate invariants and return diagnostics. The command-line entry
point orchestrates those passes and presents their results.

Prefer immutable dataclasses or similarly lightweight values where identity and
mutation are not part of the modeled concept. Do not create a class hierarchy
to mirror the module layout.

## Diagnostics

Represent validation findings as structured diagnostics rather than immediate
printing or exceptions when compilation can continue deterministically.

**Default.**

- an **error** means a valid deterministic result cannot be established and
  compilation fails;
- a **warning** means compilation is valid but a condition requires attention;
- diagnostics carry stable codes, severity, location, and a concrete message;
- presentation layers may render the same diagnostic to console output, GitHub
  annotations, or machine-readable artifacts.

Use exceptions for failures that prevent the compiler from constructing or
evaluating the model at all, not as the ordinary representation of every
validation finding.

## Exceptions

An exception must name the concrete constraint that defeats the default and
must remain narrower than the rule it overrides.

Do not document several equivalent alternatives as peer recommendations. When
the repository needs a second supported pattern, state the condition that
selects it so an agent can choose deterministically rather than rank competing
preferences.
