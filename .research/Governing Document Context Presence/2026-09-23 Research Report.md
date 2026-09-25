---
uid: 3PW763
form:
  path: '<a href="../../a.%20Document%20Design/a.%20Document/b.%20Document%20Forms/d.%20Research/b.%20Research%20Report/README.md" uid="AKNN1G">documentation-system:§a.a.b.d.b</a>'
  version: '1.0'
description: >-
  `Consult when` *the initial governing-document context-presence research
  run must be reviewed or compared with a later rerun* `to` **use the
  retained findings, evidence, and recommendations from this specific run
  while keeping them distinct from current governing guidance**.
research-prompt: RMRAE6
research-run:
  executed-at: '2026-09-23'
  model: gpt-5-thinking
  version: GPT-5.6 Sol
---

# Verifying That a Governing Document Is Actually Present in an LLM Agent’s Effective Context

## Executive findings and taxonomy

The central finding is that **an LLM’s apparent familiarity with a document is not reliable evidence that the authoritative document is presently available to it**. A model can reproduce headings, rules, quotations, structure, or interpretations because the material is in its pretrained parameters, appeared earlier in the conversation, survived as a summary after compaction, was contained in a near-duplicate document, or can be semantically reconstructed from surrounding material. Research on model self-evaluation shows that models can have useful estimates of whether they know an answer, but those estimates concern answerability or correctness, not the provenance or residency of the source that supports the answer. Long-context research separately shows that even material actually included in an input can be used unreliably depending on its position and context length. citeturn21view2turn21view0

The most defensible design is therefore:

> **Treat document presence as observable external state maintained by the retrieval/context-management harness, not as a fact that the LLM is expected to infer about itself.**

The stronger primary abstraction is not usually **“the full document is in context.”** It is:

> **“Required authoritative coverage for this decision has been established, at the required version, and is attached to the current effective model invocation.”**

“Full document present” should be a special case of that abstraction, used when the whole document really is required—for example because relevant dependencies cannot be bounded, because precedence or exception clauses can occur anywhere, or because the governing system explicitly requires examination of the complete instrument.

Six independent properties should be tracked rather than collapsed into `document_in_context: true`:

| Property | Question being proved | Typical evidence |
|---|---|---|
| **Identity** | Is this the intended governing document, rather than a similar document? | Stable document UID, canonical authority/origin, resource identifier |
| **Version** | Is this the intended effective state of that document? | Immutable revision ID, effective-state ID, strong ETag, trusted representation digest |
| **Coverage** | Which exact parts were supplied? | Byte/character/page/section ranges, chunk IDs, source handles |
| **Completeness** | Was every part required for this decision supplied? | Range-union check, all required chunk IDs, explicit non-truncation/completion metadata |
| **Availability** | Is that supplied content part of the effective current invocation rather than merely something fetched earlier? | Invocation-scoped attachment receipt or externally maintained active-context manifest |
| **Understanding** | Can the model correctly interpret and apply it? | Task-specific evaluation, cross-checks, citations, reasoning tests—not presence metadata |

This decomposition is important because mechanisms that are excellent at one dimension can prove nothing about another. HTTP itself makes a similar distinction useful for document engineering: a strong validator is meant to change with observable representation changes and be unique across versions of a particular resource, while byte-range metadata separately identifies what portion of a representation was transferred. citeturn16view0turn16view1turn16view2

A useful taxonomy of states is therefore:

| Actual state | What the agent may safely say |
|---|---|
| Authoritative document, exact version, entire representation currently attached | “The complete authoritative document, version X, is attached to this invocation.” |
| Exact authoritative version, only all sections required for the decision attached | “The authoritative coverage required for this decision is attached.” |
| One complete authoritative section attached | “Section S is present”; **not** “the document is present in full.” |
| Noncontiguous ranges attached | “Ranges A, B, C are attached”; no completeness claim beyond them |
| Retrieval explicitly truncated | “Retrieved content is truncated”; must not claim complete coverage |
| Summary/compacted representation only | “A derived summary is available”; source text is not established |
| Document appeared many turns earlier | “The document was previously supplied”; current availability is unproved unless the harness says otherwise |
| Pretrained/model knowledge only | “The model appears familiar with the document”; no source-presence claim |
| Prior version attached | “Version X is attached”; not current if X is superseded |
| Near-identical document attached | Identity unresolved until UID/origin/version is checked |
| Tool fetched entire file, but only excerpts reached the model | “Retriever has the file”; model-side coverage is only the forwarded excerpts |
| All nominal chunks supplied but from mixed versions | Invalid coverage set; reject it |
| Opening and closing passages supplied, middle absent | Partial document; endpoints do not establish completeness |
| Content was formerly present but replaced by compaction/summary | Historical retrieval is true; current verbatim availability is false or unestablished |

The last distinctions are not hypothetical quirks. Current context-management APIs explicitly support transformations that break the implication “it was once retrieved, therefore it is still present.” OpenAI compaction replaces prior context with a smaller opaque compaction representation and describes the returned compacted window as the canonical context for subsequent calls. Anthropic can clear old tool results before a prompt reaches Claude, replacing cleared results with placeholders, and its compaction system replaces old conversation turns with a generated summary. citeturn19view0turn19view1turn18view4turn18view5

**Bottom line:** a model should be allowed to assert “I have the governing document in context” only when external evidence establishes the necessary identity, version, coverage, completeness, and current attachment. Correctly recalling what the document says is evidence of **knowledge**; it is not evidence of **source presence**.

## What an LLM and current APIs can actually establish

### Model-side knowledge is fundamentally different from presence evidence

