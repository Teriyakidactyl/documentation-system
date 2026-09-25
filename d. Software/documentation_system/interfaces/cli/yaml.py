"""YAML command-line adapter."""
from __future__ import annotations
import argparse,json
from core import invoke
from documentation_system.operations.yaml import OPERATION
from .common import require_success

def main(argv: list[str] | None=None) -> None:
    parser=argparse.ArgumentParser(prog="documentation_system yaml")
    sub=parser.add_subparsers(dest="command",required=True)
    parse=sub.add_parser("parse"); parse.add_argument("path")
    args=parser.parse_args(argv)
    print(json.dumps(require_success(invoke(OPERATION,{"path":args.path})),indent=2,ensure_ascii=False))
