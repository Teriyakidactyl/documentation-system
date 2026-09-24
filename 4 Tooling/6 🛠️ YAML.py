#!/usr/bin/env python3
r'''---
architecture: '<a href="../6%20Software%20Design/2%20%F0%9F%93%96%20Organizing%20Architecture.md" uid="55NHDB">documentation-system:§6.2</a>'
description: >-
  `Read in full and follow when` *a YAML file or YAML value must be parsed
  or validated independently of frontmatter and corpus semantics* `to`
  **confirm its generic YAML structure through the shared YAML capability
  without importing higher-level document rules**.
quadrant: HowTo
outline:
  topology: linear
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
# 🛠️ YAML

Parse a YAML file and emit its normalized data as JSON:

```text
python3 "4 Tooling/6 🛠️ YAML.py" PATH
```

A successful exit confirms YAML syntax. Higher-level frontmatter or corpus
validation remains with the capability that owns those semantics.
'''

from __future__ import annotations

import json
from pathlib import Path
import sys

from _capabilities.yaml import YamlError, load


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(f"Usage: {Path(sys.argv[0]).name} PATH")
    path = Path(sys.argv[1])
    try:
        value = load(path)
    except YamlError as exc:
        raise SystemExit(f"yaml: {exc}") from exc
    print(json.dumps(value, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
