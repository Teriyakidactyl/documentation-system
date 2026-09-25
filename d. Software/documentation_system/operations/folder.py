"""Interface-neutral Folder operation declarations."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from capabilities.folder import FolderError, Rename, apply, plan_strip_prefix, validate
from core import (
    Effects, ExpectedFailure, Failure, Field, InputSchema, Operation, Probe,
    Result, Source, Verification, invoke, register,
)

OWNER=Source("documentation_system.operations.folder","d. Software/documentation_system/operations/folder.py")
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
    commands=(("folder","rename"),),
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
    commands=(("folder","strip-prefix"),),
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
