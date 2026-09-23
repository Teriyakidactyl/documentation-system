---
uid: BCSYYG
description: >-
  `Read in full and follow when` *a governing process explicitly requires a
  bounded assurance assessment of an artifact against specifications, norms, or
  declared commitments without changing it* `to` **produce a typed validation
  record that accounts for Validation Faults, explicit clean coverage,
  uncertainty, and unexamined scope**.
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

Validation reasoning compares a representation with a governing criterion. It
can occur while authoring, revising, or reviewing and is part of ordinary
competent work.

This procedure governs a **bounded Validation pass**: an explicit assurance
operation whose frame, scope, and lenses must be independently accountable.
Use it only when a user, artifact, workflow, acceptance gate, independent-review
requirement, or other governing process positively requires that assurance.

A Validation pass makes claims about an artifact. It does not mutate the
artifact. A detected Validation Fault is evidence for a later authoring or
Revision operation, not permission to choose and apply a repair during the
pass.

**Terms.**

| Term | Meaning |
|---|---|
| **validation reasoning** | Comparison of a representation with a governing criterion; it may be interleaved with mutation work and need not produce a record. |
| **validation pass** | A bounded assurance operation over a declared frame, scope, and set of lenses. |
| **frame** | The external specifications, norms, accepted criteria, and declared commitments against which the artifact is assessed. |
| **lens** | One typed fault class or conformance question run as an independent pass. |
| **Validation Fault** | A concrete observed violation supported by artifact evidence and a frame criterion or intrinsic consistency rule. |
| **checked-clean** | An explicitly examined scope in which the named lens or criterion produced no Validation Fault. |
| **uncertain** | A suspected issue for which the available frame or evidence does not determine whether a Validation Fault exists. |
| **validation record** | The immediate semantic result of the bounded pass: frame, scope, Validation Faults, checked-clean evidence, uncertainty, and out-of-scope material. |

## 1. Confirm the assurance requirement

Identify the requirement that selected a bounded Validation pass. Do not invoke
this procedure merely to prove that an author or reviser checked their own work.

State what the consuming user, reviewer, process, or acceptance gate needs the
pass to establish. If no governing requirement calls for independently
accountable validation, return to the authoring or Revision procedure and use
validation reasoning there instead.

The assurance requirement determines the scope that must be accounted for; it
does not predetermine whether the result will be clean.

## 2. Fix the validation frame

Identify the authority for every claim the validation is allowed to make.
Applicable sources can include an accepted change frame, document
specification, schema, house style, artifact-specific style sheet, repository
conventions, interface contracts, or explicit acceptance criteria.

Do not substitute preference for a missing norm. When the artifact declares its
own commitments, those commitments are valid validation inputs. When no
external or declared criterion determines a judgment, report the observation as
uncertain rather than inventing a rule.

Freeze the frame for the pass. Validation against a moving frame cannot
demonstrate bounded assurance.

## 3. Inventory the artifact

Enumerate the artifact's named and structural elements before judging them.
Include the applicable forms of sections, definitions, identifiers, keys,
references, anchors, citations, declarations, dependencies, and external
targets.

Treat the inventory as the coverage surface. A later clean claim is meaningful
only when its scope can be distinguished from material that was never examined.

## 4. Run typed passes

Run one lens at a time over the full in-scope artifact. Do not combine fault
classes into a general review; an easy fault in one class must not stand in for
inspection of another.

Use the lenses required by the frame and artifact type. For prose-bearing
artifacts, keep the established editorial pass name when one applies. The pass
scopes the validation lenses; it does not grant mutation authority.

| Editorial pass | Validation emphasis |
|---|---|
| **developmental editing** | Requirement, structural, and semantic lenses over the artifact's macro architecture, coverage, sequence, and logic. |
| **line editing** | Semantic and surface lenses over paragraph- and sentence-level clarity, flow, emphasis, and local logic. |
| **copyediting** | Referential, semantic, and surface lenses over correctness, consistency, terminology, usage, cross-references, and house style. |
| **proofreading** | Surface lens after content and structure are stable; inspect typographical, punctuation, spacing, formatting, and other microscopic mechanical defects without reopening structure. |

At minimum, test the applicable categories below:

| Lens | Question |
|---|---|
| **Requirement conformance** | Does each governing criterion have observable supporting evidence, with no artifact behavior or statement that violates it? |
| **Referential integrity** | Does every named target resolve correctly, and does every defined named element have a legitimate consumer or purpose? |
| **Structural consistency** | Do the artifact's parts, ordering, hierarchy, and declared structure agree with one another and with the frame? |
| **Semantic consistency** | Are claims mutually compatible, current, terminology-coherent, and free of unresolved placeholders or stale assumptions? |
| **Surface conformance** | Where prose or another styled surface is present, does it satisfy its governing grammar, style, formatting, and mechanical rules? |
| **Suspected drift** | Is any passage or structure plausibly shaped by an assumption the artifact has revised elsewhere even though no enumerable violation can yet be proved? |

A lens with no Validation Fault still produces a `checked-clean` result. Do not
invent a fault to populate an empty pass.

For referential and semantic work, explicitly check for dangling references,
orphaned definitions, stale claims, internal contradictions, terminological
inconsistency, unresolved placeholders, structural orphans, and genuine
suspected drift.

## 5. Separate detection from repair

Describe each Validation Fault in terms of the observed artifact, the violated
criterion, and the evidence. Do not rewrite the artifact during the bounded
Validation pass.

Where several repairs are plausible, validation stops at the fault. Where one
repair is mechanically determined by an authoritative rule, record that fact
without applying it unless the task separately enters an authoring or Revision
operation.

Keep uncertainty explicit. A suspected inconsistency with insufficient evidence
is not a clean result and is not a defect proven by confidence.

## 6. Emit the validation record

Return one record:

```yaml
validation-record:
  frame: <sources that governed the pass>
  faults: []          # { unit, lens, criterion, fault, evidence }
  checked-clean: []   # { unit, lens-or-criterion, evidence }
  uncertain: []       # { unit, lens-or-criterion, observation, reason }
  out-of-scope: []    # { unit, reason }
```

Every required lens must appear through a Validation Fault or
`checked-clean` evidence. Every in-scope unit must be represented in
`faults`, `checked-clean`, or `uncertain`. Do not report the artifact as
validated when required scope is only present in `out-of-scope`.

A clean validation result means the declared frame was tested over the declared
scope and no Validation Fault was found. It does not mean that no possible error
exists outside that frame or scope.

If the result must cross a context or process boundary, package the record as a
Validation Receipt using
<a href="5%20%F0%9F%93%96%20Validation%20Evidence.md" uid="5SK5Z4">documentation-system:§7.5</a>.
Do not persist the record merely because the pass occurred.
