# Diátaxis is a partial fit for amnesiac agents

## Context

Diátaxis derives its four documentation kinds from two dimensions of a
practitioner's relationship to a skill:

- **action vs cognition**: doing versus knowing or understanding;
- **acquisition vs application**: study versus work, or acquiring a skill
  versus applying it.

Those dimensions produce Tutorial, How-to, Explanation, and Reference as
different responses to what the user is doing and what state their relationship
to the skill is in.

The Documentation System increasingly treats an agent arriving at a repository
or document boundary as potentially amnesiac. The same agent may perform many
different tasks, but repository-specific knowledge available in one encounter
cannot be presumed to persist into another.

Official Diátaxis descriptions of the model:

- <https://diataxis.fr/foundations/>
- <https://diataxis.fr/map/>
- <https://diataxis.fr/compass/>

## Observation

Diátaxis is a partial rather than complete fit for documentation designed for
amnesiac agents.

For a human practitioner, acquisition and application can describe different
situations of a user whose accumulated competence persists across encounters.
The person at work can apply skill learned earlier; the person at study can
acquire more of a skill they continue to possess afterward.

For an amnesiac agent, competence is not a durable property of a distinct
reader persona. The same agent can act competently when the required knowledge
is present in active context and then lose that effective competence when the
context is absent. A later encounter does not necessarily contain what an
earlier Tutorial, Explanation, Reference lookup, or workflow established.

The Diátaxis quadrants therefore do not by themselves model a central
agent-facing problem: how the documentation surface establishes enough active
knowledge state for the same agent to continue correctly.

This is an observation about the fit of the model, not a decision about how the
Documentation System should replace, extend, or reinterpret it.

## Rationale

The mismatch does not make the Diátaxis dimensions useless.

**Action vs cognition** still distinguishes material whose immediate job is to
support doing from material whose immediate job is to support knowing,
reasoning, or understanding.

**Acquisition vs application** can still distinguish whether a document unit is
helping establish a capability or helping exercise a capability already
available in the current working context.

Those distinctions may be especially useful when reasoning about
multi-quadrant documents. One bounded artifact can legitimately contain units
with different local relationships to the same agent even though that agent is
not a different persistent user at each boundary.

The useful part of Diátaxis may therefore be its two-dimensional analysis of
the work a document unit performs, while the mismatch lies in treating the
quadrants as a sufficient model of the reader state that agent-facing
documentation can presume.

## Consequences

Do not treat this note as authority for changing Technical Writing, quadrant
definitions, or multi-quadrant document rules.

When those subjects are reconsidered, preserve the distinction between:

1. what the Diátaxis axes reveal about the local function of a document unit;
2. what persistent human-user assumptions are embedded in the usual quadrant
   interpretation; and
3. what an amnesiac agent must have reconstructed in active context before a
   document unit can safely rely on prior competence.

The eventual design response remains open.
