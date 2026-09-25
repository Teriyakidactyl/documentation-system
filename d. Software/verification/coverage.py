"""Public-operation and interface-route coverage checks."""
from __future__ import annotations
from collections import Counter
from .discovery import Surface

def coverage_findings(surface: Surface) -> list[str]:
    findings=[]
    for operation in surface.operations:
        if not operation.commands:
            findings.append(f"{operation.id}: no public CLI route declared")
        if not operation.owner.module.startswith("documentation_system.operations."):
            findings.append(f"{operation.id}: operation owner is not interface-neutral: {operation.owner.module}")
    counts=Counter(surface.commands)
    for command,count in sorted(counts.items()):
        if count>1:
            findings.append(f"duplicate CLI route {' '.join(command)} declared by {count} operations")
    return findings
