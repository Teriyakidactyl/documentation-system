---
uid: BCSYYG
description: >-
  `Read in full and follow when` *an existing artifact must be assessed
  against governing specifications, norms, or declared commitments without
  changing it* `to` **produce typed findings and explicit clean coverage that
  distinguish detected faults, uncertainty, and unexamined scope**.
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

# 🛠️ Validate an Artifact

Validation makes claims about an existing artifact. It does not mutate the
artifact. A detected fault is evidence for a later revision, not permission to
choose and apply a repair during the validation pass.

**Terms.**

| Term | Meaning |
|---|---|
| **frame** | The external specifications, norms, accepted criteria, and declared commitments against which the artifact is assessed. |
| **lens** | One typed fault class or conformance question run as an independent pass. |
| **finding** | A concrete observed deviation supported by artifact evidence and a frame criterion or intrinsic consistency rule. |
| **checked-clean** | An explicitly examined scope in which the named lens or criterion produced no finding. |
| **uncertain** | A suspected issue for which the available frame or evidence does not determine a finding. |

## 1. Fix the validation frame

Identify the authority for every claim the validation is allowed to make.
Applicable sources can include an accepted change frame, document
specification, schema, style rules, repository conventions, interface
contracts, or explicit acceptance criteria.

Do not substitute preference for a missing norm. When the artifact declares its
own commitments, those commitments are valid validation inputs. When no
external or declared criterion determines a judgment, report the observation as
uncertain rather than inventing a rule.

Freeze the frame for the pass. Validation against a moving frame cannot
demonstrate conformance.

## 2. Inventory the artifact

Enumerate the artifact's named and structural elements before judging them.
Include the applicable forms of sections, definitions, identifiers, keys,
references, anchors, citations, declarations, dependencies, and external
targets.

Treat the inventory as the coverage surface. A later clean claim is meaningful
only when its scope can be distinguished from material that was never examined.

## 3. Run typed passes

Run one lens at a time over the full in-scope artifact. Do not combine fault
classes into a general review; an easy finding in one class must not stand in
for inspection of another.

Use the lenses required by the frame and artifact type. At minimum, test the
applicable categories below:

| Lens | Question |
|---|---|
| **Requirement conformance** | Does each governing criterion have observable supporting evidence, with no artifact behavior or statement that violates it? |
| **Referential integrity** | Does every named target resolve correctly, and does every defined named element have a legitimate consumer or purpose? |
| **Structural consistency** | Do the artifact's parts, ordering, hierarchy, and declared structure agree with one another and with the frame? |
| **Semantic consistency** | Are claims mutually compatible, current, terminology-coherent, and free of unresolved placeholders or stale assumptions? |
| **Surface conformance** | Where prose or another styled surface is present, does it satisfy its governing grammar, style, formatting, and mechanical rules? |
| **Suspected drift** | Is any passage or structure plausibly shaped by an assumption the artifact has revised elsewhere even though no enumerable violation can yet be proved? |

A lens with no findings still produces a `checked-clean` result. Do not invent a
finding to populate an empty pass.

For referential and semantic work, explicitly check for dangling references,
orphaned definitions, stale claims, internal contradictions, terminological
inconsistency, unresolved placeholders, structural orphans, and genuine
suspected drift.

## 4. Separate detection from repair

Describe each finding in terms of the observed artifact, the violated
criterion, and the evidence. Do not rewrite the artifact during validation.

Where several repairs are plausible, validation stops at the fault. Where one
repair is mechanically determined by an authoritative rule, record that fact
without applying it unless the task has separately entered a revision
procedure.

Keep uncertainty explicit. A suspected inconsistency with insufficient evidence
is not a clean result and is not a defect proven by confidence.

## 5. Emit the validation record

Return one record:

```yaml
validation-record:
  frame: <sources that governed the pass>
  findings: []       # { unit, lens, criterion, fault, evidence }
  checked-clean: []  # { unit, lens-or-criterion, evidence }
  uncertain: []      # { unit, lens-or-criterion, observation, reason }
  out-of-scope: []   # { unit, reason }
```

Every required lens must appear through a finding or `checked-clean` evidence.
Every in-scope unit must be represented in `findings`, `checked-clean`, or
`uncertain`. Do not report the artifact as validated when required scope is
only present in `out-of-scope`.

A clean validation result means the declared frame was tested over the declared
scope and no violation was found. It does not mean that no possible error exists
outside that frame or scope.
