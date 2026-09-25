"""Runtime operation registry used by interfaces and verification."""
from __future__ import annotations
from .operation import Operation

_OPERATIONS: dict[str, Operation] = {}

def register(operation: Operation) -> Operation:
    existing = _OPERATIONS.get(operation.id)
    if existing is not None and existing is not operation:
        raise ValueError(f"Duplicate operation id: {operation.id}")
    _OPERATIONS[operation.id] = operation
    return operation

def all_operations() -> tuple[Operation, ...]:
    return tuple(_OPERATIONS[key] for key in sorted(_OPERATIONS))
