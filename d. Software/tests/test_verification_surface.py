from __future__ import annotations

from pathlib import Path
import sys
import unittest

SOFTWARE=Path(__file__).resolve().parents[1]
if str(SOFTWARE) not in sys.path:
    sys.path.insert(0,str(SOFTWARE))

from repo_manager.verification.cases import assemble
from repo_manager.verification.coverage import coverage_findings
from repo_manager.verification.discovery import discover

class VerificationSurfaceTests(unittest.TestCase):
    def test_public_operations_are_discovered_without_cli_ownership(self) -> None:
        surface=discover()
        ids={operation.id for operation in surface.operations}
        self.assertTrue({
            "yaml.parse","frontmatter.inspect","html.inspect",
            "organizing.refresh","organizing.inspect","organizing.resolve","organizing.normalize",
        }<=ids)
        self.assertEqual([],coverage_findings(surface))

    def test_cli_routes_are_unique(self) -> None:
        surface=discover()
        self.assertEqual(len(surface.commands),len(set(surface.commands)))

    def test_every_public_operation_has_self_assembled_cases(self) -> None:
        for operation in discover().operations:
            with self.subTest(operation=operation.id):
                self.assertTrue(assemble(operation))

if __name__=="__main__":
    unittest.main()
