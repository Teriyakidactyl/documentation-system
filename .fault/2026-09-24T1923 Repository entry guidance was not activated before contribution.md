---
uid: FS44E8
form:
  path: '<a href="../e.%20Technical%20Writing/a.%20Document/b.%20Document%20Forms/c.%20Fault%20Record/README.md" uid="CD4R6P">documentation-system:§e.a.b.c</a>'
  version: '1.0'
description: >-
  `Read in full when` *the failure in which repository documentation was
  authored before root entry guidance was active needs review* `to`
  **reconstruct how passive repository guidance and harness discovery failed to
  establish the user-before-contributor route, distinguish the writing failure
  from the entry trigger, and evaluate recurrence controls without treating
  this record as current authority**.
quadrant: Explanation
fault:
  recorded-at: '2026-09-24T19:23:40-07:00'
  repository-revision: 33749394c42603b03c98764655270447b01807a5
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

# 💡 Repository entry guidance was not activated before contribution

## Expectation

At the repository revision identified by `fault.repository-revision`, the root
`README.md` required repository entry to begin with that literal file. It
defined progressive disclosure as the interaction model, required an arriving
reader to traverse the applicable `README.md` chain, and stated that a reader
modifying the repository is a user before becoming a contributor.

The same root guidance required selected documents whose complete source was
not identifiable in active, non-compacted conversation history to be read in
full before reliance.

The repository's root `SKILL.md` supplied an additional entry pointer:

~~~text
Begin with README.md.
~~~

The expected contribution path was therefore not to infer repository rules from
the target file or from prior conversation. The expected path was to activate
the repository entry guidance first, route the work from the root, establish the
applicable guidance chain, and only then modify controlled information.

The expectation did not require an arbitrary agent to discover every repository
file spontaneously. Some agent, skill, harness, or interaction control had to
cause the repository entry instruction to enter the agent's active context
before contribution began.

## Occurrence

Work on the open Tooling architecture branch proceeded from conversational
project context and direct repository targets. The agent inspected and modified
Software Design material without first reading the repository-root `README.md`
in full.

The first affected write was commit
`2c6cdf5609088413b5de5a17abd0bc1a6e693b9a`, which substantially rewrote
`6 Software Design/README.md`. Its parent,
`33749394c42603b03c98764655270447b01807a5`, already contained both the root
entry requirements and the root `SKILL.md` pointer.

A second Software Design README revision followed before the root entry document
had been read. When the user later asked whether the root `README.md` had been
read, the agent answered that it had not.

That omission was not itself the complete fault. The observable failure was
that technical documentation was authored before the repository's required
user-before-contributor route and applicable authoring guidance had been
established. The writing operation therefore proceeded without the governing
context that the repository requires before contribution.

After the root `README.md` was explicitly requested and read, the agent began
following progressive disclosure without further prompting: Document Control
routed the controlled sideband, Technical Writing routed document authoring,
Document Forms exposed the Fault Record Form, and Tooling exposed Organizing.
The contrast shows that the repository's routing works once its entry context is
active.

## Evidence

The interaction and repository state establish the failure and its boundary:

- before the affected writes, the repository root `README.md` already required
  entry through itself and required contributors to establish guidance before
  modifying the repository;
- the root `SKILL.md` already stated `Begin with README.md.`;
- the agent later stated explicitly that it had not read the repository-root
  `README.md` in the conversation before the user asked;
- commit `2c6cdf5609088413b5de5a17abd0bc1a6e693b9a` changed
  `6 Software Design/README.md` while the parent revision already contained
  the unconsumed root entry controls;
- after the user explicitly directed attention to the root `README.md`, the
  agent followed its routing model and independently discovered the Fault
  Record package and its required procedures;
- the repository root contained no `AGENTS.md` at the time this fault was
  analyzed; and
- in this interaction, repository files became available to the agent only when
  fetched through the GitHub connection. No observed platform behavior
  automatically placed `SKILL.md`, `README.md`, or another repository-root
  instruction file into active context.

The evidence supports a contribution-entry failure. It does not establish that
every sentence written before discovery was substantively incorrect, nor that
the root `README.md` itself was unclear once read.

## Causal analysis

The triggering condition was a request to change repository documentation. The
agent already had substantial conversational knowledge of the project and a
known target branch and file. That context made direct contribution appear
actionable without first reconstructing repository entry.

The failure mechanism was an unguarded transition from external task context
into contributor behavior. No active instruction in the chat or harness caused
the repository's own entry contract to be loaded before the first mutation.
The agent therefore treated known repository paths and prior conversation as
sufficient operating context.

