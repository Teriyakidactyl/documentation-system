---
description: >-
  `Consult when` *an agent is the primary consumer of a command boundary and
  failures must support immediate diagnosis and recovery* `to` **apply the
  canonical agent-facing error architecture: source-addressable origin,
  preserved provenance, safe accumulation, origin-first grouping, structured
  recovery, and high-information default responses without dependency on
  hidden logs**.
quadrant: Reference
outline:
  topology: tree
  axis: agent-facing error architecture concern
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

# 📖 Agent-Facing Error Architecture

This architecture applies Error Management concepts when an agent is the
primary consumer of a command response.

The normal command response is the primary recovery surface. The architecture
therefore favors structured, source-addressable, high-information failures over
terse messages that require a second diagnostic call or hidden log inspection.

This architecture is selected by the consumer constraint. It is not a claim
that every error consumer is an agent. Another architecture may be selected
when another consumer imposes materially different requirements.

## 1. Canonical failure record

Represent each semantic failure with the following conceptual fields:

~~~yaml
origin:
  module: documentation_system.frontmatter
  file: 4 Tooling/_frontmatter/parser.py
  symbol: validate
name: REQUIRED_FIELD_MISSING
classification: malformed
subject:
  path: docs/example.md
  field: uid
message: Required field 'uid' is absent.
details: {}
recovery: {}
provenance:
  - documentation_system.document.inspect
  - documentation_system.registry.rebuild
  - documentation_system.organizing.refresh
~~~

A concrete language may use classes, tagged unions, records, or another typed
representation. Preserve the semantics even when the implementation form
changes.

## 2. Source-addressable origin

The component that first recognizes a semantic failure establishes its origin.
Preserve that origin unchanged through every caller.

Use implementation vocabulary that leads directly to the owning code:

~~~yaml
origin:
  module: documentation_system.markdown
  file: 4 Tooling/4 🛠️ Markdown.py
  symbol: Markdown.resolve_section
~~~

Module or owning namespace supplies stable source ownership. Repository-relative
file path supplies direct navigation. Symbol or operation narrows the origin to
the meaningful recognition boundary.

A line number may be included as transient navigation metadata but is not part
of durable identity.

A caller may append provenance or contextual information. It must not replace
the subordinate origin with itself.

## 3. Local error identity

Name errors locally inside the originating implementation instead of creating a
detached global error catalogue.

~~~text
documentation_system.markdown.resolve_section::SECTION_NOT_FOUND
documentation_system.yaml.parse::MALFORMED
documentation_system.frontmatter.parse::MALFORMED
~~~

The local name need not be globally unique. Full identity is origin plus local
name.

Classification remains available as a secondary cross-origin dimension when it
helps a caller branch. Do not substitute a broad classification for the local
semantic identity.

## 4. Subject and details

Keep the affected subject separate from source origin.

~~~yaml
subject:
  path: docs/example.md
  line: 42
  selector: "3.2"
~~~

Return occurrence-specific details when they change the agent's next decision,
including expected values, observed values, bounded candidate sets, or
dependency state.

Do not expose arbitrary locals, complete process state, credentials, or
unbounded implementation dumps merely because they exist at the failure site.

## 5. Propagation

### 5.1 Provenance

Append meaningful operation boundaries as the failure propagates:

~~~yaml
provenance:
  - document.inspect
  - registry.rebuild
  - organizing.refresh
~~~

Origin answers where the failure was produced. Provenance answers how it
reached the current command response.

Do not mirror the language stack. The default provenance contains domain
operations useful to diagnosis.

### 5.2 Context enrichment

A parent may add context that it legitimately owns, such as the corpus root,
requested top-level action, or batch identity.

Do not repeatedly wrap the message:

~~~text
Refresh failed: Registry failed: Document failed: Frontmatter failed: UID missing
~~~

Keep the originating message and route separate.

### 5.3 Unexpected exceptions

Convert an unexpected implementation exception once, at the first meaningful
repository-owned boundary capable of naming the failed operation.

