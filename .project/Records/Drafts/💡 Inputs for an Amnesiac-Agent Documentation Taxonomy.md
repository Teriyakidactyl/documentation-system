---
description: >-
  `Read when` *investigating whether amnesiac agents have universal
  documentation needs analogous to Diátaxis and the derivation inputs are at
  risk of being collapsed into a premature taxonomy* `to` **preserve the
  active observations, candidate dimensions, incompatibility tests, and open
  hypotheses that should be stress-tested before any agent-facing content-type
  vocabulary becomes authority**.
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

# 💡 Inputs for an Amnesiac-Agent Documentation Taxonomy

> [!NOTE]
> This file is working information in `.project/Records/Drafts/`. It is not current
> Documentation System authority and does not establish a content taxonomy,
> glyph vocabulary, filename convention, or contributor convention.

## 1. Purpose

The current investigation is not trying to rename the four Diátaxis quadrants
for agents. It is trying to recover the kind of reasoning that made Diátaxis a
useful taxonomy in the first place, then repeat that reasoning under the
different constraints of amnesiac agents.

The desired result, if one exists, is a small set of universal document or
document-unit types derived from genuinely different agent needs. The types
should not be selected because their names sound useful or because existing
documents can be sorted into them. They should emerge because the agent
approaches information in measurably different situations and content optimized
for one situation becomes materially worse for another.

The possibility that no Diátaxis-like taxonomy exists for amnesiac agents
remains open. The investigation should be allowed to end with a grammar of
information interactions, a matrix of independent dimensions, or another model
if those explain the evidence better than a small set of document types.

## 2. Diátaxis as the methodological precedent

Diátaxis is useful here less as a four-name vocabulary than as an example of a
derivation.

Its four documentation kinds arise from two dimensions of a practitioner's
relationship to a skill:

- action versus cognition;
- acquisition versus application.

The resulting quadrants serve different user needs:

- Tutorial supports learning through guided practice.
- How-to supports accomplishing a goal while working.
- Explanation supports understanding.
- Reference supports looking up information while working.

The important observation for this investigation is that Diátaxis does not
merely classify subject matter. Its types imply different obligations for the
document. A tutorial optimized for guided acquisition is not simply a verbose
how-to. A reference optimized for lookup is not simply a compressed
explanation.

The relevant question is therefore not:

> What kinds of information do agents often need?

It is:

> Which relationships between an amnesiac agent and information create
> incompatible requirements for a bounded document unit?

That incompatibility is the main admission test for a candidate universal
content type.

## 3. Amnesiac-agent constraints

The Documentation System treats an arriving agent as potentially amnesiac.
Repository-specific competence available in one encounter cannot be presumed to
persist into another.

This changes the Diátaxis problem.

A human practitioner can acquire durable competence and later apply it. An
amnesiac agent can act competently while the required information is in active
context and then lose that effective competence when the context is absent.
The same nominal agent therefore arrives repeatedly without a reliable
longitudinal learning state.

The existing working note
`.user/2026-09-25T0533 Diátaxis Is A Partial Fit For Amnesiac Agents.md`
already records two useful consequences:

- action versus cognition still appears meaningful;
- acquisition versus application remains informative locally but cannot by
  itself model the reconstruction of active context across encounters.

The investigation should preserve those findings rather than assuming that
either the whole Diátaxis model transfers or that none of it does.

## 4. Structural constraints on the investigation

The repository's current structural guidance supplies several constraints on
how candidate taxonomies should be evaluated.

A candidate category should correspond to a stable difference in meaning,
invariants, work context, or downstream reasoning. Existing files, folders, or
glyphs are evidence about the current representation, not authority for the
conceptual boundary.

Independent dimensions should remain independent. One classificatory layer
should answer one organizing question. When two attributes can combine freely,
their Cartesian product should not be forced into one hierarchy merely because
a tree is convenient.

Semantic ownership, physical containment, and interaction convergence are also
separate. Two needs may occur in one workflow or one file without becoming one
content type. Conversely, one document can contain several independently
meaningful document units when delivery constraints require convergence.

