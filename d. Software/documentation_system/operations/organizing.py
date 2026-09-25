"""Interface-neutral Organizing operation declarations."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from automation.organizing.diagnostics import Diagnostic as OrganizingDiagnostic, Severity as OrganizingSeverity, annotate
from automation.organizing.engine import refresh_corpus, resolve_address
from automation.organizing.model import OrganizingError
from automation.organizing.refactor import inspect_organization, normalize_conventions
from core import Diagnostic, Effects, ExpectedFailure, Failure, Field, InputSchema, Operation, Probe, Result, Severity, Source, Verification, register

OWNER=Source("documentation_system.operations.organizing","d. Software/documentation_system/operations/organizing.py")
ENGINE=Source("automation.organizing.engine","d. Software/automation/organizing/engine.py","refresh_corpus")
REFACTOR=Source("automation.organizing.refactor","d. Software/automation/organizing/refactor.py")
MODEL=Source("automation.organizing.model","d. Software/automation/organizing/model.py")
DIAGNOSTICS=Source("automation.organizing.diagnostics","d. Software/automation/organizing/diagnostics.py","validate")

def _corpus_root(inputs: Mapping[str,Any]) -> Path:
    root=_corpus_root(inputs)
    if not root.is_dir():
        raise ExpectedFailure(Failure(
            origin=OWNER,
            name="INVALID_CORPUS_ROOT",
            classification="invalid-input",
            subject={"corpus_root":str(root)},
            message=f"Corpus root is not a directory: {root}",
        ))
    return root

def _failure(exc: OrganizingError, root: Path, symbol: str, origin: Source) -> ExpectedFailure:
    return ExpectedFailure(Failure(
        origin=Source(origin.module,origin.file,symbol),
        name="ORGANIZING_ERROR",
        classification="invalid-corpus",
        subject={"corpus_root":str(root)},
        message=str(exc),
        details={"exception_type":type(exc).__name__},
    ))

def _canonical_diagnostic(item: OrganizingDiagnostic, root: Path) -> Diagnostic:
    severity={
        OrganizingSeverity.ERROR:Severity.ERROR,
        OrganizingSeverity.WARNING:Severity.WARNING,
        OrganizingSeverity.INFO:Severity.INFO,
    }[item.severity]
    try:
        path=item.path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        path=str(item.path)
    return Diagnostic(
        code=item.code,
        severity=severity,
        message=item.message,
        subject={"path":path,"line":item.line},
        origin=DIAGNOSTICS,
    )

def _diagnostic_failure(item: OrganizingDiagnostic, root: Path) -> Failure:
    try:
        path=item.path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        path=str(item.path)
    return Failure(
        origin=DIAGNOSTICS,
        name=item.code,
        classification="validation",
        subject={"path":path,"line":item.line},
        message=item.message,
    )

def _refresh_payload(observed) -> dict[str,Any]:
    return {
        "artifacts":observed.artifacts,
        "locations":observed.locations,
        "links_refreshed":observed.links_refreshed,
        "uids_minted":observed.uids_minted,
        "diagnostics":[
            {"code":item.code,"severity":item.severity.value,"path":str(item.path),"line":item.line,"message":item.message}
            for item in observed.diagnostics
        ],
    }

def _refresh(inputs: Mapping[str,Any]) -> Result[Any]:
    root=_corpus_root(inputs)
    try:
        observed=refresh_corpus(root)
        diagnostics=tuple(_canonical_diagnostic(item,root) for item in observed.diagnostics)
        if bool(inputs["annotate"]):
            annotate(root,list(observed.diagnostics))
    except OrganizingError as exc:
        raise _failure(exc,root,"refresh_corpus",ENGINE) from exc
    payload=_refresh_payload(observed)
    failures=tuple(_diagnostic_failure(item,root) for item in observed.diagnostics if item.severity is OrganizingSeverity.ERROR)
    if failures:
        return Result.failure(failures,value=payload,diagnostics=diagnostics)
    return Result.success(payload,diagnostics=diagnostics)

def _inspect(inputs: Mapping[str,Any]) -> Result[Any]:
    root=_corpus_root(inputs)
    try:
        return Result.success(inspect_organization(root))
    except OrganizingError as exc:
        raise _failure(exc,root,"inspect_organization",REFACTOR) from exc

def _resolve(inputs: Mapping[str,Any]) -> Result[Any]:
    root=_corpus_root(inputs)
    try:
        return Result.success(resolve_address(root,str(inputs["address"])))
    except OrganizingError as exc:
        raise _failure(exc,root,"resolve_address",ENGINE) from exc

def _normalize(inputs: Mapping[str,Any]) -> Result[Any]:
    root=_corpus_root(inputs)
    apply=bool(inputs["apply"])
    try:
        payload=normalize_conventions(root,apply=apply)
        if apply and payload.get("applied"):
            observed=refresh_corpus(root)
            payload=dict(payload)
            payload["refresh"]=_refresh_payload(observed)
            diagnostics=tuple(_canonical_diagnostic(item,root) for item in observed.diagnostics)
            failures=tuple(_diagnostic_failure(item,root) for item in observed.diagnostics if item.severity is OrganizingSeverity.ERROR)
            if failures:
                return Result.failure(failures,value=payload,diagnostics=diagnostics)
            return Result.success(payload,diagnostics=diagnostics)
        return Result.success(payload)
    except OrganizingError as exc:
        raise _failure(exc,root,"normalize_conventions",REFACTOR) from exc

REFRESH=register(Operation(
    id="organizing.refresh",
    commands=(("organizing","refresh"),),
    owner=Source(OWNER.module,OWNER.file,"refresh"),
    input_schema=InputSchema((
        Field("corpus_root","path",example="."),
        Field("annotate","boolean",required=False,default=False),
    )),
    handler=_refresh,
    effects=Effects(filesystem="write"),
    verification=Verification(probes=(
        Probe(name="missing-corpus",inputs={"corpus_root":"{tmp}/missing","annotate":False},expected_status="failure",expected_failure_origin=OWNER.file),
    )),
))

INSPECT=register(Operation(
    id="organizing.inspect",
    commands=(("organizing","inspect"),),
    owner=Source(OWNER.module,OWNER.file,"inspect"),
    input_schema=InputSchema((Field("corpus_root","path",example="."),)),
    handler=_inspect,
    effects=Effects(filesystem="read"),
    verification=Verification(probes=(
        Probe(name="missing-corpus",inputs={"corpus_root":"{tmp}/missing"},expected_status="failure",expected_failure_origin=OWNER.file),
    )),
))

RESOLVE=register(Operation(
    id="organizing.resolve",
    commands=(("organizing","resolve"),),
    owner=Source(OWNER.module,OWNER.file,"resolve"),
    input_schema=InputSchema((
        Field("corpus_root","path",example="."),
        Field("address","string",example="documentation-system:§1"),
    )),
    handler=_resolve,
    effects=Effects(filesystem="read"),
    verification=Verification(probes=(
        Probe(name="missing-corpus",inputs={"corpus_root":"{tmp}/missing","address":"documentation-system:§1"},expected_status="failure",expected_failure_origin=OWNER.file),
    )),
))

NORMALIZE=register(Operation(
    id="organizing.normalize",
    commands=(("organizing","normalize"),),
    owner=Source(OWNER.module,OWNER.file,"normalize"),
    input_schema=InputSchema((
        Field("corpus_root","path",example="."),
        Field("apply","boolean",required=False,default=False),
    )),
    handler=_normalize,
    effects=Effects(filesystem="write"),
    verification=Verification(probes=(
        Probe(name="missing-corpus",inputs={"corpus_root":"{tmp}/missing","apply":False},expected_status="failure",expected_failure_origin=OWNER.file),
    )),
))
