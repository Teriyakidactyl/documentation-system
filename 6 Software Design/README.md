---
uid: 1SGQXT
description: >-
  `Consult when` *a software design concern must be resolved before its
  implementation pattern or boundary is chosen* `to` **select the canonical
  Software Design guidance that fixes the repository's default decision**.
---

# Software Design

This location collects reusable software-design guidance for agent and human
implementation work.

Software Design is organized primarily around recurring design concerns whose
decisions arise independently across systems and architectures. Software Design
Principles supplies defaults inherited across those concerns. Architecture
guidance explains when several resolved decisions warrant durable implemented
architecture and how that authority is kept with the code it governs.

Prefer documented defaults and established concern architectures over reopening
equivalent alternatives. Add another Software Design concern when recurring use
establishes an independently routable decision domain; do not pre-create a
maximal taxonomy from a framework or book.

## Index
<!--
element:
  path:
    uid: BZJASV
    filepath: 2 Technical Writing/3 Document/2 Document Elements/5 Index/README.md
  version: '2.0'
  renderer:
    uid: 45E225
    filepath: 4 Tooling/1 🛠️ Navigation Crawler.py
-->

### 📖 Software Design Principles

`Consult when` *a software design decision admits several plausible implementations or an existing implementation boundary is being materially changed* `to` **apply the Documentation System's canonical defaults for concepts, ownership, classes, modules, validation, and projections without reopening equivalent alternatives**.

<a href="1%20%F0%9F%93%96%20Software%20Design%20Principles.md" uid="M8MDHY" data-ds-link="relative-path">../1 📖 Software Design Principles.md</a>

### Architecture

`Consult when` *implemented code needs durable architecture authority or an existing architecture must be located, reviewed, or changed* `to` **route between the Implemented Architecture reference and the procedure for designing, recording, colocating, and maintaining that authority**.

<a href="2%20Architecture/README.md" uid="20KRDM" data-ds-link="relative-path">../2 Architecture/README.md</a>

- `1 📖 Implemented Architecture.md`
- `2 🛠️ Design And Record An Implemented Architecture.md`

### Error Management

`Consult when` *software failure behavior must be designed or an established error architecture must be selected* `to` **route between general error management concepts and formal architectures that apply those concepts under recurring consumer constraints**.

<a href="3%20Error%20Management/README.md" uid="TJBYJ1" data-ds-link="relative-path">../3 Error Management/README.md</a>

- `1 📖 Error Management.md`
- `2 Architectures/README.md`

### Testing

`Consult when` *software behavior or architecture requires executable verification, or an established verification architecture must be selected* `to` **route between general testing principles and formal architectures that implement those principles for recurring verification surfaces**.

<a href="4%20Testing/README.md" uid="R0J5KF" data-ds-link="relative-path">../4 Testing/README.md</a>

- `1 📖 Testing.md`
- `2 Architectures/README.md`
