---
form:
  path: '<a href="../../2%20Technical%20Writing/3%20Document/1%20Document%20Forms/11%20Architecture%20Decision%20Record/README.md" uid="A1FANY">documentation-system:§2.3.1.11</a>'
  version: '1.0'
description: >-
  `Read in full when` *the rationale for organizing Software Design around
  recurring independent decision domains rather than architecture viewpoints,
  named traditions, or a predetermined maximal taxonomy needs to be reviewed*
  `to` **understand why concern-oriented guidance is the primary navigation
  model while viewpoints and perspectives remain completeness lenses for
  architecture work**.
quadrant: Explanation
decision:
  status: accepted
  decided-at: '2026-09-24T15:48:55-07:00'
  repository-revision: b7e028e25ac2be1995f6a36033abf0bb241c3425
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

# 💡 Why Software Design Is Organized Around Recurring Independent Decisions

## Context

Software Design is growing from a compact principles reference into a reusable
body of guidance. Error Management and Testing have already emerged as useful
independent topics because a maintainer can encounter either problem across many
projects and architectures and should not need to reconstruct the design space
from implementation clues.

A possible way to predict the eventual shape of Software Design was to use the
viewpoints and perspectives described by established software-architecture
methods. Those lenses are valuable because they prompt architects to inspect a
design from multiple structural and cross-cutting directions. They are less
natural as the repository's primary navigation categories, however. A maintainer
usually arrives with a problem such as error behavior, verification,
persistence, configuration, or concurrency rather than with a need to enter a
"functional" or "development" viewpoint.

This distinction matters especially for amnesiac agents. Repository structure
should lead them toward reusable decisions by the problem they must resolve,
rather than require them to infer which architectural lens contains the answer.

## Decision

Organize Software Design primarily around **recurring design concerns whose
decisions can arise independently across different systems and architectures**.

A concern earns independent guidance when it recurs broadly enough, contains a
stable design vocabulary or decision sequence, and would otherwise force an
amnesiac maintainer to reconstruct consequential choices from first principles
or from existing code.

Use architecture viewpoints and perspectives as **completeness lenses** when
designing or reviewing an architecture. Do not use them as the default Software
Design folder taxonomy merely because they provide a comprehensive way to
describe architectures.

Treat named design traditions such as Domain-Driven Design, information hiding,
GRASP, Ports and Adapters, or Viewpoints and Perspectives as sources of tested
concepts and reasoning. They may inform several concern domains without
determining the navigation hierarchy themselves.

Allow formal architectures to resolve several decisions within a concern for a
recurring selecting condition. Keep general concern guidance distinct from
those formal architectures so a reader can either solve a local design question
or select an established architecture without conflating the two.

Do not pre-create a maximal hierarchy of empty Software Design topics. Add a
topic when a concrete recurring decision domain has enough useful guidance to
justify an independently routable location.

## Rationale

A concern-oriented taxonomy matches the question a maintainer actually knows
they have. "How should failures behave?" routes naturally to Error Management;
"how should this contract be proved?" routes naturally to Testing. The same
pattern can later justify other topics such as persistence, configuration,
concurrency, compatibility, or security when repository needs establish them.

Viewpoints and perspectives solve a different problem. They reduce architectural
blind spots by asking whether relevant context, information, runtime,
development, operational, security, resilience, performance, and evolution
concerns have been considered. That makes them strong inputs to future guidance
for designing and reviewing architectures, but weak substitutes for problem-led
navigation.

This separation also prevents a literature-derived taxonomy from becoming cargo
cult. The repository can use established architecture thinking without creating
folders simply because a book names a viewpoint, and it can add concern domains
that are especially important to this environment even when they do not map
cleanly to one canonical architecture framework.

The decision preserves two valid uses of Software Design. A reader may consult
one concern to resolve a local decision, while an architecture author may draw
from several concern references and use architectural lenses to check for
omissions before recording a formal architecture.

## Alternatives and consequences

**Organize by architecture viewpoints and perspectives.** This offers a
well-established completeness model, but it makes navigation depend on knowing
which lens applies before the maintainer has resolved the design problem. Errors
and Testing also demonstrate that useful recurring concerns can cut across
several viewpoints.

**Organize by named design traditions.** A DDD, GRASP, Parnas, Ports and
Adapters, or similar hierarchy would preserve recognizable intellectual
lineage, but real design decisions routinely draw from several traditions.
Readers would have to translate their current problem into a school of thought
before finding guidance.

**Keep all guidance in Software Design Principles.** This minimizes navigation
but causes the principles document to accumulate unrelated decision spaces and
makes specialized architectures harder to route to as the body grows.

**Define the complete future taxonomy now.** This gives an apparently orderly
destination, but encourages empty categories and speculative boundaries.
Concern domains should earn independent locations from recurring use.

The accepted consequence is that Software Design's final folder shape is not
fixed in advance. Its growth must be justified concern by concern. Architecture
guidance will also need an explicit way to use viewpoints, perspectives, and
other completeness techniques without turning those lenses into mandatory
document sections or navigation categories.
