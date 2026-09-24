---
uid: 0AQHNH
description: >-
  `Read in full and follow when` *documented information is created, moved,
  renamed, indexed, linked, or otherwise brought under repository control* `to`
  **keep its durable identity, applicable address and index state, and
  controlled relationships valid**.
quadrant: HowTo
outline:
  topology: branching
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

# 🛠️ Control Documented Information

Apply these steps to an existing artifact or to the output of an authoring
procedure. For each Organizing job, the declared corpus root and filesystem
hierarchy own classification and location. Each documentation address makes its
own corpus-root declaration by directory name, then names a location beneath
that declared root. A `uid` owns durable document identity; a numbered internal
outline can extend an address into a file. Recognized metadata makes an artifact
controlled. An addressable position additionally makes it indexable. Organizing derives indexes from the corpus hierarchy established for the current
job; controlled sideband artifacts can retain identity and validation without
entering that navigation surface.

**Terms.** One name per concept, with relationships shown before definitions:

```text
corpus root
├── declared by Organizing job
│   └── bounds corpus
│       ├── controlled artifact
│       │   ├── uid
│       │   ├── description
│       │   ├── indexed artifact
│       │   └── controlled sideband artifact
│       └── origin
│           └── README.md
│               └── index
└── declared by address
    └── anchors location
        ├── location ordinal
        └── README.md
            └── index
```

| Term | Meaning |
|---|---|
| **corpus root** | A contextual role declared for a filesystem directory, not a permanent property of that directory. An Organizing job declares its corpus root by filesystem path; when omitted, that job defaults to the Git repository root containing Organizing. A documentation address separately declares its corpus root by directory name before `:`; omission is a syntax error. |
| **corpus** | The controlled artifacts and locations discovered beneath the corpus root declared for the current Organizing job. |
| **origin** | The reader-facing entry role of a corpus, carried by the `README.md` in the directory serving as corpus root for the current Organizing job. The root README uses the ordinary folder representation plus the additional corpus-entry contract required before the first routing choice. |
| **controlled artifact** | A file on an Organizing-traversed path whose supported metadata surface contains a `description` and Organizing-minted `uid`. It participates in durable identity and validation whether or not it has an address. |
| **indexed artifact** | A controlled artifact whose filesystem position derives an address and can therefore participate in generated index navigation. |
| **controlled sideband artifact** | A controlled artifact stored in a reserved sideband whose retrieval policy excludes it from normal index navigation. It keeps a UID and validation participation but has no Documentation System address. |
| **uid** | A permanent six-character Crockford Base32 identifier minted by Organizing for one controlled artifact. It survives moves and renames; duplicate UIDs are invalid. |
| **description** | The canonical Markdown routing statement for a controlled artifact. Indexed projections reuse it where the artifact participates in routing. |
| **location** | A position in the corpus hierarchy defined by the filesystem. A numbered directory defines an addressable location whether or not it contains `README.md`. |
| **location ordinal** | A local numeric position read from the start of a numbered directory or numbered artifact name. The accepted prefix is `^([0-9]+)(?:\.\s+|\s+)`, so both `9 Name` and `9. Name` carry ordinal `9`. |
| **address** | A machine-resolvable identifier such as `documentation-system:§2.1#4.2`. The required prefix before `:` declares the corpus root by directory name; the `§` path is derived from location ordinals beneath that declared root; optional `#` extends into a numbered heading. A bare form such as `§2.1` omits the required corpus-root declaration, is invalid address syntax, and is unresolvable. |
| **`README.md`** | The reader-facing representation of its containing folder. In a numbered directory it contributes no location ordinal and resolves to that location's address; at the selected corpus root it carries the origin role and no location address of its own. |
| **index** | The Document Element declared by an `## Index` section in a folder `README.md`; its generated body projects that folder's immediate indexed children as controlled link, title, and exact `description`. |
| **progressive disclosure** | The reader behavior enabled by traversing successive indexes and exposing only the next immediate choices needed. |
| **Organizing** | The Tooling capability that declares a corpus root for each job, scans supported metadata surfaces beneath it, maintains controlled identity and organization, derives navigation projections, refreshes controlled links, reports diagnostics, resolves locators, and plans deterministic structural normalization. |

