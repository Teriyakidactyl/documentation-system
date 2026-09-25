---
uid: HXHQ9T
form:
  path: '<a href="../2%20Technical%20Writing/3%20Document/1%20Document%20Forms/11%20Architecture%20Decision%20Record/README.md" uid="A1FANY">documentation-system:§2.3.1.11</a>'
  version: '1.0'
description: >-
  `Read in full when` *the rationale for separating domain-independent
  structural reasoning from document-specific and software-specific design,
  including workflow-derived document routing and placement, must be reviewed*
  `to` **understand the intended future design domains, their ownership
  boundaries, and the consequences for repository realignment without treating
  this decision record as current authority**.
quadrant: Explanation
decision:
  status: accepted
  decided-at: '2026-09-25T07:43:58-07:00'
  repository-revision: 215d608ec7ea0d3d5109655f90ffe67ce45d3536
  supersedes: []
  superseded-by:
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

# 💡 Why Structural Reasoning, Document Design, and Software Design Are Separate Design Domains

## Context

The Documentation System currently places several different kinds of design
reasoning beside one another at the repository root. Document Control governs
controlled documented information, Technical Writing governs authored
documents, Organizing Concepts supplies repository-agnostic structural
reasoning, Software Design supplies reusable software-design guidance, and
Tooling implements mechanical behavior. This arrangement worked while the
document navigation model was understood primarily as a classification tree
with one routing `description` per controlled artifact.

Work on the interaction model for amnesiac agents exposed a sharper problem.
The document filesystem is not merely storage. Folders, files, Folder READMEs,
generated Indexes, filenames, and routing metadata together form the interface
through which an agent with no reliable repository-specific state discovers
what work applies, acquires the context needed for that work, and acts.

The initial attempt to account for that interface treated workflow as another
possible decomposition strategy for the same folder tree. That creates an
ownership conflict. A physical folder or file has one physical parent, and one
sibling layer can faithfully encode one primary containment relation at a time.
A semantic decomposition, a workflow sequence, a code dependency structure,
and every other useful relationship therefore cannot all independently own the
same physical hierarchy.

The conflict became clearer after examining ordinary documentation work. A
documentation gap does not always imply a new document. A typical work
encounter may identify the gap, identify its domain, inspect existing
information, and then branch. If an existing document already owns the
information, the remaining work collapses to an edit. If no owner exists, new
structural-unit and placement decisions remain. If the apparent owner exposes a
structural contradiction, the work returns to the earliest contradicted
structural question. Repository state therefore determines which work remains;
a universal linear workflow is not executed merely because its stages exist.

This led to a second distinction. The larger workflow is valuable to the
*author* because tracing representative work reveals the states, branch
conditions, dependencies, and outcomes that must be supported. The consuming
agent does not necessarily need that whole workflow. It needs locally
discoverable jobs whose applicability can be recognized from the current state
and whose successful completion establishes a new observable state.

A routed document can therefore own more than one job-to-be-done. The document
is the reusable information or procedure; each job is a reason to enter it.
Conceptually, a job has an applicability condition, a required interaction, and
an observable result:

```text
precondition / exigence
        ↓
document-owned job / interaction
        ↓
postcondition / acceptance criterion
```

Those jobs form a capability-oriented state-transition system. Representative
workflows are plans through that system. The filesystem remains a containment
tree, while the work relationships form a graph. A README or Index can project
the locally available transitions onto the current tree location without
requiring the tree itself to encode every workflow.

This interpretation also clarifies the existing `description` field. Its
grammar already approximates a routing contract: the exigence identifies why
the route applies, the directive identifies the interaction, and the acceptance
criterion identifies what successful use enables. The current implementation
permits exactly one canonical `description` per controlled artifact. Early
Technical Writing guidance explicitly justified that scalar as reusable by
indexes, skills, and harness instructions. The current root `SKILL.md` now
carries its own harness-facing description and routes the harness into
`README.md`; the Harness Installer uses `SKILL.md#name` rather than requiring
every controlled document to remain directly skill-compatible. Corpus routing
metadata is therefore free to evolve according to the needs of the document
interface rather than the metadata constraints of an external skill surface.

The same workflow-discovery reasoning can inform software design, but the
physical consequence differs. A document filesystem is directly traversed as an
agent interface. A source-code filesystem is primarily an implementation and
maintainer representation; runtime dependencies, state ownership, public APIs,
deployment, failure isolation, performance, test seams, and change coupling can
outweigh workflow locality. Workflow discovery is therefore a general design
input, while folder-and-file-as-user-interface is specifically important to
document design.

These observations expose a boundary in Organizing Concepts. Determining stable
conceptual units, relationships, axes, ownership, containment, and convergence
is reusable across documents, code, schemas, and other artifacts. Selecting a
final physical representation is not. Document placement depends on
document-specific interaction and context forces. Software placement depends on
software-specific architectural forces. A domain-neutral discipline can
validate structural facts that a representation must preserve, but it cannot by
itself select every domain's final folders and files.

## Decision

Separate the architecture into three primary design domains:

```text
Structural Reasoning
Document Design
Software Design
```

