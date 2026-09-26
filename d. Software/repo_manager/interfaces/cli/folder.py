"""Folder command-line adapter."""
from __future__ import annotations

import argparse
import json
from typing import Any, Mapping

from repo_manager.capabilities.folder import FOLDER_RENAME, FOLDER_STRIP_PREFIX
from repo_manager.core import invoke

from .common import require_success
from .surface import CliRoute, RouteVerification


def main(argv: list[str] | None = None, *, executor=invoke) -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    rename = sub.add_parser("rename")
    rename.add_argument("source")
    rename.add_argument("destination")
    rename.add_argument("--apply", action="store_true")
    strip = sub.add_parser("strip-prefix")
    strip.add_argument("root")
    strip.add_argument("--match", required=True)
    strip.add_argument("--include", default="")
    kind = strip.add_mutually_exclusive_group()
    kind.add_argument("--files-only", action="store_true")
    kind.add_argument("--folders-only", action="store_true")
    strip.add_argument("--apply", action="store_true")
    args = parser.parse_args(argv)
    if args.command == "rename":
        value = require_success(
            executor(
                FOLDER_RENAME,
                {
                    "source": args.source,
                    "destination": args.destination,
                    "apply": args.apply,
                },
            )
        )
    else:
        value = require_success(
            executor(
                FOLDER_STRIP_PREFIX,
                {
                    "root": args.root,
                    "match": args.match,
                    "include": args.include,
                    "files_only": args.files_only,
                    "folders_only": args.folders_only,
                    "apply": args.apply,
                },
            )
        )
    print(json.dumps(value, indent=2, ensure_ascii=False))


def _rename_arguments(values: Mapping[str, Any]) -> list[str]:
    arguments = [str(values["source"]), str(values["destination"])]
    if values.get("apply"):
        arguments.append("--apply")
    return arguments


def _strip_arguments(values: Mapping[str, Any]) -> list[str]:
    arguments = [str(values["root"]), "--match", str(values["match"])]
    if values.get("include"):
        arguments.extend(["--include", str(values["include"])])
    if values.get("files_only"):
        arguments.append("--files-only")
    if values.get("folders_only"):
        arguments.append("--folders-only")
    if values.get("apply"):
        arguments.append("--apply")
    return arguments


CLI_ROUTES = (
    CliRoute(
        command=FOLDER_RENAME.commands[0],
        operation=FOLDER_RENAME,
        main=main,
        arguments=_rename_arguments,
        verification=RouteVerification(success_value={}, output="json"),
    ),
    CliRoute(
        command=FOLDER_STRIP_PREFIX.commands[0],
        operation=FOLDER_STRIP_PREFIX,
        main=main,
        arguments=_strip_arguments,
        verification=RouteVerification(success_value={}, output="json"),
    ),
)