A model can directly respond to the input made available for a generation, but ordinary language-model output does not carry a trustworthy provenance label saying which portions of that output came from the current prompt rather than model parameters, earlier contextual residue, or inference. Existing research on self-knowledge does not provide such a primitive. Kadavath et al. found that sufficiently capable models could be meaningfully calibrated on questions such as whether they knew an answer, and that their predicted probability of knowing increased when relevant source material was supplied. But the same result illustrates the distinction here: `P(IK)` is about expected answerability, and the authors report calibration problems on new tasks; it was not an experiment in detecting whether an authoritative source was literally resident in a current prompt. citeturn21view2

Accordingly, these observations are **not proof of source presence**:

- reproducing a document title or heading hierarchy;
- quoting its opening or closing paragraph;
- remembering its approximate length;
- answering questions about its provisions;
- saying “I remember reading it”;
- assigning high confidence to “it is in context”;
- reconstructing a missing rule from domain knowledge;
- producing the same answer repeatedly.

All of them are compatible with a world in which the authoritative text is absent.

This is especially dangerous for well-known governing material. A model with strong pretrained familiarity may pass a sophisticated document quiz when no source was supplied at all. Conversely, a model may fail a quiz despite the text actually being present because long-context retrieval and reasoning are imperfect. Liu et al.’s “Lost in the Middle” experiments found that models’ performance could deteriorate substantially when relevant information moved into the middle of a long context, including for models expressly designed for long contexts. Thus **failure to recall is not proof of absence, and success at recall is not proof of presence**. citeturn21view0

Research on intrinsic self-correction reinforces the broader warning about asking the model to certify its own internal condition. Huang et al. found that LLMs attempting reasoning self-correction without external feedback often failed to improve and sometimes became worse. That result is not specifically a document-residency experiment, but it is evidence against treating an internally generated second opinion as an independent verification channel. citeturn21view3

Self-consistency methods such as SelfCheckGPT can detect some hallucinations by comparing independently sampled answers, but their signal is consistency among generations. A highly familiar model can be consistently right about a document that is absent, and consistently wrong about a changed clause in a newer version. Such techniques therefore test epistemic stability, not authoritative-source residency. citeturn15view4

### Current platform observability is mostly outside the model

As of **September 23, 2026**, in the official OpenAI, Anthropic, and Google Gemini API documentation reviewed for this research, I found **no documented model-callable primitive equivalent to**:

```text
is_source_currently_in_my_context(
    source_uid,
    version,
    exact_ranges
) -> authoritative answer
```

Nor did I find a documented model-facing operation exposing an exact inventory of prompt tokens currently represented in attention/KV state. The APIs instead expose context construction, token counts, caching, conversation state, compaction, and context editing to the **application/API layer**. This is an inference from the documented public API capabilities, not a claim about undisclosed model internals. citeturn15view9turn19view2turn19view3turn19view4turn20view0turn18view7

Anthropic explicitly documents that the system prompt, messages—including tool results and documents—and tool definitions count as request context, while its context-editing facility can modify that history server-side *before the prompt reaches Claude*. That is a particularly clear example of why a client transcript and a model's effective current context cannot always be treated as identical. citeturn19view3turn18view4

OpenAI exposes an input-token counting endpoint and prompt-cache usage data. Its prompt-caching documentation says cache reuse depends on a matching rendered prefix and that the cached artifact consists of KV state rather than copies of prompt tokens. It also says compaction can replace earlier conversation context with a shorter representation and thereby alter the reusable prefix. Those are useful harness signals, but a count such as “42,000 input tokens” does not say which document occupies those tokens, and a cache hit does not by itself prove that the cached prefix contains the required version or complete coverage of the target document. citeturn19view2turn15view9

Anthropic similarly reports cached-prefix token counts such as `cache_read_input_tokens`; cached tokens are part of the overall processed input, but the counter itself describes a quantity rather than a document-level provenance map. citeturn19view4 Google’s Gemini API exposes token counting and `total_cached_tokens` for implicit cache hits; again, these are application-visible context accounting signals, not model introspection or document-identity evidence. citeturn18view7turn20view0

A prompt-cache hit **can become strong supporting evidence** when the harness has separately recorded an exact mapping from a particular immutable document representation to an exact cached prefix. For example, if the harness knows that bytes `0..N-1` of version `V`, with digest `H`, occupy a particular exact prefix, an exact prefix-cache match helps establish that the same prefix was reused. But identity, authority, version and coverage come from the harness’s mapping; the generic cache statistic does not provide them. OpenAI states that reuse requires matching the rendered prefix, while Anthropic exposes how many tokens were read from a cached prefix. citeturn15view9turn19view4

### Retrieval is not attachment

A second architectural distinction is essential:

```text
authoritative store
      ↓
retrieval layer obtained bytes
      ↓
selection / ranking / truncation
      ↓
tool result forwarded to model
      ↓
context management / compaction
      ↓
effective model invocation
```

Evidence at one arrow does not automatically establish the state at the next. For example, OpenAI file search supports limiting the number of search results, and its documentation notes that raw search results are not returned in the response by default unless requested. This is an example of a retrieval interface designed to return relevant excerpts rather than to certify complete-file attachment. citeturn19view6turn19view7

The same distinction should be encoded explicitly in any serious governing-document system:

```text
retrieved_from_source = true
```

must be separate from

```text
attached_to_current_invocation = true
```

and both must be separate from

```text
complete_for_required_coverage = true
```

### “Present” is also different from “usable”

Even perfect harness evidence that bytes were included in an invocation does not establish that the model will interpret them correctly. The “Lost in the Middle” result demonstrates that information physically included in a long context can have position-dependent accessibility in downstream behavior. This means **availability in the request** and **functional use/understanding** must remain separate proof dimensions. citeturn21view0

