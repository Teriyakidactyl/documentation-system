---
uid: 5SK5Z4
description: >-
  `Consult when` *validation evidence may need to survive the validating task,
  be reused by an amnesiac agent, or be combined with reproducible checks* `to`
  **distinguish validation records, durable receipts, exact validation basis,
  and current status without mutating the validated artifact or treating every
  check as permanently stored evidence**.
quadrant: Reference
outline:
  topology: tree
  axis: validation evidence concept
  numbering: hierarchical-decimal
writing-style:
  formality: professional
  tone: clinical/detached
  mode: declarative
  density: compressed/dense
  abstraction: concrete/specific
  redundancy: zero
  signposting: entry-headers only
  register: technical
---

# 📖 Validation Evidence

Validation evidence records what was actually examined, against which authority,
over which scope, and with what result. It allows a later agent to distinguish
material that was checked clean from material that was never examined without
turning a past validation into a timeless claim of correctness.

The evidence model is:

```text
validation operation
        ↓
validation record
        │
        ├── cheap deterministic evidence → recompute when needed
        │
        └── evidence worth preserving    → validation receipt
                                                ↓
                                  compare with current basis
                                                ↓
                                        validation status
```

## 1. Evidence concepts

| Term | Meaning |
|---|---|
| **validation record** | The immediate semantic result of one validation operation: frame, scope, findings, checked-clean evidence, uncertainty, and out-of-scope material. |
| **validation basis** | The exact subject state and governing frame or dependency states required for the recorded claims to remain applicable. |
| **validation receipt** | A durable, schema-valid representation of a validation record bound to its validation basis. |
| **validation status** | A current projection assembled from applicable receipts and reproducible checks; it states what evidence applies now rather than what once happened. |
| **authored evidence** | Evidence produced by a human or agent where interpretation, contextual judgment, semantic inspection, or nontrivial coverage work materially contributes to the result. |
| **deterministic evidence** | Evidence mechanically reproducible from declared inputs by a compiler, linter, test, schema validator, or equivalent deterministic tool. |
| **current** | The evidence basis still matches the subject, frame, and dependencies required by the recorded claim. |
| **stale** | A recorded receipt exists, but one or more basis states no longer match the state the receipt evaluated. |
| **not evaluated** | No current evidence establishes that the named lens or criterion was examined. |

A `clean` result and `not evaluated` are different states. Absence of a
finding does not establish that a validation pass occurred.

## 2. Persist evidence selectively

Persist validation evidence when reproducing it would lose meaningful work,
context, or provenance. Recompute deterministic evidence when reproduction is
cheaper and more authoritative than maintaining a receipt.

Authored semantic validation is the default case for a durable receipt when its
coverage or reasoning would otherwise disappear with the task. A future agent
cannot reconstruct that another reviewer actually examined a criterion merely
from the artifact's current appearance.

Cheap deterministic checks are normally rerun. A compiler or linter that can
re-establish its result quickly is itself the more reliable source of current
status. Persist deterministic evidence only when a concrete requirement selects
durability, such as an expensive run, an external dependency that may not remain
available, a release or compliance attestation, or an environment-dependent
result whose provenance is part of the evidence.

Do not persist a receipt merely because a validator exists. Durability is
selected by the cost or loss of reconstruction, not by symmetry between
producers.

## 3. Preserve pre-fix evidence before mutation

When a validation finding will trigger a repair and that validation evidence is
selected for durability, persist the finding against the pre-fix subject state
before the repair changes that state.

This preserves the distinction among:

```text
pre-existing fault
→ observed before mutation

repair
→ authorized mutation

post-edit finding
→ residual or edit-induced fault observed after mutation
```

Do not let the corrective edit become the only surviving evidence that a fault
was ever observed. The pre-fix receipt remains historical evidence bound to the
state that contained the fault; the post-edit validation establishes whether
the resulting state is clean, still faulty, or uncertain.

A revision may contain both receipts in one review or delivery workflow, but
they remain separate validation events with separate subject states. Never
rewrite a pre-fix receipt to describe the repaired state.

A repository-wide baseline sweep follows the same rule. Establish authored
receipts only for lenses and scopes actually examined. Record findings before
their fixes land, then let subsequent validation produce receipts for the
corrected states. Do not manufacture a clean baseline by fixing first and
retrospectively claiming that the original state was examined clean.

## 4. Bind receipts to exact basis

