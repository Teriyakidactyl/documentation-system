---
uid: DYZW24
description: >-
  `Read in full and follow when` *an observed failure should be retained as
  explicit fault evidence* `to` **create a reconstructable record that
  separates observation from causal analysis, records recurrence controls, and
  traces resulting current truth to its owning authority**.
quadrant: HowTo
outline:
  topology: linear
  numbering: hierarchical-decimal
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

# 🛠️ Record A Fault

## 1. Establish the failure boundary

State the governing expectation and the observable divergence from it. Bound one
Fault Record around one failure mechanism or one unresolved causal question
whose evidence must be evaluated together. Do not name a person as the fault.

Identify the repository revision involved when repository state materially
constrained the failure.

## 2. Capture provenance and evidence

Set `fault.recorded-at` to the local retention time with an explicit timezone
offset. Preserve direct observations that establish the divergence, including
tool warnings, returned state, repository state, or interaction facts that
matter to reconstruction.

Separate observed evidence from explanations added later. Do not improve an
observation merely because the eventual mechanism is now understood.

## 3. Reconstruct the occurrence

Describe the context, trigger, failure, and impact in causal order. Add a
timeline only when the ordering itself changes the analysis.

State enough environment or tool behavior to make the event reconstructable.
Do not turn the section into a transcript when a smaller evidence set proves the
same facts.

## 4. Analyze the causal mechanism

Explain how the failure arose from the evidence. Distinguish the trigger from
the mechanism and from conditions that enabled or failed to prevent it.

Retain uncertainty when more than one explanation remains plausible. Do not
force a singular root cause or infer causality from sequence alone.

## 5. Record response and recurrence control

Record how the failed condition was detected, contained, corrected, and
recovered. Then name each corrective action intended to prevent recurrence and
the mechanism by which it should work.

For every corrective action, state what future observation would demonstrate
that the recurrence condition actually changed. A proposed control without an
effectiveness test remains a proposal.

## 6. Trace authority propagation

When the fault changes current guidance, tooling, or another binding rule,
update the controlled artifact that owns that truth. In the Fault Record,
identify that authority and the relationship to the corrective action.

Do not make the Fault Record the sole source of a rule needed for current work.

## 7. Bind the Form and retain the record

Create the timestamp-prefixed filename from `fault.recorded-at`. Bind `form`
to the Fault Record Form package `README.md` and record the contract version
used. Let Organizing mint the record UID.

Store the record in the repository's controlled `.fault` sideband. Run
Organizing and finish only when the record is controlled, remains unaddressed
and unindexed, and its Form provenance resolves.