A useful terminology is therefore:

**Attachment availability** means the required source representation is mechanically established as an input to the current effective invocation.

**Functional accessibility** means the model can actually recover the needed rule from that attached material under the task conditions.

**Understanding** means the model applies the rule correctly.

Only the first is principally a context-management problem. The latter two require evaluations.

## Comparison of candidate mechanisms

The following matrix distinguishes what each mechanism can actually establish. Ratings are an architectural assessment derived from the mechanism’s semantics, not published measured false-positive rates for the specific “document present?” task.

**S** = strong/mechanical when stated preconditions hold.  
**C** = conditional or incomplete evidence.  
**W** = weak/probabilistic heuristic.  
**—** = does not establish the property.

| Mechanism | Identity | Version | Coverage | Completeness | Current availability | Understanding | False-positive risk for “document present” | Cost / portability |
|---|---:|---:|---:|---:|---:|---:|---|---|
| **Harness context manifest + invocation-scoped presence receipt** | S | S | S | S | S | — | Very low if harness state is truthful | Low runtime cost; moderate implementation; provider-portable |
| **All expected chunk IDs from one immutable version + current attachment receipt** | S | S | S | S | S | — | Very low | Low token cost; good portability |
| **Strong resource validator + exact range union + invocation receipt** | S | S | S | S for declared range | S | — | Very low | Low; standards-friendly |
| **Trusted full-representation digest plus exact supplied ranges** | S* | S | C/S | C/S | — unless invocation-bound | — | Low once bound to UID/ranges; hash alone insufficient | Very low verification cost |
| **Per-chunk digests plus canonical chunk manifest** | S | S | S | S if every required chunk accounted for | — unless invocation-bound | — | Low | Low; more metadata |
| **Tool says `complete=true`, `truncated=false`, plus UID/version/ranges** | S | S | S | S if tool contract guarantees it | C | — | Low–moderate; depends on tool correctness | Very cheap |
| **Explicit truncation/pagination/omitted-range reporting** | C | C | S for omissions | Strong evidence of *incompleteness* | C | — | Excellent rejection signal | Very cheap |
| **Citation/source handle containing exact file/version/range metadata** | S | C/S | S for cited spans | — beyond cited spans | C for the producing invocation | C | Low for span presence; high if generalized to whole file | Cheap; provider-dependent |
| **Provider prompt/cache hit mapped by harness to a known prefix** | C/S | C/S | C/S | C | S for mapped prefix | — | Low only with exact external mapping | Cheap; provider-specific |
| **Prompt-cache hit without document mapping** | — | — | — | — | W | — | High if treated as document proof | Cheap |
| **Input token count or remembered document length** | — | — | W | W | W | — | High | Very cheap |
| **First and last ranges / boundary markers** | C | W/C | W | W | C | — | High for missing-middle attacks | Cheap |
| **Canonical end-of-document sentinel** | C | W | Proves endpoint only | W | C | — | High for missing-middle attacks | Very cheap |
| **Random secret canary or random interior challenge** | C | C/S for specially instrumented versions | W | Probabilistic only | C/S | C | Depends strongly on sampling and leakage | Moderate token/model cost |
| **Reconstruct headings** | W | W | — | — | W | W | High | Cheap |
| **Quote boundary text** | W | W | W | — | W | W | High | Cheap |
| **Answer random substantive questions** | W | W/C | W | Probabilistic | W | C | High when model has priors | Potentially expensive |
| **Self-reported confidence** | — | — | — | — | — | W | Very high | Essentially free |
| **“Do you remember reading it?”** | — | — | — | — | — | — | Very high | Free |
| **Semantic reconstruction / pretrained familiarity** | — | — | — | — | — | C | Extreme | Free |

\* A digest establishes content identity only relative to a trusted expected digest and a defined canonical representation. It does not by itself establish the authority or logical document identity of the bytes.

### Why validators, digests and ranges work well together

HTTP semantics provide a useful precedent for the proposed document-evidence model. RFC 9110 defines a strong validator as metadata that changes when observable representation data changes and says a strong validator is unique across versions of representations of a particular resource. It notes strict revision identifiers and collision-resistant hashes as suitable approaches. Importantly, the RFC also says the same strong validator value does not imply equivalence across *different resources*, which is precisely why a digest or ETag should be paired with a stable document UID rather than used as the UID itself. citeturn17view3

Range metadata solves another part of the problem. An HTTP `Content-Range` such as:

```text
bytes 42-1233/1234
```

states both what interval was returned and the known complete representation length. Thus a harness can mechanically compute whether the union of received ranges covers the required interval. It need not ask an LLM whether anything seems absent. citeturn16view2

RFC 9530's digest fields are also directly relevant. It distinguishes the digest of transferred content from a representation digest and expressly supports validating a resource reconstructed from parts. Its examples show a partial range response carrying both the digest of the transferred partial content and a `Repr-Digest` for the complete representation. citeturn17view2turn16view4

That combination gives a strong pattern for documentation systems:

```text
document UID
+ immutable version/strong validator
+ trusted whole-representation digest
+ exact delivered range/chunk set
+ current-invocation attachment receipt
```

The important qualifier is **trusted**. RFC 9530 explicitly says its integrity mechanism does not itself define authentication and warns that digest metadata can be replaced by an attacker unless protected by mechanisms such as TLS or signatures. A digest returned by the same untrusted component that may have served the wrong document is not an independent proof of authority. citeturn17view0turn17view2

### Why endpoint checks are weak

