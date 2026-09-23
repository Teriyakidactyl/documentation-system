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
procedure. The filesystem owns classification and the location portion of an
address; a `uid` owns durable document identity; a numbered internal outline
can extend that address into a file. Recognized metadata makes an artifact
controlled. An addressable position additionally makes it indexable. The
compiler derives indexes from the addressed filesystem hierarchy; controlled
sideband artifacts can retain identity and validation without entering that
navigation surface.

**Terms.** One name per concept, with relationships shown before definitions:

```text
address space
└── corpus root
    ├── controlled artifact
    │   ├── uid
    │   ├── description
    │   ├── indexed artifact
    │   └── controlled sideband artifact
    ├── origin
    │   └── index
    └── location
        ├── location ordinal
        ├── address
        └── INDEX.md
            └── index
```

| Term | Meaning |
|---|---|
| **address space** | A stable logical namespace for one controlled corpus. Its name qualifies addresses independently of the corpus root's physical path or mount location. |
| **corpus root** | The filesystem directory selected as the root of one controlled corpus and the relative origin of its address tree. Every `§` location path is derived from numbered descendants beneath this directory; filesystem ancestors do not contribute to the address. |
| **origin** | The root reader-facing entry point of an address space, represented by `README.md`. It contributes no location ordinal. |
| **controlled artifact** | A file on a compiler-traversed path whose supported metadata surface contains a `description` and compiler-minted `uid`. It participates in durable identity and validation whether or not it has an address. |
| **indexed artifact** | A controlled artifact whose filesystem position derives an address and can therefore participate in generated index navigation. |
| **controlled sideband artifact** | A controlled artifact stored in a reserved sideband whose retrieval policy excludes it from normal index navigation. It keeps a UID and validation participation but has no Documentation System address. |
| **uid** | A permanent six-character Crockford Base32 identifier minted by the compiler for one controlled artifact. It survives moves and renames; duplicate UIDs are invalid. |
| **description** | The canonical Markdown routing statement for a controlled artifact. Indexed projections reuse it where the artifact participates in routing. |
| **location** | A position in the corpus hierarchy defined by the filesystem. A numbered directory defines an addressable location whether or not it contains `INDEX.md`. |
| **location ordinal** | A local numeric position read from the start of a numbered directory or numbered artifact name. The accepted prefix is `^([0-9]+)(?:\.\s+|\s+)`, so both `9 Name` and `9. Name` carry ordinal `9`. |
| **address** | A machine-resolvable identifier such as `documentation-system:§2.1#4.2`. Its `§` portion is fully derived from location ordinals beneath the corpus root; optional `#` extends into a numbered heading; optional address-space qualification keeps the reference unambiguous outside its corpus. |
| **`INDEX.md`** | The reader-facing representation of its containing location. It contributes no location ordinal of its own and therefore resolves to the containing location's address. |
| **index** | The compiler-generated projection of an origin or `INDEX.md`'s immediate indexed children, each shown with its controlled link, title, and exact `description`. |
| **progressive disclosure** | The reader behavior enabled by traversing successive indexes and exposing only the next immediate choices needed. |
| **compiler** | The Documentation Compiler that scans supported metadata surfaces, mints and validates UIDs, validates the location/address space, derives projections, refreshes controlled links, reports diagnostics, and resolves addresses. |

## 1. Establish the controlled corpus

Start from the **corpus root**. A file becomes a controlled artifact only when
it is on a compiler-traversed path and the compiler recognizes its metadata
surface. Address and index participation are additional properties rather than
requirements for controlled identity.

The compiler currently recognizes two shapes:

- Markdown: YAML frontmatter fenced by `---` at the start of the file.
- Python: YAML frontmatter fenced by `---` at the start of the module docstring.

Both normalize into the same metadata model. A Python module therefore does
not need a companion Markdown document merely to participate in control. Add a
new source format by adding a metadata adapter; do not change the address model
for each file type.

Do not infer that every file under the corpus root is controlled information.
Presence establishes physical location; compiler traversal plus recognizable
metadata establishes controlled participation. Addressability determines index
participation separately.

Most dot-prefixed directories remain outside the controlled corpus. Reserved
exceptions can define a controlled sideband when information needs durable UID
identity and compiler validation without normal routing. The current reserved
behavior is defined by
<a href="2%20%F0%9F%93%96%20Folder%20Conventions.md" uid="TRJS8V">documentation-system:§1.2</a>.
Apply
<a href="3%20%F0%9F%93%96%20Repository%20Information%20Storage.md" uid="S9HVWB">documentation-system:§1.3</a>
before introducing another sideband representation.

On a normal compile, the compiler adds a missing `uid` to each controlled
artifact. Never change an existing UID because an artifact moved or was renamed.
Copying a controlled artifact also copies its UID, so the duplicate must be
replaced by a newly minted UID before the corpus can compile.

## 2. Place information in the location hierarchy

Use the existing repository hierarchy before creating another one. Numbered
directories define classification locations. Numbered artifacts occupy
terminal positions within those locations. Unnumbered directories may organize
files physically but contribute no address component.

For example:

```text
2 Conventions/
├── INDEX.md
└── 11 Technical Writing/
    ├── INDEX.md
    └── 9 Write A Technical Document.md
```

contains these positions:

```text
§2       2 Conventions/
§2       2 Conventions/INDEX.md
§2.11    2 Conventions/11 Technical Writing/
§2.11    2 Conventions/11 Technical Writing/INDEX.md
§2.11.9  2 Conventions/11 Technical Writing/9 Write A Technical Document.md
```

