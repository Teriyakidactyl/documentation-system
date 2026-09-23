---
uid: 5CFFZW
description: >-
  `Read in full and follow when` *authoring or substantially revising a technical
  document* `to` **commit its description, controlled placement, quadrant,
  outline, and writing style before drafting prose that satisfies them**.
---

# 🛠️ Write A Technical Document
<!--
quadrant: HowTo
outline:
  topology: linear
  numbering: hierarchical-decimal
writing-style:
  formality: professional
  tone: neutral/detached
  mode: imperative
  density: moderate
  abstraction: concrete/specific
  redundancy: zero
  signposting: light
  register: technical
-->

Work the seven steps in order; each constrains the next. Quadrant Reference
below carries every per-quadrant value they call for, plus the one format
all four quadrants share.

**Terms.** One name per concept, used throughout. The three description
primitives also project their semantic role through Markdown formatting:

```text
description
├── `directive`
├── *exigence*
└── **acceptance criterion**
```

| Term | Meaning |
|---|---|
| **specification** | The record of what a document commits to, kept in frontmatter or metamatter. Never the document itself. |
| **frontmatter** | YAML fenced by `---` at the top of a file. Governs the whole file. |
| **metamatter** | Structured YAML data inside an HTML comment whose first non-whitespace content is a data key (`key:`). Position supplies its scope; the key supplies its meaning. |
| **ordinary HTML comment** | An HTML comment whose first non-whitespace content is not a YAML data key. It carries freeform maintenance or tool-control information, not structured metamatter or reader-required topic content. |
| **description** | One imperative Markdown routing statement composed from a `directive`, *exigence*, and **acceptance criterion**. The exact scalar is reusable by indexes, skills, and harness instructions. |
| **form** | An optional file-level controlled link from a derived document to the Standard Form governing its recurring repository role. |
| **element** | A position-scoped controlled link in metamatter from a reusable document section to the Document Element governing its source structure. |
| `directive` | The imperative phrase that specifies what the document user must do with the information and how deeply they must interact with it. |
| *exigence* | The pressure that exists before the document does, and would exist without it. |
| **acceptance criterion** | The observable thing successful use enables the reader to do, decide, or understand in order to act. |
| **quadrant** | Exactly one of Tutorial, HowTo, Explanation, Reference. |
| **quadrant glyph** | The emoji standing for a quadrant: 🧭 🛠️ 💡 📖. |
| **heading structure** | How a quadrant requires its headings to arrange. Each quadrant's entry states one. |
| **heading axis** | The single question every heading at one level answers. Held in `outline.axis`. |
| **heading topology** | The shape the headings form. A HowTo picks linear, branching, or fan-in. A Reference picks tree, matrix, graph, or list. Held in `outline.topology`. |
| **HTIL gate** | A stop requiring human sign-off. Not a slow-down. |

## 1. Open the specification

A *specification* records what a document commits to. It is not the document
and does not contain it: `outline` declares the shape the headings take,
while the headings themselves live in the document.

### 1.1 Know the keys

Every key a specification can carry, with the step that binds each:

```yaml
description: >-              # bound at step 2.1
  `Read in full and follow when` *a connector has stopped authenticating and
  the required credential fields are unknown* `to` **restore the connector to
  an authenticating state without escalating**.
form: '<a href="*" uid="ABC123">documentation-system:§3.10</a>' # optional; bound by Standard Forms
quadrant: HowTo               # bound at step 2.2
outline:                      # bound at step 4.1
  topology: linear
  numbering: hierarchical-decimal
writing-style:                # bound at step 5
  formality: professional
  tone: neutral/detached
  mode: imperative
  density: moderate
  abstraction: concrete/specific
  redundancy: zero
  signposting: light
  register: technical
```

### 1.2 Choose the container

Scope decides the container, not preference.

`description` describes the whole file and stays in *frontmatter* whatever
shape the document takes. When a document derives from a Standard Form, its
`form` controlled link also stays in frontmatter because the provenance
governs the whole file. Standard Forms owns when that key is required and how
the form is applied.

`quadrant`, `outline`, and `writing-style` describe one quadrant: they sit
in frontmatter while a document carries one quadrant, and move into each H1's
*metamatter* once it carries several (step 4.4).

Metamatter is structured YAML data carried by an HTML comment. An HTML comment
is metamatter when its first non-whitespace content is a data key of the form
`key:`; no literal wrapper is used. Position supplies scope and the leading
key supplies meaning.

Heading-scoped metamatter sits immediately beneath the heading it governs, with
no blank line between them:

