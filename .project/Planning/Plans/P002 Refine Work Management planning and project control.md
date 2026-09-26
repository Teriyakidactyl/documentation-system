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
- Plan-local Tasks remain in the Plan file and do not consume repository-wide
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
An item needing independent handoff, blocking, cancellation, review, or
acceptance should normally be promoted to a Plan Task or standalone Task.

The Plan Form convention is:

- Task heading outside the callout;
- `[!NOTE] State: Ready` for ready Tasks;
- `[!IMPORTANT] State: Active` for active Tasks;
- a state-appropriate callout for blocked/review Tasks;
- completed Tasks are not callouts or quotes and are struck through;
- Steps use `- [ ]` or `- [x]`;
- `---` separates every Task block.

---

## Tasks

### T1 — Reconcile Work Management semantics

> [!IMPORTANT] State: Active
>
> **Acceptance**
> - Work Model and Plan Model distinguish standalone Tasks, Plan-local Tasks,
>   and Steps.
> - Plan-local Tasks do not consume global Task IDs or require external files.
> - Promotion to standalone Work Object is explicit.
>
> **Steps**
> - [ ] Revise Work Model Task and Plan definitions.
> - [ ] Revise Plan Model around Plan-local Tasks and checkbox-backed Steps.
> - [ ] Remove ordinary multi-file Plan Task guidance.
> - [ ] Define the promotion boundary to standalone Tasks.
> - [ ] Route Plan authoring representation to the Plan Document Form.

---

### T2 — Create the Plan Document Form

> [!NOTE] State: Ready
>
> **Acceptance**
> - A canonical Plan Form package exists under Document Design Assemblies.
> - The Form owns Plan source arrangement and the agreed Task/Step conventions.
>
> **Steps**
> - [ ] Create the Form package README.
> - [ ] Write the Plan Form reference.
> - [ ] Write Author A Plan.
> - [ ] Route the package from Forms.
> - [ ] Encode headings, state callouts, checkboxes, separators, and completed
>       strike-through representation.

---

### T3 — Add explicit Work Management project setup

> [!NOTE] State: Ready
>
> **Acceptance**
> - One Work Management procedure initializes the complete project skeleton and
>   `metrics.json`.
>
> **Steps**
> - [ ] Add Set Up Work Management.
> - [ ] Define the full active and Archive skeleton.
> - [ ] Define `.gitkeep` treatment for empty folders.
> - [ ] Define adoption when Work Objects already exist.
> - [ ] Route setup from Work Management README.

---

### T4 — Implement repo-automation Work Management operations

> [!NOTE] State: Ready
>
> **Acceptance**
> - Repo automation can initialize Work Management and register standalone Work
>   IDs without collisions.
>
> **Steps**
> - [ ] Add a Work Management automation module.
> - [ ] Define kind-to-prefix mapping and `metrics.json` schema.
> - [ ] Scan active and archived Work Objects for IDs.
> - [ ] Detect duplicates.
> - [ ] Allocate monotonic IDs without recycling.
> - [ ] Reconcile counters against actual Work Objects.
> - [ ] Expose setup/register operations through the repo-manager interface.
> - [ ] Reuse repo automation UID minting/validation behavior.

---

### T5 — Update standalone Task creation

> [!NOTE] State: Ready
>
> **Acceptance**
> - Record A Task delegates global ID allocation to repo automation and clearly
>   excludes Plan-local Tasks from the allocator.
>
> **Steps**
> - [ ] Replace manual next-ID scanning guidance.
> - [ ] Clarify standalone Task scope.
> - [ ] Require checkbox-backed Steps when standalone Tasks contain Steps.
> - [ ] Remove obsolete Organizing runtime wording.

---

### T6 — Add validation and regression coverage

> [!NOTE] State: Ready
>
> **Acceptance**
> - Automated tests cover setup, allocation, collisions, metrics reconciliation,
>   UID maintenance, and interface exposure.
>
> **Steps**
> - [ ] Test duplicate IDs across active stores.
> - [ ] Test duplicate IDs across active and Archive.
> - [ ] Test stale metrics reconciliation.
> - [ ] Test monotonic allocation with gaps and archival.
> - [ ] Test empty and pre-populated project setup.
> - [ ] Test repo-manager public operation/CLI surface.
> - [ ] Test Plan Form representation where supported.

---

### T7 — Migrate repository examples and current project state

> [!NOTE] State: Ready
>
> **Acceptance**
> - Current `.project/` state demonstrates the new setup and Plan conventions.
>
> **Steps**
> - [ ] Add `.project/metrics.json`.
> - [ ] Update `.project/README.md`.
> - [ ] Reformat P001 using the Plan Form conventions without changing its
>       historical outcome.
> - [ ] Keep this P002 Plan current as implementation advances.

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

Implementation has begun on branch `work-management-refinement`. The semantic
and Plan Form boundary is the active work.

## Next action

Complete T1 and T2 before changing repo automation so the software implements a
stable semantic and representation contract.
