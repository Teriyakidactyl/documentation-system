#!/usr/bin/env python3
r'''---
uid: 6JTNRT
architecture: '<a href="9%20%F0%9F%93%90%20Architecture/2%20%F0%9F%93%96%20Tooling%20Architecture.md" uid="K7W3P9">documentation-system:§4.9.2</a>'
description: >-
  `Read in full and follow when` *one filesystem sibling must be renamed
  without clobbering another path* `to` **preview or execute the rename
  through the same collision-safe Folder capability used by structural
  organization refactors**.
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
# 🛠️ Folder

Preview a sibling rename by supplying the source and destination paths. Add
`--apply` to execute it. Folder owns filesystem safety only; it does not
decide corpus meaning, ordinals, addresses, or reference repair.

```text
python3 "4 Tooling/Folder.py" SOURCE DESTINATION
python3 "4 Tooling/Folder.py" --apply SOURCE DESTINATION
```
'''

from __future__ import annotations

import argparse
import json
from pathlib import Path

from _capabilities.folder import FolderError, Rename, apply


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    rename = Rename(args.source.resolve(), args.destination.absolute())
    print(json.dumps({"from": str(rename.source), "to": str(rename.destination), "applied": args.apply}, indent=2))
    if args.apply:
        try:
            apply([rename])
        except FolderError as exc:
            raise SystemExit(f"folder: {exc}") from exc


if __name__ == "__main__":
    main()
