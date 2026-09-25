"""Assemble and execute baseline verification for the current operation surface."""

from __future__ import annotations

from dataclasses import dataclass

from core.execution import execute

from .cases import assemble
from .contracts import Finding, result_contract
from .discovery import discover


@dataclass(frozen=True)
class VerificationReport:
    operations: int
    boundary_verified: int
    generated_operations: int
    cases: int
    gaps: tuple[str, ...]
    findings: tuple[Finding, ...]

    @property
    def passed(self) -> bool:
        return not self.findings and not self.gaps


def verify() -> VerificationReport:
    operation_set = discover()
    findings: list[Finding] = []
    gaps: list[str] = []
    boundary_verified = 0
    generated_operations = 0
    case_count = 0

    for operation in operation_set:
        cases = assemble(operation)
        if not cases:
            gaps.append(operation.id)
            continue
        generated_operations += 1
        operation_reached_boundary = False
        for case in cases:
            result = execute(operation, case.inputs)
            case_count += 1
            operation_reached_boundary = True
            if result.status.value != case.expected_status:
                findings.append(
                    Finding(
                        operation.id,
                        case.name,
                        "expected-status",
                        f"Expected {case.expected_status}, observed {result.status.value}.",
                    )
                )
            findings.extend(result_contract(operation, case.name, result))
        boundary_verified += int(operation_reached_boundary)

    return VerificationReport(
        operations=len(operation_set),
        boundary_verified=boundary_verified,
        generated_operations=generated_operations,
        cases=case_count,
        gaps=tuple(sorted(gaps)),
        findings=tuple(findings),
    )
