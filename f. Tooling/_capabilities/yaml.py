"""Own generic YAML parsing and deterministic serialization."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


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
