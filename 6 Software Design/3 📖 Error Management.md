---
description: >-
  `Consult when` *software can reject input, fail during execution, or
  propagate failures across component boundaries and the caller-facing error
  contract is not already fixed* `to` **design an error contract that
  preserves source-addressable origin, accumulates propagation context and
  independently knowable failures, and exposes sufficient structured
  information for the caller to respond without reconstructing hidden
  execution state**.
quadrant: Reference
outline:
  topology: tree
  axis: error-management concern
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

# 📖 Error Management

Error management governs the failure information software exposes across a
boundary. Treat that information as part of the caller contract, not as an
implementation afterthought.

A validation diagnostic and an execution error can share a command response
without becoming the same domain value. Validators continue to return the
structured diagnostics defined by
<a href="1%20%F0%9F%93%96%20Software%20Design%20Principles.md#53-diagnostics" uid="M8MDHY">documentation-system:§6.1#5.3</a>.
Execution failures use the principles below when construction, evaluation,
or orchestration cannot continue normally. A command boundary may collect both
and present them through one result.

Resolve error design in this order:

```text
consumer and required decision
-> failure boundary
-> origin and subject
-> local identity and classification
-> propagation and accumulation
-> response projection
-> persistence, when separately required
```

Do not begin by choosing an exception hierarchy, log format, status code, or
serialization schema while an earlier decision remains unsettled.

## 1. Error consumers

### 1.1 Consumer observation

An **error consumer** is the caller or reader that receives failure information
and must decide what happens next. Identify that consumer and the decision it
must make before designing the error surface.

> [!IMPORTANT]
> **Observe the consumer before choosing the error representation.** Determine
> who or what receives the failure and what decision it must make before
> choosing message density, structured fields, recovery information, or
> persistence. An agentic caller is the repository default when no concrete
> constraint selects another primary consumer. That default does not erase
> human, programmatic, or operational consumers; it prevents an unspecified
> audience from silently determining the contract.

A consumer distinction is load-bearing only when it changes what information
must be exposed or how that information can be acted on. Do not create separate
error semantics merely because several presentation surfaces exist.

### 1.2 Agentic callers

Design the normal command response so an agent can diagnose and choose its next
action without performing a second diagnostic operation for information already
known when the failure occurred.

The default agent-facing response therefore favors high-information structured
failure data over terse prose. Return the semantic condition, source-addressable
origin, affected subject, relevant known values, propagation context, and
deterministic recovery information when available.

Do not require the agent to:

- parse prose to recover a stable classification;
- inspect a logfile for facts already available to the failing invocation;
- request a separate "last error" or debug operation before it can recover;
- infer which subordinate component actually emitted a top-level failure;
- reconstruct valid alternatives that the tool already computed.

Additional information is useful when it changes the caller's next decision.
Internal state that does not change that decision is debug material rather than
default response content.

### 1.3 Other consumers

A human-facing CLI may compress or reorder the same canonical failure data for
scanability. A programmatic caller may consume a serialization with no prose
beyond the message field. An operator may need correlation, timing, or
persistence that does not belong in the caller-facing response.

These are projections of one failure model. Do not create a human error, agent
error, API error, and logged error as independently authored truths.

When another consumer has a concrete constraint that conflicts with the agentic
default, state the selecting condition at that boundary and preserve the
canonical failure facts underneath it.

## 2. Error identity

### 2.1 Source-addressable origin

The component that first recognizes a semantic failure establishes its
**origin**. Origin is immutable evidence about where the error was produced.

Represent origin with enough source information for a caller or maintainer to
navigate directly to the owning implementation. For code-backed tooling, use
the repository's real implementation vocabulary rather than a detached error
namespace:

```yaml
origin:
  module: documentation_system.markdown
  file: 4 Tooling/4 🛠️ Markdown.py
  operation: resolve_section
  symbol: Markdown.resolve_section
```

Use the module or owning implementation namespace as the stable source
namespace. Keep the repository-relative file path because it provides direct
navigation. Include the operation or symbol at the narrowest stable boundary
that actually recognized the failure.

A source line may be returned as navigation metadata, but do not make a line
number part of durable error identity because ordinary edits move it.

A caller may append propagation context. It must not replace the original
origin with itself.

### 2.2 Local error name

Name an error locally inside its origin instead of constructing a globally
abstract taxonomy.

```yaml
name: SECTION_NOT_FOUND
```

The effective identity is the source namespace plus the local name:

```text
documentation_system.markdown.resolve_section::SECTION_NOT_FOUND
```

This keeps the error visibly connected to the module that owns its semantics
and avoids identifiers whose only purpose is global uniqueness.

Do not use names such as `INVALID_INPUT`, `RESOURCE_ERROR`, or
`OPERATION_FAILED` as complete identities when the originating capability
knows a more specific condition.

### 2.3 Classification

Classification describes a condition across origins without replacing origin
or local identity.

