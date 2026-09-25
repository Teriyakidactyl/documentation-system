"""Harness command-line adapter."""
from __future__ import annotations
import argparse
from pathlib import Path
import sys
from capabilities.harness import HarnessError,find_repository_root
from core import invoke
from core.projection import json_text
from core.result import Result
from documentation_system.operations.harness import HARNESS_PROJECT

def main(argv: list[str] | None=None, *, script: Path | None=None) -> None:
    parser=argparse.ArgumentParser(prog="documentation_system harness")
    sub=parser.add_subparsers(dest="command",required=True)
    for name in ("install","check","remove"):
        cmd=sub.add_parser(name); cmd.add_argument("host_root",nargs="?"); cmd.add_argument("--target",action="append",default=[])
    args=parser.parse_args(argv)
    script=script or Path(sys.argv[0]).resolve()
    try:
        source_root=find_repository_root(script)
    except HarnessError as exc:
        print(str(exc),file=sys.stderr); raise SystemExit(1)
    host_root=Path(args.host_root).resolve() if args.host_root else Path.cwd().resolve()
    result=invoke(HARNESS_PROJECT,{"source_root":str(source_root),"host_root":str(host_root),"mode":args.command,"targets":args.target})
    if result.value:
        for row in result.value["results"]:
            print(f"{row['state']:12} {row['link']}")
    if not result.ok:
        print(json_text(result),file=sys.stderr); raise SystemExit(1)
