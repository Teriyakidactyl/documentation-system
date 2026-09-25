---
uid: 55NHDB
form:
  path: '<a href="../../a.%20Document%20Design/a.%20Assemblies/b.%20Forms/b.%20Architecture%20Document/README.md" uid="T6P28F">documentation-system:§a.a.b.b</a>'
  version: '1.0'
description: >-
  `Consult when` *the Organizing tool, an organization scheme, a peer
  representation capability, a validation rule, a projection, or a structural
  refactor is being introduced or materially changed* `to` **place
  responsibility with the owning capability while preserving one normalized
  corpus and one deterministic organization workflow**.
quadrant: Reference
outline:
  topology: tree
  axis: organizing responsibility
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

# 📖 Organizing Architecture

## 1. Scope

This architecture governs the public Organizing tool and the `automation/organizing`
implementation that maintains stable controlled identities, organization, and
derived representations for a Documentation System corpus.

It specializes the enclosing
<a href="%F0%9F%93%96%20Software%20Architecture.md" uid="K7W3P9">documentation-system:§d.g.2</a>
for corpus-wide organization semantics. The Software architecture governs the
shared public-tool, representation-capability, source-documentation, and
composition boundaries that Organizing inherits.

Its governed implementation is rooted in `d. Software` and entered through
`Navigation Crawler.py`. Folder, Markdown, Frontmatter, YAML, and HTML
remain independently routable peer capabilities. This architecture governs how
Organizing composes them for corpus-wide work; it does not make their generic
representation semantics subordinate to Organizing.

The architecture inherits Software Design Principles. It does not claim a
specialized reusable Error Management or Testing architecture merely because
those architectures exist. Such selection requires explicit conformance and
verification.

## 2. Drivers

Organizing must preserve these design forces:

- controlled artifact identity remains stable across moves, renames, and
  organization changes;
- current organization and locators remain projections rather than durable
  identity;
- one normalized corpus supplies organization truth to later passes;
- each representation capability retains ownership of its own syntax and local
  invariants;
- deterministic derived state can be rebuilt from canonical source state;
- structural mutation stops rather than guesses when unmanaged dependencies make
  a refactor unsafe;
- current architecture is discoverable from the public Organizing entry point
  and from the Software Architecture store;
- the historical `Navigation Crawler.py` executable basename remains an
  automation-compatibility boundary while external workflows depend on it.

The architecture favors explicit ownership and deterministic projections over
parallel models, duplicated parsers, or convention inferred from incidental
implementation shape.

## 3. Architecture

### 3.1 Core contract

Keep one normalized corpus model and one public Organizing entry point for
corpus-wide organization operations.

Do not create a second corpus model, parallel link authority, independent index
assembler, or filesystem refactorer that reconstructs organization semantics
separately.

Treat `automation/organizing` as the address-transparent semantic
implementation. `documentation_system/operations/organizing.py` owns the
interface-neutral public operation contracts over that implementation.
`documentation_system/interfaces/cli/organizing.py` owns command parsing and
result projection only. Treat `capabilities` as reusable representation-level
behavior used by Organizing and independently routable peer tools.

A peer capability owns its representation semantics. Organizing owns how those
representations participate in one controlled corpus.

### 3.2 Identity, organization, and locators

Keep durable identity independent from current organization.

~~~text
uid
 └── identifies controlled artifact
      └── participates in organization scheme
           ├── membership and topology
           ├── representation constraints
           └── locator projection, when the scheme defines one
~~~

The UID remains authority for artifact identity across moves, renames, and
organization changes.

An **organization scheme** defines how controlled artifacts participate in an
organized structure. A scheme may define membership rules, naming constraints,
relationships, ordering, and a locator notation. Do not require every future
scheme to use the same token vocabulary or projection rules as the current
folder-convention scheme.

A **locator** is a current coordinate projected by a scheme. It is not durable
identity. The current folder-convention scheme derives `§` location tokens from
the effective child naming policy and can extend an addressed document with a
Markdown-local numbered section after `#`.

A controlled reference binds durable UID identity to the current physical and
locator projections required by its representation. The UID selects the target;
the organization scheme and local representation determine what should be
displayed and linked now.

### 3.3 Peer capabilities

#### 3.3.1 Folder

Folder owns filesystem path inspection and collision-safe path mutation. It does
not decide what a path means to a corpus or which ordinal a sibling should
receive.

Organizing supplies an already-decided rename or move plan. Folder verifies the
transaction can be applied without clobbering unrelated paths and performs the
filesystem mutation.

#### 3.3.2 Markdown

Markdown owns Markdown structure: headings, heading-scoped comments, sections,
fenced code blocks, anchors, local heading numbering, and mechanically decidable
Markdown structural validation.

markdown-it-py is the structural parser behind that capability. The capability
translates parser output into repository-owned values with source coordinates;
parser-specific tokens are not public Documentation System architecture.
Markdown may return an old-to-new local section mapping after deterministic
normalization. Organizing consumes those structures and mappings when Element
metadata, generated sections, or controlled references must be maintained.
Markdown does not own corpus locations or UIDs.