First/last-range verification and end-of-document sentinels are useful **sanity checks**, but not completeness proofs. Consider:

```text
expected:
[A][B][C][D][E][EOF]

supplied:
[A]      [D][E][EOF]
```

The beginning, end, and EOF sentinel are all correct while two middle sections are absent. Therefore even a cryptographically unpredictable EOF token proves, at most, that the endpoint token is present—not that all preceding content was supplied.

A sentinel becomes useful as one component of a stronger protocol when combined with sequential pagination or a complete chunk/range manifest:

```text
chunks 0..117 received
same version digest on every chunk
total_chunks = 118
chunk hashes validated
EOF observed in chunk 117
```

Now completeness follows primarily from the manifest and coverage arithmetic; the sentinel is a corruption/error check.

### Why length is only a consistency check

Exact byte length is valuable when paired with exact ranges and a digest, but matching lengths alone prove almost nothing. A document with one 500-byte section deleted and another 500 bytes accidentally duplicated has the expected length while being wrong. Token counts are weaker still because they depend on tokenizer/model settings. OpenAI and Gemini expose mechanisms for counting request tokens, but those APIs report the size of input, not its document identity or completeness. citeturn19view2turn18view7

For manifests, stable byte or canonical-character offsets should therefore be primary. A token count can be recorded as diagnostics only when accompanied by a tokenizer/model identifier.

### Can completeness be established without rereading the whole document?

**Yes—by the harness, if it possesses trustworthy structural metadata.** It does not need to repeatedly send the entire document through an LLM.

Suppose canonical version `V17` has:

```text
source_uid = policy:travel-expense
version = V17
repr_sha256 = H
canonical_length = 1,284,991 bytes
required_ranges =
    [0, 12,402]          # precedence + definitions
    [220,100, 248,991]   # reimbursement section
    [901,337, 914,822]   # exceptions
```

If a trusted source has already established `H` and the harness receives exactly those intervals under the same strong version validator, it can determine mechanically that **required coverage** is complete without rereading the other million bytes. Strong validators and representation digests were specifically designed to support efficient comparisons and reconstruction checks of this general kind. citeturn17view3turn17view2

Whole-document completeness can similarly be proved from a canonical chunk manifest:

```text
version V17
expected chunks: 0..247
observed chunks: 0..247
every chunk.version = V17
every chunk.digest validates
manifest digest = trusted V17 manifest digest
```

This is categorically stronger than asking an LLM to “check whether anything seems missing.”

## Cognitive checks, false confidence, and their failure modes

Cognitive tests should be treated as **secondary functional diagnostics**, never the primary safety gate for authoritative context presence.

### Self-report is the weakest mechanism

Questions such as:

> “Do you have the complete policy in context?”

> “Are you sure you saw the whole file?”

> “Do you remember reading section 14?”

ask a generative model to infer facts about the construction of its own input from behavioral evidence. The current API documentation reviewed here exposes prompt and context-management information at the application level, not a model-facing exact-residency primitive, while model self-evaluation research concerns correctness/knowledge rather than source provenance. citeturn21view2turn19view3turn19view2

An agent that answers such a question confidently after recognizing a well-known policy is exhibiting exactly the motivating failure mode: it has inferred **presence from familiarity**.

### Heading reconstruction is particularly vulnerable to near duplicates

Suppose versions `V42` and `V43` have identical:

```text
1. Purpose
2. Scope
3. Definitions
4. Authorization
5. Exceptions
6. Appeals
```

but `V43 §4.7` changes:

```text
approval threshold: $25,000 → $10,000
```

A heading reconstruction test can score perfectly while the governing rule is stale. The same applies to first-page and final-page quotation tests when the only change is in a middle paragraph.

A document UID plus immutable version validator catches this deterministically; a heading quiz does not. RFC 9110’s distinction between resource identity and strong per-version validators is directly applicable here. citeturn17view3

### Random questions are probabilistic and can become expensive

Randomly sampling document locations is more defensible than endpoint checking, but it still does not prove complete coverage. Under an idealized model where a fraction \(f\) of the source is missing, every challenge samples a location independently and uniformly, and the LLM answers perfectly whenever the sampled content is available, the probability of failing to notice the omission after \(k\) probes is:

\[
P(\text{false pass})=(1-f)^k
\]

For a document missing its final **10%**, achieving less than a 1% chance of missing the omission requires **44 independent probes**. If only **1%** of the document is missing, it requires **459 probes** for the same idealized 99% detection probability.

That calculation is actually optimistic because real LLM answers are not perfect and, more importantly, a model might answer a challenge from pretrained knowledge or earlier conversational residue even when the challenged bytes are currently absent. Random challenges are therefore useful for measuring **functional accessibility**, especially with unpredictable synthetic canaries, but poor substitutes for mechanical coverage accounting.

### Secret canaries are substantially better, but still not complete proof

A version-specific unpredictable nonce can test whether the model has access to *some* content that could not plausibly come from pretraining:

```text
V43 canary at randomized location:
AUTH-CANARY = "7Q4M-19PX-F2"
```

If that value is generated after model training and revealed only inside the authoritative content, correctly returning it is strong evidence that the model had access to the canary-bearing content somewhere in its information path.

It still does **not** establish that the other 99.9% of the document is present. A retriever could have forwarded only the canary paragraph.

Canaries are best used for end-to-end tests of a context pipeline, not for production completeness certification.

### Confidence can correlate with knowledge without establishing provenance

