"""Independent common contracts evaluated by self-assembled verification."""

from __future__ import annotations

from dataclasses import dataclass

from core.operation import Operation
from core.result import Completion, Result, Status


@dataclass(frozen=True)
class Finding:
    operation: str
    case: str
    contract: str
    message: str


def result_contract(operation: Operation, case_name: str, result: Result[object]) -> tuple[Finding, ...]:
    findings: list[Finding] = []
    if not isinstance(result, Result):
        return (
            Finding(
                operation.id,
                case_name,
                "canonical-result",
                f"Observed {type(result).__name__}, expected core.result.Result.",
            ),
        )

    if result.status is Status.FAILURE:
        for failure in result.failures:
            if not failure.origin.module or not failure.origin.file or not failure.origin.symbol:
                findings.append(
                    Finding(
                        operation.id,
                        case_name,
                        "source-addressable-origin",
                        "Failure origin must include module, file, and symbol.",
                    )
                )
            if not failure.name:
                findings.append(
                    Finding(
                        operation.id,
                        case_name,
                        "local-error-identity",
                        "Failure must carry a local semantic name.",
                    )
                )

    if result.completion is Completion.PARTIAL and result.stopped_at is None:
        findings.append(
            Finding(
                operation.id,
                case_name,
                "partial-completion",
                "Partial completion must identify stopped_at.",
            )
        )
    return tuple(findings)