For linting, Markdown separately composes PyMarkdownLnt for generic Markdown
rules and retains only Documentation-System-specific checks the package cannot
express. Enable the generic rule set selectively so upgrading the dependency
cannot silently create a new house opinion. Frontmatter supplies the
host-document boundary when linting a controlled Markdown file.

#### 3.3.3 Frontmatter

Frontmatter owns the metadata envelope carried by a host artifact: locating,
extracting, updating, and preserving the boundary between metadata and body.

Frontmatter consumes YAML for YAML payload semantics. That implementation
dependency does not make YAML subordinate in Software navigation.

#### 3.3.4 YAML

YAML owns generic YAML parsing, serialization, and mechanically decidable YAML
validation. It does not know frontmatter, controlled artifacts, UIDs, or
organization schemes.

YAML remains independently routable because pure YAML is a valid work encounter
even when no frontmatter or Documentation System corpus is involved.

#### 3.3.5 HTML

HTML owns generic element, attribute, comment, entity, and constrained anchor
parsing. It does not know that a `uid` attribute is a controlled identity or
that an anchor represents a Documentation System reference.

Markdown may use HTML to understand raw HTML carried by Markdown. Organizing may
use HTML when a controlled representation is encoded as HTML. HTML remains
independently routable because inspecting an HTML fragment or file is a coherent
work encounter without Markdown or corpus semantics.

### 3.4 Folder convention organization scheme

The implemented organization scheme is **folder convention organization**.
A literal `.folder.json` is semantic input owned by Organizing. It declares
how the immediate children of its containing directory are named and ordered;
it never governs the basename of that containing directory. Missing properties
inherit recursively from the nearest ancestor declaration.

The scheme maintains independent folder and file namespaces. Each namespace may
declare:

- a prefix `scheme`: `decimal`, `alpha`, an empty string for active
  prefix stripping, or `none` for no naming action;
- a literal `separator` rendered between an emitted token and the basename;
  and
- a `sort` policy: `alphabetical`, `numerical`, `date`, `size`, or
  sticky `none`.

An empty scheme and `none` are not synonyms. Empty is an active canonical
state: Organizing removes recognized managed prefixes while retaining an
implicit location token derived from the inherited coordinate scheme and the
declared deterministic sort. `none` leaves that namespace unmanaged. A corpus with no `.folder.json` retains the historical
decimal-prefix interpretation without silently turning that compatibility
behavior into an active rename policy.

The scheme owns:

- strict declaration parsing and recursive inheritance;
- canonical and recognized legacy prefix parsing;
- deterministic ordering and token encoding;
- classification of canonical, legacy, unprefixed, and unsafe prefix-like
  states;
- complete old-to-new path planning before mutation;
- current locator-token derivation; and
- rejection of ambiguous or unsafe transitions.

Normalization is reconciliation, not blind renaming. A partially applied
conversion may be completed when every source and destination is provable.
Exact current path literals are migrated only when their replacement is
unambiguous. Before a convention-managed refresh mutates the real corpus, the
complete normalization and refresh pipeline runs against a temporary copy;
structural, indexing, link, or diagnostic failure there aborts the real
mutation.

Folder remains the transaction owner. Organizing supplies the already-decided
rename plan; Folder validates and applies sibling renames collision-safely.

### 3.5 Corpus and projections

Model values carry normalized facts such as controlled artifact identity,
metadata, body, current organization facts, and corpus relationships. They do
not perform filesystem mutation, rewrite references, render indexes, or emit
diagnostics.

Corpus construction discovers supported controlled artifacts, applies the
selected organization scheme, validates unique identities and coordinates, and
produces the normalized corpus consumed by later passes.

Source-format adapters may call Frontmatter, Markdown, YAML, or HTML. Do not copy
those representation parsers into the corpus model.

Index projection derives reader navigation from the normalized corpus into the
Index Document Element declared by a folder `README.md`. The `README.md`
represents the folder; the Index element is generated navigation inside that
representation. Structured Element filepaths are projections of durable UIDs
when those targets participate in the selected corpus.

Controlled-reference processing owns UID target resolution and mechanical
refresh of physical links plus the display projection selected by the catalogued
link type. UID identity is invariant across link types.

A stale location or relative path is repairable when UID identity remains
valid. A missing or ambiguous UID, unknown link type, invalid locator syntax, or
unresolved local section is not repairable by guessing.

Each capability evaluates invariants it legitimately owns and returns structured
diagnostics. Organizing collects corpus-wide findings and presents them
consistently. Console output, GitHub Actions annotations, JSON, and optional
inline comments are projections of the same diagnostic facts.

### 3.6 Operations

#### 3.6.1 Refresh

Refresh reconciles deterministic derived state with current canonical sources:

