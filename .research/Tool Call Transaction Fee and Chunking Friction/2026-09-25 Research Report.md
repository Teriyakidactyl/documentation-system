---
uid: RAXX41
form:
  path: '<a href="../../a.%20Document%20Design/a.%20Assemblies/b.%20Forms/d.%20Research/b.%20Research%20Report/README.md" uid="AKNN1G">documentation-system:§a.a.b.d.b</a>'
  version: '1.0'
description: >-
  `Consult when` *the 2026-09-25 discussion of tool-call transaction cost
  and chunking friction is reviewed* `to` **use the retained methodology,
  cost model, uncertainty, and provisional engineering conclusion without
  treating the estimate as measured current authority**.
research-prompt: G9H9K7
research-run:
  executed-at: '2026-09-25'
  model: GPT-5.6 Sol
  version: GPT-5.6 Sol
  prompt-provenance: post-documented-after-interactive-run
---

# Tool-call transaction fee as chunking friction

> [!WARNING]
> **Post-documentation provenance.** This report preserves reasoning developed
> interactively before the sibling `Prompt.md` was formalized. The prompt is
> a reusable reconstruction of the investigation, not the literal pre-frozen
> input that produced this report. The numeric transaction fee below is an
> engineering estimate, not a token-meter measurement from this ChatGPT
> session.

## Research question

The discussion asked whether model-visible tool calls consume context outside
the substantive payload they return and, if so, whether that overhead should
be treated as a fixed friction when deciding how finely to chunk context for an
amnesiac agent.

The question was narrowed to a practical modeling problem:

```text
If each model-visible retrieval has a small fixed context cost,
how much should that cost influence chunk size?
```

The intended use is not API billing analysis. The intended use is information
architecture: decide whether progressive disclosure can become so granular
that repeated retrieval transactions consume enough context to matter.

## Methodology

The reasoning separated fixed, per-call, and payload costs before assigning any
number:

```text
total effective context cost
    =
fixed tool-definition context
    +
sum(model-visible transaction framing)
    +
useful returned payload
    +
irrelevant returned payload
    +
reasoning/navigation reconstruction cost
```

The fixed tool definitions were excluded from the per-transaction fee because
they are available before an individual call and do not recur once per
transaction in the same way as request/result messages.

The candidate per-call fee included:

```text
tool-call representation
+ arguments
+ result envelope
+ tool-message framing
```

and explicitly excluded the substantive result payload whose useful size is the
quantity chunking is trying to manage.

### Check for direct measurement

The harness was inspected for an exposed per-conversation input-token or
context-usage meter that could support a before-and-after measurement. No such
meter was available to the agent in the observed conversation.

Therefore the discussion did not claim an exact measured transaction cost.

### Establish a provisional engineering constant

Representative connector/orchestration calls were considered in terms of the
visible request representation plus small non-payload response metadata.
Because hidden harness framing could not be observed, the result was treated as
a range estimate rather than a count.

A round value of approximately **100 tokens per model-visible tool
transaction** was selected as a provisional engineering constant because it is:

- plausible for small structured call arguments plus framing;
- conservative enough to avoid dismissing repeated calls as free;
- simple enough for architectural reasoning; and
- explicitly replaceable when instrumentation becomes available.

The estimate does not apply to substantive payload and does not assert that
every tool class has the same actual overhead.

### Test the estimate against chunk sizes

Let:

```text
F = fixed model-visible transaction fee
C = useful payload tokens in one chunk
```

Then the simple transaction-friction ratio is:

```text
F / C
```

Using the provisional `F = 100` tokens:

| Useful payload per transaction | Fixed friction | Relative surcharge |
|---:|---:|---:|
| 100 tokens | 100 tokens | 100% |
| 500 tokens | 100 tokens | 20% |
| 1,000 tokens | 100 tokens | 10% |
| 2,000 tokens | 100 tokens | 5% |
| 5,000 tokens | 100 tokens | 2% |
| 10,000 tokens | 100 tokens | 1% |

For a workflow whose useful payload totals `P` tokens across `N`
model-visible retrievals, the simplified fee is:

```text
transaction friction = N × F
relative surcharge   = (N × F) / P
```

This makes the fee mostly irrelevant for large coherent chunks and increasingly
important as chunks become very small.

### Separate token friction from stronger costs

The discussion identified several costs that can dominate the approximate
100-token transaction fee:

