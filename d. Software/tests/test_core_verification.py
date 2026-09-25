from __future__ import annotations

import unittest

from core.execution import execute
from core.failure import Failure
from core.registry import get
from core.result import Completion, Result, Status
from core.source import SourceAddress
from verification.discovery import discover
from verification.runner import verify


class CoreResultTests(unittest.TestCase):
    def test_provenance_preserves_origin_and_identity(self) -> None:
        origin = SourceAddress("example.owner", "example.py", "parse")
        failure = Failure(origin=origin, name="MALFORMED", message="bad input")

        propagated = failure.through("parent.inspect").through("system.refresh")

        self.assertEqual(origin, propagated.origin)
        self.assertEqual((origin, "MALFORMED"), propagated.identity)
        self.assertEqual(("parent.inspect", "system.refresh"), propagated.provenance)

    def test_partial_result_requires_stop_boundary(self) -> None:
        failure = Failure(
            origin=SourceAddress("example.owner", "example.py", "run"),
            name="STOPPED",
            message="stopped",
        )
        with self.assertRaisesRegex(ValueError, "partial Result requires stopped_at"):
            Result.failure(failure, completion=Completion.PARTIAL)

    def test_success_cannot_contain_failure(self) -> None:
        failure = Failure(
            origin=SourceAddress("example.owner", "example.py", "run"),
            name="FAILED",
            message="failed",
        )
        with self.assertRaisesRegex(ValueError, "successful Result cannot contain failures"):
            Result(
                status=Status.SUCCESS,
                completion=Completion.COMPLETE,
                failures=(failure,),
            )


class OperationVerificationTests(unittest.TestCase):
    def setUp(self) -> None:
        discover()

    def test_discovery_finds_declared_capability_operations(self) -> None:
        identifiers = {operation.id for operation in discover()}
        self.assertIn("yaml.parse", identifiers)
        self.assertIn("frontmatter.parse", identifiers)

    def test_yaml_semantic_failure_has_source_addressable_origin(self) -> None:
        result = execute(get("yaml.parse"), {"text": "[unterminated"})

        self.assertEqual(Status.FAILURE, result.status)
        failure = result.failures[0]
        self.assertEqual("_capabilities.yaml", failure.origin.module)
        self.assertEqual("MALFORMED", failure.name)
        self.assertEqual("malformed", failure.classification)

    def test_schema_failure_is_structured_at_execution_boundary(self) -> None:
        result = execute(get("frontmatter.parse"), {"text": "---\n---\n"})

        self.assertEqual(Status.FAILURE, result.status)
        failure = result.failures[0]
        self.assertEqual("core.execution", failure.origin.module)
        self.assertEqual("REQUIRED_INPUT_MISSING", failure.name)
        self.assertEqual({"operation": "frontmatter.parse"}, dict(failure.subject))

    def test_self_assembled_baseline_passes_for_current_declared_surface(self) -> None:
        report = verify()

        self.assertGreaterEqual(report.operations, 2)
        self.assertEqual(report.operations, report.boundary_verified)
        self.assertEqual((), report.gaps)
        self.assertEqual((), report.findings)


if __name__ == "__main__":
    unittest.main()
