"""Harness projection CLI and discoverable operation declaration."""
from __future__ import annotations

import argparse
from pathlib import Path
import sys
from typing import Any, Mapping

from capabilities.frontmatter import FrontmatterError
from capabilities.harness import HarnessError, discover_targets, find_repository_root, install, remove, skill_name, status
from capabilities.yaml import YamlError
from core import (
    Completion, Effects, ExpectedFailure, Failure, Field, InputSchema, Operation,
    Probe, Recovery, Result, Source, Verification, invoke, register,
)

OWNER=Source("documentation_system.interfaces.cli.harness","d. Software/interfaces/cli/harness.py","project")
HARNESS=Source("documentation_system.capabilities.harness","d. Software/capabilities/harness.py")
FRONTMATTER=Source("documentation_system.capabilities.frontmatter","d. Software/capabilities/frontmatter.py","load")
YAML=Source("documentation_system.capabilities.yaml","d. Software/capabilities/yaml.py","parse_mapping")

def _cause_chain(exc: BaseException):
    current=exc
    while current is not None:
        yield current
        current=current.__cause__

def _outer_failure(exc: BaseException, subject: Mapping[str,Any]) -> ExpectedFailure:
    chain=list(_cause_chain(exc))
    if any(isinstance(item,YamlError) for item in chain):
        origin=YAML; name="YAML_ERROR"; classification="malformed"; provenance=("frontmatter.load","harness.skill_name")
    elif any(isinstance(item,FrontmatterError) for item in chain):
        origin=FRONTMATTER; name="FRONTMATTER_ERROR"; classification="invalid-frontmatter"; provenance=("harness.skill_name",)
    else:
        origin=Source(HARNESS.module,HARNESS.file,"discover_targets")
        name="HARNESS_ERROR"; classification="invalid-harness-state"; provenance=()
    return ExpectedFailure(Failure(
        origin=origin,name=name,classification=classification,subject=dict(subject),
        message=str(exc),details={"exception_type":type(exc).__name__},provenance=provenance,
    ))

def _state_failure(link: Path, state: str) -> Failure:
    recovery=()
    if state in {"missing","broken","wrong-target"}:
        recovery=(Recovery("harness.install",{"target":str(link.parent)}),)
    return Failure(
        origin=Source(HARNESS.module,HARNESS.file,"status"),
        name=f"HARNESS_{state.replace('-','_').upper()}",
        classification="state-mismatch",
        subject={"link":str(link),"state":state},
        message=f"Harness projection is {state}: {link}",
        recovery=recovery,
    )

def _handler(inputs: Mapping[str,Any]) -> Result[Any]:
    source_root=Path(str(inputs["source_root"])).resolve()
    host_root=Path(str(inputs["host_root"])).resolve()
    mode=str(inputs["mode"])
    explicit=[Path(str(value)) for value in inputs["targets"]]
    if not source_root.is_dir():
        raise ExpectedFailure(Failure(
            origin=OWNER,name="INVALID_SOURCE_ROOT",classification="invalid-input",
            subject={"source_root":str(source_root)},message=f"Source root is not a directory: {source_root}",
        ))
    if not host_root.is_dir():
        raise ExpectedFailure(Failure(
            origin=OWNER,name="INVALID_HOST_ROOT",classification="invalid-input",
            subject={"host_root":str(host_root)},message=f"Host root is not a directory: {host_root}",
        ))
    try:
        name=skill_name(source_root)
        targets=discover_targets(host_root,explicit)
    except HarnessError as exc:
        raise _outer_failure(exc,{"source_root":str(source_root),"host_root":str(host_root)}) from exc

    rows=[]
    failures=[]
    completed=0
    for skills_dir in targets:
        link=skills_dir/name
        if mode=="check":
            state=status(link,source_root)
            rows.append({"state":state,"link":str(link)})
            if state!="correct":
                failures.append(_state_failure(link,state))
            else:
                completed+=1
            continue
        try:
            action=remove(link,source_root) if mode=="remove" else install(link,source_root)
            rows.append({"state":action,"link":str(link)})
            completed+=1
        except HarnessError as exc:
            failures.append(Failure(
                origin=Source(HARNESS.module,HARNESS.file,mode),
                name="HARNESS_ERROR",
                classification="unsafe-mutation",
                subject={"link":str(link),"mode":mode},
                message=str(exc),
                details={"exception_type":type(exc).__name__},
            ))

    value={"mode":mode,"source_root":str(source_root),"host_root":str(host_root),"results":rows}
    if failures:
        completion=Completion.PARTIAL if completed else Completion.COMPLETE
        return Result.failure(failures,completion=completion,value=value)
    return Result.success(value)

HARNESS_PROJECT=register(Operation(
    id="harness.project",
    adapter="Harness Installer.py",
    owner=OWNER,
    input_schema=InputSchema((
        Field("source_root","path",example="source"),
        Field("host_root","path",example="host"),
        Field("mode","string",required=False,default="install",enum=("install","check","remove")),
        Field("targets","array",required=False,default=[]),
    )),
    handler=_handler,
    effects=Effects(filesystem="write"),
    verification=Verification(probes=(
        Probe(
            name="install-projection",
            inputs={"source_root":"{tmp}/source","host_root":"{tmp}/host","mode":"install","targets":[]},
            fixture_files={"source/SKILL.md":"---\nname: documentation-system\n---\n# Skill\n"},
            fixture_dirs=("host/.agents/skills",),
        ),
        Probe(
            name="check-missing-projection",
            inputs={"source_root":"{tmp}/source","host_root":"{tmp}/host","mode":"check","targets":[]},
            fixture_files={"source/SKILL.md":"---\nname: documentation-system\n---\n# Skill\n"},
            fixture_dirs=("host/.agents/skills",),
            expected_status="failure",
            expected_failure_origin=HARNESS.file,
        ),
    )),
))

def main(script: Path | None=None, argv: list[str] | None=None) -> None:
    script=script or Path(sys.argv[0]).resolve()
    argv=list(sys.argv[1:] if argv is None else argv)
    mode="install"
    targets=[]
    positional=[]
    i=0
    while i<len(argv):
        arg=argv[i]
        if arg=="--check":
            mode="check"; i+=1
        elif arg=="--remove":
            mode="remove"; i+=1
        elif arg=="--target":
            if i+1>=len(argv):
                raise SystemExit("--target requires a path")
            targets.append(argv[i+1]); i+=2
        elif arg in {"-h","--help"}:
            parser=argparse.ArgumentParser(prog=script.name)
            parser.add_argument("--check",action="store_true")
            parser.add_argument("--remove",action="store_true")
            parser.add_argument("--target",action="append")
            parser.add_argument("host_root",nargs="?")
            parser.print_help(); return
        else:
            positional.append(arg); i+=1
    if len(positional)>1:
        raise SystemExit("Expected at most one host_root argument")
    try:
        source_root=find_repository_root(script)
    except HarnessError as exc:
        failure=_outer_failure(exc,{"script":str(script)}).failure.with_provenance("harness.project")
        from core.projection import json_text
        print(json_text(Result.failure([failure])),file=sys.stderr)
        raise SystemExit(1)
    host_root=Path(positional[0]).resolve() if positional else Path.cwd().resolve()
    result=invoke(HARNESS_PROJECT,{
        "source_root":str(source_root),"host_root":str(host_root),"mode":mode,"targets":targets,
    })
    if result.value:
        for row in result.value["results"]:
            print(f"{row['state']:12} {row['link']}")
    if not result.ok:
        from core.projection import json_text
        print(json_text(result),file=sys.stderr)
        raise SystemExit(1)

if __name__=="__main__":
    main()