A receipt never means only "this artifact was validated." Bind every durable
claim to the state that was actually examined.

For a controlled artifact, distinguish identity from state:

```text
uid
= which controlled artifact

representation state
= exact content state examined

validation basis
= representation state
  + governing frame state
  + dependency states required by the claim
```

A move or rename does not invalidate evidence merely because the path changed
when the same controlled artifact and applicable representation state remain
identifiable. A content change invalidates claims that depended on the prior
content state. A frame or dependency change can make evidence stale even when
the subject's own content did not change.

The basis must contain enough identity to evaluate those conditions
mechanically. Storage-specific object identifiers are implementation facts,
not replacements for the controlled artifact's `uid`.

## 5. Preserve typed coverage

A durable authored receipt preserves the semantic distinctions of the
validation record instead of reducing them to one Boolean.

At minimum retain:

```yaml
validation-receipt:
  subject:
    uid: <controlled artifact identity>
    state: <exact evaluated representation state>

  basis:
    frame: []
    dependencies: []

  producer:
    kind: authored | tool
    identity: <reviewer or validator identity>

  method:
    procedure: <validation procedure or deterministic validator>
    lenses: []

  findings: []
  checked-clean: []
  uncertain: []
  out-of-scope: []
```

The persisted representation may use another canonical serialization, but its
schema must preserve these meanings.

An authored receipt records auditable evidence and concise rationale needed to
justify the result. It does not require a transcript of private reasoning.
Record the applied criterion, observed artifact evidence, material inference,
and uncertainty needed for another reviewer to understand why the claim was
made.

A tool receipt, when durability is selected, identifies the deterministic
validator, its applicable version or rule set, and the inputs required to
reproduce the result.

## 6. Validate receipts before storage

Treat the receipt representation as structured data. Validate its schema and
cross-field invariants before persistence so minor authoring errors do not
become durable repository memory.

The receipt validator rejects at least:

- a missing or invalid subject identity or subject state;
- an unknown producer kind, result vocabulary, or validation lens;
- a clean result contradicted by recorded findings;
- a tool receipt without the validator identity needed to reproduce it;
- an authored receipt that claims evaluated scope without findings,
  checked-clean evidence, or explicit uncertainty;
- basis references that cannot be resolved where resolution is required; and
- a receipt whose serialization cannot be normalized deterministically.

Schema validity proves that the receipt is structurally admissible. It does not
prove that an authored observation is true. Validation procedure, evidence, and
coverage remain the authority for the underlying claim.

## 7. Derive status rather than storing it as document truth

Validation status is a projection over current evidence:

```text
current subject and frame
        +
applicable durable receipts
        +
recomputed deterministic checks
        ↓
validation status
```

Expose status per lens or criterion. Useful states include:

```text
current / clean
current / findings
current / uncertain
stale
not evaluated
```

Do not collapse those states into `validated: true`.

A receipt can remain valid for one lens while another lens is stale or
unevaluated. Likewise, a clean compiler or lint result does not imply semantic
review occurred, and an authored semantic review does not substitute for a
mechanical invariant that can be checked deterministically.

## 8. Keep receipts outside the validated artifact

Validation remains observational. Recording that validation occurred does not
mutate the validated subject merely to record its status.

Do not add receipt identifiers, last-validation timestamps, validation status,
or validation-version fields to ordinary artifact frontmatter solely because a
validation occurred. The artifact owns what it is and how it is governed;
receipts own evidence about particular states of that artifact; status is
derived from the two.

A separate declaration that an artifact requires particular validation before
acceptance would be a governing specification decision, not a receipt-storage
pointer.

Keep durable receipt storage outside the subject and behind the validation
interface. The selected storage mechanism may use repository version-control
facilities, but agents and guidance reason in terms of records, receipts, basis,
and status rather than storage commands.

## 9. Use current evidence before claiming conformance

Before asserting that an artifact satisfies a governing specification, norm,
accepted change, or declared commitment, determine which validation lenses and
criteria the claim requires.

For each required claim:

1. use current durable evidence when its basis and scope match;
2. rerun cheap deterministic validation when recomputation is authoritative;
3. treat stale evidence as historical evidence, not current proof;
4. treat missing evidence as `not evaluated`; and
5. perform validation for any required lens that remains stale, uncertain, or
   unevaluated.

A prior authored receipt may prevent needless repetition of unchanged semantic
inspection. It does not satisfy a new validation frame merely because the same
artifact was reviewed before.