These constraints make a matrix of candidate axes the appropriate working
representation until stronger evidence justifies a smaller taxonomy.

## 5. Incompatibility as the primary fracture test

A distinction becomes interesting as a content-type boundary when optimizing
for one side predictably harms the other side.

Useful probes include:

- Does one need require preserving alternatives while the other requires
  suppressing them?
- Does one need require observation before mutation while the other requires
  mutation?
- Does one need require dense random access while the other requires ordered
  reasoning?
- Does one need require establishing uncertainty while the other assumes the
  relevant uncertainty is already resolved?
- Do the two needs demand different heading structures, ordering rules,
  density, branching, examples, or acceptance criteria?
- Can a reader safely enter the middle of one representation while the other
  requires a dependency sequence?
- Would mixing the two needs cause an amnesiac agent to act before a condition
  is established, reopen a settled question, mistake an alternative for
  authority, or consume unnecessary context?

A mere semantic distinction is not enough. Descriptive and normative
information, for example, can often coexist without the document fighting
itself. The investigation should prefer fractures that create conflicting
interaction requirements.

## 6. Present-state and target-state certainty

One current hypothesis starts from two questions that can vary independently
for the same agent:

1. Is the present state sufficiently recognized?
2. Is the desired state sufficiently specified?

Their cross-product produces four candidate need states:

| | Desired state known | Desired state unresolved |
|---|---|---|
| **Present state known** | Execute | Decide or design |
| **Present state unresolved** | Diagnose | Investigate or frame |

These are provisional names. Their value lies in the different content
obligations they predict.

### 6.1 Execute

The agent knows where the work is and where it must go.

Useful content tends toward:

- prerequisites;
- one selected path or explicit operational branches;
- concrete actions;
- invariants that must survive the change;
- postconditions and acceptance criteria.

Unnecessary reopening of alternatives makes execution worse.

### 6.2 Decide or design

The current state is sufficiently understood, but the appropriate target state
has not yet been selected.

Useful content tends toward:

- candidate alternatives;
- discriminating criteria;
- constraints;
- trade-offs and consequences;
- decision rules;
- explicit stopping conditions for when the question is resolved.

Presenting one arbitrary procedure as though the choice were already settled
makes this interaction unsafe.

### 6.3 Diagnose

The acceptable target state is known, but the present condition or cause of the
difference is unresolved.

Useful content tends toward:

- symptoms and observations;
- discriminating checks;
- hypothesis elimination;
- evidence preservation;
- minimal or reversible probes;
- criteria for declaring the present state sufficiently understood.

Premature remediation can destroy evidence or commit to an unestablished
cause.

### 6.4 Investigate or frame

Neither the present condition nor the appropriate target state is sufficiently
understood.

Useful content tends toward:

- problem bounding;
- evidence acquisition;
- hypothesis formation;
- vocabulary and model establishment;
- discovery of relevant constraints;
- criteria for deciding which question has become sufficiently specified to
  route into diagnosis, decision, or execution.

A narrow execution procedure is especially hazardous here because it can turn
an unstated assumption into an action.

## 7. Resolve versus execute

A particularly strong candidate fracture appears between determining what
should be done and carrying out something already determined.

Resolution needs information that keeps meaningful alternatives visible long
enough to distinguish them. It benefits from discriminators, counterexamples,
trade-offs, constraint interaction, and explicit evidence.

Execution needs information that minimizes unnecessary choice after the
relevant decision has already been made. It benefits from a narrow path,
preconditions, concrete actions, invariant preservation, and checkable
postconditions.

Optimizing for resolution can burden execution with irrelevant alternatives.
Optimizing for execution can hide unresolved choices and cause one candidate
answer to masquerade as authority.

The current
`5 Organizing Concepts/1 🛠️ Determine Structural Units.md`
is a useful pressure case. Although currently classified as HowTo, its central
job is not to replay a stored answer. It gives an agent a reasoning system for
deriving a defensible structural answer from the facts of the present case.

## 8. Diagnose versus remediate

Diagnosis and remediation may impose directly opposed behavioral obligations.

