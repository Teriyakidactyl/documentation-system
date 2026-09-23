---
uid: SE6M58
description: >-
  `Read in full and follow when` *an existing artifact must incorporate a
  stated change without leaving superseded meaning, broken dependencies, or
  unexamined residual* `to` **freeze the change frame, validate the current
  state, propagate the change, independently validate the result, and return a
  checkable revision record**.
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

# 🛠️ Revise an Artifact

Revision changes an existing artifact so it satisfies an external frame. Do not
use the artifact's current contents, the edits already made, or your own sense
of completion as authority for what remains to be done.

The procedure deliberately separates assessment from mutation:

```text
freeze frame
→ validate current state
→ revise
→ validate resulting state
→ declare residual
```

Validation makes claims about the artifact. Revision changes it. Do not collapse
the two authorities merely because one task invokes both.

**Terms.**

| Term | Meaning |
|---|---|
| **frame** | The frozen, numbered criteria the revised artifact must satisfy. |
| **unit** | One bounded portion of the artifact that can be inspected and changed without treating the whole artifact as one edit. |
| **residual** | Required work not completed by the revision, named explicitly rather than absorbed into a completion claim. |
| **superseded representation** | A representation of a state, rule, term, relationship, or implementation that the accepted change has made non-current. |
| **edit-induced fault** | A defect introduced by the revision that was not present before mutation. |
| **style sheet** | For prose work, an artifact-specific record of editorial decisions such as terminology, capitalization, spelling, numbering, and other consistency choices. It contributes to the frame but does not replace governing specifications or house style. |

## 1. Freeze the change frame

State the accepted change before searching for edit sites. Derive numbered,
checkable criteria that say what must become true, what must stop being true,
and which dependent representations must change as a consequence.

Take the frame from an authority outside the revision itself: an explicit user
decision, accepted design, governing specification, norm, or other confirmed
source. Do not derive the frame from whichever passages first attract attention.

For prose-bearing artifacts, include the applicable document specification,
house style, and artifact-specific style sheet in the frame when they govern the
work. Keep the established editorial term for the surrounding scope when one
fits: developmental editing, line editing, copyediting, or proofreading. A
proofreading pass remains validation-only; if it yields an authorized
correction, enter Revision for that correction rather than expanding the
proofreading mandate. The frozen frame determines the exact authority for this
revision.

Freeze the criteria before the first mutation. If the frame proves wrong or
incomplete, stop, replace it explicitly, and restart coverage against the new
frame. Do not amend criteria merely to make completed edits appear sufficient.

## 2. Validate the current state

Before changing the artifact, apply
<a href="2%20%F0%9F%9B%A0%EF%B8%8F%20Validate%20an%20Artifact.md" uid="BCSYYG">documentation-system:§7.2</a>
against the frozen frame and the full in-scope artifact.

The pre-edit validation record is the detection artifact for the revision. It
separates observed faults from assumptions about where changes will be needed
and records material already checked clean.

Current durable validation evidence may supply checked-clean coverage only when
its subject state, scope, and governing frame match this revision's frozen
frame. A stale receipt or a receipt produced against a different change frame
is historical evidence, not a substitute for revision-specific validation.

Do not begin mutation until the required validation lenses have current
evidence. A search result, edit plan, list of obvious lexical matches, or
mismatched prior receipt is not a substitute for current-state validation.

## 3. Map the implications

Use the frozen frame and the pre-edit validation record to derive the edit set.
Search is a discovery aid, not a completeness test: a representation can embody
the old model without repeating the words that named it.

For each criterion, ask:

- What must now be true?
- What must no longer be true?
- Which definitions, references, examples, structures, names, behaviors, or
  explanations depend on either state?
- Which units would read or behave differently if the new criterion had been
  true when the artifact was first produced?

Include dependencies implied by the accepted change even when the pre-edit
validation did not enumerate them as faults. Validation detects against a frame;
revision must also propagate the consequences of changing that frame.

## 4. Remove superseded representations

Remove superseded representations unless the superseded state itself is
required information for the artifact's job.

Operational guidance, reference material, configuration, and agent-facing
instructions normally carry only current truth. Do not preserve an obsolete
rule, implementation, name, or example merely to narrate the change; leaving it
available gives a future reader another candidate interpretation.

Retain a superseded state only when the artifact requires it as information,
such as an explanation whose job is historical, a migration record, or a local
recurrence-prevention note for a non-obvious failed implementation. Mark
retained material so its non-current role is explicit.

## 5. Apply bounded changes

Change one unit at a time. Trace every mutation to one or more numbered frame
criteria. A change with no criterion is scope creep.

Preserve the artifact's existing job and governing specification unless the
accepted change explicitly changes them. When revising a technical document
requires re-establishing its description, quadrant, outline, or writing style,
apply the relevant authoring rules from
<a href="../2%20Technical%20Writing/1%20%F0%9F%9B%A0%EF%B8%8F%20Write%20A%20Technical%20Document.md" uid="5CFFZW">documentation-system:§2.1</a>
to those authoring decisions; Editing still owns propagation of the resulting
change through the existing artifact.

Record each changed unit and the criterion that required it.

## 6. Validate the resulting state

Apply
<a href="2%20%F0%9F%9B%A0%EF%B8%8F%20Validate%20an%20Artifact.md" uid="BCSYYG">documentation-system:§7.2</a>
again against the frozen frame after mutation. Do not treat the edit log as
evidence that the result is correct. Prior receipts from the pre-edit state are
stale for claims affected by the revision unless their validation basis remains
unchanged and the governing criterion still applies exactly.

Re-scan changed units and inspect the artifact for edit-induced faults:

| Fault | Detection cue |
|---|---|
| **Edit-orphaned definition** | The revision removed the definition's last consumer. |
| **Stranded reference** | A moved, renamed, or removed target left a reference behind. |
| **Doubled representation** | The new representation exists while the superseded one also remains without a required job. |
| **Register break** | New prose violates the governing writing style of its context. |
| **Severed dependency** | A prerequisite, definition, or ordering relation no longer precedes or supports its consumer. |
| **Criterion collision** | Two frame criteria were implemented in incompatible ways. |
| **Scope creep** | A mutation traces to no frame criterion. |
| **Confabulated finding** | A requested additional pass produced a claim unsupported by the frame or artifact after genuine findings were exhausted. |

Do not silently repair a newly discovered issue whose correct resolution is not
determined by the frame. Record it as residual.

## 7. Emit the revision record

Return a checkable record with the artifact:

```yaml
revision-record:
  frame: <path or identifier for the frozen frame>
  pre-edit-validation: <validation record or identifier>
  changed: []           # { unit, criterion, what }
  checked-clean: []     # { unit, criterion, evidence }
  unresolved: []        # { unit, criterion, fault, why-not-fixed }
  out-of-scope: []      # { unit, observation, reason }
  post-edit-validation: <validation record or identifier>
```

`checked-clean` distinguishes examined material from material never inspected.
Every in-scope unit must appear in at least one record list, and every frame
criterion must appear in `changed`, `checked-clean`, or `unresolved`.
Coverage is demonstrated by the records, not by a prose claim that the revision
is complete.
