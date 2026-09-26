"""Repository Work Management command-line adapter."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Mapping

from repo_manager.automation.work_management.operations import (
    RECONCILE,
    REGISTER_TASK,
    SETUP,
    VALIDATE,
)
from repo_manager.core import invoke
from repo_manager.core.projection import json_text

from .surface import CliRoute, RouteVerification


def _root(value: str | None) -> str:
    return str(Path(value or ".").resolve())


def main(argv: list[str] | None = None, *, executor=invoke) -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    for name in ("setup", "reconcile", "validate"):
        command = sub.add_parser(name)
        command.add_argument("corpus_root", nargs="?")

    register_task = sub.add_parser("register-task")
    register_task.add_argument("title")
    register_task.add_argument("corpus_root", nargs="?")

    args = parser.parse_args(argv)
    inputs = {"corpus_root": _root(getattr(args, "corpus_root", None))}

    if args.command == "setup":
        operation = SETUP
    elif args.command == "reconcile":
        operation = RECONCILE
    elif args.command == "validate":
        operation = VALIDATE
    else:
        operation = REGISTER_TASK
        inputs["title"] = args.title

    result = executor(operation, inputs)
    if result.ok:
        print(json.dumps(result.value, indent=2, ensure_ascii=False))
        return

    print(json_text(result), file=sys.stderr)
    raise SystemExit(1)


def _root_arguments(values: Mapping[str, Any]) -> list[str]:
    return [str(values["corpus_root"])]


def _root_inputs(values: Mapping[str, Any]) -> Mapping[str, Any]:
    return {"corpus_root": _root(str(values["corpus_root"]))}


def _register_arguments(values: Mapping[str, Any]) -> list[str]:
    return [str(values["title"]), str(values["corpus_root"])]


def _register_inputs(values: Mapping[str, Any]) -> Mapping[str, Any]:
    return {
        "corpus_root": _root(str(values["corpus_root"])),
        "title": str(values["title"]),
    }


CLI_ROUTES = (
    CliRoute(
        command=SETUP.commands[0],
        operation=SETUP,
        main=main,
        arguments=_root_arguments,
        project_inputs=_root_inputs,
        verification=RouteVerification(success_value={}, output="json"),
    ),
    CliRoute(
        command=RECONCILE.commands[0],
        operation=RECONCILE,
        main=main,
        arguments=_root_arguments,
        project_inputs=_root_inputs,
        verification=RouteVerification(success_value={}, output="json"),
    ),
    CliRoute(
        command=VALIDATE.commands[0],
        operation=VALIDATE,
        main=main,
        arguments=_root_arguments,
        project_inputs=_root_inputs,
        verification=RouteVerification(success_value={}, output="json"),
    ),
    CliRoute(
        command=REGISTER_TASK.commands[0],
        operation=REGISTER_TASK,
        main=main,
        arguments=_register_arguments,
        project_inputs=_register_inputs,
        verification=RouteVerification(success_value={}, output="json"),
    ),
)
