---
description: >-
  `Consult when` *a callable software surface is mechanically discoverable
  and baseline verification should expand when that surface changes* `to`
  **design verification that discovers public operations, derives safe cases
  from canonical runtime declarations, evaluates independent contracts, and
  exposes coverage gaps without maintaining a duplicate handwritten test
  inventory**.
quadrant: Reference
outline:
  topology: tree
  axis: self-assembling verification architecture concern
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

# 📖 Self-Assembling Verification Architecture

Self-Assembling Verification derives a baseline verification suite from a
mechanically discoverable public surface.

The architecture reduces duplicated test inventory while preserving an
independent oracle:

~~~text
discover callable surface
→ inspect canonical public declarations
→ derive fixtures and boundary cases where safe
→ execute the real public boundary
→ evaluate independent contracts
→ expose cases that could not be derived
~~~

Self-assembly concerns test discovery and case construction. It does not allow
the implementation under test to define its own expected answer.

## 1. Selecting condition

Use this architecture when:

- the public callable surface can be discovered mechanically;
- its input shape is available through typed declarations, schemas, signatures,
  or another canonical runtime representation;
- baseline behavior can be checked against independent cross-command contracts;
  and
- newly added public operations should automatically become visible to
  verification.

Do not adopt the machinery solely to eliminate handwritten tests. Stateful
domain scenarios, semantic expectations, or cross-system contracts may still
require authored fixtures and tests.

## 2. Architecture

~~~text
public declarations
├── callability marker or registry
├── input schema
├── runtime-useful examples and constraints
└── optional verification override
          │
          ▼
verification discovery
          │
          ▼
case assembler
├── baseline valid case
├── mechanically derivable invalid cases
└── declared stateful fixture when required
          │
          ▼
real callable boundary
          │
          ▼
independent contract evaluators
├── common response contract
├── error architecture contract
├── command-specific declared invariant
└── structural architecture rules
          │
          ▼
coverage + findings
~~~

The same declarations may serve runtime discovery, agent help, schema
generation, and verification. Prefer that shared authority over parallel
test-only metadata.

## 3. Public surface discovery

A public operation must carry a mechanically recognizable callability signal.

Possible realizations include a decorator, interface implementation, command
registry, route declaration, exported schema, manifest entry, or another
machine-readable marker.

The verifier derives the command inventory from that signal.

Do not maintain a second handwritten list of commands that are supposed to be
tested when the runtime already owns a complete discoverable inventory.

A newly callable operation therefore changes verification coverage
automatically.

## 4. Input contract discovery

The verifier reads the canonical input contract for each discovered operation.

Useful information includes:

~~~text
field or parameter names
required versus optional
types
defaults
allowed values
bounds and constraints
schema relationships
runtime-useful examples
~~~

Typed Python models and generated JSON Schema are one implementation. They are
not required by the architecture.

The input declaration must already have a runtime consumer. Do not add metadata
solely to satisfy the verifier when a more natural runtime declaration can carry
the same information.

## 5. Fixture derivation

### 5.1 Baseline derivation

Derive representative safe values from the public contract when the semantics
are sufficiently constrained.

Examples:

~~~text
boolean          → deterministic boolean
bounded integer  → in-range value
enumeration      → declared member
structured value → schema-valid object
path             → isolated temporary artifact when contents can be inferred
~~~

The resulting probe establishes only the property supported by the derivation.
A type-correct generated path does not prove domain correctness merely because
the command returned.

### 5.2 Runtime-useful examples

Prefer examples already needed by command consumers, documentation, generated
schemas, or help systems.

A single declaration can then support:

~~~text
agent orientation
schema generation
help
example invocation
baseline verification fixture
~~~

This reduces duplicated maintenance while keeping the example useful outside
the test suite.

### 5.3 Escalation

Escalate when generic derivation cannot construct a semantically valid state.

Use the least additional authored information necessary:

~~~text
automatic derivation
→ declared fixture overrides
→ authored setup/teardown or stateful scenario
→ dedicated integration test
~~~

An operation that mutates external systems, requires network state, depends on a
multi-document relationship, or needs consequential prior state may opt out of
automatic execution while remaining visible as a coverage gap or explicit
higher-tier case.

## 6. Failure-case derivation

