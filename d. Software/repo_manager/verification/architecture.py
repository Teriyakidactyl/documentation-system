"""Mechanically decidable dependency checks for Repo Manager roles."""
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

def dependency_findings(package_root: Path) -> list[str]:
    rules={
        "core":("repo_manager.capabilities","repo_manager.automation","repo_manager.interfaces","repo_manager.verification"),
        "capabilities":("repo_manager.automation","repo_manager.interfaces","repo_manager.verification"),
        "automation":("repo_manager.interfaces","repo_manager.verification"),
        "verification":("repo_manager.interfaces",),
    }
    findings=[]
    for package,forbidden in rules.items():
        root=package_root/package
        if not root.exists():
            continue
        for path in sorted(root.rglob("*.py")):
            for imported in sorted(_imports(path)):
                if any(imported==name or imported.startswith(name+".") for name in forbidden):
                    findings.append(f"{path.relative_to(package_root).as_posix()}: forbidden dependency on {imported}")
    return findings
