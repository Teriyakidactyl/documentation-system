"""Runtime registry for mechanically discoverable Software operations."""

from __future__ import annotations

from .operation import Operation

_OPERATIONS: dict[str, Operation] = {}


def register(operation: Operation) -> Operation:
    existing = _OPERATIONS.get(operation.id)
    if existing is not None and existing is not operation:
        raise ValueError(f"duplicate Software operation id: {operation.id}")
    _OPERATIONS[operation.id] = operation
    return operation


def operations() -> tuple[Operation, ...]:
    return tuple(_OPERATIONS[key] for key in sorted(_OPERATIONS))


def get(operation_id: str) -> Operation:
    try:
        return _OPERATIONS[operation_id]
    except KeyError as exc:
        raise KeyError(f"unknown Software operation: {operation_id}") from exc
