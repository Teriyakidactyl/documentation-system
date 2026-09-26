"""Public repository Work Management operations."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from repo_manager.core import (
    Effects,
    ExpectedFailure,
    Failure,
    Field,
    InputSchema,
    Operation,
    Probe,
    Result,
    Source,
    Verification,
    register,
)
from .project import (
    WorkManagementError,
    reconcile_project,
    register_task,
    setup_project,
    validate_project,
)

OWNER = Source(
    "repo_manager.automation.work_management.operations",
    "d. Software/repo_manager/automation/work_management/operations.py",
)


def _root(inputs: Mapping[str, Any]) -> Path:
    root = Path(str(inputs["corpus_root"])).resolve()
    if not root.is_dir():
        raise ExpectedFailure(Failure(
            origin=OWNER,
            name="INVALID_REPOSITORY_ROOT",
            classification="invalid-input",
            subject={"corpus_root": str(root)},
            message=f"Repository root is not a directory: {root}",
        ))
    return root


def _run(inputs: Mapping[str, Any], symbol: str, function, *args) -> Result[Any]:
    root = _root(inputs)
    try:
        return Result.success(function(root, *args))
    except WorkManagementError as exc:
        raise ExpectedFailure(Failure(
            origin=Source(OWNER.module, OWNER.file, symbol),
            name="WORK_MANAGEMENT_ERROR",
            classification="invalid-project-state",
            subject={"corpus_root": str(root)},
            message=str(exc),
            details={"exception_type": type(exc).__name__},
        )) from exc


def _setup(inputs: Mapping[str, Any]) -> Result[Any]:
    return _run(inputs, "setup_project", setup_project)


def _reconcile(inputs: Mapping[str, Any]) -> Result[Any]:
    return _run(inputs, "reconcile_project", reconcile_project)


def _validate(inputs: Mapping[str, Any]) -> Result[Any]:
    return _run(inputs, "validate_project", validate_project)


def _register_task(inputs: Mapping[str, Any]) -> Result[Any]:
    return _run(inputs, "register_task", register_task, str(inputs["title"]))


SETUP = register(Operation(
    id="work_management.setup",
    commands=(("work", "setup"),),
    owner=Source(OWNER.module, OWNER.file, "setup"),
    input_schema=InputSchema((
        Field("corpus_root", "path", example="."),
    )),
    handler=_setup,
    effects=Effects(filesystem="write"),
    verification=Verification(probes=(
        Probe(name="initialize-empty-project", inputs={"corpus_root": "{tmp}"}),
    )),
))

RECONCILE = register(Operation(
    id="work_management.reconcile",
    commands=(("work", "reconcile"),),
    owner=Source(OWNER.module, OWNER.file, "reconcile"),
    input_schema=InputSchema((
        Field("corpus_root", "path", example="."),
    )),
    handler=_reconcile,
    effects=Effects(filesystem="write"),
    verification=Verification(probes=(
        Probe(name="reconcile-empty-project", inputs={"corpus_root": "{tmp}"}),
    )),
))

VALIDATE = register(Operation(
    id="work_management.validate",
    commands=(("work", "validate"),),
    owner=Source(OWNER.module, OWNER.file, "validate"),
    input_schema=InputSchema((
        Field("corpus_root", "path", example="."),
    )),
    handler=_validate,
    effects=Effects(filesystem="read"),
    verification=Verification(probes=(
        Probe(
            name="uninitialized-project",
            inputs={"corpus_root": "{tmp}"},
            expected_status="failure",
            expected_failure_origin=OWNER.file,
        ),
    )),
))

REGISTER_TASK = register(Operation(
    id="work_management.register_task",
    commands=(("work", "register-task"),),
    owner=Source(OWNER.module, OWNER.file, "register_task"),
    input_schema=InputSchema((
        Field("corpus_root", "path", example="."),
        Field("title", "string", example="Example task"),
    )),
    handler=_register_task,
    effects=Effects(filesystem="write"),
    verification=Verification(probes=(
        Probe(
            name="register-first-task",
            inputs={"corpus_root": "{tmp}", "title": "Example task"},
        ),
    )),
))
