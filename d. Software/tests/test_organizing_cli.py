from __future__ import annotations

from contextlib import redirect_stdout
from io import StringIO
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import Mock

SOFTWARE = Path(__file__).resolve().parents[1]
if str(SOFTWARE) not in sys.path:
    sys.path.insert(0, str(SOFTWARE))

from repo_manager.core import Diagnostic, Result, Severity
from repo_manager.interfaces.cli import organizing


class OrganizingCliContractTests(unittest.TestCase):
    def test_omitted_corpus_root_uses_repository_containing_invoking_script(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "repo"
            root.mkdir()
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            script = root / "d. Software" / "Navigation Crawler.py"
            script.parent.mkdir(parents=True)
            script.write_text("# test wrapper\n", encoding="utf-8")

            result = Result.success(
                {
                    "artifacts": 0,
                    "locations": 0,
                    "links_refreshed": 0,
                    "uids_minted": 0,
                    "diagnostics": [],
                }
            )
            invoked = Mock(return_value=result)
            with redirect_stdout(StringIO()):
                organizing.main(["refresh"], script=script, executor=invoked)

            inputs = invoked.call_args.args[1]
            self.assertEqual(str(root.resolve()), inputs["corpus_root"])

    def test_refresh_emits_success_diagnostics_and_writes_diagnostics_schema(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "corpus"
            root.mkdir()
            output = Path(temp) / "diagnostics.json"
            diagnostic = Diagnostic(
                code="DS005",
                severity=Severity.WARNING,
                message="ordinal sequence has a gap",
                subject={"path": "2 Page.md", "line": 7},
            )
            result = Result.success(
                {
                    "artifacts": 1,
                    "locations": 1,
                    "links_refreshed": 0,
                    "uids_minted": 0,
                    "diagnostics": [
                        {
                            "code": "DS005",
                            "severity": "warning",
                            "path": str(root / "2 Page.md"),
                            "line": 7,
                            "message": "ordinal sequence has a gap",
                        }
                    ],
                },
                diagnostics=(diagnostic,),
            )

            stdout = StringIO()
            executor = Mock(return_value=result)
            with redirect_stdout(stdout):
                organizing.main(
                    [
                        "refresh",
                        str(root),
                        "--diagnostics-json",
                        str(output),
                    ],
                    executor=executor,
                )

            rendered = stdout.getvalue()
            self.assertIn(
                "WARNING DS005 2 Page.md:7 ordinal sequence has a gap",
                rendered,
            )
            payload = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(
                {
                    "errors": 0,
                    "warnings": 1,
                    "info": 0,
                    "diagnostics": [
                        {
                            "code": "DS005",
                            "severity": "warning",
                            "path": "2 Page.md",
                            "line": 7,
                            "message": "ordinal sequence has a gap",
                        }
                    ],
                },
                payload,
            )


if __name__ == "__main__":
    unittest.main()
