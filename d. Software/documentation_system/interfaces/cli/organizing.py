"""Organizing command-line adapter."""
from __future__ import annotations
import argparse,json
import sys
from pathlib import Path
from core import Severity,invoke
from core.projection import json_text
from documentation_system.operations.organizing import INSPECT,NORMALIZE,REFRESH,RESOLVE

def _root(value: str | None) -> str:
    return str(Path(value or ".").resolve())

def main(argv: list[str] | None=None) -> None:
    parser=argparse.ArgumentParser(prog="documentation_system organizing")
    sub=parser.add_subparsers(dest="command",required=True)
    p=sub.add_parser("refresh"); p.add_argument("corpus_root",nargs="?"); p.add_argument("--annotate",action="store_true"); p.add_argument("--diagnostics-json",default="")
    p=sub.add_parser("inspect"); p.add_argument("corpus_root",nargs="?")
    p=sub.add_parser("resolve"); p.add_argument("address"); p.add_argument("corpus_root",nargs="?")
    p=sub.add_parser("normalize"); p.add_argument("corpus_root",nargs="?"); p.add_argument("--apply",action="store_true")
    args=parser.parse_args(argv)
    if args.command=="refresh":
        result=invoke(REFRESH,{"corpus_root":_root(args.corpus_root),"annotate":args.annotate})
        if args.diagnostics_json:
            Path(args.diagnostics_json).write_text(json_text(result)+"\n",encoding="utf-8")
        if result.value:
            value=result.value
            print(f"Refreshed {value['artifacts']} controlled artifacts across {value['locations']} organized locations; minted {value['uids_minted']} uids, refreshed {value['links_refreshed']} controlled links, and reported {len(value['diagnostics'])} diagnostics")
    elif args.command=="inspect":
        result=invoke(INSPECT,{"corpus_root":_root(args.corpus_root)})
        if result.ok: print(json.dumps(result.value,indent=2,ensure_ascii=False))
    elif args.command=="resolve":
        result=invoke(RESOLVE,{"corpus_root":_root(args.corpus_root),"address":args.address})
        if result.ok: print(json.dumps(result.value,indent=2,ensure_ascii=False))
    else:
        result=invoke(NORMALIZE,{"corpus_root":_root(args.corpus_root),"apply":args.apply})
        if result.ok: print(json.dumps(result.value,indent=2,ensure_ascii=False))
    if not result.ok:
        print(json_text(result),file=sys.stderr); raise SystemExit(1)
    if any(item.severity is Severity.ERROR for item in result.diagnostics):
        raise SystemExit(1)
