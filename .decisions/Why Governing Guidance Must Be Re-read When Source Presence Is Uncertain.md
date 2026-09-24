---
uid: QWJ9VN
description: >-
  `Read in full when` *the reason governing guidance must be reread after its
  complete source ceases to be identifiable in active non-compacted
  conversation history needs to be reviewed* `to` **understand the evidence
  chain from context-presence research to the repository-wide
  source-availability rule without treating this decision record as current
  authority**.
quadrant: Explanation
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

**Status:** Accepted  
**Date:** 2026-09-23  
**Authority:** Decision provenance only. The current binding rule belongs in
the repository Origin and its Document Form.

The originating investigation is
[Verifying That a Governing Document Is Actually Present in an LLM Agent’s Effective Context](../.research/Governing%20Document%20Context%20Presence/2026-09-23%20Research%20Report.md).

## 1. Presence and familiarity are different

The research began with a strict question: can an agent determine that a
governing document is actually present in its effective context rather than
merely appearing familiar with it?

The research rejects semantic familiarity as proof. Correct answers,
quotations, reconstructed headings, confidence, remembered prior reading, and
similar model-side behavior can arise from pretrained knowledge, prior
conversation state, summaries, near-duplicate material, or inference. None of
those observations establishes that the authoritative source text itself is
present.

The same research found no documented general-purpose model-facing primitive
that exposes an exact inventory of authoritative sources in the current
effective context. Proposed manifests, source receipts, context epochs, and
similar structures describe what a stronger harness could expose; they do not
establish a capability already available in the environments considered here.

## 2. Active history supplies a narrower observable

The practical question was narrowed to the existing environments used for this
repository: ChatGPT Web and Codex in Visual Studio Code. The relevant operating
case was narrowed further to the period before a known compaction event,
because users can ordinarily recognize compaction as a context-management
boundary and can respond to it explicitly.

Before that boundary, the agent receives conversation and tool history from the
surrounding harness. A document read that injected literal source text into
that active history is therefore different from a model merely remembering the
document semantically.

This permits a narrower test:

> Is the complete source text of the governing document identifiable in the
> active, non-compacted conversation or tool history?

That test does not ask the model to infer whether it remembers reading the
document. It asks the agent to inspect the history supplied to it and identify
the literal source material on which reliance would be based.

The history may also be externalized to a deterministic tool for searching,
counting, or structural inspection. Such a tool does not gain independent
access to the conversation automatically; the agent must serialize the history
it sees. The useful property is that the source being serialized is
harness-supplied active history rather than reconstructed semantic memory.

## 3. Compaction ends that source-level assurance

Compacted history is not equivalent to literal retained source text. A
compaction mechanism can preserve task-relevant information while replacing or
transforming earlier source material. The agent may continue to know what a
document says without being able to establish that the complete authoritative
text remains available.

A surviving literal source item can still be relied on after some other
history has been compacted when the complete document remains identifiable as
an active item. What cannot be relied on is the possibility that the document
may have survived only inside an opaque or lossy compacted representation.

The distinction is therefore not simply before versus after compaction. It is
literal complete source text identifiable in active history versus source
presence that is absent, partial, or only possibly represented through
compacted history.

## 4. The repository-wide reliance rule

Every guidance document in this repository is subject to one reliance rule:

> Before relying on a governing document, confirm that its complete source text
> is identifiable in the active, non-compacted conversation history. If it is
> not, or if its prior presence is only within compacted history, read the
> document in full before relying on it.

The rule intentionally prefers a false reread over false reliance on
authoritative material that may no longer be present in full.

It does not require rereading a governing document on every turn. As long as
the complete source remains identifiable in active history, the prior read can
continue to satisfy the full-read requirement. This preserves token efficiency
without using model familiarity as a substitute for source presence.

Partial excerpts do not satisfy a full-read obligation. A filename, URL,
citation, discussion of the document, statement that it was previously read,
or remembered content likewise does not establish complete source presence.

## 5. Rejected substitutes

Several candidate shortcuts were considered and rejected as the repository
rule.

**Model self-report.** Asking whether the model remembers or has a document in
context is circular and cannot distinguish source presence from semantic
knowledge.

**Substantive quizzes or quotations.** Correct answers can be produced from
prior knowledge, reconstruction, summaries, or stale versions. They test
functional knowledge rather than authoritative source presence.

**Blind rereading on every use.** This is reliable but unnecessarily consumes
context and can itself accelerate context pressure. Active literal source
presence provides a reuse condition before compaction.

**Turns since read.** Turn distance can be measured from active history and may
be useful diagnostically, but no particular turn count proves that the
complete source is present or absent.

**Hypothetical harness receipts.** A source UID, version, attached ranges,
invocation identifier, or context epoch would be useful if an existing harness
reliably exposed and populated them. They are not a present answer when the
environment does not expose those facts.

**Compacted-history familiarity.** Continuing to know the document after
compaction is not evidence that its complete authoritative source survived
unchanged.

## 6. Authority and provenance remain separate

This ADR records why the rule was adopted. It is not the repository location
from which an agent should learn the rule during ordinary work.

Repository Information Storage distinguishes current authority from decision
provenance. A binding constraint belongs in the controlled information whose
readers need it to act correctly, while a retained decision record can preserve
the original problem, reasoning, alternatives, and tradeoffs.

The rule therefore belongs in the reader-facing entry contract of the
repository Origin and in the Origin Document Form that governs derived
origins. That placement makes the requirement universal over subsequent
guidance routing without requiring every guidance document to repeat it.

The root `.decisions` directory retains this reasoning as explicitly
retrieved historical evidence. Because it is an unreserved dot-prefixed
directory, it remains outside the controlled corpus under the current folder
conventions and does not become a competing source of current authority.
