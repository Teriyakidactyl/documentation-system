---
uid: BZJASV
description: >-
  `Consult when` *an `INDEX.md` representing a controlled location is being
  authored or reviewed for conformance* `to` **confirm its location blurb,
  optional local convention, and crawler-owned immediate-child index are
  arranged without duplicating generated navigation**.
quadrant: Reference
outline:
  topology: list
  axis: index element
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

A derived `INDEX.md` contains a location title, a compact authored blurb, an
optional local convention needed before the first routing choice, and one
crawler-owned immediate-child index.

```markdown
# [Location name]

[One compact blurb stating what the location collects and, when necessary,
what it does not own.]

[Optional local convention required to interpret the immediate choices.]

&lt;!-- BEGIN index --&gt;
&lt;!-- END index --&gt;
```

<!--
The marker lines are escaped in this form so the crawler does not treat the
form itself as a projection owner. In a derived INDEX.md, write the literal
HTML comments named BEGIN index and END index using normal angle-bracket
comment syntax.

The derived INDEX.md carries a file-level `form` controlled link back to this
artifact. Keep the title location-specific. Keep the blurb authored and
compact; it defines the location boundary rather than summarizing its children.

Add the optional local convention only when a reader must know it before
choosing among immediate children. Standard Forms, for example, states its
ordinal reservation before the generated region.

Place exactly one crawler-owned region after authored context. Do not hand-list
children, copy child descriptions, or put authored prose inside that region.
-->
