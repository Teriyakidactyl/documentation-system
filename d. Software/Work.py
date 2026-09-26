#!/usr/bin/env python3
r'''---
uid: XZ09JW
description: >-
  `Read in full and follow when` *repository-local Work Management state must
  be initialized, reconciled, validated, or given a new standalone Task or Plan*
  `to` **use Repo Manager's Work Management automation for the current
  `.project/` skeleton, allocator metrics, UID maintenance, and collision-safe
  work registration**.
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

Setup materializes the current Planning, Execution, and Archive skeleton,
migrates allocator metrics to the current schema, and mints missing controlled
UIDs for metadata-bearing project artifacts.

## 2. Reconcile allocator state

```text
python3 "d. Software/Work.py" reconcile [repository_root]
```

Reconcile preserves monotonic active counters while raising stale counters above
allocated Work IDs. Legacy Idea, Feedback, Issue, and Fault Work Objects remain
readable for migration/history but do not receive active allocator counters.

## 3. Validate project state

```text
python3 "d. Software/Work.py" validate [repository_root]
```

Validation rejects duplicate or malformed standalone Work IDs, an incomplete
current project skeleton, or active allocator counters behind actual Work
Objects.

## 4. Register a standalone Task

```text
python3 "d. Software/Work.py" register-task "Concise task title" [repository_root]
```

Registration allocates the next collision-free `T###`, creates a captured Task,
advances metrics, and mints its controlled UID when applicable.

## 5. Register a Plan

```text
python3 "d. Software/Work.py" register-plan "Concise plan title" [repository_root]
```

Registration allocates the next collision-free `P###` and immediately creates
durable captured Plan state before decomposition is relied on. Apply Planning
guidance and the Plan Form after registration.

Plan-local Tasks do not use either standalone allocator.
'''

from repo_manager.interfaces.cli.work_management import main

if __name__ == "__main__":
    main()
