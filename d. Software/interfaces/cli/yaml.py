"""YAML command interface and discoverable operation declaration."""
from __future__ import annotations
import json
from pathlib import Path
import sys
from typing import Any, Mapping
from capabilities.yaml import YamlError, load
from core import Effects, ExpectedFailure, Failure, Field, InputSchema, Operation, Probe, Result, Source, Verification, invoke, register
from ._common import require_success

OPERATION_ID="yaml.parse"
OWNER=Source("documentation_system.interfaces.cli.yaml","d. Software/interfaces/cli/yaml.py","parse")
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
    adapter="YAML.py",
    owner=OWNER,
    input_schema=InputSchema((Field("path","path",example="fixture.yaml"),)),
    handler=_handler,
    effects=Effects(filesystem="read"),
    verification=Verification(probes=(
        Probe(name="valid-yaml",fixture_input="path",fixture_content="key: value\n",fixture_suffix=".yaml"),
        Probe(name="malformed-yaml",fixture_input="path",fixture_content="key: [\n",fixture_suffix=".yaml",expected_status="failure",expected_failure_origin=CAPABILITY.file),
    )),
))

def main(argv: list[str] | None=None) -> None:
    argv=list(sys.argv[1:] if argv is None else argv)
    if len(argv)!=1:
        raise SystemExit(f"Usage: {Path(sys.argv[0]).name} PATH")
    value=require_success(invoke(OPERATION,{"path":argv[0]}))
    print(json.dumps(value,indent=2,ensure_ascii=False))

if __name__=="__main__":
    main()
