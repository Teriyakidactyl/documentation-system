"""Discover public operation declarations and unmigrated root adapters."""
from __future__ import annotations
import importlib
import pkgutil
from dataclasses import dataclass
from pathlib import Path
from core.registry import all_operations

@dataclass(frozen=True)
class Surface:
    operations: tuple
    public_adapters: tuple[str, ...]
    unmigrated_adapters: tuple[str, ...]

def _import_cli_modules() -> None:
    package=importlib.import_module("interfaces.cli")
    for module in pkgutil.iter_modules(package.__path__):
        if not module.name.startswith("_"):
            importlib.import_module(f"interfaces.cli.{module.name}")

def discover(software_root: Path | None=None) -> Surface:
    _import_cli_modules()
    operations=all_operations()
    root=(software_root or Path(__file__).resolve().parents[1]).resolve()
    adapters=tuple(sorted(path.name for path in root.glob("*.py") if path.is_file()))
    declared={operation.adapter for operation in operations}
    return Surface(operations,adapters,tuple(name for name in adapters if name not in declared))
