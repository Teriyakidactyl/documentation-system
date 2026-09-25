"""Organizing command-line adapter."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from repo_manager.automation.organizing.diagnostics import (
    Diagnostic as OrganizingDiagnostic,
    Severity as OrganizingSeverity,
    emit,
    write_json,
)
from repo_manager.automation.organizing.model import find_repository_root
from repo_manager.automation.organizing.operations import INSPECT, NORMALIZE, REFRESH, RESOLVE
from repo_manager.core import Severity, invoke
from repo_manager.core.projection import json_text


def _root(value: str | None, script: Path | None) -> Path:
    if value:
        return Path(value).resolve()
    return find_repository_root(script or Path(__file__).resolve())


def _organizing_diagnostics(result, corpus_root: Path) -> list[OrganizingDiagnostic]:
    diagnostics: list[OrganizingDiagnostic] = []
    for item in result.diagnostics:
        subject_path = Path(str(item.subject.get("path", "")))
        path = subject_path if subject_path.is_absolute() else corpus_root / subject_path
        diagnostics.append(
            OrganizingDiagnostic(
                code=item.code,
                severity=OrganizingSeverity(item.severity.value),
                path=path,
                line=int(item.subject.get("line") or 1),
                message=item.message,
            )
        )
    return diagnostics


def main(argv: list[str] | None = None, *, script: Path | None = None) -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    refresh = sub.add_parser("refresh")
    refresh.add_argument("corpus_root", nargs="?")
    refresh.add_argument("--annotate", action="store_true")
    refresh.add_argument("--diagnostics-json", default="")

    inspect = sub.add_parser("inspect")
    inspect.add_argument("corpus_root", nargs="?")

    resolve = sub.add_parser("resolve")
    resolve.add_argument("address")
    resolve.add_argument("corpus_root", nargs="?")

    normalize = sub.add_parser("normalize")
    normalize.add_argument("corpus_root", nargs="?")
    normalize.add_argument("--apply", action="store_true")

    args = parser.parse_args(argv)
    corpus_root = _root(getattr(args, "corpus_root", None), script)

    if args.command == "refresh":
        result = invoke(
            REFRESH,
            {"corpus_root": str(corpus_root), "annotate": args.annotate},
        )
        diagnostics = _organizing_diagnostics(result, corpus_root)
        if diagnostics:
            emit(diagnostics, corpus_root)
        if args.diagnostics_json:
            write_json(Path(args.diagnostics_json), diagnostics, corpus_root)
        if result.value:
            value = result.value
            print(
                f"Refreshed {value['artifacts']} controlled artifacts across "
                f"{value['locations']} organized locations; minted "
                f"{value['uids_minted']} uids, refreshed "
                f"{value['links_refreshed']} controlled links, and reported "
                f"{len(value['diagnostics'])} diagnostics"
            )
    elif args.command == "inspect":
        result = invoke(INSPECT, {"corpus_root": str(corpus_root)})
        if result.ok:
            print(json.dumps(result.value, indent=2, ensure_ascii=False))
    elif args.command == "resolve":
        result = invoke(
            RESOLVE,
            {"corpus_root": str(corpus_root), "address": args.address},
        )
        if result.ok:
            print(json.dumps(result.value, indent=2, ensure_ascii=False))
    else:
        result = invoke(
            NORMALIZE,
            {"corpus_root": str(corpus_root), "apply": args.apply},
        )
        if result.ok:
            print(json.dumps(result.value, indent=2, ensure_ascii=False))

    if not result.ok:
        print(json_text(result), file=sys.stderr)
        raise SystemExit(1)
    if any(item.severity is Severity.ERROR for item in result.diagnostics):
        raise SystemExit(1)
