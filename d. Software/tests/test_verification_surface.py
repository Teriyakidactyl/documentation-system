from __future__ import annotations

from pathlib import Path
import sys
import unittest

SOFTWARE=Path(__file__).resolve().parents[1]
if str(SOFTWARE) not in sys.path:
    sys.path.insert(0,str(SOFTWARE))

from verification.cases import assemble
from verification.coverage import coverage_findings
from verification.discovery import discover

class VerificationSurfaceTests(unittest.TestCase):
    def test_public_operations_are_discovered_without_cli_ownership(self) -> None:
        surface=discover(SOFTWARE)
        ids={operation.id for operation in surface.operations}
        self.assertTrue({
            "yaml.parse","frontmatter.inspect","html.inspect",
            "organizing.refresh","organizing.inspect","organizing.resolve","organizing.normalize",
        }<=ids)
        self.assertEqual([],coverage_findings(surface))

    def test_cli_routes_are_unique(self) -> None:
        surface=discover(SOFTWARE)
        self.assertEqual(len(surface.commands),len(set(surface.commands)))

    def test_every_public_operation_has_self_assembled_cases(self) -> None:
        for operation in discover(SOFTWARE).operations:
            with self.subTest(operation=operation.id):
                self.assertTrue(assemble(operation))

if __name__=="__main__":
    unittest.main()
