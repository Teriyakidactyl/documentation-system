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
> is designed for readers to navigate themselves from `README.md` to
> `README.md`, acquiring only the context needed for the current decision. At
> each location, use the local guidance and glossary, compare only the immediate
> Index choices, select the narrowest matching `description`, and load deeper
> guidance only when the route requires it. Authors therefore place definitions
> and instructions at the earliest scope where they become necessary rather
> than exposing repository-wide knowledge by default.

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

Before relying on any selected document, confirm that its complete source text
is identifiable in the active, non-compacted conversation history. If it is
not, or if its prior presence is only within compacted history, read the
document in full before relying on it.

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

## Enter the corpus

A task may present several independent concerns. Route each concern separately.

For the current concern, compare only the immediate choices in the current
Index and select the narrowest matching `description`. When that choice enters
a folder, read that folder's literal `README.md` before using its Index.
Repeat until the concern-specific document or documents are selected, then
satisfy each according to its directive.

## Index
<!--
element:
  path:
    uid: BZJASV
    filepath: 2 Technical Writing/3 Document/2 Document Elements/5 Index/README.md
  version: '1.0'
  renderer:
    uid: 45E225
    filepath: 4 Tooling/1 🛠️ Navigation Crawler.py
-->

- <a href="1%20Document%20Control/README.md" uid="YVXKT9">documentation-system:§1</a> — Document Control
  - `Consult when` *documented information needs a controlled repository location, retrieval policy, storage representation, address, index presence, progressive-disclosure exposure, or Organizing validation* `to` **select the Document Control rule or procedure that governs how users encounter and rely on the information**.
- <a href="2%20Technical%20Writing/README.md" uid="6J52FM">documentation-system:§2</a> — Technical Writing
  - `Consult when` *technical documented information must be authored* `to` **select the Technical Writing procedure before drafting the document body**.
- <a href="4%20Tooling/README.md" uid="YT5Y7F">documentation-system:§4</a> — Tooling
  - `Consult when` *the Documentation System needs Tooling runtime preparation, corpus organization, representation-level tooling, or harness projection* `to` **prepare the required execution environment or select the narrowest capability that owns the mechanical operation**.
- <a href="5%20Organizing%20Concepts/README.md" uid="A7K3QF">documentation-system:§5</a> — Organizing Concepts
  - `Consult when` *a structural decision is shared across documents, code, schemas, or other repository artifacts* `to` **enter the earliest unresolved organizing question and resolve conceptual structure before domain-specific representation rules are applied**.
- <a href="6%20Software%20Design/README.md" uid="1SGQXT">documentation-system:§6</a> — Software Design
  - `Consult when` *a software design concern must be resolved before its implementation pattern or boundary is chosen* `to` **select the canonical Software Design guidance that fixes the repository's default decision**.
- <a href="7%20Editing/README.md" uid="X74GZ1">documentation-system:§7</a> — Editing
  - `Consult when` *an existing artifact must be changed, checked against governing criteria, or subjected to an explicitly required assurance pass* `to` **separate mutation authority, validation reasoning, bounded Validation, and the editorial scope that governs prose-bearing work**.
