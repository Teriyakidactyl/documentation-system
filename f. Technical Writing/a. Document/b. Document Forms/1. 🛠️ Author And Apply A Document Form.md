---
uid: PK9FPF
description: >-
  `Read in full and follow when` *a recurring document role needs a reusable
  Document Form or a document is being derived from one* `to` **create or use
  the folder-backed authoring package that separately specifies the artifact,
  its assembly procedure, and any judgment that requires exemplars**.
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

A Document Form is a controlled authoring package for one recurring document
role. The Form is the concept represented by its numbered directory and
`README.md`; its quadrant documents divide specification, assembly, and
instructional judgment instead of forcing those reader relationships into one
file.

## 1. Confirm the recurring role

Create a Form when multiple documents can occupy the same recurring role and
should make the same structural, metadata, or presentation decisions. Do not
create one for a one-off artifact, a domain fact, or a heading-bounded shape
already owned by a Document Element.

## 2. Create the Form package

Create one numbered directory in Document Forms. Keep ordinals 1–9 for guidance
about Document Forms and place Form packages at ordinal 10 or above.

The package has this minimum shape:

```text
<Form>/
├── README.md
├── 1 📖 <Form>.md
└── 2 🛠️ <Form assembly procedure>.md
```

`README.md` represents the Form concept, carries its stable UID and routing
`description`, declares the Form contract version, and contains the Index
element. It does not carry a `form` link to itself.

Declare the Form contract in that package `README.md`:

```yaml
version:
  value: '1.0'
  info: true
  warn: minor
  error: major
```

Use `major.minor`. Increment `minor` when the contract changes without making
existing conforming instances nonconforming. Increment `major` when an existing
conforming instance may no longer conform. Pure editorial changes that do not
change the contract do not increment the version.

`info` is optional and defaults to `true`; set it to `false` only when stale
contract provenance should produce no informational diagnostic. `warn` and
`error` are optional and disabled when absent. When present, each value is
`minor` or `major` and acts as the minimum drift class for that severity; the
highest applicable configured severity wins.

The Reference and HowTo are both required. Their separate reader relationships
are part of the Form contract, not an optional decomposition discovered later.

## 3. Specify the artifact in Reference

Use the Reference document to define the canonical result: required metadata,
filename grammar, section anatomy, ordering, special terms, required source
constructs, and links to reusable Document Elements.

Show required reader-facing Markdown as live Markdown when doing so cannot
activate generation. Use a fenced specimen when a literal source construct
would otherwise execute maintenance behavior.

Keep assembly procedure out of the Reference. A reader consulting one entry
must be able to confirm what the resulting artifact requires without following
a sequence of authoring steps.

## 4. Define assembly in HowTo

Use the HowTo to tell an author how to produce a conforming instance. Walk the
Reference requirements in the dependency order needed to author them, including
how to determine section content rather than merely repeating that the section
exists.

Link back to the owning Reference entries when a requirement needs lookup. Do
not duplicate the full structural contract in the procedure.

## 5. Add Tutorial for ambiguous judgment

Add a Tutorial when Reference plus HowTo still leave a recurring distinction
that correct authors must learn by contrast. For an agent reader, use paired
good and bad specimens that isolate one distinction at a time and state the
rule separating them.

Do not create a Tutorial merely to repeat the template or procedure. Its
presence is selected by an actual judgment boundary.

## 6. Bind the derived document

Add `form` to the derived document's file frontmatter. Its `path` is the
UID-controlled link to the Form package `README.md`, not to its Reference or
HowTo child; its `version` records the Form contract actually used to author
or last deliberately migrate the instance:

```yaml
form:
  path: '<a href="*" uid="ABC123">documentation-system:§2.3.1.10</a>'
  version: '1.0'
```

The package UID identifies the recurring role. `form.version` is retained
provenance rather than a projection of the Form's current version: do not rewrite
it merely because the Form advances. Organizing compares it with the Form
authority and emits drift according to the Form's `version.info`,
`version.warn`, and `version.error` policy. A document claiming a newer
version than its Form authority knows is invalid provenance and is an error.

The instance still owns its own `description`, quadrant specification, local
content, and document-control state. Form provenance does not create metadata
inheritance.

## 7. Apply and validate the instance

Consult the Form Reference for the target contract, follow its HowTo for
assembly, and use its Tutorial when the authored case crosses a documented
judgment boundary. Keep instance-specific facts in the instance.

Apply Technical Writing to each Form document, Document Control to its
controlled state, and Organizing after package, metadata, heading, or link
changes. Finish when the package Index, Form link, and resulting instance agree
with the filesystem.
