"""Markdown command-line adapter."""
from __future__ import annotations

import argparse
import json
from typing import Any, Mapping

from repo_manager.capabilities.markdown import (
    MARKDOWN_FIX,
    MARKDOWN_GET_SECTION,
    MARKDOWN_HEADINGS,
    MARKDOWN_LINT,
    MARKDOWN_RENUMBER,
    MARKDOWN_RULES,
    MARKDOWN_SECTIONS,
)
from repo_manager.core import invoke

from .common import require_success
from .surface import CliRoute, RouteVerification


def main(argv: list[str] | None = None, *, executor=invoke) -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    command = sub.add_parser("headings")
    command.add_argument("path")
    command = sub.add_parser("sections")
    command.add_argument("path")
    command = sub.add_parser("get-section")
    command.add_argument("path")
    command.add_argument("selector")
    command.add_argument("--no-heading", action="store_true")
    command = sub.add_parser("lint")
    command.add_argument("path")
    command = sub.add_parser("fix")
    command.add_argument("path")
    sub.add_parser("rules")
    command = sub.add_parser("renumber")
    command.add_argument("path")
    command.add_argument("--write", action="store_true")
    args = parser.parse_args(argv)

    if args.command == "rules":
        print(
            json.dumps(
                require_success(executor(MARKDOWN_RULES, {})),
                indent=2,
                ensure_ascii=False,
            )
        )
        return
    if args.command == "headings":
        value = require_success(executor(MARKDOWN_HEADINGS, {"path": args.path}))
    elif args.command == "sections":
        value = require_success(executor(MARKDOWN_SECTIONS, {"path": args.path}))
    elif args.command == "get-section":
        value = require_success(
            executor(
                MARKDOWN_GET_SECTION,
                {
                    "path": args.path,
                    "selector": args.selector,
                    "no_heading": args.no_heading,
                },
            )
        )
        print(value, end="")
        return
    elif args.command == "lint":
        value = require_success(executor(MARKDOWN_LINT, {"path": args.path}))
        print(json.dumps(value, indent=2, ensure_ascii=False))
        raise SystemExit(1 if value["diagnostics"] else 0)
    elif args.command == "fix":
        value = require_success(executor(MARKDOWN_FIX, {"path": args.path}))
        print(json.dumps(value, indent=2, ensure_ascii=False))
        raise SystemExit(1 if value["diagnostics"] else 0)
    else:
        value = require_success(
            executor(
                MARKDOWN_RENUMBER,
                {"path": args.path, "write": args.write},
            )
        )
    print(json.dumps(value, indent=2, ensure_ascii=False))


def _path_arguments(values: Mapping[str, Any]) -> list[str]:
    return [str(values["path"])]


def _get_section_arguments(values: Mapping[str, Any]) -> list[str]:
    arguments = [str(values["path"]), str(values["selector"])]
    if values.get("no_heading"):
        arguments.append("--no-heading")
    return arguments


def _no_arguments(values: Mapping[str, Any]) -> list[str]:
    return []


def _renumber_arguments(values: Mapping[str, Any]) -> list[str]:
    arguments = [str(values["path"])]
    if values.get("write"):
        arguments.append("--write")
    return arguments


CLI_ROUTES = (
    CliRoute(
        command=MARKDOWN_HEADINGS.commands[0],
        operation=MARKDOWN_HEADINGS,
        main=main,
        arguments=_path_arguments,
        verification=RouteVerification(success_value=[], output="json"),
    ),
    CliRoute(
        command=MARKDOWN_SECTIONS.commands[0],
        operation=MARKDOWN_SECTIONS,
        main=main,
        arguments=_path_arguments,
        verification=RouteVerification(success_value=[], output="json"),
    ),
    CliRoute(
        command=MARKDOWN_GET_SECTION.commands[0],
        operation=MARKDOWN_GET_SECTION,
        main=main,
        arguments=_get_section_arguments,
        verification=RouteVerification(success_value="section\n", output="text"),
    ),
    CliRoute(
        command=MARKDOWN_LINT.commands[0],
        operation=MARKDOWN_LINT,
        main=main,
        arguments=_path_arguments,
        verification=RouteVerification(success_value={"diagnostics": []}, output="json"),
    ),
    CliRoute(
        command=MARKDOWN_FIX.commands[0],
        operation=MARKDOWN_FIX,
        main=main,
        arguments=_path_arguments,
        verification=RouteVerification(success_value={"diagnostics": []}, output="json"),
    ),
    CliRoute(
        command=MARKDOWN_RULES.commands[0],
        operation=MARKDOWN_RULES,
        main=main,
        arguments=_no_arguments,
        verification=RouteVerification(success_value={}, output="json"),
    ),
    CliRoute(
        command=MARKDOWN_RENUMBER.commands[0],
        operation=MARKDOWN_RENUMBER,
        main=main,
        arguments=_renumber_arguments,
        verification=RouteVerification(success_value={}, output="json"),
    ),
)
