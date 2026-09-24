---
uid: DAZ7FV
description: >-
  `Read in full and follow when` *one completed research execution must be
  retained* `to` **bind the output to the prompt and actual execution
  provenance while preserving the run as historical evidence**.
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

# 🛠️ Retain A Research Report

## 1. Identify the executed prompt

Use the UID of the exact `Prompt.md` whose payload was executed. Do not bind
the report to a later materially changed prompt merely because it occupies the
same investigation folder.

## 2. Capture execution provenance

Record `executed-at`, the model label, and model version actually exposed for
the run. Add another field only when it changes how the result can be
reproduced or compared.

## 3. Preserve the substantive output

Place the run output in the report body without silently rewriting its
findings, evidence, citations, uncertainty, or recommendations. Wrapper
normalization is allowed; changing the research result requires an explicitly
revised report or another run.

## 4. Bind the Form and prompt

Set `form` to the Research Report Form package UID `AKNN1G` and
`research-prompt` to the executed prompt UID. Give the report a routing
`description` that distinguishes this retained run from current authority.

## 5. Retain repeated runs separately

Name and store each run as a sibling report. Never overwrite an earlier run.
When a conclusion becomes current guidance, author it into the controlled
artifact that owns the subject and leave the report as provenance.
