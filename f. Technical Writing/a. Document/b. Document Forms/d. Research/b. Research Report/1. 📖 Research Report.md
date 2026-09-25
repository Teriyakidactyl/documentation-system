---
uid: 7KXYGE
description: >-
  `Consult when` *a Research Report instance is being authored or reviewed
  for conformance* `to` **confirm its prompt relationship, run provenance,
  body-preservation rule, repeated-run behavior, and authority boundary**.
quadrant: Reference
outline:
  topology: list
  axis: research report facet
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

## 1. Report frontmatter

A report carries this minimum run envelope:

```yaml
uid: <Organizing-minted>
form:
  path: '<controlled link to the Research Report Form package>'
  version: '<major.minor contract used by this report>'
description: >-
  <routing statement for this retained run>
research-prompt: <uid of the investigation Prompt.md>
research-run:
  executed-at: <date or timestamp>
  model: <agent model actually used>
  version: <model version actually used>
```

`research-prompt` identifies the reusable prompt by UID. The report normally
sits beside that prompt for human navigation.

## 2. Run provenance

Record the execution environment labels actually exposed by the research
environment or supplied by the user. Do not infer a more precise build than the
environment exposes.

Add further run metadata only when it materially affects reproducibility or
comparison.

## 3. Report body

Preserve the substantive output. Normalization may add the Form envelope,
provenance, stable relationships, and repository placement, but it does not
silently rewrite findings, evidence, citations, uncertainty, or recommendations
produced by the run.

## 4. Repeated runs

Each execution receives a separate report. A later run never overwrites an
earlier report, even when both execute the same prompt.

A materially changed prompt receives a new prompt identity; reports from
different prompt identities are not repeated runs of one request.

## 5. Promotion to authority

Research remains supporting information until a controlled artifact that owns
the subject adopts the required current conclusion. Promotion changes the
authority, not the historical report.
