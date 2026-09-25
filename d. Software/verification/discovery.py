"""Discover interface-neutral public operation declarations."""
from __future__ import annotations
import importlib
import pkgutil
from dataclasses import dataclass
from pathlib import Path
from core.registry import all_operations

@dataclass(frozen=True)
class Surface:
    operations: tuple

    @property
    def commands(self) -> tuple[tuple[str,...], ...]:
        return tuple(command for operation in self.operations for command in operation.commands)

def _import_operation_modules() -> None:
    package=importlib.import_module("documentation_system.operations")
    for module in pkgutil.iter_modules(package.__path__):
        if not module.name.startswith("_"):
            importlib.import_module(f"documentation_system.operations.{module.name}")

def discover(software_root: Path | None=None) -> Surface:
    _import_operation_modules()
    return Surface(all_operations())
