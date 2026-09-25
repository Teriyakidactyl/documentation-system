---
uid: G9J8W8
form:
  path: '<a href="../a.%20Document%20Design/a.%20Document/b.%20Document%20Forms/a.%20Architecture%20Decision%20Record/README.md" uid="A1FANY">documentation-system:§a.a.b.a</a>'
  version: '1.0'
description: >-
  `Read in full when` *the rationale for using separate Markdown parsing and
  linting dependencies must be reviewed* `to` **understand why
  markdown-it-py owns structural interpretation while PyMarkdownLnt remains
  generic lint-and-fix tooling, including the accepted duplication and parser
  authority boundary**.
quadrant: Explanation
decision:
  status: accepted
  decided-at: '2026-09-24T08:08:25-07:00'
  repository-revision: 8e16fbc593fb638fd283e2f4779a4fc0b0263d4e
  supersedes: []
  superseded-by:
outline:
  numbering: hierarchical-decimal
writing-style:
  formality: professional
  tone: collegial/earnest
  mode: declarative
  density: moderate
  abstraction: mixed
  redundancy: zero
  signposting: suppressed
  register: accessible
---

# 💡 Why Markdown Parsing and Linting Use Separate Dependencies

## Context

Executable Document Elements and the planned Renderer increase what the
Markdown capability must understand. Headings and fenced blocks are no longer
the complete requirement: element discovery and deterministic bounded edits
also need reliable block structure, raw HTML recognition, tables, and source
positions without gradually reimplementing Markdown grammar in repository code.

The repository already uses PyMarkdownLnt 0.9.40 for generic Markdown linting.
Its rule-plugin engine scans parsed Markdown and its fix workflow applies only
rules that declare mechanical autofix support. That is valuable behavior worth
retaining.

A single dependency would reduce duplicate Markdown interpretation, so
parser-plus-linter candidates received extra consideration. The decision does
not make dependency count the primary criterion, however. Structural parsing
and lint policy have different ownership and API requirements.

## Decision

Use **markdown-it-py** as the third-party structural parser behind the shared
Markdown capability.

Keep **PyMarkdownLnt** as the generic Markdown linting and mechanical-fix
dependency.

The shared Markdown capability owns the canonical structural model exposed to
the rest of the Documentation System. Parser-specific markdown-it-py tokens or
tree nodes do not become public repository architecture. PyMarkdownLnt findings
remain lint diagnostics and fixes; its internal parser is not a second
structural authority for Renderer or Document Elements.

Parse Markdown to understand source structure, then perform the smallest
deterministic text replacement over owned source ranges. Do not adopt
whole-document parse/mutate/serialize as the default editing mechanism.

This decision selects dependencies and ownership. It does not itself implement
the planned Renderer or parser adapter.

## Rationale

markdown-it-py 4.2.0 is a production Python Markdown parser with CommonMark and
GFM-like configurations. Its parser returns block tokens carrying source-line
maps, nests inline tokens beneath block tokens, and can project the token stream
into its syntax-tree representation. That gives the Markdown capability a
mature grammar boundary while allowing our adapter to expose only the
structures and source ranges the Documentation System needs.

PyMarkdownLnt 0.9.40 is already specialized for the other job. It provides a
large rule-plugin surface, read-only scan behavior, and a fix workflow for
rules whose authors declare a change mechanically safe. Replacing that coverage
with local lint rules merely to share one parser would move generic Markdown
policy into repository code.

Using PyMarkdownLnt alone for both responsibilities was attractive because one
engine would interpret Markdown once. Its supported application surface,
however, is centered on scanning, fixing, configuration, and rule plugins.
Making its parser/token internals the repository's general structural API would
couple Renderer to a linter implementation boundary rather than to a parser
contract.

The adapter boundary makes the parser replaceable. If future requirements need
finer source offsets or a different Markdown dialect, the Markdown capability
can change its underlying parser without forcing every Element implementation
to change with it.

## Alternatives and consequences

**PyMarkdownLnt alone.** This minimizes dependencies and parser disagreement,
but makes a lint engine's internal token model carry an architectural role its
public application API does not currently target.

**markdown-it-py alone with local linting.** This gives one structural engine
but discards mature generic rule and autofix coverage already provided by
PyMarkdownLnt.

**A newer positional-AST parser plus PyMarkdownLnt.** A richer positional tree
could eventually reduce adapter work for inline source offsets. The current
need is satisfied by markdown-it-py's mature block structure and source maps;
the adapter keeps future replacement possible if that tradeoff changes.

**Continue the handwritten Markdown parser.** This avoids another dependency
only by making each new Renderer need another piece of Markdown grammar owned
locally. The maintenance burden grows with the exact capability the dependency
is intended to supply.

The accepted cost is two Markdown engines. They can disagree on edge cases.
When that occurs, the parser-backed Markdown structural model is authoritative
for element discovery and bounded edits; PyMarkdownLnt remains authoritative
only for the lint rules it reports. Corpus fixtures should exercise dialect
features used by both so meaningful disagreements become visible regressions
rather than silent interpretation drift.
