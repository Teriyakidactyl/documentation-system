"""Mechanically discoverable public operation declarations."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Mapping

from .result import Result
from .source import SourceAddress

Handler = Callable[..., Result[Any]]


@dataclass(frozen=True)
class Operation:
    """Runtime declaration shared by invocation, help, and verification."""

    id: str
    owner: SourceAddress
    handler: Handler
    input_schema: Mapping[str, Any]
    effects: tuple[str, ...] = ()
    examples: tuple[Mapping[str, Any], ...] = ()
    verification: Mapping[str, Any] = field(default_factory=dict)

    def invoke(self, **inputs: Any) -> Result[Any]:
        return self.handler(**inputs)