Diagnosis often requires the agent to avoid changing the state until evidence
has been gathered and competing causes have been distinguished. The
interaction may prioritize observation, evidence preservation, minimal probes,
and uncertainty reduction.

Remediation assumes enough of the relevant state has been established to
justify mutation. It prioritizes the selected repair, protection of required
invariants, and confirmation of the resulting state.

A combined troubleshooting artifact can legitimately contain both phases, but
the boundary between them may still be a document-unit boundary. An amnesiac
agent should be able to recognize when it has left evidence gathering and is
authorized to mutate the system.

## 9. Retrieve versus resolve

Another candidate fracture concerns whether the answer already exists as
information to be found or must be derived for the present case.

Retrieval benefits from:

- stable keys;
- predictable decomposition;
- dense entries;
- independent lookup;
- minimal narrative;
- direct authoritative statements.

Resolution benefits from:

- ordered reasoning;
- discriminators;
- dependency exposure;
- examples and counterexamples;
- evidence interpretation;
- explicit stopping criteria.

A reference optimized for direct retrieval is often poor at carrying the
reasoning required to derive a case-specific answer. A reasoning sequence is
often poor when the agent already holds the lookup key and needs one value.

This distinction may be independent, or resolution may prove to be a
superordinate need containing diagnosis, decision, design, and other forms of
case-specific inference. That relationship remains unresolved.

## 10. Action versus cognition

The Diátaxis action-versus-cognition dimension remains in the experiment.

For an amnesiac agent, the discriminator should probably be the required
outcome rather than whether the surface activity looks like reasoning.

A candidate interpretation is:

```text
action
    success is an external task-state change or a decision that enables one

cognition
    success is an adequate model or understanding without a required
    task-state transition
```

An agent can reason extensively while still occupying the action side when the
acceptance criterion is a decision or artifact change.

The repository's current routing grammar is useful evidence here because each
`description` already attempts to pair an exigence with an observable
acceptance criterion.

## 11. Semantic dimensions that may not be reader-need fractures

Several dimensions remain useful for describing information without yet
showing the incompatibility required for a content taxonomy.

### 11.1 Descriptive versus normative

```text
descriptive
    what is, exists, happens, or follows

normative
    what must, should, may, or must not be true or done
```

This distinction can affect correctness criteria but does not necessarily
force separate documents. Architecture, policy, and procedures can contain
both when one coherent interaction requires them together.

### 11.2 State versus transition

```text
state
    condition, structure, value, relationship, invariant

transition
    change, behavior, propagation, transformation
```

This dimension is useful for modeling what information refers to, but state and
transition can often be needed in the same reasoning encounter.

### 11.3 Descriptive or normative crossed with state or transition

The cross-product remains a useful semantic map:

| | State | Transition |
|---|---|---|
| **Descriptive** | what exists or is true | what happens or changes |
| **Normative** | what must remain or be true | what must be done or changed |

The four cells may predict different correctness obligations without
necessarily constituting four incompatible reader postures.

## 12. Establish context versus operate from context

A possible amnesiac-agent replacement for human acquisition versus application
is:

```text
establish active context
        ↔
operate from established active context
```

This hypothesis fits progressive disclosure. A README chain, local glossary,
routing surface, and selected governing documents reconstruct enough active
knowledge for correct work.

The hypothesis has a serious possible failure: every document interaction
establishes some active context. If the distinction cannot be made without
arbitrary thresholds, it may describe the routing protocol rather than a
content-type axis.

The investigation should try to falsify this dimension rather than assume that
an agent-native replacement for acquisition versus application must exist.

## 13. Audience role is probably orthogonal

Consumer versus contributor appears to answer a different question from the
content-type investigation.

A consumer can need retrieval, resolution, diagnosis, execution, explanation,
or other interactions. A contributor can need the same interactions.

Changing audience role changes which information surface should be exposed, but
does not necessarily change the logical function of the information once
selected.

A useful working distinction is therefore:

```text
audience / interaction role
    consumer
    contributor

content relationship
    independently classified
```

This is why a contributor glyph can plausibly be a filename or projection cue
without becoming a replacement for a content-type glyph.

## 14. Reliance status is probably orthogonal

