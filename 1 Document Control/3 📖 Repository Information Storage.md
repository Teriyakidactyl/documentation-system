---
uid: S9HVWB
description: >-
  `Consult when` *repository information must be retained but its authority,
  discoverability, retrieval path, or storage representation is unclear* `to`
  **separate information role from retrieval policy and storage method, using
  ordinary repository files by default and selecting another Git-backed method
  only for a concrete control benefit**.
quadrant: Reference
outline:
  topology: tree
  axis: repository information storage concept
  numbering: hierarchical-decimal
writing-style:
  formality: professional
  tone: clinical/detached
  mode: declarative
  density: compressed/dense
  abstraction: mixed
  redundancy: zero
  signposting: entry-headers only
  register: technical
---

# 📖 Repository Information Storage

Repository information has three independent properties:

```text
information role
≠ retrieval policy
≠ storage method
```

Storage mechanism does not determine authority. A Markdown file, Git note,
commit trailer, tag, or object in another ref can each carry authoritative,
auxiliary, historical, or working information when a governing process assigns
that role.

Ordinary files in the ordinary repository tree are the default storage
representation because they provide the broadest shared ergonomics for humans
and agents. Another storage method is justified only when it provides a
concrete control benefit that outweighs its additional retrieval and tooling
cost.

## 1. Access environment

Human maintainers primarily interact with repository information through Visual
Studio Code. Ordinary filesystem navigation, search, editing, diff, and
source-control review are therefore baseline human capabilities for storage
design.

Agent access has a different constraint: information exposed during ordinary
retrieval competes for context and can compete with current authority.
Discoverability can be controlled independently of human file visibility, so
information does not need to become difficult for humans to access merely
because agents should not retrieve it by default.

Ordinary file ergonomics remain preferable when retrieval policy alone can
solve the control problem.

## 2. Information roles

Information role states what retained information does.

| Role | Function |
|---|---|
| **current authority** | Information a user must be able to rely on when acting now. |
| **working information** | Mutable planning, task, project, or investigation state used to produce another result. |
| **evidence and provenance** | Information whose job is to establish how a claim, review, decision, or state was supported. |
| **historical or cold information** | Retained material whose past state or supporting detail has a legitimate future use but is not current operating authority. |

One artifact can change role over time. A research conclusion becomes current
authority when users need it to act correctly; the current rule should not
remain available only through research, project tracking, an ADR history, or
process evidence.

A superseded representation leaves current authority when its remaining job is
historical or evidentiary rather than operational.

## 3. Retrieval policies

Retrieval policy states how readily information should enter a user's working
context.

| Policy | Use |
|---|---|
| **normal retrieval** | The information participates in ordinary discovery for its subject. |
| **explicit retrieval** | The information is available when a user deliberately asks for that class, project, investigation, or history, but does not compete with current authority by default. |
| **object- or event-specific retrieval** | The information is naturally requested through a particular repository state, commit, tag, review, or other Git event rather than by browsing a topic tree. |

A requirement for explicit retrieval does not by itself require moving
information out of the ordinary filesystem. A routing or folder convention is
preferred when it preserves human ergonomics and still gives agents an
unambiguous access condition.

Dot-prefixed directories are one existing explicit-retrieval mechanism in this
corpus; their access behavior is defined by
<a href="2%20%F0%9F%93%96%20Folder%20Conventions.md" uid="TRJS8V">documentation-system:§1.2</a>.
That convention applies when its explicit-only retrieval rule is the intended
policy.

## 4. Storage methods

| Method | Strong fit | Cost or constraint |
|---|---|---|
| **Ordinary repository file or directory** | Current authority, working information, research, project state, decisions, or other material naturally browsed by subject. | Participates in ordinary filesystem discovery unless routing says otherwise. |
| **Reserved sideband directory** | Human-browsable working, research, or cold material that should require explicit agent retrieval. | Remains in the working tree and repository history; the convention must make its retrieval rule unambiguous. |
| **Separate branch, worktree, or custom ref** | Information requiring an independent history or lifecycle from the main tree. | Additional navigation, synchronization, and tooling complexity; ordinary tree access may require projection through a worktree or tool. |
| **Git-attached metadata such as a note** | Evidence or metadata whose natural subject is an exact Git object and which should not mutate that object's file representation. | Poorer ordinary filesystem visibility; requires tooling or Git-aware retrieval. |
| **Commit trailer** | Small structured relationships or facts whose natural subject is the commit itself. | Payload must remain compact and commit-scoped. |
| **Annotated tag** | Named milestone, release, approval, or attestation attached to an important repository state. | Suited to sparse named states rather than routine mutable records. |

