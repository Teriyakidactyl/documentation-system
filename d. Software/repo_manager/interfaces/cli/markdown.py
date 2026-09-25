"""Markdown command-line adapter."""
from __future__ import annotations
import argparse,json
from repo_manager.core import invoke
from repo_manager.capabilities.markdown import MARKDOWN_FIX,MARKDOWN_GET_SECTION,MARKDOWN_HEADINGS,MARKDOWN_LINT,MARKDOWN_RENUMBER,MARKDOWN_RULES,MARKDOWN_SECTIONS
from .common import require_success

def main(argv: list[str] | None=None) -> None:
    parser=argparse.ArgumentParser()
    sub=parser.add_subparsers(dest="command",required=True)
    p=sub.add_parser("headings"); p.add_argument("path")
    p=sub.add_parser("sections"); p.add_argument("path")
    p=sub.add_parser("get-section"); p.add_argument("path"); p.add_argument("selector"); p.add_argument("--no-heading",action="store_true")
    p=sub.add_parser("lint"); p.add_argument("path")
    p=sub.add_parser("fix"); p.add_argument("path")
    sub.add_parser("rules")
    p=sub.add_parser("renumber"); p.add_argument("path"); p.add_argument("--write",action="store_true")
    args=parser.parse_args(argv)
    if args.command=="rules":
        print(json.dumps(require_success(invoke(MARKDOWN_RULES,{})),indent=2,ensure_ascii=False)); return
    if args.command=="headings":
        value=require_success(invoke(MARKDOWN_HEADINGS,{"path":args.path}))
    elif args.command=="sections":
        value=require_success(invoke(MARKDOWN_SECTIONS,{"path":args.path}))
    elif args.command=="get-section":
        value=require_success(invoke(MARKDOWN_GET_SECTION,{"path":args.path,"selector":args.selector,"no_heading":args.no_heading}))
        print(value,end=""); return
    elif args.command=="lint":
        value=require_success(invoke(MARKDOWN_LINT,{"path":args.path}))
        print(json.dumps(value,indent=2,ensure_ascii=False)); raise SystemExit(1 if value["diagnostics"] else 0)
    elif args.command=="fix":
        value=require_success(invoke(MARKDOWN_FIX,{"path":args.path}))
        print(json.dumps(value,indent=2,ensure_ascii=False)); raise SystemExit(1 if value["diagnostics"] else 0)
    else:
        value=require_success(invoke(MARKDOWN_RENUMBER,{"path":args.path,"write":args.write}))
    print(json.dumps(value,indent=2,ensure_ascii=False))