```markdown
# 📖 Connector Field Reference
<!--
quadrant: Reference
outline:
  axis: field-name
-->
```

A single-key comment is valid metamatter too. Reusable document-element
provenance uses `element:` immediately beneath the heading that bounds the
element:

```markdown
## Terms
<!-- element: '<a href="*" uid="BJS5BZ">documentation-system:§2.3.1</a>' -->
```

The key determines retention and semantics. `quadrant`, `outline`,
`writing-style`, and `element` are controlled, permanent document data.
Other structured maintenance keys may define their own lifecycle. A comment
whose first content is prose or a non-data marker is an ordinary HTML comment.

When an H1 carries quadrant specification in metamatter, state its complete
`quadrant`, `outline`, and `writing-style` set; those specification keys do
not inherit from file frontmatter or another H1. An `element:`-only comment
records provenance without creating a new quadrant unit and does not cancel the
quadrant specification already governing its containing document.

### 1.3 Classify ordinary HTML comments

An ordinary HTML comment is not structured metamatter and is not body content.
Its first non-whitespace content is prose or a non-data marker rather than a
YAML data key. It carries information that a document maintainer or maintenance
tool needs but the intended reader does not.

| Information | Location |
|---|---|
| Governs the whole file | Frontmatter |
| Structured hidden data scoped by position | Metamatter |
| Needed by the reader to satisfy the acceptance criterion | Body, heading, table, or quadrant-qualified callout |
| Needed only to maintain, generate, lint, or edit the source document | Ordinary HTML comment |

Ordinary comments can hold freeform deferred documentation-cleanup TODOs,
generated-region boundaries, stable insertion anchors, Markdown linter or
formatter directives, source-formatting notes for editors, and temporary
review markers that must be removed before acceptance. A maintenance tool
may act on one, but the comment still does not govern the document's reader
relationship, quadrant, outline, or writing style.

Do not hide a system invariant, safety warning, procedure step, lookup fact,
reader-required rationale, or specification decision in an ordinary HTML
comment.

Use this test: would removing the comment prevent the intended reader from
satisfying the document's acceptance criterion? If yes, put the information
in the visible document. If no, but removing it would break maintenance,
generation, linting, or editing, an ordinary HTML comment is the right
container.

## 2. Write the description

### 2.1 Compose the routing statement

Write one `description` whose Markdown formatting exposes its three semantic
primitives:

> `directive` *[exigence]* `to` **[acceptance criterion]**`.`

The formatting is grammar, not decoration. Keep the `directive` in code,
*exigence* in italics, and **acceptance criterion** in bold inside the YAML
scalar so the same sentence remains legible to authors, routing agents, and
harnesses without rephrasing.

Choose the `directive` as a precise imperative that states both the required
action and the required depth of interaction. In particular, do not let a
keyword search, grep hit, or partial read satisfy a directive that requires
full context.

| Directive | Required interaction |
|---|---|
| `Read in full when` | Consume the entire document; targeted retrieval is not compliance. |
| `Read in full and follow when` | Consume the entire document, then perform the task under its instructions and constraints. |
| `Follow when` | Execute the governing procedure; full-document reading is not independently required unless the procedure demands it. |
| `Consult when` | Targeted lookup is sufficient. |
| `Review relevant sections when` | Selective contextual reading is sufficient, but a single search hit is not. |

Prefer the narrowest directive that states the actual obligation. Reject vague
phrases such as `Use when`, bare `Read when`, `Refer to as needed`, or
`Consider` when they leave the required interaction ambiguous.

Write the other two primitives with the same semantic discipline throughout:

