"""HTML command-line adapter."""
from __future__ import annotations

import argparse
import json
from typing import Any, Mapping

from repo_manager.capabilities.html import HTML_ANCHORS, HTML_INSPECT
from repo_manager.core import invoke

from .common import require_success
from .surface import CliRoute, RouteVerification


def main(argv: list[str] | None = None, *, executor=invoke) -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("inspect", "anchors"):
        command = sub.add_parser(name)
        command.add_argument("path")
    args = parser.parse_args(argv)
    operation = HTML_INSPECT if args.command == "inspect" else HTML_ANCHORS
    print(
        json.dumps(
            require_success(executor(operation, {"path": args.path})),
            indent=2,
            ensure_ascii=False,
        )
    )


def _arguments(values: Mapping[str, Any]) -> list[str]:
    return [str(values["path"])]


CLI_ROUTES = tuple(
    CliRoute(
        command=operation.commands[0],
        operation=operation,
        main=main,
        arguments=_arguments,
        verification=RouteVerification(success_value={}, output="json"),
    )
    for operation in (HTML_INSPECT, HTML_ANCHORS)
)