Mechanically derive boundary violations that follow directly from the input
contract.

Common cases include:

~~~text
missing required input
unknown input
wrong primitive type
out-of-range value
invalid enum member
absent temporary target
malformed container when a canonical malformed case exists
~~~

Execute these through the real callable boundary when the goal is to verify
agent-facing or transport-facing error behavior.

Do not generate destructive or externally consequential failures without an
isolated fixture or explicit safety declaration.

## 7. Independent oracles

Self-assembly is trustworthy only when the expected property comes from an
independent authority.

Strong independent oracles include:

- a repository-wide command response contract;
- an Error Management architecture;
- a schema owned outside the implementation operation;
- a domain invariant;
- a round-trip property;
- a canonical reference implementation;
- a consumer contract; or
- an explicit known counterexample.

Weak or circular verification looks like:

~~~text
implementation emits expected value
→ verifier asks same implementation for expected value
→ equality passes
~~~

The public declaration may tell the verifier how to call the operation. It must
not be the sole source of a substantive expected result produced by the same
logic being tested.

## 8. Baseline verification levels

Use capability levels to communicate what self-assembled verification actually
proves.

A useful generic model is:

~~~text
Boundary
    operation is discoverable and reaches the canonical response boundary

Generated
    verifier can derive a semantically valid representative case

Declared
    operation supplies additional fixture or state facts derivation needs

Dedicated
    a distinct authored property, regression, or integration test proves
    behavior not representable by the generic verifier
~~~

Names may vary by implementation. The distinction must remain visible so a
no-crash baseline is not reported as semantic correctness.

## 9. Coverage model

Coverage is derived from the discovered public surface.

A verification report can state:

~~~text
43 callable operations discovered
43 reach the response boundary
31 support generated valid cases
12 require declared stateful fixtures
0 have no failure-boundary verification
~~~

Every public operation belongs to exactly one visible coverage state for each
required verification capability.

Do not silently omit commands the generator cannot exercise.

### 9.1 Coverage ratchet

When complete coverage cannot be achieved immediately, record the accepted gap
set or equivalent baseline and prevent it from silently growing.

Prefer a ratchet tied to named uncovered operations over a percentage detached
from the public surface.

A deliberate baseline update is a governance action, not an automatic
consequence of adding uncovered code.

## 10. Verification integrity

Generated verification can become stale even when the generator still runs.

Detect mismatches between the declarations the verifier assumes and the current
callable surface when practical. A stale or unsupported case should become an
explicit gap rather than silently producing misleading confidence.

Do not introduce hash registries or lock files merely because another
implementation used them. Select drift machinery only when the verification
artifact has independent state capable of becoming stale.

When cases are assembled directly from live canonical declarations on every
run, much of the drift problem disappears by construction.

## 11. CI execution

Continuous integration is the normal execution environment for repository-wide
self-assembled verification.

A CI run should:

~~~text
discover the current callable surface
assemble all safe baseline cases
execute independent contract checks
run dedicated tests
report command-level coverage gaps
fail on violated required contracts
enforce any accepted coverage ratchet
~~~

GitHub Actions is one suitable executor for repositories hosted on GitHub. It is
not part of the semantic architecture.

Run the same verifier locally when practical so CI is not the only environment
capable of explaining a failure.

## 12. Agent-facing findings

The verification result is consumed by an agent or maintainer trying to repair
the repository.

A failed generated case should identify:

~~~text
discovered operation
case derivation source
input or fixture used
violated independent contract
observed structured result
coverage level
owning implementation location when known
~~~

Do not emit only a generic "generated probe failed" message when the verifier
already knows which contract and operation were involved.

When multiple generated cases fail independently, aggregate them so the agent
can repair the surface without repeated CI cycles.

## 13. Relationship to authored tests

Self-assembled verification supplies a broad baseline, not a replacement for
purposeful tests.

Use authored tests for:

- specific domain semantics that cannot be inferred;
- regression counterexamples from consequential faults;
- stateful sequences;
- cross-component relationships;
- persistence and concurrency behavior;
- properties whose independent oracle is an authored expectation; and
- architectures whose guarantees exceed the common callable contract.

The strongest suite combines broad mechanically maintained coverage with narrow
authored tests for behavior that requires human-specified semantic authority.
