"""Own harness discovery and symlink projection mechanics."""
from __future__ import annotations

import os
import subprocess
from pathlib import Path

from .frontmatter import FrontmatterError, load as load_frontmatter

KNOWN_SKILL_DIRS=(
    Path(".agents/skills"),
    Path(".claude/skills"),
    Path(".github/skills"),
)

class HarnessError(RuntimeError):
    """Raised when a harness projection cannot be evaluated or applied safely."""

InstallError=HarnessError

def find_repository_root(script: Path) -> Path:
    try:
        result=subprocess.run(
            ["git","-C",str(script.resolve().parent),"rev-parse","--show-toplevel"],
            check=True,capture_output=True,text=True,
        )
    except (OSError,subprocess.CalledProcessError) as exc:
        raise HarnessError("Could not determine the containing Git repository root") from exc
    root=Path(result.stdout.strip()).resolve()
    if not root.is_dir():
        raise HarnessError(f"Git repository root is not a directory: {root}")
    return root

def skill_name(source_root: Path) -> str:
    path=source_root/"SKILL.md"
    try:
        frontmatter=load_frontmatter(path)
    except FrontmatterError as exc:
        raise HarnessError(str(exc)) from exc
    if frontmatter is None:
        raise HarnessError(f"{path}: missing YAML frontmatter")
    name=frontmatter.data.get("name")
    if not isinstance(name,str) or not name.strip():
        raise HarnessError(f"{path}: frontmatter.name must be a non-empty string")
    return name.strip()

def discover_targets(host_root: Path, explicit: list[Path]) -> list[Path]:
    if explicit:
        targets=[(path if path.is_absolute() else host_root/path).resolve() for path in explicit]
    else:
        targets=[(host_root/relative).resolve() for relative in KNOWN_SKILL_DIRS if (host_root/relative).is_dir()]
    if not targets:
        raise HarnessError(
            "No harness skill directories detected. Create one of "
            ".agents/skills, .claude/skills, .github/skills, or pass --target PATH."
        )
    return sorted(set(targets),key=lambda path:path.as_posix().casefold())

def expected_target(link: Path, source_root: Path) -> Path:
    return Path(os.path.relpath(source_root,start=link.parent))

def status(link: Path, source_root: Path) -> str:
    if not link.exists() and not link.is_symlink():
        return "missing"
    if not link.is_symlink():
        return "conflict"
    try:
        resolved=link.resolve(strict=True)
    except FileNotFoundError:
        return "broken"
    return "correct" if resolved==source_root.resolve() else "wrong-target"

def install(link: Path, source_root: Path) -> str:
    state=status(link,source_root)
    if state=="correct":
        return "already correct"
    if state=="conflict":
        raise HarnessError(f"Refusing to replace non-symlink path: {link}")
    if link.is_symlink():
        link.unlink()
    link.parent.mkdir(parents=True,exist_ok=True)
    link.symlink_to(expected_target(link,source_root),target_is_directory=True)
    return "installed" if state=="missing" else "repaired"

def remove(link: Path, source_root: Path) -> str:
    state=status(link,source_root)
    if state=="missing":
        return "already absent"
    if state=="conflict":
        raise HarnessError(f"Refusing to remove non-symlink path: {link}")
    if state not in {"correct","broken","wrong-target"}:
        raise HarnessError(f"Unexpected link state for {link}: {state}")
    link.unlink()
    return "removed"

from pathlib import Path
from typing import Any, Mapping

from repo_manager.capabilities.frontmatter import FrontmatterError
from repo_manager.capabilities.yaml import YamlError
from repo_manager.core import (
    Completion, Effects, ExpectedFailure, Failure, Field, InputSchema, Operation,
    Probe, Recovery, Result, Source, Verification, invoke, register,
)

OWNER=Source("repo_manager.capabilities.harness","d. Software/repo_manager/capabilities/harness.py","project")
HARNESS=Source("repo_manager.capabilities.harness","d. Software/repo_manager/capabilities/harness.py")
FRONTMATTER=Source("repo_manager.capabilities.frontmatter","d. Software/repo_manager/capabilities/frontmatter.py","load")
YAML=Source("repo_manager.capabilities.yaml","d. Software/repo_manager/capabilities/yaml.py","parse_mapping")

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
    commands=(("harness","install"),("harness","check"),("harness","remove")),
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