```yaml
classification: absent
```

Useful classifications include conditions such as absent, malformed,
ambiguous, conflicting, unsupported, unavailable, and internal. Add one only
when a caller can make a meaningfully different decision from it.

Two origins may both emit an `absent` classification while retaining distinct
local identities and recovery rules. Classification is therefore a secondary
query dimension, not the primary namespace.

### 2.4 Subject

The **subject** identifies the input, artifact, field, selector, resource, or
other domain object about which the failure is true.

```yaml
subject:
  path: docs/example.md
  line: 42
  selector: "3.2"
```

Keep subject separate from origin. A Markdown resolver can originate an error
whose subject is a controlled document, and a YAML parser can originate an
error whose subject is a frontmatter payload.

Include only subject facts that are safe to expose and useful for identifying
or correcting the failure.

## 3. Error content

### 3.1 Message

The message states the concrete failure in domain language. It complements
structured fields rather than encoding them for later parsing.

Prefer:

```text
No section resolves selector '3.2'.
```

over:

```text
Resolution failed.
```

Do not repeat every structured field in prose merely to make the message look
complete. The message explains the condition; the record carries the facts.

### 3.2 Details

Put occurrence-specific facts in structured `details` when they help explain
or recover from the failure and do not have a more specific first-class field.

Examples include expected values, found values, candidate targets, dependency
state, or a bounded set of conflicting identifiers.

```yaml
details:
  requested: "3.2"
  nearby:
    - "3"
    - "3.1"
    - "3.3"
```

Do not capture arbitrary local variables, complete argument lists, environment
contents, credentials, or implementation state merely because they are
available.

### 3.3 Recovery

Return recovery information when the originating capability can state a valid
next action deterministically.

```yaml
recovery:
  action: select_section
  candidates:
    - "3.1"
    - "3.3"
```

Keep uncertain advice in the message or omit it. Do not encode a guessed fix as
an executable recovery action.

A recovery instruction belongs to the origin that knows the relevant invariant.
A top-level caller must not invent a repair for a subordinate domain merely to
make the response appear helpful.

## 4. Propagation

### 4.1 Provenance

**Provenance** records the meaningful operation boundaries crossed after the
error was created.

```yaml
provenance:
  - document.inspect
  - registry.rebuild
  - organizing.refresh
```

Origin answers where the failure was produced. Provenance answers how it
reached the current response.

Append provenance as the error crosses a boundary whose operation is useful for
understanding execution. Do not mirror every language-level stack frame. A
runtime traceback is a debug projection, not the default provenance model.

### 4.2 Context enrichment

A caller may add context that it legitimately knows and that remains separate
from the originating facts.

For example, an orchestration layer may add the corpus root or requested
top-level operation while preserving the subordinate origin and local error
name.

Do not implement propagation by repeatedly wrapping the message:

```text
Refresh failed: registry failed: document failed: frontmatter failed: UID missing
```

Preserve one originating message and represent the route structurally.

### 4.3 Causal relationships

When one surfaced failure causes another independently meaningful failure,
represent the causal relationship explicitly rather than relying on response
order or repeated prose.

Use a stable occurrence identifier within the command result when causal edges
are required:

```yaml
id: e17
caused_by:
  - e03
```

Do not manufacture separate downstream errors for every skipped operation when
one prerequisite failure already explains why those operations could not be
evaluated. Record the stop or dependency relationship instead.

## 5. Error accumulation

### 5.1 Collection

Return the maximum set of independently knowable failures that can be
discovered safely in one invocation.

A validation, inspection, compilation, indexing, or other read-oriented pass
should continue across independent subjects after one subject fails when the
remaining evaluations do not depend on invalid state.

A parent routine collects subordinate failure records rather than flattening
them into one parent error. The parent may also originate its own error when a
distinct parent-owned invariant fails.

This rule prevents fix-run-fix-run loops where the tool already had enough
information to report several failures in the first run.

### 5.2 Hard-stop boundaries

Stop collection when continuing would make later findings untrustworthy or
would risk unsafe mutation.

Typical stop conditions include:

- a required model cannot be constructed, so later checks would reason about
  invented state;
- a mutation precondition fails and continuing could produce a partial or
  conflicting write;
- an unavailable prerequisite makes dependent evaluations semantically
  meaningless;
- integrity uncertainty prevents distinguishing a valid result from corruption.

Return every valid finding discovered before the stop and mark completion so
the consumer can distinguish an exhaustive result from a partial one.

```yaml
status: failure
completion: partial
stopped_at: write.apply
```

### 5.3 Origin-first grouping

Group the default failure response primarily by source-addressable origin.

