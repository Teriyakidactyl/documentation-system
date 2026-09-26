---
uid: RMRAE6
form:
  path: '<a href="../../a.%20Document%20Design/a.%20Assemblies/b.%20Forms/c.%20Records/d.%20Research/a.%20Research%20Prompt/README.md" uid="BSJY2D">documentation-system:§a.a.b.c.d.a</a>'
  version: '1.0'
description: >-
  `Read in full and follow when` *the governing-document context-presence
  investigation is rerun* `to` **execute the preserved research request
  without substituting a summary, reconstructed criteria, or run-specific
  assumptions for the original prompt**.
---

# Research Prompt: Governing Document Context Presence

The fenced block below is the exact rerunnable research payload. Repository
frontmatter and this wrapper are not part of the prompt.

````text
@ Research methods by which an LLM-based agent can determine, with useful reliability, whether a governing document is fully present in its current effective context before relying on it.
The motivating failure mode is this: an agent may remember a rule, summary, heading, or prior interpretation from a document and therefore behave as though the document is “in context,” even though the authoritative document is absent, truncated, represented only by an old summary, partially retrieved, or present at the wrong version. The research should distinguish **knowledge or familiarity with a document** from **evidence that the authoritative document content is presently available to the agent**.
Evaluate both **tool-assisted mechanisms** and **agent-side cognitive/self-check mechanisms**. Do not assume that models have direct introspection into their context window, attention state, hidden prompt, or exact token residency unless a specific platform actually exposes such a capability.
The research should answer these questions:

1. What can an LLM reliably know about whether a document is fully present in its current context?
2. Which signals can only establish that the model remembers or can reconstruct content, rather than proving that the source itself is present?
3. What tool or harness mechanisms can establish presence more strongly than model self-assessment?
4. Can completeness be established without rereading the whole document every time?
5. How should an agent distinguish:
   - complete authoritative document;
   - complete relevant section only;
   - truncated retrieval;
   - selected line ranges;
   - summary or compressed representation;
   - earlier-conversation residue;
   - model prior knowledge;
   - stale version;
   - duplicate or near-identical versions;
   - content retrieved through a tool but no longer reliably available in active context?
6. What evidence should be sufficient before an agent says, “I have the governing document in context”?
7. When evidence is insufficient, what is the cheapest reliable recovery action?

Investigate candidate mechanisms including, but not limited to:

- retrieval manifests recording document identity, version, byte/token length, retrieved ranges, and completion status;
- tool responses that explicitly report truncation, pagination, omitted ranges, or full-document completion;
- content hashes or digests associated with retrieved documents;
- first/last-range or boundary-marker verification;
- canonical end-of-document sentinels;
- chunk manifests proving that all chunks of a version were supplied;
- document UID + exact version/state identifiers;
- context manifests maintained by the harness rather than inferred by the model;
- citations or source handles whose metadata identifies exact retrieved ranges;
- tool calls that answer whether a source/range is currently attached to the model invocation;
- re-fetch-on-demand protocols;
- lightweight “presence receipts” emitted by retrieval tools;
- agent self-tests such as reconstructing headings, quoting boundary text, recalling document length, or answering randomly selected questions;
- confidence/self-report checks;
- asking the model whether it remembers reading the document;
- semantic reconstruction from learned or earlier context.

For every mechanism, distinguish what it actually proves. In particular, determine whether it establishes:

- **identity** — this is the intended document;
- **version** — this is the intended state of that document;
- **coverage** — the required content range was supplied;
- **completeness** — no required portion was omitted;
- **availability** — the supplied content is still usable in the current model invocation;
- **understanding** — the model interpreted the content correctly.

Do not collapse these into one Boolean such as `document_in_context: true`.
Design adversarial experiments. At minimum test:

- a full document versus the same document missing its final 10%;
- a document missing one middle section;
- a tool response explicitly marked truncated;
- several noncontiguous retrieved ranges;
- a high-quality summary with no source text;
- a document read many turns earlier after substantial intervening context;
- conversation/context compaction;
- two versions differing by one important rule;
- a near-duplicate document with the same headings;
- a model that has strong pretrained familiarity with the subject;
- a document whose opening and closing passages are present but whose middle is absent;
- all chunks present but supplied in the wrong version combination;
- a full document supplied to a tool or retrieval layer but only an excerpt actually passed to the model.

For cognitive checks, deliberately measure **false confidence**. A self-check is unsafe if the agent frequently concludes that the document is present when it merely remembers or reconstructs it. False positives should be weighted substantially more heavily than unnecessary re-fetches.
Compare approaches on:

- false-positive rate;
- false-negative rate;
- version-detection reliability;
- completeness-detection reliability;
- dependence on model capability;
- dependence on hidden model internals;
- token cost;
- tool-call cost;
- latency;
- implementation complexity;
- portability across model providers;
- robustness under context compaction and long-running agent sessions.

Identify which mechanisms are fundamentally impossible or unreliable without harness support. In particular, investigate whether current LLM APIs provide any trustworthy model-facing primitive for determining exact context residency, or whether this must be represented externally by retrieval/context-management tooling.
Produce a recommended architecture for an agentic documentation system. Prefer the smallest mechanism that gives strong evidence. Consider a model such as:

```text
governing document required
        ↓
context evidence available?
        │
        ├── exact identity/version + complete required coverage established
        │       ↓
        │   proceed
        │
        └── absent / uncertain
                ↓
          retrieve authoritative content
                ↓
          record retrieval evidence
                ↓
          proceed

```

Evaluate whether “full document present” should even be the primary abstraction, or whether the more useful concept is **required authoritative coverage established for this decision**.
The final research output should contain:

1. a taxonomy of the different meanings of “document is in context”;
2. a comparison matrix of candidate detection mechanisms;
3. empirical or documented evidence about reliability where available;
4. failure modes for cognitive/self-assessment techniques;
5. mechanisms requiring harness/tool support;
6. a recommended default protocol;
7. a minimal fallback protocol for agents operating without special context tooling;
8. recommendations for what retrieval tools should return to make presence mechanically checkable;
9. any implications for documentation-system routing or authoring guidance;
10. a clear separation between conclusions supported by current platform/API evidence and proposed designs.

Favor mechanisms that make context availability **observable external state** over mechanisms that ask an LLM to infer its own internal context condition.
````
