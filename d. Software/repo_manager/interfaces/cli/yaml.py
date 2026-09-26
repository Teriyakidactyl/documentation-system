"""YAML command-line adapter."""
from __future__ import annotations

import argparse
import json
from typing import Any, Mapping

from repo_manager.capabilities.yaml import OPERATION
from repo_manager.core import invoke

from .common import require_success
from .surface import CliRoute, RouteVerification


def main(argv: list[str] | None = None, *, executor=invoke) -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    parse = sub.add_parser("parse")
    parse.add_argument("path")
    args = parser.parse_args(argv)
    print(
        json.dumps(
            require_success(executor(OPERATION, {"path": args.path})),
            indent=2,
            ensure_ascii=False,
        )
    )


def _arguments(values: Mapping[str, Any]) -> list[str]:
    return [str(values["path"])]


CLI_ROUTES = (
    CliRoute(
        command=OPERATION.commands[0],
        operation=OPERATION,
        main=main,
        arguments=_arguments,
        verification=RouteVerification(success_value={}, output="json"),
    ),
)
