---
description: >-
  `Read in full and follow when` *an existing artifact must incorporate a
  stated change without leaving superseded meaning, broken dependencies, or
  unexamined residual* `to` **apply the change against a frozen frame,
  propagate its implications, verify the result, and return a checkable revision
  record**.
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
of completion as the authority for what remains to be done.

**Terms.**

| Term | Meaning |
|---|---|
| **frame** | The frozen, numbered criteria the revised artifact must satisfy. |
| **unit** | One bounded portion of the artifact that can be inspected and changed without treating the whole artifact as one edit. |
| **residual** | Required work not completed by the revision, named explicitly rather than absorbed into a completion claim. |
| **superseded representation** | A representation of a state, rule, term, relationship, or implementation that the accepted change has made non-current. |
| **edit-induced fault** | A defect introduced by the revision that was not present before mutation. |

## 1. Freeze the change frame

State the accepted change before searching for edit sites. Derive numbered,
checkable criteria that say what must become true, what must stop being true,
and which dependent representations must change as a consequence.

Take the frame from an authority outside the revision itself: an explicit user
decision, accepted design, governing specification, norm, or other confirmed
source. Do not derive the frame from whichever passages first attract attention.

Freeze the criteria before the first mutation. If the frame proves wrong or
incomplete, stop, replace it explicitly, and restart coverage against the new
frame. Do not amend criteria merely to make completed edits appear sufficient.

## 2. Map the implications

Inspect the artifact against each criterion before changing it. Search is a
discovery aid, not a completeness test: a representation can embody the old
model without repeating the words that named it.

For each criterion, ask:

- What must now be true?
- What must no longer be true?
- Which definitions, references, examples, structures, names, behaviors, or
  explanations depend on either state?
- Which units would read or behave differently if the new criterion had been
  true when the artifact was first produced?

Build the edit set from those implications.

## 3. Remove superseded representations

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

## 4. Apply bounded changes

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

## 5. Verify the result

Assess the revised artifact against the frozen frame rather than against the
reasoning that produced the edits. A revision is not complete because its
planned mutations were applied.

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

Do not silently repair a newly discovered issue whose correct resolution is not
determined by the frame. Record it as residual.

## 6. Emit the revision record

Return a checkable record with the artifact:

```yaml
revision-record:
  frame: <path or identifier for the frozen frame>
  changed: []         # { unit, criterion, what }
  checked-clean: []   # { unit, criterion, evidence }
  unresolved: []      # { unit, criterion, fault, why-not-fixed }
  out-of-scope: []    # { unit, observation, reason }
```

`checked-clean` distinguishes examined material from material never inspected.
Every in-scope unit must appear in at least one record list, and every frame
criterion must appear in `changed`, `checked-clean`, or `unresolved`.
Coverage is demonstrated by the record, not by a prose claim that the revision
is complete.
