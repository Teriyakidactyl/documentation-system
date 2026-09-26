"""Discoverable CLI projection declarations over public operations."""
from __future__ import annotations

import importlib
import pkgutil
from dataclasses import dataclass
from typing import Any, Callable, Mapping

from repo_manager.core.operation import Operation
from repo_manager.core.result import Result

Executor = Callable[[Operation, Mapping[str, Any]], Result[Any]]
Arguments = Callable[[Mapping[str, Any]], list[str]]
InputProjection = Callable[[Mapping[str, Any]], Mapping[str, Any]]


def _identity_inputs(values: Mapping[str, Any]) -> Mapping[str, Any]:
    return dict(values)


@dataclass(frozen=True)
class RouteVerification:
    """Authored facts needed to exercise one CLI projection generically."""

    success_value: Any
    output: str = "text"


@dataclass(frozen=True)
class CliRoute:
    """One executable CLI projection of a public semantic operation."""

    command: tuple[str, ...]
    operation: Operation
    main: Callable[..., None]
    arguments: Arguments
    project_inputs: InputProjection = _identity_inputs
    verification: RouteVerification = RouteVerification(success_value=None)

    def argv(self, values: Mapping[str, Any]) -> list[str]:
        if len(self.command) != 2:
            raise ValueError(f"CLI route must use subject/action grammar: {self.command!r}")
        return [self.command[1], *self.arguments(values)]

    def expected_inputs(self, values: Mapping[str, Any]) -> dict[str, Any]:
        return dict(self.project_inputs(values))


def discover_routes() -> tuple[CliRoute, ...]:
    """Discover CLI route declarations without a handwritten central inventory."""

    package = importlib.import_module("repo_manager.interfaces.cli")
    routes: list[CliRoute] = []
    for module in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
        leaf = module.name.rsplit(".", 1)[-1]
        if leaf.startswith("_"):
            continue
        loaded = importlib.import_module(module.name)
        routes.extend(getattr(loaded, "CLI_ROUTES", ()))
    return tuple(sorted(routes, key=lambda route: route.command))
