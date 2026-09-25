---
uid: K7W3P9
form:
  path: '<a href="../../e.%20Technical%20Writing/a.%20Document/b.%20Document%20Forms/b.%20Architecture%20Document/README.md" uid="T6P28F">documentation-system:§e.a.b.b</a>'
  version: '1.0'
description: >-
  `Consult when` *a Software entry point, shared capability, representation
  boundary, code-facing documentation surface, or cross-tool composition is
  being introduced or materially changed* `to` **preserve Software's public
  work-encounter surfaces, nearest-expertise ownership, composition boundaries,
  source-local documentation model, and deterministic handoff between semantic
  and representation responsibilities**.
quadrant: Reference
outline:
  topology: tree
  axis: tooling responsibility
  numbering: hierarchical-decimal
writing-style:
  formality: professional
  tone: clinical/detached
  mode: declarative
  density: compressed/dense
  abstraction: mixed
  redundancy: zero
  signposting: entry-headers only
  register: technical
---

# 📖 Software Architecture

## 1. Scope

This architecture governs the shared design of Documentation System Software
rooted at `f. Software`: the public executable and procedural entry surfaces, the
address-transparent implementation capabilities beneath them, and the
composition rules that keep representation expertise separate from higher-level
Documentation System semantics.

The public Software surfaces currently include Organizing, Harness Installer,
Folder, Markdown, Frontmatter, YAML, HTML, and Software environment preparation.
The Python implementation beneath those surfaces is primarily split between
`_capabilities`, which owns reusable representation mechanics, and
`_organizing`, which owns corpus-wide organization semantics and orchestration.

<a href="%F0%9F%93%96%20Organizing%20Architecture.md" uid="55NHDB">documentation-system:§f.d.1</a>
is the narrower architecture governing Organizing and its use of peer
capabilities. It specializes this Software architecture for corpus identity,
organization schemes, projections, controlled references, diagnostics, and
structural refactoring.

This architecture does not make every public tool one subsystem with one release
lifecycle. Independently routable tools remain independently useful work
encounters. It governs their shared boundaries and composition model.

## 2. Drivers

Software must preserve these design forces:

- an agent must be able to enter through the narrowest tool that owns the
  mechanical operation it needs rather than loading an unrelated orchestration
  surface;
- representation-specific parsing and mutation must stay with the capability
  nearest to that representation;
- higher-level semantic tools must compose lower-level capabilities rather than
  duplicate their parsers or safe-write mechanics;
- public tools must remain understandable from their own source-local
  documentation when an agent arrives without conversational history;
- current code and documentation frequently share one Python source artifact, so
  docstring mutation must preserve executable syntax and avoid blind text
  replacement;
- mechanically derived facts should be rediscovered from implementation instead
  of copied into parallel hand-maintained inventories;
- semantic decisions that cannot be derived reliably must remain explicitly
  authored at the layer that owns them;
- deterministic operations may be automated and refreshed; ambiguous semantic
  choices must stop or remain authored rather than be guessed;
- Software must remain locally executable and compatible with the repository's
  current GitHub Actions entry paths and dependency declaration; and
- architecture guidance must remain discoverable without requiring an agent to
  reconstruct design intent from imports, filenames, or historical discussion.

The architecture favors small semantic owners connected by explicit handoffs
over one tool that understands every representation and every Documentation
System concept.

## 3. Architecture

### 3.1 Public work encounters and internal capabilities

A numbered Software artifact is a public work encounter. Its documentation tells
an agent when the tool is the appropriate entry point and its executable surface
adapts that work encounter to implementation capabilities.

Address-transparent implementation packages are not additional navigation
levels. They exist to give independently changing responsibilities stable code
boundaries without requiring an agent to discover internal modules before it can
choose a tool.

The current shape is:

~~~text
public Software artifact
    ↓ adapts one work encounter
shared implementation capability
    ↓ owns reusable mechanics
optional semantic orchestrator
    ↓ composes capabilities for a broader system operation
~~~

A public tool may be thin when its value is independent routability rather than
new domain logic. A thin public adapter must not cause the underlying capability
to be reimplemented elsewhere.

### 3.2 Nearest-expertise ownership

Assign representation work to the capability with the nearest structural
expertise.

Current ownership includes:

- Folder owns collision-safe filesystem path mutation;
- Markdown owns Markdown structure, local coordinates, and mechanically
  decidable Markdown operations;
