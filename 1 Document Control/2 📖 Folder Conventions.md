---
uid: TRJS8V
description: >-
  `Consult when` *a directory name begins with a reserved prefix and its corpus
  membership, crawler traversal, or access condition is unknown* `to` **confirm
  what the prefix reserves, whether the crawler enters it, and whether reading
  it requires a specific instruction**.
quadrant: Reference
outline:
  topology: list
  axis: name prefix
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

# 📖 Folder Conventions

A *reserved prefix* is the leading character of a directory name that fixes how
the corpus treats that directory. The name following the prefix is a
placeholder. It labels the directory's purpose and carries no meaning to the
crawler, so `.cache`, `.work`, `_staging`, and `_review` each take their
prefix's treatment whatever the rest of the name says.

Two prefixes are reserved. Both mark a directory as holding something other
than indexed documented information.

## 1. Dot prefix

A directory named `.<name>` sits outside the controlled corpus. The crawler
does not descend into it, so nothing beneath it receives a uid, an address, or
a place in any generated index. Use one for repository or tool state, or for
local working material.

Its contents drift. Nothing beneath a dot prefix states current, authoritative
information, and no document elsewhere in the corpus cites into it as though it
did.

An agent does not scan a dot-prefixed directory as part of ordinary work,
including a search that would otherwise reach it. Reading one requires a
specific instruction from the user naming the directory. Silence elsewhere is
not permission.

## 2. Underscore prefix

A directory named `_<name>` holds operational organizing. It groups working
material by handling stage rather than by subject. A numbered location
classifies documented information; an underscore directory stages material that
is not documented information at all.

> [!IMPORTANT]
> The crawler does not act on an underscore prefix. Three directory-name rules
> stop traversal today: a dot prefix, an `old_` prefix, and the literal name
> `__pycache__`. The crawler walks an underscore directory placed directly in
> the corpus like any other unnumbered directory, and indexes any file beneath
> it that carries a `description`.

Nest an underscore directory inside a dot-prefixed directory to keep it out of
the corpus. It then takes that directory's exclusion and its access condition,
and an agent enters it only on a specific instruction.
