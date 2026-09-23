---
uid: 5SK5Z4
description: >-
  `Consult when` *a formal Validation result must be communicated beyond the
  validating context or retained as assurance evidence* `to` **distinguish
  validation reasoning, bounded validation records, transmissible receipts,
  and optional durable evidence without turning ordinary self-checking into a
  persistent process ledger**.
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

Validation is first a reasoning operation: compare a representation with a
criterion and determine whether the criterion is satisfied. That reasoning can
occur while authoring, revising, or reviewing; it is not inherently a
post-operation stage.

A bounded Validation pass is different. It deliberately fixes a frame, scope,
and set of lenses so the resulting assurance can be accounted for independently
of mutation. Apply
<a href="2%20%F0%9F%9B%A0%EF%B8%8F%20Validate%20an%20Artifact.md" uid="BCSYYG">documentation-system:§7.2</a>
when a governing process explicitly requires that bounded assurance.

The evidence model is:

```text
validation reasoning
    │
    └── when bounded assurance is selected
            ↓
       validation pass
            ↓
       validation record
            │
            ├── same context can consume the result directly
            │
            └── result must cross a context/process boundary
                    ↓
             validation receipt
                    │
                    └── evidence itself must survive
                            ↓
                     durable storage
```

Do not create a receipt merely because validation reasoning occurred.

## 1. Evidence concepts

| Term | Meaning |
|---|---|
| **validation reasoning** | Comparison of a representation with a governing criterion. It may be interleaved with authoring or revision and normally leaves no independent artifact. |
| **validation pass** | A bounded application of validation reasoning over a declared frame, scope, and set of lenses for an explicit assurance purpose. |
| **Validation Fault** | A confirmed violation of a criterion established by validation evidence. Tool-detected and authored faults share this domain meaning even when their native evidence differs. |
| **checked-clean** | An explicitly examined scope in which the named lens or criterion produced no Validation Fault. |
| **uncertain** | An observation for which the available frame or evidence does not determine whether a Validation Fault exists. |
| **out-of-scope** | Material deliberately excluded from the bounded validation claim. |
| **validation record** | The immediate semantic result of one validation pass: frame, scope, Validation Faults, checked-clean evidence, uncertainty, and out-of-scope material. |
| **validation receipt** | A validation record packaged so its assurance result can be transmitted across a context, reviewer, agent, process, or task boundary. |
| **validation basis** | When exact-state binding is required, the subject state and governing frame or dependency states to which the receipt's claims apply. |

A receipt is a communication representation, not evidence that every ordinary
authoring or revision operation requires a separate validation phase.

## 2. Select bounded Validation explicitly

Ordinary competent authoring and revision use validation reasoning while work is
performed. They do not require a formal Validation pass merely to prove that the
author checked their own work.

Use a bounded Validation pass when an assurance requirement positively selects
one, for example:

- an explicit user or process request for validation;
- an acceptance gate requiring accounted validation coverage;
- independent review separated from the authoring or revision context;
- a high-consequence or audit workflow whose governing specification requires
  formal assurance; or
- another declared requirement that makes the validation operation itself part
  of acceptance.

Context loss alone does not create an assurance requirement. A future agent can
normally read the current artifact, current governing information, and current
task, then perform the work required now. Preserve prior validation because its
occurrence or result has a continuing job, not merely because a later agent may
be amnesiac.

## 3. Emit the record at the validation boundary

A bounded Validation pass emits one validation record. Preserve the distinctions
among faults, clean coverage, uncertainty, and excluded scope:

```yaml
validation-record:
  frame: <sources that governed the pass>
  faults: []          # { unit, lens, criterion, fault, evidence }
  checked-clean: []   # { unit, lens-or-criterion, evidence }
  uncertain: []       # { unit, lens-or-criterion, observation, reason }
  out-of-scope: []    # { unit, reason }
```

A clean record means the declared frame was tested over the declared scope and
no Validation Fault was established there. It does not claim universal
error-freedom.

A compiler, linter, test, or other deterministic validator may produce a native
`Diagnostic`, test result, or equivalent machine finding. When a formal
validation record needs to account for that evidence, the native result can
establish a Validation Fault without becoming a second fault ontology.

## 4. Create a receipt only for communication

Package the validation record as a receipt when another context or process must
consume the validation result without repeating the pass.

Typical cases include:

```text
authoring context
    → independent validation context
    → receipt returned to author/coordinator

agent A
    → validation
    → receipt
    → agent B continues the workflow
```

When the validating and consuming work remain in one continuous context, the
validation record can remain ordinary task state. Serializing and persisting it
adds no assurance merely by existing.

The receipt preserves enough of the record for the receiving context to know
what was examined, against what frame, with which lenses, and with what result.
It records auditable evidence and concise rationale needed to support the
conclusion; it does not require a transcript of private reasoning.

## 5. Persist only when assurance must outlive the context

Durability is a separate decision from producing a receipt.

Persist a receipt when a governing process requires the assurance evidence
itself to survive the immediate coordination context, such as a release
attestation, audit requirement, durable independent approval, or another
explicit cross-context tracking obligation.

When durability requires claims about an exact repository state, bind the
receipt to an exact validation basis. Artifact identity and representation state
remain distinct: a controlled `uid` identifies which artifact is involved,
while a Git object or equivalent state identifier can identify the exact
representation examined.

Do not add receipt identifiers, last-validation timestamps, validation status,
or validation-version fields to ordinary artifact frontmatter merely because a
validation occurred. Recording assurance must not mutate the validated subject
solely to record that it was inspected.

Cheap deterministic checks normally remain authoritative by recomputation.
Persist a deterministic result only when the run itself carries required
provenance or would be materially costly or impossible to reproduce.

Repository Information Storage in Document Control owns the choice among
ordinary files, sideband files, Git-attached metadata, separate histories, and
other Git-backed storage methods. Git Notes are a possible object-attached
storage pattern for exact-state assurance evidence, not the default
representation of Validation.

## 6. Track fault lifecycle only when coordination requires it

Most Validation Faults need no durable identity. A current deterministic fault
can be recomputed, projected beside source, repaired, and disappear on the next
check.

When a cross-context workflow must coordinate the lifecycle of a particular
fault, give that fault a durable identifier in the receipt and preserve events
rather than mutating the original observation:

```text
Validation Fault F1 observed
        ↓
revision addresses F1
        ↓
later validation explicitly rechecks F1
        ↓
fault status is derived
```

A revision that claims to address a fault does not close it. Later validation
establishes whether the criterion is now checked clean, the fault remains, or
the result is uncertain. The original receipt continues to describe the state
in which the fault was observed.

This lifecycle is an optional coordination pattern. Do not introduce fault IDs,
open/closed status, or durable resolution records unless another context or
governing process actually needs to track them.
