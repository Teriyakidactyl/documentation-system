---
uid: A7K3QF
form: '<a href="../2%20Technical%20Writing/3%20Document/1%20Document%20Forms/11%20%F0%9F%93%96%20Index.md" uid="BZJASV">documentation-system:§2.3.1.11</a>'
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

## Resolution flow

Enter at the earliest unresolved question. Do not rerun an upstream decision
that is already established merely because a later stage is selected. If later
evidence contradicts an earlier decision, return to the earliest contradicted
stage instead of patching the downstream representation.

| Stage | Question | Result |
|---|---|---|
| 1. Structural units | Is the candidate one cohesive unit or several? | Stable units and explicit unresolved boundaries. |
| 2. Relationships and topology | What relation connects the units, and what topology preserves it? | Named relationship, axis where applicable, and topology. |
| 3. Ownership and convergence | Who owns the meaning or invariant, where is it contained, and where do independent concerns merely meet? | Owner, container, and convergence distinctions. |
| 4. Placement | Where does a known unit fit in an existing structure? | Confirmed placement or the earliest contradicted structural decision. |
| 5. Structural validation | Does a consequential decomposition remain coherent and complete? | PASS, FAIL, or AMBIGUOUS with evidence. |

A caller may stop as soon as its structural question is resolved. The stages are
a dependency order, not a requirement to execute every document for every task.

<!-- BEGIN index -->
<!-- This block is owned by the Documentation Compiler; run the compiler whenever indexed information or classification may have changed. -->

- <a href="1%20%F0%9F%9B%A0%EF%B8%8F%20Test%20A%20Placement.md" uid="M4R8XC">documentation-system:§5.1</a> — 🛠️ Test A Placement
  - `Read in full and follow when` *a non-trivial item must be placed into an existing structure or more than one placement plausibly fits* `to` **test the candidate against topology, relation, axis, granularity, ownership, and coverage, then confirm it or surface the unresolved ambiguity instead of guessing**.
- <a href="2%20%F0%9F%93%96%20Structural%20Topologies.md" uid="P6V2HN">documentation-system:§5.2</a> — 📖 Structural Topologies
  - `Consult when` *the relation governing a structural layer is unclear* `to` **distinguish tree, list, matrix, and graph topology by the relation each preserves and the failure signal each exposes**.
- <a href="3%20%F0%9F%92%A1%20Ownership%20and%20Containment.md" uid="W9D5TG">documentation-system:§5.3</a> — 💡 Ownership and Containment
  - `Read in full when` *the place holding an item and the concept responsible for it are being treated as the same thing* `to` **separate containment from ownership and choose the owner before domain-specific placement rules determine the container**.
- <a href="4%20%F0%9F%9B%A0%EF%B8%8F%20Decompose%20A%20Subject%20Into%20MECE.md" uid="K8T4ZM">documentation-system:§5.4</a> — 🛠️ Decompose A Subject Into MECE
  - `Read in full and follow when` *a consequential structure must be authored from scratch, an existing structure requires formal MECE validation, or Test A Placement leaves an ambiguity whose resolution will become structural precedent* `to` **derive and validate the structure explicitly, returning PASS, FAIL, or AMBIGUOUS without guessing**.
<!-- END index -->
