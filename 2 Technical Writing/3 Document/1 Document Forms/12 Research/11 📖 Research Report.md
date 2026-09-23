---
uid: AKNN1G
description: >-
  `Consult when` *the output of a research run is being retained for later
  review, comparison, or promotion into current authority* `to` **bind the
  output to its Research Prompt, record the actual model and version used, and
  preserve the run as historical research evidence without rewriting its
  substantive findings**.
quadrant: Reference
outline:
  topology: list
  axis: research report element
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

# 📖 Research Report

A Research Report is the retained output of one execution of a Research Prompt.
It is historical research evidence, not current governing authority merely
because it is retained.

## 1. Research report role

Each run produces a separate report. A later run never overwrites an earlier
report, even when both execute the same prompt.

Reports from one prompt remain comparable because every report carries the same
`research-prompt` UID while recording its own execution provenance.

## 2. Report frontmatter

A derived report carries ordinary frontmatter with this minimum structure:

```yaml
uid: <compiler-minted>
form: '<controlled link to this Research Report form>'
description: >-
  <routing statement for this retained run>
research-prompt: <uid of the investigation Prompt.md>
research-run:
  executed-at: <date or timestamp>
  model: <agent model actually used>
  version: <model version actually used>
```

`research-prompt` identifies the reusable prompt artifact directly by UID.
The report normally sits beside that prompt for human navigation; the UID,
rather than the relative path, supplies durable relationship identity.

## 3. Run provenance

`research-run.model` and `research-run.version` record the execution
environment actually used, using the labels available from the research
environment or supplied by the user. Do not infer a more precise model build
than the environment exposes.

`research-run.executed-at` records when the run occurred so time-sensitive
sources and platform capabilities can be interpreted against the appropriate
period.

Additional run metadata belongs here only when it materially affects
reproducibility or comparison. Do not turn the report envelope into a general
execution log.

## 4. Report body

The body preserves the substantive research output. Normalization can add the
form envelope, provenance, stable relationships, and repository placement, but
does not silently rewrite findings, evidence, citations, uncertainty, or
recommendations produced by the run.

If a later review discovers an error, correct the current authority that
depends on it and retain the historical report as evidence of what that run
produced. A revised research result is another run or an explicitly revised
report, not an unmarked replacement.

## 5. Repeated runs

Repeated execution of the same Research Prompt produces sibling reports:

```text
Prompt.md
2026-09-23 Research Report.md
2027-02-14 Research Report.md
```

A materially changed prompt receives a new prompt identity. Reports should not
be grouped as repeated executions of one prompt when the research question,
scope, evidence requirement, evaluation method, or required output materially
changed.

## 6. Promotion to authority

Research remains supporting information until a conclusion is adopted by the
controlled artifact that owns the subject.

Promotion copies or reauthors the required current conclusion into that
authority. The report remains research evidence for why the conclusion was
considered; readers should not need to reconstruct current policy from the
research history.
