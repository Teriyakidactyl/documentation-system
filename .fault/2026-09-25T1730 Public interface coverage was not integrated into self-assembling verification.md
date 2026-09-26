---
form:
  path: '<a href="../a.%20Document%20Design/a.%20Assemblies/b.%20Forms/c.%20Fault%20Record/README.md" uid="CD4R6P">documentation-system:§a.a.b.c</a>'
  version: '1.0'
description: >-
  `Read in full when` *the verification-design gap that left public command
  projection outside self-assembled coverage needs review* `to` **reconstruct
  which boundary-testing requirements already existed, which integration
  requirement became explicit later, and why operation discovery did not
  automatically exercise the consumer-visible CLI boundary**.
quadrant: Explanation
fault:
  recorded-at: '2026-09-25T17:30:00-07:00'
  repository-revision: d29a01d0a806a36bcaa39474cd23218bcb9ef803
outline:
  numbering: hierarchical-decimal
writing-style:
  formality: professional
  tone: collegial/earnest
  mode: declarative
  density: moderate
  abstraction: mixed
  redundancy: zero
  signposting: suppressed
  register: accessible
---

# 💡 Public interface coverage was not integrated into self-assembling verification

## Expectation

Before the current self-assembling verification implementation was introduced,
the Software Design Testing Reference already required verification to use the
smallest faithful boundary and explicitly warned against substituting an
internal boundary when the risk lies in public dispatch, propagation, or
presentation. Its coverage guidance named `public commands with boundary
verification` as a preferred coverage surface.

That Testing Reference was present at commit
`c075639941b2` at 2026-09-25T19:55:14Z. The first commit adding
`test_verification_surface.py` followed at `75216ef550eb` at
2026-09-25T20:18:01Z. The requirement to verify consumer-visible command
behavior therefore existed in repository authority before the verification
surface was implemented.

The Software Architecture at the same earlier revision also treated the public
Organizing executable as part of verification: CI ran Organizing through its
historical public entry path and the same public boundary was required to remain
usable locally.

A later working migration plan made the final intent still more concrete: every
supported CLI route was to be exercised through the final `repo` entry point
with representative success and failure projection tests. That plan was working
migration material rather than repository current authority, but it shows that
public-boundary verification was an accepted completion condition during the
migration.

One requirement was **not** explicit at the beginning: repository guidance and
the migration plan did not state that public-interface execution itself had to
be assembled by the same self-discovering verifier. They required public
boundary coverage. The stronger integration rule—discover an operation, then
automatically require and exercise its public projection—became explicit only
after the Organizing diagnostic regression exposed the gap and was clarified
further in the later discussion that led to this record.

The final installed `repo` executable and its packaging mechanism were also
deliberately unresolved while the intermediate verification machinery was being
built. Absence of tests through a not-yet-existent executable was therefore not,
by itself, a failure.

## Occurrence

The implemented self-assembling verifier discovers semantic-owner
`Operation` declarations and assembles generated operation cases. Its coverage
check treats a declared command tuple as evidence that a public CLI route exists,
checks that command tuples are unique, and checks that the operation owner is a
semantic owner.

The generated cases execute the operation boundary directly. They do not execute
the corresponding CLI adapter or another public-interface projection. The
verification model therefore has no mechanically enforced relationship of the
form:

~~~text
discovered operation
→ discovered public route
→ executable public projection
→ interface contract
~~~

A separate authored test,
`d. Software/tests/test_organizing_cli.py`, was added after three concrete
Organizing CLI regressions were found. It protects those exact projection
contracts, including successful diagnostic rendering and diagnostics JSON shape,
but it is not connected to the discovered operation surface. Adding another
public command can therefore satisfy current self-assembled coverage without
automatically acquiring equivalent public-boundary execution.

The practical divergence was visible in the Organizing regression: the semantic
diagnostics remained available through the operation result while terminal and
JSON projection behavior changed. Operation-level verification remained green
because the defect existed after the operation boundary.

During later discussion, the verification design was initially described as two
separate layers—self-assembled operation verification and additional
public-interface tests. The user asked whether the public interface could
participate in self-assembled testing. Re-examining the design showed that it
can and should: route discovery can mechanically require public-boundary
execution while authored declarations remain the independent authority for
projection-specific semantics.

## Evidence

Repository and interaction evidence constrain the diagnosis:

- `e. Software Design/l. Testing/1. 📖 Testing.md` existed before the first
  verification-surface test and required faithful public-boundary testing where
  dispatch or presentation is the risk.
- That Reference explicitly used `public commands with boundary verification`
  as a coverage example.
- The earlier Software Architecture required Organizing verification through its
  historical public executable boundary.
- `repo_manager.verification.discovery` discovers operations from semantic
  owners without importing the CLI, which correctly preserves semantic
  ownership.
- `repo_manager.verification.coverage.coverage_findings` currently checks that
  an operation has command metadata and that command tuples are unique, but it
  does not prove that those routes are implemented or executable.
- `repo_manager.verification.cases.assemble` generates operation cases for the
  direct operation boundary; there is no corresponding interface-case assembly.
- `test_organizing_cli.py` exists because operation correctness alone did not
  preserve terminal and diagnostics-file behavior.
- The working migration plan already required eventual execution of every final
  CLI route and representative CLI success/failure projection tests, but it did
  not explicitly require those checks to be driven by the same discovery
  mechanism.
