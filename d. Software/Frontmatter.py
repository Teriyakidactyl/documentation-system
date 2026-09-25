#!/usr/bin/env python3
r'''---
uid: 4M3G0Z
architecture: '<a href="%F0%9F%93%90%20Architecture/%F0%9F%93%96%20Software%20Architecture.md" uid="K7W3P9">documentation-system:§d.i.2</a>'
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
python3 "d. Software/Frontmatter.py" PATH
```

Markdown frontmatter begins at the file start. Python frontmatter begins at the
start of the module docstring. Frontmatter delegates YAML payload semantics to
the YAML capability.
'''

from interfaces.cli.frontmatter import main


if __name__ == "__main__":
    main()
