---
description: >-
  `Consult when` *plan P002 for refining Work Management project setup,
  Work ID allocation, Plan-local Tasks, and the Plan Document Form must be
  resumed or inspected* `to` **recover the agreed semantic boundaries,
  implementation tasks, current state, and next action without relying on
  prior conversation**.
work:
  id: P002
  type: plan
  state: active
  retention: active
  updated: '2026-09-25'
---
# P002 — Refine Work Management planning and project control

## Outcome

Refine Work Management so repositories have an explicit setup path,
collision-resistant standalone Work IDs, single-file Plans with Plan-local
Tasks, and a canonical Plan Document Form that owns Markdown authoring
conventions separately from Work Management semantics.

## Acceptance conditions

- Work Management provides an explicit project-setup procedure for the complete
  `.project/` skeleton.
- `.project/metrics.json` records repo-automation operational state for
  standalone Work ID allocation.
- Standalone Work IDs are programmatically allocated, monotonic, archive-aware,
  and globally unique across `.project/`.
- Repo automation owns Work Management setup, ID allocation, metrics
  reconciliation, UID maintenance, and Work Management validation.
- Work Management distinguishes standalone Tasks from Plan-local Tasks and
  Steps.
- Plan-local Tasks remain inside the Plan file and do not consume repository-wide
  `T###` IDs.
- Plan Tasks may contain Steps, and every Step is represented by a Markdown
  checkbox.
- Work Management owns Plan/Task/Step semantics and storage.
- Document Design Assemblies owns the Plan Markdown representation through a
  Plan Document Form.
- Plan Task source uses a heading outside the state callout, a state callout
  immediately beneath it, checkbox-backed Steps, and `---` between Tasks.
- Completed Plan Tasks are unquoted and struck through.
- Existing guidance and P001 are reconciled with the new model.
- Repository validation and publication checks pass before merge.

## Constraints

- `.project/` remains mutable repository-local Work Management state and stays
  absent from the published `latest` projection.
- File placement is not lifecycle truth.
- Standalone Work IDs are permanent and never recycled.
- Archived Work Objects retain their IDs and occupy the global namespace.
- Plan-local IDs are scoped to their Plan.
- `metrics.json` is operational/control state, not semantic authority for
  actual Work Objects.
- Ordinary Plan Tasks must not cause one-file-per-task proliferation.

## Decisions

Work Management owns semantic concepts, lifecycle, storage, Work IDs, and the
promotion boundary from Plan-local Task to standalone Work Object. The Plan
Document Form owns Markdown source arrangement and visual conventions.

A standalone Task is a Work Object with a repository-global `T###` ID. A
Plan-local Task exists only inside its Plan, uses a local ID such as `T1`,
and is externally qualified as `P002:T1` only when needed.

A Plan-local Task owns one acceptance boundary. Its Steps are execution actions
inside that boundary. Step completion is represented by Markdown checkbox state.

---

## Tasks

### ~~T1 — Reconcile Work Management semantics~~

~~State: Completed~~

~~**Acceptance**~~

- ~~Work Model and Plan Model distinguish standalone Tasks, Plan-local Tasks,
  and Steps.~~
- ~~Plan-local Tasks do not consume global Task IDs or require external files.~~
- ~~Promotion to standalone Work Object is explicit.~~

~~**Steps**~~

- [x] ~~Revise Work Model Task and Plan definitions.~~
- [x] ~~Revise Plan Model around Plan-local Tasks and checkbox-backed Steps.~~
- [x] ~~Remove ordinary multi-file Plan Task guidance.~~
- [x] ~~Define the promotion boundary to standalone Tasks.~~
- [x] ~~Route Plan representation to the Plan Document Form.~~

---

### ~~T2 — Create the Plan Document Form~~

~~State: Completed~~

~~**Acceptance**~~

- ~~A canonical Plan Form package exists under Document Design Assemblies.~~
- ~~The Form owns Plan source arrangement and Task/Step conventions.~~

~~**Steps**~~

