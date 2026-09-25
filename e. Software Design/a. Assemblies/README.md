---
uid: ASM8QY
description: >-
  `Consult when` *software design should reuse an established representation
  rather than derive every implementation arrangement or fragment anew* `to`
  **select the Assembly type whose reuse scope matches the work: Blueprint for
  a durable recurring design or Snippet for a bounded reusable fragment**.
---

# Assemblies

Assemblies is the reusable-representation surface of Software Design.

An Assembly is selected and composed into a live implementation; it does not
become implementation-specific authority merely because it is applicable or
resembles existing code. The code-local Software Architecture Specification
remains the authority for what one implementation has actually selected and
committed to.

## Assembly types

- **Blueprints** fix durable reusable software designs for recurring selecting
  conditions. They may combine decisions from several Software Design concerns.
- **Snippets** are reserved for smaller reusable source-level fragments whose
  selection does not by itself adopt a whole Blueprint.

## Index
<!--
element:
  path:
    uid: BZJASV
    filepath: a. Document Design/a. Assemblies/a. Elements/a. Index/README.md
  version: '2.0'
  renderer:
    uid: 45E225
    filepath: d. Software/Navigation Crawler.py
-->

### Blueprints

`Consult when` *a recurring software constraint calls for an established reusable design rather than ad-hoc architecture* `to` **select the Software Specification Blueprint owned by the design concern that governs the selecting condition**.

<a href="a.%20Blueprints/README.md" uid="BPR7K2" data-ds-link="relative-path">../a. Blueprints/README.md</a>

- `a. Error Management/README.md`
- `b. Testing/README.md`

### Snippets

`Consult when` *a bounded reusable software fragment is sought and adopting a whole Software Specification Blueprint would be broader than the work* `to` **select a canonical Snippet when one exists without treating the fragment as implementation-specific architecture authority**.

<a href="b.%20Snippets/README.md" uid="SNP401" data-ds-link="relative-path">../b. Snippets/README.md</a>
