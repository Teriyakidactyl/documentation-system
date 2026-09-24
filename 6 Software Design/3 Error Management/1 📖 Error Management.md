---
description: >-
  `Consult when` *software can reject input, fail during execution, or
  propagate failures across component boundaries and the governing error
  architecture is not already fixed* `to` **identify the consumer, failure
  boundary, identity, propagation, accumulation, recovery, presentation, and
  persistence decisions that an error design must resolve**.
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
  abstraction: mixed
  redundancy: zero
  signposting: entry-headers only
  register: technical
---

# 📖 Error Management

Error management governs how software represents a failed or invalid operation
to the consumers that must respond to it. It provides a design vocabulary and
decision order. A formal error architecture may fix these decisions for a
recurring context; otherwise resolve them explicitly for the system at hand.

A validation diagnostic and an execution error can share a response without
becoming the same domain value. Diagnostics describe findings that can coexist
with a valid deterministic result. Errors describe conditions in which the
requested result, transition, or evaluation cannot be established as intended.

Resolve an error design in this order:

~~~text
consumer and required decision
→ failure boundary
→ origin and subject
→ identity and classification
→ propagation and causality
→ accumulation and stopping
→ recovery
→ presentation
→ persistence, when separately required
~~~

Do not begin with an exception hierarchy, log format, status code, or
serialization schema while an earlier decision remains unresolved.

## 1. Consumers

### 1.1 Consumer observation

An **error consumer** is the caller or reader that receives failure information
and must decide what happens next.

> [!IMPORTANT]
> Observe who or what consumes the failure before choosing its representation.
> The consumer and its required next decision constrain message density,
> structured fields, recovery information, transport, and persistence.

Potential consumers include an agent calling a command, a human using a CLI, a
programmatic client, a parent component, an operator investigating runtime
behavior, or an assurance process evaluating retained evidence.

A difference between consumers is architecturally relevant only when it changes
what information must be available or what response behavior is required.
Several presentation surfaces do not by themselves justify several competing
error truths.

### 1.2 Consumer decision

Design the error around the decision it must support.

Typical decisions include:

~~~text
correct input
select another target
acquire a prerequisite
retry
stop
continue with independent work
escalate
inspect retained operational evidence
~~~

Information that cannot change any intended consumer decision is not
automatically part of the normal error contract.

## 2. Failure boundary

A **failure boundary** is the operation or domain boundary at which software can
no longer establish the requested valid result.

Place semantic failure recognition with the component that owns the violated
invariant. A transport or orchestration layer may surface the failure without
becoming the semantic owner of it.

Distinguish a semantic failure from an unexpected implementation exception. A
semantic failure is understood by the domain. An unexpected exception becomes a
domain error only when a meaningful owned boundary converts it into the
system's error model.

## 3. Origin and subject

### 3.1 Origin

**Origin** identifies the component and operation that first recognized the
failure.

Origin is evidence about ownership. Propagation through a parent component does
not change where the failure originated.

Represent origin at a level stable enough to preserve ownership and precise
enough to locate the responsible implementation. Source-addressable module,
file, operation, or symbol information may be appropriate when maintainers or
agents must navigate directly to the owner.

Do not use a moving source line as durable error identity.

### 3.2 Subject

**Subject** identifies the artifact, value, field, selector, resource, or other
domain object about which the failure is true.

Origin and subject answer different questions:

~~~text
origin  → who recognized the failure?
subject → what is the failure about?
~~~

Do not overload a path, object identifier, or message with both meanings.

## 4. Identity and classification

### 4.1 Error identity

An error needs a stable semantic identity when callers branch on it, tests
assert it, or documentation promises it.

Prefer identities owned by the originating domain over detached global
taxonomies. A local name can be globally meaningful when interpreted together
with its origin.

### 4.2 Classification

A **classification** groups failures that imply similar handling across several
origins, such as absent, malformed, ambiguous, conflicting, unsupported,
unavailable, or internal.

