# Process Interrogator

**Version:** 2.0
**Supersedes:** Constraint Compiler / Process Creator v1.x
**Core change from v1.x:** Stop points are no longer a separate compilation pass. They are embedded in the dependency question itself via Q1b.

---

## 1. Purpose

The Process Interrogator converts:

- **User Need** (the Lock — reader constraints)
- **Document Shape** (the Key — artifact constraints)
- **Generators and Validators** (derived forces, facet-aligned per PMEST)

into:

> **A self-gating execution graph — a DAG with embedded cycles, validation barriers, and acceptance thresholds at every dependency edge.**

The output is not merely ordered. It is **stoppable**: every node knows what its output must achieve before the next node is permitted to fire.

---

## 2. Core Claim

> Process is derived from conflicts between constraints.
> **Stop points are derived from the mass transfer requirements between those constraints.**

A process that cannot stop itself cannot be executed deterministically. v1.x produced DAGs that looked deterministic but required external judgment at every gate. v2.0 forces the compiler to specify sufficiency thresholds as a condition of emitting a dependency edge at all.

---

## 3. Inputs

Same as v1.x, with one added requirement:

- Generators and Validators must be PMEST-facet-aligned per `forces.yaml` v1.2.0+.
  Specifically, every Generator must declare `[P] Actant`, `[M] Mass`, `[E] Energy`. Every Validator must declare `[P] Target Actant`, `[S] Scope`, `[T] Temporal Address`.
- Without facet-alignment, Q1b cannot be computed. The interrogator halts.

---

## 4. The Interrogation Step

For every pair of Generators, and for every Generator-Validator relationship, answer five questions.

### Q1a. Dependency — Existence

> Must A exist before B can fire?

**Output:** `PREREQUISITE` | `INDEPENDENT` | `SOFT_DEPENDENCY`

---

### Q1b. Dependency — Sufficiency *(NEW)*

> If A is a prerequisite or soft dependency, **what minimum state must A's Information Mass [M] reach before B can fire correctly?**

This is not "did A run?" — that is Q1a. This is "what must A have *produced* for B to operate without structural risk?"

**Derivation method:**
The sufficiency threshold is computed at the intersection of:
- **A's PMEST [M]** — what mass A is acting on, and what state it leaves that mass in.
- **B's PMEST [M] + [E]** — what mass B requires as input and what work verb it performs on it.
- **The Lock/Key intersection** — the User Need qualities and Document Shape qualities that the mass must satisfy at this boundary.

**Output format:** A concrete, checkable threshold statement bound to the mass.
Example (from the thriller compilation):
- **Edge:** G1 (Instantiator) → G4 (Transformer)
- **Threshold:** G1's output mass must include at least one character-bound vulnerability that the reader has been given cause to value (per Lock: `arousal-seeking`, `affective alienation` failure mode) AND that is *revisable under retroactive recontextualization* (per Key: `heavily gapped`, Transformer's constant-mass requirement).
- **Stop rule:** G4 is forbidden from firing until both conditions are observable in the prior output.

**If Q1b cannot be answered, Q1a is invalid.** A dependency without a sufficiency threshold is a wish, not a gate. The interrogator halts and flags the edge for re-derivation.

---

### Q2. Coupling — Iteration Requirement

> Can A and B be completed independently, or must they converge through mutual adjustment?

**Output:** `INDEPENDENT` | `SEQUENTIAL` | `BIDIRECTIONAL` | `MULTI_NODE_CYCLE`

**New requirement:** Any BIDIRECTIONAL or MULTI_NODE_CYCLE output **must also specify a cycle exit condition** expressed in the same mass-threshold form as Q1b.

v1.x allowed cycles to float with an implicit "converge until stable" exit. v2.0 rejects this. A cycle must declare what mass state ends it.

---

### Q3. Validation Timing

> When can this be validated?

**Output:** `IMMEDIATE` | `DEFERRED` | `TERMINAL` | `CONTINUOUS`

**New requirement:** Any TERMINAL validator must be checked for a continuous shadow. If the validated property requires upstream seeding (i.e., it cannot be constructed post-hoc at the end), the compiler must emit a paired CONTINUOUS validator that seeds the terminal one.

Example: Schema Satisfaction cannot be validated terminally if schema elements were not seeded throughout. The compiler emits V6a (CONTINUOUS seeding check) alongside V6b (TERMINAL assessment).