## 1. Declare the corpus root

Declare the **corpus root** for the Organizing operation by passing its filesystem
path as the optional `corpus_root` argument. When that argument is omitted, Organizing selects the root of the Git repository containing Organizing. The
declaration is operational state; do not store a second corpus-root name in
artifact metadata.

For that Organizing job, the selected directory **serves as** the corpus root.
The role belongs to the declaration and job, not permanently to the directory;
the same directory may be a corpus root in one job and an ordinary descendant
or unrelated path in another.

An address makes its own corpus-root declaration: the directory name before
`:` designates which directory serves as the root for that address. When Organizing resolves an address, that declared name must match the directory
selected as the corpus root for the current job. Changing only that directory's
ancestor path does not change addresses that declare it. Renaming the directory
changes the corpus-root declaration in addresses that use it. A directory name
containing `:` cannot be represented by the address grammar and cannot serve as
a corpus root for Organizing or addressing.

A file becomes a controlled artifact only when it is on an Organizing-traversed
path beneath the selected corpus root and Organizing recognizes its metadata
surface. Address and index participation are additional properties rather than
requirements for controlled identity.

Organizing currently recognizes two shapes:

- Markdown: YAML frontmatter fenced by `---` at the start of the file.
- Python: YAML frontmatter fenced by `---` at the start of the module docstring.

Both normalize into the same metadata model. A Python module therefore does
not need a companion Markdown document merely to participate in control. Add a
new source format by adding a metadata adapter; do not change the address model
for each file type.

Do not infer that every file under the corpus root is controlled information.
Presence establishes physical location; Organizing traversal plus recognizable
metadata establishes controlled participation. Addressability determines index
participation separately.

Most dot-prefixed directories remain outside the controlled corpus. Reserved
exceptions can define a controlled sideband when information needs durable UID
identity and Organizing validation without normal routing. The current reserved
behavior is defined by
<a href="2%20%F0%9F%93%96%20Folder%20Conventions.md" uid="TRJS8V">documentation-system:§1.2</a>.
Apply
<a href="3%20%F0%9F%93%96%20Repository%20Information%20Storage.md" uid="S9HVWB">documentation-system:§1.3</a>
before introducing another sideband representation.

On a normal refresh, Organizing adds a missing `uid` to each controlled
artifact. Never change an existing UID because an artifact moved or was renamed.
Copying a controlled artifact also copies its UID, so the duplicate must be
replaced by a newly minted UID before the corpus can refresh.

## 2. Place information in the location hierarchy

Use the existing repository hierarchy before creating another one. Numbered
directories define classification locations. Numbered artifacts occupy
terminal positions within those locations. Unnumbered directories may organize
files physically but contribute no location component.

When a reserved controlled sideband is selected by Folder Conventions, place
the artifact there instead of the address hierarchy. A controlled sideband is
address-opaque: its descendants receive no Documentation System address and do
not enter generated indexes. After sideband placement, continue at step 5.

For example:

```text
2 Conventions/
├── README.md
└── 11 Technical Writing/
    ├── README.md
    └── 9 Write A Technical Document.md
```

contains these ordinal paths relative to the corpus root declared for the
Organizing job:

```text
2       2 Conventions/
2       2 Conventions/README.md
2.11    2 Conventions/11 Technical Writing/
2.11    2 Conventions/11 Technical Writing/README.md
2.11.9  2 Conventions/11 Technical Writing/9 Write A Technical Document.md
```

Use one ordinal once among physical siblings in the current corpus state. A
numbered directory and a numbered artifact with the same ordinal under one
parent collide even when their names differ.

An ordinal is a current structural coordinate, not durable identity. After an
item moves or is removed, its former ordinal may be reused. Preserve durable
identity with the artifact's UID rather than reserving historical coordinates.

## 3. Derive and use addresses

