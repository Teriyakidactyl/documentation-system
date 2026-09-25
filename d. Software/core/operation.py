"""Discoverable public operation declarations."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable, Mapping
from .result import Result
from .schema import InputSchema
from .source import Source

Handler = Callable[[Mapping[str, Any]], Result[Any] | Any]

@dataclass(frozen=True)
class Effects:
    filesystem: str = "none"
    external: bool = False

@dataclass(frozen=True)
class Probe:
    name: str
    inputs: Mapping[str, Any] = field(default_factory=dict)
    fixture_input: str | None = None
    fixture_content: str | None = None
    fixture_suffix: str = ""
    expected_status: str = "success"
    expected_failure_origin: str | None = None

@dataclass(frozen=True)
class Verification:
    probes: tuple[Probe, ...] = ()
    dedicated: tuple[str, ...] = ()

@dataclass(frozen=True)
class Operation:
    id: str
    adapter: str
    owner: Source
    input_schema: InputSchema
    handler: Handler
    effects: Effects = Effects()
    verification: Verification = Verification()
