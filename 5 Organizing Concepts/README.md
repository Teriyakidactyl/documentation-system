---
uid: A7K3QF
description: >-
  `Consult when` *a structural decision is shared across documents, code,
  schemas, or other repository artifacts* `to` **enter the earliest unresolved
  organizing question and resolve conceptual structure before domain-specific
  representation rules are applied**.
---

# Organizing Concepts

This location is a repository-agnostic structural resolution system. It decides
what the conceptual units are, how they relate, who owns their meaning, where a
known unit fits, and whether a consequential structure withstands formal
validation. Domain-specific control, writing, or implementation rules represent
the result afterward.

The index owns the resolution order and handoffs. Each child document owns one
structural question and should not silently absorb an earlier or later stage.

## Resolution flow

Enter at the earliest unresolved question. Do not rerun an upstream decision
that is already established merely because a later stage is selected. If later
evidence contradicts an earlier decision, return to the earliest contradicted
stage instead of patching the downstream representation.

| Stage | Question | Result |
|---|---|---|
| 1. Structural units (<a href="1%20%F0%9F%9B%A0%EF%B8%8F%20Determine%20Structural%20Units.md" uid="YF43JX">documentation-system:§5.1</a>) | Is the candidate one cohesive unit or several? | Stable units and explicit unresolved boundaries. |
| 2. Relationships and topology (<a href="2%20%F0%9F%93%96%20Relationships%20and%20Structural%20Topologies.md" uid="P6V2HN">documentation-system:§5.2</a>) | What relation connects the units, and what topology preserves it? | Named relationship, axis where applicable, and topology. |
| 3. Ownership and convergence (<a href="3%20%F0%9F%92%A1%20Ownership%2C%20Containment%2C%20and%20Convergence.md" uid="W9D5TG">documentation-system:§5.3</a>) | Who owns the meaning or invariant, where is it contained, and where do independent concerns merely meet? | Owner, container, and convergence distinctions. |
| 4. Placement (<a href="4%20%F0%9F%9B%A0%EF%B8%8F%20Test%20A%20Placement.md" uid="M4R8XC">documentation-system:§5.4</a>) | Where does a known unit fit in an existing structure? | Confirmed placement or the earliest contradicted structural decision. |
| 5. Structural validation (<a href="5%20%F0%9F%9B%A0%EF%B8%8F%20Decompose%20And%20Validate%20A%20Structure.md" uid="K8T4ZM">documentation-system:§5.5</a>) | Does a consequential decomposition remain coherent and complete? | PASS, FAIL, or AMBIGUOUS with evidence. |

A caller may stop as soon as its structural question is resolved. The stages are
a dependency order, not a requirement to execute every document for every task.

## Index
<!--
element:
  path:
    uid: BZJASV
    filepath: 2 Technical Writing/3 Document/2 Document Elements/5 Index/README.md
  version: '2.0'
  renderer:
    uid: 45E225
    filepath: 4 Tooling/Navigation Crawler.py
-->

### 🛠️ Determine Structural Units

`Read in full and follow when` *a candidate subject, responsibility, document unit, module, or other structural item may combine concerns that do not need to remain one unit* `to` **establish cohesive structural units at genuine semantic or reasoning boundaries before later relationship, ownership, placement, and validation decisions treat them as given**.

<a href="1%20%F0%9F%9B%A0%EF%B8%8F%20Determine%20Structural%20Units.md" uid="YF43JX" data-ds-link="relative-path">../1 🛠️ Determine Structural Units.md</a>

### 📖 Relationships and Structural Topologies

`Consult when` *structural units are known but the relationship, axis, or topology that organizes them is unclear* `to` **name the governing relation and axis first, then select tree, list, matrix, or graph without letting a representation invent the structure**.

<a href="2%20%F0%9F%93%96%20Relationships%20and%20Structural%20Topologies.md" uid="P6V2HN" data-ds-link="relative-path">../2 📖 Relationships and Structural Topologies.md</a>

### 💡 Ownership, Containment, and Convergence

`Read in full when` *semantic responsibility, physical containment, or a location where independently owned concerns meet are being treated as the same thing* `to` **separate ownership from containment and convergence before domain-specific placement chooses a representation**.

<a href="3%20%F0%9F%92%A1%20Ownership%2C%20Containment%2C%20and%20Convergence.md" uid="W9D5TG" data-ds-link="relative-path">../3 💡 Ownership, Containment, and Convergence.md</a>

### 🛠️ Test A Placement

`Read in full and follow when` *a known structural unit with an established relationship and owner must be placed into an existing structure or more than one container plausibly fits* `to` **test candidate containers against the established structure and either confirm one placement or surface the structural contradiction without redefining the unit to make it fit**.

<a href="4%20%F0%9F%9B%A0%EF%B8%8F%20Test%20A%20Placement.md" uid="M4R8XC" data-ds-link="relative-path">../4 🛠️ Test A Placement.md</a>

### 🛠️ Decompose And Validate A Structure

`Read in full and follow when` *established structural units must be organized into a consequential reusable structure, an existing structure requires formal validation, or placement exposes a contradiction that would become structural precedent* `to` **construct or test the structure under one relation and axis at a time, returning PASS, FAIL, or AMBIGUOUS without changing unit boundaries merely to force a fit**.

<a href="5%20%F0%9F%9B%A0%EF%B8%8F%20Decompose%20And%20Validate%20A%20Structure.md" uid="K8T4ZM" data-ds-link="relative-path">../5 🛠️ Decompose And Validate A Structure.md</a>