Kadavath et al.’s self-evaluation work is relevant because it shows that model confidence-like outputs are not meaningless: larger models could be calibrated under some conditions, and access to relevant source material appropriately affected their estimates of knowing. But that is precisely why a high confidence value cannot distinguish “I know this because the authoritative source is presently attached” from “I know this because I learned it previously.” citeturn21view2

The correct decision-theoretic treatment is therefore asymmetric:

\[
L = \lambda_{FP}\,FP + \lambda_{FN}\,FN
\]

where a **false positive** means allowing reliance on a source that is absent, incomplete, stale, or wrong-version, while a false negative causes an unnecessary refetch.

For governing documents I recommend evaluating systems with \(\lambda_{FP}\) far greater than \(\lambda_{FN}\), for example reporting results at 10:1, 20:1, 50:1, and 100:1 ratios rather than optimizing ordinary accuracy. The precise operational weight should depend on consequence severity. This weighting strongly favors cheap re-fetches over unsupported self-confidence.

### Compaction is the decisive adversary to conversational memory

A model can truthfully have “read” a document earlier while no longer possessing its verbatim text. OpenAI says its compaction mechanism carries forward prior state in an opaque, smaller representation and makes the compacted window the canonical input for continuation. Anthropic says its compaction replaces old turns with a summary, while context editing can remove old tool results before they reach Claude. citeturn19view0turn18view5turn18view4

Therefore these are different facts:

```text
document_was_seen_in_session = true
document_summary_survives = true
document_source_text_currently_attached = false
```

A robust system must represent all three separately.

## Adversarial evaluation program

There does not appear to be an established benchmark in the primary literature reviewed here for the narrow question **“Can an LLM accurately detect that the exact authoritative document is fully present in its current effective context?”** Existing empirical work instead establishes adjacent facts: models can have useful but imperfect self-knowledge, intrinsic self-correction is unreliable without external feedback, and actual use of information inside long contexts can degrade significantly. citeturn21view2turn21view3turn21view0

A dedicated evaluation should therefore be built. Its ground truth must be supplied by the harness—not by model labels.

### Experimental design

Create two document families.

The **synthetic family** should use generated documents with random names, arbitrary rules, random version-specific numbers, and unpredictable canaries. This prevents pretrained familiarity from contaminating source-presence measurements.

The **familiar family** should use real or structurally familiar policies, standards, public rules, or synthetic documents modeled closely on common material. It deliberately measures the false-confidence problem arising from prior knowledge.

For every trial the harness records:

```text
authoritative_source_uid
authoritative_version
expected_required_ranges
actual_retrieved_ranges
actual_forwarded_ranges
actual_effective_context_ranges
compaction/edit events
summary presence
document digest(s)
```

Then run each detection mechanism independently and require it to output both:

```text
safe_to_rely: true | false
```

and a structured diagnosis:

```text
identity
version
coverage
completeness
availability
confidence
```

The primary false-positive denominator should consist of every trial in which at least one required property is unsatisfied.

### Required adversarial conditions

| Test condition | Primary failure it detects | Correct safe outcome |
|---|---|---|
| Full exact current document | Over-conservative detector | Accept |
| Same document missing final 10% | EOF/truncation detection | Reject |
| One middle section removed | Endpoint-check weakness | Reject |
| Tool result explicitly marked `truncated=true` | Failure to honor metadata | Reject |
| Several noncontiguous ranges | Mistaking excerpts for completeness | Reject unless ranges exactly equal requirement |
| High-quality summary, no source text | Familiarity/semantic reconstruction | Reject source-presence claim |
| Full document many turns earlier + substantial distractor context | Historical-versus-current state | Reject unless active manifest still proves attachment |
| Context compaction after document retrieval | Summary/residue confusion | Invalidate old verbatim receipt |
| `V42` supplied, `V43` governing; one important rule changed | Version detection | Reject |
| Near-duplicate with same headings | Identity detection | Reject |
| Public document highly familiar from pretraining but not supplied | Parametric-knowledge false confidence | Reject |
| Opening and ending supplied, middle removed | Boundary/sentinel weakness | Reject |
| Every chunk index present but half from `V42`, half from `V43` | Cross-version consistency | Reject |
| Retriever obtained entire file, only excerpt forwarded | Retrieval-versus-attachment distinction | Reject full-coverage claim |
| Current document plus stale summary also present | Conflict handling | Prefer authoritative exact-version source |
| Old version obtains a prompt-cache hit | Cache-metadata overclaim | Reject current-version claim |

The mixed-version experiment is especially important. A naïve manifest can report:

```text
chunks_received = 100 / 100
```

and still be catastrophically wrong. The correct invariant is:

```text
all required chunks present
AND all chunks bind to one authoritative representation identifier
AND that representation is the required effective version
```

### Explicit false-confidence measurement

For every condition, ask the model several differently worded questions such as:

```text
Is the complete governing document currently available to you?
Do you have every section of version V43?
Can you rely on the document without retrieving it again?
What probability do you assign that the full authoritative source is present?
```

Record **acceptance confidence on unsafe trials** as the key cognitive metric. A presence detector should be considered unsuitable as a governance gate if it frequently assigns high confidence to summary-only, familiar-document, stale-version, or near-duplicate conditions.

The most diagnostic comparison is:

```text
same substantive knowledge
different provenance state

Trial A: exact V43 text supplied
Trial B: no text, but model strongly knows V43 from training
Trial C: V42 supplied, model knows V43 from training
Trial D: V43 summary supplied
```

A true presence detector must distinguish all four despite potentially answering substantive policy questions equally well.

### Metrics

Report at least:

