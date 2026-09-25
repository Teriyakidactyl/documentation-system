---
uid: 0QZE9Q
form:
  path: '<a href="../a.%20Document%20Design/a.%20Document/b.%20Document%20Forms/c.%20Fault%20Record/README.md" uid="CD4R6P">documentation-system:§a.a.b.c</a>'
  version: '1.0'
description: >-
  `Read in full when` *the failure in which a required full-document load
  terminated after relevant material was found before EOF needs review* `to`
  **reconstruct how output truncation led recovery to lose its EOF completion
  criterion and distinguish the evidence, causal mechanism, and recurrence
  controls without treating this record as current authority**.
quadrant: Explanation
fault:
  recorded-at: '2026-09-24T13:15:04-07:00'
  repository-revision: 8c6af09c666cc71fdc8a13f6e41fb01aeb87303f
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

# 💡 Full-document traversal stopped before EOF

## Expectation

The repository state identified by `fault.repository-revision` required a
selected document's complete source text to be identifiable in active,
non-compacted conversation history before reliance. When that condition was not
met, the root `README.md` required the document to be read in full.

The selected Technical Writing procedure, `2 Technical Writing/1 🛠️ Write A
Technical Document.md`, carried a `Read in full and follow when` directive.
Its directive grammar explicitly defined `Read in full and follow when` as
consuming the entire document before performing the task and stated that a
keyword search, grep hit, or partial read does not satisfy a directive that
requires full context.

The completion condition for entering that procedure was therefore complete
source consumption, not discovery of the immediately relevant rule.

## Occurrence

The agent correctly routed the documentation edit into Technical Writing and
Editing and initially requested the complete selected procedures. It fetched
both procedures inside one orchestration call and attempted to emit their
combined source into active context.

The orchestration output exceeded its 10,000-token emission cap and reported:

```text
Warning: truncated output (original token count: 14255)
```

The agent recognized the truncation and changed to ranged retrieval of the
Technical Writing procedure. It requested ranges `1-180`, `181-360`, and
`361-540`, then redundantly requested `361-540` again.

The range containing the terminology-placement rule answered the immediate
question. Retrieval stopped without establishing that line 540 was EOF and
without requesting the remaining source. The agent then relied on the
procedure and landed the documentation edit.

The resulting edit was not shown to be substantively wrong. The failure was
procedural: a selected governing document was relied on before its required
full-read completion condition had been satisfied.

## Evidence

Direct observations establish the failure:

- the first combined retrieval explicitly reported output truncation;
- the wrapper used for orchestration caps emitted output at 10,000 tokens;
- the combined attempted emission was reported as 14,255 tokens;
- recovery switched from a whole-file request to bounded line ranges;
- the recovered ranges stopped at line 540 and did not establish EOF;
- the relevant terminology rule had already been found before retrieval
  stopped; and
- subsequent review established that the procedure actually contained 968
  lines.

The repository text at the involved revision independently establishes that
partial retrieval was not an allowed substitute for the selected directive.

During preparation of this Fault Record, the same class of trigger recurred:
four contiguous ranges of the 968-line procedure were batched into one
orchestration output, which reported:

```text
Warning: truncated output (original token count: 11631)
```

This time the agent treated truncation as incomplete traversal, discarded the
combined call as evidence of completion, replayed the ranges one call at a
time, and continued through line 968/EOF. That observation demonstrates the
intended recovery behavior in this interaction. It does not establish that a
durable repository control now enforces it.

## Causal analysis

The initial output truncation was the trigger, not the complete failure
mechanism. Before truncation, the agent had attempted to honor the full-read
directive.

The failure mechanism arose during recovery. The original operation had an EOF
termination condition: load the complete selected document. After truncation,
the operation was reframed as retrieval of manageable pieces. Once the
immediately relevant section was present, the agent's ordinary
relevance-oriented retrieval heuristic supplied a different stopping condition:
enough authoritative information had been found to continue the task.

That substitution changed the operation from full-document traversal into
search-like retrieval without an explicit decision to do so.

Several conditions contributed:

- two complete documents were batched into one emitted orchestration result,
  making the 10,000-token transport limit more likely to truncate the result;
- the recovery ranges were chosen as an ad hoc transport tactic rather than as
  a traversal whose remaining range was mechanically tracked;
- no explicit state such as `eof-observed: false` or `complete: false`
  remained visible after each ranged read;
- the relevant rule appeared before the document ended, allowing the normal
  relevance stopping heuristic to fire; and
- the repository stated the semantic obligation clearly but did not separately
  state a truncation-recovery protocol that preserved EOF as the mandatory
  completion criterion.

The evidence does not support instruction ambiguity as the cause. The
repository explicitly required complete consumption and explicitly rejected
partial retrieval as compliance.

## Response and recovery

The failure was detected during later review of the tool-call sequence. The
agent first described its behavior as having read "enough" of the writing
procedure, then corrected that characterization after the incomplete traversal
was examined against the `Read in full` directive.

The immediate correction was to distinguish routing correctness from
document-consumption compliance and to identify that EOF had never been
established. Subsequent investigation isolated the orchestration output cap,
the batching decision, and the transition from whole-file retrieval to ranged
retrieval.

The replay performed while authoring this record recovered correctly from a
second truncation by preserving the original completion condition and
continuing contiguous reads until line 968/EOF was positively present.

## Recurrence control

The corrective behavior is:

1. Treat entry into a document carrying `Read in full` or `Read in full and
   follow` as full-document traversal rather than relevance search.
2. When a complete retrieval is truncated, preserve EOF as the original
   completion criterion.
3. Retrieve contiguous bounded ranges that fit the transport channel and keep
   reading regardless of whether the immediately relevant passage has already
   been found.
4. Do not rely on the document until EOF has been positively established in
   active context.
5. Treat a successful full-source API call as insufficient when a downstream
   tool, orchestration, or context boundary truncated the source before it
   reached active context.

The effectiveness test is a deliberately truncated required full-document
read in which relevant material appears before EOF. The control is effective
only if the agent continues contiguous retrieval through EOF before relying on
the document.

The successful replay during this record is one positive observation of that
test. A durable corrective action remains to encode the recovery rule in the
current authority or tooling that owns full-document entry, then repeat the
test under that control.

## Authority propagation

Current authority already establishes the underlying obligation in the root
`README.md`: a selected document's complete source must be identifiable in
active, non-compacted history before reliance.

Technical Writing also already states that targeted retrieval is not compliance
for a full-context directive in
<a href="../a.%20Document%20Design/c.%20Technical%20Writing/1.%20%F0%9F%9B%A0%EF%B8%8F%20Write%20A%20Technical%20Document.md#21-compose-the-routing-statement" uid="5CFFZW">documentation-system:§a.c.1#2.1</a>.

No new current-authority rule for truncation recovery is claimed by this Fault
Record. The open corrective action is to place the EOF-preserving recovery rule
in the controlled authority or tooling that owns full-document entry. This
record remains the evidence for why that control is needed.
