"""Canonical repo-owned operation execution boundary."""
from __future__ import annotations
from typing import Any, Mapping
from .failure import ExpectedFailure, Failure
from .operation import Operation
from .result import Result
from .schema import SchemaError

def _attach(operation: Operation, result: Result[Any]) -> Result[Any]:
    if result.ok:
        return result
    return Result.failure(
        [failure.with_provenance(operation.id) for failure in result.failures],
        completion=result.completion, value=result.value,
        diagnostics=result.diagnostics, stopped_at=result.stopped_at,
    )

def invoke(operation: Operation, inputs: Mapping[str, Any]) -> Result[Any]:
    try:
        normalized = operation.input_schema.validate(inputs)
    except SchemaError as exc:
        return Result.failure([Failure(
            origin=operation.owner, name="INVALID_INPUT", classification="invalid-input",
            subject={"operation": operation.id}, message=str(exc),
            details={"inputs": sorted(inputs)}, provenance=(operation.id,),
        )])
    try:
        observed = operation.handler(normalized)
        result = observed if isinstance(observed, Result) else Result.success(observed)
        return _attach(operation, result)
    except ExpectedFailure as exc:
        return Result.failure([exc.failure.with_provenance(operation.id)])
    except Exception as exc:
        return Result.failure([Failure(
            origin=operation.owner, name="INTERNAL", classification="internal",
            subject={"operation": operation.id}, message=str(exc) or type(exc).__name__,
            details={"exception_type": type(exc).__name__}, provenance=(operation.id,),
        )])