---

### Q4. Irreversibility — Commitment Cost

> Does executing this early create costly rework later?

**Output:** `REVERSIBLE` | `STABILIZING` | `LOCKING`

**New requirement:** LOCKING and STABILIZING nodes must have Q1b answered for every downstream edge. REVERSIBLE nodes may defer Q1b to runtime reassessment.

---

## 5. Compilation Rules

### Rule 1: DAG Construction
- `PREREQUISITE` (Q1a) + concrete threshold (Q1b) → directed edge with gate
- `INDEPENDENT` → parallelizable nodes
- An edge without a Q1b threshold is not a valid edge.

### Rule 2: Cycle Formation
- `BIDIRECTIONAL` → 2-node cycle with declared exit condition
- `MULTI_NODE_CYCLE` → synchronized cluster with declared exit condition
- A cycle without a declared exit condition is not a valid cycle.

### Rule 3: Validation Placement
- `IMMEDIATE` → inline after generator
- `DEFERRED` → checkpoint after dependent nodes
- `TERMINAL` → end-stage, with mandatory CONTINUOUS shadow if property requires seeding
- `CONTINUOUS` → global constraint

### Rule 4: Ordering
- `LOCKING` → must occur early and pass its Q1b threshold before downstream nodes fire
- `STABILIZING` → floats; fires when upstream Q1b thresholds are met, not on a fixed schedule
- `REVERSIBLE` → safe to defer

### Rule 5: Floating Nodes *(NEW)*
A STABILIZING node does not have a fixed phase position. It fires when its upstream mass thresholds (Q1b) are satisfied. The DAG is therefore not fully sequential — it contains conditional transitions. The compiler must explicitly mark these as `FLOATING_GATE` edges.

---

## 6. Output Structure

The compiler produces:

### Node Set
Generators, Validators, and any paired CONTINUOUS shadows.

### Edge Set
- Directed dependencies *with Q1b thresholds attached to each edge*
- Cyclic couplings *with declared exit conditions*
- Floating gates for STABILIZING nodes

### Execution Phases
Derived from topological layers, cycle clusters, and floating gate positions. Phase transitions are themselves gated by threshold checks.

### Iteration Model
Each cycle specifies:
- Loop contents
- Synchronization rule (which validator arbitrates)
- **Mass-threshold exit condition**

### Validation Schedule
Explicit checkpoints: when, what property, what tolerance.
Terminal validators paired with continuous shadows where required.

### Acceptance Threshold Register *(NEW)*
A flat list of every Q1b threshold in the DAG, indexed by edge. This is the document against which execution can be audited. If every threshold is met at its gate, the process completed correctly. If any threshold cannot be observed, the process has drifted and must be halted for re-derivation.

---

## 7. Halting Conditions of the Interrogator Itself

The interrogator halts and refuses to emit a DAG if:

1. Any Generator or Validator is not PMEST-facet-aligned.
2. Any `PREREQUISITE` or `SOFT_DEPENDENCY` edge has no answerable Q1b.
3. Any cycle has no declared exit condition.
4. Any TERMINAL validator has no continuous shadow where seeding is required.
5. Any LOCKING or STABILIZING node has missing Q1b thresholds on its outbound edges.

These are not warnings. They are compilation errors. A DAG that passes these checks is self-gating. A DAG that doesn't is a v1.x artifact — structurally valid-looking but not executable without human judgment.

---

## 8. Why This Restores Determinism

v1.x produced DAGs that required an operator to judge "is this node done?" at every gate. That judgment is exactly the reasoning the compiler was built to eliminate.

v2.0 moves the sufficiency question into compile-time. The operator no longer asks "is G1 done?" at runtime. The compiler has already declared what G1's output mass must contain. The runtime question becomes "does the output match the declared threshold?" — which is checkable, not judged.

The Lock/Key intersection is the source of truth. Sufficiency is not invented per node. It is read out of the same inputs the DAG itself is read out of.

---

## 9. One-line Summary

> The v2.0 Interrogator produces a self-gating DAG because Q1b forces every dependency edge to declare its own stop condition from the same Lock/Key source the DAG is compiled from. Process design failure in v1.x came from asking *whether* A blocks B without asking *what* A owes B. v2.0 refuses to emit an edge until both are known.