Use one ordinal once among physical siblings in the current corpus state. A
numbered directory and a numbered artifact with the same ordinal under one
parent collide even when their names differ.

An ordinal is a current structural coordinate, not durable identity. After an
item moves or is removed, its former ordinal may be reused. Preserve durable
identity with the artifact's UID rather than reserving historical coordinates.

## 3. Derive and use addresses

Treat the corpus structure as the source of truth. Derive the location portion
of an address by walking from the corpus root, taking each location ordinal,
and appending a terminal artifact ordinal when the target is not `INDEX.md`.
Join those ordinals with `.` and prefix them with `§`:

```text
2 Technical Writing/
└── 1 🛠️ Write A Technical Document.md

§2.1
```

A numbered heading extends that location into the resolved file after `#`.
Qualification with the address-space name is optional inside the same corpus
and explicit when the address must survive being cited from elsewhere:

```text
address = [address-space ":"] "§" location-ordinal ("." location-ordinal)* ["#" heading-number]
heading-number = integer ("." integer)*

§2.1
§2.1#4.2
documentation-system:§2.1#4.2
```

The periods express hierarchical descent on either side of `#`; `#` marks the
boundary between repository location and the file's internal outline. An
address is a current coordinate: moving an addressed item changes it, and a
former coordinate may later identify different information. Moving the whole
address space does not change internal coordinates. The UID does not change.

Use a controlled HTML anchor when the reference must survive a move or rename:

```text
control-link = '<a href="' physical-target '" uid="' uid '">' qualified-address '</a>'
uid          = 6 Crockford Base32 characters
```

For example:

```html
<a href="*" uid="5CFFZW">documentation-system:§2.1#4.2</a>
```

The `uid` identifies the document; the optional `#` in the displayed address
selects a numbered heading within it. On every pass the compiler finds the
current document by UID, derives its current fully qualified address, validates
the section when present, and rewrites both `href` and the displayed address.
The address-space qualifier names the logical namespace; it does not encode the
corpus root's physical path. Moving or mounting the whole corpus elsewhere does
not change its qualifier or its internal coordinates. Ordinary Markdown links
are not touched.
If the UID is missing or duplicated, or the selected heading no longer exists,
the compiler fails rather than guessing.

Use a controlled UID anchor for every durable reference in reader-visible
prose. A bare address is only a current-location notation suitable for examples,
lookup input, or other non-reference contexts. The compiler reports live bare
references as `ERROR DS001` so structural changes cannot silently retarget
prose.

Do not store authored address components in metadata or reconstruct location
ancestry from generated projections. An unnumbered artifact outside a numbered location
has no location address. A numbered location remains addressable without an
`INDEX.md`, but a controlled link can target it only when an indexed body
represents that location.

## 4. Represent a location with INDEX.md

Add `INDEX.md` when a location needs a reader-facing representation. The
numbered directory already created the location; `INDEX.md` describes what the
location collects and provides the surface on which the compiler can project
its immediate indexed children.

Keep the index focused. Give it its own `description`, then place one generated
region where immediate choices should appear. The compiler derives those choices
from the filesystem and reuses each child's exact `description`; do not repeat
descendant metadata by hand.

`INDEX.md` is a reserved representation, so it carries neither an ordinal nor
a quadrant glyph. Its address is exactly the address of its containing
location.

## 5. Make an artifact indexable

Put descriptive metadata on the artifact itself when its native format can
carry it safely. Markdown uses frontmatter. Python uses its module docstring.
The compiler reads metadata without executing the artifact.

Every indexed artifact carries exactly one canonical `description`. Author or
correct it with
<a href="../2%20Technical%20Writing/1%20%F0%9F%9B%A0%EF%B8%8F%20Write%20A%20Technical%20Document.md#2-write-the-description" uid="5CFFZW">documentation-system:§2.1#2</a>
rather than inventing another routing or rule schema here. The compiler mints a
missing `uid`; never author a replacement UID merely because the artifact
moves.

Keep classification, routing, and identity separate:

```text
filesystem path   → where the artifact is
description       → when and why to use it
uid               → which artifact it is
address           → where it is now
```

## 6. Generate the index

The index is a derived reader projection, not authored topology. The filesystem
already determines the hierarchy. `README.md` represents the origin and projects
the immediate indexed items at the corpus root; each `INDEX.md` with immediate
indexed children projects only those children. Traversing successive indexes
provides progressive disclosure.

Place exactly one generated region where those choices should appear:

```markdown
<!-- BEGIN index -->
<!-- END index -->
```

The compiler owns everything between the markers and renders each immediate
child as its controlled link, title, and exact `description`. Do not hand-edit
generated content and do not author a parallel child list.

## 7. Run and validate the compiler

Run the Documentation Compiler after classification, recognized metadata, numbered
headings, generated-index membership, or controlled-link targets may have
changed:

```text
python3 "4 Tooling/1 🛠️ Navigation Crawler.py" [corpus_root]
```

The compiler validates duplicate sibling ordinals, duplicate addresses and
UIDs, missing descriptions, malformed generated regions, and controlled links
before it writes indexes.

Resolve an address without writing anything:

```text
python3 "4 Tooling/1 🛠️ Navigation Crawler.py" --resolve documentation-system:§2.1#4.2 [corpus_root]
```

Resolution returns the indexed body and provenance for the addressed document
or numbered section. A location address resolves through its `INDEX.md` when
one exists; a location with no index resolves as a location with no body. A
normal compiler pass also refreshes every controlled HTML anchor carrying a
`uid`, including anchors carried by a supported Python module docstring.

Finish only when the compiler succeeds and each generated projection contains
the immediate indexed children implied by the filesystem.
