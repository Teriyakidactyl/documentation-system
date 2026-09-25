"""Own generic YAML parsing and deterministic serialization."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from core.failure import Failure
from core.operation import Operation
from core.registry import register
from core.result import Result
from core.source import SourceAddress


class YamlError(ValueError):
    """Raised when YAML cannot be parsed or does not satisfy the requested shape."""


def parse(text: str) -> Any:
    try:
        return yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise YamlError(str(exc)) from exc


def parse_mapping(text: str) -> dict:
    data = parse(text)
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise YamlError("YAML value must be a mapping")
    return data


def serialize(value: Any) -> str:
    return yaml.safe_dump(value, sort_keys=False, allow_unicode=True)


def load(path: Path) -> Any:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise YamlError(f"Can't read {path}: {exc}") from exc
    return parse(text)


_PARSE_ORIGIN = SourceAddress(
    module="_capabilities.yaml",
    file="d. Software/_capabilities/yaml.py",
    symbol="parse",
)


def _parse_operation(*, text: str) -> Result[Any]:
    try:
        return Result.success(parse(text))
    except YamlError as exc:
        return Result.failure(
            Failure(
                origin=_PARSE_ORIGIN,
                name="MALFORMED",
                classification="malformed",
                message=str(exc),
            )
        )


PARSE_OPERATION = register(
    Operation(
        id="yaml.parse",
        owner=_PARSE_ORIGIN,
        handler=_parse_operation,
        input_schema={
            "type": "object",
            "required": ["text"],
            "properties": {"text": {"type": "string"}},
            "additionalProperties": False,
        },
        examples=({"text": "key: value\n"},),
        verification={"generated": True},
    )
)
