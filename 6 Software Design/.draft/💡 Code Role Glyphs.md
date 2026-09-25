---
description: >-
  `Read in full when` *a code-role glyph vocabulary is being considered for
  source filenames and implementation roles need a stable visual classification
  distinct from documentation posture* `to` **understand the proposed
  role/glyph model, evaluate its candidate members, and decide what should
  become canonical Software Design guidance**.
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

# 💡 Code Role Glyphs

> [!NOTE]
> This file is working information in `.draft/`. It is not current Software
> Design authority and does not establish a filename convention.

> [!WARNING]
> **A glyph can truthfully denote what a `.py` file is doing only when the file
> itself is a stable responsibility boundary.**

## 1. Problem

The public Tooling Python files carry Technical Writing quadrant glyphs in the
controlled documentation embedded in their module docstrings, while their
source filenames are glyphless:

~~~text
1 Navigation Crawler.py
4 Markdown.py
5 Frontmatter.py
~~~

The quadrant glyph still classifies the posture of the embedded documentation.
It does not classify the implementation responsibility of the Python module.

For source navigation, a glyph is useful only when it helps answer a code
placement or ownership question. A source-facing glyph should therefore
communicate an implementation role, while the filename text continues to name
the concept or capability.

~~~text
🔌 Frontmatter.py
│  └──────────── subject: Frontmatter
└──────────────── role: boundary translation
~~~

The proposed distinction is:

~~~text
documentation quadrant
    → reader relationship of documented information

code role
    → primary implementation responsibility of a source artifact
~~~

A Python module may carry both facts. They need not use the same projection.

## 2. Separate role from subject

The textual filename names the semantic subject. The glyph identifies the
module's primary implementation role.

~~~text
<role glyph> <subject>.py
~~~

Examples:

~~~text
🔌 Frontmatter.py
🧠 Corpus.py
🎯 Corpus Validation.py
📤 Index.py
~~~

The role must not replace the subject with generic names such as
`adapter.py`, `service.py`, or `manager.py` when the domain concept can be
named directly. The intended value is fast visual classification without
discarding the vocabulary that makes the module discoverable.

Changing the subject and changing the role are different events. Renaming
`Frontmatter` because the concept changed is a naming/domain change. Changing
its glyph because its primary responsibility changed is an architectural signal.

## 3. Candidate role vocabulary

The vocabulary should remain small. Each admitted role needs a stable ownership
meaning, a selecting condition, and boundaries that distinguish it from every
peer.

| Candidate | Glyph | Meaning | Put code here when |
|---|---|---|---|
| **Model** | 🧠 | Canonical domain facts and local invariants | The artifact primarily represents what the system knows or is, including stable values, relationships, and locally owned invariants. |
| **Processor** | ⚙️ | Mechanical transformation or operation | The artifact primarily transforms established inputs or state according to deterministic mechanics owned by that capability. |
| **Adapter** | 🔌 | Boundary or representation translation | The artifact primarily translates between canonical concepts and an external representation, host language, protocol, provider, or storage boundary. |
| **Validator** | 🎯 | Invariant evaluation | The artifact primarily evaluates established facts against rules and reports violations or diagnostics without owning the canonical facts it checks. |
| **Orchestrator** | 🎛️ | Workflow coordination | The artifact primarily sequences or coordinates other owners while leaving their specialist semantics with them. |
| **Projection** | 📤 | Derived consumer representation | The artifact primarily derives a reader-, tool-, transport-, or consumer-facing representation from canonical state. |
| **Entry Point** | 🚪 | Public invocation boundary | The artifact primarily receives a public invocation and adapts it into the implementation's internal workflow. |
| **Policy / Scheme** | 📏 | Selectable rules governing permissible behavior | The artifact primarily defines a strategy, organization scheme, policy, or decision rules selected by a broader capability. |
| **Verification** | 🧪 | Executable proof of another contract | The artifact primarily exists to prove behavior, architecture, or invariants rather than implement the production responsibility itself. |

These are candidates, not a closed taxonomy yet.

## 4. Candidate boundaries

The roles should classify primary responsibility rather than implementation
technique.

A parser is not automatically a peer role. Parsing an external representation
into canonical values is normally an Adapter responsibility. Parsing as one
step of an internally owned transformation may instead belong to a Processor.

A serializer, mapper, repository, gateway, persistence component, or protocol
client is normally an Adapter when its defining responsibility is crossing a
representation or system boundary.

A factory is normally an implementation mechanism within Model, Processor, or
Adapter responsibility rather than a top-level role.

A service, manager, helper, or utility does not identify a sufficiently stable
ownership relationship by itself. Those names should not become roles without a
more precise recurring responsibility.

Testing is different from validation. Validator denotes production logic that
evaluates invariants as part of system behavior. Verification denotes executable
evidence whose purpose is to prove a contract.