Treat the selected corpus structure as the source of truth. Derive the target's
**location** by walking from the corpus root, taking each location ordinal, and
appending a terminal artifact ordinal when the target is not `README.md`. Join
those ordinals with `.`. Form the address by declaring the corpus root's
directory name before `:`, then prefixing the ordinal path with `§`:

```text
2 Technical Writing/
└── 1 🛠️ Write A Technical Document.md

documentation-system:§2.1
```

A numbered heading extends the complete address into the resolved file after
`#`:

```text
address        = corpus-root ":" "§" location-ordinal ("." location-ordinal)* ["#" heading-number]
corpus-root    = directory name declared as corpus root by the address
heading-number = integer ("." integer)*

documentation-system:§2.1
documentation-system:§2.1#4.2
```

`§2.1` and `§2.1#4.2` are bare corpus-root addresses: each omits the
required corpus-root declaration, is syntactically invalid, and cannot resolve.
The periods express hierarchical descent on either side of `#`; `#` marks
the boundary between filesystem location and the file's internal outline.

An address is a current coordinate. Moving an addressed item within the corpus
changes its location portion, and a former coordinate may later identify
different information. Moving a directory that an address declares as its
corpus root to another parent without renaming it leaves that address unchanged
because the declaration uses the directory's name, not its ancestor path.
Renaming that directory changes the corpus-root declaration in addresses that
use it. The UID does not change when an artifact moves.

Use a controlled HTML anchor when the reference must survive a move or rename:

```text
control-link = '<a href="' physical-target '" uid="' uid '">' address '</a>'
uid          = 6 Crockford Base32 characters
```

For example:

```html
<a href="*" uid="5CFFZW">documentation-system:§2.1#4.2</a>
```

The `uid` identifies the document within the selected corpus; the optional
`#` in the displayed address selects a numbered heading within it. On every
refresh Organizing finds the current document by UID, derives its current
location, prefixes the selected corpus root's current directory name, validates
the section when present, and rewrites both `href` and the displayed address.
A controlled link may therefore carry a stale corpus-root declaration or location
after a rename or move; the UID remains authority and Organizing refreshes
that projection. Ordinary Markdown links are not touched. If the UID is missing
or duplicated, the displayed value is not valid address syntax, or the selected
heading no longer exists, Organizing fails rather than guessing.

Use a controlled UID anchor for every durable reference in reader-visible
prose. An address written as plain reader-visible prose is a current coordinate
rather than durable identity, so Organizing reports it as `ERROR DS001`.
A bare corpus-root address such as `§2.1` is invalid and unresolvable because
it omits the required corpus-root declaration; Organizing reports that
violation as `ERROR DS004`.

Do not store the corpus-root declaration or derived location components in
artifact metadata, and do not reconstruct location ancestry from generated
projections. An unnumbered artifact outside a numbered location has no
addressable location. A numbered location remains addressable without a
`README.md`, but a controlled link can target it only when a reader-facing body
represents that location.

## 4. Represent a folder with README.md

Use `README.md` for every folder that needs a reader-facing representation. A
numbered directory already creates its addressable location; its `README.md`
describes what the folder collects and contributes no additional ordinal. The
`README.md` at the selected corpus root uses the same representation with the
additional origin entry contract required before the first routing choice.

The corpus Origin defines the default reader-facing scope semantics for folder
representations. A downstream `README.md` needs its own `## Scope` section
only when it must state a different or more specific boundary; otherwise apply
the Origin's default recursive scope rule.

Keep the folder representation focused. Give the `README.md` one routing
`description`. When it has immediate indexed children, declare one Index element
where those choices should appear. Organizing derives the choices from the
filesystem and reuses each child's exact `description`; do not repeat descendant
metadata by hand.

`README.md` is a reserved folder representation, so it carries neither an
ordinal nor a quadrant glyph. In a numbered directory its location is exactly
that of its containing directory. At the selected corpus root it represents the
origin rather than an addressed descendant location.

For a `README.md` serving as the corpus origin, put the corpus entry contract
before its Index element. That contract:

- gives the corpus a specific H1 and a `description` that routes a reader into
  the corpus;
