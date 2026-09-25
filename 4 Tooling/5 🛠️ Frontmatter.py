#!/usr/bin/env python3
r'''---
uid: 4M3G0Z
architecture: '<a href="9%20%F0%9F%93%90%20Architecture/2%20%F0%9F%93%96%20Tooling%20Architecture.md" uid="K7W3P9">documentation-system:§4.9.2</a>'
description: >-
  `Read in full and follow when` *a Markdown or Python artifact's metadata
  envelope must be inspected independently of corpus semantics* `to`
  **parse and validate the frontmatter boundary and its YAML payload without
  treating the host body as metadata**.
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
# 🛠️ Frontmatter

Inspect a supported metadata surface:

```text
python3 "4 Tooling/5 🛠️ Frontmatter.py" PATH
```

Markdown frontmatter begins at the file start. Python frontmatter begins at the
start of the module docstring. Frontmatter delegates YAML payload semantics to
the YAML capability.
'''

from __future__ import annotations

import json
from pathlib import Path
import sys

from _capabilities.frontmatter import FrontmatterError, load


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(f"Usage: {Path(sys.argv[0]).name} PATH")
    path = Path(sys.argv[1])
    try:
        value = load(path)
    except FrontmatterError as exc:
        raise SystemExit(f"frontmatter: {exc}") from exc
    if value is None:
        raise SystemExit("frontmatter: no supported frontmatter surface found")
    print(json.dumps({"kind": value.kind, "start_line": value.start_line, "data": value.data}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
