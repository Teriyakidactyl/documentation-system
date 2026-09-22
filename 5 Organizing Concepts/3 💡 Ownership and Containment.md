---
uid: W9D5TG
description: >-
  `Read in full when` *the place holding an item and the concept responsible
  for it are being treated as the same thing* `to` **separate containment from
  ownership and choose the owner before domain-specific placement rules
  determine the container**.
quadrant: Explanation
outline:
  numbering: hierarchical-decimal
writing-style:
  formality: professional
  tone: collegial/earnest
  mode: declarative
  density: moderate
  abstraction: mixed
  redundancy: zero
  signposting: suppressed
  register: accessible
---

# 💡 Ownership and Containment

Containment answers where an item is held. Ownership answers which concept is
responsible for the item's meaning and invariants. They often coincide, which
makes them easy to confuse, but neither implies the other.

## 1. Containment

A container is a representation boundary: a file, directory, heading, object,
module, table, or other structure that physically or syntactically holds an
item. Containers are often chosen under constraints unrelated to conceptual
ownership: delivery format, runtime behavior, addressability, tool syntax, or
reader navigation.

Moving an item can therefore change its container without changing what owns
it.

## 2. Ownership

An owner is the smallest stable concept whose responsibility includes the fact,
rule, behavior, or relation being placed. The owner is where a reader should
look to learn why the item exists and which invariant would be violated by
changing it.

Ownership is semantic rather than physical. Several independently owned facts
may share one file, while one concept may be represented across several files.

## 3. Proximity

Physical proximity is weak evidence of ownership. An item can be placed in the
file already open because it concerns the same host, uses the same variable, or
touches the same subsystem while still belonging to a different responsibility.

That error is durable: later work sees the first placement and treats it as
precedent. Proximity then compounds into a false boundary.

Naming the owner before choosing the container prevents the current workspace
from becoming the taxonomy.

## 4. Divergence

When ownership and containment differ, state both relationships:

```text
owner      → concept responsible for the item
container  → representation in which the item currently resolves
constraint → reason the owner is represented there
```

The container should point toward the owner when a reader would otherwise infer
the wrong responsibility. Do not duplicate the owner's reasoning locally merely
to make the container look self-contained.

## 5. Domain-specific placement

Ownership does not choose a filesystem path, heading number, package, schema
key, or runtime boundary by itself. It establishes the conceptual unit that a
domain-specific procedure then represents.

For documented information, document control can turn ownership into a
classification location and address. For a document outline, technical writing
can turn it into a heading boundary. Software architecture may turn it into a
module, package, type, or dependency boundary under constraints that
Documentation System does not define.

The shared rule is only that representation follows an identified owner rather
than inventing one from physical containment.
