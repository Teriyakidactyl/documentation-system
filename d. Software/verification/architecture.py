"""Mechanically decidable dependency checks for the Software role split."""
from __future__ import annotations
import ast
from pathlib import Path

def _imports(path: Path) -> set[str]:
    tree=ast.parse(path.read_text(encoding="utf-8"),filename=str(path))
    result=set()
    for node in ast.walk(tree):
        if isinstance(node,ast.Import):
            result.update(alias.name for alias in node.names)
        elif isinstance(node,ast.ImportFrom) and node.module:
            result.add(node.module)
    return result

def dependency_findings(software_root: Path) -> list[str]:
    rules={"core":("capabilities","interfaces","automation","verification"),"capabilities":("interfaces","automation","verification")}
    findings=[]
    for package,forbidden in rules.items():
        root=software_root/package
        if not root.exists():
            continue
        for path in sorted(root.rglob("*.py")):
            for imported in sorted(_imports(path)):
                if any(imported==name or imported.startswith(name+".") for name in forbidden):
                    findings.append(f"{path.relative_to(software_root).as_posix()}: forbidden dependency on {imported}")
    return findings
