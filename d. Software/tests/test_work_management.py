from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
import unittest

SOFTWARE = Path(__file__).resolve().parents[1]
if str(SOFTWARE) not in sys.path:
    sys.path.insert(0, str(SOFTWARE))

from repo_manager.automation.work_management import (
    WorkManagementError,
    reconcile_project,
    register_plan,
    register_task,
    setup_project,
    validate_project,
)


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def work_record(work_id: str, kind: str, title: str = "Record") -> str:
    return f"""---
description: >-
  `Consult when` *{work_id} must be inspected* `to` **recover test work state**.
work:
  id: {work_id}
  type: {kind}
  state: ready
---
# {work_id} — {title}
"""


class WorkManagementAutomationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_setup_materializes_current_skeleton_and_metrics_from_existing_work(self) -> None:
        write(
            self.root / ".project/Planning/Plans/P004 Existing.md",
            work_record("P004", "plan"),
        )

        result = setup_project(self.root)

        self.assertTrue((self.root / ".project/README.md").is_file())
        self.assertTrue((self.root / ".project/Archive/Execution/Handoffs").is_dir())
        self.assertFalse((self.root / ".project/Intake").exists())
        metrics = json.loads((self.root / ".project/metrics.json").read_text(encoding="utf-8"))
        self.assertEqual(2, metrics["version"])
        self.assertEqual(5, metrics["ids"]["plan"])
        self.assertNotIn("feedback", metrics["ids"])
        self.assertGreater(result["uids_minted"], 0)

    def test_duplicate_work_id_across_active_and_archive_is_rejected(self) -> None:
        write(
            self.root / ".project/Execution/Tasks/T001 Active.md",
            work_record("T001", "task"),
        )
        write(
            self.root / ".project/Archive/Execution/Tasks/T001 Archived.md",
            work_record("T001", "task"),
        )

        with self.assertRaisesRegex(WorkManagementError, "Duplicate work.id T001"):
            setup_project(self.root)

    def test_legacy_record_work_object_remains_readable_without_active_counter(self) -> None:
        write(
            self.root / ".project/Intake/Feedback/FB007 Legacy.md",
            work_record("FB007", "feedback"),
        )

        result = setup_project(self.root)

        self.assertEqual(1, result["metrics"]["ids"]["plan"])
        self.assertNotIn("feedback", result["metrics"]["ids"])
        validated = validate_project(self.root)
        self.assertEqual(1, validated["legacy_work_objects"])

    def test_reconcile_migrates_version_one_metrics_and_preserves_active_counters(self) -> None:
        setup_project(self.root)
        metrics_path = self.root / ".project/metrics.json"
        metrics_path.write_text(json.dumps({
            "version": 1,
            "ids": {
                "idea": 9,
                "feedback": 8,
                "issue": 7,
                "fault": 6,
                "investigation": 5,
                "decision": 4,
                "plan": 3,
                "task": 20,
                "handoff": 2,
            },
        }), encoding="utf-8")

        repaired = reconcile_project(self.root)

        self.assertEqual(2, repaired["metrics"]["version"])
        self.assertEqual(20, repaired["metrics"]["ids"]["task"])
        self.assertNotIn("idea", repaired["metrics"]["ids"])

    def test_register_task_allocates_monotonically_and_mints_uid(self) -> None:
        setup_project(self.root)
        metrics_path = self.root / ".project/metrics.json"
        metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
        metrics["ids"]["task"] = 9
        metrics_path.write_text(json.dumps(metrics), encoding="utf-8")

        result = register_task(self.root, "Fix publication link")

        self.assertEqual("T009", result["work_id"])
        self.assertTrue(result["uid"])
        task = self.root / result["path"]
        self.assertTrue(task.is_file())
        self.assertIn("state: captured", task.read_text(encoding="utf-8"))
        updated = json.loads(metrics_path.read_text(encoding="utf-8"))
        self.assertEqual(10, updated["ids"]["task"])

    def test_register_plan_allocates_durable_captured_plan(self) -> None:
        setup_project(self.root)
        metrics_path = self.root / ".project/metrics.json"
        metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
        metrics["ids"]["plan"] = 3
        metrics_path.write_text(json.dumps(metrics), encoding="utf-8")

        result = register_plan(self.root, "Refactor work forms")

        self.assertEqual("P003", result["work_id"])
        self.assertTrue(result["uid"])
        plan = self.root / result["path"]
        body = plan.read_text(encoding="utf-8")
        self.assertIn("state: captured", body)
        self.assertIn("## Execution-environment check", body)
        self.assertIn("conversation-only", body)

    def test_validate_rejects_metrics_behind_allocated_ids(self) -> None:
        setup_project(self.root)
        write(
            self.root / ".project/Execution/Tasks/T003 Existing.md",
            work_record("T003", "task"),
        )

        with self.assertRaisesRegex(WorkManagementError, "metrics.json is behind"):
            validate_project(self.root)


if __name__ == "__main__":
    unittest.main()