```yaml
origins:
  - origin:
      module: documentation_system.frontmatter
      file: 4 Tooling/5 🛠️ Frontmatter.py
      operation: validate
    errors:
      - name: REQUIRED_FIELD_MISSING
        classification: malformed
        subject:
          path: docs/a.md
          field: uid
      - name: INVALID_FIELD_VALUE
        classification: malformed
        subject:
          path: docs/b.md
          field: quadrant

  - origin:
      module: documentation_system.markdown
      file: 4 Tooling/4 🛠️ Markdown.py
      operation: resolve_link
    errors:
      - name: TARGET_NOT_FOUND
        classification: absent
        subject:
          path: docs/c.md
          line: 42
```

Within an origin group, a presentation may secondarily organize by local name,
classification, severity, subject, or another domain-relevant dimension.

Do not make a cross-origin classification the default top-level grouping.
Doing so hides which implementation boundary owns the failure.

### 5.4 Deterministic ordering

Keep response ordering deterministic so repeated runs over unchanged inputs
produce comparable output.

Order origin groups by a stable source key or deterministic execution order.
Order records inside a group by stable subject coordinates or another
domain-owned ordering rule.

Do not depend on incidental thread completion, filesystem enumeration, hash
iteration, or exception timing.

## 6. Response projections

### 6.1 Default command response

The normal command response is the primary diagnostic surface for the caller.

For an agentic caller, return enough structured information to distinguish at
least these decisions when the originating domain can know them:

```text
correct input
acquire prerequisite
select another target
retry
stop
escalate
```

Do not withhold caller-relevant facts behind a debug flag solely to keep the
default response short. Prefer high-information responses over minimal
responses.

A command result may contain diagnostics and execution errors together, but
preserve each originating value and its semantics. The command boundary
coordinates presentation; it does not become the semantic owner of subordinate
failures.

### 6.2 Complete and partial responses

State whether error discovery completed.

Use `complete` when every applicable evaluation that could safely run did
run. Use `partial` when a hard-stop boundary prevented further trustworthy
evaluation.

A nonzero process exit alone does not communicate this distinction.

### 6.3 Unexpected failures

Convert an unexpected implementation exception into the canonical failure
model once, at the first meaningful repository-owned boundary capable of
identifying the failed operation.

Preserve:

- the repository-owned origin where conversion occurred;
- an `internal` or equivalent classification;
- the exception type;
- the exception message when safe and meaningful;
- the subject and operation context already known at that boundary.

Do not relabel the boundary as though it semantically understood an unexpected
condition that it did not understand.

A full language traceback, stack locals, and implementation frames belong to an
explicit debug projection. Their absence must not make the default response
incapable of locating the repository-owned failure boundary.

### 6.4 Canonical result and projections

Maintain one canonical command result and derive consumer-specific
representations from it.

```text
canonical failure result
├── agent-facing CLI projection
├── human-facing CLI projection
├── machine-readable serialization
├── GitHub annotation projection
└── telemetry projection, when selected
```

A projection may filter or format facts under an explicit consumer constraint.
It must not silently change error identity, origin, provenance, causal
relationships, or completion state.

## 7. Persistence and verification

### 7.1 Logs and telemetry

Use logs or telemetry when persistence serves a purpose distinct from immediate
caller recovery, such as cross-invocation correlation, operational monitoring,
audit, or performance analysis.

Do not require ordinary caller recovery to read a log. If the failing
invocation already knows a fact needed for the caller's next decision, include
that fact in the normal response.

Do not persist raw arguments, arbitrary keyword values, complete environment
state, or sensitive subject data by default. Persistence expands both retention
and exposure boundaries and therefore requires its own selecting condition.

A retained Fault Record serves historical evidence and recurrence analysis, not
ordinary runtime error delivery. Do not create one merely because a command
returned an error.

### 7.2 Contract stability

Treat source-addressable origin, local error name, classification semantics,
and structured field meanings as interface contracts once callers depend on
them.

A file move may update the physical file projection while a stable module and
symbol continue to identify the same origin. A semantic move to a different
owner is an origin change and should not be disguised as a path-only refactor.

Do not preserve an obsolete global error identifier at the cost of obscuring
the module that now owns the condition. Preserve compatibility at an explicit
boundary when a real consumer requires it.

### 7.3 Failure-contract tests

Test error behavior as an interface rather than testing only for nonzero exit
status or raised exceptions.

A failure-contract test should exercise the applicable guarantees:

- the originating module, file, operation, and local name survive propagation;
- parent routines append provenance without replacing origin;
- independently knowable subordinate failures are returned in one invocation;
- hard-stop boundaries report partial completion without inventing downstream
  findings;
- origin groups and records are deterministically ordered;
- structured details contain the facts required for the intended next decision;
- deterministic recovery is present only when the domain can prove it;
- the default agent-facing response does not require a logfile or second
  diagnostic command for known recovery facts;
- unexpected exceptions identify the repository-owned conversion boundary while
  reserving full tracebacks for debug projection;
- every presentation projection preserves canonical error identity and
  completion semantics.

Test the failure path that callers actually consume. An internal exception unit
test does not establish that the command boundary preserved its origin,
aggregation, and recovery information.
