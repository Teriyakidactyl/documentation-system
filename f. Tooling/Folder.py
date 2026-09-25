#!/usr/bin/env python3
r'''---
uid: 6JTNRT
architecture: '<a href="%F0%9F%93%90%20Architecture/%F0%9F%93%96%20Tooling%20Architecture.md" uid="K7W3P9">documentation-system:§f.d.2</a>'
description: >-
  `Read in full and follow when` *one filesystem path must be renamed or a
  declared basename prefix must be removed from matching descendant files or
  folders* `to` **preview or execute one collision-safe rename plan without
  stripping non-matching names or removing text outside the proven prefix
  match**.
quadrant: HowTo
outline:
  topology: branching
  axis: operation
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

Use Folder for filesystem-name mutation only. It can rename one sibling path or
derive a recursive batch plan by matching a basename prefix. Folder does not
decide corpus meaning, ordinals, addresses, or reference repair.

Every operation is a dry run unless `--apply` is supplied.

## 1. Rename one sibling

Supply one source and one destination:

```text
python3 "f. Tooling/Folder.py" SOURCE DESTINATION
python3 "f. Tooling/Folder.py" --apply SOURCE DESTINATION
```

The source and destination must be siblings. Folder refuses to overwrite an
unrelated existing destination.

## 2. Strip a matched basename prefix

Use `strip-prefix` when the text to remove is itself the evidence selecting a
path for mutation:

```text
python3 "f. Tooling/Folder.py" strip-prefix ROOT --match REGEX
python3 "f. Tooling/Folder.py" strip-prefix ROOT --match REGEX --apply
```

Folder recursively examines descendant basenames under `ROOT`. Files and
directories are both candidates by default. The root itself and symlinks are
not renamed.

> [!IMPORTANT]
> **Prefix stripping is match-driven, not blind.** Folder evaluates `REGEX`
> against the basename from character zero. A path changes only when that
> prefix match succeeds, and Folder removes exactly the characters consumed by
> that match. It does not call `lstrip`, normalize a class of characters, or
> remove a guessed prefix from non-matching names.

For example:

```text
--match '^[0-9]+ 🛠️ '
```

selects and removes only a leading sequence such as `1 🛠️ `. A basename such
as `3 📖 Reference.md` does not match and is untouched.

Narrow the candidate set independently of the removed prefix with
`--include GLOB`:

```text
python3 "f. Tooling/Folder.py" strip-prefix "f. Tooling" \
  --files-only \
  --include "*.py" \
  --match '^[0-9]+ '
```

Here `*.py` decides which basenames may be considered; it contributes no
characters to the removed span. A matching `1 Tool.py` becomes `Tool.py`,
while `8 🛠️ Prepare Tooling Environment.md` is not a candidate and remains
unchanged.

Use `--files-only` or `--folders-only` when one path kind alone should be
eligible. Omit both to consider both files and directories.

## 3. Inspect the plan before applying it

The command emits the complete rename plan as JSON. For `strip-prefix`, each
`from` and `to` path is shown relative to `ROOT`.

Do not add `--apply` until every planned destination expresses the intended
basename transformation. An empty plan is valid and means no candidate
satisfied both the optional selector and the prefix match.

## 4. Rely on transaction safety, not guessing

Folder validates the complete plan before mutation. It rejects:

- a missing source;
- a destination outside the source's parent;
- duplicate sources or destinations;
- collision with an unmatched existing sibling;
- an invalid regular expression;
- a prefix match that consumes zero characters; and
- a prefix match that would remove the entire basename.

Batch application processes deeper sibling groups before their parent
directories so nested file and folder renames can participate in one plan.
Each group uses temporary names to avoid swap and cycle collisions. If a later
group fails, Folder attempts to roll already-completed groups back in reverse
order.

Folder changes filesystem paths only. A caller that owns semantic references
must repair or refresh those references after the path transaction. For the
Documentation System corpus, Organizing owns controlled-link, index, and other
derived path projections.
'''

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from _capabilities.folder import FolderError, Rename, apply, plan_strip_prefix


def _single_rename(argv: list[str]) -> None:
    parser = argparse.ArgumentParser(
        prog=Path(sys.argv[0]).name,
        description="Preview or apply one collision-safe sibling rename.",
    )
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args(argv)

    rename = Rename(args.source.resolve(), args.destination.absolute())
    payload = {
        "operation": "rename",
        "renames": [{"from": str(rename.source), "to": str(rename.destination)}],
        "applied": False,
    }
    if args.apply:
        apply([rename])
        payload["applied"] = True
    print(json.dumps(payload, indent=2, ensure_ascii=False))


def _strip_prefix(argv: list[str]) -> None:
    parser = argparse.ArgumentParser(
        prog=f"{Path(sys.argv[0]).name} strip-prefix",
        description=(
            "Recursively strip exactly the basename prefix consumed by a "
            "successful regular-expression match."
        ),
    )
    parser.add_argument("root", type=Path)
    parser.add_argument(
        "--match",
        required=True,
        help="Regular expression matched from basename character zero; exactly its consumed span is removed.",
    )
    parser.add_argument(
        "--include",
        dest="name_glob",
        help="Optional basename glob selecting candidates before prefix matching, for example '*.py'.",
    )
    kind = parser.add_mutually_exclusive_group()
    kind.add_argument("--files-only", action="store_true")
    kind.add_argument("--folders-only", action="store_true")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args(argv)

    root = args.root.resolve()
    plan = plan_strip_prefix(
        root,
        args.match,
        include_files=not args.folders_only,
        include_directories=not args.files_only,
        name_glob=args.name_glob,
    )

    payload = {
        "operation": "strip-prefix",
        "root": str(root),
        "match": args.match,
        "include": args.name_glob,
        "path_kinds": (
            "files"
            if args.files_only
            else "folders"
            if args.folders_only
            else "files-and-folders"
        ),
        "renames": [
            {
                "from": item.source.relative_to(root).as_posix(),
                "to": item.destination.relative_to(root).as_posix(),
            }
            for item in plan
        ],
        "applied": False,
    }

    if args.apply:
        apply(plan)
        payload["applied"] = True
    print(json.dumps(payload, indent=2, ensure_ascii=False))


def main() -> None:
    try:
        if len(sys.argv) > 1 and sys.argv[1] == "strip-prefix":
            _strip_prefix(sys.argv[2:])
        else:
            _single_rename(sys.argv[1:])
    except FolderError as exc:
        raise SystemExit(f"folder: {exc}") from exc


if __name__ == "__main__":
    main()