- Frontmatter owns metadata-envelope location, extraction, preservation, and
  replacement within supported host representations;
- YAML owns generic YAML parsing and serialization;
- HTML owns HTML syntax and constrained anchor parsing; and
- Organizing owns controlled-corpus semantics that use those representations.

A higher-level capability may ask a representation expert to extract or mutate a
surface, but it must retain ownership of the higher-level meaning assigned to
that surface.

For a Python module docstring carrying YAML frontmatter and controlled HTML
links, the responsibility chain is therefore conceptually:

~~~text
Python-aware host handling
    ↓ locates and safely replaces the module docstring
Frontmatter
    ↓ owns the metadata envelope
YAML
    ↓ owns YAML payload syntax
HTML
    ↓ owns anchor syntax where embedded HTML is used
Organizing
    ↓ assigns controlled-reference semantics to uid-bearing anchors
~~~

Implementation may collapse adjacent mechanical steps into one capability when
the boundary remains explicit. Do not make Organizing a Python parser merely
because an Organizing operation happens to touch a Python docstring.

### 3.3 Semantic orchestration over representation mechanics

Semantic tools own decisions that require Documentation System meaning.
Representation capabilities own mechanics that remain valid without that
meaning.

The dependency direction is:

~~~text
Documentation System semantics
        ↓
semantic orchestration
        ↓
representation capability
        ↓
generic parser / filesystem primitive
~~~

Lower layers must not acquire higher-layer concepts merely to make one caller
convenient. YAML does not know frontmatter. Frontmatter does not know corpus
identity. HTML does not know that `uid` denotes controlled identity. Folder does
not decide organization ordinals.

When a format-specific capability can return normalized repository-owned values,
higher layers consume those values instead of parser-library token objects.

### 3.4 Source-local documentation as a Software surface

Python Software module docstrings are both source-local documentation and, where
frontmatter is present, controlled Documentation System artifacts.

The module docstring is the natural file-level orientation surface because an
agent may arrive directly at a source file through search, a stack trace, a test
failure, or an implementation reference rather than through repository
navigation.

Module-level documentation may therefore carry:

- the public purpose of an executable Software artifact;
- controlled metadata needed for indexing and governance;
- compact routing links to governing authority; and
- file-level context that cannot be recovered safely from syntax alone.

Function and class docstrings have a narrower responsibility. They should state
contract information that the signature, types, names, and implementation do not
make safely inferable. They are not a place to reproduce the file's governance
graph or enumerate every Software Design concern that could apply.

The architectural distinction is:

~~~text
module docstring
    → file orientation and governance routing

symbol docstring
    → local contract gap

Architecture Document
    → system-level design authority
~~~

### 3.5 Controlled source mutation

Software that mutates source documentation must use a host-aware boundary rather
than unrestricted text replacement.

The current Frontmatter capability parses Python with the AST to identify the
module docstring and uses token coordinates to replace that string literal.
Organizing's controlled-link refresh can therefore scan Python files, isolate
their module docstrings, refresh UID-controlled anchors inside that surface, and
replace the docstring without rewriting executable statements.

This establishes the current mutation rule:

> Parse enough of the host representation to identify the owned documentation
> surface, delegate embedded-format semantics to the corresponding capability,
> and write back only the owned surface.

Do not generalize the current module-docstring support into a claim that Software
already provides arbitrary function/class docstring refactoring.

### 3.6 Help and generated projections

Generated help is a projection of authored and mechanically discoverable facts,
not a second authority.

When a Software surface exposes help, prefer facts already present in:

- callable names and signatures;
- type declarations;
- argument declarations and descriptions;
- module or symbol docstrings; and
- other code-local declarations owned by the implementation.

A help renderer may assemble these facts into a bounded agent-facing view. It
must not become the only place where a contract exists.

Following a governance or architecture link is a navigation operation, not a
substitute for a useful local contract. A renderer should not need to traverse a
large governance graph merely to explain the immediate callable in front of an
agent.

### 3.7 Derivation before duplication

Do not maintain a parallel handwritten inventory of files, functions, classes,
imports, or other facts that Software can reliably derive from source.

Machine-readable authored declarations are justified when they express semantic
facts that implementation structure cannot establish reliably, such as an
intentional ownership boundary, a selected governing concept, or an allowed
dependency that would otherwise be ambiguous.

