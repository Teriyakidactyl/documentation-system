"""Assemble declared probes and mechanically derivable input-boundary cases."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Mapping
from core.operation import Operation

@dataclass(frozen=True)
class Case:
    name: str
    inputs: Mapping[str, Any]
    expected_status: str
    coverage: str
    fixture_input: str | None=None
    fixture_content: str | None=None
    fixture_suffix: str=""
    fixture_files: Mapping[str, str] | None=None
    fixture_dirs: tuple[str, ...]=()
    expected_failure_origin: str | None=None

def assemble(operation: Operation) -> tuple[Case, ...]:
    cases=[]
    for probe in operation.verification.probes:
        cases.append(Case(
            name=probe.name,inputs=dict(probe.inputs),expected_status=probe.expected_status,
            coverage="declared",fixture_input=probe.fixture_input,
            fixture_content=probe.fixture_content,fixture_suffix=probe.fixture_suffix,
            fixture_files=dict(probe.fixture_files),fixture_dirs=probe.fixture_dirs,
            expected_failure_origin=probe.expected_failure_origin,
        ))
    has_valid=any(case.expected_status=="success" for case in cases)
    path_fields=any(field.kind=="path" for field in operation.input_schema.fields)
    if not has_valid and not path_fields and operation.effects.filesystem=="none" and not operation.effects.external:
        example=operation.input_schema.example()
        if example is not None:
            cases.append(Case(name="generated-valid",inputs=example,expected_status="success",coverage="generated"))
    for name,inputs in operation.input_schema.invalid_examples():
        cases.append(Case(name=name,inputs=inputs,expected_status="failure",coverage="generated"))
    return tuple(cases)
