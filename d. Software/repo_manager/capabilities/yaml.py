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

from pathlib import Path
from typing import Any, Mapping
from repo_manager.core import Effects, ExpectedFailure, Failure, Field, InputSchema, Operation, Probe, Result, Source, Verification, invoke, register

OPERATION_ID="yaml.parse"
OWNER=Source("repo_manager.capabilities.yaml","d. Software/repo_manager/capabilities/yaml.py","parse")
CAPABILITY=Source("repo_manager.capabilities.yaml","d. Software/repo_manager/capabilities/yaml.py","load")

def _handler(inputs: Mapping[str, Any]) -> Result[Any]:
    path=Path(str(inputs["path"]))
    try:
        return Result.success(load(path))
    except YamlError as exc:
        raise ExpectedFailure(Failure(
            origin=CAPABILITY,
            name="YAML_ERROR",
            classification="malformed-or-unreadable",
            subject={"path":str(path)},
            message=str(exc),
            details={"exception_type":type(exc).__name__},
        )) from exc

OPERATION=register(Operation(
    id=OPERATION_ID,
    commands=(("yaml","parse"),),
    owner=OWNER,
    input_schema=InputSchema((Field("path","path",example="fixture.yaml"),)),
    handler=_handler,
    effects=Effects(filesystem="read"),
    verification=Verification(probes=(
        Probe(name="valid-yaml",fixture_input="path",fixture_content="key: value\n",fixture_suffix=".yaml"),
        Probe(name="malformed-yaml",fixture_input="path",fixture_content="key: [\n",fixture_suffix=".yaml",expected_status="failure",expected_failure_origin=CAPABILITY.file),
    )),
))
