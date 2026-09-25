---
uid: D6NE0B
description: >-
  `Read in full and follow when` *an implemented architecture has been
  resolved and must be expressed as durable current authority* `to` **assemble
  a concise Architecture Document from the resolved scope, drivers, design,
  realization, verification, and evolution contract and bind it to the code it
  governs**.
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

# 🛠️ Author An Architecture Document

## 1. Resolve the architecture before templating it

Use the Software Design Architecture guidance to establish that durable
implemented architecture is warranted and to resolve the architectural
decisions.

Do not use the Form headings as a brainstorming substitute. The document records
a design; it does not create architectural completeness merely by containing six
sections.

## 2. Place the document with governed code

Create or use the `📐 Architecture/` store at the nearest stable root of the
governed implementation.

Apply the host repository's organization scheme to the store and filename. Do
not hide current architecture in a dot-prefixed sideband or historical
directory.

## 3. Bind Form provenance

Add the Architecture Document Form package to `form.path` and record the Form
version used.

Let Organizing mint the document UID when the host corpus owns UID control, or
retain the existing UID when moving an already controlled Architecture
Document.

## 4. Write Scope and Drivers

In **Scope**, identify the governed implementation and any relationship to
enclosing or narrower architectures.

In **Drivers**, retain only forces that materially shape architecture. Link to
the authority for requirements or policies that change independently.

Name reusable Software Design architectures only when the implementation
actually accepts their obligations.

## 5. Write the Architecture

Describe the fixed design using the structure natural to the system.

State ownership, boundaries, canonical state, interactions, invariants, and
other load-bearing relationships before implementation detail. Use diagrams or
tables when relationships would otherwise be harder to recover, not because the
Form requires a particular representation.

Avoid historical narrative and rejected alternatives in this section.

## 6. Map Realization

For each load-bearing concept, identify the stable implementation boundary that
realizes it.

Prefer source-addressable entry points, modules, packages, schemas, registries,
interfaces, processes, or stores over moving line numbers and incidental helper
functions.

Remove mappings that do not help a future maintainer locate architectural
evidence.

## 7. State Verification

Identify executable or inspectable evidence for architecture claims.

Where a claim is not yet mechanically verified, state that gap explicitly.
Do not make a test prove its own expected behavior from the same implementation
facts it is meant to validate.

## 8. Bound Evolution

State what may vary without changing the architecture and what selecting
conditions justify known alternatives.

Call out stable extension points, replaceable adapters, independent modules, or
other intentional variation. Do not promise hypothetical extensibility that the
current architecture does not support.

## 9. Connect implementation discovery

Ensure the Architecture store README routes to the document.

Where the repository supports controlled architecture metadata, update the
governed public or indexed entry point to link directly to the Architecture
Document. Preserve that link across moves through stable identity when
available.

## 10. Retain rationale separately

When a consequential choice needs historical explanation, create or link an ADR.
Do not copy the ADR's alternatives and chronology into the Architecture Document
unless part of that information remains a current design constraint.

## 11. Validate and maintain

Run the host repository's organization and verification tooling.

Review the document whenever a change alters architectural scope, selected
reusable architectures, fixed commitments, realization mappings, verification
obligations, or supported evolution.

Leave the document unchanged when an internal refactor preserves all of those
contracts.
