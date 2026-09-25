"""Visible public-surface coverage and accepted-gap ratchet."""
from __future__ import annotations
import json
from pathlib import Path
from .discovery import Surface

def baseline_path() -> Path:
    return Path(__file__).with_name("coverage-baseline.json")

def accepted_gaps(path: Path | None=None) -> set[str]:
    payload=json.loads((path or baseline_path()).read_text(encoding="utf-8"))
    return set(payload.get("unmigrated_adapters",[]))

def ratchet_findings(surface: Surface, path: Path | None=None) -> list[str]:
    new=sorted(set(surface.unmigrated_adapters)-accepted_gaps(path))
    return [f"new unverified public adapter: {name}" for name in new]

def stale_baseline(surface: Surface, path: Path | None=None) -> tuple[str,...]:
    return tuple(sorted(accepted_gaps(path)-set(surface.unmigrated_adapters)))
