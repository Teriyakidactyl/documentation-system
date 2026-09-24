---
uid: 68PAX9
description: >-
  `Consult when` *an Architecture Decision Record is being authored or
  reviewed for conformance* `to` **confirm its chronological filename,
  repository-state provenance, status relationships, and required explanatory
  sections**.
quadrant: Reference
outline:
  topology: list
  axis: ADR facet
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

# 📖 Architecture Decision Record

An Architecture Decision Record preserves why an architectural choice was made
at a particular repository state. It is decision provenance, not the current
source of binding implementation or documentation rules.

## 1. Filename

Use:

```text
YYYY-MM-DDTHHmm <Decision title>.md
```

The local timestamp prefix makes directory ordering chronological without a
separate ADR ordinal. Use the time the decision entered its recorded status.

## 2. Frontmatter

Every ADR carries:

```yaml
uid: <Organizing-minted>
form: '<controlled link to the ADR Form package>'
description: >-
  <routing statement for reviewing this decision provenance>
quadrant: Explanation
decision:
  status: proposed | accepted | superseded | rejected
  decided-at: <ISO 8601 timestamp with offset>
  repository-revision: <40-character Git commit SHA evaluated by the decision>
  supersedes: []
  superseded-by:
```

`repository-revision` identifies the repository state the reasoning evaluated.
Git history separately identifies the later commit that introduced the ADR.

Use ADR UIDs in `supersedes` and `superseded-by`. Do not encode mutable file
paths as decision relationships.

## 3. Required sections

Use these H2 sections in order:

```markdown
## Context
## Decision
## Rationale
## Alternatives and consequences
```

`Context` states the condition that forced a choice and the constraints that
matter. `Decision` states the selected choice concretely. `Rationale`
preserves the evidence-bearing reasoning. `Alternatives and consequences`
records serious alternatives and the costs or obligations knowingly accepted.

## 4. Authority

An accepted ADR does not become governing guidance by status alone. Put current
rules in the controlled artifact that owns the subject and use the ADR only
when the historical reasoning needs review.

When a later choice replaces an ADR, retain the old record, set its status to
`superseded`, and connect both records by UID.
