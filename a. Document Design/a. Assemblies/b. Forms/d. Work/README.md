---
description: >-
  `Consult when` *repository work must be represented as a reusable Task or
  Plan document and the applicable Form or shared authoring preparation is not
  yet known* `to` **select the Task or Plan Form and establish informed,
  durable, harness-aware execution context without redefining Work Management
  lifecycle or planning semantics**.
---
# Work

Work Forms represent executable or coordinating repository work.

Task represents one independently executable acceptance boundary. Plan
represents coordinated work whose multiple acceptance boundaries, dependencies,
Gates, or resumability justify an explicit execution model.

Work Management owns lifecycle, identity, storage, execution, retention, and
Planning semantics. Task and Plan Forms own recurring document representation
and assembly.

## Shared authoring preparation

Before executable Steps are finalized, the author must:

1. identify the Work Management guidance that governs the intended work;
2. identify the domains and operations implied by the outcome and read their
   governing guidance according to each document's directive;
3. inventory the authoring harness capabilities relevant to discovering,
   representing, and validating the work, including material limitations;
4. inspect enough current repository state to trace the currently discoverable
   implementation, validation, handoff, and completion implications; and
5. revise the work representation when newly discovered guidance, repository
   state, or capabilities materially change what safe execution requires.

The initially discovered guidance and capability set is a minimum known set, not
a closed list. A newly encountered governed concern requires its applicable
guidance before the affected work is defined or performed.

Preparation required to construct a trustworthy Plan is not automatically
planned work. Reading guidance, inventorying authoring tools, inspecting current
state to derive decomposition, and checking the Plan's own representation are
plan-authoring work unless they independently contribute to the repository
outcome.

## Execution-environment check

The authoring agent and an executing agent may have different harnesses.
Therefore every Plan must retain an early execution instruction requiring the
current executor to inventory the capabilities and material limitations of its
own harness before entering the execution frontier.

The check should consider only materially relevant capabilities, including when
applicable:

- bounded reads, pagination, and end-of-file guarantees;
- search-result, context, and output limits;
- durable writable storage and repository checkout availability;
- shell or code execution, dependency availability, and timeouts;
- network and external-call availability;
- connector permissions and read versus mutation authority; and
- specialized artifact or domain tools.

A Task carries the same invariant in compressed form: before acting, confirm
that the current harness can safely perform and validate the Task, and surface
any material limitation that changes execution, blocking, handoff, or
acceptance.

Do not freeze the Plan author's tool list as execution truth. Retain specific
capability facts in a Task or Plan only when they materially constrain later
execution.

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
