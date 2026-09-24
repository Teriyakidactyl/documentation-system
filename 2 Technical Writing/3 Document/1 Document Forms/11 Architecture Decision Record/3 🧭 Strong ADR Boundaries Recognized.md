---
description: >-
  `Read in full when` *ADR instructions are understood but the boundary
  between useful decision provenance and implementation narrative remains
  ambiguous* `to` **distinguish strong Context, Decision, and Rationale
  statements from plausible but non-decisional substitutes**.
quadrant: Tutorial
writing-style:
  formality: professional
  tone: neutral/detached
  mode: declarative
  density: moderate
  abstraction: concrete/specific
  redundancy: zero
  signposting: light
  register: technical
---

# 🧭 Strong ADR Boundaries Recognized

## Context boundary recognized

**Bad:** "We rewrote the Markdown tooling and started comparing AST parsers."

**Good:** "Executable Document Elements require Markdown structures to be
identified with source ranges precise enough for deterministic bounded edits."

The good specimen names the pressure that forces a choice. The bad specimen
only narrates preceding work.

## Decision boundary recognized

**Bad:** "We investigated markdown-it-py, Wenmode, and PyMarkdownLnt."

**Good:** "Use markdown-it-py for structural Markdown parsing and
PyMarkdownLnt for generic Markdown linting and mechanical fixes."

The good specimen commits to a selected architecture. The bad specimen reports
activity without a decision.

## Rationale boundary recognized

**Bad:** "markdown-it-py looked better."

**Good:** "markdown-it-py exposes deterministic block tokens with source-line
maps while remaining a production-stable Python dependency; keeping its tokens
behind the Markdown capability prevents parser-specific types from becoming
repository architecture."

The good specimen preserves the criterion and mechanism that justified the
choice. The bad specimen records an opinion that cannot be re-evaluated.