The repository already contained two correct passive controls: `SKILL.md`
pointed to `README.md`, and `README.md` defined the user-before-contributor
route. Neither control was effective in this interaction because neither had
been activated. The problem was therefore not primarily absence of an entry
rule. It was absence of a reliable mechanism that makes the rule active for an
amnesiac agent before repository mutation.

Several conditions contributed:

- the agent had enough prior conversational context to feel oriented without
  repository entry;
- GitHub repository content was retrieved on demand rather than presented as an
  automatically entered workspace;
- the connected Documentation System skill was not active in the conversation,
  so its `SKILL.md` entry instruction did not govern the interaction;
- the target file was known before the repository's routing context was known,
  making target-first retrieval easier than root-first traversal; and
- the contribution path depended on the agent voluntarily remembering to
  inspect repository entry files despite the repository being designed for an
  amnesia agent.

A root `AGENTS.md` could change this outcome only under an execution
environment that treats that file as automatically discoverable governing
instruction. In such a harness, a thin root `AGENTS.md` directing the agent to
read and follow `README.md` would likely place the existing rule into active
context before contribution and could prevent this failure.

In the GitHub-connector interaction observed here, merely adding another passive
root file would not establish the same protection. If the platform does not
automatically retrieve `AGENTS.md`, that file would be subject to the same
discovery problem as `SKILL.md` and `README.md`.

The recurrence condition is therefore broader than filename choice. A
repository-entry rule must have an activation path appropriate to the agent
environment.

## Response and recovery

The user detected the missing entry context by asking whether the repository
root `README.md` had been read. The agent answered that it had not, then read
the file in full.

After entry was established, the agent followed the progressive-disclosure
model through the relevant Document Control, Technical Writing, Document Forms,
Fault Record, and Tooling locations. Required full-read procedures that had
previously been truncated were reread in bounded ranges through EOF before this
record was authored.

The existing Software Design README changes remain changes on the open branch;
this Fault Record does not retrospectively certify them merely because the
missing guidance was later loaded. They remain subject to the governing
authoring and repository controls now established in active context.

The immediate failed condition was recovered when repository work stopped
depending only on conversational context and began using the root
`README.md` as the entry authority.

## Recurrence control

The existing root guidance and `SKILL.md` pointer should remain because they
state the intended route correctly. The corrective problem is to make that
route reliably active before contribution.

Candidate controls are environment-specific entry adapters rather than another
independent source of repository rules:

1. A supported agent harness should automatically activate the Documentation
   System skill or an equivalent root instruction before allowing repository
   mutation.
2. When a harness automatically loads root `AGENTS.md`, that file can serve
   as a thin adapter that directs the agent to the canonical root `README.md`
   rather than duplicating repository guidance.
3. When no repository instruction convention is automatically loaded, the
   initiating chat or task prompt should explicitly require the agent to read
   and follow the root `README.md` before modifying the repository.
4. Harness installation or projection tooling should preserve one canonical
   entry rule and adapt discovery to each supported environment rather than
   copying the full Documentation System instructions into multiple root files.

Effectiveness must be tested per supported environment. Start a fresh agent with
no project conversation history, provide the repository and a request to modify
a descendant controlled document, and observe the interaction before the first
mutation. The control is effective only when the agent loads the root
`README.md`, establishes the applicable `README.md` chain, and selects the
governing concern-specific documents before changing the repository.

Repeat the test separately for skill-aware environments, environments that
automatically honor `AGENTS.md`, and chat or connector environments with no
automatic repository instruction discovery. Passing in one harness does not
establish protection in another.

## Authority propagation

Current authority already states the essential repository behavior. The root
`README.md` requires repository entry through itself and requires a user to
establish guidance before contributing. The root `SKILL.md` already directs a
skill consumer to begin with `README.md`.

This Fault Record therefore does not introduce a replacement root rule. The
open corrective action is to identify the owning agent-entry or harness
integration surface for each supported environment and encode the activation
mechanism there.

If `AGENTS.md` is adopted for a harness that automatically recognizes it, its
current-authority role should be limited to routing into the canonical
Documentation System entry rather than becoming a competing copy of the root
guidance. If chat prompting is required in environments without repository-file
auto-discovery, that requirement belongs in the mechanism that initiates those
sessions.

This record remains evidence for why passive presence of correct repository
guidance is insufficient when no active control causes an amnesiac agent to
encounter it before contribution.
