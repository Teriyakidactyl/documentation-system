---
uid: 5NV1K9
description: >-
  `Consult when` *a technical document needs a reusable internal structure
  whose source pattern should remain recognizable across documents* `to`
  **select the Document Element that governs the heading-bounded structure
  before authoring its local content**.
---

# Document Elements

This location collects reusable, heading-bounded document structures. Each
element owns source arrangement and provenance conventions; the consuming
document owns its subject-specific content.

An element may occupy a numbered directory when deterministic support code is
part of using that element. In that representation, the directory's `README.md`
is the Document Element authority and unnumbered implementation and test files
live beside it. Those support files may call common Tooling capabilities for
generic Markdown, YAML, HTML, or other representation mechanics; they do not
move the element's semantic rules into those generic capabilities.

Every tracked Document Element authority declares a major.minor contract under
`version.value`. An instance records that consumed version together with
`element.path.uid` and `element.path.filepath`. Non-dynamic instances retain
that provenance until deliberately migrated. Dynamic heading-bounded Elements
also record a controlled Python `renderer`; a successful render updates the
generated representation and its recorded Element version together.

The version policy may use the same optional `info`, `warn`, and `error`
keys as a Document Form: informational drift is on by default, while warning
and error thresholds are off unless configured. Atomic representations may
explicitly remain untracked when per-instance metadata would outweigh the
benefit; controlled HTML links are the current example.

## Index
<!--
element:
  path:
    uid: BZJASV
    filepath: e. Technical Writing/a. Document/a. Document Elements/a. Index/README.md
  version: '2.0'
  renderer:
    uid: 45E225
    filepath: f. Tooling/Navigation Crawler.py
-->

### 📖 Comparison Matrix

`Consult when` *several peer entities must be compared across the same independent attributes* `to` **represent the peers as rows and shared attributes as columns so differences can be located by intersection**.

<a href="1.%20%F0%9F%93%96%20Comparison%20Matrix.md" uid="Z3X0VE" data-ds-link="relative-path">../1. 📖 Comparison Matrix.md</a>

### 📖 Index

`Consult when` *a controlled folder representation needs deterministic immediate-child navigation* `to` **declare an Index section whose generated body projects only the folder's immediate indexed children**.

<a href="a.%20Index/README.md" uid="BZJASV" data-ds-link="relative-path">../a. Index/README.md</a>

### 📖 Decision Table

`Consult when` *a bounded set of conditions maps deterministically to actions or outcomes and prose would obscure the branch boundaries* `to` **represent each decision rule as a scannable condition-to-result row**.

<a href="2.%20%F0%9F%93%96%20Decision%20Table.md" uid="EEG680" data-ds-link="relative-path">../2. 📖 Decision Table.md</a>

### 📖 Semantic Registry

`Consult when` *named entries need definitions and repeated attributes in one dense lookup surface whose source hierarchy must remain directly readable* `to` **render a column-aligned Semantic YAML registry in which labels, definitions, values, and nesting remain visually distinct without becoming runtime data**.

<a href="b.%20Semantic%20Registry/README.md" uid="81D5SK" data-ds-link="relative-path">../b. Semantic Registry/README.md</a>

### 📖 Glossary

`Consult when` *a document boundary needs a glossary to orient readers to project-specific terms or concepts relevant at that scope* `to` **select only entries required at the reader's current knowledge horizon, define them to the depth needed for correct use, and choose the smallest representation that preserves necessary relationships**.

<a href="3.%20%F0%9F%93%96%20Glossary.md" uid="BJS5BZ" data-ds-link="relative-path">../3. 📖 Glossary.md</a>