Prefer:

~~~text
authored semantic claim
+ discovered implementation facts
→ verification
~~~

over:

~~~text
authored semantic claim
+ copied implementation inventory
+ implementation
→ three independently drifting descriptions
~~~

### 3.8 Verification boundaries

Mechanically decidable claims should be verified mechanically when the cost is
proportionate. Semantic architectural claims remain review obligations unless a
faithful mechanical representation exists.

Do not redesign a semantic rule into a weaker machine-detectable proxy merely so
all architecture can be checked by static analysis.

A mechanical verifier may use source structure, controlled metadata, UIDs,
imports, paths, schemas, and other explicit declarations as evidence. It should
report conflicts between authored claims and discovered implementation rather
than silently selecting one as truth.

### 3.9 Implemented error design

Software follows the general
<a href="../../d.%20Software%20Design/f.%20Error%20Management/README.md" uid="TJBYJ1">documentation-system:§d.f</a>
guidance, but the current implementation does **not** select the reusable
Agent-Facing Error Architecture.

The implemented error design is:

- each capability owns a domain-specific exception for failures it can recognize
  semantically, such as `FolderError`, `FrontmatterError`,
  `MarkdownLintError`, or `OrganizingError`;
- a higher semantic layer translates a lower-layer exception only at a meaningful
  ownership boundary and preserves the original exception as the cause when it
  wraps it;
- public command boundaries catch expected tool/domain failures and convert them
  to concise tool-prefixed exit messages;
- unexpected implementation exceptions are not blanket-converted into ordinary
  domain failures;
- deterministic validation findings that can coexist with an otherwise
  established result are represented as diagnostics rather than exceptions;
- Organizing diagnostics carry structured code, severity, path, line, and
  message facts, then project those same facts to console, GitHub Actions, JSON,
  or optional inline comments; and
- unsafe structural mutation fails before mutation or rolls back the owned
  transaction rather than guessing through an unresolved condition.

For Organizing refresh, accumulated diagnostics do not all imply command failure.
`error` severity produces a non-zero exit; warning and information findings can
be reported with a completed deterministic refresh.

### 3.10 Implemented testing design

Software follows the general
<a href="../../d.%20Software%20Design/k.%20Testing/README.md" uid="R0J5KF">documentation-system:§d.k</a>
guidance, but the current implementation does **not** select the reusable
Self-Assembling Verification Architecture.

The implemented testing design is manually authored and layered by owned
contract:

- capability tests exercise representation mechanics at their narrow owned
  boundary;
- Organizing tests exercise normalized corpus semantics and composition across
  capabilities;
- tests use temporary filesystem state and real deterministic implementations
  where practical rather than reproducing internal call choreography with mocks;
- assertions target stable outputs, errors, diagnostics, mutations, and
  invariants rather than private helper sequences;
- the repository workflow executes the authored unit/integration-style suites,
  then runs Organizing through its historical public executable path;
- a second refresh must produce the same diff as the first, making idempotence a
  first-class verification property; and
- `git diff --check` verifies the resulting generated state is mechanically
  clean.

The authored test inventory is current verification evidence. It does not grow
automatically from callable declarations, so Software must not claim
Self-Assembling Verification until that reusable architecture's selecting
conditions and obligations are actually satisfied.

## 4. Realization

The current public Software boundary is the numbered set of artifacts under
`f. Software`. Python tools use source-local module docstrings as their indexed
Documentation System representation.

The principal shared implementation boundaries are:

- `_capabilities/folder.py` for collision-safe filesystem mutation;
- `_capabilities/markdown.py` and `markdown_lint.py` for Markdown structure
  and deterministic lint/fix mechanics;
- `_capabilities/frontmatter.py` for Markdown/Python metadata envelopes and
  safe Python module-docstring extraction/replacement;
- `_capabilities/yaml.py` for YAML semantics;
- `_capabilities/html.py` for generic HTML and anchor syntax;
- `_organizing` for corpus-wide identity, organization, projection,
  controlled-reference, diagnostic, and refactor semantics; and
- `f. Software/tests` for executable coverage of the shared capability and
  Organizing boundaries.

Current composition examples include:

~~~text
Markdown tool
    → Frontmatter
    → Markdown capability
    → markdown-it-py / PyMarkdownLnt

Frontmatter tool
    → Frontmatter capability
    → YAML capability