The repository already distinguishes:

- current authority;
- working information;
- evidence and provenance;
- historical or cold information.

These roles produce a genuine interaction hazard. Material used to understand
why a decision was made can contain rejected alternatives and superseded facts
that must not be mistaken for current operating authority.

That is an important incompatibility, but it may belong to a reliance and
retrieval dimension rather than the universal content taxonomy.

The key separation is:

```text
What kind of information interaction is this?
        ≠
May this information be relied on as current authority?
```

The present file is itself an example: it is Explanation-shaped working
information, not current authority.

## 15. Routing may be a control plane rather than a content type

Scope, authority, applicability, exigence, and acceptance criteria repeatedly
appear around all candidate content types.

That suggests they may not form another peer content category. They may form a
control layer that lets an amnesiac agent decide which content interaction to
enter.

A provisional interaction shape is:

```text
observable current state
        ↓
recognize applicable exigence
        ↓
select locally exposed interaction
        ↓
consume the information or procedure
        ↓
satisfy an observable acceptance criterion
        ↓
new observable state
        ↓
route again if work remains
```

The exact routing metadata remains a separate design problem. The important
point for the taxonomy investigation is to avoid classifying the control plane
and its payload under one axis merely because both are represented in a
document.

## 16. Current candidate map

The active candidate dimensions can be summarized without yet choosing a
hierarchy:

| Dimension | Candidate values | Current status |
|---|---|---|
| Engagement | action / cognition | Strong inherited candidate |
| Present-state certainty | recognized / unresolved | Strong agent-specific candidate |
| Target-state certainty | specified / unresolved | Strong agent-specific candidate |
| Answer formation | retrieve / resolve | Strong candidate fracture |
| Interaction phase | diagnose / remediate | Strong candidate fracture, perhaps derived |
| Choice state | decide / execute | Strong candidate fracture, perhaps derived |
| Modality | descriptive / normative | Useful semantic dimension, fracture unproven |
| Object | state / transition | Useful semantic dimension, fracture unproven |
| Context relation | establish / operate-from | Open hypothesis |
| Audience role | consumer / contributor | Likely orthogonal exposure dimension |
| Reliance status | authority / working / evidence / history | Likely orthogonal control dimension |
| Routing relation | control / payload | Likely protocol layering rather than taxonomy |

## 17. Stress-test method

The next investigation should use actual agent-document encounters rather than
classifying existing document titles.

For each encounter:

1. State the observable situation before routing.
2. State what the agent knows about the present state.
3. State what the agent knows about the desired state.
4. State the acceptance criterion that would dissolve the exigence.
5. Determine whether the needed answer is retrieved or derived.
6. Determine whether success is primarily action or cognition.
7. Record descriptive, normative, state, and transition characteristics without
   assuming they are content-type boundaries.
8. Ask what document shape optimally satisfies the need.
9. Pair the encounter with nearby need states and test whether combining them
   forces conflicting structure or behavior.
10. Treat empty cells, forced exceptions, and correlated dimensions as evidence
    against the candidate model rather than repairing the examples to preserve
    it.

The test set should cross domains. Repository organization, software design,
document control, editing, architecture, troubleshooting, research, and
unrelated operational domains should all be able to challenge the same
candidate dimensions.

A universal taxonomy should survive changes in subject, agent instance,
repository, and audience role.

## 18. Evidence that a content fracture is real

A candidate split becomes stronger when it repeatedly predicts different
requirements for:

- entry conditions;
- acceptance criteria;
- heading topology;
- ordering;
- branching;
- information density;
- use of alternatives;
- use of examples and counterexamples;
- permission to mutate the subject;
- evidence preservation;
- random access versus dependency sequence;
- stopping conditions;
- failure modes when the wrong content shape is supplied.

The strongest evidence is a predictable failure caused by the wrong
interaction shape.

Examples currently hypothesized include:

- an investigating agent given execution guidance acts on an unstated
  assumption;
- an executing agent given decision material unnecessarily reopens a settled
  question;
- a diagnosing agent given remediation instructions mutates evidence before a
  cause is established;
