from __future__ import annotations

from pathlib import Path
import sys
import unittest

SOFTWARE = Path(__file__).resolve().parents[1]
if str(SOFTWARE) not in sys.path:
    sys.path.insert(0, str(SOFTWARE))

from repo_manager.interfaces.cli.surface import discover_routes
from repo_manager.verification.cases import assemble
from repo_manager.verification.coverage import coverage_findings
from repo_manager.verification.discovery import discover
from repo_manager.verification.interface import (
    coverage_findings as interface_coverage_findings,
)
from repo_manager.verification.interface import evaluate as evaluate_interface


class VerificationSurfaceTests(unittest.TestCase):
    def test_public_operations_are_discovered_without_cli_ownership(self) -> None:
        surface = discover()
        ids = {operation.id for operation in surface.operations}
        self.assertTrue(
            {
                "yaml.parse",
                "frontmatter.inspect",
                "html.inspect",
                "organizing.refresh",
                "organizing.inspect",
                "organizing.resolve",
                "organizing.normalize",
            }
            <= ids
        )
        self.assertEqual([], coverage_findings(surface))

    def test_cli_routes_are_unique_and_use_approved_organize_subject(self) -> None:
        surface = discover()
        self.assertEqual(len(surface.commands), len(set(surface.commands)))
        self.assertIn(("organize", "refresh"), surface.commands)
        self.assertNotIn(("organizing", "refresh"), surface.commands)

    def test_declared_cli_routes_have_executable_projections(self) -> None:
        surface = discover()
        routes = discover_routes()
        self.assertEqual([], interface_coverage_findings(surface, routes))
        self.assertEqual(set(surface.commands), {route.command for route in routes})

    def test_public_cli_projections_participate_in_self_assembled_verification(self) -> None:
        for route in discover_routes():
            with self.subTest(command=" ".join(route.command)):
                findings, executed = evaluate_interface(route)
                self.assertEqual(2, executed)
                self.assertEqual([], findings)

    def test_every_public_operation_has_self_assembled_cases(self) -> None:
        for operation in discover().operations:
            with self.subTest(operation=operation.id):
                self.assertTrue(assemble(operation))


if __name__ == "__main__":
    unittest.main()
