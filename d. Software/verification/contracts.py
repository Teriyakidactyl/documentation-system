"""Independent common contracts applied to observed operation results."""
from __future__ import annotations
from core.operation import Operation
from core.result import Result
from .cases import Case

def evaluate(operation: Operation, case: Case, result: Result) -> list[str]:
    findings=[]
    if result.status.value!=case.expected_status:
        findings.append(f"{operation.id}/{case.name}: expected status {case.expected_status}, observed {result.status.value}")
    if result.failures:
        expected=tuple(sorted(result.failures,key=lambda item:item.canonical_key()))
        if result.failures!=expected:
            findings.append(f"{operation.id}/{case.name}: failures are not deterministic")
        for failure in result.failures:
            if not failure.origin.module or not failure.origin.file:
                findings.append(f"{operation.id}/{case.name}: failure lacks source-addressable origin")
            if not failure.name or not failure.classification or not failure.message:
                findings.append(f"{operation.id}/{case.name}: failure identity is incomplete")
            if not failure.provenance or failure.provenance[-1]!=operation.id:
                findings.append(f"{operation.id}/{case.name}: operation provenance was not preserved")
    if case.expected_failure_origin is not None:
        observed=result.failures[0].origin.file if result.failures else None
        if observed!=case.expected_failure_origin:
            findings.append(f"{operation.id}/{case.name}: expected failure origin {case.expected_failure_origin}, observed {observed}")
    return findings
