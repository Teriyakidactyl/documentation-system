"""Documentation System command-line entry point."""
from __future__ import annotations
import argparse
from documentation_system.interfaces.cli import folder,frontmatter,harness,html,markdown,organizing,yaml

COMMANDS={
    "folder":folder.main,
    "frontmatter":frontmatter.main,
    "harness":harness.main,
    "html":html.main,
    "markdown":markdown.main,
    "organizing":organizing.main,
    "yaml":yaml.main,
}

def main(argv: list[str] | None=None) -> None:
    parser=argparse.ArgumentParser(prog="python -m documentation_system")
    parser.add_argument("command",choices=tuple(COMMANDS))
    args,rest=parser.parse_known_args(argv)
    COMMANDS[args.command](rest)

if __name__=="__main__":
    main()
