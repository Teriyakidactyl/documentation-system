---
uid: K8T4ZM
description: >-
  `Read in full and follow when` *established structural units must be
  organized into a consequential reusable structure, an existing structure
  requires formal validation, or placement exposes a contradiction that would
  become structural precedent* `to` **construct or test the structure under
  one relation and axis at a time, returning PASS, FAIL, or AMBIGUOUS without
  changing unit boundaries merely to force a fit**.
quadrant: HowTo
outline:
  topology: linear
  numbering: hierarchical-decimal
writing-style:
  formality: professional
  tone: neutral/detached
  mode: imperative
  density: moderate
  abstraction: mixed
  redundancy: zero
  signposting: light
  register: technical
---

# 🛠️ Decompose And Validate A Structure

Use this procedure when the consequences justify formal structural construction
or assurance. Routine placement belongs in
<a href="4%20%F0%9F%9B%A0%EF%B8%8F%20Test%20A%20Placement.md" uid="M4R8XC">documentation-system:§5.4</a>.
This procedure takes over when a reusable taxonomy or other consequential
structure must be authored, when an important existing structure needs formal
validation, or when a placement contradiction would otherwise become
precedent.

The procedure assumes that the structural units have already been established
by
<a href="1%20%F0%9F%9B%A0%EF%B8%8F%20Determine%20Structural%20Units.md" uid="YF43JX">documentation-system:§5.1</a>
and that load-bearing relationships are explicit under
<a href="2%20%F0%9F%93%96%20Relationships%20and%20Structural%20Topologies.md" uid="P6V2HN">documentation-system:§5.2</a>.
If construction repeatedly requires splitting, merging, or redefining those
units, return upstream rather than treating the decomposition as authority over
their boundaries.

## 1. Apply the invariants

Keep these conditions true throughout the decomposition:

- **Stable units.** Do not silently split or merge an established unit to make a
  candidate structure work.
- **Explicit relationship.** Each layer preserves one named governing
  relationship.
- **MECE where exclusivity is claimed.** Exclusive siblings do not overlap and
  the declared domain has no confirmed gap.
- **Single-axis locking.** A classification or ordered layer answers one
  organizing question. Independent dimensions remain independent.
- **Superordinate validation.** A hierarchical parent remains more abstract
  than every child it contains.
- **Ownership before containment.** Representation does not redefine semantic
  ownership.
- **Deterministic ordering where order carries meaning.** Name the canonical
  ordering rule rather than accepting incidental sequence.

Do not force exclusivity onto a matrix or graph merely because MECE is the
validation frame. Exclusivity applies only where a layer claims exclusive
membership.

## 2. Choose an execution path

Choose one path from the condition of the problem, not by preference.

### 2.1 Top-down: constraint first

Use top-down decomposition when an external system or representation imposes a
non-negotiable shape.

1. State the imposed constraint.
2. Draft the smallest candidate structure compatible with it.
3. Run the established units against that structure.
4. Abandon or revise the hypothesis when collisions are frequent rather than
   stretching definitions to preserve it.

An imposed representation can constrain what is possible without proving that
the underlying conceptual relationship has the same shape.

### 2.2 Bottom-up: units first

Use bottom-up decomposition for unstructured material, overlapping legacy
categories, or structures whose current hierarchy is not trustworthy.

1. Start from the established unit set.
2. Record the relationships that distinguish or connect the units.
3. Group only where one governing relation and axis explain the grouping.
4. Surface uncovered units or combinations as possible gaps.
5. Let the relationship select the topology rather than choosing a convenient
   container first.

### 2.3 Synthesis: hypothesize then test

Use synthesis when a plausible structure already exists but still needs formal
confirmation.

1. Draft the likely structure.
2. Run every established unit against it.
3. Treat repeated collisions or forced exceptions as evidence against the
   hypothesis.
4. Continue only when the hypothesized structure and the unit analysis agree.

## 3. Build one layer at a time

At each layer:

