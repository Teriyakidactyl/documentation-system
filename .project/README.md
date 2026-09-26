---
uid: 2Q1HKP
description: >-
  `Consult when` *the Documentation System's current repository-local work
  state must be resumed or inspected* `to` **locate the active Plan and
  Work Objects without treating them as current Documentation System
  authority**.
---
# Project Work

This controlled sideband holds mutable Work Management state for this repository.

This repository materializes the complete recognized Work Management folder
skeleton so humans and agents always have predictable destinations even before a
particular Work Object kind is present.

```text
.project/
├── README.md
├── Intake/
│   ├── Ideas/
│   ├── Feedback/
│   ├── Issues/
│   └── Faults/
├── Planning/
│   ├── Plans/
│   ├── Investigations/
│   └── Decisions/
├── Execution/
│   ├── Tasks/
│   └── Handoffs/
└── Archive/
    ├── Intake/
    │   ├── Ideas/
    │   ├── Feedback/
    │   ├── Issues/
    │   └── Faults/
    ├── Planning/
    │   ├── Plans/
    │   ├── Investigations/
    │   └── Decisions/
    └── Execution/
        ├── Tasks/
        └── Handoffs/
```

The active responsibility layer remains `Intake/`, `Planning/`,
`Execution/`, and `Archive/`. Object-kind folders organize retrieval; they
do not encode lifecycle state.

Archive mirrors the active responsibility/object-kind structure so cold Work
Objects retain an obvious type-preserving destination after Close-Out.

Empty directories are retained in Git with `.gitkeep` anchors. Those anchors
carry no Work Object semantics.

Current technical and documentation authority remains outside this sideband.
