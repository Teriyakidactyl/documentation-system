---
uid: 6E9QHP
form: '<a href="2%20Technical%20Writing/3%20Document/1%20Document%20Forms/10%20%F0%9F%93%96%20Origin.md" uid="DNFDSK">documentation-system:§2.3.1.10</a>'
description: >-
  `Consult when` *repository work reaches a documentation, documented-information,
  or Documentation System tooling concern and the applicable procedure is not
  yet known* `to` **select the narrowest applicable Documentation System
  location before changing the repository**.
---

# Documentation System Origin

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
such as `v1.2.0`, when published, identify immutable states of the distribution
history.

**Corpus root** is a contextual role declared for a filesystem directory; it
is not a permanent designation of that directory. An Organizing job declares its
corpus root with the optional `corpus_root` path argument; when omitted, that
job defaults to the root of the Git repository containing Organizing. A
documentation address separately declares its corpus root by directory name
before `:`, and that declaration is required. Thus
`documentation-system:§2.3.2.1` declares the directory named
`documentation-system` as the corpus root for that address, then descends
through ordinal 2, child 3, child 2, and artifact 1; `#4.2` selects numbered
heading 4.2 inside the resolved artifact. A bare form such as `§2.3.2.1`
omits the required corpus-root declaration, is invalid address syntax, and is
unresolvable.

> [!IMPORTANT]
> Start here. A task may present several independent concerns; route each one
> separately. For the current concern, compare only the immediate indexed
> choices, select the narrowest matching description, and descend one index at
> a time until the governing artifact is identified. Repeat for every remaining
> concern, satisfying each resulting document according to its directive.
>
> Before relying on any governing document selected through this routing
> process, confirm that its complete source text is identifiable in the active,
> non-compacted conversation history. If it is not, or if its prior presence is
> only within compacted history, read the document in full before relying on it.

<!-- BEGIN index -->
<!-- This block is owned by the Documentation Compiler; run the compiler whenever indexed information or classification may have changed. -->

- <a href="1%20Document%20Control/INDEX.md" uid="YVXKT9">documentation-system:§1</a> — Document Control
  - `Consult when` *documented information needs a controlled repository location, retrieval policy, storage representation, address, index presence, progressive-disclosure exposure, or compiler validation* `to` **select the Document Control rule or procedure that governs how users encounter and rely on the information**.
- <a href="2%20Technical%20Writing/INDEX.md" uid="6J52FM">documentation-system:§2</a> — Technical Writing
  - `Consult when` *technical documented information must be authored* `to` **select the Technical Writing procedure before drafting the document body**.
- <a href="4%20Tooling/INDEX.md" uid="YT5Y7F">documentation-system:§4</a> — Tooling
  - `Consult when` *the Documentation System needs compilation, address resolution, or harness projection* `to` **select the tool that performs the required control operation**.
- <a href="5%20Organizing%20Concepts/INDEX.md" uid="A7K3QF">documentation-system:§5</a> — Organizing Concepts
  - `Consult when` *a structural decision is shared across documents, code, schemas, or other repository artifacts* `to` **enter the earliest unresolved organizing question and resolve conceptual structure before domain-specific representation rules are applied**.
- <a href="6%20Software%20Design/INDEX.md" uid="1SGQXT">documentation-system:§6</a> — Software Design
  - `Consult when` *a software design concern must be resolved before its implementation pattern or boundary is chosen* `to` **select the canonical Software Design guidance that fixes the repository's default decision**.
- <a href="7%20Editing/INDEX.md" uid="X74GZ1">documentation-system:§7</a> — Editing
  - `Consult when` *an existing artifact must be changed, checked against governing criteria, or subjected to an explicitly required assurance pass* `to` **separate mutation authority, validation reasoning, bounded Validation, and the editorial scope that governs prose-bearing work**.
<!-- END index -->
