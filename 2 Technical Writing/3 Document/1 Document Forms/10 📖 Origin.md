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

**Corpus root** is a contextual role declared for a filesystem directory; it
is not a permanent designation of that directory. A compiler job declares its
corpus root with the optional `corpus_root` path argument; when omitted, that
job defaults to the root of the Git repository containing the compiler. A
documentation address separately declares its corpus root by directory name
before `:`, and that declaration is required. Thus
`documentation-system:§2.3.2.1` declares this directory as the corpus root for
that address, then descends through ordinal 2, child 3, child 2, and artifact 1;
`#4.2` selects numbered heading 4.2 inside the resolved artifact. `§2.3.2.1` without a corpus-root declaration is location notation, not a
valid documentation address.

> [!IMPORTANT]
> Start here. A task may present several independent concerns; route each one
> separately. For the current concern, compare only the immediate indexed
> choices, select the narrowest matching description, and descend one index at
> a time until the governing artifact is identified. Repeat for every remaining
> concern, satisfying each resulting document according to its directive.

<!--
The address paragraph and callout above are the standard reader-facing entry
contract for an Origin. Keep the address explanation compact: establish the
corpus root as a contextual role rather than a permanent directory property.
State that a compiler job declares the role by filesystem path, with the
Git-repository-root default when the path argument is omitted, and that a
documentation address separately declares the role by directory name before
`:`. Teach
decimal location descent and the optional heading suffix. Make clear that
`§...` notation without a corpus-root declaration is not an address. Leave UID, move, and detailed
compiler mechanics to Document Control.

Keep the navigation behavior intact when adapting wording to a corpus:

- identify each independent concern presented by the task;
- begin at the Origin for the current concern;
- compare that concern only with immediate indexed choices;
- select the narrowest matching description;
- descend through one INDEX.md at a time when another location is selected;
- stop descending that branch when its governing artifact is identified;
- repeat for every remaining concern; and
- satisfy every resulting document according to its directive.

For a compiler job, the Origin is `README.md` at the directory serving as that
job's corpus root. Give it a corpus-specific H1 and a description that routes a
reader into the corpus. Do not add a persistent corpus-root field: the job
declares the role by path, while each address declares the role for itself by
directory name.
The derived README.md carries a `form` controlled link in frontmatter back to
this artifact. Place the compiler-owned immediate-child index after the
reader-facing navigation contract.

Do not copy this generic guidance block into the derived README.md; the
`form` link keeps this form as its owner.

Add root context only when it is needed before the first routing decision. A
compact glossary can define terms required to interpret the immediate choices.
Folder conventions can appear here when a reader must understand root names
before choosing a location. Otherwise let the selected document own that
information.

Do not hand-author descendant summaries, duplicate child descriptions, or a
parallel navigation map. Generated index content remains owned by the compiler.
-->