Use **Structural Reasoning** as the future identity of the domain-independent
work currently centered in Organizing Concepts. Structural Reasoning owns the
discovery and validation of structural facts: stable units, relationships,
topologies and axes, semantic ownership, containment distinctions, convergence,
and structural consistency. It supplies constraints and evidence to
domain-specific design. It does not own the final physical representation of
documents, software, schemas, or other artifact domains merely because those
representations use folders and files.

Retain the substance of the current Organizing Concepts guidance that is truly
domain independent. In particular, determining structural units, determining
relationships and topologies, and distinguishing ownership, containment, and
convergence remain Structural Reasoning concerns. Reframe placement guidance so
the universal layer tests whether a proposed representation preserves
established units, relationships, ownership, and convergence. Move or rewrite
criteria that actually choose a physical document or software location according
to the domain-specific design force that owns that choice.

Establish **Document Design** as the design domain for documented information as
an interface for completing work. Document Design owns the document-specific
decomposition and representation decision, including:

- discovering representative workflows before finalizing the interface;
- identifying meaningful states, branch conditions, and state transitions;
- deriving reusable jobs-to-be-done from those workflows;
- assigning one or more jobs to coherent document units;
- using workflow and reasoning co-occurrence as evidence when deciding document
  boundaries;
- selecting document folder and file placement while preserving Structural
  Reasoning constraints;
- designing progressive disclosure, context locality, and context-closure
  behavior for amnesiac agents;
- designing Folder README and Index interaction surfaces;
- owning the routing semantics projected through document metadata; and
- validating that representative workflows can be completed through the
  published job surface without hidden dependencies or unnecessary context
  reconstruction.

Treat **Technical Writing**, **Document Control**, and reusable **Document
Forms/Elements** as concerns within Document Design rather than as peers of
domain-independent Structural Reasoning. Technical Writing owns how a selected
document unit communicates. Document Control owns durable identity, addresses,
controlled links, indexing mechanics, storage/control state, and maintenance of
the chosen representation. Document Forms and Elements own reusable document
representations. None of those mechanisms independently decides conceptual
structure merely because it stores, renders, or expresses the result.

A document's jobs are part of its agent-facing interaction contract. A document
may legitimately own multiple jobs when several distinct workflow states require
the same body of information or procedure. Do not force distinct jobs into one
over-general routing statement merely because they converge on one document.
Conversely, multiple apparent jobs that are only symptoms of one common forcing
condition may still be represented as one generalized job.

Treat the current single `description` as the existing prototype of that
routing contract, not as a permanent one-job cardinality rule. Future Document
Design work may replace or augment it with plural job metadata. The exact field
name, syntax, normalization model, and migration mechanism are downstream
implementation decisions and are not fixed by this ADR. The separate
harness-facing `SKILL.md` description remains free to summarize the whole
Documentation System for skill discovery.

Model larger workflows primarily as **design-time evidence**. Authors use them
to discover preconditions, outcomes, branches, joins, omitted states, and
co-occurrence. Consumers need not be shown a master workflow when local job
contracts and observable repository state are sufficient to determine the next
applicable action. A workflow may be retained as design provenance or current
design material when useful, but the runtime routing system should not require
the agent to remember a global step number when the repository can expose what
is now true and which jobs apply.

Understand the runtime interaction in these terms:

```text
current observable state
        ↓
locally exposed applicable job
        ↓
document supplies the required information or procedure
        ↓
new observable state
        ↓
route again if work remains
```

The larger workflow is therefore a plan over document-owned capabilities rather
than a second containment hierarchy. A job should prefer state-based
preconditions over explicit dependencies on another named job when either of
several operations could establish the required state. Explicit order or
dependency belongs in the model only when order itself is an invariant.

Keep **Software Design** as the domain that converts structural facts plus
software-specific forces into software representations. Software Design owns
software decomposition choices such as components, modules, packages,
interfaces, dependency direction, state boundaries, and other implementation
structure. Workflow discovery may contribute evidence, but it does not make the
source tree a direct analogue of the document navigation interface.

Treat the repository root as a **convergence site for artifact domains**, not as
evidence that one universal repository-layout procedure should determine every
domain's internal structure. Document Design determines document
representation. Software Design determines software representation. Other
artifact domains should likewise apply Structural Reasoning plus their own
domain forces rather than inherit document or software placement rules by
analogy.

Keep Tooling conceptually separate from these design domains. Tooling implements
and validates mechanisms selected by the design and control disciplines.
Implementation-specific architecture may remain code-local when that locality
is part of the Software Design model; generic software-design authority belongs
under Software Design rather than becoming Tooling guidance merely because the
implemented system is Tooling.

The intended future design relationship is:

```text
                        Structural Reasoning
                       /                    \
                      v                      v
             Document Design          Software Design
             /      |      \                |
            v       v       v               v
      Workflow/UI  Writing  Control    software structure
             \       |       /
              \      |      /
               document representation

Tooling implements and validates selected mechanisms.
```

This ADR records the architectural direction. It does not itself move folders,
rename Organizing Concepts, change `description` cardinality, or make the
future tree current authority. Those changes must be promoted into the
controlled artifacts that own the relevant rules.