- [x] ~~Create the Form package README.~~
- [x] ~~Write the Plan Form reference.~~
- [x] ~~Write Author A Plan.~~
- [x] ~~Encode headings, state callouts, checkboxes, separators, and completed
  strike-through representation.~~

---

### ~~T3 — Add explicit Work Management project setup~~

~~State: Completed~~

~~**Acceptance**~~

- ~~One Work Management procedure initializes the complete project skeleton and
  `metrics.json`.~~

~~**Steps**~~

- [x] ~~Add Set Up Work Management.~~
- [x] ~~Define the full active and Archive skeleton.~~
- [x] ~~Define `.gitkeep` treatment for empty folders.~~
- [x] ~~Define adoption when Work Objects already exist.~~

---

### T4 — Implement repo-automation Work Management operations

> [!IMPORTANT] State: Active
>
> **Acceptance**
> - Repo automation can initialize Work Management, reconcile and validate
>   allocator state, and register standalone Tasks without collisions.
>
> **Steps**
> - [x] Add a Work Management automation module.
> - [x] Define kind-to-prefix mapping and `metrics.json` schema.
> - [x] Scan active and archived Work Objects for IDs.
> - [x] Detect duplicates.
> - [x] Allocate monotonic Task IDs without recycling.
> - [x] Reconcile counters against actual Work Objects.
> - [x] Expose setup, reconcile, validate, and register-task operations.
> - [x] Reuse repository UID minting mechanics for project artifacts.
> - [ ] Run repository verification against the new operation surface.

---

### ~~T5 — Update standalone Task creation~~

~~State: Completed~~

~~**Acceptance**~~

- ~~Record A Task delegates global ID allocation to repo automation and excludes
  Plan-local Tasks from the allocator.~~

~~**Steps**~~

- [x] ~~Replace manual next-ID scanning guidance.~~
- [x] ~~Clarify standalone Task scope.~~
- [x] ~~Require checkbox-backed Steps when standalone Tasks contain Steps.~~
- [x] ~~Remove obsolete user-facing Organizing runtime wording.~~

---

### T6 — Add validation and regression coverage

> [!NOTE] State: Ready
>
> **Acceptance**
> - Automated tests cover setup, allocation, collisions, metrics reconciliation,
>   UID maintenance, and interface exposure.
>
> **Steps**
> - [x] Add duplicate-ID coverage.
> - [x] Add stale-metrics reconciliation coverage.
> - [x] Add monotonic Task registration coverage.
> - [x] Add setup and UID-minting coverage.
> - [x] Add public operation/CLI discovery coverage.
> - [ ] Execute the full CI verification surface.

---

### ~~T7 — Migrate repository examples and current project state~~

~~State: Completed~~

~~**Acceptance**~~

- ~~Current `.project/` state demonstrates the new setup and Plan conventions.~~

~~**Steps**~~

- [x] ~~Add `.project/metrics.json`.~~
- [x] ~~Update `.project/README.md`.~~
- [x] ~~Reformat P001 using the Plan Form conventions.~~
- [x] ~~Keep this P002 Plan current.~~

---

### T8 — Validate and merge

> [!NOTE] State: Ready
>
> **Acceptance**
> - All repository checks pass and the change is merged with publication
>   behavior intact.
>
> **Steps**
> - [ ] Run capability and automation tests.
> - [ ] Run architecture and generated-contract checks.
> - [ ] Run repository convergence/idempotence.
> - [ ] Verify `.project/` remains excluded from `latest`.
> - [ ] Open and review the PR.
> - [ ] Resolve CI faults.
> - [ ] Merge after all required checks pass.
> - [ ] Verify post-merge main and publication.

---

## Current state

The semantic model, Plan Form, setup guidance, project metrics, Work Management
automation operations, CLI projection, and dedicated tests are implemented on
`work-management-refinement`. Per-commit reconciliation and full repository
verification remain.

## Next action

Wire Work Management reconciliation into repository convergence, then open the
pull request and use CI to complete T4, T6, and T8.
