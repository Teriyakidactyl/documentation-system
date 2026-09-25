"""Discover public operations from semantic-owner packages."""
from __future__ import annotations
import importlib
import pkgutil
from dataclasses import dataclass
from repo_manager.core.registry import all_operations

@dataclass(frozen=True)
class Surface:
    operations: tuple

    @property
    def commands(self) -> tuple[tuple[str,...], ...]:
        return tuple(command for operation in self.operations for command in operation.commands)

def _import_tree(package_name: str) -> None:
    package=importlib.import_module(package_name)
    for module in pkgutil.walk_packages(package.__path__,package.__name__+"."):
        if not module.name.rsplit(".",1)[-1].startswith("_"):
            importlib.import_module(module.name)

def discover() -> Surface:
    _import_tree("repo_manager.capabilities")
    _import_tree("repo_manager.automation")
    return Surface(all_operations())