- a deciding agent given one prescriptive procedure mistakes one candidate
  answer for the selected answer;
- an agent needing retrieval is forced through a reasoning sequence to obtain a
  known value;
- an agent needing resolution receives isolated facts without the
  discriminators required to derive an answer.

## 19. Questions still open

The investigation has not yet established:

- whether present-state certainty and target-state certainty are truly
  independent axes across domains;
- whether Execute, Diagnose, Decide, and Investigate are universal content
  types, workflow states, or only useful labels for a larger state-transition
  model;
- whether retrieve versus resolve is independent of that matrix or explains
  much of it;
- whether diagnose versus remediate should be a top-level fracture or a
  specialization of unresolved-present versus resolved-present work;
- whether decision and design are one need state or two;
- whether action versus cognition remains an independent dimension after the
  state-certainty model is applied;
- whether establishing active context is a genuine content relationship or
  only part of the progressive-disclosure control plane;
- whether current authority versus provenance/history belongs in the same
  taxonomy or exclusively in information-role and retrieval policy;
- whether a small closed taxonomy exists at all.

The investigation should resist naming permanent glyphs until these questions
have been attacked with enough heterogeneous encounters to expose collisions,
gaps, and false axes.

## 20. Open questions for external discussion

This section turns the working model above into a common investigation contract
for independent agents. The goal is not to obtain agreement with the current
hypotheses. The goal is to expose which observations survive independent
reasoning, which candidate axes collapse, and whether any stable taxonomy of
incompatible agent needs actually emerges.

### 20.1 Research assignment

Investigate whether amnesiac agents exhibit a small set of universal
documentation needs analogous in derivation to Diátaxis.

Treat the supplied matrices, labels, and candidate fractures as hypotheses to
challenge, not as a taxonomy to complete. Begin from the agent's relationship
to information at the moment of use. Look for needs whose optimal document
shapes are incompatible enough that serving them in one bounded document unit
predictably makes at least one need worse.

A useful result may be:

- a small closed taxonomy;
- a set of independent dimensions whose combinations matter more than named
  types;
- a state-transition or interaction grammar;
- a demonstration that some proposed axes are derived from others;
- or evidence that no universal taxonomy comparable to Diátaxis exists for
  amnesiac agents.

Do not preserve a four-cell structure merely because Diátaxis has four
quadrants or because the present-state and target-state hypothesis happens to
form a two-by-two matrix.

### 20.2 Falsification targets

Actively look for evidence against the current model.

Test whether:

- present-state certainty and target-state certainty are actually independent;
- supposedly different need states can be served well by one homogeneous
  document unit without structural tension;
- apparently independent axes are strongly correlated and therefore describe
  one underlying distinction;
- some combinations are impossible, incoherent, or only artifacts of the
  vocabulary used to name them;
- retrieve versus resolve explains the present-state and target-state matrix,
  or vice versa;
- diagnose versus remediate is a genuine content fracture rather than an
  ordinary sequence within one interaction;
- decide, design, investigate, and frame are distinct needs or merely
  variations in unresolved state;
- action versus cognition still predicts incompatible content obligations once
  other agent-specific dimensions are controlled;
- establish-context versus operate-from-context can be distinguished without an
  arbitrary threshold;
- reliance status or audience role has been mistaken for content type;
- routing/control information has been mistaken for payload content;
- a missing need produces a stronger and more general incompatibility than any
  current candidate.

When a counterexample appears, prefer revising or rejecting the candidate model
over redefining the example until it fits.

### 20.3 Required return shape

For comparison across independent discussions, return findings under the
following headings:

1. **Accepted observations** — claims in this draft that survive scrutiny.
2. **Disputed observations** — claims that are unsupported, overgeneralized, or
   framed incorrectly.
3. **Candidate fundamental dimensions** — proposed independent axes, including
   the relation each axis classifies.
4. **Strongest incompatible-needs fractures** — pairs or sets of needs where
   optimizing for one predictably damages another.
5. **Counterexamples** — concrete encounters that break or blur the proposed
   distinctions.
6. **Derived relationships** — candidate needs or axes that appear to be
   specializations, workflow phases, or consequences of something more
   fundamental.
