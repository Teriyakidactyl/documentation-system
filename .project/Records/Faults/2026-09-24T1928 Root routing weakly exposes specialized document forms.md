---
uid: FDNZFS
form:
  path: '<a href="../a.%20Document%20Design/a.%20Assemblies/b.%20Forms/c.%20Records/a.%20Fault%20Record/README.md" uid="CD4R6P">documentation-system:§a.a.b.c.a</a>'
  version: '1.0'
description: >-
  `Read in full when` *the weak root-level discoverability of specialized
  Document Forms and their task-specific functions needs review* `to`
  **reconstruct how progressive routing requires a reader to classify work as
  generic technical authoring before specialized roles such as Fault Record
  become visible, and evaluate stronger routing without treating this record
  as current authority**.
quadrant: Explanation
fault:
  recorded-at: '2026-09-24T19:28:30-07:00'
  repository-revision: 6f113ca681ef4595166f8dd644f74e38bd73c3cd
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

# 💡 Root routing weakly exposes specialized document forms

## Expectation

Progressive disclosure should let an amnesia agent begin with the work it
recognizes and reach the narrowest governing procedure without already knowing
the repository's internal information architecture.

The root `README.md` defines that interaction model. It tells the reader to
compare immediate Index choices, select the narrowest matching
`description`, enter that child's `README.md`, and continue until the
applicable concern-specific guidance is reached.

Document Forms exist specifically to govern recurring document roles. The
current Form catalog includes specialized packages for Research, Architecture
Decision Records, Fault Records, and Architecture Documents. Their individual
descriptions express recognizable task-level situations such as retaining an
observed failure, preserving an architectural decision, or authoring durable
architecture.

A reader whose task is "record this fault" should therefore be able to enter at
the root and reach the Fault Record procedure from the task's observable
purpose, without first having to know that fault recording is classified under
Technical Writing, then Document, then Document Forms.

## Occurrence

While recording a fault about repository-entry behavior, the agent successfully
followed the root progressive-disclosure model after the root `README.md` had
been activated.

The route was:

~~~text
README.md
→ Technical Writing/README.md
→ Document/README.md
→ Document Forms/README.md
→ Fault Record/README.md
→ Record A Fault
~~~

The route worked, but the specialized function did not become explicit until
four routing levels below the repository root.

At the root, the relevant immediate choice was only:

~~~text
Technical Writing
  technical documented information must be authored
~~~

The root's one-hop orientation hints exposed
`3 Document/README.md`, but not the specialized Form roles beneath it.
`.fault` itself is intentionally excluded from normal index navigation, so
its physical presence cannot supply the missing task-level routing cue.

The user had already named the desired operation as "record a fault." That
external wording supplied the semantic classification needed to keep descending
until the Fault Record Form appeared. The repository route did not expose
"observed failure should be retained" or an equivalent fault-specific trigger
near the entry surface.

The same structural condition applies to other specialized Forms. A reader may
arrive wanting to preserve an architectural decision, retain a research run, or
write the architecture governing a live implementation, while the root exposes
only the broader category of technical-document authoring.

## Evidence

Repository structure at `fault.repository-revision` establishes the routing
depth and information available at each step:

- the root `README.md` exposes **Technical Writing** as the immediate
  authoring route;
- the root's orientation hints under Technical Writing list
  `Write A Technical Document`, `Routable Descriptions Recognized`, and
  `Document/README.md`, but do not expose individual Document Forms;
- `Technical Writing/README.md` exposes **Document** only after the reader has
  already selected Technical Writing;
- `Document/README.md` exposes **Document Forms**;
- `Document Forms/README.md` is the first routing surface that names the
  specialized roles Research, Architecture Decision Record, Fault Record, and
  Architecture Document;
- `Fault Record/README.md` is the first location whose route directly matches
  the work encounter "an observed failure should be retained"; and
- Folder Conventions intentionally keeps `.fault` outside ordinary agent
  navigation, so browsing the sideband is not intended to compensate for the
  routing depth.

The interaction supplies a second observation. Once the agent knew the task was
fault recording and entered Technical Writing, it independently discovered
Document Forms and the Fault Record package without further user instruction.
This shows that the lower routing chain functions. The weakness is the
transition from a concrete work encounter to the broad root category that owns
the specialized Form.

## Causal analysis

The trigger is a reader arriving with a specialized documentation job stated in
domain language, such as "record this fault."

