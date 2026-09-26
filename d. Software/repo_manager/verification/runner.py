"""Local and CI entry point for self-assembled Software verification."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import tempfile

from repo_manager.core.execution import invoke
from repo_manager.interfaces.cli.surface import discover_routes

from .architecture import dependency_findings
from .cases import assemble
from .contracts import evaluate
from .coverage import coverage_findings
from .discovery import discover
from .interface import coverage_findings as interface_coverage_findings
from .interface import evaluate as evaluate_interface


def _replace_tmp(value, directory: Path):
    if isinstance(value, str):
        return value.replace("{tmp}", str(directory))
    if isinstance(value, list):
        return [_replace_tmp(item, directory) for item in value]
    if isinstance(value, dict):
        return {key: _replace_tmp(item, directory) for key, item in value.items()}
    return value


def _materialize(case, directory: Path) -> dict:
    for relative in case.fixture_dirs:
        (directory / relative).mkdir(parents=True, exist_ok=True)
    for relative, content in (case.fixture_files or {}).items():
        path = directory / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    values = {key: _replace_tmp(value, directory) for key, value in case.inputs.items()}
    if case.fixture_input is not None:
        path = directory / f"fixture{case.fixture_suffix}"
        path.write_text(case.fixture_content or "", encoding="utf-8")
        values[case.fixture_input] = str(path)
    return values


def _summary(
    surface,
    routes,
    findings: list[str],
    *,
    operation_executed: int = 0,
    interface_executed: int = 0,
) -> str:
    lines = [
        "## Software verification",
        "",
        f"- public operations: {len(surface.operations)}",
        f"- declared public CLI routes: {len(surface.commands)}",
        f"- executable CLI projections: {len(routes)}",
        f"- operation cases executed: {operation_executed}",
        f"- interface projection cases executed: {interface_executed}",
        f"- findings: {len(findings)}",
    ]
    if findings:
        lines.extend(["", "### Findings", *[f"- {item}" for item in findings]])
    return "\n".join(lines) + "\n"


def _emit_summary(value: str) -> None:
    print(value, end="")
    target = os.getenv("GITHUB_STEP_SUMMARY")
    if target:
        with open(target, "a", encoding="utf-8") as handle:
            handle.write(value)


def run(mode: str) -> int:
    root = Path(__file__).resolve().parents[1]
    surface = discover()
    routes = discover_routes()
    findings = coverage_findings(surface)
    findings.extend(interface_coverage_findings(surface, routes))

    operation_executed = 0
    interface_executed = 0
    if mode in {"generated", "all"}:
        for operation in surface.operations:
            cases = assemble(operation)
            if not cases:
                findings.append(f"{operation.id}: no generated or declared verification case")
                continue
            for case in cases:
                with tempfile.TemporaryDirectory(prefix="software-verification-") as temp:
                    directory = Path(temp)
                    result = invoke(operation, _materialize(case, directory))
                    operation_executed += 1
                    findings.extend(evaluate(operation, case, result))

        for route in routes:
            route_findings, executed = evaluate_interface(route)
            findings.extend(route_findings)
            interface_executed += executed

    if mode in {"architecture", "all"}:
        findings.extend(dependency_findings(root))

    _emit_summary(
        _summary(
            surface,
            routes,
            findings,
            operation_executed=operation_executed,
            interface_executed=interface_executed,
        )
    )
    return 1 if findings else 0


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "mode",
        choices=("surface", "generated", "architecture", "all"),
        nargs="?",
        default="all",
    )
    args = parser.parse_args(argv)
    raise SystemExit(run(args.mode))


if __name__ == "__main__":
    main()