| Metric | Definition |
|---|---|
| Unsafe-accept false-positive rate | Fraction of absent/incomplete/stale/wrong-source trials accepted |
| False-negative rate | Fraction of valid complete-required-coverage trials unnecessarily rejected |
| Exact-version detection | Accuracy at rejecting wrong and mixed versions |
| Coverage detection | Ability to identify missing ranges/chunks |
| Compaction robustness | Whether prior receipts are invalidated correctly |
| Prior-knowledge robustness | FP rate when model knows content without source |
| Near-duplicate robustness | FP rate under same-heading/similar-text impostors |
| Provider portability | Same mechanism can be implemented without undocumented internals |
| Model dependence | Performance variation by model capability |
| Token cost | Extra input/output required per check |
| Tool-call cost | Additional retrieval/metadata requests |
| Latency | Added critical-path time |
| Implementation burden | State, metadata and integration complexity |

For harness-based deterministic mechanisms, the meaningful test is less “does the model detect the omission?” and more “does the gate reject every malformed receipt/manifold combination?” Such tests can be exhaustively property-tested: randomly delete chunks, duplicate chunks, swap versions, alter offsets, change digests, or replay receipts from older context epochs.

For cognitive checks, by contrast, model capability, context length, position and prior familiarity should be explicit experimental factors. Long-context research already shows that content position can materially affect successful use even when the information is actually present. citeturn21view0

## Recommended architecture and default protocol

The smallest mechanism giving strong evidence is a **versioned required-coverage manifest plus an invocation-scoped attachment receipt**. Whole-document re-reading is unnecessary when metadata is trustworthy.

The architecture should look like:

```text
decision requires governing authority
              ↓
determine required authoritative coverage
              ↓
active context manifest has a valid receipt?
              │
      ┌───────┴────────┐
      │                │
     yes               no / uncertain
      │                │
verify:                resolve canonical source
  source UID                 ↓
  exact version         obtain immutable version ID
  required ranges             ↓
  same-version set      fetch missing required ranges
  current context epoch       ↓
      │                 verify ranges/digests
      │                       ↓
      │                 attach to model invocation
      │                       ↓
      │                 issue presence receipt
      └──────────┬────────────┘
                 ↓
        model interprets source
                 ↓
       citations / understanding checks
                 ↓
             decision
```

### Declare required coverage before retrieval

The routing layer should resolve a request to something like:

```text
DecisionRequirement {
  authority_uid,
  version_policy,
  required_sections,
  required_dependencies
}
```

`required_dependencies` matters. A section may use terms defined elsewhere, incorporate another provision by reference, be subject to an exception section, or be overridden by a precedence clause. The retrieval policy should therefore compute a **dependency closure** before declaring required coverage complete.

For example:

```text
required:
  §7.2 travel approval

dependencies:
  §1.3 "employee"
  §2 precedence
  §7.1 scope
  §7.8 exceptions
  Appendix B monetary thresholds
```

The correct gate is not “§7.2 was found.” It is “the authoritative coverage needed to interpret §7.2 for this decision has been established.”

### Resolve authority and immutable version first

A canonical document should have a stable logical UID independent of filename, title, or URL:

```text
source_uid = corp-policy://travel-expense
```

Then bind it to an immutable representation:

```text
version_id = 2026-07-01-r17
effective_from = 2026-07-01T00:00:00Z
strong_validator = "..."
repr_sha256 = "..."
canonical_length = ...
```

RFC 9110’s strong-validator semantics are a suitable model: validators distinguish versions of one resource, while resource identity itself remains separately represented. citeturn17view3

For rules whose applicability depends on event time, “latest version” is not necessarily the correct version policy. The request may require:

```text
version_effective_at(incident_date)
```

rather than:

```text
latest_version()
```

This should be decided by the routing layer, not guessed by the model from document wording.

### Verify coverage mechanically

Each retrieval result should expose exactly which source representation and range it contains:

```text
chunk_id
source_uid
version_id
start_offset
end_offset
chunk_digest
representation_digest
```

Then compute the union of `attached_ranges`, not merely `retrieved_ranges`.

For a whole-document requirement:

\[
\bigcup attached\_ranges = [0,L)
\]

For partial required coverage:

\[
required\_ranges \subseteq \bigcup attached\_ranges
\]

Every range participating in the union must bind to the **same required immutable version**.

HTTP `Content-Range` and representation digest semantics demonstrate that exact range and full-representation metadata can be represented separately and validated mechanically. citeturn16view2turn16view4

### Issue an invocation-scoped presence receipt

The crucial extra step is to distinguish retrieval from current attachment.

A useful proposed receipt is:

```json
{
  "receipt_type": "authoritative_context_presence",
  "source": {
    "uid": "corp-policy://travel-expense",
    "authority": "canonical-policy-repository",
    "version_id": "2026-07-01-r17",
    "effective_from": "2026-07-01T00:00:00Z",
    "strong_validator": "\"r17-991ce...\"",
    "representation_sha256": "..."
  },
  "representation": {
    "canonical_byte_length": 1284991
  },
  "requirement": {
    "required_ranges": [
      [0, 12403],
      [220100, 248992],
      [901337, 914823]
    ]
  },
  "retrieval": {
    "retrieved_ranges": [
      [0, 12403],
      [220100, 248992],
      [901337, 914823]
    ],
    "truncated": false,
    "omitted_required_ranges": []
  },
  "attachment": {
    "attached_ranges": [
      [0, 12403],
      [220100, 248992],
      [901337, 914823]
    ],
    "complete_for_requirement": true,
    "complete_document": false,
    "same_version": true,
    "model_invocation_id": "inv_...",
    "context_epoch": 37
  }
}
```

The model should receive a compact rendering of that receipt alongside the content, but the enforcement gate should live **outside the LLM**. The model is allowed to proceed only when the harness says the receipt validates.

