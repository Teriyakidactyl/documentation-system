"""Canonical invocation boundary for declared Software operations."""

from __future__ import annotations

from typing import Any, Mapping

from .failure import Failure
from .operation import Operation
from .result import Result
from .source import SourceAddress

_ORIGIN = SourceAddress(
    module="core.execution",
    file="d. Software/core/execution.py",
    symbol="execute",
)


def _failure(operation: Operation, name: str, message: str, **details: Any) -> Result[Any]:
    return Result.failure(
        Failure(
            origin=_ORIGIN,
            name=name,
            classification="malformed",
            subject={"operation": operation.id},
            message=message,
            details=details,
        )
    )


def _matches_type(value: Any, declared: str) -> bool:
    if declared == "string":
        return isinstance(value, str)
    if declared == "boolean":
        return isinstance(value, bool)
    if declared == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if declared == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if declared == "object":
        return isinstance(value, Mapping)
    if declared == "array":
        return isinstance(value, (list, tuple))
    return True


def execute(operation: Operation, inputs: Mapping[str, Any]) -> Result[Any]:
    """Validate a declared input shape and invoke the real operation handler."""

    schema = operation.input_schema
    properties = schema.get("properties", {})
    required = tuple(schema.get("required", ()))

    missing = [name for name in required if name not in inputs]
    if missing:
        return _failure(
            operation,
            "REQUIRED_INPUT_MISSING",
            "Required operation input is absent.",
            missing=missing,
        )

    if schema.get("additionalProperties") is False:
        unknown = sorted(set(inputs) - set(properties))
        if unknown:
            return _failure(
                operation,
                "UNKNOWN_INPUT",
                "Operation input contains undeclared fields.",
                unknown=unknown,
            )

    for name, value in inputs.items():
        declaration = properties.get(name)
        if declaration is None:
            continue
        declared_type = declaration.get("type")
        if declared_type and not _matches_type(value, declared_type):
            return _failure(
                operation,
                "INVALID_INPUT_TYPE",
                f"Operation input {name!r} has the wrong type.",
                field=name,
                expected=declared_type,
                observed=type(value).__name__,
            )
        allowed = declaration.get("enum")
        if allowed is not None and value not in allowed:
            return _failure(
                operation,
                "INVALID_INPUT_VALUE",
                f"Operation input {name!r} is outside the declared values.",
                field=name,
                allowed=list(allowed),
                observed=value,
            )

    return operation.invoke(**dict(inputs))
