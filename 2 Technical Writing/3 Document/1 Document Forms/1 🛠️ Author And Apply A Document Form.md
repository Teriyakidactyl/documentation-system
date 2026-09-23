---
uid: PK9FPF
description: >-
  `Read in full and follow when` *a recurring repository document role needs a
  reusable Document Form or a document is being derived from one* `to`
  **author the canonical form, bind each derived document back to it, and keep
  recurring guidance owned by the form instead of copied into instances**.
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

# 🛠️ Author And Apply A Document Form

A Document Form captures stable source structure and authoring guidance for a
recurring document role. It is not a template engine and does not own
instance-specific content. A controlled Document Form is the adopted standard
for its role; standardization is its authority, not its concept type.

## 1. Confirm the recurring role

Create a form when multiple documents can occupy the same repository role and
should make the same structural or presentation decisions. Do not create one
for a one-off artifact, a domain fact, or a shape already owned by a more
specific procedure.

## 2. Author the canonical form

Create a Reference artifact in Document Forms. Keep ordinals 1–9 for guidance
about Document Forms and place reusable forms at ordinal 10 or above. Show
required reader-facing Markdown as live Markdown so the rendered form
demonstrates the intended result. Place author guidance in an ordinary HTML
comment immediately after the element it governs.

Use those comments to distinguish required behavior, adaptable wording,
optional material, and forbidden duplication. Keep only rules that recur
across instances. A form does not carry a `form` link to itself.

When a required source construct cannot be live in the form because it would
activate generation or another maintenance mechanism, show the nearest safe
reader-facing specimen and state the exact source requirement in its adjacent
comment.

## 3. Bind the derived document

Add `form` to the derived document's file frontmatter as a controlled link to
the governing form:

```yaml
form: '<a href="*" uid="ABC123">documentation-system:§2.3.1.10</a>'
```

Use the form's real UID and current address. The compiler owns the link target
and displayed address after that. Keep the `form` field when the instance is
moved or locally adapted.

The form records provenance, not inheritance. The derived document still owns
its own `description`, quadrant specification, local content, and document
control state.

## 4. Apply the instance-specific content

Preserve the form's required structure and behavior while replacing
corpus-specific names, routing language, and other local facts. Add an optional
form element only when its stated condition is true for the instance.

Do not copy the form's generic author-guidance comments into the derived
document. Add a local maintenance comment only for an instance-specific reason;
otherwise follow the `form` link back to the owning guidance.

## 5. Validate the result

Apply Technical Writing to the authored or revised document, apply Document
Control to its controlled state, then run the Documentation Compiler. Finish only
when the form link resolves and the generated projections agree with the
filesystem.
