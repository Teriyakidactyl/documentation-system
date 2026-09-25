"""HTML command-line adapter."""
from __future__ import annotations
import argparse,json
from core import invoke
from documentation_system.operations.html import HTML_ANCHORS,HTML_INSPECT
from .common import require_success

def main(argv: list[str] | None=None) -> None:
    parser=argparse.ArgumentParser(prog="documentation_system html")
    sub=parser.add_subparsers(dest="command",required=True)
    for name in ("inspect","anchors"):
        cmd=sub.add_parser(name); cmd.add_argument("path")
    args=parser.parse_args(argv)
    op=HTML_INSPECT if args.command=="inspect" else HTML_ANCHORS
    print(json.dumps(require_success(invoke(op,{"path":args.path})),indent=2,ensure_ascii=False))
