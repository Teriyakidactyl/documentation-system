---
uid: E1AK8J
form:
  path: '<a href="../../2%20Technical%20Writing/3%20Document/1%20Document%20Forms/10%20Research/2%20Research%20Report/README.md" uid="AKNN1G">documentation-system:§2.3.1.10.2</a>'
  version: '1.0'
description: >-
  `Consult when` *the 2026-09-25 conversation-derived investigation of
  repository-inspection workflow is reviewed* `to` **use the retained
  observations about entry guidance, tree reconnaissance, whole-file reading,
  targeted search, EOF evidence, and connector context economics without
  treating them as current workflow authority**.
research-prompt: HJ78QV
research-run:
  executed-at: '2026-09-25'
  model: GPT-5.6 Sol
  version: GPT-5.6 Sol
  prompt-provenance: post-documented-after-interactive-run
---

# Agentic repository workflow styles under connector-based harnesses

> [!WARNING]
> **Post-documentation provenance.** This record was authored after the
> interactive investigation it preserves. The sibling `Prompt.md` is a
> post-hoc formalization of the questions that drove the dialogue, not a
> prompt frozen before execution. The `research-prompt` relationship records
> that later reusable formulation and must not be interpreted as evidence that
> this run executed its fenced payload verbatim.

## Investigation context

The investigation began with a hypothetical comparative code-architecture
task: open `Teriyakidactyl/saps`, evaluate whether its `Skills/` code is
more coherent and well designed than the Documentation System's
`4 Tooling/`, and explain which tools an agent in the current harness would
naturally call and in what order.

The user was primarily investigating the workflow itself. The concrete
repository comparison was used only far enough to reveal actual retrieval and
context-management behavior. No final SAPS-versus-Tooling design verdict was
attempted.

The conversation then tightened three questions:

1. whether a recursive tree was being preferred over a local `README.md`;
2. how a connector-based agent can know that a chunked read reached EOF; and
3. what it means for the harness to favor structured connector calls rather
   than a persistent local checkout.

## Default inspection sequence

The corrected default sequence is:

```text
repository metadata
        ↓
repository-root directory listing
        ↓
repository entry and governance files
README.md / AGENTS.md / SKILL.md / harness-specific entry files
        ↓
target directory entry guidance, when present
        ↓
target directory listing
        ↓
recursive target tree or compact structural inventory
        ↓
selected whole implementation files
        ↓
representative tests and declared architecture
        ↓
targeted cross-corpus search
        ↓
history, execution, or further validation when the question requires it
```

A recursive tree does not replace a local README. A tree establishes what
exists. An entry document may establish how that space is intended to be
interpreted. When a target directory exposes local entry guidance, that
guidance belongs before recursive structural interpretation.

The first live calls made against SAPS followed most of this sequence:

1. repository metadata;
2. repository-root contents;
3. root `README.md`;
4. immediate `Skills/` contents;
5. inspection of the root `.agent/` surface;
6. immediate `4 Tooling/` contents in the comparison repository; and
7. a recursive tree of SAPS `Skills/`.

The dialogue then identified that the workflow description should have made
the check for a target-local `Skills/README.md` explicit before treating
recursive enumeration as the next default step.

## Tree reconnaissance before grep

A code-coherence comparison is primarily a question about units, ownership,
dependency direction, and seams. Search results expose lexical matches and
fragments. Used too early, they encourage the agent to infer architecture from
the vocabulary it happened to query.

A recursive tree can expose:

- active versus archived areas;
- candidate architecture and requirements documents;
- shared versus skill-local directories;
- implementation entry points;
- test locations;
- file sizes that determine sensible retrieval strategy; and
- repeated structural patterns across sibling components.

This gives the agent a topology without loading every implementation body.

The SAPS reconnaissance demonstrated both the value and the risk. Its
`Skills/` tree exposed architecture files, manifests, tests, skill-local
`scripts/skill.py` modules, archives, logs, and multiple shared areas. The
raw recursive result was also very large. Emitting it directly caused the tool
output presented to the model to be truncated.

That failure is itself evidence for the workflow principle:

```text
broad external inspection
        ≠
broad model-context exposure
```

The better operation is to retrieve broad structural metadata, aggregate or
filter it inside the orchestration layer, and expose a compact inventory to
the model.

## Whole-file reading and targeted search

Whole-file retrieval is preferred when the file itself is the reasoning unit.
Understanding a module's imports, local abstractions, error paths, entry point,
and bottom-of-file orchestration often requires relationships that search
snippets destroy.

For small and medium modules, a complete read is normally more informative
than a collection of matches. Large files can still be treated as whole
reasoning units by reading deliberate bounded ranges through EOF.

Search becomes more valuable after an architectural hypothesis exists. Typical
questions then become:

```text
Who imports this shared package?
Does a supposed adapter import domain code?
Where is subprocess execution owned?
Does another module parse Markdown directly?
Do sibling skills bypass the declared common abstraction?
Where is this error/result type constructed?
```

Search is strong at testing those corpus-wide propositions. It is weaker at
discovering the initial architecture without a model of what the repository
claims its boundaries are.

Tests should also be inspected relatively early. Tests expose which seams are
stable enough to exercise independently. A component that cannot be tested
without assembling unrelated infrastructure provides different architectural
evidence from one whose boundary can be instantiated directly.

## EOF and truncation evidence