Organizing
    → Frontmatter / Markdown / HTML / Folder / YAML mechanics
    → corpus semantics in _organizing
~~~

`requirements.txt` is the shared dependency declaration for Software execution.
`Prepare Software Environment` defines the current repository-local execution
environment procedure.

## 5. Verification

`f. Software/tests/test_capabilities.py` exercises representation-capability
boundaries including Python docstring frontmatter extraction, Markdown
structure, HTML anchor parsing, and organization refactor behavior.

`f. Software/tests/test_organizing.py` exercises corpus semantics and the
composition of representation capabilities through Organizing.

The `Maintain documentation organization` GitHub Actions workflow remains the
repository verification boundary that runs Software tests and the public
Organizing entry path, establishes refresh idempotence, and checks generated
state.

Current verification does not yet prove every ownership statement in this
document mechanically. In particular, the absence of duplicated parser
responsibilities and the semantic distinction between local contracts and
governance guidance remain architecture-review obligations.

## 6. Evolution

The following directions are deliberately **not current architecture claims**.
They record selecting conditions and constraints exposed by the present design
so that later work can be evaluated without reconstructing this reasoning from
conversation history.

### 6.1 Code help projection

If agents need a bounded help surface for arbitrary Python modules or symbols,
prefer a projection assembled from local source facts before introducing a
separate authored help corpus.

A candidate flow is:

~~~text
Python structure and signature
+ module docstring
+ symbol docstring
+ existing typed declarations
→ compact agent-facing help
~~~

The renderer should preserve the ownership rule in section 3.6: it assembles existing
contracts; it does not invent them or require architecture traversal for routine
callable help.

Select this direction only when repeated code-entry workflows show that raw
source-local contracts are insufficiently consumable.

### 6.2 Semantic controlled links in docstrings

Organizing already refreshes UID-controlled HTML anchors inside Python module
docstrings. If code needs compact links to governing design concepts, extend the
controlled-link model rather than creating an unrelated code-governance
registry.

A useful link would preserve three properties:

~~~text
relationship clue
+ human semantic clue
+ durable controlled identity
~~~

For a Software Design concept, its controlled `README.md` is a plausible
stable routing target because that entry point can evolve the guidance beneath
the concept without requiring every source link to change.

The exact source syntax is unresolved. Possibilities such as a frontmatter
field, a compact docstring field, HTML with a semantic link type, or a
reStructuredText role are not selected by this architecture. Choose a
representation only after its authoring cost, human readability, batch mutation,
and language portability are understood.

### 6.3 Reverse routing from arbitrary code entry

If agents routinely enter implementation through search results, stack traces,
tests, or direct file references, establish a local route back to governing
context that remains discoverable when the file is inspected in isolation.

Do not answer this need by copying the entire governance hierarchy into every
file or function. Prefer one compact file-level route to a stable authority or
concept entry point, with deeper guidance discovered from there.

Whether the route should name the implemented Architecture Document, one or more
Software Design concepts, or another controlled authority remains unresolved.

### 6.4 Sparse symbol guidance

Do not make every function carry design ancestry.

Add symbol-level guidance only when a locally plausible change could violate a
non-obvious contract that names, signatures, types, and surrounding code do not
communicate sufficiently.

The preferred progression is:

~~~text
types and names
    ↓
symbol contract gap, when needed
    ↓
file-level orientation
    ↓
governing architecture or design concept, when needed
~~~

If a future renderer or metadata convention makes every symbol repeat the same
governance facts, treat that repetition as a design failure rather than a
completeness achievement.

### 6.5 Representation-aware handoff

If Software adds support for another host language or embedded documentation
format, preserve nearest-expertise delegation.

A host-language capability should identify and safely extract the relevant
documentation surface. An embedded-format capability should parse that payload.
The semantic consumer should interpret only the concepts it owns.

Do not require one generalized documentation parser to understand Python, Rust,
JavaScript, YAML, reStructuredText, Markdown, HTML, and Documentation System
governance simultaneously.

### 6.6 Architecture conformance

If architecture verification becomes a first-class Software capability, derive
file lists, imports, declarations, call surfaces, and similar structural facts
from implementation wherever possible.

Add authored machine-readable architecture declarations only for non-derivable
semantic claims. Cross-check authored scope against discovered implementation
rather than introducing a second handwritten implementation manifest.

Preserve the distinction between structural verification and semantic review.
