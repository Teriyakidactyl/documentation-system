"""Harness command-line adapter."""
from __future__ import annotations
import argparse
from pathlib import Path
import sys
from repo_manager.core import invoke
from repo_manager.core.projection import json_text
from repo_manager.capabilities.harness import HARNESS_PROJECT

def _source_root() -> Path:
    for candidate in Path(__file__).resolve().parents:
        if (candidate/"SKILL.md").is_file():
            return candidate
    raise SystemExit("Cannot locate Documentation System source root containing SKILL.md")

def main(argv: list[str] | None=None) -> None:
    parser=argparse.ArgumentParser()
    sub=parser.add_subparsers(dest="command",required=True)
    for name in ("install","check","remove"):
        cmd=sub.add_parser(name)
        cmd.add_argument("host_root",nargs="?")
        cmd.add_argument("--target",action="append",default=[])
    args=parser.parse_args(argv)
    source_root=_source_root()
    host_root=Path(args.host_root).resolve() if args.host_root else Path.cwd().resolve()
    result=invoke(HARNESS_PROJECT,{
        "source_root":str(source_root),
        "host_root":str(host_root),
        "mode":args.command,
        "targets":args.target,
    })
    if result.value:
        for row in result.value["results"]:
            print(f"{row['state']:12} {row['link']}")
    if not result.ok:
        print(json_text(result),file=sys.stderr)
        raise SystemExit(1)
