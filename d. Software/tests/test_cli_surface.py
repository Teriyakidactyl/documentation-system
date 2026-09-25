from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path
import unittest

SOFTWARE=Path(__file__).resolve().parents[1]
if str(SOFTWARE) not in sys.path:
    sys.path.insert(0,str(SOFTWARE))

from verification.discovery import discover

class CliSurfaceTests(unittest.TestCase):
    def _run(self,*args:str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable,"-m","documentation_system",*args],
            cwd=SOFTWARE,
            text=True,
            capture_output=True,
            timeout=30,
        )

    def test_every_declared_cli_route_resolves_through_final_dispatcher(self) -> None:
        for route in sorted(set(discover(SOFTWARE).commands)):
            with self.subTest(route=" ".join(route)):
                result=self._run(*route,"--help")
                self.assertEqual(
                    0,result.returncode,
                    msg=f"{' '.join(route)} --help failed\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
                )

    def test_success_projection_uses_final_dispatcher(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/"value.yaml"
            path.write_text("key: value\n",encoding="utf-8")
            result=self._run("yaml","parse",str(path))
        self.assertEqual(0,result.returncode,result.stderr)
        self.assertEqual({"key":"value"},json.loads(result.stdout))

    def test_failure_projection_uses_canonical_result(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/"broken.yaml"
            path.write_text("key: [\n",encoding="utf-8")
            result=self._run("yaml","parse",str(path))
        self.assertEqual(1,result.returncode)
        payload=json.loads(result.stderr)
        self.assertEqual("failure",payload["status"])
        self.assertEqual("complete",payload["completion"])
        self.assertEqual("YAML_ERROR",payload["failures"][0]["name"])
        self.assertEqual("documentation_system.capabilities.yaml",payload["failures"][0]["origin"]["module"])

if __name__=="__main__":
    unittest.main()
