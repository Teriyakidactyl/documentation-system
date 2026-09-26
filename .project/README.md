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

Repository automation maintains the current project skeleton and
`metrics.json`. The metrics file records monotonic next-ID counters for active
standalone Work Object kinds; Work Objects themselves remain semantic truth.

```text
.project/
├── README.md
├── metrics.json
├── Planning/
│   ├── Plans/
│   ├── Investigations/
│   └── Decisions/
├── Execution/
│   ├── Tasks/
│   └── Handoffs/
└── Archive/
    ├── Planning/
    │   ├── Plans/
    │   ├── Investigations/
    │   └── Decisions/
    └── Execution/
        ├── Tasks/
        └── Handoffs/
```

Retained Records such as Feedback, Issue, Fault Record, and Research are not
Work Objects merely because work can derive from them.

Legacy repositories may still contain historical `.project/Intake/` Work
Objects. Current setup does not create that branch, and current allocator state
does not allocate Idea, Feedback, Issue, or Fault IDs.

Plans normally keep Plan-local Tasks and checkbox-backed Steps in one durable
Plan file. Standalone Plans and Tasks receive repository-global IDs through Work
automation.

Empty current leaves may use `.gitkeep` anchors. Current technical and
documentation authority remains outside this sideband.