Projection is different from Adapter. A Projection derives another view of
canonical information without creating a new authority. An Adapter translates
across a boundary whose representation or vocabulary is not the canonical
domain model.

Orchestration is different from processing. A Processor owns the mechanics of a
transformation. An Orchestrator coordinates independently owned operations and
should not absorb their expertise.

## 5. Admission test for a role

A new role should enter the vocabulary only when all of these conditions hold:

1. **Placement value.** Knowing the role helps an amnesiac maintainer decide
   where a responsibility belongs.
2. **Ownership meaning.** The role names a durable reason to change rather than
   a framework construct or coding technique.
3. **Peer distinction.** Its selecting condition can be distinguished from
   every existing role without relying on the current example.
4. **Language independence.** The role remains meaningful across programming
   languages and frameworks.
5. **Primary-role usefulness.** A source artifact can normally claim the role
   as its primary responsibility without needing a string of role glyphs.
6. **Architectural signal.** Changing the role while keeping the subject fixed
   would indicate a meaningful responsibility change.

A proposed role that fails these tests should remain an implementation detail or
a more specific name beneath an existing role.

## 6. One primary role per source artifact

A source artifact should normally carry one role glyph.

~~~text
🎛️📤🎯 Organizing.py
~~~

is not a richer classification. It indicates either that the vocabulary does
not distinguish the responsibilities correctly or that the artifact combines
independently changing responsibilities.

Secondary behavior can exist inside a module without becoming part of its
filename classification. The glyph identifies the responsibility that explains
why the artifact exists.

## 7. Keep documentation posture independent

Documentation quadrant remains a separate fact:

~~~yaml
quadrant: HowTo
code-role: adapter
~~~

A representation intended for documentation navigation can project the
quadrant:

~~~text
🛠️ Frontmatter
~~~

A representation intended for source navigation can project the code role:

~~~text
🔌 Frontmatter.py
~~~

The physical filename does not need to encode both classifications. If
Organizing eventually owns filename projection, the selected projection should
follow the consumer rather than forcing one glyph vocabulary to serve two
different questions.

The code-role glyph vocabulary should avoid glyphs already carrying a
repository-wide documentation meaning where the two can appear in the same
navigation surface. The current documentation quadrant glyphs are:

~~~text
🧭 Tutorial
🛠️ HowTo
💡 Explanation
📖 Reference
~~~

The candidate code-role set deliberately does not reuse those four glyphs.

## 8. Relationship to Software Design domains

Software Design domains and code roles classify different things.

~~~text
Software Design domain
    = recurring question the architecture must resolve

code role
    = primary implementation responsibility of a source artifact
~~~

Error Management, Testing, Concurrency, Configuration, Data Flow,
Decomposition, Extension, Interfaces, Naming, and Performance are therefore not
default source-folder or source-file roles. They are design concerns that can
apply across many implementation responsibilities.

For example, an Adapter can have error-management, concurrency, testing, naming,
and performance decisions without becoming five modules organized under those
concern names.

## 9. Candidate application to current Tooling

The existing Tooling implementation offers useful pressure tests, but these
classifications remain hypotheses until the role definitions are accepted.

~~~text
_organizing/
├── 🧠 model.py
├── 🚪 cli.py
├── 🎛️ engine.py
├── 📤 indexes.py
├── 📤 links.py
├── 📤 elements.py
├── 🎯 diagnostics.py        # may combine validation and diagnostic projection
├── ⚙️ refactor.py
└── schemes/
    └── 📏 ordinal.py

_capabilities/
├── 🔌 markdown.py
├── 🔌 frontmatter.py
├── 🔌 yaml.py
├── 🔌 html.py
└── ⚙️ folder.py

tests/
├── 🧪 test_capabilities.py
└── 🧪 test_organizing.py
~~~

Several entries are deliberately contestable. For example,
`diagnostics.py` may expose that validation and diagnostic representation are
separate responsibilities, while the representation capabilities may prove that
Adapter is too broad. Those tensions are evidence for refining the taxonomy
before it becomes naming authority.

## 10. Open decisions

The proposal still needs answers to these questions before becoming canonical:

- Is **Processor** a stable role, or does it hide several independently useful
  responsibilities?
- Is **Policy / Scheme** a peer implementation role or a specialization of
  Model or Processor?
- Should **Verification** participate in the same production-code role
  vocabulary, or use a separate test classification?
- Should public executable modules be classified by **Entry Point** even when a
  thin entry point shares a file with a capability implementation?
- Should role be canonical metadata projected into filenames, or should the
  filename itself remain the authored source of the role?
- Should all source files receive a role glyph, or only files that participate
  in controlled/public source navigation?
- Which current modules cannot be classified cleanly by exactly one candidate
  role, and what do those failures reveal about either the taxonomy or the
  implementation boundaries?

The vocabulary should become authority only after concrete source files can be
classified consistently and ambiguous cases have been used to revise the model
rather than forced into the nearest category.
