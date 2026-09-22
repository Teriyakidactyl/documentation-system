---
uid: M4R8XC
description: >-
  `Read in full and follow when` *a non-trivial item must be placed into an
  existing structure or more than one placement plausibly fits* `to` **test the
  candidate against topology, relation, axis, granularity, ownership, and
  coverage, then confirm it or surface the unresolved ambiguity instead of
  guessing**.
quadrant: HowTo
outline:
  topology: linear
  numbering: hierarchical-decimal
writing-style:
  formality: professional
  tone: neutral/detached
  mode: imperative
  density: moderate
  abstraction: concrete/specific
  redundancy: zero
  signposting: light
  register: technical
---

# 🛠️ Test A Placement

Use this procedure before domain-specific placement rules when conceptual fit is
not obvious. It decides what relation and owner justify a placement, not the
filesystem path, heading syntax, module boundary, or other representation a
caller may impose afterward.

## 1. Identify the topology

Name the topology of the layer receiving the item. Consult
<a href="2%20%F0%9F%93%96%20Structural%20Topologies.md" uid="P6V2HN">documentation-system:§5.2</a>
and choose the relation that the structure actually preserves: tree, list,
matrix, or graph.

Do not infer topology from visual nesting alone. Folders, YAML keys, headings,
and object fields can render different relations with the same indentation. Ask
what makes the existing siblings belong at this layer and what information
would be lost if their relation changed.

A structure may use different topologies at different depths. That is valid
when each layer has a clear relation of its own.

## 2. Name the relation to the parent

Distinguish a subtype from a slot before accepting nested placement.

- **Is-a.** `X` is a kind of `Y` regardless of which instance of `Y` is meant.
  This is a classification relation.
- **Part-of.** `X` is a constituent of `Y` and the containment is part of the
  model being represented.
- **Has-a.** `Y` carries an `X` as a slot or property, and another `Y` can carry
  a different value under the same slot name.
- **Edge relation.** The important fact is a named connection such as
  `depends on`, `calls`, or `blocks`; the relation belongs in a graph rather
  than being implied by containment.

Repeated names are not automatically collisions. A property such as `port`
may occur under unrelated owners because the slot repeats while its value does
not. Conversely, a subtype repeated in two exclusive branches means the
classification has not resolved the item.

If neither relation fits convincingly, or more than one fits for independent
reasons, keep the ambiguity open and continue to §7 rather than choosing the
nearer-looking branch.

## 3. Check the layer's axis

A sibling layer organized as a classification or ordered list answers one
question. If one sibling groups by function while another groups by component,
the layer carries two axes and an item can plausibly belong to both for
unrelated reasons.

Choose the dimension that the layer actually owns. Move the other concern to a
different layer or represent it as an independent attribute. A matrix carries
several independent axes by design; do not simulate those combinations by
mixing the axes as sibling categories.

## 4. Judge the granularity

Give a grouping depth only when the grouping is real.

Pull an isolated leaf back up when no sibling can reasonably join it. Nest two
or more items when they already share a stable relation that distinguishes the
group from its peers. A parent must remain more abstract than every child it
contains; if parent and child can exchange names without changing the meaning,
the hierarchy is false.

Do not add depth merely because a template has room for it, and do not keep a
real group flat merely to avoid adding structure.

## 5. Find the owner

Apply
<a href="3%20%F0%9F%92%A1%20Ownership%20and%20Containment.md" uid="W9D5TG">documentation-system:§5.3</a>.
The file, folder, heading, object, or other container already in front of you is
not evidence that it owns the new item.

Name the smallest stable concept whose responsibility includes the item. When
that owner and the physical container differ, name both rather than letting
containment imply ownership.

## 6. Check overlap and gaps

Check the candidate structure for the two halves of MECE where exclusivity is
actually claimed.

**Overlap.** An item should not compete between exclusive siblings for
independent reasons. If it does, revisit the relation or axis. Do not force this
test onto a matrix: combinations across independent axes are expected, not a
classification collision.

**Gap.** A new item that fits only after stretching every candidate definition
has exposed missing structure. Test for a gap cheaply in two ways:

1. Invert a category's apparent claim to completeness: ask what would *not*
   belong there, then look for a real example.
2. Try a concrete counter-example from the same kind of domain problem and ask
   where the current structure would place it without changing a definition.

A counter-example confirms a gap. Failing to find one is evidence, not proof,
that the structure is exhaustive.

## 7. Resolve or escalate

Confirm the placement only when the preceding checks agree on the same
relation, axis, granularity, owner, and coverage.

When they do not, state the unresolved primitive and the competing placements.
Do not hide the uncertainty by selecting one. Escalate before establishing a
new root, a widely reused category, or another decision that later placements
will inherit. A caller may impose a stricter human-review gate; this procedure
sets the minimum rule that unresolved structure is surfaced rather than guessed.
