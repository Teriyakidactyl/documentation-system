"""Consumer projections of canonical Software results."""

from __future__ import annotations

from typing import Any

from .result import Result


def result_dict(result: Result[Any]) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "status": result.status.value,
        "completion": result.completion.value,
        "value": result.value,
        "diagnostics": [
            item.to_dict() if hasattr(item, "to_dict") else item
            for item in result.diagnostics
        ],
        "failures": [failure.to_dict() for failure in result.failures],
    }
    if result.stopped_at is not None:
        payload["stopped_at"] = result.stopped_at
    return payload
