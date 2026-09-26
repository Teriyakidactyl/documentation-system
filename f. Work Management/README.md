---
uid: S4QDC1
description: >-
  `Consult when` *repository-local work must be captured, stored, planned,
  executed, resumed, reviewed, or closed and the applicable Work Management
  guidance is not yet known* `to` **route to the narrowest Work Management
  procedure or reference without confusing work state with the authority of the
  artifact being changed**.
---
# Work Management

Work Management governs repository-local working information: how work enters
the repository, becomes actionable, is coordinated, survives agent handoff, and
leaves active attention with a durable disposition.

Work Management owns work state and work relationships. It does not acquire the
semantic authority of the code, documentation, architecture, decision record,
research result, or other artifact that the work concerns.

## Scope

Use this location for repository work represented beneath the target
repository's `.project/` sideband. A Task may exist without a Plan. A Plan
coordinates work when decomposition, dependencies, gates, ordering, validation,
or multi-session continuity justify that structure.

## Index
<!--
element:
  path:
    uid: BZJASV
    filepath: a. Document Design/a. Assemblies/a. Elements/a. Index/README.md
  version: '2.0'
  renderer:
    uid: 45E225
    filepath: d. Software/Navigation Crawler.py
-->

### 💡 Work Management

`Read in full when` *repository-local work state is being treated as product authority, process history, or filesystem position* `to` **understand the ownership and graph principles that keep intake, planning, execution, handoff, close-out, and retention coherent without transferring authority from the artifacts being changed**.

<a href="1.%20%F0%9F%92%A1%20Work%20Management.md" uid="V1PBTD" data-ds-link="relative-path">../1. 💡 Work Management.md</a>

### Close-Out

`Consult when` *tracked work should stop competing for active attention or move into retained cold state* `to` **select the close-out guidance that records why work ended and determines its retention treatment independently of its prior active location**.

<a href="a.%20Close-Out/README.md" uid="BDEF9N" data-ds-link="relative-path">../a. Close-Out/README.md</a>

- `1. 🛠️ Close Work.md`

### 📖 Project Storage

`Consult when` *repository-local Work Management information needs a durable filesystem location, retrieval rule, lifecycle transition, or archival treatment* `to` **place and retain work beneath the controlled `.project/` sideband using its Intake, Planning, Execution, and Archive responsibilities without making path location the sole source of work state**.

<a href="2.%20%F0%9F%93%96%20Project%20Storage.md" uid="11J42Y" data-ds-link="relative-path">../2. 📖 Project Storage.md</a>

### Execution

`Consult when` *tracked work is ready to be acted on, resumed, blocked, reviewed, or transferred between agents* `to` **select the execution or handoff guidance that preserves actionable state and continuation context**.

<a href="b.%20Execution/README.md" uid="A4WPXZ" data-ds-link="relative-path">../b. Execution/README.md</a>

- `1. 🛠️ Execute And Hand Off Work.md`

### 📖 Work Model

`Consult when` *a Work Object, identifier, state, disposition, relation, gate, maturity, or retention fact must be interpreted or authored consistently* `to` **confirm the canonical semantics that determine repository work state without forcing all work kinds into one lifecycle**.

<a href="3.%20%F0%9F%93%96%20Work%20Model.md" uid="2QZ9BC" data-ds-link="relative-path">../3. 📖 Work Model.md</a>

### Faults

`Consult when` *an observed repository failure may require retained evidence, causal analysis, remediation work, or recurrence control* `to` **select the fault semantics or management procedure while preserving the distinction between fault evidence, work state, and current technical authority**.

<a href="c.%20Faults/README.md" uid="1P4MHA" data-ds-link="relative-path">../c. Faults/README.md</a>

- `1. 📖 Fault.md`
- `2. 🛠️ Manage A Fault.md`

### 🛠️ Record A Task

`Read in full and follow when` *one repository action should be durably registered without first creating a project or plan* `to` **create a minimally sufficient Task with stable identity, actionable state, acceptance conditions, and next action in the repository's `.project/Execution/Tasks/` store**.

<a href="4.%20%F0%9F%9B%A0%EF%B8%8F%20Record%20A%20Task.md" uid="D9Z403" data-ds-link="relative-path">../4. 🛠️ Record A Task.md</a>

### Intake And Shaping

`Consult when` *a repository signal has entered Work Management but has not yet been given its appropriate work disposition* `to` **select the shaping procedure that determines whether the signal becomes tracked work, investigation, planning input, deferred material, or no work**.

<a href="d.%20Intake%20And%20Shaping/README.md" uid="7PB1HN" data-ds-link="relative-path">../d. Intake And Shaping/README.md</a>

- `1. 🛠️ Shape Work.md`

### Planning

`Consult when` *repository work needs decomposition, ordering, dependency reasoning, gates, optimization, or a durable resumable plan* `to` **select the planning procedure, plan-model reference, or advanced planning reference appropriate to the work's complexity**.

<a href="e.%20Planning/README.md" uid="Z8WFHG" data-ds-link="relative-path">../e. Planning/README.md</a>

- `1. 📖 Plan Model.md`
- `a. Reference/README.md`
- `2. 🛠️ Plan Work.md`
