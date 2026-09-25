from __future__ import annotations

from pathlib import Path
import sys
import unittest

SOFTWARE=Path(__file__).resolve().parents[1]
if str(SOFTWARE) not in sys.path:
    sys.path.insert(0,str(SOFTWARE))

from verification.cases import assemble
from verification.coverage import ratchet_findings
from verification.discovery import discover

class VerificationSurfaceTests(unittest.TestCase):
    def test_migrated_cli_adapters_are_discovered(self) -> None:
        surface=discover(SOFTWARE)
        declared={operation.adapter for operation in surface.operations}
        self.assertTrue({"YAML.py","Frontmatter.py","HTML.py"}<=declared)
        self.assertNotIn("YAML.py",surface.unmigrated_adapters)
        self.assertNotIn("Frontmatter.py",surface.unmigrated_adapters)
        self.assertNotIn("HTML.py",surface.unmigrated_adapters)

    def test_current_unmigrated_surface_is_accepted_by_ratchet(self) -> None:
        self.assertEqual([],ratchet_findings(discover(SOFTWARE)))

    def test_every_migrated_operation_has_self_assembled_cases(self) -> None:
        for operation in discover(SOFTWARE).operations:
            with self.subTest(operation=operation.id):
                self.assertTrue(assemble(operation))

if __name__=="__main__":
    unittest.main()