The failure mechanism is semantic compression at the root routing boundary.
Several distinct recurring document functions are represented by one broad
Technical Writing route whose exigence is simply that technical documented
information must be authored.

That abstraction is accurate but weak as a selector for readers who do not yet
know the Documentation System's classification. To follow it confidently, the
reader must infer that recording a fault is first and foremost "authoring
technical documented information." Only after making that inference can the
progressive route expose the more specific Fault Record description that
directly matches the task.

Several conditions contribute:

- specialized Document Forms are four README transitions below the root;
- root one-hop hints stop at `Document/README.md` and therefore provide no
  task vocabulary for the Forms beneath it;
- the specialized Forms represent semantically different work encounters even
  though they share an authoring mechanism;
- controlled sidebands such as `.fault` are intentionally absent from normal
  index navigation;
- progressive disclosure minimizes early context, which increases the
  importance of each immediate description carrying enough vocabulary to let
  an amnesia agent recognize the next route; and
- current routing optimizes for repository taxonomy more strongly than for some
  task-level entry phrases.

The observed route does not show that progressive disclosure itself is wrong.
Once the reader entered the correct branch, progressive disclosure worked as
designed and prevented unrelated Form details from entering context.

The weakness is therefore not excessive depth by itself. It is that the higher
levels do not provide a strong enough semantic bridge from specialized user
intent to the branch containing the specialized Form.

Fault recording makes the problem especially visible because the physical
`.fault` store is deliberately non-routable. The Form route is the intended
way to learn how to create a fault record, so weakness in that route cannot be
offset by ordinary filesystem discovery.

## Response and recovery

The user explicitly named fault recording, which allowed the agent to retain
that task concept while traversing the broader Technical Writing hierarchy.

After entering Technical Writing, the agent selected Document, then Document
Forms, discovered the Fault Record package, and read its Reference and HowTo.
No manual path guess was needed once the Form catalog became visible.

The immediate task was therefore recoverable, and the existing routing chain
was sufficient for an agent that persisted through the hierarchy with the
specialized intent already in mind.

No current routing rule is changed by this Fault Record.

## Recurrence control

A corrective control should preserve progressive disclosure while improving the
semantic bridge between root-level work encounters and specialized Document
Forms.

The control should not flatten every Form into the root Index or duplicate Form
instructions at repository entry. Either response would undermine the
repository's own context-minimization model.

Candidate mechanisms include:

1. strengthen the root Technical Writing routing description so its selecting
   condition explicitly includes creating a document with a recognized
   recurring role, not only generic technical authoring;
2. strengthen the Technical Writing or Document routing surfaces with compact
   task-level cues that make specialized Forms discoverable before the reader
   already knows the term "Document Form";
3. provide a controlled task-to-route mechanism that can map recognizable work
   encounters such as "record a fault," "record an architectural decision,"
   "retain research," and "write the live architecture specification" to their
   owning Form package without loading unrelated Form content; or
4. allow a harness or skill entry surface to preserve these specialized trigger
   phrases as routing aliases while keeping the canonical procedures in their
   existing locations.

The effectiveness test starts a fresh amnesia agent at the repository root with
only one specialized task phrased in ordinary work language. Examples include:

~~~text
record this fault
preserve why this architecture decision was made
retain this research run
write the architecture specification for this subsystem
~~~

The control is effective when the agent reaches the correct Form package through
the documented progressive-disclosure path without path guessing, repository
search, prior knowledge of the Form taxonomy, or a user having to translate the
task into "Technical Writing."

The test should also confirm that unrelated Forms remain undisclosed until
selected. Improving task recognition should not collapse progressive
disclosure into a root-level catalog of every specialized artifact.

## Authority propagation

Current authority already defines progressive disclosure, Document Forms, and
the specialized Fault Record procedure. This record does not replace those
rules.

The open corrective action belongs to the routing authority that determines how
an entering reader maps recognizable work encounters to the repository's
immediate choices. Any change should keep the specialized Form package as the
owner of its document contract and assembly procedure.

For Fault Records specifically, `.fault` should remain a controlled sideband
unless a separate Document Control decision changes that storage policy.
Discoverability of the action "record a fault" should be solved by routing to
the Fault Record Form, not by making historical fault evidence part of ordinary
navigation.

This record remains evidence that a lower-level route can be correct and still
be weak at its entry boundary when the reader must already know the repository's
classification before the route becomes recognizable.
