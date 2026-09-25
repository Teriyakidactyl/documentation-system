"""HTML command-line adapter."""
from __future__ import annotations
import argparse,json
from repo_manager.core import invoke
from repo_manager.capabilities.html import HTML_ANCHORS,HTML_INSPECT
from .common import require_success

def main(argv: list[str] | None=None) -> None:
    parser=argparse.ArgumentParser()
    sub=parser.add_subparsers(dest="command",required=True)
    for name in ("inspect","anchors"):
        cmd=sub.add_parser(name); cmd.add_argument("path")
    args=parser.parse_args(argv)
    op=HTML_INSPECT if args.command=="inspect" else HTML_ANCHORS
    print(json.dumps(require_success(invoke(op,{"path":args.path})),indent=2,ensure_ascii=False))
