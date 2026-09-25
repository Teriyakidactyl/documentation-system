"""YAML command-line adapter."""
from __future__ import annotations
import argparse,json
from repo_manager.core import invoke
from repo_manager.capabilities.yaml import OPERATION
from .common import require_success

def main(argv: list[str] | None=None) -> None:
    parser=argparse.ArgumentParser()
    sub=parser.add_subparsers(dest="command",required=True)
    parse=sub.add_parser("parse"); parse.add_argument("path")
    args=parser.parse_args(argv)
    print(json.dumps(require_success(invoke(OPERATION,{"path":args.path})),indent=2,ensure_ascii=False))