7. **Proposed model** — a taxonomy, matrix, graph, interaction grammar, or other
   structure only if the evidence supports one.
8. **No-taxonomy case** — if no stable universal taxonomy is found, state what
   model better explains the evidence.
9. **Unresolved tests** — the smallest additional experiments or encounter sets
   that would discriminate between remaining hypotheses.

Prefer concrete agent-document encounters over abstract agreement with labels.

### 20.4 Minimal vocabulary

Use these terms consistently during the investigation.

**Amnesia agent.** An agent whose repository-specific knowledge available in
one encounter cannot be presumed to persist into another. The relevant
competence is what is present in active context now.

**Exigence.** The pressure or condition that exists before a document
interaction and makes that interaction applicable.

**Acceptance criterion.** The minimum observable action, decision,
understanding-in-order-to-act, or state change that dissolves the exigence.

**Progressive disclosure.** Navigation in which only the context and immediate
choices needed for the current decision are exposed, with deeper information
loaded only when routing requires it.

**Current authority.** Information that may be relied on when acting now.

**Working information.** Mutable planning, investigation, or design material
used to produce another result and not automatically current authority.

**Content-type fracture.** A boundary between needs where optimizing a bounded
document unit for one need predictably degrades its ability to serve the other.

**Workflow state.** A condition of the work or agent-task relationship at some
point in a larger process. A workflow state is not automatically a document
type.

**Document unit.** A bounded body of information that can be reasoned about as
one interaction contract even when several such units must share one physical
file.

### 20.5 Primary Diátaxis material

Do not rely only on this draft's characterization of Diátaxis. Read the
framework's own account of its derivation and user-needs model before comparing
it with amnesiac-agent needs:

- Foundations: <https://diataxis.fr/foundations/>
- Map: <https://diataxis.fr/map/>
- Compass: <https://diataxis.fr/compass/>

Use those sources to distinguish Diátaxis's underlying dimensions and user
relationships from the familiar four document labels. The purpose of the
comparison is to imitate the quality of the derivation, not to preserve its
surface structure.

### 20.6 Workflow state versus document type

This is the most important open question in the present model.

The labels Execute, Diagnose, Decide, and Investigate may describe work states
accurately without implying four universal kinds of documents. A useful
workflow decomposition is not sufficient evidence for a content taxonomy.

For every candidate need state, prove the additional step:

> Does this need impose a distinctive enough set of content obligations that
> combining it with another need in one bounded document unit predictably
> damages at least one interaction?

Test this through observable representation consequences such as:

- required entry information;
- whether alternatives must be preserved or suppressed;
- whether mutation is permitted;
- whether evidence must be preserved;
- random access versus ordered dependency;
- heading topology;
- branching shape;
- information density;
- examples and counterexamples;
- stopping conditions;
- acceptance criteria;
- and predictable failures when the wrong shape is supplied.

If two workflow states require materially the same document shape, they should
not become separate content types merely because they occur at different points
in a process.

If one workflow state can require several incompatible document shapes
depending on another independent dimension, the workflow state is likewise
insufficient as the taxonomy axis.

### 20.7 Universality standard

A candidate taxonomy should survive changes in subject, repository, agent
instance, and audience role.

Pressure-test it against at least:

- software implementation and architecture;
- document design and editing;
- troubleshooting and recovery;
- research and evidence evaluation;
- configuration and operations;
- planning and design decisions;
- lookup-heavy technical reference;
- and domains unrelated to repositories or software.

A distinction that exists only because of one repository's control model may
still be valuable locally, but it is not the sought universal analogue.

### 20.8 External-agent independence

Independent agents should be encouraged to introduce alternative axes and
models before reconciling with the candidates in this draft.

Agreement among agents is weak evidence when they all inherit the same framing.
Stronger evidence comes from independently derived models converging on the
same fracture, or from a candidate surviving attempts to replace it with a
simpler explanation.

When synthesizing several external discussions, preserve minority
counterexamples and incompatible models long enough to determine what
observation causes the disagreement. Do not reduce the outputs to a vote.

