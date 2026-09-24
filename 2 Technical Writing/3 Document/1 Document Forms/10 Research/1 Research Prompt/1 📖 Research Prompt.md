---
description: >-
  `Consult when` *a Research Prompt instance is being authored or reviewed
  for conformance* `to` **confirm its payload boundary, identity rule, folder
  relationship, and separation from run-specific provenance**.
quadrant: Reference
outline:
  topology: list
  axis: research prompt facet
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

# 📖 Research Prompt

A Research Prompt is the reusable input specification for one investigation.
It preserves what should be investigated independently of any particular
execution environment or result.

## 1. Investigation folder

One investigation owns one `Prompt.md`. Repeated runs reuse that prompt and
produce separate Research Reports beside it:

```text
<Investigation>/
├── Prompt.md
├── <run> Research Report.md
└── <later run> Research Report.md
```

## 2. Prompt frontmatter

A prompt carries its controlled `uid`, routing `description`, and `form`
link to the Research Prompt Form package `README.md`.

Execution-specific model, version, time, findings, and encountered sources do
not belong to the prompt.

## 3. Prompt payload

The rerunnable request is exactly one fenced `text` block beneath the H1.
The payload owns the objective, questions, scope, comparison criteria, tests,
required evidence, and requested output.

Frontmatter, title, and surrounding maintenance prose are not part of the
executable payload.

## 4. Prompt identity

The prompt UID identifies one conceptual research request across repeated runs.
A materially different objective, scope, required evidence, evaluation method,
or deliverable is a new prompt rather than an in-place revision.

Purely representational wrapper changes can retain the UID. Git history supplies
an exact prior representation when reproduction requires more than conceptual
identity.

## 5. Run separation

Each retained Research Report identifies the prompt by UID and carries its own
execution provenance. A report never turns run-specific metadata into prompt
state.
