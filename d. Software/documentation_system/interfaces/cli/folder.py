"""Folder command-line adapter."""
from __future__ import annotations
import argparse,json
from pathlib import Path
from core import invoke
from documentation_system.operations.folder import FOLDER_RENAME,FOLDER_STRIP_PREFIX
from .common import require_success

def main(argv: list[str] | None=None) -> None:
    parser=argparse.ArgumentParser(prog="documentation_system folder")
    sub=parser.add_subparsers(dest="command",required=True)
    rename=sub.add_parser("rename"); rename.add_argument("source"); rename.add_argument("destination"); rename.add_argument("--apply",action="store_true")
    strip=sub.add_parser("strip-prefix"); strip.add_argument("root"); strip.add_argument("--match",required=True); strip.add_argument("--include",default="")
    kind=strip.add_mutually_exclusive_group(); kind.add_argument("--files-only",action="store_true"); kind.add_argument("--folders-only",action="store_true")
    strip.add_argument("--apply",action="store_true")
    args=parser.parse_args(argv)
    if args.command=="rename":
        value=require_success(invoke(FOLDER_RENAME,{"source":args.source,"destination":args.destination,"apply":args.apply}))
    else:
        value=require_success(invoke(FOLDER_STRIP_PREFIX,{"root":args.root,"match":args.match,"include":args.include,"files_only":args.files_only,"folders_only":args.folders_only,"apply":args.apply}))
    print(json.dumps(value,indent=2,ensure_ascii=False))
