---
uid: P6V2HN
description: >-
  `Consult when` *the relation governing a structural layer is unclear* `to`
  **distinguish tree, list, matrix, and graph topology by the relation each
  preserves and the failure signal each exposes**.
quadrant: Reference
outline:
  topology: list
  axis: topology
  numbering: hierarchical-decimal
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

# 📖 Structural Topologies

A *topology* names the relation a structural layer preserves. It describes why
items belong together, not how indentation, folders, headings, keys, or other
syntax happen to render them.

## 1. Tree

**Relation:** strict `is-a` or `part-of` hierarchy.

Use a tree when traversal moves from a broader parent to a more specific subtype
or constituent and each node has one parent within that relation.

**Failure signal:** an item must live in two branches for independent reasons,
or a parent is not more abstract than its children. The layer is probably
mixing axes or representing independent attributes as hierarchy.

## 2. List

**Relation:** one meaningful order.

Use a list when sequence, priority, dependency order, or another single ordering
dimension is part of the information.

**Failure signal:** reordering the members changes nothing relevant. The
ordering is then presentation rather than organizing structure.

## 3. Matrix

**Relation:** independent, orthogonal attributes that may combine.

Use a matrix when an item is selected or described by several axes at once and
valid combinations are expected.

**Failure signal:** every attribute combination becomes another branch in a
deep tree. Represent the independent dimensions independently rather than
encoding their Cartesian product as containment.

## 4. Graph

**Relation:** explicit edges between nodes.

Use a graph when connections such as `depends on`, `calls`, `blocks`, or
`routes to` carry information equal to the nodes themselves.

**Failure signal:** moving a node into a folder or branch erases, hides, or
falsely implies one of the relationships. Store the edge explicitly instead of
making containment stand in for it.

## 5. Mixed structures

A larger structure may change topology across layers. A tree of components can
contain an ordered procedure; a matrix-selected entity can expose a tree of
parts; a graph node can contain ordinary fields.

The change is valid when each layer has one legible governing relation. Do not
call unrelated sibling relations a mixed topology at the same layer; that is an
unresolved axis.
