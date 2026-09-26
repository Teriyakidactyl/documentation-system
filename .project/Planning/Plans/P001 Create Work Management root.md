---
uid: R2MVGF
description: >-
  `Consult when` *plan P001 for creating the Work Management root must be
  inspected* `to` **recover its completed outcome and retained implementation
  evidence without treating the historical Plan as current product authority**.
work:
  id: P001
  type: plan
  state: closed
  disposition: completed
  retention: active
  updated: '2026-09-25'
---
# P001 — Create Work Management root

## Outcome

Add a root-level Work Management capability that lets a target repository
capture, plan, execute, hand off, close, and durably retain repository work
under a `.project/` sideband.

## Acceptance conditions

- Root routing exposes Work Management as a peer capability.
- `.project/` is a reserved controlled sideband and is absent from `latest`.
- Intake, Planning, Execution, and Archive are stable storage responsibilities.
- A standalone Task can be registered without a Plan.
- Plans support resumable coordinated work.
- Fault work integrates with Work Management while legacy `.fault/` evidence
  remains compatible.
- Planning references are retained under Planning/Reference.
- Repository verification passes and the change is merged.

## Tasks

### ~~T1 — Establish Work Management semantic ownership~~

~~State: Completed~~

~~**Acceptance**~~

- ~~Work Management owns repository-local work state without acquiring authority
  over the artifacts being changed.~~

~~**Steps**~~

- [x] ~~Define the semantic boundary.~~
- [x] ~~Separate work state from product authority.~~

---

### ~~T2 — Establish root placement and responsibility structure~~

~~State: Completed~~

~~**Acceptance**~~

- ~~Work Management is a root peer with stable Intake, Planning, Execution, and
  Archive storage responsibilities.~~

~~**Steps**~~

- [x] ~~Validate root placement.~~
- [x] ~~Define responsibility branches.~~

---

### ~~T3 — Specify Work Object and Plan models~~

~~State: Completed~~

~~**Acceptance**~~

- ~~Work Objects have stable identity, typed state, disposition, relations,
  Gates, and retention.~~

~~**Steps**~~

- [x] ~~Define Work Object semantics.~~
- [x] ~~Define the initial Plan graph model.~~

---

### ~~T4 — Specify `.project/` storage~~

~~State: Completed~~

~~**Acceptance**~~

- ~~The sideband is controlled, address-opaque, and excluded from publication.~~

~~**Steps**~~

- [x] ~~Define the storage root.~~
- [x] ~~Separate Close-Out from storage topology.~~

---

### ~~T5 — Author Work Management guidance~~

~~State: Completed~~

~~**Acceptance**~~

- ~~Root, intake, planning, execution, close-out, fault, storage, and Task
  guidance are present.~~

~~**Steps**~~

- [x] ~~Author the guidance set.~~
- [x] ~~Connect root routing.~~

---

### ~~T6 — Retain planning references~~

~~State: Completed~~

~~**Acceptance**~~

- ~~Process Creator and Externalized Cognition references remain available as
  non-authoritative planning support.~~

~~**Steps**~~

- [x] ~~Retain the three planning sources.~~

---

### ~~T7 — Integrate controlled sideband behavior~~

~~State: Completed~~

~~**Acceptance**~~

- ~~`.project/` artifacts are controlled but unaddressed.~~

~~**Steps**~~

- [x] ~~Recognize the sideband.~~
- [x] ~~Add regression coverage.~~

---

### ~~T8 — Refresh and validate repository~~

~~State: Completed~~

~~**Acceptance**~~

- ~~Repository convergence and all verification jobs pass.~~

~~**Steps**~~

- [x] ~~Run the verification suite.~~
- [x] ~~Resolve the reference-index convergence fault.~~

---

### ~~T9 — Review pull request~~

~~State: Completed~~

~~**Acceptance**~~

- ~~The change contains no unplanned authority transfer or failing review
  condition.~~

~~**Steps**~~

- [x] ~~Review the final diff and CI state.~~

---

### ~~T10 — Merge~~

~~State: Completed~~

~~**Acceptance**~~

- ~~PR #61 is merged and post-merge verification passes.~~

~~**Steps**~~

- [x] ~~Merge the pull request.~~
- [x] ~~Verify main and publication.~~

---

## Current state

PR #61 is merged. The Plan remains in active retention as historical Work
Management evidence.

## Next action

None. This Plan is closed with disposition `completed`.