1. name the governing relationship;
2. name the axis when the relation is classificatory or ordered;
3. select the topology that preserves that relationship;
4. place only units or groups already justified by an upstream relation;
5. confirm that every parent remains a legitimate superordinate where
   hierarchy is used.

A larger structure may change topology between layers. That is valid when the
new layer states a different governing relation explicitly.

If a node can validly be read in two incompatible ways, or if a child needs two
exclusive parents for independent reasons, return **AMBIGUOUS** or revisit the
earliest upstream decision that the evidence contradicts. Do not encode the
ambiguity as accidental nesting.

## 4. Run terminal structural validation

Validate only after the candidate structure has stabilized.

For every exclusive layer:

1. **Check overlap.** Attempt to place every unit. A unit that legitimately
   satisfies two exclusive siblings exposes a unit, axis, or relation problem.
2. **Check gaps.** Look for a real member of the declared domain that fits no
   sibling without stretching a definition.
3. **Check superordinates.** Confirm every parent remains more abstract than
   its children.
4. **Check the governing relation.** Confirm the representation still preserves
   the relation selected for that layer.
5. **Check parent-chain completeness.** Do not issue a nested verdict while an
   intermediate relationship remains unresolved.

Use two cheap probes when exhaustiveness is uncertain:

- invert a category's completeness claim by asking what would *not* belong and
  whether such a case exists;
- bring a concrete counter-example from the same kind of organizing problem and
  ask where it fits without changing a definition.

A counter-example confirms a gap. Failure to find one is evidence of
exhaustiveness, not proof.

## 5. Record the evidence

The validation record must let another reader audit the verdict without
reconstructing unstated reasoning.

Record:

- every established unit and its resulting location or relationship in the
  candidate structure;
- the governing relationship, axis where applicable, and topology for every
  load-bearing layer;
- each overlap or gap candidate that could affect the verdict and its
  disposition;
- every unresolved relationship or boundary that prevents a definitive result.

Confirm that every input unit is accounted for before issuing the verdict.

Declare exactly one outcome:

- **PASS:** no confirmed overlap or gap remains and every load-bearing
  relationship needed for the verdict is resolved.
- **FAIL:** a confirmed overlap, gap, false superordinate, mixed axis, or other
  structural contradiction remains.
- **AMBIGUOUS:** one or more load-bearing units, relationships, or axes admit
  competing valid readings, so PASS or FAIL cannot yet be justified.

Do not collapse **AMBIGUOUS** into either PASS or FAIL. Name the earliest
unresolved decision and route back to it.

## 6. Troubleshoot a symptom

| Symptom | Likely failure | Corrective direction |
|---|---|---|
| “This could go in either of two branches for unrelated reasons.” | Mixed axis, wrong unit boundary, or false tree | Revisit the earliest of unit boundary, relationship, or axis. |
| “The list feels random.” | No meaningful ordering relation | Name the canonical order or remove the false sequence. |
| “The parent name is also one of its own children.” | False superordinate | Raise, split, or rename the parent so it remains more abstract. |
| “The tree is deep because every attribute combination has a folder.” | Matrix forced into a tree | Represent the independent dimensions independently. |
| “A new case fits only after stretching every definition.” | Collective-exhaustiveness gap | Add the missing structure or return the gap for decision. |
| “A nested node has two valid relationship readings.” | Relationship ambiguity | Return `AMBIGUOUS`; resolve the relation before continuing. |

## 7. Author a structure from scratch

When no candidate structure exists, nominate a flat set of candidate concepts
without imposing hierarchy.

Determine whether those candidates are stable structural units with
<a href="1%20%F0%9F%9B%A0%EF%B8%8F%20Determine%20Structural%20Units.md" uid="YF43JX">documentation-system:§5.1</a>.
Merge true duplicates, split compound candidates only through that procedure,
and keep unresolved boundaries explicit.

Then establish their relationships with
<a href="2%20%F0%9F%93%96%20Relationships%20and%20Structural%20Topologies.md" uid="P6V2HN">documentation-system:§5.2</a>
and run this procedure from step 2. The hierarchy, axes, and topology are
outputs of the structural reasoning, not assumptions smuggled into concept
nomination.
