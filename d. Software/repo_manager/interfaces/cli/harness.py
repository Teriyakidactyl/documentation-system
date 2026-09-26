"""Harness command-line adapter."""
from __future__ import annotations

import argparse
from pathlib import Path
import sys
from typing import Any, Mapping

from repo_manager.capabilities.harness import HARNESS_PROJECT
from repo_manager.core import invoke
from repo_manager.core.projection import json_text

from .surface import CliRoute, RouteVerification


def _source_root() -> Path:
    for candidate in Path(__file__).resolve().parents:
        if (candidate / "SKILL.md").is_file():
            return candidate
    raise SystemExit("Cannot locate Documentation System source root containing SKILL.md")


def main(argv: list[str] | None = None, *, executor=invoke) -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("install", "check", "remove"):
        command = sub.add_parser(name)
        command.add_argument("host_root", nargs="?")
        command.add_argument("--target", action="append", default=[])
    args = parser.parse_args(argv)
    source_root = _source_root()
    host_root = Path(args.host_root).resolve() if args.host_root else Path.cwd().resolve()
    result = executor(
        HARNESS_PROJECT,
        {
            "source_root": str(source_root),
            "host_root": str(host_root),
            "mode": args.command,
            "targets": args.target,
        },
    )
    if result.value:
        for row in result.value["results"]:
            print(f"{row['state']:12} {row['link']}")
    if not result.ok:
        print(json_text(result), file=sys.stderr)
        raise SystemExit(1)


def _arguments(values: Mapping[str, Any]) -> list[str]:
    arguments = [str(values["host_root"])]
    for target in values.get("targets", []):
        arguments.extend(["--target", str(target)])
    return arguments


def _project_inputs(mode: str):
    def project(values: Mapping[str, Any]) -> Mapping[str, Any]:
        return {
            "source_root": str(_source_root()),
            "host_root": str(Path(str(values["host_root"])).resolve()),
            "mode": mode,
            "targets": list(values.get("targets", [])),
        }

    return project


CLI_ROUTES = tuple(
    CliRoute(
        command=command,
        operation=HARNESS_PROJECT,
        main=main,
        arguments=_arguments,
        project_inputs=_project_inputs(command[1]),
        verification=RouteVerification(success_value={"results": []}, output="none"),
    )
    for command in HARNESS_PROJECT.commands
)
