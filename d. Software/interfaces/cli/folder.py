"""Folder command interfaces and discoverable operation declarations."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Mapping

from capabilities.folder import FolderError, Rename, apply, plan_strip_prefix, validate
from core import (
    Effects, ExpectedFailure, Failure, Field, InputSchema, Operation, Probe,
    Result, Source, Verification, invoke, register,
)
from ._common import require_success

OWNER=Source("documentation_system.interfaces.cli.folder","d. Software/interfaces/cli/folder.py")
CAPABILITY=Source("documentation_system.capabilities.folder","d. Software/capabilities/folder.py")

def _failure(exc: FolderError, subject: Mapping[str, Any], symbol: str) -> ExpectedFailure:
    return ExpectedFailure(Failure(
        origin=Source(CAPABILITY.module,CAPABILITY.file,symbol),
        name="FOLDER_ERROR",
        classification="unsafe-mutation",
        subject=dict(subject),
        message=str(exc),
        details={"exception_type":type(exc).__name__},
    ))

def _rename(inputs: Mapping[str, Any]) -> Result[Any]:
    source=Path(str(inputs["source"])).resolve()
    destination=Path(str(inputs["destination"])).absolute()
    rename=Rename(source,destination)
    try:
        validate([rename])
        payload={
            "operation":"rename",
            "renames":[{"from":str(rename.source),"to":str(rename.destination)}],
            "applied":False,
        }
        if bool(inputs["apply"]):
            apply([rename])
            payload["applied"]=True
        return Result.success(payload)
    except FolderError as exc:
        raise _failure(exc,{"source":str(source),"destination":str(destination)},"validate") from exc

def _strip_prefix(inputs: Mapping[str, Any]) -> Result[Any]:
    root=Path(str(inputs["root"])).resolve()
    files_only=bool(inputs["files_only"])
    folders_only=bool(inputs["folders_only"])
    if files_only and folders_only:
        raise ExpectedFailure(Failure(
            origin=OWNER,
            name="INVALID_PATH_KIND_SELECTION",
            classification="invalid-input",
            subject={"operation":"folder.strip-prefix"},
            message="files_only and folders_only are mutually exclusive",
        ))
    try:
        plan=plan_strip_prefix(
            root,
            str(inputs["match"]),
            include_files=not folders_only,
            include_directories=not files_only,
            name_glob=(str(inputs["include"]) or None),
        )
        payload={
            "operation":"strip-prefix",
            "root":str(root),
            "match":str(inputs["match"]),
            "include":str(inputs["include"]) or None,
            "path_kinds":"files" if files_only else "folders" if folders_only else "files-and-folders",
            "renames":[
                {
                    "from":item.source.relative_to(root).as_posix(),
                    "to":item.destination.relative_to(root).as_posix(),
                }
                for item in plan
            ],
            "applied":False,
        }
        if bool(inputs["apply"]):
            apply(plan)
            payload["applied"]=True
        return Result.success(payload)
    except FolderError as exc:
        raise _failure(exc,{"root":str(root),"match":str(inputs["match"])},"plan_strip_prefix") from exc

FOLDER_RENAME=register(Operation(
    id="folder.rename",
    adapter="Folder.py",
    owner=Source(OWNER.module,OWNER.file,"rename"),
    input_schema=InputSchema((
        Field("source","path",example="source.txt"),
        Field("destination","path",example="destination.txt"),
        Field("apply","boolean",required=False,default=False),
    )),
    handler=_rename,
    effects=Effects(filesystem="write"),
    verification=Verification(probes=(
        Probe(
            name="preview-sibling-rename",
            inputs={"source":"{tmp}/source.txt","destination":"{tmp}/destination.txt","apply":False},
            fixture_files={"source.txt":"content\n"},
        ),
    )),
))

FOLDER_STRIP_PREFIX=register(Operation(
    id="folder.strip-prefix",
    adapter="Folder.py",
    owner=Source(OWNER.module,OWNER.file,"strip_prefix"),
    input_schema=InputSchema((
        Field("root","path",example="root"),
        Field("match","string",example="^[0-9]+ "),
        Field("include","string",required=False,default=""),
        Field("files_only","boolean",required=False,default=False),
        Field("folders_only","boolean",required=False,default=False),
        Field("apply","boolean",required=False,default=False),
    )),
    handler=_strip_prefix,
    effects=Effects(filesystem="write"),
    verification=Verification(probes=(
        Probe(
            name="preview-prefix-strip",
            inputs={
                "root":"{tmp}/root","match":"^[0-9]+ ","include":"",
                "files_only":False,"folders_only":False,"apply":False,
            },
            fixture_files={"root/1 One.txt":"one\n","root/Two.txt":"two\n"},
        ),
    )),
))

def _single_rename(argv: list[str]) -> None:
    parser=argparse.ArgumentParser(
        prog=Path(sys.argv[0]).name,
        description="Preview or apply one collision-safe sibling rename.",
    )
    parser.add_argument("--apply",action="store_true")
    parser.add_argument("source",type=Path)
    parser.add_argument("destination",type=Path)
    args=parser.parse_args(argv)
    value=require_success(invoke(FOLDER_RENAME,{
        "source":str(args.source),"destination":str(args.destination),"apply":args.apply,
    }))
    print(json.dumps(value,indent=2,ensure_ascii=False))

def _strip(argv: list[str]) -> None:
    parser=argparse.ArgumentParser(
        prog=f"{Path(sys.argv[0]).name} strip-prefix",
        description="Recursively strip exactly the basename prefix consumed by a successful regular-expression match.",
    )
    parser.add_argument("root",type=Path)
    parser.add_argument("--match",required=True)
    parser.add_argument("--include",dest="name_glob")
    kind=parser.add_mutually_exclusive_group()
    kind.add_argument("--files-only",action="store_true")
    kind.add_argument("--folders-only",action="store_true")
    parser.add_argument("--apply",action="store_true")
    args=parser.parse_args(argv)
    value=require_success(invoke(FOLDER_STRIP_PREFIX,{
        "root":str(args.root),"match":args.match,"include":args.name_glob or "",
        "files_only":args.files_only,"folders_only":args.folders_only,"apply":args.apply,
    }))
    print(json.dumps(value,indent=2,ensure_ascii=False))

def main(argv: list[str] | None=None) -> None:
    argv=list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0]=="strip-prefix":
        _strip(argv[1:])
    else:
        _single_rename(argv)

if __name__=="__main__":
    main()
