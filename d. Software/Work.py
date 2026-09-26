#!/usr/bin/env python3
r'''---
uid: XZ09JW
description: >-
  `Read in full and follow when` *repository-local Work Management state must
  be initialized, reconciled, validated, or given a new standalone Task*
  `to` **use Repo Manager's Work Management automation for the `.project/`
  skeleton, allocator metrics, controlled UID maintenance, and collision-safe
  Task registration**.
quadrant: HowTo
outline:
  topology: branching
  axis: operation
writing-style:
  formality: professional
  tone: neutral/detached
  mode: imperative
  density: moderate
  abstraction: concrete/specific
  redundancy: zero
  signposting: light
  register: technical
---
# 🛠️ Work

Use Work for repository-local `.project/` control operations.

## 1. Initialize Work Management

```text
python3 "d. Software/Work.py" setup [repository_root]
```

Setup materializes the canonical project skeleton, reconciles
`.project/metrics.json`, and mints missing controlled UIDs for metadata-bearing
project artifacts.

## 2. Reconcile allocator state

```text
python3 "d. Software/Work.py" reconcile [repository_root]
```

Reconcile preserves monotonic counters while raising any stale counter to one
greater than the highest active or archived Work ID of that kind.

## 3. Validate project state

```text
python3 "d. Software/Work.py" validate [repository_root]
```

Validation rejects duplicate or malformed standalone Work IDs, an incomplete
project skeleton, or allocator counters behind actual Work Objects.

## 4. Register a standalone Task

```text
python3 "d. Software/Work.py" register-task "Concise task title" [repository_root]
```

Registration allocates the next collision-free `T###`, creates a captured Task
record, advances metrics, and mints its controlled UID when applicable.

Plan-local Tasks do not use this allocator.
'''

from repo_manager.interfaces.cli.work_management import main

if __name__ == "__main__":
    main()
