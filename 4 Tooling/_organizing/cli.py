"""Own Organizing command-line orchestration and presentation."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .diagnostics import annotate, emit, write_json
from .engine import refresh_corpus, resolve_address
from .model import OrganizingError, find_repository_root
from .refactor import inspect_organization, normalize_conventions

COMMANDS = {"refresh", "inspect", "resolve", "normalize"}


def _compatibility_argv(argv: list[str]) -> list[str]:
    if not argv:
        return ["refresh"]
    if argv[0] == "--resolve":
        if len(argv) < 2:
            raise OrganizingError("--resolve requires an address")
        return ["resolve", argv[1], *argv[2:]]
    if argv[0] in COMMANDS or argv[0] in {"-h", "--help"}:
        return argv
    return ["refresh", *argv]


def parser(script: Path) -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog=script.name)
    sub = root.add_subparsers(dest="command", required=True)

    refresh = sub.add_parser("refresh", help="refresh deterministic organization state")
    refresh.add_argument("--annotate", action="store_true")
    refresh.add_argument("--diagnostics-json", type=Path)
    refresh.add_argument("corpus_root", nargs="?")

    inspect = sub.add_parser("inspect", help="inspect organization and normalization facts")
    inspect.add_argument("corpus_root", nargs="?")

    resolve = sub.add_parser("resolve", help="resolve a current documentation locator")
    resolve.add_argument("address")
    resolve.add_argument("corpus_root", nargs="?")

    normalize = sub.add_parser("normalize", help="plan or apply folder convention normalization")
    normalize.add_argument("--apply", action="store_true")
    normalize.add_argument("corpus_root", nargs="?")

    return root


def _corpus_root(script: Path, value: str | None) -> Path:
    return Path(value).resolve() if value else find_repository_root(script)


def _refresh(args: argparse.Namespace, corpus_root: Path) -> int:
    result = refresh_corpus(corpus_root)
    if result.diagnostics:
        emit(list(result.diagnostics), corpus_root)
        if args.diagnostics_json is not None:
            write_json(args.diagnostics_json, list(result.diagnostics), corpus_root)
        if args.annotate:
            annotate(corpus_root, list(result.diagnostics))
    elif args.diagnostics_json is not None:
        write_json(args.diagnostics_json, [], corpus_root)

    print(
        f"Refreshed {result.artifacts} controlled artifacts across {result.locations} "
        f"organized locations beneath corpus root {corpus_root}; minted "
        f"{result.uids_minted} uids, refreshed {result.links_refreshed} controlled "
        f"links, and reported {len(result.diagnostics)} diagnostics"
    )
    return 1 if result.errors else 0


def run(script: Path, argv: list[str]) -> int:
    args = parser(script).parse_args(_compatibility_argv(argv))
    corpus_root = _corpus_root(script, getattr(args, "corpus_root", None))

    if args.command == "resolve":
        print(json.dumps(resolve_address(corpus_root, args.address), indent=2, ensure_ascii=False))
        return 0

    if args.command == "inspect":
        print(json.dumps(inspect_organization(corpus_root), indent=2, ensure_ascii=False))
        return 0

    if args.command == "normalize":
        payload = normalize_conventions(corpus_root, apply=args.apply)
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        if args.apply and payload["applied"]:
            refresh_args = argparse.Namespace(annotate=False, diagnostics_json=None)
            return _refresh(refresh_args, corpus_root)
        return 0

    return _refresh(args, corpus_root)


def main(script: Path | None = None, argv: list[str] | None = None) -> None:
    script = script or Path(sys.argv[0]).resolve()
    argv = list(sys.argv[1:] if argv is None else argv)
    try:
        code = run(script, argv)
    except OrganizingError as exc:
        raise SystemExit(f"organizing: {exc}") from exc
    raise SystemExit(code)
