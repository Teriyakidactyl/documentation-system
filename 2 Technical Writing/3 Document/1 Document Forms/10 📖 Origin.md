---
uid: DNFDSK
description: >-
  `Consult when` *the `README.md` representing a Documentation System origin
  is being authored or reviewed for conformance* `to` **confirm the required
  compact address legend, root navigation contract, source guidance, and
  placement of its generated immediate-child index**.
quadrant: Reference
outline:
  topology: list
  axis: origin element
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

# 📖 Origin

Addresses are relative to the corpus root, the filesystem directory at the top
of this controlled corpus. `documentation-system:§2.3.2.1` means start at that
directory, then descend through ordinal 2, child 3, child 2, and artifact 1; `#4.2`
selects numbered heading 4.2 inside the resolved artifact. The
`documentation-system:` qualifier names the logical address space independently
of the corpus root's physical path. Every Origin declares that stable name in
its file-level `address-space` metadata. When the corpus carries durable
controlled links into another corpus, its Origin also declares that foreign
address space under `corpus-dependencies` with a path relative to this corpus
root.

> [!IMPORTANT]
> Start here. A task may present several independent concerns; route each one
> separately. For the current concern, compare only the immediate indexed
> choices, select the narrowest matching description, and descend one index at
> a time until the governing artifact is identified. Repeat for every remaining
> concern, satisfying each resulting document according to its directive.

<!--
The address paragraph and callout above are the standard reader-facing entry
contract for an Origin. Keep the address explanation compact: establish the
corpus root as the filesystem directory that is the relative origin of the
address tree, teach decimal path descent and the optional heading suffix, and
distinguish the logical address-space qualifier from the root's physical path.
Leave UID, move, resolution, and compiler mechanics to Document Control.

Keep the navigation behavior intact when adapting wording to a corpus:

- identify each independent concern presented by the task;
- begin at the Origin for the current concern;
- compare that concern only with immediate indexed choices;
- select the narrowest matching description;
- descend through one INDEX.md at a time when another location is selected;
- stop descending that branch when its governing artifact is identified;
- repeat for every remaining concern; and
- satisfy every resulting document according to its directive.

The Origin is README.md at the corpus root. Give it a corpus-specific H1 and a
description that routes a reader into the corpus. Its frontmatter declares one
canonical `address-space` name. Do not derive that logical identity from the
directory name or invocation. When the corpus needs durable controlled links to
another corpus, add `corpus-dependencies` as a mapping from the foreign
address-space name to that corpus root, expressed relative to this corpus root.
The dependency target's own Origin must declare the same address-space name.

The derived README.md carries a `form` controlled link in frontmatter back to
this artifact. A derived Origin in another corpus therefore declares the
Documentation System as a corpus dependency before using that cross-corpus
controlled link. Place the compiler-owned immediate-child index after the
reader-facing navigation contract.

Do not copy this generic guidance block into the derived README.md; the
`form` link keeps this form as its owner.

A minimal derived Origin metadata shape is:

```yaml
---
uid: ABC123
address-space: example-system
corpus-dependencies:
  documentation-system: ../1 Documentation System
form: '<a href="*" uid="DNFDSK">documentation-system:§2.3.1.10</a>'
description: >-
  ...
---
```

Omit `corpus-dependencies` when the corpus has no controlled foreign links.
Dependency declarations are routing configuration, not authority over the
foreign corpus: compiling this corpus may read a dependency to resolve identity
and current address, but must not mutate it.

Add root context only when it is needed before the first routing decision. A
compact glossary can define terms required to interpret the immediate choices.
Folder conventions can appear here when a reader must understand root names
before choosing a location. Otherwise let the selected document own that
information.

Do not hand-author descendant summaries, duplicate child descriptions, or a
parallel navigation map. Generated index content remains owned by the compiler.
-->
