---
description: >-
  `Consult when` *a repeatable research request needs a durable source
  representation* `to` **preserve one exact rerunnable prompt under stable
  identity while keeping execution-specific model, version, date, and output
  information in the resulting Research Report**.
quadrant: Reference
outline:
  topology: list
  axis: research prompt element
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

A Research Prompt is the reusable input specification for one research
investigation. It preserves what should be investigated independently of any
particular execution environment or result.

## 1. Research prompt role

One investigation owns one `Prompt.md`. Repeated research runs reuse that
prompt and produce separate Research Reports.

The prompt owns the requested objective, questions, scope, comparison criteria,
tests, required evidence, and requested output. It does not own the model,
model version, execution date, findings, or sources actually encountered by a
particular run.

## 2. Investigation folder

A repeatable investigation is stored as one folder:

```text
<Investigation>/
├── Prompt.md
├── <run> Research Report.md
└── <later run> Research Report.md
```

The folder name identifies the investigation for human navigation. `Prompt.md`
provides the stable controlled identity used by reports.

## 3. Prompt artifact

A derived prompt carries ordinary frontmatter containing its `description`,
compiler-minted `uid`, and `form` link to this Research Prompt form.

The rerunnable prompt is preserved as one fenced `text` block beneath the
document title. Text inside that block is the executable research request.
Frontmatter, title, and surrounding maintenance prose are not part of the
payload.

<!--
Keep the payload verbatim when normalizing an already-executed research
request. Formatting or rewriting the payload would create a different prompt
state and could make the historical report appear to derive from instructions
that were never actually run.

For a newly authored prompt, use Technical Writing while composing the request,
then freeze the payload before the first run.
-->

## 4. Prompt identity

The prompt UID identifies the conceptual research request across repeated runs.
A materially different objective, scope, required evidence, evaluation method,
or deliverable is a new prompt rather than an in-place revision of the old
research request.

Purely non-semantic wrapper changes can retain the UID. When exact prompt-state
reproduction matters beyond conceptual identity, Git history supplies the
representation state used by the historical run.

## 5. Run-specific metadata

Execution metadata belongs to each Research Report rather than `Prompt.md`.
At minimum, every retained report records the agent model and model version
actually used for that run.

This separation keeps one prompt rerunnable across later models or versions
without rewriting its source specification.
