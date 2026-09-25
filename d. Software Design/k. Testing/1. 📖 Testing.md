---
uid: XW9VC3
description: >-
  `Consult when` *software behavior, invariants, or component relationships
  require executable verification and the appropriate test boundary,
  environment, or assertion strategy is not already fixed* `to` **design
  tests that prove the owned contract at the smallest faithful boundary,
  remain deterministic and maintainable across implementation changes, and
  expose failures with enough evidence to locate the violated invariant**.
quadrant: Reference
outline:
  topology: tree
  axis: testing concern
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

# 📖 Testing

Testing produces executable evidence that a software contract or invariant still
holds.

A test is trustworthy when its pass or failure can be attributed to the property
it claims to verify. Test design therefore begins with the owned contract, not
with a preferred framework, test size label, or mocking technique.

Resolve test design in this order:

~~~text
owned contract or invariant
→ consumer-visible behavior
→ smallest faithful verification boundary
→ fixture and environment requirements
→ dependency fidelity
→ case-generation strategy
→ assertion
→ failure evidence
→ larger relationship checks still required
~~~

## 1. Verification subject

### 1.1 Owned contract

State what must remain true before choosing how to test it.

A useful test proves one or more externally meaningful properties such as:

~~~text
input contract
output contract
state transition
domain invariant
error contract
serialization round trip
relationship between components
architectural dependency rule
idempotence or convergence property
~~~

Do not make implementation steps the test subject unless those steps are
themselves an explicit architectural contract.

### 1.2 Independent authority

Expected behavior must come from an authority independent enough to detect a
defect in the implementation under test.

A specification, domain invariant, stable public schema, consumer contract,
known counterexample, or independently derived reference implementation can
supply that authority.

Do not ask the implementation under test to generate both the result and the
expected answer.

## 2. Verification boundary

Use the smallest boundary that can faithfully prove the property.

A narrow boundary improves diagnosis and execution cost when the property is
locally owned. A larger boundary is required when the property concerns
interaction, transport, persistence, composition, or another relationship that a
local test cannot observe.

Do not substitute an internal method test for a public-boundary contract when
the risk lies in serialization, dispatch, propagation, or presentation.

Do not force every property through an end-to-end path when a smaller owned
boundary proves it completely.

## 3. Public behavior over implementation choreography

Assert stable observable semantics rather than incidental call sequences,
private methods, intermediate variables, or internal organization.

Refactors that preserve the contract should usually preserve the test.

This does not forbid white-box structural verification. Import graphs,
annotations, declarations, ownership rules, or other architecture-visible code
structure may themselves be the contract. In that case, structure is the
intentional verification subject rather than an accidental implementation
detail.

## 4. Environment and isolation

A test should depend only on declared inputs and controlled test resources.

Prefer temporary files, local fixtures, deterministic clocks, explicit
configuration, hermetic substitutes, and other controlled dependencies over
live mutable state.

Tests must not depend on execution order or residue from earlier tests.

When external behavior is itself the contract, isolate ordinary fast tests from
the live dependency and add a separate contract or integration check that proves
the substitute remains faithful.

## 5. Dependency fidelity

Prefer the real implementation when it is fast, deterministic, and safe.

Use a faithful fake when the real dependency is impractical but its semantics
can be reproduced locally.

Use mocks for narrow interaction constraints that cannot be established more
directly. Do not reproduce the implementation's call choreography in mocks and
then treat agreement with that choreography as proof of behavior.

A lower-fidelity substitute creates a new verification obligation: prove that
the substitute still represents the contract that matters.

## 6. Cases

### 6.1 Success and failure

Test successful behavior and deliberate failure behavior when both are public
contracts.

A command that returns valid success output but collapses malformed input into an
unstructured crash is not adequately verified by its success tests.

### 6.2 Boundary cases

Select cases at semantic boundaries: missing versus present, valid versus
malformed, one versus many, empty versus populated, before versus after a
threshold, supported versus unsupported, or complete versus partial.

Avoid arbitrary example multiplication when several examples exercise the same
property.

### 6.3 Regression counterexamples

When a consequential fault is discovered, preserve the smallest useful
counterexample when an executable test can prevent recurrence.

A regression case should state the property the fault violated rather than
memorializing irrelevant implementation details from the incident.

## 7. Generated and property-based verification

Use generated cases when the invariant applies across a domain larger than a
small authored example set.

Strong property candidates include:

~~~text
parse → serialize → parse preserves meaning
normalize(normalize(x)) == normalize(x)
valid input never crashes the compiler or linter
ordering remains deterministic under input permutation
encode/decode round trips
optimized behavior matches a simpler reference
~~~

Generation expands the search for counterexamples. It does not supply the
invariant being tested.

When generated input requires semantic validity that types alone cannot express,
derive it from an independent schema or generator, or escalate to authored
fixtures.

## 8. Assertions

Assert every stable part of the contract that matters to a consumer.

Do not assert exact prose merely because it is easy. Do assert structured
semantics such as stable error identity, origin, state, result shape, ordering,
or recovery behavior when those are contractual.

A weak assertion such as "did not crash" can be useful as a baseline probe but
must not be mistaken for functional correctness.

Prefer assertions that identify the violated invariant directly when they fail.

## 9. Structural and semantic verification

Separate deterministically decidable conformance from judgment.

**Structural verification** checks properties that can be evaluated
mechanically: schemas, type surfaces, import rules, required declarations,
response shapes, deterministic transformations, or architectural constraints.

**Semantic verification** evaluates properties that require interpretation:
whether responsibilities are well placed, an explanation is adequate, or a
design tradeoff is justified.

Use automation to enforce what can be decided mechanically. Do not encode
subjective judgment as a brittle pseudo-binary test merely to increase
automation.

When semantic review repeatedly discovers the same mechanically recognizable
fault, consider promoting that condition into structural verification.

## 10. Determinism

Repeated execution against the same declared state should produce the same
verification result unless nondeterminism is itself the subject.

Control ordering, random seeds where relevant, time, temporary resources, and
environmental dependencies sufficiently to make a failure attributable.

Flaky tests weaken evidence because the consumer cannot tell whether the source
change caused the failure.

## 11. Failure evidence

A test failure is itself an error consumed by a maintainer or agent.

Return enough evidence to locate:

~~~text
the test or generated case
the violated contract
the relevant subject
expected and observed semantics
the owning implementation boundary when known
~~~

Do not require an out-of-context agent to rerun the complete suite merely to
discover information already known by the failed assertion.

Keep machine-readable structure available when CI or agents must aggregate and
act on findings.

## 12. Coverage

Coverage answers whether the relevant verification surface is represented, not
how many lines happened to execute.

Prefer coverage measures tied to owned contracts or discoverable public
surfaces:

~~~text
public commands with boundary verification
error identities with contract tests
architectural rules with structural checks
transformations with invariant tests
known fault classes with regression coverage
~~~

A coverage gap should be explicit. A known gap can be governed deliberately;
an invisible gap cannot.

A ratchet may prevent known coverage from degrading when immediate complete
coverage is impractical.

## 13. Formal architectures

Use a Testing architecture when a recurring verification surface justifies a
reusable arrangement of discovery, fixture production, execution, assertions,
coverage, and reporting.

A testing architecture must identify which information is independently
authoritative and which parts may be derived mechanically.

The architecture package may retain research and decision provenance without
turning that supporting material into the executable contract.
