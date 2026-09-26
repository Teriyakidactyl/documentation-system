---
uid: R2MVGF
description: >-
  `Consult when` *plan P001 for creating the Work Management root must be
  resumed or inspected* `to` **recover its outcome, completed decisions,
  current execution frontier, and remaining merge work**.
work:
  id: P001
  type: plan
  state: active
  updated: '2026-09-25'
---
# P001 — Create Work Management root

## Outcome

Add a root-level Work Management capability that lets a target repository
capture, plan, execute, hand off, close, and durably retain repository work
under a `.project/` sideband, including a lightweight one-off Task route and an
advanced Plan graph model.

## Acceptance conditions

- Root routing exposes Work Management as a peer capability.
- `.project/` is a reserved controlled sideband and is absent from `latest`.
- `.project/` uses the stable responsibility layer Intake, Planning, Execution,
  and Archive.
- A Task can be registered without a Plan.
- Plans support explicit Nodes, Relations, Gates, dependency sufficiency, and
  resumable state.
- Fault work integrates with Work Management while legacy `.fault/` evidence
  remains compatible.
- Planning retains Process Creator and both Externalized Cognition Methods
  references under Planning/Reference.
- Organizing recognizes `.project` as controlled and address-opaque.
- Repository verification passes.
- The change is merged to `main`.

## Work graph

### N001 — Establish Work Management semantic owner

State: closed

Result: Work Management owns repository-local work state and relations without
acquiring authority over the artifacts being changed.

### N002 — Validate root placement and responsibility structure

State: closed
Requires: N001

Result: Work Management is a root peer. Its guidance responsibilities are
Close-Out, Execution, Faults, Intake And Shaping, and Planning, plus root-level
model/storage/task entry documents.

### N003 — Specify Work Object and Plan models

State: closed
Requires: N001

Result: Work Objects have stable identity, typed state, explicit disposition,
relations, Gates, and retention. Plans progressively formalize from simple
checklists to explicit execution graphs.

### N004 — Specify `.project/` storage

State: closed
Requires: N002, N003

Result: `.project/` is controlled and address-opaque; its stable storage
responsibilities are Intake, Planning, Execution, and Archive. Close-Out is an
operation rather than a storage branch.

### N005 — Author Work Management guidance

State: closed
Requires: N001, N002, N003, N004

Result: Root guidance, intake, planning, execution, close-out, fault semantics,
storage, one-off task creation, and Plan model documents are authored.

### N006 — Retain planning references

State: closed
Requires: N005

Result: Process Creator and Externalized Cognition Methods v1/v2 are colocated
under Work Management Planning/Reference as non-authoritative planning support.

### N007 — Integrate Document Control and Organizing

State: closed
Requires: N004, N005

Gate: `.project` is documented as reserved, Organizing treats it as a controlled
sideband, and regression coverage proves artifacts are controlled but
unaddressed.

### N008 — Refresh and validate repository

State: closed
Requires: N007

Gate: repository-convergence and all verification jobs pass on the pull request.

### N009 — Review pull request

State: closed
Requires: N008

Gate: diff contains no unplanned authority transfer, stale generated
representation, or failing review thread.

### N010 — Merge

State: active
Requires: N009

Gate: pull request is mergeable and required checks are successful.

## Current state

The Work Management guidance root and planning references are committed on
`work-management-root`. Root routing, `.project` reservation, Organizing support, and sideband regression
coverage are committed. PR #61 passes Software Surface, Generated Contracts,
Capability Tests, Automation Tests, Architecture Conformance, and Repository
Convergence. The PR is mergeable with no structural validation failure.

## Next action

Merge PR #61. After merge, confirm the main-branch refresh completes and updates
derived UIDs/indexes as required.
