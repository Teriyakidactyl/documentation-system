"""Interface-neutral Frontmatter operation declaration."""
from __future__ import annotations
from pathlib import Path
from typing import Any, Mapping
from capabilities.frontmatter import FrontmatterError, load
from capabilities.yaml import YamlError
from core import Effects, ExpectedFailure, Failure, Field, InputSchema, Operation, Probe, Result, Source, Verification, invoke, register

OPERATION_ID="frontmatter.inspect"
OWNER=Source("documentation_system.operations.frontmatter","d. Software/documentation_system/operations/frontmatter.py","inspect")
FRONTMATTER=Source("documentation_system.capabilities.frontmatter","d. Software/capabilities/frontmatter.py","load")
YAML=Source("documentation_system.capabilities.yaml","d. Software/capabilities/yaml.py","parse_mapping")

def _handler(inputs: Mapping[str, Any]) -> Result[Any]:
    path=Path(str(inputs["path"]))
    try:
        value=load(path)
    except FrontmatterError as exc:
        cause=exc.__cause__
        origin=YAML if isinstance(cause,YamlError) else FRONTMATTER
        raise ExpectedFailure(Failure(
            origin=origin,
            name="YAML_ERROR" if origin is YAML else "FRONTMATTER_ERROR",
            classification="malformed" if origin is YAML else "invalid-frontmatter",
            subject={"path":str(path)},
            message=str(exc),
            details={"exception_type":type(exc).__name__},
            provenance=("frontmatter.load",) if origin is YAML else (),
        )) from exc
    if value is None:
        raise ExpectedFailure(Failure(
            origin=FRONTMATTER,
            name="NO_FRONTMATTER",
            classification="not-found",
            subject={"path":str(path)},
            message="no supported frontmatter surface found",
        ))
    return Result.success({"kind":value.kind,"start_line":value.start_line,"data":value.data})

OPERATION=register(Operation(
    id=OPERATION_ID,
    commands=(("frontmatter","inspect"),),
    owner=OWNER,
    input_schema=InputSchema((Field("path","path",example="fixture.md"),)),
    handler=_handler,
    effects=Effects(filesystem="read"),
    verification=Verification(probes=(
        Probe(name="valid-frontmatter",fixture_input="path",fixture_content="---\nname: example\n---\n# Body\n",fixture_suffix=".md"),
        Probe(name="malformed-frontmatter-yaml",fixture_input="path",fixture_content="---\nname: [\n---\n# Body\n",fixture_suffix=".md",expected_status="failure",expected_failure_origin=YAML.file),
    )),
))