These are selecting conditions, not a progression toward more sophisticated
storage. Ordinary files remain preferred unless another method models the
information better or prevents a concrete control failure.

## 5. Alternative storage conditions

A non-file or separate-history representation is justified when at least one
concrete constraint materially applies:

- ordinary discovery would cause historical or evidentiary material to compete
  with current authority;
- the information's natural identity is a Git object or event rather than a
  repository topic;
- the information requires an independent lifecycle, retention policy, or
  synchronization path;
- generated volume or churn would materially degrade ordinary repository
  history or review; or
- a governing assurance, audit, or provenance requirement requires attachment
  to an exact repository state.

Secondary status, infrequent use, or potential size does not by itself justify
an exotic storage mechanism. Human browseability, ordinary search, diff, and
editing are control benefits too.

The discriminating test is:

> If this information were an ordinary well-named repository file, what
> concrete control failure would result?

Absent a concrete failure, the ordinary representation remains the default.

## 6. Recurring information patterns

### 6.1 Research

Substantial research material is naturally browsed by investigation or topic.
Source records, notes, intermediate analysis, and other retained research
therefore fit ordinary files unless another constraint selects different
storage.

When research should not enter normal agent retrieval, a reserved sideband
directory can provide explicit-only access without sacrificing ordinary human
file navigation.

Conclusions required for current action belong in the controlled information
that owns the subject. Current policy should not require reconstruction from
research history.

### 6.2 Projects and tasks

Project and task information is normally mutable, hierarchical, and
human-browsable. Ordinary files are therefore the default repository-local
representation when the repository itself owns that tracking.

Another system or Git storage plane becomes appropriate when collaboration,
assignment, notification, independent lifecycle, or another concrete process
requirement selects it. Conceptual separation from product information alone
does not justify moving project state out of the ordinary tree.

### 6.3 Architectural decisions

A currently binding architectural constraint belongs in the controlled
architecture information whose readers need it to implement the system
correctly.

A retained decision record can additionally preserve the original problem,
alternatives, tradeoffs, rejected approaches, and decision provenance when
that history has a concrete future job. That deliberation may use explicit
retrieval or another storage method without becoming the sole source of the
current architectural rule.

### 6.4 Cross-context validation evidence

Formal Validation can produce evidence that must be communicated from one
context or reviewer to another. A Validation Receipt is the transmissible
representation of that result.

When the receipt only needs to cross the immediate coordination boundary, the
message or task context can carry it. When a governing process requires the
evidence to survive that context and the claim is about an exact repository
state, Git-attached storage is a plausible pattern because it can bind evidence
to the state without modifying the validated artifact.

A durable Git-attached receipt can follow this pattern:

```text
validation record
        ↓
schema + cross-field invariant validation
        ↓
bind controlled artifact identity + exact repository state
        ↓
canonical receipt representation
        ↓
Git-attached persistence adapter
        ↓
Git storage primitive
```

Receipt semantics remain above the storage primitive. The receipt model decides
what evidence is admissible and what subject state it describes; the storage
adapter only persists and retrieves already-valid representations. Validation
users therefore do not need to manipulate note refs, object IDs, or other Git
plumbing directly.

Schema validation protects durable process evidence from malformed fields,
unknown result vocabulary, contradictory clean/fault claims, missing subject
identity, and similar representation errors. It establishes structural
admissibility, not the truth of an authored judgment.

For a controlled artifact, its `uid` supplies conceptual identity and an exact
Git object or equivalent state identifier can supply the representation state
examined. Neither substitutes for the other.

Git Notes are one candidate implementation of this pattern, not a repository
default. They are selected only when object attachment and durable assurance
evidence justify the loss of ordinary file visibility. A tool may also project
a stored receipt back over its exact subject state as an annotated artifact so
faults, clean checks, or uncertainty appear beside the material reviewed; that
annotation is a view of the receipt, not a mutation of the canonical artifact.

Validation receipt semantics are owned by
<a href="../7%20Editing/5%20%F0%9F%93%96%20Validation%20Evidence.md" uid="5SK5Z4">documentation-system:§7.5</a>.