The `context_epoch` is important. Any context-changing operation—compaction, summarization, truncation, old-tool-result clearing, model migration, conversation reconstruction—should increment the epoch or otherwise invalidate receipts whose source bytes can no longer be mechanically shown to survive.

Current platform behavior supports the need for that invalidation rule: OpenAI compaction creates a shorter canonical subsequent context, while Anthropic can summarize history or remove old tool results before model inference. citeturn19view1turn18view4turn18view5

### Distinguish five different completion flags

Retrieval tools should avoid a single ambiguous `complete: true`. Prefer:

```text
source_resolution_complete
retrieval_complete_for_request
attachment_complete_for_request
complete_authoritative_document
complete_required_authoritative_coverage
```

This prevents the common error:

```text
search operation completed successfully
```

being interpreted as:

```text
the search returned every byte of the document
```

or:

```text
every returned byte remains in the current model input
```

### Use cache evidence opportunistically, not as the authority

Provider prompt caching can reduce repeated document cost. OpenAI says its cache reuses matching rendered prompt prefixes and exposes cached-token accounting; Anthropic likewise exposes cached-prefix usage, and Gemini reports cache-hit token quantities. citeturn15view9turn19view4turn20view0

A good implementation can therefore attach a stable governing source once, record its immutable version and prefix mapping, and reuse the provider cache where supported.

But the logical proof should remain:

```text
source/version/coverage → known exact prompt prefix → current provider request
```

not:

```text
cache hit → therefore correct governing document
```

Caching is an optimization layer beneath the evidence protocol.

### Cheapest reliable recovery

When the gate fails, the recovery should be **minimal missing authoritative coverage**, not automatically the entire document.

The escalation order I recommend is:

1. **Receipt stale, bytes locally cached by digest:** reattach the already verified required chunks to the new context epoch. No remote document fetch is necessary.
2. **Version uncertain, content otherwise available:** ask the authoritative store for inexpensive metadata—a version identifier, strong validator or representation digest. If unchanged, reuse verified local bytes. Strong validators were designed precisely to support validation without retransmitting an unchanged representation. citeturn17view3
3. **Known missing ranges:** fetch only those ranges from the exact version and attach them.
4. **Required section known but absent:** retrieve that section plus its dependency closure.
5. **Tool output truncated:** continue pagination/range fetching until required coverage is mechanically complete.
6. **Dependencies cannot be bounded or metadata is inadequate:** fetch the complete authoritative representation.
7. **Authoritative version itself cannot be established:** stop relying on remembered content and resolve the authority/version before substantive reasoning.

This produces the intended asymmetry: an uncertain state causes a cheap deterministic repair rather than a potentially dangerous model self-certification.

## Minimal fallback, retrieval-tool contract, and documentation implications

### Minimal fallback without special context tooling

An agent running on a platform with no context manifests or attachment receipts cannot honestly establish exact current residency with the same strength. Its fallback should therefore be conservative.

Immediately before a consequential decision, re-fetch the **smallest authoritative unit known to be sufficient**—normally the relevant section plus definitions, exceptions, cross-references and precedence clauses—and rely on that fresh tool result rather than conversational memory.

The tool response should be inspected for:

```text
source identity
version/effective date
range or section identifier
pagination
truncation marker
total length/count if available
```

Any explicit `truncated`, `has_more`, pagination cursor, omitted-range indication or incomplete-result condition requires further fetching before completeness is claimed.

When the retrieval mechanism exposes no trustworthy completeness metadata, the agent should **not say “I have the full document in context.”** It can instead make a narrower truthful claim such as:

> “I have freshly retrieved the authoritative text of sections 4.1–4.8 and the referenced definitions; full-document presence has not been established.”

If whole-document coverage is mandatory and the tool has no manifest facility, sequential bounded pagination until authoritative EOF is substantially safer than asking the model whether the document “looks complete.” First/last-page checks and EOF markers can be added as sanity checks, but—as shown above—they do not detect arbitrary middle omissions.

This fallback incurs more tool calls than a manifest architecture but sharply reduces false-positive risk.

### What retrieval tools should return

A retrieval API intended for agentic governance should return **evidence about delivery**, not merely text. The minimum useful contract is:

| Field | Why it matters |
|---|---|
| `source_uid` | Distinguishes logical document identity from title similarity |
| `canonical_origin` / authority | Establishes where authoritative status comes from |
| `version_id` | Separates versions |
| `effective_from` / `effective_to` or state ID | Allows temporal applicability checks |
| `strong_validator` | Cheap change/version validation |
| `representation_digest` | Binds to exact representation bytes |
| `canonical_byte_length` | Supports coverage arithmetic |
| `requested_ranges` | Records what caller intended |
| `retrieved_ranges` | Records what retrieval layer actually obtained |
| `forwarded/attached_ranges` | Records what the model actually receives |
| `chunk_ids` and `total_chunks` | Enables all-chunk checking |
| `per_chunk_digest` | Detects wrong/duplicate/mixed chunks |
| `same_version` | Explicit mixed-version guard |
| `truncated` | Unambiguous failure signal |
| `omitted_ranges` | Makes partial results explicit |
| `has_more` / pagination cursor | Prevents silently treating first page as complete |
| `complete_for_request` | States completion relative to requested coverage |
| `complete_document` | Separately states whole-document completion |
| `retrieval_receipt_id` | Audit/debugging handle |
| `model_invocation_id` / `context_epoch` | Connects retrieval to current effective invocation |
| `representation_type` | Distinguishes `source_text`, `excerpt`, `summary`, `embedding`, `compaction` |
| `derived_from` | Makes summaries and transformations traceable to a source version |

