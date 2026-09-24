---
description: >-
  `Consult when` *named entries need definitions and repeated attributes in one
  dense lookup surface whose source hierarchy must remain directly readable*
  `to` **render a column-aligned Semantic YAML registry in which labels,
  definitions, values, and nesting remain visually distinct without becoming
  runtime data**.
quadrant: Reference
outline:
  topology: list
  axis: element facet
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

# 📖 Semantic Registry

## Anatomy

A Semantic Registry is one heading-bounded Document Element containing exactly
one fenced `yaml` block. It is a reading surface for humans and agents, not a
runtime configuration format: keys are visible labels, trailing comments may
carry definitions, scalar values carry entry attributes, and indentation scopes
those attributes beneath their entry.

Use a Semantic Registry when definitions and repeated attributes belong in one
dense source surface. Use Hierarchical Glossary instead when the relationship
tree and prose definition table must remain separate representations.

## Source specimen

```markdown
## Profiles
<!-- element: [controlled link to this Document Element] -->

```yaml
# Terms: -------------------------- # Definitions -----------------------------------------
  "Profile":                         # A named execution configuration.
    "Substrate":                     "Typed Relation Modeling"
    "Storage":                       "Semantic YAML"
    "Inference Level":               "Minimal"

  "Another Profile":                 # A second execution configuration.
    "Substrate":                     "Inferential Derivation"
    "Storage":                       "Prolog"
    "Inference Level":               "Deductive"
```
```

## Entry contract

The smallest indentation used by mapping entries identifies registry entries.
Each registry entry is a double-quoted reader-visible label followed by a
trailing-comment definition. Indented mapping entries belong to that registry
entry as attributes or nested groups.

A scalar attribute carries its value on the same line:

```yaml
  "Profile":                         # A named execution configuration.
    "Storage":                       "Semantic YAML"
```

An empty mapping value opens a nested group. Nesting establishes scope only; it
does not imply `is-a`, `part-of`, inheritance, or another semantic relation
unless the surrounding document explicitly defines that meaning.

Use two spaces for each indentation step. Keep every rendered key double-quoted
so labels remain visually uniform and the formatter can treat keys as labels
without inventing runtime identifiers.

## Definition alignment

Use one absolute definition anchor for the complete block. The anchor is four
spaces after the longest rendered key prefix, including indentation and the
colon. Every non-empty value or trailing-comment definition starts at that
anchor.

The header uses the same anchor:

```yaml
# Terms: -------------------------- # Definitions -----------------------------------------
```

The alignment is a deterministic projection of the authored keys, indentation,
and values. Recalculate it after any edit that changes a key or nesting depth;
do not align by eye.

## Constraints

The element is valid when all of the following hold:

- the heading-bounded section contains exactly one fenced `yaml` block;
- the block parses as one YAML mapping;
- indentation contains spaces only and every mapping-entry indentation is a
  multiple of two spaces;
- every rendered mapping key is double-quoted;
- every root registry entry has a non-empty trailing-comment definition;
- the Terms/Definitions header and every non-empty value use the canonical
  absolute definition anchor;
- subject-specific meaning remains in the consuming document; the formatter
  changes spacing and the canonical header only.

Comments are authoritative reader content in this element. Do not use a
Semantic Registry as runtime YAML or feed its comments to software as if YAML
parsing preserved them.

## Operational support

The implementation is colocated with this element in `semantic_registry.py`.
It calls the shared Markdown capability for heading-bounded section and fenced
block structure and the shared YAML capability for generic YAML parsing. The
local adapter owns only this element's entry contract and deterministic
alignment.

Check an instance without changing it:

```text
python3 "2 Technical Writing/3 Document/2 Document Elements/4 Semantic Registry/semantic_registry.py" check PATH SELECTOR
```

Preview the canonical YAML block:

```text
python3 "2 Technical Writing/3 Document/2 Document Elements/4 Semantic Registry/semantic_registry.py" format PATH SELECTOR
```

Apply the deterministic formatting:

```text
python3 "2 Technical Writing/3 Document/2 Document Elements/4 Semantic Registry/semantic_registry.py" format --write PATH SELECTOR
```

`SELECTOR` uses the same section selector rules as the shared Markdown
capability: a local heading number, exact heading, or unique heading title.

Instances record provenance with `element:` metamatter immediately beneath
the element heading as defined by the technical-writing procedure.