Classification is secondary to semantic identity. Add it only when a consumer
can make a different useful decision from it.

Do not force all failures into a global category hierarchy merely to make them
look uniform.

## 5. Content

### 5.1 Message

The message explains the concrete condition in domain language. Structured
fields carry facts that callers must not recover by parsing prose.

Do not make wording the only representation of identity, subject, expected
values, candidates, or recovery actions when those facts have stable semantics.

### 5.2 Details

Occurrence-specific facts may include expected values, observed values,
candidate targets, dependency state, bounded conflicting identifiers, or
similar information needed to diagnose or recover.

Expose only facts that are safe and useful for the intended consumer.

### 5.3 Recovery

Return recovery information when the component that owns the violated invariant
can establish a valid next action.

Distinguish deterministic recovery from advice. A suggested action is not a
machine-applicable repair merely because it sounds plausible.

## 6. Propagation and causality

### 6.1 Propagation

When a failure crosses a meaningful component boundary, preserve its origin and
semantic identity. A caller may add operation context without relabeling itself
as the source of the subordinate failure.

Avoid message chains that encode propagation only through repeated wrapping.

### 6.2 Provenance

**Provenance** records meaningful operation boundaries crossed after origin.
Use it when understanding the execution route changes diagnosis or recovery.

Provenance is not a language traceback. Keep implementation stacks as a
separate debug projection unless the consumer specifically requires them.

### 6.3 Causality

When one failure causes another independently meaningful failure, represent the
causal relationship explicitly.

Do not manufacture a new error for every downstream operation that could not
run after one prerequisite already failed. A dependency or stop relation can
represent that condition without multiplying noise.

## 7. Accumulation

### 7.1 Independent failures

Collect independently knowable failures when continuing does not make later
findings untrustworthy or unsafe.

Validation, inspection, compilation, indexing, and other read-oriented
operations commonly support accumulation across independent subjects.

### 7.2 Hard stops

Stop when later findings would depend on invalid invented state, when a failed
precondition makes dependent evaluation meaningless, or when continuing a
mutation could create unsafe partial state.

A consumer must be able to distinguish an exhaustive result from one stopped
before all applicable evaluations completed.

### 7.3 Grouping and ordering

Choose grouping according to the questions the consumer must answer. Origin,
subject, classification, severity, or causal chain can each be a useful axis.

Keep ordering deterministic when callers compare repeated runs, review diffs, or
consume the output programmatically.

A formal architecture may select a default grouping and ordering rule for a
specific consumer.

## 8. Presentation and projection

Maintain one canonical set of failure facts and derive consumer-specific
representations from it when practical.

A projection may compress, reorder, or format information for its consumer. It
must not silently change the semantic identity, origin, causal relationships,
or completion state on which callers rely.

A CLI response, machine-readable serialization, editor annotation, operational
event, and retained report can therefore share facts without becoming
independently authored error models.

## 9. Persistence boundary

Immediate caller recovery and retained operational observation are separate
concerns.

Persist failure information when persistence serves a distinct purpose such as
cross-invocation correlation, operational monitoring, audit, recurrence
analysis, or historical evidence.

Do not require an immediate caller to consult a log for facts already available
when the failure occurred.

Persistence expands retention and exposure boundaries. Select it deliberately
and apply the privacy, lifecycle, and operational controls appropriate to the
retained information.

## 10. Formal architectures

Use an Error Management architecture when a recurring consumer and operating
constraint justify fixing several of these decisions together.

An error architecture should make explicit:

~~~text
primary consumer
canonical failure representation
origin and identity rule
propagation rule
accumulation and stopping rule
recovery rule
default presentation
persistence boundary
verification obligations
~~~

The architecture applies these concepts; it does not redefine them. Supporting
research and decision provenance may live with the architecture package without
becoming current architectural authority.
