"""Interface-neutral YAML operation declaration."""
from __future__ import annotations
from pathlib import Path
from typing import Any, Mapping
from capabilities.yaml import YamlError, load
from core import Effects, ExpectedFailure, Failure, Field, InputSchema, Operation, Probe, Result, Source, Verification, invoke, register

OPERATION_ID="yaml.parse"
OWNER=Source("documentation_system.operations.yaml","d. Software/documentation_system/operations/yaml.py","parse")
CAPABILITY=Source("documentation_system.capabilities.yaml","d. Software/capabilities/yaml.py","load")

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
