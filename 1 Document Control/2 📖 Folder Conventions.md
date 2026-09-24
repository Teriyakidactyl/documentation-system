---
uid: TRJS8V
description: >-
  `Consult when` *a directory name begins with a reserved prefix and its corpus
  membership, Organizing traversal, or access condition is unknown* `to` **confirm
  what the prefix reserves, whether the Organizing enters it, and whether reading
  it requires a specific instruction**.
quadrant: Reference
outline:
  topology: list
  axis: name prefix
  numbering: hierarchical-decimal
writing-style:
  formality: professional
  tone: clinical/detached
  mode: declarative
  density: compressed/dense
  abstraction: concrete/specific
  redundancy: zero
  signposting: entry-headers only
  register: technical
---

# 📖 Folder Conventions

A *reserved prefix* changes how a directory participates in the controlled
corpus. The remainder of the name is descriptive only.

| Prefix | Meaning | Organizing | Agent |
|---|---|---|---|
| `.research` | Controlled research sideband for retained investigation prompts and run outputs. | Descend and control metadata-bearing artifacts, including UID minting and research-provenance validation; descendants have no Documentation System address and do not enter generated indexes. Preserve prompt/report payloads as historical evidence rather than applying current-authority prose diagnostics to them. | Read only when the user explicitly requests research material or names the directory or investigation. |
| `.<name>` | Any other dot-prefixed directory is outside the controlled corpus; repository/tool state or local working material. | Do not descend. | Read only when the user explicitly names the directory. |
| `_<name>` | Operational grouping, not classification; address-transparent. | No special treatment; descendants participate normally. | Normal access unless an enclosing rule excludes it. |
