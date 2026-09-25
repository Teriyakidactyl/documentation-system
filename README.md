---
uid: 6E9QHP
description: >-
  `Consult when` *repository work reaches a documentation, documented-information,
  or Documentation System tooling concern and the applicable procedure is not
  yet known* `to` **select the narrowest applicable Documentation System
  location before changing the repository**.
---

# Documentation System

This repository contains guidance documents and supporting tools for technical
writing, document control, repository organization, software design, editing,
and code creation.

> [!IMPORTANT]
> **Progressive disclosure is the interaction model.** The Documentation System
> assumes no repository-specific context for any user or contributor arriving
> at this root `README.md`; it calls that arriving reader an *amnesia agent*.
> Readers navigate themselves from `README.md` to `README.md`, acquiring only
> the context needed for the current decision. At
> each location, use the local guidance and glossary, compare only the immediate
> Index choices, select the narrowest matching `description`, and load deeper
> guidance only when the route requires it. Displayed descendant filenames are
> orientation clues, not routing choices: they do not authorize bypassing the
> indexed child that exposes them; enter that child and read its `README.md`
> before making the next routing decision. A task may present several
> independent concerns; route each concern separately and satisfy every selected
> concern-specific document according to its directive. Authors therefore place
> definitions and instructions at the earliest scope where they become
> necessary rather than exposing repository-wide knowledge by default.

## Project glossary
<!--
element:
  path:
    uid: BJS5BZ
    filepath: a. Document Design/a. Assemblies/a. Elements/3. 📖 Glossary.md
  version: '2.0'
-->

| Term | Meaning |
|---|---|
| **Assembly** | A reusable representation, or reusable part of a representation, intended to be selected and composed rather than designed anew for each instance. Each design domain defines the Assembly types appropriate to its artifacts. |
| **Folder README** | The literal `README.md` representing a descendant folder. Read it when entering that folder; it supplies applicable local guidance and the next routing choices. |
| **Index** | The immediate routing choices exposed by the current `README.md`. |
| **description** | The project-defined routing statement used to decide whether a choice applies and how it must be used. |
| **directive** | The part of a `description` that specifies the required interaction depth with the selected document. |
| **quadrant glyph** | A Technical Writing glyph indicating documented-information posture: 🧭 Tutorial, 🛠️ HowTo, 💡 Explanation, or 📖 Reference. It classifies the document relationship to its reader, not the implementation role of a source file. Software code currently has no canonical analogous role-glyph vocabulary. |
| **current authority** | Information that may be relied on when acting now. |

## Scope

This `README.md` provides repository-wide entry guidance for the complete Git
repository. A Folder README specializes the context of its containing folder.
Unless a Folder README states a different boundary in its own Scope, its
guidance applies recursively beneath that folder; more-specific guidance does
not silently cancel still-applicable ancestor requirements.

## Authority

Repository entry begins with this literal `README.md`. Before relying on a
descendant controlled document, read every literal `README.md` on the
filesystem path from the repository root to that document. Each Folder README
adds local context; it does not silently cancel still-applicable ancestor
requirements. After that README chain is established, route each concern to its
specific controlled documents and obey each selected document according to its
`description` directive.

Current authority is information a user must be able to rely on when acting
now. Working information, evidence and provenance, and historical or cold
information do not become current authority because of their storage mechanism
or proximity to current guidance. The complete information-role and retrieval
model is owned by
<a href="a.%20Document%20Design/b.%20Document%20Control/2.%20%F0%9F%93%96%20Repository%20Information%20Storage.md" uid="S9HVWB">documentation-system:§a.b.2</a>.

## Guidance Context Integrity

Before relying on any selected document, confirm that its complete source text
is identifiable in the active, non-compacted conversation history. If it is
not, or if its prior presence is only within compacted history, read the
document in full before relying on it. Plan that read around the retrieval,
output, and context limits of the available tools so the complete source can be
delivered through EOF; if retrieval must be split or retried, preserve that
completion requirement across the continuation.

## Contributing

Are you navigating this repository under a request to modify it? Then you are a
user of the repository before you are a contributor.

Before making changes, follow the repository's progressive-disclosure path from
this `README.md`, establish the applicable `README.md` chain, gather the
concern-specific guidance that governs the work, and adhere to that guidance
throughout the contribution. Do not begin from the intended edit location and
work backward; establish the applicable guidance before modifying the
repository.

## Source and distribution

This repository's `main` branch is the canonical maintainer/source corpus.
Skill consumers who need only the published consumer surface should clone the
generated `latest` branch instead:

```bash
git clone --branch latest --single-branch https://github.com/Teriyakidactyl/documentation-system.git
```

