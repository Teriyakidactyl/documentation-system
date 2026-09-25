# Conspicuous canary conventions

## Context

An agent can produce a superficially plausible free-form document without
having read or applied the conceptual guidance that governs it.

A separate receipt stating that guidance was read is weak evidence for this
case. The stronger signal can be the artifact itself: important guidance often
has consequences that should be visibly present when it actually shaped the
work. Their conspicuous absence can tell a human reviewer that something went
wrong, and some absences can also be detected mechanically.

This is a design note, not a selected repository convention.

## General idea

Prefer guidance whose application leaves useful, native fingerprints in the
artifact.

A good conspicuous canary is not merely a magic phrase proving that an agent
saw one instruction. It is normally a property the artifact should have anyway
when the governing concept was applied correctly.

Examples include:

- required structural elements whose absence is obvious at a glance;
- metadata whose relationships encode an authoring decision rather than merely
  recording that a procedure ran;
- heading or section shapes derived from the governing model;
- required distinctions that make conceptual collapse visually apparent; and
- combinations of individually lintable properties whose collective absence
  strongly suggests that the governing workflow was never entered.

The useful failure signal is often **conspicuous absence**. A document may look
generally competent while still looking unmistakably unlike an artifact
produced under its governing guidance.

## Canary properties

A useful artifact canary should tend toward these properties:

- **native**: it belongs in the artifact for a real reason rather than only as
  audit decoration;
- **conspicuous**: a reviewer can notice its absence without reconstructing the
  whole authoring history;
- **lintable where practical**: deterministic structure should be checked by
  code rather than left solely to visual review;
- **causally relevant**: satisfying the canary should require applying at least
  part of the governing model, not merely copying a token;
- **diagnostic in groups**: several missing fingerprints may indicate one
  upstream failure to load or follow guidance rather than many unrelated local
  defects; and
- **non-authoritative**: presence is evidence of a shaped artifact, not proof
  that the agent understood every governing concept.

Semantic canaries and mechanical canaries need not have the same strength.
A structural marker can prove that a structural condition was met. It cannot
prove comprehension.

## EOF truncation canary

A special case may justify an intentionally simple token because the condition
being tested is itself mechanical completeness.

Candidate convention:

```text
eof:<uid>
```

The candidate means that a controlled artifact ends with a canary containing
that artifact's UID.

Possible contract:

1. The canary appears exactly once at the literal end of the artifact, allowing
   only the file's final newline after it.
2. The value matches the artifact's controlled UID.
3. A retrieval or workflow claiming a complete-document read must have observed
   the matching EOF canary.
4. A linter can reject a missing, duplicated, misplaced, or mismatched canary.
5. A user inspecting a supposedly complete retrieval has a conspicuous positive
   marker for the endpoint that should have been reached.

This does not prove that the agent read or understood the preceding content.
It makes one narrower failure easy to see: retrieval that stopped before the
controlled artifact's expected end.

That narrow guarantee is valuable because truncation can otherwise masquerade
as a successful full-document read.

## Relationship between the two canary uses

The EOF case and conceptual artifact fingerprints solve related but different
problems.

```text
EOF canary
    -> Did retrieval reach the expected end of this artifact?

artifact fingerprint
    -> Did the governing guidance leave the consequences we expect in the work?
```

The first can be nearly binary and fully lintable. The second can range from
fully structural to semantic and judgment-dependent.

Both make silent agent failure more observable by designing an expected signal
into the surface that the user or tooling already inspects.

## Open questions

The EOF form remains deliberately unresolved:

- whether `eof:<uid>` should be visible prose, an ordinary HTML comment, or a
  small structured representation;
- whether every controlled artifact should carry it or only artifacts whose
  routing directive can require a full read;
- whether authoring, Organizing, or another tool should create and validate it;
- how generated files and non-Markdown controlled artifacts should represent
  the same end condition; and
- whether a general canary convention should name different assurance strengths
  for mechanical presence, structural conformance, and semantic fingerprints.

Do not treat this note as deciding those questions.
