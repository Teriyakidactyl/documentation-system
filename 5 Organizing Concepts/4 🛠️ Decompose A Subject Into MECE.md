---
uid: K8T4ZM
description: >-
  `Read in full and follow when` *a consequential structure must be authored
  from scratch, an existing structure requires formal MECE validation, or Test
  A Placement leaves an ambiguity whose resolution will become structural
  precedent* `to` **derive and validate the structure explicitly, returning
  PASS, FAIL, or AMBIGUOUS without guessing**.
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

# 🛠️ Decompose A Subject Into MECE

Use this procedure for structural decisions whose consequences justify formal
decomposition. Routine placement belongs in
<a href="1%20%F0%9F%9B%A0%EF%B8%8F%20Test%20A%20Placement.md" uid="M4R8XC">documentation-system:§5.1</a>.
This procedure takes over when a new taxonomy or other reusable structure must
be authored, when an important existing structure needs formal validation, or
when the lightweight placement test leaves an ambiguity that future decisions
would inherit.

Every completed decomposition evaluates the target structure for **MECE**:
mutual exclusivity, so distinct members do not compete for the same
responsibility under an exclusive axis, and collective exhaustiveness, so the
declared domain is covered without stretching category definitions.

## 1. Apply the invariants

Keep these conditions true throughout the decomposition:

- **MECE.** Exclusive siblings do not overlap; the declared domain has no
  confirmed gap.
- **Single-axis locking.** A classification or ordered layer answers one
  organizing question. Do not mix dimensions at the same sibling level.
- **Superordinate validation.** A parent remains more abstract than every child
  it contains. A parent is not a peer of its contents.
- **Ownership before containment.** Identify the concept responsible for an
  item before selecting the representation that holds it. Apply
  <a href="3%20%F0%9F%92%A1%20Ownership%20and%20Containment.md" uid="W9D5TG">documentation-system:§5.3</a>.
- **Deterministic ordering where order carries meaning.** When the selected
  topology is ordered, name the canonical ordering rule rather than accepting
  incidental sequence.

Do not force exclusivity onto a matrix or graph merely because MECE is the
validation frame. Exclusivity applies to a layer only when that layer claims
exclusive membership.

## 2. Select the structural topology

Consult
<a href="2%20%F0%9F%93%96%20Structural%20Topologies.md" uid="P6V2HN">documentation-system:§5.2</a>
and select the topology each layer actually preserves: tree, list, matrix, or
graph.

Choose topology from the relation in the data, not from the syntax available to
represent it. A filesystem may force a tree-shaped representation without
making every conceptual relation a tree. A larger structure may change topology
between layers when each layer still has one legible governing relation.

Record any external constraint that makes a topology non-negotiable before
decomposing the subject. A constraint can determine representation without
proving that the subject's underlying relation has the same shape.

## 3. Identify the unit of analysis

Before classifying whole files, folders, documents, modules, or other physical
containers, decompose the subject into **facet-coherent units**: independently
addressable fragments whose active organizing facets do not conflict.

Use S. R. Ranganathan's PMEST—Personality, Matter, Energy, Space, and
Time—as a completeness prompt for candidate facets. PMEST originates in Colon
Classification. This procedure preserves the five fundamental category names
but adapts them to repository structural analysis; it does not implement Colon
Classification notation, citation order, or its full classification rules.

| PMEST category | Operational question here |
|---|---|
| Personality | What primary subject or entity is this about? |
| Matter | What substance, content, or artifact type is involved? |
| Energy | What action, process, or work verb applies? |
| Space | What location, scope, or contextual boundary applies? |
| Time | What lifecycle position or temporal stage applies? |

Only active facets need values. Two candidate concepts belong to the same unit
while their active facet values agree. A divergence that changes how the unit
must be classified, owned, sequenced, or governed marks a boundary.

Split a candidate unit when it needs incompatible primary actions, owners, or
organizing relations to describe its members. Do not assign one classification
to a whole physical container merely because its contents are co-located.

For each resulting unit, record:

1. its active facet values;
2. its conceptual owner;
3. the topology and axis that organize it;
4. the specific divergence that separates it from adjacent units.

If this step cannot establish coherent units, return **AMBIGUOUS** before
building deeper structure.

## 4. Choose an execution path

Choose one path from the condition of the problem, not by preference.

### 4.1 Top-down: shape first

Use top-down decomposition when an external system or representation imposes a
non-negotiable shape.

1. State the imposed shape and constraint.
2. Draft the smallest set of candidate top-level containers or categories.
3. Test the empty structure for overlap and obvious gaps.
4. Populate it with the units from <a href="4%20%F0%9F%9B%A0%EF%B8%8F%20Decompose%20A%20Subject%20Into%20MECE.md#3-identify-the-unit-of-analysis" uid="K8T4ZM">documentation-system:§5.4#3</a>.
5. Abandon or revise the hypothesis when collisions are frequent rather than
   stretching category definitions to preserve it.

### 4.2 Bottom-up: data first

