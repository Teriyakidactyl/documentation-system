"""Self-assembled verification of declared public CLI projections."""
from __future__ import annotations

from contextlib import redirect_stderr, redirect_stdout
from dataclasses import dataclass
from io import StringIO
import json
from typing import Any, Mapping

from repo_manager.core.failure import Failure
from repo_manager.core.result import Result
from repo_manager.interfaces.cli.surface import CliRoute, discover_routes

from .discovery import Surface


@dataclass(frozen=True)
class InterfaceObservation:
    exit_code: int
    stdout: str
    stderr: str
    calls: tuple[tuple[str, dict[str, Any]], ...]


def coverage_findings(surface: Surface, routes: tuple[CliRoute, ...]) -> list[str]:
    """Require every declared public command to have one executable CLI projection."""

    findings: list[str] = []
    declared: dict[tuple[str, ...], str] = {}
    for operation in surface.operations:
        for command in operation.commands:
            declared[command] = operation.id

    realized: dict[tuple[str, ...], list[CliRoute]] = {}
    for route in routes:
        realized.setdefault(route.command, []).append(route)
        if route.command not in route.operation.commands:
            findings.append(
                f"{route.operation.id}: CLI projection {' '.join(route.command)} "
                "is not declared by its operation"
            )

    for command, operation_id in sorted(declared.items()):
        matches = realized.get(command, [])
        if not matches:
            findings.append(
                f"{operation_id}: public CLI route {' '.join(command)} has no executable projection"
            )
            continue
        if len(matches) > 1:
            findings.append(
                f"{operation_id}: public CLI route {' '.join(command)} has "
                f"{len(matches)} executable projections"
            )
            continue
        if matches[0].operation.id != operation_id:
            findings.append(
                f"{operation_id}: public CLI route {' '.join(command)} is projected by "
                f"{matches[0].operation.id}"
            )

    for command, matches in sorted(realized.items()):
        if command not in declared:
            for route in matches:
                findings.append(
                    f"{route.operation.id}: executable CLI projection "
                    f"{' '.join(command)} has no semantic operation declaration"
                )
    return findings


def _run(route: CliRoute, values: Mapping[str, Any], result: Result[Any]) -> InterfaceObservation:
    calls: list[tuple[str, dict[str, Any]]] = []

    def executor(operation, inputs):
        calls.append((operation.id, dict(inputs)))
        return result

    stdout = StringIO()
    stderr = StringIO()
    exit_code = 0
    with redirect_stdout(stdout), redirect_stderr(stderr):
        try:
            route.main(route.argv(values), executor=executor)
        except SystemExit as exc:
            if exc.code is None:
                exit_code = 0
            elif isinstance(exc.code, int):
                exit_code = exc.code
            else:
                exit_code = 1
    return InterfaceObservation(
        exit_code=exit_code,
        stdout=stdout.getvalue(),
        stderr=stderr.getvalue(),
        calls=tuple(calls),
    )


def _traceback_leaked(observation: InterfaceObservation) -> bool:
    return "Traceback (most recent call last)" in observation.stdout + observation.stderr


def evaluate(route: CliRoute) -> tuple[list[str], int]:
    """Exercise parsing, operation-input projection, and generic CLI result projection."""

    findings: list[str] = []
    sample = route.operation.input_schema.example()
    if sample is None:
        return [f"{route.operation.id}: {' '.join(route.command)} has no interface sample"], 0

    expected_inputs = route.expected_inputs(sample)
    success = _run(route, sample, Result.success(route.verification.success_value))
    prefix = f"{route.operation.id}/{' '.join(route.command)}"

    if success.exit_code != 0:
        findings.append(f"{prefix}: successful Result projected exit {success.exit_code}, expected 0")
    if success.stderr:
        findings.append(f"{prefix}: successful Result wrote to stderr")
    if _traceback_leaked(success):
        findings.append(f"{prefix}: successful projection leaked a traceback")
    if len(success.calls) != 1:
        findings.append(f"{prefix}: successful projection invoked {len(success.calls)} operations, expected 1")
    elif success.calls[0] != (route.operation.id, expected_inputs):
        findings.append(
            f"{prefix}: parsed operation inputs {success.calls[0][1]!r}, "
            f"expected {expected_inputs!r}"
        )
    if route.verification.output == "json":
        try:
            json.loads(success.stdout)
        except (TypeError, json.JSONDecodeError):
            findings.append(f"{prefix}: declared JSON success projection was not valid JSON")
    elif route.verification.output not in {"text", "none"}:
        findings.append(
            f"{prefix}: unknown interface output contract {route.verification.output!r}"
        )

    failure = Failure(
        origin=route.operation.owner,
        name="VERIFICATION_FAILURE",
        classification="verification",
        subject={"operation": route.operation.id},
        message="synthetic public-interface failure",
        provenance=(route.operation.id,),
    )
    failed = _run(route, sample, Result.failure((failure,)))
    if failed.exit_code == 0:
        findings.append(f"{prefix}: failed Result projected a successful exit code")
    if not failed.stderr:
        findings.append(f"{prefix}: failed Result produced no stderr evidence")
    if _traceback_leaked(failed):
        findings.append(f"{prefix}: failed projection leaked a traceback")
    if len(failed.calls) != 1:
        findings.append(f"{prefix}: failed projection invoked {len(failed.calls)} operations, expected 1")
    elif failed.calls[0] != (route.operation.id, expected_inputs):
        findings.append(
            f"{prefix}: failure path parsed operation inputs {failed.calls[0][1]!r}, "
            f"expected {expected_inputs!r}"
        )

    return findings, 2