~~~text
select corpus root
→ preflight generated navigation boundaries
→ clear stale inline diagnostics
→ establish controlled identities
→ build normalized corpus
→ refresh structured Element filepath projections
→ rebuild corpus
→ refresh deterministic navigation projections
→ rebuild corpus
→ refresh UID-controlled references
→ rebuild corpus
→ validate organized state
→ emit selected diagnostic projections
~~~

A pass may write only the representation it owns. Rebuild the corpus after a
write that changes facts consumed by a later pass.

#### 3.6.2 Inspect

Inspect exposes organization facts and violations without changing the corpus.
Use it to debug how paths become locations, identify ordinal gaps, and view the
normalization plan implied by the selected scheme.

#### 3.6.3 Resolve

Resolve maps a supported locator to its current controlled artifact, location,
or local section without refreshing derived state.

#### 3.6.4 Normalize

Normalize plans a deterministic structural refactor of the selected organization
scheme. Dry-run is the default.

Before applying a rename plan:

1. derive the complete old-to-new filesystem and locator mapping;
2. reject duplicate sources, duplicate destinations, or unrelated destination
   collisions;
3. identify unmanaged literal path references that UID-controlled reference
   repair cannot prove safe; and
4. stop rather than mutate when an unmanaged dependency remains.

When the plan is safe to apply, Folder performs the collision-safe filesystem
transaction. Organizing then rebuilds the corpus, refreshes navigation and
UID-controlled references, and validates the resulting state.

Normalization does not decide that two concepts should exchange semantic
positions. It only applies an organization change already determined by the
selected scheme or an explicit caller decision.

## 4. Realization

The public implementation boundary is:

~~~text
d. Software/Navigation Crawler.py        temporary wrapper
    → documentation_system/interfaces/cli/organizing.py
        → documentation_system/operations/organizing.py
            → automation/organizing/
                → normalized corpus and organization passes
~~~

The principal implementation responsibilities are:

- `automation/organizing/model.py` owns normalized corpus facts, UID identity, locator
  derivation, controlled sideband traversal, and corpus construction;
- `automation/organizing/engine.py` owns corpus-wide operation sequencing;
- `documentation_system/operations/organizing.py` owns the public Organizing
  operation contracts and canonical result/failure boundary;
- `documentation_system/interfaces/cli/organizing.py` owns command parsing,
  result projection, and exit behavior;
- `automation/organizing/indexes.py` owns navigation projection;
- `automation/organizing/links.py` owns controlled-reference refresh;
- `automation/organizing/diagnostics.py` owns diagnostic representation and projections;
- `automation/organizing/refactor.py` and `automation/organizing/schemes/ordinal.py` own
  organization inspection and deterministic normalization; and
- `capabilities` owns reusable Folder, Markdown, Frontmatter, YAML, and HTML
  mechanics.

Keep semantic ownership and implementation dependency distinct:

~~~text
Organizing CLI -> organizing engine
               -> organization scheme
               -> corpus model
               -> indexes
               -> controlled references
               -> diagnostics
               -> Folder
               -> Markdown -> Frontmatter -> YAML
               -> Frontmatter -> YAML
               -> HTML

Markdown    -> markdown-it-py
Markdown    -> PyMarkdownLnt

YAML        <- independently routable
HTML        <- independently routable
Frontmatter <- independently routable
Markdown    <- independently routable
Folder      <- independently routable
~~~

Share normalized facts through explicit values rather than hidden mutable state.
Do not infer a Software navigation hierarchy from the import graph.

## 5. Verification

The authored Software test suite under `d. Software/tests` is the current
executable verification surface for Organizing. It must continue to cover
corpus-root behavior, index boundaries, controlled sidebands, UIDs and
locators, controlled references, ordinal inspection and normalization,
representation capabilities, and deterministic refresh behavior.

The `Maintain documentation organization` GitHub Actions workflow executes the
Software tests, runs Organizing through the historical public entry path, runs a
second refresh to establish idempotence, and checks the resulting diff for
formatting errors.

The same public Organizing boundary must remain usable locally. CI is a
projection of verification, not the sole semantic owner of it.

This implementation does not yet claim the Self-Assembling Verification
Architecture. Adopting that reusable architecture requires mechanically
discoverable callable declarations, visible coverage classification, and the
other obligations defined by that architecture rather than a metadata-only
selection.

## 6. Evolution

Add a deterministic capability when canonical inputs and declarations select one
output without contextual interpretation. Keep semantic choices authored when
several meanings remain plausible.

Add an internal module when a responsibility has an independent reason to change
and a stable boundary. Do not split one function per file for symmetry.

Add another public Software artifact when the work encounter is independently
routable and useful without entering Organizing. Do not require an independent
package or release lifecycle merely because a capability deserves a separate
routing surface.

Add another organization scheme only when a real corpus requires behavior the
current scheme cannot represent without distorting its meaning.

The public entry filename may change only when its automation compatibility
constraint is deliberately retired and all dependent workflows or external
hooks are migrated together.