A particularly important field is:

```text
representation_type: "summary"
lossy: true
```

A high-quality summary should never be permitted to masquerade as source text merely because it correctly reproduces most rules.

Similarly, the tool should report two separate facts:

```text
retrieval.full_document_available_to_tool = true
attachment.complete_document_to_model = false
```

when a retrieval service has access to the complete file but forwards only ranked excerpts.

### Prefer stable structural identifiers over natural-language identity

Document authors and repositories should supply stable section identifiers that survive heading edits:

```text
section_uid = travel.approval.threshold
```

rather than making agents identify material by:

```text
heading = "Approval Requirements"
```

Two near-identical versions can preserve every heading while changing one operative sentence. Identity and version should therefore be machine metadata, not semantic guesses.

Versioned chunk identifiers should incorporate or bind to the immutable source version:

```text
chunk_uid = hash(
    source_uid,
    version_id,
    canonical_start,
    canonical_end,
    chunk_digest
)
```

This makes “all chunk numbers present but some came from last month’s version” mechanically rejectable.

### Encode cross-reference structure for routing

The primary abstraction **required authoritative coverage** works best when document systems expose machine-readable dependencies. A section could declare:

```text
depends_on:
  - definitions.employee
  - precedence.general
  - exceptions.executive
```

The router can then fetch a dependency closure instead of forcing every decision to carry a 300-page manual.

This substantially improves the token economics of high-assurance document use: the system spends tokens on all *relevant authoritative material*, rather than on either an unsafe search-result excerpt or an unnecessarily complete corpus.

### Keep governing-source evidence out of disposable conversational memory

Critical context metadata should live in a harness-controlled data structure rather than in an assistant sentence such as:

> “Earlier I confirmed that policy.pdf was complete.”

That sentence can survive while the actual bytes are removed, summarized, or compacted. Current APIs explicitly support exactly such transformations of earlier context. citeturn19view0turn18view4turn18view5

The persistent record should instead resemble:

```text
active_context_manifest[context_epoch=37]:
    policy://travel-expense@V17
        ranges = {...}
        receipt = R381
        valid = true
```

On compaction:

```text
context_epoch = 38
invalidate R381
```

unless the context-management component can mechanically certify that the authoritative content itself—not merely a derived summary—survived into epoch 38.

### Current evidence versus proposed design

The distinction between documented present capabilities and design recommendations is important:

| Status | Finding |
|---|---|
| **Documented today** | Models accept bounded contexts; information in those contexts can be used imperfectly, especially in long inputs. citeturn21view0 |
| **Documented today** | Model self-evaluation can contain useful information about expected correctness/knowledge, but it is imperfect and does not establish source provenance. citeturn21view2 |
| **Documented today** | Intrinsic model self-correction without external feedback can fail or degrade performance. citeturn21view3 |
| **Documented today** | OpenAI exposes prompt caching, input-token accounting and compaction; compaction may replace earlier context with a smaller opaque state. citeturn15view9turn19view2turn19view0 |
| **Documented today** | Anthropic exposes prompt-cache accounting and can remove old tool results or summarize earlier turns as part of context management. citeturn19view4turn18view4turn18view5 |
| **Documented today** | Gemini exposes input token counting and cache-hit token counts. citeturn18view7turn20view0 |
| **Documented today** | HTTP standards provide strong validators, exact range metadata and full-representation digests suitable for externally verifying version and reconstructed coverage. citeturn17view3turn16view2turn17view2 |
| **Research conclusion from reviewed public APIs** | I found no documented general-purpose model-facing primitive that lets the LLM itself inspect an authoritative inventory of exact current context residency. |
| **Proposed architecture** | Maintain `required_authoritative_coverage` and active-context manifests in the harness. |
| **Proposed architecture** | Introduce invocation-scoped “presence receipts” binding source UID, version, ranges and context epoch. |
| **Proposed architecture** | Invalidate receipts on compaction, truncation, summarization or other transformations unless exact source retention is mechanically certified. |
| **Proposed architecture** | Make retrieval tools report retrieved ranges and model-attached ranges separately. |
| **Proposed architecture** | Treat cognitive checks as understanding/accessibility tests, never as the authoritative presence gate. |

### Recommended default rule

A production agent should implement the following gate:

```text
MAY_RELY(document, decision) =
    authoritative_identity_verified
    AND required_version_verified
    AND required_coverage_declared
    AND every_required_range_accounted_for
    AND all_ranges_from_same_version
    AND no_unresolved_truncation_or_omission
    AND attachment_receipt_valid_for_current_context_epoch
```

Understanding is deliberately not in that Boolean. It is a subsequent requirement:

```text
MAY_ACT =
    MAY_RELY
    AND interpretation/decision checks pass
```

The agent may say **“I have the governing document in context”** only when the `MAY_RELY` evidence covers the entire document. When only the decision-relevant subset is established, it should instead say **“I have the required authoritative coverage for this decision.”**

That wording is more precise, less costly, and more robust to long-running sessions.

The conceptual hierarchy is therefore:

```text
familiar with document
        ≠
previously read document
        ≠
retriever currently has document
        ≠
some excerpts currently attached
        ≠
complete required authoritative coverage attached
        ≠
complete authoritative document attached
        ≠
model understood document correctly
```

The decisive design principle is to move as far down that chain as the decision requires **using externally checkable metadata rather than model confidence**. A cheap refetch of a missing or stale authoritative section is ordinarily far less costly than a false-positive certification that lets an agent apply a remembered, truncated, summarized, mixed-version, or superseded rule.