Use bottom-up decomposition for unstructured data, overlapping concepts, or
legacy structures whose current categories are not trustworthy.

1. Atomize compound subjects into the facet-coherent units from <a href="4%20%F0%9F%9B%A0%EF%B8%8F%20Decompose%20A%20Subject%20Into%20MECE.md#3-identify-the-unit-of-analysis" uid="K8T4ZM">documentation-system:§5.4#3</a>.
2. Record the attributes that distinguish those units.
3. Compare units across the candidate axes.
4. Merge true duplicates and surface uncovered combinations or concepts as
   possible gaps.
5. Let the relation determine the topology: subsumption tends toward a tree;
   independent attributes toward a matrix; meaningful order toward a list;
   explicit relational edges toward a graph.

### 4.3 Synthesis: hypothesize then validate

Use synthesis when a plausible structure already exists but still needs formal
confirmation.

1. Draft the likely structure top-down.
2. Run the units bottom-up against that hypothesis.
3. Treat a repeated collision or forced exception as evidence against the
   hypothesis rather than as an invitation to special-case it.
4. Continue only when the hypothesized structure and the unit analysis agree.

## 5. Locate the structural horizon where needed

Use the **structural horizon** only in nested structures where classification
(`is-a`) and schema composition (`has-a`) can be confused by the same syntax.
Do not force part-of relations or explicit graph edges through this test; they
should already have been identified by <a href="4%20%F0%9F%9B%A0%EF%B8%8F%20Decompose%20A%20Subject%20Into%20MECE.md#2-select-the-structural-topology" uid="K8T4ZM">documentation-system:§5.4#2</a> and <a href="4%20%F0%9F%9B%A0%EF%B8%8F%20Decompose%20A%20Subject%20Into%20MECE.md#3-identify-the-unit-of-analysis" uid="K8T4ZM">documentation-system:§5.4#3</a>.

For each candidate node `N` under parent `P`, apply both tests:

- **Test A — is-a:** complete “`N` is a type of `P`.” It holds only when `N`
  names a distinct subtype or variant of `P`, not merely something contained by
  or associated with it.
- **Test B — has-a:** complete “`N` is a named slot or field of `P`, where
  different instances of `P` could carry different values for `N`.”

Classify the result explicitly:

| Test A | Test B | Result |
|---|---|---|
| holds | fails | `is-a` |
| fails | holds | `has-a` |
| holds | holds | `AMBIGUOUS` |
| fails | fails | relation unresolved; revisit <a href="4%20%F0%9F%9B%A0%EF%B8%8F%20Decompose%20A%20Subject%20Into%20MECE.md#2-select-the-structural-topology" uid="K8T4ZM">documentation-system:§5.4#2</a>–<a href="4%20%F0%9F%9B%A0%EF%B8%8F%20Decompose%20A%20Subject%20Into%20MECE.md#3-identify-the-unit-of-analysis" uid="K8T4ZM">documentation-system:§5.4#3</a> |

The horizon is branch-local. Different branches may change from classification
to composition at different depths.

Above the horizon, evaluate uniqueness by the classified term: two exclusive
concepts should not carry the same leaf term merely at different addresses.
Below the horizon, evaluate uniqueness by full address: repeating a property
name under different owners can be valid because the qualified slots differ.

## 6. Run terminal MECE validation

Validate only after the structure has stabilized.

For every exclusive layer:

1. **Check overlap.** Attempt to place every unit. A unit that legitimately
   satisfies two exclusive siblings exposes an axis or relation problem.
2. **Check gaps.** Look for a real member of the declared domain that fits no
   sibling without stretching a definition.
3. **Check superordinates.** Confirm every parent remains more abstract than
   its children.
4. **Check the structural horizon where applicable.** Do not diagnose a
   collision using leaf-term uniqueness on one side of the horizon and
   full-address uniqueness on the other.
5. **Check parent-chain completeness.** Do not issue a verdict about a nested
   collision while an intermediate relation remains unclassified.

Use two cheap probes when exhaustiveness is uncertain:

- invert a category's completeness claim by asking what would *not* belong and
  whether such a case exists;
- bring a concrete counter-example from the same kind of organizing problem and
  ask where it fits without modifying a definition.

A counter-example confirms a gap. Failure to find one is evidence of
exhaustiveness, not proof.

**Record the validation evidence before issuing a verdict.** The record must let
another reader audit the result without reconstructing unstated reasoning.

- Record one row for every facet-coherent unit from <a href="4%20%F0%9F%9B%A0%EF%B8%8F%20Decompose%20A%20Subject%20Into%20MECE.md#3-identify-the-unit-of-analysis" uid="K8T4ZM">documentation-system:§5.4#3</a>, including its active
  PMEST values, owner, topology and axis, and boundary from adjacent units.