- explains compactly that corpus-root status is contextual to the Organizing
  job, while each documentation address declares the root by directory name,
  then descends through decimal locations and may select a numbered heading
  after `#`;
- states that a bare `§...` locator is invalid because it omits the required
  corpus-root declaration;
- tells the reader to separate independent concerns, compare each concern only
  with the immediate indexed choices, select the narrowest matching
  `description`, descend one Index at a time, and satisfy every resulting
  governing document according to its directive.

Add corpus-specific source, distribution, glossary, or folder context before
the first routing choice only when a reader must know it to choose correctly.
Do not add a persistent corpus-root metadata field: the Organizing job declares
that role by path and an address declares it by root directory name. The root
`README.md` carries no `form` link merely because it serves as the origin.

## 5. Add controlled metadata

Put descriptive metadata on the artifact itself when its native format can
carry it safely. Markdown uses frontmatter. Python uses its module docstring.
Organizing reads metadata without executing the artifact.

Every controlled artifact carries exactly one canonical `description`. Author
or correct it with
<a href="../2%20Technical%20Writing/1%20%F0%9F%9B%A0%EF%B8%8F%20Write%20A%20Technical%20Document.md#2-write-the-description" uid="5CFFZW">documentation-system:§2.1#2</a>
rather than inventing another routing or rule schema here. Organizing mints a
missing `uid`; never author a replacement UID merely because the artifact
moves.

For an addressed artifact, continue to step 6. For a controlled sideband
artifact, skip generated index work and continue to step 7.

Keep classification, routing, and identity separate:

```text
filesystem path   → where the artifact is
description       → when and why to use it
uid               → which artifact it is
address           → where it is now
```

## 6. Render the Index element

The Index element is a derived reader projection, not authored topology. The
filesystem already determines the hierarchy. A folder `README.md` with
immediate indexed children declares one `## Index` section and projects only
those children. The corpus-root `README.md` uses the same element after its
additional origin context. Traversing successive Index elements provides
progressive disclosure.

Declare the dynamic Index Document Element directly beneath its heading:

```markdown
## Index
<!--
element:
  path:
    uid: BZJASV
    filepath: 2 Technical Writing/3 Document/2 Document Elements/5 Index/README.md
  version: '1.0'
  renderer:
    uid: 45E225
    filepath: 4 Tooling/1 🛠️ Navigation Crawler.py
-->
```

The `element.path.uid` identifies the Index contract, `filepath` is its
refreshable physical projection, `version` records the contract emitted by the
renderer, and `renderer` identifies the controlled Python entry point that
owns regeneration. The heading supplies the structural write boundary.
Organizing owns the remainder of that heading-bounded section and renders each
immediate child as its controlled link, title, and exact `description`. Do not
hand-edit generated content or author a parallel child list.

## 7. Run and validate Organizing

Run Organizing refresh after classification, recognized metadata, numbered
headings, generated-index membership, or controlled-link targets may have
changed:

```text
python3 "4 Tooling/1 🛠️ Navigation Crawler.py" refresh [corpus_root]
```

Organizing validates the corpus-root declaration, duplicate sibling ordinals,
duplicate artifact locations and UIDs, missing descriptions, malformed generated
regions, controlled links with address declarations, and supported sideband
relationships before it writes indexes.

Resolve an address without writing anything:

```text
python3 "4 Tooling/1 🛠️ Navigation Crawler.py" resolve documentation-system:§2.1#4.2 [corpus_root]
```

Resolution requires an address whose corpus-root declaration matches the
Organizing job's corpus root. A bare corpus-root address such as `§2.1` is a
syntax error and cannot resolve.
Resolution returns the indexed body and provenance for the addressed document
or numbered section. An address naming a location resolves through its
`README.md` when one exists; a location with no `README.md` resolves as a
location with no body. A normal Organizing refresh also refreshes every controlled HTML anchor
carrying a `uid`, including anchors carried by a supported Python module
docstring.

Finish only when Organizing succeeds and each generated projection contains
the immediate indexed children implied by the filesystem.
