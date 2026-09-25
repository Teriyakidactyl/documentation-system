---
uid: QWJ9VN
form:
  path: '<a href="../e.%20Technical%20Writing/a.%20Document/b.%20Document%20Forms/a.%20Architecture%20Decision%20Record/README.md" uid="A1FANY">documentation-system:§e.a.b.a</a>'
  version: '1.0'
description: >-
  `Read in full when` *the reason governing guidance must be reread after its
  complete source ceases to be identifiable in active non-compacted
  conversation history needs to be reviewed* `to` **understand the evidence
  chain from context-presence research to the repository-wide
  source-availability rule without treating this decision record as current
  authority**.
quadrant: Explanation
decision:
  status: accepted
  decided-at: '2026-09-23T13:46:19-07:00'
  repository-revision: 4548e9901a6160b0b4a6e80ad5a87e8ce441baea
  supersedes: []
  superseded-by:
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
---

# 💡 Why Governing Guidance Must Be Re-read When Source Presence Is Uncertain

## Context

The originating investigation is
[Verifying That a Governing Document Is Actually Present in an LLM Agent’s Effective Context](../.research/Governing%20Document%20Context%20Presence/2026-09-23%20Research%20Report.md).

The investigation asked whether an agent can establish that a governing
document is actually present in its effective context rather than merely
appearing familiar with it. Correct answers, quotations, reconstructed
headings, confidence, remembered prior reading, and similar model behavior can
arise from pretrained knowledge, prior conversation state, summaries,
near-duplicate material, or inference. Those observations therefore do not
establish that the authoritative source text itself is present.

The practical operating case was narrowed to active conversation and tool
history supplied by the harness. Before a known compaction boundary, a full
document read that injected literal source text into that active history is an
observable source event rather than an inference from model familiarity.

## Decision

Use this repository-wide reliance rule:

> Before relying on a governing document, confirm that its complete source text
> is identifiable in the active, non-compacted conversation history. If it is
> not, or if its prior presence is only within compacted history, read the
> document in full before relying on it.

The rule does not require rereading a governing document on every turn. A prior
read continues to satisfy the requirement while the complete source remains
identifiable in active, non-compacted history.

Partial excerpts, filenames, URLs, citations, discussion of the document,
statements that it was previously read, and remembered content do not satisfy a
full-read obligation.

## Rationale

### Active history supplies a narrower observable

The decision does not ask a model to introspect whether it remembers reading a
document. It asks the agent to identify literal complete source material in the
history supplied to it. That history can also be serialized to deterministic
tools for searching, counting, or structural inspection without changing the
fact being tested.

### Compaction ends source-level assurance

Compacted history is not equivalent to retained literal source text. A
compaction mechanism can preserve task-relevant information while replacing or
transforming earlier source material. The agent may continue to know what a
document says without being able to establish that the complete authoritative
text remains available.

A surviving literal source item can still satisfy the rule after unrelated
history is compacted. What cannot satisfy it is the possibility that the source
survived only inside an opaque or lossy compacted representation.

### False rereads are cheaper than false reliance

The rule intentionally prefers an unnecessary reread over reliance on
authoritative material that may no longer be present in full. Reuse remains
allowed while complete literal source presence is observable, which avoids the
larger cost of blindly rereading on every use.

## Alternatives and consequences

**Model self-report.** Asking whether the model remembers or has a document in
context is circular and cannot distinguish source presence from semantic
knowledge.

**Substantive quizzes or quotations.** Correct answers can be produced from
prior knowledge, reconstruction, summaries, or stale versions. They test
functional knowledge rather than authoritative source presence.

**Blind rereading on every use.** This is reliable but unnecessarily consumes
context. Active literal source presence provides a reuse condition.

**Turns since read.** Turn distance can be measured but no particular count
proves that complete source is present or absent.

**Hypothetical harness receipts.** Source UIDs, versions, attached ranges, or
context epochs would provide stronger evidence if a harness reliably exposed
them. They are not a present substitute where the environment does not expose
those facts.

The ADR preserves why the rule was adopted; it is not the authority from which
ordinary work should learn the rule. The current binding requirement belongs in
the repository entry contract and the Document Control guidance that owns
reliance on governed information.
