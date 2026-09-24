---
uid: P6V2HN
description: >-
  `Consult when` *structural units are known but the relationship, axis, or
  topology that organizes them is unclear* `to` **name the governing relation
  and axis first, then select tree, list, matrix, or graph without letting a
  representation invent the structure**.
quadrant: Reference
outline:
  topology: list
  axis: structural relation
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

# 📖 Relationships and Structural Topologies

A structural relationship states why established units are connected. A
*topology* is the shape that preserves that relationship. Choose the relation
before the topology; folders, indentation, headings, object fields, and other
syntax can render the same visual shape while meaning different things.

This reference assumes the unit boundaries are already established. When the
relationship problem exposes a compound or unstable unit, return to
<a href="1%20%F0%9F%9B%A0%EF%B8%8F%20Determine%20Structural%20Units.md" uid="YF43JX">documentation-system:§5.1</a>
rather than choosing a relation that only fits the current representation.

## 1. Classification

**Relation:** `is-a`.

`X is a Y` remains true regardless of which instance of `Y` is meant.
Classification normally uses a **tree** when each subtype has one parent under
the selected classification axis.

A subtype that must occupy two exclusive branches for independent reasons
signals mixed axes or an unresolved boundary.

## 2. Composition

**Relation:** strict `part-of` or local `has-a`.

Use **part-of** when the child is a constituent of the parent and that
constituency is part of the model. Use **has-a** when the parent carries a named
slot or property and different parent instances may carry different values in
that slot.

Strict composition can use a **tree** when each constituent has one parent
inside the modeled relation. Repeated slot names under different owners are not
automatically collisions; their qualified relationships differ.

Do not treat visual nesting as proof of either composition or classification.

## 3. Meaningful order

**Relation:** one canonical sequence, dependency order, priority, or other
ordering dimension.

Use a **list** when position carries information.

**Failure signal:** reordering the members changes nothing relevant. The order
is then presentation rather than organizing structure.

## 4. Independent axes

**Relation:** orthogonal attributes that may combine.

Use a **matrix** when a unit is selected or described by several independent
dimensions and valid combinations are expected.

**Failure signal:** every attribute combination becomes another branch in a
deep tree. Preserve the dimensions independently rather than encoding their
Cartesian product as containment.

## 5. Explicit edges

**Relation:** a named connection such as `depends on`, `calls`, `blocks`,
`routes to`, or another edge whose identity matters.

Use a **graph** when the connections carry information equal to the nodes.

**Failure signal:** moving a node into a folder or branch erases, hides, or
falsely implies one of its relationships. Store the edge explicitly instead of
making containment stand in for it.

## 6. Layer axis

A relationship says how units connect. An **axis** says which question selects
siblings within one classificatory or ordered layer.

Keep one such question per layer. A sibling set where one member groups by
function and another groups by component mixes axes even if both can be drawn
as a tree. Move the independent concern to another layer or represent
independent dimensions as a matrix.

An axis is not required for every topology. Graph edges carry their own named
relations, and a composition can be meaningful without forming an exclusive
classification.

## 7. Mixed structures

A larger structure may change topology across layers. A tree of components can
contain an ordered procedure; a matrix-selected entity can expose a tree of
parts; a graph node can contain ordinary fields.

The change is valid when each layer has one legible governing relation of its
own. Unrelated sibling relations at the same layer are not a mixed topology;
they are an unresolved axis.

When two relationship readings both remain valid, keep the ambiguity open.
Ownership or placement must not choose a topology merely because one
representation is convenient.

Once the relationship, applicable axis, and topology are established, resolve
semantic ownership separately with
<a href="3%20%F0%9F%92%A1%20Ownership%2C%20Containment%2C%20and%20Convergence.md" uid="W9D5TG">documentation-system:§5.3</a>
when that question remains open.