Preserve the conversion boundary, exception type, safe exception message, and
known subject context. Classify the condition as internal or equivalent without
pretending the boundary semantically understood the underlying defect.

Reserve full tracebacks and stack locals for an explicit debug projection.

## 6. Accumulation

Return the maximum set of independently knowable failures that can be discovered
safely in one invocation.

A parent routine collects subordinate failure records rather than translating
them into one parent-owned generic error. The parent may additionally originate
its own error when a distinct parent-owned invariant fails.

This reduces repeated fix-run cycles for agent consumers.

### 6.1 Hard stops

Stop when continuing would make later findings untrustworthy or mutation unsafe.

Return all valid findings already discovered and state whether discovery was
complete:

~~~yaml
status: failure
completion: partial
stopped_at: write.apply
~~~

Use `complete` only when every applicable evaluation that could safely run did
run.

### 6.2 Cascades

Do not generate one synthetic error for every dependent operation skipped after
a prerequisite failed.

Represent a causal or blocked-by relationship when the downstream condition is
important to the caller. Emit another error only when it represents an
independently meaningful failure.

## 7. Origin-first response topology

Group the default agent-facing response first by source-addressable origin.

~~~text
command result
└── origin
    └── failure records
        ├── local name
        ├── classification
        ├── subject
        ├── message
        ├── details
        └── recovery
~~~

A presentation may organize records inside an origin group by local name,
classification, severity, subject, or another domain-relevant dimension.

Do not make a cross-origin classification the default top-level grouping.
Source ownership is the first navigation question when an agent must diagnose
or repair a command implementation or its inputs.

If two invocations of the same origin carry materially different provenance,
retain occurrence-level provenance or introduce an invocation grouping rather
than discarding execution topology.

## 8. Deterministic recovery

Return a structured recovery action when the originating domain can prove a
valid next step.

~~~yaml
recovery:
  action: select_section
  candidates:
    - "3.1"
    - "3.3"
~~~

Do not encode uncertain advice as a machine-applicable action.

When the domain already computed valid alternatives, return them in the failure
rather than requiring the agent to issue another command to rediscover them.

## 9. Default command response

The default response is intentionally information-rich.

Do not require the agent to:

~~~text
parse prose to recover stable identity
inspect a logfile for known failure facts
request a separate "last error" operation
infer the subordinate source of a parent failure
recompute alternatives already known by the command
~~~

Prefer enough structured information to distinguish whether the next action is
to correct input, acquire a prerequisite, choose another target, retry, stop, or
escalate.

High-information does not mean implementation dump. Include domain evidence that
changes the next decision; leave unrelated internal state out.

## 10. Canonical result and projections

Maintain one canonical failure result and derive presentations from it.

~~~text
canonical failure result
├── agent-facing CLI
├── human-facing CLI
├── machine-readable serialization
├── editor or GitHub annotation
└── telemetry projection when separately selected
~~~

A projection may compress or reorder facts for its consumer. It must preserve
error identity, origin, provenance, causal relationships, and completion
semantics on which that consumer depends.

## 11. Persistence boundary

Logs and telemetry solve a different problem from immediate agent recovery.

Use persistence for cross-invocation correlation, operational monitoring, audit,
recurrence analysis, or another explicit retained-evidence requirement.

Do not make a logfile the ordinary continuation of a failed command when the
command already knows the facts required for recovery.

## 12. Verification contract

Test this architecture at the boundary the agent actually consumes.

Verification should establish, where applicable, that:

- originating module, file, symbol, and local name survive propagation;
- parent operations append provenance without replacing origin;
- independently knowable subordinate failures arrive in one invocation;
- hard stops expose partial completion without invented downstream findings;
- origin groups and records are deterministically ordered;
- structured details expose facts needed for the intended next decision;
- deterministic recovery appears only when the domain can prove it;
- known recovery facts do not require a logfile or second diagnostic command;
- unexpected exceptions identify the repository-owned conversion boundary; and
- all projections preserve canonical identity and completion semantics.

General test design belongs to Testing. These assertions are the behavioral
contract this architecture requires Testing to prove.
