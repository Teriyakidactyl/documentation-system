"""Local and CI entry point for self-assembled Software verification."""
from __future__ import annotations
import argparse
import os
from pathlib import Path
import tempfile
from core.execution import invoke
from .architecture import dependency_findings
from .cases import assemble
from .contracts import evaluate
from .coverage import ratchet_findings, stale_baseline
from .discovery import discover

def _replace_tmp(value,directory: Path):
    if isinstance(value,str):
        return value.replace("{tmp}",str(directory))
    if isinstance(value,list):
        return [_replace_tmp(item,directory) for item in value]
    if isinstance(value,dict):
        return {key:_replace_tmp(item,directory) for key,item in value.items()}
    return value

def _materialize(case,directory: Path) -> dict:
    for relative in case.fixture_dirs:
        (directory/relative).mkdir(parents=True,exist_ok=True)
    for relative,content in (case.fixture_files or {}).items():
        path=directory/relative
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(content,encoding="utf-8")
    values={key:_replace_tmp(value,directory) for key,value in case.inputs.items()}
    if case.fixture_input is not None:
        path=directory/f"fixture{case.fixture_suffix}"
        path.write_text(case.fixture_content or "",encoding="utf-8")
        values[case.fixture_input]=str(path)
    return values

def _summary(surface,findings:list[str],executed:int=0) -> str:
    lines=[
        "## Software verification","",
        f"- public adapters: {len(surface.public_adapters)}",
        f"- declared operations: {len(surface.operations)}",
        f"- unmigrated adapters: {len(surface.unmigrated_adapters)}",
        f"- assembled cases executed: {executed}",
        f"- findings: {len(findings)}",
    ]
    if surface.unmigrated_adapters:
        lines.append(f"- accepted migration gaps: {', '.join(surface.unmigrated_adapters)}")
    stale=stale_baseline(surface)
    if stale:
        lines.append(f"- stale baseline entries: {', '.join(stale)}")
    if findings:
        lines.extend(["","### Findings",*[f"- {item}" for item in findings]])
    return "\n".join(lines)+"\n"

def _emit_summary(value:str) -> None:
    print(value,end="")
    target=os.getenv("GITHUB_STEP_SUMMARY")
    if target:
        with open(target,"a",encoding="utf-8") as handle:
            handle.write(value)

def run(mode:str) -> int:
    root=Path(__file__).resolve().parents[1]
    surface=discover(root)
    findings=ratchet_findings(surface)
    executed=0
    if mode in {"generated","all"}:
        for operation in surface.operations:
            cases=assemble(operation)
            if not cases:
                findings.append(f"{operation.id}: no generated or declared verification case")
                continue
            for case in cases:
                with tempfile.TemporaryDirectory(prefix="software-verification-") as temp:
                    directory=Path(temp)
                    result=invoke(operation,_materialize(case,directory))
                    executed+=1
                    findings.extend(evaluate(operation,case,result))
    if mode in {"architecture","all"}:
        findings.extend(dependency_findings(root))
    _emit_summary(_summary(surface,findings,executed))
    return 1 if findings else 0

def main(argv:list[str] | None=None) -> None:
    parser=argparse.ArgumentParser()
    parser.add_argument("mode",choices=("surface","generated","architecture","all"),nargs="?",default="all")
    args=parser.parse_args(argv)
    raise SystemExit(run(args.mode))

if __name__=="__main__":
    main()