- *Exigence.* Name the pressure that already exists before this document does.
  Make it recognizable from the reader's side, locate it at a moment of
  encounter rather than a phase, and confirm it would still be true if this
  document were never written. Ask what job the reader is trying to finish and
  what stops them finishing it without this document. Reject topics ("for
  anyone interested in X"), phases ("during onboarding"), and unspecified
  needs ("when the user needs help").
- **Acceptance criterion.** Name the observable thing the reader will do,
  decide, or understand-in-order-to-act as a direct result of using the
  document. Name the minimum, not the ideal: it sets the scope floor, so
  anything below it is failure and anything above it is bonus. Reject
  artifact-naming ("read the guide"). Accept internal states ("understand the
  system") only when paired with the action they enable.

Identify the primary reader while deriving those primitives, because later
style decisions still depend on the reader. The reader is not another
`description` slot: the *exigence* is their circumstance and the **acceptance
criterion** is their successful outcome. When audience qualification changes
applicability, state it inside the *exigence*.

Write the finished Markdown sentence directly into frontmatter:

```yaml
---
description: >-
  `Read in full and follow when` *a technical document is about to be drafted
  with none of the decisions governing its structure and prose committed* `to`
  **commit its description, controlled placement, outline, writing style, and
  heading grammar before drafting its body**.
quadrant: HowTo
---
```

### 2.2 Read the quadrant off the acceptance criterion

Derive `quadrant` from the **acceptance criterion** rather than choosing it
separately. What the reader does and the posture that fixes the quadrant are
one thing:

| An acceptance criterion like | Is | Quadrant |
|---|---|---|
| "Execute the procedure without escalating" | A task | HowTo |
| "Choose between rollback and forward-fix" | Understanding serving a decision | Explanation |
| "Confirm which field carries which constraint" | Lookup | Reference |
| "Has shipped a first working integration" | Guided learning | Tutorial |

If the quadrant and the **acceptance criterion** disagree, one of the two is
wrong. Fix it before continuing. Every later step reads from both.

### 2.3 Check for description overlap

Before drafting the outline, confirm the description is not already covered by
an existing document. Read the generated index descriptions for existing
documents in the same quadrant as the one just derived. Scope to the same
quadrant, not every description in the corpus: a HowTo and the Reference it
cites can share a topic without colliding because they serve different reader
postures.

The test: would a reader who already satisfies an existing document's
**acceptance criterion** be equipped to handle this new document's *exigence*
without reading it? If yes, it is covered. If the new *exigence* needs
something the existing **acceptance criterion** does not provide, a different
scope, or a genuinely separate observable outcome, it is not, even where the
two descriptions read alike on the surface.

Run this against the draft description before 2.4's checks. Polishing a
statement that turns out to be someone else's document wastes the work this
step exists to save.

A hit does not get resolved alone. Carry it into 2.4's gate: is the new
document genuinely distinct, should its scope fold into the existing document,
or should it not get written at all.

### 2.4 Run two checks before continuing

**Pairing.** Verify that meeting the **acceptance criterion** dissolves the
*exigence*, so that nothing of the original pressure survives it. Both can be
well-formed and still mismatched: a reader who must ship a fix today is not
served by "understands the architecture". The forcing condition survives it.
Re-pair before writing.

**Abstraction.** State the *exigence* at the level of the forcing condition,
not a symptom of it. If several specific triggering events share the same
reader and resolve to overlapping **acceptance criteria**, restate the
*exigence* as the category of pressure those events belong to. A domain-level
*exigence* brings any new triggering event inside the category into scope
automatically; a symptom-level one forces the document's structure to narrow
to the list.

> [!CAUTION]
> 🛑 **HTIL Gate.** Get the description, its overlap result from 2.3, and both
> checks above signed off together before anything downstream binds to it.
> Every later step reads from all of it and none can correct it after the fact.
> A wrong description, or an unresolved overlap, yields a document whose
> outline, style, and grammar are all correctly derived from a wrong or
> redundant root. An HTIL gate is a stop, not a slow-down: do not proceed on
> your own judgment.

## 3. Control the document

Writing creates documented information; controlling it is a separate job. Keep
this step here because every technical-writing task produces an artifact that
must enter whatever larger body governs it, but do not duplicate that body's
classification rules in this procedure.

### 3.1 Check whether the concept needs its own folder

Ask whether this concept creates distinct reader outcomes in other quadrants.
Draft a description for each candidate document and run step 2.2 against its
**acceptance criterion**. Descriptions that resolve to different quadrants are
different documents because one document cannot hold two reader relationships
without blending what step 2.2 just separated.

A second same-quadrant document is a document-unit exception governed by
§4.4's HTIL gate.

Deciding now bounds the outline. A concept covered by several documents
leaves this one a share of the ground instead of all of it.

### 3.2 Name the concept directory

Create it when the second document exists, never in anticipation. One file
does not justify a folder. The directory takes the concept name, leaving
each filename to name only what its own document does:

```text
Authentication/
├── 🧭 Your First Signed Request.md
├── 🛠️ Configure SSO.md
└── 📖 Token Field Reference.md
```

### 3.3 Apply document control

Apply <a href="../1%20Document%20Control/1%20%F0%9F%9B%A0%EF%B8%8F%20Control%20Documented%20Information.md#2-place-information-in-the-location-hierarchy" uid="0AQHNH">documentation-system:§1.1#2</a> to the file or concept directory
produced above. That procedure owns corpus
placement, location ordinals and addresses, `INDEX.md`, indexing,
progressive disclosure, and compiler validation. The writing procedure owns none of those rules; it
only requires that its output satisfy them before signoff.

## 4. Build the outline

Build the *heading structure*, everything visible without reading body text,
so a human can pathfind it from the heading list alone. Humans traverse a
path. Agents retrieve by heading match and entry boundary. Both need the
headings to carry the navigation, which is why the rest of this step serves
them together. They part company over orientation prose, and step 5 records
where.

Treat that same structure as the writing plan. Every committed heading is a
bounded unit of work: an agent drafts one without holding the whole document
in front of it, and several draft in parallel without colliding. That only
holds if no two headings could plausibly own the same content. Where they
overlap, the same paragraph gets written twice by writers who cannot see
each other.

Keep orientation prose ("in this section, we'll cover…") out of the
load-bearing path. It costs an agent reader context budget and returns
nothing. Where a human needs it, add it as a lead-in sentence under a
heading, never as navigation the document depends on to be findable.

### 4.1 Shape the headings for the quadrant

Take the heading structure from your quadrant's entry in Quadrant Reference,
then record the choice under `outline`. A HowTo declares
`topology: linear | branching | fan-in`. A branching one also declares
`axis` for the dimension its branches divide on, plus how a reader picks a
branch and where the branches reconverge. A Reference declares both keys:
`topology: tree | matrix | graph | list` for the shape its decomposition
takes, and `axis` for the question that decomposition answers. Tutorial and
Explanation declare neither key. Their shape is fixed, so their entry is the
whole structure.

**Hold every level to between two and seven siblings.** This is Miller's
Law: roughly 7 ± 2 items fit in working memory at once, so a reader scanning
a level with twelve headings cannot hold them as a set. The level is too
shallow and needs subdividing along its own heading axis. One child is the
opposite failure and not a decomposition at all. Fold it back into its
parent. The band bounds both directions, and a level that will not fit
inside it is usually carrying two heading axes rather than one.

**Number the headings once the outline nests, or once it sits in a
collection others cite into.** Declare `numbering: hierarchical-decimal`
under `outline` and number every level below the H1: `1`, `1.1`, `1.2`, `2`,
`2.1`. Numbers buy addressing. A `3.2` locates a section for a reader
arriving from a cross-reference, and a `2.1` with no `2.2` exposes a lone
child at a glance. In a controlled corpus, the local heading number extends
the file's address after `#`: heading `4.2` in `§2.1` is `§2.1#4.2`. Leave a
flat, standalone outline unnumbered; ordinals on five headings that nothing
points into are noise.

Exceeding the sibling bound is the usual route to that trigger, not a
separate one: a level forced to subdivide gains the depth numbering
addresses. Regenerate numbers with tooling when sections move. Hand-typed
numbers drift on the first reorder.

**Size sections by reasoning load, not evenly.** A section carrying a real
decision earns more words than one that is a lookup, and an outline whose
sections all come out the same length is usually hiding one of the two
failures: a decision compressed into a table it does not fit, or a lookup
padded to match its neighbours.

### 4.2 Identify terms and place necessary definitions

Identify the document's terms before drafting its body or choosing a
glossary. A glossary can preserve an incorrect conceptual model as neatly as
a correct one.

Start with the concepts required by the acceptance criterion. Separate facts
that can vary independently, relationship-dependent values, and
representations derived through composition or formatting. Give each concept
one term and each term one meaning. Fix any term that recurs across
independently written sections in the outline itself.

Test each proposed term:

| Test | Question | Example |
|---|---|---|
| Independence | Can the named facts change separately? | `host platform` can remain `Docker` while `host purpose` changes |
| Base versus derived | Is this a source fact or a rendered representation? | `hypervisor identifier` is a fact; `hypervisor project slug` is derived |
| Relationship | Does the value depend on another entity? | `hosting hypervisor identifier` comes from the guest's parent |
| Coverage | Does the term include every intended member? | `hosted guest` includes VM and LXC; `VM` does not |
| Collision | Does the domain or tool already assign the word another meaning? | `host purpose` avoids collision with Ansible `role` |
| Stability | Does the term survive changes unrelated to its meaning? | `Media` survives a VM-to-LXC implementation change |
| Specificity | Does the term answer one question? | `Docker` names platform; `Media` names purpose |
| Derivation | Can the terms produce every required representation without exceptions? | `Mist`, `Docker`, `Media`, and `DMZ` produce `Mist-Docker-Media-DMZ` |

Reject a term when it combines independently changing concepts, names
formatting as though it were a source fact, covers only part of the intended
category, collides with an established domain term, or needs the current
example to explain its meaning.

After identifying the terms, choose the smallest definition treatment that
lets the declared reader satisfy the acceptance criterion:

| Condition | Treatment |
|---|---|
| The declared reader already knows the term and the document uses its standard meaning | No definition |
| One project-specific term has a local use | Define it inline at first use |
| Several terms apply only within one section | Use section-local definitions or a local glossary |
| Interdependent terms recur throughout the document | Use a document-wide glossary |
| The definitions have independent lookup value across documents | Move them to an owning Reference document and link it |

Place a document-wide glossary after the scope statement and before the first
content that depends on it. Place a section-local glossary at the smallest
common parent of every section that uses it. Never place a definition after
its first load-bearing use.

A dedicated glossary gives the reader a Reference lookup task. Carry it into
§4.4's quadrant check when it could stand as an independent lookup document.

### 4.3 Check the outline for overlap and gaps

An outline is sound when it is MECE: mutually exclusive, so no two headings
compete for the same content, and collectively exhaustive, so nothing the
acceptance criterion requires goes uncovered. The quadrant's heading
structure settles neither. Check both before drafting.

**Mutual exclusivity.** The failure to catch is clustering by word
association, where a database model, a UI component, and an auth script land
under one heading because all three mention "user." Ask both questions, in
any quadrant.

- **Is this a subtype, or a slot?** Ask whether X is a kind of Y, true no
  matter which Y is meant. That is is-a: a tree branch, where the same term
  cannot recur anywhere above this point. Then ask the other way: does Y
  carry an X as one of its fields, where a different Y could carry a
  different value under the same name. That is has-a, and a repeated field
  name under unrelated parents is not a collision. Apply the
  single-heading-axis rule to is-a levels only. A Reference document's
  top-level decomposition is is-a; a single entry's own `Parameters` /
  `Returns` / `Examples` sub-headings are has-a, and were never siblings
  answering one question.
- **Does this need its own heading, or is it a leaf pretending to be one?**
  Pull back up any isolated fact nested under its own heading with no
  sibling that will ever join it. Nest any two or more items that already
  share a prefix or a sibling shape but were left flat to avoid "adding
  structure". The grouping is real.

> [!CAUTION]
> 🛑 **HTIL Gate.** When neither reading holds, or both hold at once, stop.
> Surface it as an explicit decision for someone else to close rather than
> picking the nearer fit. A guessed placement is one every later heading
> gets placed against.

**Collective exhaustiveness.** Walk the outline against
**acceptance criterion** and ask whether following it end to end meets that,
assuming nothing the document never supplies. A step the reader
would need that no heading covers is a gap. A section that could be cut
without endangering it is the opposite failure, and cutting that section is
the fix. The acceptance criterion is what makes this answerable at all.
Without one, an outline can be checked for tidiness but never for whether
it is finished.

### 4.4 Check whether one quadrant still holds

Watch for content that resists the heading structure. Entries that refuse to
sequence inside a path, or procedure that refuses to sit in a decomposition,
are the outline reporting that it carries two reader relationships, not
one. This is where the count becomes visible: the description predicts a
quadrant, but the outline is the first place a second one shows itself.

Split into separate documents by default, one per quadrant, in the concept
directory from step 3.3. That keeps every document homogeneous, and costs
nothing but files.

**Where the deliverable cannot be split, one file may carry several
quadrants.** A skill, a standard, anything shipped as a single artifact has
no concept directory available to it. Give each quadrant its own H1,
prefixed with its *quadrant glyph*, and treat everything beneath that H1 as
a separate document: its own heading structure, its own writing style, its own
heading grammar, its own numbering. Nothing inherits across an H1 boundary.

**One quadrant has one H1 by default.** A second same-quadrant H1 is a
document-unit exception governed by the HTIL gate below.

```markdown
# 🛠️ Configure the Connector
# 💡 Why Connections Drop
# 📖 Connector Field Reference
```

The quadrant glyph is the boundary signal. A reader scrolling past an H1 has
to see the reader relationship change without reading the words, and an
agent retrieving a fragment has to know which quadrant's rules govern it.
Take the glyph from that quadrant's entry in Quadrant Reference. One per
quadrant, no substitutes.

Move the per-quadrant half of the specification out of frontmatter and into
each H1's metamatter, placed immediately after the heading line with no blank
line between them. The file-level `description` remains the routing statement
for the combined artifact; each H1's metamatter carries the quadrant-specific
specification. Frontmatter keeps only what describes the file:

```markdown
---
description: >-
  `Consult when` *working with a connector whose authentication behavior or
  credential fields must be acted on* `to` **configure the connector or look
  up the field constraints needed to restore authentication**.
---

# 🛠️ Configure the Connector
<!--
quadrant: HowTo
outline:
  topology: linear
  numbering: hierarchical-decimal
writing-style:
  formality: professional
  tone: neutral/detached
  mode: imperative
  density: moderate
  abstraction: concrete/specific
  redundancy: zero
  signposting: light
  register: technical
-->

## 1. Check the credential fields

# 📖 Connector Field Reference
<!--
quadrant: Reference
outline:
  axis: field-name
writing-style:
  formality: professional
  tone: clinical/detached
  mode: declarative
  density: compressed/dense
  abstraction: concrete/specific
  redundancy: zero
  signposting: entry-headers only
  register: technical
-->

## client_id
```

The leading data key makes each block metamatter rather than an ordinary
comment. In these blocks the quadrant specification is load-bearing: strip it
and the document mixes shapes with no account of why.
Note what the two blocks share and where they part: same `formality`,
`abstraction`, and `redundancy`, different `tone`, `mode`, `density`, and
`signposting`. Each block states its full set anyway, because nothing
cascades and neither H1 can read the other's.

Leave nothing per-quadrant behind in frontmatter: a document-level value in
a multi-quadrant file is not a summary of the file, it is a false one, true
of neither half.

This is an exception, not a second default. It is available when the
single-file constraint is real, imposed by how the artifact is delivered
and not by preference, and when each quadrant's content would stand as a
document on its own. It is not available for convenience, or to avoid the
work of splitting a concept that could be split.

> [!CAUTION]
> 🛑 **HTIL Gate: document-unit exceptions.** Get authorization before
> either keeping several quadrant units in one file or creating a second
> file or H1 for the same concept and quadrant.
>
> For a single-file exception, show why delivery prevents separate files.
> For a duplicate-quadrant exception, show that neither description covers the
> other, each unit can be discovered and completed independently, one H1
> with H2–H6 branches cannot serve both, and name the query, citation, or
> owner that selects one unit but not the other.
>
> H2–H6 headings inside one H1 are ordinary outline structure and never
> require authorization.

## 5. Calibrate writing-style

Take the style block matching your `quadrant` and the primary reader type
identified while writing the description from Quadrant Reference, and record
it under `writing-style`. Tutorial is the one quadrant where reader type
changes what the document contains, not just how it reads, so it carries two
blocks; the rest carry one.

Two rules hold across every quadrant and both reader types, whatever the
block says. Keep voice active. Write "the function returns X," never "X is
returned." Keep terminology monoreferential, one name per concept. Passive
voice and synonym variation cost a human's working memory and an agent's
retrieval accuracy alike.

Read the fracture from the block itself rather than generalizing from
another quadrant. Reference fractures on signposting, HowTo on tone, and
Explanation on both redundancy and signposting. Each block is a separate
reader-type analysis, not one template applied four times.

## 6. Apply heading grammar

Write every heading in the grammar your quadrant requires. The pattern is
in that quadrant's entry in Quadrant Reference. A heading in the wrong
quadrant's grammar signals the wrong reader relationship and misdirects the
reader before they reach a sentence.

Grammar comes from the quadrant. Case and syntax come from the shared format
block and do not vary.

The quadrant holds for the whole document. Both the heading structure and this
grammar are subordinate to it. Neither is a per-heading judgment, and
neither reopens the decision. A heading that wants a different quadrant's
grammar is content for a different document, not licence to blend: a reader
cannot be doing a task and looking something up at the same heading, so two
grammars in one section state two reader relationships at once.

In a multi-quadrant document authorized at step 4.4, grammar resets at each
H1: every heading below one takes that H1's declared quadrant, and numbering
restarts there, because each H1 is a separate document that happens to share
a file.

## 7. Write the body

Write one heading at a time and stay inside it. The outline already decided
what goes where. Prose that drifts into the next heading's subject either
leaves that heading with nothing to say or says the same thing twice.

Write to the primary reader identified at step 2.1. Their discipline decides
what can go unexplained: an engineer does not need "API" expanded, an auditor
does not need the implementation walked. Explaining past it is padding. Stopping
short of it strands the reader.

Step 4.2 checked that the outline can deliver the **acceptance criterion**.
The body is where it does or does not.

The rules below are prose rules, not register. No style block exempts them.

- **State current truth, not change history.** Describe what is true and why it
  matters now; leave rename, move, previous-state, and implementation-status
  narrative to version history or task tracking. Historical narration belongs
  only where recording history is the document's job, such as a changelog or
  migration audit.
- **Make every passage earn its place.** Delete it and reread the surrounding
  material. If no information required by the reader is lost, omit it. Do not
  restate the filename, subject name, nearby facts, or generic tool mechanics.
- **Put each fact at the scope that owns it.** Keep whole-document facts at
  document scope, section facts in their section, and one-off details locally.
  When reasoning generalizes across instances, document it once with the concept
  that owns it and point to that source rather than re-deriving it locally.
- **Name the mechanism, not the feeling.** "Queries stay fast" tells a
  reader nothing. "The index is consulted before any table scan" tells them
  what happens. Test it: a sentence that would read the same in another
  project's document says nothing about this one.
- **Name the set. Never write "etc."** Every set in a real system is
  countable. List it, or give the count and the file that holds it.
- **Put the mechanism before the metaphor.** "Orphaned", "leaks", "rots"
  work as shorthand once the mechanism is on the page. Used before it, they
  stand in for a fact nobody looked up.
- **Use the natural number.** Three reasons because there are three, not
  because three sounds finished.
- **Cut the adverb or fix the verb.** "Runs quickly" wants a number. An
  adverb propping up a weak verb means the verb is wrong.
- **One idea per sentence.** If a reader backtracks to parse it, split it.
- **Take the plain word.** Use, not utilize. Help, not facilitate. If, not
  in the event that.
- **Drop the em dash.** End the sentence, or use a comma. Reaching for
  parentheses instead trades one tell for another.

---

# 📖 Quadrant Reference
<!--
quadrant: Reference
outline:
  axis: quadrant
writing-style:
  formality: professional
  tone: clinical/detached
  mode: declarative
  density: compressed/dense
  abstraction: concrete/specific
  redundancy: zero
  signposting: entry-headers only
  register: technical
-->

One entry per quadrant, carrying everything the steps above call for.

Format is the exception: it does not vary by quadrant, with one deliberate
exception inside it, `callouts`, which does. All four take the same guide
otherwise, because format follows the medium rather than the reader's
posture. A YAML-dominant body is the only split, and it is rare in prose.

```yaml
format:                  # shared by all four quadrants
  medium: prose-markdown # a YAML-dominant body takes the YAML guide instead
  emphasis:
    bold: RFC 2119 keywords, critical terms
    italic: new terminology, referenced works
    code: commands, file paths, variables, technical syntax
  headings:
    h1: exactly one, title case. Only a multi-quadrant file authorized at
        step 4.4 carries more, and each of its H1s is a separate document
    h2-h6: sentence case
    syntax: ATX, no skipped levels, no emphasis, siblings uniquely named
  filenames: title case, matching h1 — no separate casing rule for what
             names a document versus what titles it

  comments:
    structured:
      name: metamatter
      syntax: "HTML comment whose first non-whitespace content is a YAML data key"
      purpose: position-scoped structured specification, provenance, or maintenance data
      placement: immediately beneath the governed heading unless the key defines another scope
    ordinary: # Markdown has no native comment syntax; use an HTML comment.
      syntax: "HTML comment beginning with prose or a non-data marker"
      purpose: freeform hidden document maintenance or maintenance-tool control
      placement: adjacent to its target, or at file end for file-wide cleanup
      forbidden: reader-required topic content or structured document data

  # FIXME see if this can be compacted
  callouts:               # elevates one claim above prose's flat weighting;
                           # bold (above) stays the default — one preferred
                           # type per quadrant below, never a menu, and
                           # exceeding the cap dilutes the signal it carries
    cap: 1-2 per document — a third candidate is prose or bold, not a callout
    tutorial:
      reader: human only — tutorial-agent's exemplar-pair format already differentiates
      type: TIP
      trigger: a step where learners predictably stall and need encouragement or a way past it
    howto:
      type: CAUTION | WARNING
      trigger: an irreversible, destructive, or safety-critical step — binding on an agent
               executing the procedure, not only a human reading it
    explanation:
      type: NOTE
      trigger: a true, load-bearing fact that would break the concept-dependency throughline
               if inlined — a scope fence, not part of the argument's own spine
    reference:
      type: IMPORTANT
      trigger: a misconception whose absence causes a wrong lookup, not merely an incomplete one
```

## Tutorial

**Quadrant glyph** 🧭 · **Reader posture** learning by guided practice
· **Acceptance criterion pattern** "has shipped a first working integration"

**Heading grammar.** Milestone-marking declarative:
`[Past-tense / noun phrase marking achievement]`.

**Heading structure.** For a human reader, a milestone sequence on a fixed
spine: introduction, safe-environment setup, milestones, summary. Each
milestone builds on the last and produces a checkable result; the first
requires nothing but the environment. For an agent reader, an exemplar
ladder: paired good and bad implementations of one topic, ordered so each
pair isolates a single distinction, with the rule that separates them
stated.

**Writing style.** Reader type changes what the document contains here, not
only how it reads, so this quadrant carries two blocks.

```yaml
tutorial-human: # guided practice toward a skill
  formality: conversational
  tone: warm/earnest                # a learner must feel safe to fail
  mode: imperative
  density: spacious/expanded
  abstraction: concrete/specific
  redundancy: structural-echo       # spaced repetition consolidates a
                                     # learner's schema
  signposting: explicit
  register: accessible

tutorial-agent: # paired good and bad implementations of one topic.
                # Derived here, not compressed from an authored profile;
                # the other four blocks are.
  formality: professional
  tone: neutral/detached            # warmth buys nothing; an agent is not
                                     # afraid of failing
  mode: declarative                 # label each specimen and name the
                                     # discriminating rule, rather than
                                     # walking the reader through doing it
  density: moderate
  abstraction: concrete/specific    # specimens, not descriptions of them
  redundancy: zero                  # a good/bad pair is one unit, not
                                     # repetition. The contrast is the
                                     # payload
  signposting: light
  register: technical
```

## HowTo

**Quadrant glyph** 🛠️ · **Reader posture** doing a task
· **Acceptance criterion pattern** "execute the procedure without escalating"

**Heading grammar.** Goal-first imperative:
`[Verb] [object] [optional qualifier]`.

**Heading structure.** A path, under one declared topology: **linear** (one
route), **branching** (diverges by reader choice, each branch
self-contained), or **fan-in** (diverges only in starting state, converges
to one shared procedure). Whichever applies, place prerequisites and
conditions before the step they gate, never inside it.

**Writing style.**

```yaml
howto:          # primary reader: agent
  formality: professional
  tone: neutral/detached            # can read as curt to a human under task
                                     # stress; presentation layer may add
                                     # minimum professional warmth
  mode: imperative
  density: moderate
  abstraction: concrete/specific
  redundancy: zero                  # human mitigation: brief confirmatory
                                     # callback at safety-critical steps only
  signposting: light
  register: technical
```

## Explanation

**Quadrant glyph** 💡 · **Reader posture** understanding a concept
· **Acceptance criterion pattern** "choose between rollback and forward-fix"

**Heading grammar.** Concept-naming declarative: `[Concept name]`,
`Why [concept]`, or `How [concept] works`.

**Heading structure.** A concept dependency graph, laid out as a topological
sort: no concept, as a heading or in prose, appears before every concept it
presupposes. Split or merge one concept to break a circular prerequisite.

**Writing style.**

```yaml
explanation:    # primary reader: agent
  formality: professional
  tone: collegial/earnest
  mode: declarative
  density: moderate
  abstraction: mixed
  redundancy: zero                  # human default is light- to
                                     # structural-echo; spaced repetition
                                     # builds a human's schema, costs an
                                     # agent tokens
  signposting: suppressed           # human default is moderate; "as
                                     # discussed earlier" carries zero
                                     # information for an agent
  register: accessible
```

## Reference

**Quadrant glyph** 📖 · **Reader posture** looking something up
· **Acceptance criterion pattern** "confirm which field carries which
constraint"

**Heading grammar.** Entity-naming noun phrase: `[Entity name]` or
`[Entity type]: [specific name]`.

**Heading structure.** A domain decomposition under one shared, nameable
heading axis per depth, so every heading at a level answers the same
question. Keep each parent at a strictly higher abstraction than its
children, and never group by "feels similar."

Declare the topology the decomposition takes: **tree** for a strict is-a or
part-of hierarchy, **matrix** for entities carrying independent attributes,
**graph** for explicit dependency edges, **list** for one ordered dimension.
A matrix is the case where the reader's entry point decides which dimension
nests outermost. Decompose by what the reader arrives already holding, since
that is the key they will look the entry up by.

**Writing style.**

```yaml
reference:      # primary reader: agent
  formality: professional
  tone: clinical/detached
  mode: declarative
  density: compressed/dense
  abstraction: concrete/specific
  redundancy: zero
  signposting: entry-headers only   # suppressed prose costs a human doing
                                     # multi-session lookup; mitigate with a
                                     # presentation-layer "see also"
  register: technical
```
