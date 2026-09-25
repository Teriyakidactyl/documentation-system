---
uid: R0J5KF
description: >-
  `Consult when` *software behavior or architecture requires executable
  verification, or an established verification architecture must be selected*
  `to` **route between general testing principles and formal architectures
  that implement those principles for recurring verification surfaces**.
---

# Testing

Testing owns the principles used to design executable verification and the
formal architectures that arrange those principles for recurring verification
problems.

Use the Testing Reference when choosing what a test must prove, where it should
run, what it may depend on, or what evidence makes it trustworthy. Enter
Architectures when the verification surface calls for an established reusable
arrangement.

## Index
<!--
element:
  path:
    uid: BZJASV
    filepath: a. Document Design/a. Document/a. Document Elements/a. Index/README.md
  version: '2.0'
  renderer:
    uid: 45E225
    filepath: d. Software/Navigation Crawler.py
-->

### 📖 Testing

`Consult when` *software behavior, invariants, or component relationships require executable verification and the appropriate test boundary, environment, or assertion strategy is not already fixed* `to` **design tests that prove the owned contract at the smallest faithful boundary, remain deterministic and maintainable across implementation changes, and expose failures with enough evidence to locate the violated invariant**.

<a href="1.%20%F0%9F%93%96%20Testing.md" uid="XW9VC3" data-ds-link="relative-path">../1. 📖 Testing.md</a>

### Architectures

`Consult when` *a recurring verification surface calls for an established arrangement rather than ad-hoc test design* `to` **select the Testing architecture whose discovery, fixture, execution, assertion, and coverage model matches the software being verified**.

<a href="a.%20Architectures/README.md" uid="G5NHDT" data-ds-link="relative-path">../a. Architectures/README.md</a>

- `a. Self-Assembling Verification/README.md`
