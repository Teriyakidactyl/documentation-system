"""Mechanically discover runtime Software operation declarations."""

from __future__ import annotations

import importlib
import pkgutil

import _capabilities
from core.operation import Operation
from core.registry import operations


def discover() -> tuple[Operation, ...]:
    """Import capability modules and return their registered operations."""

    prefix = _capabilities.__name__ + "."
    for module in pkgutil.walk_packages(_capabilities.__path__, prefix):
        importlib.import_module(module.name)
    return operations()
