---
uid: BJS5BZ
description: >-
  `Consult when` *related terms must be defined without losing the hierarchy
  that distinguishes parent, child, and sibling concepts* `to` **pair a
  relationship tree with a lookup table whose definition column explains each
  named term**.
quadrant: Reference
outline:
  topology: list
  axis: element facet
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

# 📖 Hierarchical Glossary

## Anatomy

A hierarchical glossary is one heading-bounded element containing a relationship
tree followed by a two-column definition table. The tree answers how the terms
relate; the table answers what each term means.

## Source specimen

```markdown
## Terms
<!-- element: [controlled link to this Document Element] -->

```text
request
├── identity
└── routing
```

| Term | Meaning |
|---|---|
| **request** | One unit of work entering the system. |
| **identity** | The durable identifier carried by the request. |
| **routing** | The rule that selects the request's destination. |
```

## Constraints

Keep the tree and table in the same order when practical. Use one canonical
name per concept. Keep the definition column left-aligned and prose-oriented;
do not turn it into a second hierarchy. The element heading owns the complete
tree-plus-table unit.

Instances record provenance with `element:` metamatter as defined by
<a href="../1%20%F0%9F%9B%A0%EF%B8%8F%20Write%20A%20Technical%20Document.md#12-choose-the-container" uid="5CFFZW">documentation-system:§2.1#1.2</a>.
