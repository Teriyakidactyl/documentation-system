---
description: >-
  `Read in full and follow when` *an architectural choice has reached a state
  worth retaining as explicit decision provenance* `to` **capture the forcing
  context, selected choice, rationale, alternatives, consequences, and exact
  repository state without turning the ADR into current authority**.
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

# 🛠️ Author An Architecture Decision Record

## 1. Establish the decision boundary

Name the architectural choice that actually requires commitment. State the
forcing condition, constraints, and decision criteria. Exclude implementation
history that does not change the choice.

Identify the Git commit representing the repository state being evaluated.

## 2. State the decision

Write the selected choice so a later reader can determine what was committed
without reconstructing it from the rationale. Separate the decision from work
that merely follows from it.

## 3. Preserve the rationale

Explain why the choice satisfies the stated constraints and criteria. Retain
facts, tradeoffs, and evidence that would otherwise disappear into conversation
or implementation history.

## 4. Record alternatives and consequences

Name serious alternatives that could plausibly have been selected and why they
were not. Record costs, risks, dependencies, or future obligations knowingly
accepted by the chosen decision.

## 5. Record provenance

Create the timestamp-prefixed filename from the decision time. Set
`decision.decided-at` with an explicit timezone offset and
`decision.repository-revision` to the full SHA of the evaluated state.

Bind `form` to the ADR Form package `README.md`. Let Organizing mint the
ADR UID if one is not already present.

## 6. Maintain supersession

Never rewrite an old ADR to make it describe a new decision. Create a new ADR,
set the old one to `superseded`, and connect `supersedes` /
`superseded-by` with ADR UIDs.

## 7. Promote current truth separately

If the decision establishes a binding rule, update the controlled artifact that
owns that rule. The ADR remains provenance for why the rule was adopted.