- At the time this fault was analyzed, the final `repo` executable still did
  not exist, so tests through that exact executable could not yet have been
  implemented faithfully.
- In the recent continuation of this work, the complete Software Architecture
  and Software Design guidance was no longer present in active, non-compacted
  context. The user explicitly asked for root re-entry and relevant guidance to
  be reread. That context loss affected the later explanation of the design.
  It does not establish that the same documents were unread when the original
  verifier was first implemented.
- Available evidence does not establish whether the complete Testing Reference
  and architecture documents were active in model context at the exact moment
  the original self-assembling design was authored. This record therefore does
  not treat failure to read those documents as a proven original cause.

The evidence establishes a design and coverage gap. It does not establish that
the existing generated operation tests are wrong or that authored CLI tests
should be removed.

## Causal analysis

The primary failure mechanism was an incomplete boundary model in the
self-assembling verifier.

The verifier was correctly centered on semantic-owner `Operation`
declarations. Interface code was intentionally excluded from semantic ownership
and discovery so a future interface could invoke the same operation without
owning it. That separation was sound, but the design stopped one step too early:
command metadata was treated as a property of the operation rather than as a
relationship to an independently executable public projection.

This produced an asymmetric model:

~~~text
operation declaration
→ generated operation cases
→ direct operation contracts

operation declaration
→ command tuple
→ uniqueness check only
~~~

Several conditions contributed.

First, the installed `repo` entry point and exact route vocabulary were
intentionally deferred. That made postponing executable CLI-boundary integration
reasonable for an intermediate milestone, but the verifier did not encode the
deferred obligation as a first-class coverage dimension. The temporary absence
therefore became structurally easy to overlook.

Second, the verification implementation optimized for keeping CLI modules out of
semantic discovery. That was the right dependency direction, but no separate
interface registry, dispatcher contract, or projection adapter was introduced
to let verification exercise the interface without transferring semantic
ownership to it.

Third, when the Organizing projection regression was found, the immediate
repair correctly added authored regression tests. That restored the observed
contract quickly, but it repaired one public projection rather than changing
the general coverage model. The successful local correction reduced pressure to
promote the discovered fault class into structural verification.

Fourth, the stronger rule that the public interface should **participate in the
self-assembled system**, rather than merely have separate public-boundary tests,
was not stated explicitly in the initial repository requirements. It emerged
from combining the existing public-boundary requirement with the later
self-discovery goal. The omission is therefore not fairly characterized as
ignoring an explicit same-verifier requirement.

Finally, recent context compaction weakened the design review. When this work
was resumed, the full governing documents were not active and the initial
explanation again separated self-assembled operation verification from public
interface tests. The repository root explicitly requires rereading selected
guidance when prior presence is only compacted. That control was reactivated
only after the user requested root re-entry. This is a contributing condition
to the recent reasoning, not a proven cause of the original implementation.

## Response and recovery

The gap was detected through discussion of what current Python testing covers,
followed by review of the remaining migration work and the earlier Organizing
diagnostic regression.

The immediate conceptual correction is:

~~~text
public Operation
├── semantic operation boundary
└── public interface projection
     └── both participate in discoverable coverage
~~~

Generated verification remains valid at the operation boundary. Authored
projection contracts also remain necessary where intended stdout/stderr,
diagnostic rendering, file schemas, or exit semantics cannot be independently
derived from the implementation.

Recovery is not complete merely by adding another dedicated CLI test. The
verification model must make public-interface participation mechanically visible
and fail coverage when a declared public route cannot be exercised.

## Recurrence control

The corrective design should introduce these controls:

1. Treat each declared public command route as a discoverable interface
   projection of its owning operation, not merely as a tuple that must be unique.
2. Make the self-assembling verifier require an executable interface route for
   every public command declaration.
3. Assemble public-interface cases from the same independently authored
   operation inputs wherever those inputs can be faithfully projected into CLI
   arguments.
4. Keep projection-specific expectations independently authored or declared when
   they cannot be derived safely, including stdout/stderr policy, diagnostic
   rendering, machine-readable output schemas, and exit behavior.
5. Report operation-boundary coverage and interface-boundary coverage
   separately so one cannot stand in for the other.
6. Preserve dedicated authored regression tests only for cases that cannot be
   expressed faithfully through generic or declared interface contracts; do not
   retain wrapper-choreography tests after the wrapper ceases to be a public
   contract.
7. When the installed `repo` entry point is established, exercise the same
   route model through that final boundary and make absence of final-boundary
   coverage a mechanically visible gap.

Effectiveness is demonstrated when adding a new public command declaration
without an executable interface projection fails verification automatically,
and when a projection regression such as lost diagnostics or an invalid declared
JSON shape fails without requiring a maintainer to remember to add a separate
test file manually.

## Authority propagation

The Testing Reference already owns the general rule that the faithful public
boundary must be tested when that boundary carries the risk. It does not need a
new rule merely to narrate this fault.

The current Software Architecture should be corrected so its implemented
verification design states that self-assembled coverage includes both semantic
operation execution and declared public-interface projections, while keeping
projection-specific semantic expectations independently authored.

The verification implementation and its executable tests must realize that
architecture. Coverage reporting must distinguish the two boundaries.

When the final `repo` dispatcher and packaging entry point are introduced,
their interface declarations become the current executable authority for public
route realization. This Fault Record remains historical evidence for why
command metadata alone is not public-boundary coverage.
