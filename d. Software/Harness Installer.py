#!/usr/bin/env python3
r'''---
uid: N5986D
architecture: '<a href="%F0%9F%93%90%20Architecture/%F0%9F%93%96%20Software%20Architecture.md" uid="K7W3P9">documentation-system:§d.g.2</a>'
description: >-
  `Read in full and follow when` *a repository has installed the Documentation
  System but an agent harness cannot discover it under the skill name declared
  by SKILL.md* `to` **project the canonical Documentation System directory into
  each selected harness skill directory with an idempotent symlink**.
quadrant: HowTo
---
# 🛠️ Harness Installer

Use this tool from the Documentation System repository or submodule. The
canonical source directory is the Git repository containing this tool; the
harness-facing symlink name is read from `SKILL.md#name`, for example
`documentation-system`.

The installer never copies the corpus. It creates or validates symlinks so one
canonical working tree is visible through harness-specific skill paths. A real
file or directory already occupying the target name is never overwritten.

By default the host repository is the current working directory and the script
looks for existing `.agents/skills`, `.claude/skills`, and `.github/skills`
directories. Pass `--target PATH` one or more times to select other skill
directories explicitly.

Usage:
    python3 "d. Software/Harness Installer.py" [host_root]
    python3 "d. Software/Harness Installer.py" --check [host_root]
    python3 "d. Software/Harness Installer.py" --remove [host_root]
    python3 "d. Software/Harness Installer.py" --target .agents/skills [host_root]

Requires PyYAML.
'''

from pathlib import Path

import sys
from documentation_system.interfaces.cli.harness import main


if __name__ == "__main__":
    argv=list(sys.argv[1:])
    mode="install"
    if "--check" in argv:
        argv.remove("--check"); mode="check"
    if "--remove" in argv:
        argv.remove("--remove"); mode="remove"
    main([mode,*argv],script=Path(__file__).resolve())
