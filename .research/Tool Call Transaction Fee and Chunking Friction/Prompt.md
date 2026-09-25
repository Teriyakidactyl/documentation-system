---
uid: G9H9K7
form:
  path: '<a href="../../f.%20Technical%20Writing/a.%20Document/b.%20Document%20Forms/d.%20Research/a.%20Research%20Prompt/README.md" uid="BSJY2D">documentation-system:§f.a.b.d.a</a>'
  version: '1.0'
description: >-
  `Read in full and follow when` *the tool-call transaction-fee and
  chunking-friction investigation is rerun* `to` **measure how much
  model-visible tool-call overhead should influence context chunking strategy
  without confusing fixed transaction cost with payload or reasoning-coherence
  cost**.
---

# Research Prompt: Tool Call Transaction Fee and Chunking Friction

> [!WARNING]
> **Post-documentation reconstruction.** This reusable prompt was composed
> after the interactive discussion that produced the sibling research report.
> It reconstructs the thrust of that discussion and was not frozen before the
> original reasoning occurred.

The fenced block below is the rerunnable research payload. Repository
frontmatter, the title, and the provenance warning are not part of the prompt.

````text
Investigate the token/context cost of model-visible tool calls as a fixed
transaction fee that should be considered when choosing chunk sizes for an
amnesiac agent.

Separate at least these quantities:

- fixed tool-definition cost already present before a call;
- per-call request and argument representation;
- per-call result-envelope and framing overhead;
- substantive returned payload;
- any harness-internal retrieval that does not cross into model context;
- navigation and reasoning-state reconstruction costs that are not captured by
  raw token counts.

Determine whether a provisional engineering estimate such as approximately
100 tokens per model-visible tool transaction is useful as a chunking-friction
constant, while clearly distinguishing an estimate from an actual meter
reading.

Develop a measurement methodology that could replace the estimate with
empirical values in a harness exposing input-token usage. The method should
compare a baseline invocation with otherwise equivalent invocations containing
minimal tool calls and minimal tool results, subtract substantive payload, and
repeat enough times to estimate mean, median, and tail transaction cost for
representative tool classes.

Evaluate how the fixed fee changes relative overhead at different chunk sizes.
For example, compare a fixed fee against useful payloads on the order of
hundreds, thousands, and several thousands of tokens.

The output should answer:

1. Is per-call token overhead a real but minor chunking cost?
2. At what chunk sizes does it become materially significant?
3. Should chunk boundaries ever violate reasoning or semantic coherence merely
   to save transaction overhead?
4. How should fixed token friction be weighed against navigation,
   reconstruction, omission, truncation, and dependency-loading costs?
5. How does orchestration that performs multiple internal retrievals but emits
   one compact model-visible result change the calculation?
6. What provisional constant is reasonable before empirical instrumentation is
   available, and how should it be labeled?

Conclude with a compact engineering rule suitable for later incorporation into
agent-facing context-loading or chunking guidance, without prematurely
promoting the research result to current authority.
````
