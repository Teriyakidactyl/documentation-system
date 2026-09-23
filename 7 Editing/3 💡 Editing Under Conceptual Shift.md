---
uid: JD245Q
description: >-
  `Read in full when` *editing is being treated as ordinary rewriting or an
  editor's internal sense of completion is being accepted as evidence that a
  conceptual change has fully propagated* `to` **understand why revision needs
  an external frame, independent validation, and explicit residual accounting
  when existing representations can preserve superseded meaning**.
quadrant: Explanation
outline:
  topology: graph
  numbering: hierarchical-decimal
writing-style:
  formality: professional
  tone: collegial/earnest
  mode: declarative
  density: moderate
  abstraction: mixed
  redundancy: zero
  signposting: suppressed
  register: accessible
---

# 💡 Editing Under Conceptual Shift

Writing and editing have different starting conditions. Writing establishes a
representation from an intended specification. Editing begins with a
representation that already exists and must reconcile it with something that
has changed or with a standard it may already violate.

That difference makes editing depend on an external frame and on validation
that is independent of the mutation itself.

## 1. Existing representations carry precedent

An existing artifact is not neutral input. Its terminology, examples,
structure, code paths, references, and explanations all provide evidence about
what the system means and how it is supposed to work.

A conceptual change can therefore be stated correctly in one location while
the artifact as a whole continues to teach the prior model. Lexical replacement
does not reach passages or behaviors that depend on the old concept without
naming it.

For agent-facing information this residual is especially costly. A future
agent can consume the surviving representation as current evidence and use it
to reconstruct a policy that was intended to be gone.

## 2. Completion needs an external frame

The editor's sense that a revision looks complete is not evidence that all
implications were examined. The edit plan has the same limitation when it was
derived from the artifact under revision: it records what the editor noticed,
not necessarily the complete set of consequences.

A frozen frame changes the completion question from:

```text
Does this look finished?
```

to:

```text
For every accepted criterion and every in-scope unit, what evidence shows the
criterion was satisfied, found already clean, left unresolved, or excluded?
```

The second question can be inspected by another reader.

## 3. Revision and validation have different authority

Revision is authorized to change an artifact. Validation is authorized to make
claims about an artifact.

Combining the two without an explicit boundary lets the reasoning that selected
a repair also decide that the repair was sufficient. Keeping them distinct
allows validation to test the result against the same external frame without
treating the edit history as proof.

The normal relationship is:

```text
external frame
     │
     ├──> validate current state
     │
     └──> revise artifact
               │
               └──> validate resulting state
```

Validation may precede revision to locate faults and follows revision to detect
remaining or edit-induced faults. The responsibility is the same in both
positions: assessment without mutation.

## 4. Residual error becomes future evidence

A missed conceptual dependency does not remain merely an isolated defect when
the artifact is used as a source of truth. Later work can depend on it. The
residual then acquires apparent precedent because subsequent readers encounter
both the corrected rule and evidence of the prior one.

This is why revision must account for checked-clean and unresolved scope rather
than ending with a general declaration of completeness. A bounded residual that
is named can be reviewed. An unexamined residual hidden behind a completion
claim cannot.

## 5. Superseded representations require removal by default

Remove superseded representations unless the superseded state itself is
required information for the artifact's job.

The default is strongest in operational and lookup artifacts, where the reader
needs current truth and a historical implementation competes with it. Keeping
old material merely because it once existed increases the number of plausible
models a future reader can infer.

The exception follows the artifact's job, not nostalgia for history. An
Explanation about repository history may require the old state because the
transition is its subject. A code comment may retain a rejected pattern when
the failed approach records a concrete, non-obvious recurrence constraint.
Such material remains useful only when its non-current role is unmistakable.

## 6. Editing is not limited to prose

Conceptual meaning can be represented in prose, structured data, code, schema,
configuration, naming, or relationships among them. A single accepted change
can require revision across several of these surfaces.

Technical Writing owns how technical documents are conceived and authored.
Editing owns reconciliation of an existing artifact with an external frame.
The two cooperate when a revision changes a document's specification, but
neither responsibility collapses into the other.