- When <a href="4%20%F0%9F%9B%A0%EF%B8%8F%20Decompose%20A%20Subject%20Into%20MECE.md#5-locate-the-structural-horizon-where-needed" uid="K8T4ZM">documentation-system:§5.4#5</a> applies, record every examined node with its parent, the literal Test A
  and Test B propositions and their results, and the resulting classification.
  Do not replace the evaluated propositions with bare `holds` / `fails` labels.
- Record each overlap or gap candidate that could affect the verdict and its
  disposition.
- Confirm that the unit-record count matches the number of units identified in
  <a href="4%20%F0%9F%9B%A0%EF%B8%8F%20Decompose%20A%20Subject%20Into%20MECE.md#3-identify-the-unit-of-analysis" uid="K8T4ZM">documentation-system:§5.4#3</a> and that every load-bearing parent relation required by a nested verdict
  has been tested. Fill any shortfall before continuing.

A verdict without this complete validation record is incomplete even when its
conclusion later proves correct.

Declare exactly one outcome:

- **PASS:** no confirmed overlap or gap remains and every load-bearing relation
  needed for the verdict is resolved.
- **FAIL:** a confirmed overlap, gap, shadowed parent, or other structural
  contradiction remains.
- **AMBIGUOUS:** one or more load-bearing relations admit competing valid
  readings, so PASS or FAIL cannot yet be justified.

Do not collapse **AMBIGUOUS** into either PASS or FAIL. Name the unresolved node,
relation, or axis and return it for an explicit decision.

## 7. Troubleshoot a symptom

Use this reverse lookup when the structure feels wrong before the failing
primitive is known.

| Symptom | Likely failure | Corrective direction |
|---|---|---|
| “This could go in either of two branches for unrelated reasons.” | Axis tilting or a false tree | Revisit <a href="4%20%F0%9F%9B%A0%EF%B8%8F%20Decompose%20A%20Subject%20Into%20MECE.md#2-select-the-structural-topology" uid="K8T4ZM">documentation-system:§5.4#2</a>–<a href="4%20%F0%9F%9B%A0%EF%B8%8F%20Decompose%20A%20Subject%20Into%20MECE.md#3-identify-the-unit-of-analysis" uid="K8T4ZM">documentation-system:§5.4#3</a>; separate axes or use a matrix/graph. |
| “The list feels random.” | No meaningful ordering relation | Name the canonical order or remove the false sequence. |
| “The parent name is also one of its own children.” | Superordinate shadowing | Raise or rename the parent so it remains more abstract. |
| “The structure mixes very broad concepts with tiny details.” | Granularity mismatch | Re-run <a href="4%20%F0%9F%9B%A0%EF%B8%8F%20Decompose%20A%20Subject%20Into%20MECE.md#3-identify-the-unit-of-analysis" uid="K8T4ZM">documentation-system:§5.4#3</a> and split or regroup at coherent boundaries. |
| “The tree is deep because every attribute combination has a folder.” | Matrix forced into a tree | Represent the independent facets separately. |
| “A new case fits only after stretching every existing definition.” | Collective-exhaustiveness gap | Add the missing concept or return the gap for decision. |
| “The subject declares its categories non-exclusive.” | Exclusivity applied to the wrong topology | Validate qualified identity or independent axes instead of forcing exclusive siblings. |
| “A nested node can validly be read as both subtype and property.” | Structural-horizon ambiguity | Return `AMBIGUOUS`; make the relationship explicit before validation. |

## 8. Author a taxonomy from scratch

When no candidate structure exists, add concept nomination before <a href="4%20%F0%9F%9B%A0%EF%B8%8F%20Decompose%20A%20Subject%20Into%20MECE.md#3-identify-the-unit-of-analysis" uid="K8T4ZM">documentation-system:§5.4#3</a>.

Produce a flat list of candidate concepts without imposing hierarchy. Enumerate
directly when the domain and vocabulary are stable. For fuzzy domains, use
assumption inversion or cross-domain comparison to surface candidates that
direct enumeration may miss. For collaborative or contested domains, collect
candidate concepts before attempting to organize them.

Nomination is complete when the candidate set exists without assumed parentage.
Then run <a href="4%20%F0%9F%9B%A0%EF%B8%8F%20Decompose%20A%20Subject%20Into%20MECE.md#3-identify-the-unit-of-analysis" uid="K8T4ZM">documentation-system:§5.4#3</a>–<a href="4%20%F0%9F%9B%A0%EF%B8%8F%20Decompose%20A%20Subject%20Into%20MECE.md#6-run-terminal-mece-validation" uid="K8T4ZM">documentation-system:§5.4#6</a> unchanged. The hierarchy, axes, and topology are outputs of the
decomposition, not inputs smuggled into concept nomination.

Before putting a newly authored taxonomy into service, stress-test each
load-bearing category with the gap probes from <a href="4%20%F0%9F%9B%A0%EF%B8%8F%20Decompose%20A%20Subject%20Into%20MECE.md#6-run-terminal-mece-validation" uid="K8T4ZM">documentation-system:§5.4#6</a> and return any unresolved
relation as **AMBIGUOUS** rather than creating precedent from a guess.
