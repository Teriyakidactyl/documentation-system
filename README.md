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
    filepath: 2 Technical Writing/3 Document/2 Document Elements/1 📖 Glossary.md
  version: '2.0'
-->

| Term | Meaning |
|---|---|
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
<a href="1%20Document%20Control/3%20%F0%9F%93%96%20Repository%20Information%20Storage.md" uid="S9HVWB">documentation-system:§1.3</a>.

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
before `:`, then descends through decimal locations and may select a numbered
heading after `#`. For example,
`documentation-system:§2.3.2.1#4.2` declares the directory named
`documentation-system` as the corpus root, descends through locations
`2.3.2.1`, and selects heading `4.2`. A bare form such as `§2.3.2.1`
omits the required corpus-root declaration and is invalid.

## Index
<!--
element:
  path:
    uid: BZJASV
    filepath: 2 Technical Writing/3 Document/2 Document Elements/5 Index/README.md
  version: '2.0'
  renderer:
    uid: 45E225
    filepath: 4 Tooling/Navigation Crawler.py
-->

### Document Control

`Consult when` *documented information needs a controlled repository location, retrieval policy, storage representation, address, index presence, progressive-disclosure exposure, or Organizing validation* `to` **select the Document Control rule or procedure that governs how users encounter and rely on the information**.

<a href="1%20Document%20Control/README.md" uid="YVXKT9" data-ds-link="relative-path">../1 Document Control/README.md</a>

- `1 🛠️ Control Documented Information.md`
- `2 📖 Folder Conventions.md`
- `3 📖 Repository Information Storage.md`

### Technical Writing

`Consult when` *technical documented information must be authored* `to` **select the Technical Writing procedure before drafting the document body**.

<a href="2%20Technical%20Writing/README.md" uid="6J52FM" data-ds-link="relative-path">../2 Technical Writing/README.md</a>

- `1 🛠️ Write A Technical Document.md`
- `2 🧭 Routable Descriptions Recognized.md`
- `3 Document/README.md`

### Tooling

`Consult when` *the Documentation System needs Tooling runtime preparation, corpus organization, representation-level tooling, harness projection, or current Tooling architecture* `to` **prepare the required execution environment, select the narrowest capability that owns the mechanical operation, or locate the Architecture Document governing a Tooling implementation**.

<a href="4%20Tooling/README.md" uid="YT5Y7F" data-ds-link="relative-path">../4 Tooling/README.md</a>

- `8 🛠️ Prepare Tooling Environment.md`
- `9 📐 Architecture/README.md`

### Organizing Concepts

`Consult when` *a structural decision is shared across documents, code, schemas, or other repository artifacts* `to` **enter the earliest unresolved organizing question and resolve conceptual structure before domain-specific representation rules are applied**.

<a href="5%20Organizing%20Concepts/README.md" uid="A7K3QF" data-ds-link="relative-path">../5 Organizing Concepts/README.md</a>

- `1 🛠️ Determine Structural Units.md`
- `2 📖 Relationships and Structural Topologies.md`
- `3 💡 Ownership, Containment, and Convergence.md`
- `4 🛠️ Test A Placement.md`
- `5 🛠️ Decompose And Validate A Structure.md`

### Software Design

`Consult when` *software design must be specified, a recurring design concern must be resolved, a reusable design must be selected, or the relationship between reusable specification and a live implementation must be understood* `to` **apply the canonical Software Design authority, preserve established decisions, and route implementation-specific design to the code-local architecture that governs it**.

<a href="6%20Software%20Design/README.md" uid="1SGQXT" data-ds-link="relative-path">../6 Software Design/README.md</a>

- `1 📖 Software Design Principles.md`
- `2 Comments/README.md`
- `3 Concurrency/README.md`
- `4 Configuration/README.md`
- `5 Data Flow/README.md`
- `6 Decomposition/README.md`
- `7 Error Management/README.md`
- `8 Extension/README.md`
- `9 Interfaces/README.md`
- `10 Naming/README.md`
- `11 Performance/README.md`
- `12 Testing/README.md`
- `13 📖 Implemented Architecture.md`
- `14 🛠️ Design And Record An Implemented Architecture.md`

### Editing

`Consult when` *an existing artifact must be changed, checked against governing criteria, or subjected to an explicitly required assurance pass* `to` **separate mutation authority, validation reasoning, bounded Validation, and the editorial scope that governs prose-bearing work**.

<a href="7%20Editing/README.md" uid="X74GZ1" data-ds-link="relative-path">../7 Editing/README.md</a>

- `1 🛠️ Revise an Artifact.md`
- `2 🛠️ Validate an Artifact.md`
- `3 💡 Editing Under Conceptual Shift.md`
- `4 📖 Editorial Terms.md`
- `5 📖 Validation Evidence.md`
