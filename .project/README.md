---
uid: 2Q1HKP
description: >-
  `Consult when` *the Documentation System's current repository-local work
  state must be resumed or inspected* `to` **locate Plans, standalone Work
  Objects, and allocator state without treating them as current Documentation
  System authority**.
---
# Project Work

This controlled sideband holds mutable Work Management state for this repository.

Repository automation maintains the complete project skeleton and
`metrics.json`. The metrics file records monotonic next-ID counters for
standalone Work Objects; the Work Objects themselves remain semantic truth.

```text
.project/
├── README.md
├── metrics.json
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

The stable responsibility layer is Intake, Planning, Execution, and Archive.
Object-kind folders organize retrieval; they do not encode lifecycle state.

Plans normally keep Plan-local Tasks and checkbox-backed Steps in one Plan file.
Only standalone Work Objects consume repository-global Work IDs.

Empty directories are retained in Git with `.gitkeep` anchors. Those anchors
carry no Work Management semantics.

Current technical and documentation authority remains outside this sideband.
