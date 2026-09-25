"""Derive safe baseline cases from canonical operation declarations."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from core.operation import Operation


@dataclass(frozen=True)
class Case:
    operation: Operation
    name: str
    inputs: Mapping[str, Any]
    expected_status: str
    source: str


def assemble(operation: Operation) -> tuple[Case, ...]:
    cases: list[Case] = []
    if operation.examples:
        cases.append(
            Case(
                operation=operation,
                name="example",
                inputs=dict(operation.examples[0]),
                expected_status="success",
                source="operation example",
            )
        )

    schema = operation.input_schema
    properties = schema.get("properties", {})
    example = dict(operation.examples[0]) if operation.examples else {}

    for required in schema.get("required", ()):
        if required in example:
            invalid = dict(example)
            invalid.pop(required)
            cases.append(
                Case(
                    operation=operation,
                    name=f"missing:{required}",
                    inputs=invalid,
                    expected_status="failure",
                    source="required input contract",
                )
            )

    for name, declaration in properties.items():
        allowed = declaration.get("enum")
        if allowed is not None and name in example:
            invalid = dict(example)
            invalid[name] = "__self_assembling_invalid_value__"
            cases.append(
                Case(
                    operation=operation,
                    name=f"invalid-enum:{name}",
                    inputs=invalid,
                    expected_status="failure",
                    source="enum input contract",
                )
            )

    if schema.get("additionalProperties") is False and example:
        invalid = dict(example)
        invalid["__unknown__"] = True
        cases.append(
            Case(
                operation=operation,
                name="unknown-input",
                inputs=invalid,
                expected_status="failure",
                source="closed input contract",
            )
        )

    return tuple(cases)
