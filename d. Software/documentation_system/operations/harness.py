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

OWNER=Source("documentation_system.operations.harness","d. Software/documentation_system/operations/harness.py","project")
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