The GitHub file-retrieval action available in the observed harness accepts
optional line ranges but does not expose a dedicated model-facing
`eof: true` or `total_lines` field.

A request for a complete file therefore does not by itself prove that the
model observed the complete result. Several layers are distinct:

```text
GitHub stores the complete file
        ↓
connector retrieves the complete file
        ↓
harness delivers the complete tool result
        ↓
model context contains the delivered result
        ↓
model encounters the expected terminal content
```

The conversation observed a concrete separation between the middle layers:
a connector operation returned a large recursive tree, while the tool surface
reported that the output shown to the model had been truncated.

For consequential full-file reads, bounded ranges provide stronger evidence.
If requests for lines 1-200 and 201-400 are full, while a request for 401-600
returns only the file's remaining lines, the final short range is evidence
that the retrieval crossed the file boundary. A subsequent empty range beyond
that point can make the transport boundary more explicit.

That remains tool-level evidence. An artifact-native terminal marker such as:

```text
eof:<uid>
```

would establish a different fact when the model actually observes it: the
retrieved artifact contained its expected terminal marker and the marker
matched the artifact identity. It would not prove that all middle content was
delivered, nor that the agent understood the preceding material. It would make
one narrow failure, stopping before the expected endpoint, conspicuous.

## Persistent local checkout and structured connector access

A persistent local coding environment normally gives the agent a repository
checked out on a filesystem. The agent can perform arbitrary operations such
as `find`, `rg`, `sed`, Git inspection, parser runs, and custom Python
analysis. Thousands of local files can be examined by a script while only a
small summary is printed for model consumption.

The observed connector environment exposes predefined GitHub operations
instead. A file fetch, repository search, directory fetch, commit lookup, or
write operation has a declared input shape and result shape. The agent does
not assume an arbitrary shell command against a persistent checkout merely
because the underlying repository is on GitHub.

This changes the natural information economics. Naively fetching many files
through a connector can place large raw results into the conversation context.
A recursive metadata operation is therefore often cheaper cognitively than
hundreds of file-body retrievals.

The harness also exposes an orchestration layer. Several connector operations
can be invoked programmatically, their results filtered or aggregated inside
the tool execution, and only a compact derived result emitted into active
model context. That restores an important advantage usually associated with a
local shell.

The relevant distinction is therefore not simply shell versus connector. It is:

```text
external state inspected
        ≠
raw state exposed to model context
```

A capable harness can permit broad inspection while keeping context exposure
narrow.

## Three useful workflow modes

Three interaction modes emerged.

**Direct retrieval** loads a complete reasoning unit into model context. It is
appropriate for a README, architecture document, source module, or other file
whose internal relationships matter directly.

**Programmatic reconnaissance** examines broad metadata or many external
objects, performs filtering or aggregation before model exposure, and returns
a compact structural result. It is appropriate for trees, inventories,
dependency counts, file-size distributions, and candidate selection.

**Targeted search** asks a specific corpus-wide question after a hypothesis
exists, then follows significant matches back into their whole owning units.
It is appropriate for dependency-boundary audits, duplicated parsing behavior,
ownership leaks, and use-site analysis.

These modes should not be collapsed into one generic retrieval behavior.

## Harness-aware implications

Agent workflow depends materially on the available harness.

A local-shell agent can cheaply transform repository state before deciding
what to read. A connector-only agent benefits more from structured directory
and tree operations. An orchestrated connector agent can combine both styles:
broad structured retrieval outside model context and selective projection into
it.

This means repository guidance that says only "inspect the repository" leaves
a consequential operational choice unspecified. The efficient and reliable
interpretation depends on whether the agent can:

- list structure without retrieving bodies;
- aggregate tool results before model exposure;
- search corpus-wide;
- address bounded file ranges;
- observe truncation or pagination metadata;
- execute repository-local analysis code; and
- maintain a persistent working copy.

These are not merely implementation details. They affect how cheaply an
amnesiac agent can reconstruct orientation state and how convincingly it can
establish that required context has been acquired.

## Implications for agent-facing information architecture

The workflow behaves like progressive disclosure over an external information
environment.

A useful sequence is:

```text
compact orientation state
        ↓
select next relevant unit
        ↓
acquire complete local state
        ↓
form architectural hypothesis
        ↓
search broadly for counterexamples
        ↓
load only evidence required to resolve them
```

This suggests several design pressures for agent-facing repositories and
harnesses:

- entry surfaces should activate before target-first mutation or analysis;
- local README files should explain how their subtree should be interpreted
  before a recursive inventory is treated as semantic structure;
- tools should separate broad retrieval from model-context projection;
- retrieval APIs should report truncation, pagination, ranges, and completion
  explicitly where possible;
- whole-unit retrieval should remain easy when internal relationships matter;
- search should be optimized for testing known structural claims rather than
  replacing orientation; and
- artifact-native terminal markers can complement tool-level completion
  metadata when observing the end of a document is itself consequential.

## Limits of this run

This run did not complete the proposed SAPS-versus-Documentation-System code
quality comparison. SAPS was inspected only far enough to expose workflow
choices and context-boundary behavior.

The observations about the current harness describe the capabilities exposed
during this conversation. They should not be generalized to every ChatGPT
configuration, every GitHub integration, or every coding-agent environment.

The reusable prompt was reconstructed after the conversation. Future runs
using that prompt can produce conventionally ordered Prompt-to-Report
provenance and can test whether the workflow conclusions remain stable across
different harnesses.
