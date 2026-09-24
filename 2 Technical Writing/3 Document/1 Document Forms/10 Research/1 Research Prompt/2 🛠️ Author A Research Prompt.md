---
uid: EPQFDF
description: >-
  `Read in full and follow when` *a repeatable research request must be
  authored before its first or next execution* `to` **compose, freeze, and
  control one Research Prompt whose later reports can identify the same request
  without inheriting run-specific assumptions**.
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

# 🛠️ Author A Research Prompt

## 1. Fix the investigation boundary

State the objective, questions, scope, comparison criteria, tests, evidence
requirements, and requested output. Separate what every run must investigate
from assumptions that belong only to one execution environment.

## 2. Compose the rerunnable payload

Write the complete executable request as one `text` fenced block. Make the
request self-sufficient for a later run; do not rely on conversation context
that will not be preserved with the prompt.

## 3. Create the controlled wrapper

Create `Prompt.md` in the investigation folder. Give it a routing
`description` and bind `form` to the Research Prompt Form package UID
`BSJY2D`. Let Organizing mint the prompt UID when one is not already present.

Keep explanatory wrapper prose outside the fenced payload.

## 4. Freeze the prompt before execution

Once a run begins, preserve the payload that was actually executed. Do not
rewrite that payload while normalizing the wrapper, because doing so would make
a historical report appear to derive from instructions that were never run.

When the research objective, scope, evidence requirement, evaluation method, or
required output materially changes, create a new prompt identity.

## 5. Produce reports separately

For each execution, follow the Research Report Form. Keep model, version,
execution time, findings, and sources in the report rather than adding them to
the prompt.