- an additional routing decision;
- preserving where the agent is in the workflow;
- reconstructing relationships among separately retrieved fragments;
- omitting a dependency because it was not discovered;
- truncating or losing a required fragment;
- rereading earlier material after context becomes noisy; and
- latency or failure opportunities introduced by extra transactions.

These costs are not captured by a raw token surcharge. Consequently, the
transaction fee should not be used as the sole objective function for
chunking.

### Account for orchestration

The current harness can execute multiple connector operations inside one
orchestration call and emit only a compact derived result to the model.

Conceptually:

```text
model
  ↓
one orchestration request
  ├── retrieve A
  ├── retrieve B
  ├── retrieve C
  ├── filter / aggregate
  └── construct bounded result
  ↓
one model-visible result
```

This demonstrates that:

```text
retrieval count
≠ model-visible transaction count
≠ context-load count
```

Internal retrieval may have compute, latency, or service costs, but it need not
pay the same model-context transaction fee if its raw request/result traffic is
not projected into model context.

## Interpretation

The fixed transaction fee is best understood as **minor chunking friction**.

It gives a real pressure against pathological fragmentation. A system that
retrieves 100 useful tokens at a time while paying roughly 100 tokens of
transaction framing is structurally inefficient even before navigation cost is
considered.

The same fee should have little influence on a coherent 5,000-token reasoning
unit. At the provisional constant, the direct surcharge is about 2%. Splitting
that unit merely to optimize an already-small fixed fee would reverse the
purpose of the model.

This produces a useful asymmetry:

```text
semantic / reasoning coherence
        = primary chunk boundary

fixed transaction friction
        = secondary pressure against unnecessary fragmentation
```

The estimate therefore should not cause independent concepts to be merged or a
natural work boundary to be crossed solely to reduce tool calls.

## Progressive-disclosure implication

Progressive disclosure remains useful because it prevents irrelevant
information from entering context before the required work is known.

The transaction-fee model adds a complementary rule:

```text
progressively disclose while work identity is uncertain
        ↓
once the work unit is resolved
        ↓
avoid fragmenting its normal coherent working set without a reason
```

A sequence of small routing transactions can still be efficient if each
transaction substantially reduces uncertainty. Repeated tiny retrievals after
the work unit is already known have weaker justification because they pay both
transaction friction and context-reconstruction friction.

The target is therefore not minimum tool-call count. The target is minimum
total context cost while preserving the coherent state required to reason
correctly.

## Empirical measurement design

A harness exposing input-token usage could replace the provisional constant
with measurements.

For each representative tool class:

1. establish a baseline invocation;
2. execute an otherwise equivalent invocation containing one minimal tool call
   and a minimal result;
3. record the increase in model input tokens;
4. subtract tokenized substantive payload;
5. repeat across argument lengths and result-envelope shapes;
6. report mean, median, and a tail value such as p95; and
7. repeat for direct connector calls and orchestrated calls separately.

A useful output would resemble:

```text
tool class                mean fee    p50    p95
minimal fetch             ...
bounded file read         ...
search                    ...
directory listing         ...
orchestration boundary    ...
```

The experiment should also distinguish whether prior tool messages remain in
subsequent effective context. A transaction that contributes 100 tokens at the
moment it occurs but is later compacted or omitted has different long-session
economics from one that remains verbatim for every subsequent invocation.

## Conclusion

Use **approximately 100 tokens per model-visible tool transaction** as a
provisional chunking-friction constant until actual harness measurements are
available.

Treat it as a **minor, cumulative cost concerning chunking strategy**, not as a
primary organizing rule.

The working rule is:

```text
Choose chunk boundaries for reasoning coherence first.

Then, among comparably coherent representations,
prefer the one that avoids unnecessary model-visible transactions.
```

At the provisional 100-token fee, transaction overhead becomes conspicuous for
sub-kilobyte/token-scale fragments, noticeable around 1,000-token chunks, minor
around 2,000-5,000-token chunks, and negligible relative to sufficiently large
coherent units.

Do not merge independent reasoning contexts merely to save the transaction
fee. Also do not treat many tiny context fetches as free merely because each
payload is individually small.

The stronger optimization target remains:

```text
minimum context needed for correct work
+
minimal fragmentation of that coherent context
```

The numeric constant should remain explicitly labeled as an estimate until an
instrumented harness replaces it with observed transaction-cost distributions.
