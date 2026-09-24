---
uid: BZJASV
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

Use an exact H2 named `Index` in a controlled folder `README.md`. Record
element provenance immediately beneath the heading, then provide the generated
region owned by Organizing:

````markdown
## Index
<!-- element: '<a href="*" uid="BZJASV">documentation-system:§2.3.2.5</a>' -->

<!-- BEGIN index -->
<!-- END index -->
````

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

The heading and `element:` provenance identify the semantic element. The
`BEGIN index` and `END index` comments are the current Organizing write
boundary; they are maintenance mechanics rather than the element's identity.

Organizing currently discovers folder `README.md` representations from the
corpus model and refreshes this region directly. A later general Renderer may
dispatch the same element contract without changing what the Index means.