The `latest` branch has an independent generated history and contains this
repository's Skill Distribution projection. This repository's publication
process omits dot-prefixed directories from that projection; that publication
choice applies to this repository and does not prescribe how repositories that
consume the Documentation System must package their own skills. Version tags
such as `v1.2.0`, when published, identify immutable states of the
distribution history.

## Documentation addresses

A corpus root is contextual to an Organizing job; it is not a permanent
designation of a directory. An Organizing job accepts an optional
`corpus_root` path and otherwise selects the Git repository root containing
Organizing.

A documentation address separately declares its corpus root by directory name
before `:`, then descends through convention-derived location tokens and may
select a numbered heading after `#`. Tokens may therefore be alphabetic or
decimal according to the effective folder policy. For example,
`documentation-system:§e.c.b.1#4.2` declares the directory named
`documentation-system` as the corpus root, descends through locations
`e.c.b.1`, and selects heading `4.2`. A bare form such as `§e.c.b.1`
omits the required corpus-root declaration and is invalid.

## Index
<!--
element:
  path:
    uid: BZJASV
    filepath: a. Document Design/a. Assemblies/a. Elements/a. Index/README.md
  version: '2.0'
  renderer:
    uid: 45E225
    filepath: d. Software/Navigation Crawler.py
-->

### Document Design

`Consult when` *documented information must be decomposed, represented, authored, controlled, or given reusable document structure* `to` **apply document-specific design forces and route to reusable Assemblies, Document Control, or Technical Writing without treating document representation as domain-independent structure**.

<a href="a.%20Document%20Design/README.md" uid="DDES01" data-ds-link="relative-path">../a. Document Design/README.md</a>

- `a. Assemblies/README.md`
- `b. Document Control/README.md`
- `c. Technical Writing/README.md`

### Editing Concepts

`Consult when` *an existing artifact must be changed, checked against governing criteria, or subjected to an explicitly required assurance pass* `to` **separate mutation authority, validation reasoning, bounded Validation, and the editorial scope that governs prose-bearing work**.

<a href="b.%20Editing%20Concepts/README.md" uid="X74GZ1" data-ds-link="relative-path">../b. Editing Concepts/README.md</a>

- `1. 💡 Editing Under Conceptual Shift.md`
- `2. 📖 Editorial Terms.md`
- `3. 📖 Validation Evidence.md`
- `4. 🛠️ Revise an Artifact.md`
- `5. 🛠️ Validate an Artifact.md`

### Organizing Concepts

`Consult when` *a structural decision is shared across documents, code, schemas, or other repository artifacts* `to` **enter the earliest unresolved organizing question and resolve conceptual structure before domain-specific representation rules are applied**.

<a href="c.%20Organizing%20Concepts/README.md" uid="A7K3QF" data-ds-link="relative-path">../c. Organizing Concepts/README.md</a>

- `1. 💡 Ownership, Containment, and Convergence.md`
- `2. 📖 Relationships and Structural Topologies.md`
- `3. 🛠️ Decompose And Validate A Structure.md`
- `4. 🛠️ Determine Structural Units.md`
- `5. 🛠️ Test A Placement.md`

### Software

`Consult when` *the Documentation System needs Software runtime preparation, corpus organization, representation-level tooling, harness projection, or current Software architecture* `to` **prepare the required execution environment, select the narrowest capability that owns the mechanical operation, or locate the Architecture Document governing a Software implementation**.

<a href="d.%20Software/README.md" uid="YT5Y7F" data-ds-link="relative-path">../d. Software/README.md</a>

- `Folder.py`
- `Frontmatter.py`
- `Harness Installer.py`
- `HTML.py`
- `Markdown.py`
- `Navigation Crawler.py`
- `📐 Architecture/README.md`
- `YAML.py`
- `🛠️ Prepare Software Environment.md`

### Software Design

`Consult when` *software design must be specified, a recurring design concern must be resolved, a reusable design must be selected, or the relationship between reusable specification and a live implementation must be understood* `to` **apply the canonical Software Design authority, preserve established decisions, and route implementation-specific design to the code-local architecture that governs it**.

<a href="e.%20Software%20Design/README.md" uid="1SGQXT" data-ds-link="relative-path">../e. Software Design/README.md</a>

- `1. 📖 Implemented Architecture.md`
- `a. Assemblies/README.md`
- `2. 📖 Software Design Principles.md`
- `b. Comments/README.md`
- `3. 🛠️ Design And Record An Implemented Architecture.md`
- `c. Concurrency/README.md`
- `d. Configuration/README.md`
- `e. Data Flow/README.md`
- `f. Decomposition/README.md`
- `g. Error Management/README.md`
- `h. Extension/README.md`
- `i. Interfaces/README.md`
- `j. Naming/README.md`
- `k. Performance/README.md`
- `l. Testing/README.md`