## Rationale

The separation resolves the decomposition conflict by distinguishing
**structural truth** from **domain representation**. Semantic cohesion,
ownership, relationship, convergence, and similar facts can constrain many
representations. They do not uniquely determine one physical document tree or
one software module tree. Domain design combines those structural facts with the
forces unique to the artifact being designed.

For documents, workflow discovery is indispensable because the filesystem and
routing metadata are directly consumed as an interface. Tracing representative
work exposes the conditions under which information must be entered, which
information is needed together, where a decision eliminates later work, and
which outcomes permit the next action. Those observations are evidence for
document decomposition and routing, not a competing universal taxonomy.

Separating the design-time workflow from the runtime route also preserves
progressive disclosure. An amnesiac agent does not need the entire global
workflow in context before acting. It needs enough state recognition and
locally projected jobs to choose the next useful unit. Once a job completes,
the newly observable state can trigger fresh routing. The repository therefore
carries more of the workflow state in its observable facts and interface rather
than relying on the agent to preserve a remembered sequence.

This also explains why multiple jobs may converge on one document. A workflow
graph can have many incoming transitions to one capability, while the
filesystem gives the document one canonical location. Keeping those models
separate avoids duplicating documents merely to make different workflows look
tree-shaped and avoids distorting the canonical hierarchy to encode one
particular sequence.

The new boundary gives Document Control a clearer role. Durable identity,
controlled links, generated Indexes, sidebands, and validation are essential,
but they are control mechanisms over a chosen document architecture. Treating
those mechanisms as the owner of semantic placement confuses maintenance of a
representation with design of the representation.

The same boundary gives Technical Writing a clearer role. Writing quality,
document posture, outline, terminology, forms, and prose are decisions about how
a document communicates once its unit and jobs are understood. Technical
Writing can shape the artifact without having to serve as the universal owner
of the corpus hierarchy.

Renaming Organizing Concepts to Structural Reasoning communicates its narrower
and more durable responsibility. The value of the current material is not
reduced; the universal portions become easier to reuse because they no longer
need to imply that one generic placement procedure can choose every domain's
physical structure.

## Alternatives and consequences

**Keep Organizing Concepts as the universal owner of physical placement.** This
retains the present hierarchy but requires a domain-neutral process to choose
between representations whose quality depends on domain-specific forces. It
also makes document workflow/context criteria and software dependency/runtime
criteria compete inside one placement procedure. This alternative is rejected.

**Add UI Design beside Organizing Concepts and let both decompose the document
tree.** This recognizes the interaction problem but gives two disciplines
authority over the same physical output. The conflict is structural rather than
terminological. This alternative is rejected in favor of Structural Reasoning
supplying constraints and Document Design owning document representation.

**Make the document tree itself the workflow.** Stable workflow boundaries can
inform folder boundaries, but workflows branch, reconverge, share capabilities,
and vary by initial state. One document can participate in several workflows and
own several jobs. Encoding the workflow graph directly as the containment tree
would duplicate information or privilege one sequence over others. This
alternative is rejected.

**Retain exactly one routing description because every document should be a
skill.** A single generalized statement can hide multiple distinct jobs that
happen to require the same document. The current harness-facing `SKILL.md`
already provides a separate skill-discovery surface. This alternative is
rejected as an architectural constraint, while the present one-description
schema remains current implementation until separately changed.

**Create a universal Repository Layout discipline.** A repository contains
documents, source code, schemas, configuration, tests, evidence sidebands, and
other artifacts whose internal organization is governed by different forces.
The repository is a convergence site, not proof of one universal physical
decomposition. This alternative is rejected.

**Keep Document Control and Technical Writing as root peers of Structural
Reasoning indefinitely.** Their current concerns remain necessary, but they are
both specific to documented information. Keeping them at the same abstraction
level obscures the emerging Document Design domain and makes document placement
ownership harder to state. They should realign under Document Design as the
future authority is implemented.

The accepted consequence is a substantial repository realignment. Current
authority will need to be updated so the root routing surface names the new
design domains, Organizing Concepts is reframed as Structural Reasoning,
document-specific placement and workflow/UI guidance move into Document Design,
and existing Technical Writing, Document Control, Forms/Elements, and related
guidance are assigned clear subdomain ownership. Software Design must be
reviewed for software-specific decomposition authority, while generic
software-design rules presently attached to implementation tooling should be
moved or referenced from their proper owner.

The routing metadata model will also require separate design work. The likely
direction is a plural job surface that preserves the existing exigence /
directive / acceptance-criterion strengths while allowing one artifact to
advertise several distinct workflow affordances. Generated Indexes would then
project locally available jobs rather than assuming one route per child.
Organizing and validation would need to detect routing overlap and gaps at the
appropriate scope. This ADR intentionally leaves the exact schema open so that
the interaction contract is designed from representative workflows rather than
from the convenience of the current parser.

Finally, the migration must preserve the ADR/current-authority boundary. The
future architecture becomes binding only when the controlled documents that own
these rules are changed. This record preserves why that migration is required
and what conceptual shape those changes are intended to realize.
