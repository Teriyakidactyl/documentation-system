"""Own Documentation Compiler command-line orchestration and diagnostic presentation."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from .diagnostics import annotate, emit, write_json
from .engine import compile_corpus, resolve_address
from .model import CompilerError, find_repository_root


def usage(script: Path) -> str:
    return (
        f'Usage:\n  python3 "{script.name}" [--annotate] [--diagnostics-json PATH] [corpus_root]\n'
        f'  python3 "{script.name}" --resolve ADDRESS [corpus_root]'
    )


def run(script: Path, argv: list[str]) -> int:
    resolve: str | None = None
    annotate_source = False
    diagnostics_json: Path | None = None
    positional: list[str] = []
    index = 0
    while index < len(argv):
        arg = argv[index]
        if arg == "--resolve":
            if index + 1 >= len(argv):
                raise CompilerError("--resolve requires an address")
            resolve = argv[index + 1]
            index += 2
        elif arg == "--annotate":
            annotate_source = True
            index += 1
        elif arg == "--diagnostics-json":
            if index + 1 >= len(argv):
                raise CompilerError("--diagnostics-json requires a path")
            diagnostics_json = Path(argv[index + 1])
            index += 2
        elif arg in {"-h", "--help"}:
            print(usage(script))
            return 0
        else:
            positional.append(arg)
            index += 1
    if len(positional) > 1:
        raise CompilerError(usage(script))
    corpus_root = Path(positional[0]).resolve() if positional else find_repository_root(script)

    if resolve is not None:
        print(json.dumps(resolve_address(corpus_root, resolve), indent=2, ensure_ascii=False))
        return 0

    result = compile_corpus(corpus_root)
    if result.diagnostics:
        emit(list(result.diagnostics), corpus_root)
        if diagnostics_json is not None:
            write_json(diagnostics_json, list(result.diagnostics), corpus_root)
        if annotate_source:
            annotate(corpus_root, list(result.diagnostics))
    elif diagnostics_json is not None:
        write_json(diagnostics_json, [], corpus_root)

    print(
        f"Compiled {result.artifacts} controlled artifacts across {result.locations} addressed locations "
        f"beneath corpus root {corpus_root}; minted {result.uids_minted} uids, refreshed {result.links_refreshed} "
        f"controlled links, and reported {len(result.diagnostics)} diagnostics"
    )
    return 1 if result.errors else 0


def main(script: Path | None = None, argv: list[str] | None = None) -> None:
    script = script or Path(sys.argv[0]).resolve()
    argv = list(sys.argv[1:] if argv is None else argv)
    try:
        code = run(script, argv)
    except CompilerError as exc:
        raise SystemExit(f"documentation compiler: {exc}") from exc
    raise SystemExit(code)
