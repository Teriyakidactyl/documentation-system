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

## Index
<!-- element: '<a href="5%20Index/README.md" uid="BZJASV">documentation-system:§2.3.2.5</a>' -->

<!-- BEGIN index -->
<!-- This block is owned by Organizing; run Organizing refresh whenever indexed information or organization may have changed. -->

- <a href="1%20%F0%9F%93%96%20Hierarchical%20Glossary.md" uid="BJS5BZ">documentation-system:§2.3.2.1</a> — 📖 Hierarchical Glossary
  - `Consult when` *related terms must be defined without losing the hierarchy that distinguishes parent, child, and sibling concepts* `to` **pair a relationship tree with a lookup table whose definition column explains each named term**.
- <a href="2%20%F0%9F%93%96%20Decision%20Table.md" uid="EEG680">documentation-system:§2.3.2.2</a> — 📖 Decision Table
  - `Consult when` *a bounded set of conditions maps deterministically to actions or outcomes and prose would obscure the branch boundaries* `to` **represent each decision rule as a scannable condition-to-result row**.
- <a href="3%20%F0%9F%93%96%20Comparison%20Matrix.md" uid="Z3X0VE">documentation-system:§2.3.2.3</a> — 📖 Comparison Matrix
  - `Consult when` *several peer entities must be compared across the same independent attributes* `to` **represent the peers as rows and shared attributes as columns so differences can be located by intersection**.
- <a href="4%20Semantic%20Registry/README.md" uid="81D5SK">documentation-system:§2.3.2.4</a> — 📖 Semantic Registry
  - `Consult when` *named entries need definitions and repeated attributes in one dense lookup surface whose source hierarchy must remain directly readable* `to` **render a column-aligned Semantic YAML registry in which labels, definitions, values, and nesting remain visually distinct without becoming runtime data**.
- <a href="5%20Index/README.md" uid="BZJASV">documentation-system:§2.3.2.5</a> — 📖 Index
  - `Consult when` *a controlled folder representation needs deterministic immediate-child navigation* `to` **declare an Index section whose generated body projects only the folder's immediate indexed children**.
<!-- END index -->
