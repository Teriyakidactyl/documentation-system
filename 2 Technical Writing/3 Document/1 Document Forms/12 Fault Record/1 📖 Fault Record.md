---
description: >-
  `Consult when` *a Fault Record instance is being authored or reviewed for
  conformance* `to` **confirm its standards lineage, chronological filename,
  structured provenance, required evidence and causal sections, recurrence
  controls, and authority boundary**.
quadrant: Reference
outline:
  topology: list
  axis: fault record facet
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

# 📖 Fault Record

A Fault Record preserves an observed failure, the evidence that establishes it,
and the causal analysis needed to understand recurrence. It is evidence and
provenance, not current authority merely because it records a corrective action.

## 1. Standards lineage

The Fault Record is informed by
[ISO/IEC/IEEE 23612-2026, *Software and systems engineering — Incident management*](https://standards.ieee.org/ieee/23612/11441/).

The Form uses that standard as a recognized incident-management vocabulary and
conceptual reference. It does not claim conformance to ISO/IEC/IEEE 23612-2026
unless a separate conformance assessment establishes that claim. Where the
Documentation System specializes a standard term, state the specialization
explicitly rather than silently redefining the standard term.

## 2. Filename

Use:

```text
YYYY-MM-DDTHHmm <Fault title>.md
```

Use the local time recorded in `fault.recorded-at`. The timestamp prefix keeps
the sideband chronological. The remainder of the filename matches the H1 title
after its quadrant glyph. Name the observable failure or established failure
mechanism rather than a person, conversation, or vague symptom.

## 3. Frontmatter

Every Fault Record carries:

```yaml
uid: <Organizing-minted>
form:
  path: '<controlled link to the Fault Record Form package>'
  version: '<major.minor contract used by this record>'
description: >-
  <routing statement for reviewing this retained fault evidence>
quadrant: Explanation
fault:
  recorded-at: <ISO 8601 timestamp with explicit offset>
  repository-revision: <40-character Git commit SHA when repository state is material, otherwise null>
outline:
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
```

Keep the structured envelope limited to facts with stable machine-readable
semantics across Fault Records. Put observations, evidence, causal reasoning,
uncertainty, and explanatory relationships in the Markdown body.

`repository-revision` identifies the repository state materially involved in
the failure. Git history separately identifies the later commit that retained
the record.

## 4. Required sections

Use these H2 sections in order:

```markdown
## Expectation
## Occurrence
## Evidence
## Causal analysis
## Response and recovery
## Recurrence control
## Authority propagation
```

`Expectation` states the governing requirement or expected state.

`Occurrence` states the context, trigger, observable failure, and material
impact. Add a timeline only when sequence is load-bearing.

`Evidence` preserves the observations that establish the failure and constrain
the causal analysis. Distinguish direct tool or repository observations from
later interpretation.

`Causal analysis` explains the failure mechanism, contributing conditions,
failed or absent controls, and material uncertainty or competing explanations.

`Response and recovery` records detection, containment or mitigation, immediate
correction, and recovery of the failed condition.

`Recurrence control` records corrective actions, the preventive mechanism each
action is expected to introduce, and the evidence required to verify
effectiveness.

`Authority propagation` identifies any current controlled information changed
because of the fault. It does not duplicate the resulting current rule merely
to make the historical record self-contained.

## 5. Causal discipline

Keep these distinctions stable:

- A **trigger** initiates or exposes the failure.
- A **failure** is the observable divergence from the governing expectation.
- A **failure mechanism** explains how the system or process produced that
  divergence.
- A **contributing condition** enables, amplifies, or fails to prevent the
  mechanism.
- A **correction** repairs the immediate failed state.
- A **corrective action** changes a condition intended to prevent recurrence.
- **Effectiveness verification** supplies evidence that the corrective action
  actually changed the recurrence condition.

Do not infer causality merely from temporal sequence. Do not require a singular
root cause. Retain multiple interacting causes, contributing conditions, or
unresolved uncertainty when the evidence supports them.

## 6. Authority boundary

A Fault Record can identify the controlled artifact that absorbed a lesson, but
the record remains evidence and provenance. Put a new rule, procedure, tooling
behavior, or other current truth in the controlled artifact that owns that
subject.

A fault record may therefore remain unchanged after later corrective work has
matured. Update the current authority rather than rewriting historical evidence
to resemble the present state.

## 7. Completion condition

A Fault Record is complete when another reader can reconstruct what was
expected, what happened, what evidence establishes the divergence, what causal
mechanism and contributing conditions are established or remain uncertain, how
the immediate condition was recovered, what recurrence controls follow, how
their effectiveness can be verified, and where resulting current authority
lives.

Repairing the immediate failure alone does not complete the record.
