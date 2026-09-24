---
uid: BZJASV
version:
  value: '1.0'
description: >-
  `Consult when` *a controlled folder representation needs deterministic
  immediate-child navigation* `to` **declare an Index section whose generated
  body projects only the folder's immediate indexed children**.
quadrant: Reference
outline:
  topology: list
  axis: index facet
writing-style:
  formality: professional
  tone: clinical/detached
  mode: declarative
  density: compressed/dense
  abstraction: concrete/specific
  redundancy: zero
  signposting: entry-headers only
  register: technical
---

# 📖 Index

An Index is a heading-bounded Document Element deployed in the `README.md`
that represents a controlled folder. It projects immediate indexed children
from canonical corpus structure; it does not create a second authored topology.

## Anatomy

Use an H2 to bound the Index Element in a controlled folder `README.md`.
Record the dynamic Element declaration immediately beneath the heading:

````markdown
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
````

The declaration identifies the Element contract, the version currently embodied
by the generated section, and the controlled Python renderer that owns
regeneration. A successful render rewrites the generated body and stamps the
renderer-supported Element version in the same operation.

The repository-root `README.md` uses the same element. Its additional origin
contract does not change the Index element.

## Projection

Each generated entry represents one immediate indexed child and contains the
child's UID-controlled link, title, and exact controlled `description`.
Ordering follows the active organization scheme.

Do not hand-author descendant summaries, duplicate deeper navigation, or put
authored prose inside the generated region. Put folder-specific authored context
before the Index heading.

## Boundary

The `element.path.uid` identifies the semantic Element. The heading containing
that metamatter supplies the structural boundary; the heading text itself is not
Element identity. Organizing replaces the remainder of that heading-bounded
section rather than relying on generated-region marker comments.

`element.path.filepath` and `element.renderer.filepath` are current physical
projections associated with their durable UIDs. When those targets participate
in the selected corpus, Organizing refreshes the filepaths from UID identity.
The renderer owns the generated body and the deployed `element.version`;
authored context remains outside the Index section.
