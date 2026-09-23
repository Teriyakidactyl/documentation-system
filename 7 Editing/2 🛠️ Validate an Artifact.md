---
uid: BCSYYG
description: >-
  `Read in full and follow when` *an artifact must be assessed against
  governing specifications, norms, or declared commitments without changing
  it, including before a conformance or completion claim that lacks current
  applicable evidence* `to` **produce a typed validation record that
  distinguishes findings, explicit clean coverage, uncertainty, and unexamined
  scope**.
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

Validation makes claims about an artifact. It does not mutate the artifact. A
detected fault is evidence for a later revision, not permission to choose and
apply a repair during the validation pass.

Before asserting that an artifact satisfies a governing specification, norm,
accepted change, or declared commitment, establish current evidence for every
lens and criterion required by that claim. A newly authored artifact is an
artifact for this purpose: authoring does not make its own conformance
self-evident.

**Terms.**

| Term | Meaning |
|---|---|
| **frame** | The external specifications, norms, accepted criteria, and declared commitments against which the artifact is assessed. |
| **lens** | One typed fault class or conformance question run as an independent pass. |
| **finding** | A concrete observed deviation supported by artifact evidence and a frame criterion or intrinsic consistency rule. |
| **checked-clean** | An explicitly examined scope in which the named lens or criterion produced no finding. |
| **uncertain** | A suspected issue for which the available frame or evidence does not determine a finding. |
| **validation record** | The immediate semantic result of this validation operation: its frame, scope, findings, checked-clean evidence, uncertainty, and out-of-scope material. |

## 1. Fix the validation frame

Identify the authority for every claim the validation is allowed to make.
Applicable sources can include an accepted change frame, document
specification, schema, house style, artifact-specific style sheet, repository
conventions, interface contracts, or explicit acceptance criteria.

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

## 6. Preserve evidence when reconstruction would lose it

The validation record is the immediate result of the pass. Persist it as a
durable validation receipt when reproducing the evidence would lose meaningful
work, context, or provenance.

Authored semantic inspection is the normal case for persistence when a future
agent would otherwise have no evidence that the frame, scope, and named lenses
were actually examined. Preserve the record's findings, checked-clean evidence,
uncertainty, out-of-scope material, and concise rationale needed to understand
the claims.

Do not persist every deterministic result by default. Re-run a cheap compiler,
linter, schema validator, or equivalent deterministic check when recomputation
is cheaper and more authoritative than maintaining its historical result.
Persist deterministic evidence only when a concrete requirement makes the run
itself significant, such as expensive execution, external dependency,
environment-specific provenance, release attestation, or compliance evidence.

A receipt is evidence about the state that was examined, not a Boolean
declaration that the artifact remains valid forever. Bind durable evidence to
the exact subject and governing basis needed for its claims. If the subject,
frame, or relevant dependency changes, treat the affected receipt as stale until
current validation re-establishes the claim.

Receipt persistence remains outside the validated artifact. Do not add
last-validation timestamps, receipt identifiers, validation versions, or
validation status to ordinary artifact frontmatter merely because validation
occurred.
