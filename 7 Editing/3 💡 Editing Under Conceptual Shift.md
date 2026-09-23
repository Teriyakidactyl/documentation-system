---
uid: JD245Q
description: >-
  `Read in full when` *editing is being treated as ordinary rewriting or an
  editor's internal sense of completion is being accepted as evidence that a
  conceptual change has fully propagated* `to` **understand why revision needs
  an external frame, validation reasoning distinct from mutation, and explicit
  residual accounting when existing representations can preserve superseded
  meaning**.
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
reasoning that remains logically distinct from the mutation it evaluates.

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

## 3. Revision and validation reasoning have different authority

Revision is authorized to change an artifact. Validation reasoning determines
whether a representation satisfies a governing criterion.

The two can be interleaved without becoming the same operation:

```text
external frame
     ↓
inspect representation
     ↓ validation reasoning
revise representation
     ↓ validation reasoning
continue until criteria and residual are accounted for
```

A correction can follow immediately from a validation judgment when the frozen
frame determines the repair and Revision already authorizes the mutation. The
judgment still does not become evidence merely because the same context made
the correction; check the resulting representation against the criterion rather
than treating the edit history as proof.

A bounded Validation pass is a stronger, separately accountable assurance
operation. Invoke it only when a governing process explicitly requires that
assurance; ordinary Revision does not need a formal pre-edit and post-edit pass
merely to separate assessment reasoning from mutation.

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

## 7. Established terms carry useful prior structure

Editing already has mature names for recurring scopes of work: developmental
editing, line editing, copyediting, proofreading, house style, and style sheet.
For agent-facing guidance, keep those names when they fit instead of replacing
them with locally coined synonyms.

An established term gives the agent a larger learned body of examples,
techniques, boundaries, and failure modes to retrieve from. The local procedure
then constrains that prior knowledge where Documentation System needs a sharper
rule.

Local terms are justified when they name a distinction the established
editorial vocabulary does not provide. `checked-clean`, `residual`,
`edit-induced fault`, and `superseded representation` exist for that reason.

This is also why Revision and validation reasoning do not replace developmental
editing, copyediting, or proofreading. Revision answers mutation authority;
validation reasoning answers assessment against criteria; a bounded Validation
pass adds independently accountable assurance only when selected. The editorial
term answers what level and class of prose work is in scope.
