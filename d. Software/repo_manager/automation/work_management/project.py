"""Own repository-local Work Management setup, allocation, and validation."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
import json
from pathlib import Path
import re
from typing import Any

from repo_manager.capabilities.frontmatter import FrontmatterError, load as load_frontmatter
from repo_manager.automation.organizing.model import (
    OrganizingError,
    add_uid_to_metadata,
    generate_uid,
    load_artifacts,
)

METRICS_VERSION = 2

KIND_PREFIX = {
    "investigation": "R",
    "decision": "D",
    "plan": "P",
    "task": "T",
    "handoff": "H",
}

LEGACY_KIND_PREFIX = {
    "idea": "I",
    "feedback": "FB",
    "issue": "IS",
    "fault": "F",
}

ALL_KIND_PREFIX = {**LEGACY_KIND_PREFIX, **KIND_PREFIX}

KIND_HOME = {
    "investigation": "Planning/Investigations",
    "decision": "Planning/Decisions",
    "plan": "Planning/Plans",
    "task": "Execution/Tasks",
    "handoff": "Execution/Handoffs",
}

LEAF_DIRS = (
    "Planning/Plans",
    "Planning/Investigations",
    "Planning/Decisions",
    "Execution/Tasks",
    "Execution/Handoffs",
    "Archive/Planning/Plans",
    "Archive/Planning/Investigations",
    "Archive/Planning/Decisions",
    "Archive/Execution/Tasks",
    "Archive/Execution/Handoffs",
)

PROJECT_README = """---
description: >-
  `Consult when` *repository-local work state must be resumed or inspected*
  `to` **locate Work Management objects without treating them as current
  product authority**.
---
# Project Work

This controlled sideband holds mutable Work Management state for this repository.

Planning, Execution, and Archive are the stable responsibility layer.
Repository automation maintains `metrics.json` for active standalone Work ID
allocation. Retained Records remain outside Work Management unless executable
work is deliberately created from them.
"""


class WorkManagementError(RuntimeError):
    """Raised when repository Work Management state is invalid or unsafe to mutate."""


@dataclass(frozen=True)
class WorkRecord:
    path: Path
    work_id: str
    kind: str
    number: int


def _project_root(corpus_root: Path) -> Path:
    return corpus_root.resolve() / ".project"


def _metrics_path(corpus_root: Path) -> Path:
    return _project_root(corpus_root) / "metrics.json"


def _relative(corpus_root: Path, path: Path) -> str:
    return path.resolve().relative_to(corpus_root.resolve()).as_posix()


def _normalize_root(corpus_root: Path) -> Path:
    root = corpus_root.resolve()
    if not root.is_dir():
        raise WorkManagementError(f"Repository root is not a directory: {root}")
    return root


def _work_metadata(path: Path) -> dict[str, Any] | None:
    try:
        parsed = load_frontmatter(path)
    except FrontmatterError as exc:
        raise WorkManagementError(f"{path}: invalid controlled frontmatter: {exc}") from exc
    if parsed is None:
        return None
    work = parsed.data.get("work")
    if work is None:
        return None
    if not isinstance(work, dict):
        raise WorkManagementError(f"{path}: work must be a mapping")
    return work


def scan_work_objects(corpus_root: Path) -> tuple[WorkRecord, ...]:
    root = _normalize_root(corpus_root)
    project = _project_root(root)
    if not project.exists():
        return ()

    records: list[WorkRecord] = []
    seen: dict[str, Path] = {}
    for path in sorted(project.rglob("*.md"), key=lambda item: item.as_posix().casefold()):
        if path.is_symlink():
            continue
        work = _work_metadata(path)
        if work is None:
            continue
        kind = work.get("type")
        work_id = work.get("id")
        if not isinstance(kind, str) or kind not in ALL_KIND_PREFIX:
            raise WorkManagementError(
                f"{_relative(root, path)}: unsupported or missing work.type {kind!r}"
            )
        if not isinstance(work_id, str):
            raise WorkManagementError(f"{_relative(root, path)}: work.id must be a string")
        prefix = ALL_KIND_PREFIX[kind]
        match = re.fullmatch(re.escape(prefix) + r"([0-9]+)", work_id)
        if match is None:
            raise WorkManagementError(
                f"{_relative(root, path)}: work.id {work_id!r} does not match "
                f"{kind} prefix {prefix!r}"
            )
        previous = seen.get(work_id)
        if previous is not None:
            raise WorkManagementError(
                f"Duplicate work.id {work_id}: {_relative(root, previous)} and "
                f"{_relative(root, path)}"
            )
        seen[work_id] = path
        records.append(WorkRecord(path, work_id, kind, int(match.group(1))))
    return tuple(records)


def _derived_next(records: tuple[WorkRecord, ...]) -> dict[str, int]:
    next_ids = {kind: 1 for kind in KIND_PREFIX}
    for record in records:
        if record.kind in next_ids:
            next_ids[record.kind] = max(next_ids[record.kind], record.number + 1)
    return next_ids


def _read_metrics(corpus_root: Path) -> dict[str, Any] | None:
    path = _metrics_path(corpus_root)
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise WorkManagementError(f"{_relative(corpus_root, path)}: invalid JSON: {exc}") from exc
    if not isinstance(payload, dict) or payload.get("version") not in {1, METRICS_VERSION}:
        raise WorkManagementError(
            f"{_relative(corpus_root, path)}: version must be 1 or {METRICS_VERSION}"
        )
    ids = payload.get("ids")
    if not isinstance(ids, dict):
        raise WorkManagementError(f"{_relative(corpus_root, path)}: ids must be an object")

    for kind in KIND_PREFIX:
        value = ids.get(kind)
        if not isinstance(value, int) or isinstance(value, bool) or value < 1:
            raise WorkManagementError(
                f"{_relative(corpus_root, path)}: ids.{kind} must be an integer >= 1"
            )

    if payload.get("version") == METRICS_VERSION:
        unknown = sorted(set(ids) - set(KIND_PREFIX))
        if unknown:
            raise WorkManagementError(
                f"{_relative(corpus_root, path)}: unknown active id counters: "
                + ", ".join(unknown)
            )
    return payload


def _write_metrics(corpus_root: Path, payload: dict[str, Any]) -> None:
    path = _metrics_path(corpus_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + ".tmp")
    temp.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    temp.replace(path)


def reconciled_metrics(corpus_root: Path) -> dict[str, Any]:
    records = scan_work_objects(corpus_root)
    derived = _derived_next(records)
    existing = _read_metrics(corpus_root)
    ids = dict(derived)
    if existing is not None:
        for kind in KIND_PREFIX:
            ids[kind] = max(ids[kind], existing["ids"][kind])
    return {"version": METRICS_VERSION, "ids": ids}


def _mint_project_uids(corpus_root: Path) -> int:
    root = _normalize_root(corpus_root)
    try:
        artifacts = load_artifacts(root)
    except OrganizingError as exc:
        raise WorkManagementError(str(exc)) from exc
    used = {artifact.uid for artifact in artifacts.values() if artifact.uid is not None}
    created = 0
    for path, artifact in sorted(
        artifacts.items(), key=lambda pair: pair[0].as_posix().casefold()
    ):
        try:
            rel = path.resolve().relative_to(root)
        except ValueError:
            continue
        if not rel.parts or rel.parts[0] != ".project" or artifact.uid is not None:
            continue
        uid = generate_uid(used)
        add_uid_to_metadata(path, uid)
        used.add(uid)
        created += 1
    return created


def _ensure_skeleton(corpus_root: Path) -> list[str]:
    root = _normalize_root(corpus_root)
    project = _project_root(root)
    created: list[str] = []
    project.mkdir(parents=True, exist_ok=True)

    readme = project / "README.md"
    if not readme.exists():
        readme.write_text(PROJECT_README, encoding="utf-8")
        created.append(_relative(root, readme))

    for relative in LEAF_DIRS:
        leaf = project / relative
        if not leaf.exists():
            leaf.mkdir(parents=True, exist_ok=True)
            created.append(_relative(root, leaf) + "/")
        if not any(leaf.iterdir()):
            anchor = leaf / ".gitkeep"
            anchor.write_text("", encoding="utf-8")
            created.append(_relative(root, anchor))
    return created


def setup_project(corpus_root: Path) -> dict[str, Any]:
    root = _normalize_root(corpus_root)
    created = _ensure_skeleton(root)
    metrics = reconciled_metrics(root)
    before = _metrics_path(root).read_text(encoding="utf-8") if _metrics_path(root).exists() else None
    rendered = json.dumps(metrics, indent=2, ensure_ascii=False) + "\n"
    if before != rendered:
        _write_metrics(root, metrics)
        if before is None:
            created.append(".project/metrics.json")
    minted = _mint_project_uids(root)
    validate_project(root)
    return {"created": created, "uids_minted": minted, "metrics": metrics}


def reconcile_project(corpus_root: Path) -> dict[str, Any]:
    root = _normalize_root(corpus_root)
    _ensure_skeleton(root)
    metrics = reconciled_metrics(root)
    before = _metrics_path(root).read_text(encoding="utf-8") if _metrics_path(root).exists() else None
    rendered = json.dumps(metrics, indent=2, ensure_ascii=False) + "\n"
    changed = before != rendered
    if changed:
        _write_metrics(root, metrics)
    minted = _mint_project_uids(root)
    validate_project(root)
    return {"changed": changed or minted > 0, "uids_minted": minted, "metrics": metrics}


def validate_project(corpus_root: Path) -> dict[str, Any]:
    root = _normalize_root(corpus_root)
    project = _project_root(root)
    if not project.is_dir():
        raise WorkManagementError(".project/ is not initialized")
    missing = [relative for relative in LEAF_DIRS if not (project / relative).is_dir()]
    if not (project / "README.md").is_file():
        missing.insert(0, "README.md")
    if missing:
        raise WorkManagementError(
            "Incomplete .project skeleton; missing: " + ", ".join(missing)
        )
    records = scan_work_objects(root)
    metrics = _read_metrics(root)
    if metrics is None:
        raise WorkManagementError(".project/metrics.json is missing")
    required = _derived_next(records)
    behind = [
        f"{kind}={metrics['ids'][kind]} requires >= {required[kind]}"
        for kind in KIND_PREFIX
        if metrics["ids"][kind] < required[kind]
    ]
    if behind:
        raise WorkManagementError(
            ".project/metrics.json is behind allocated Work IDs: " + "; ".join(behind)
        )
    return {
        "work_objects": len(records),
        "legacy_work_objects": sum(1 for record in records if record.kind in LEGACY_KIND_PREFIX),
        "metrics": metrics,
        "max_allocated": {kind: required[kind] - 1 for kind in KIND_PREFIX},
    }


def _safe_title(title: str) -> str:
    compact = " ".join(title.split()).strip()
    if not compact:
        raise WorkManagementError("Work title must not be empty")
    compact = re.sub(r'[\\/:*?"<>|]+', "-", compact).strip(" .-")
    if not compact:
        raise WorkManagementError("Work title has no safe filename characters")
    return compact


def _task_text(work_id: str, title: str) -> str:
    today = date.today().isoformat()
    return f"""---
description: >-
  `Consult when` *task {work_id} must be resumed or inspected* `to` **recover
  its outcome, current state, and next action**.
work:
  id: {work_id}
  type: task
  state: captured
  updated: '{today}'
---
# {work_id} — {title}

## Outcome

{title}

## Acceptance conditions

- Define the observable condition that proves this outcome complete.

## Current state

Captured. Acceptance and starting conditions have not yet been established.

## Next action

Apply the Task Form and establish acceptance, capability constraints, and
actionability.
"""


def _plan_text(work_id: str, title: str) -> str:
    today = date.today().isoformat()
    return f"""---
description: >-
  `Consult when` *plan {work_id} must be resumed or inspected* `to` **recover
  its intended outcome and continue durable planning without prior conversation**.
work:
  id: {work_id}
  type: plan
  state: captured
  updated: '{today}'
---
# {work_id} — {title}

> [!WARNING]
> This Plan is durable repository state. Do not replace it with conversation-only
> planning.

## Outcome

{title}

## Acceptance conditions

- Define the observable conditions that make the Plan outcome complete.

## Execution-environment check

Before execution, assess the current harness capabilities and material limits.

## Tasks

No executable decomposition has been established yet.

## Current state

Captured. Planning preparation and decomposition remain incomplete.

## Next action

Apply Planning guidance and the Plan Form to establish informed executable work.
"""


def _register(corpus_root: Path, title: str, kind: str, renderer) -> dict[str, Any]:
    root = _normalize_root(corpus_root)
    if kind not in {"task", "plan"}:
        raise WorkManagementError(f"Unsupported registration kind: {kind}")
    setup_project(root)
    records = scan_work_objects(root)
    metrics = reconciled_metrics(root)
    number = metrics["ids"][kind]
    used = {record.work_id for record in records}
    prefix = KIND_PREFIX[kind]
    while True:
        work_id = f"{prefix}{number:03d}"
        if work_id not in used:
            break
        number += 1

    safe_title = _safe_title(title)
    target_dir = _project_root(root) / KIND_HOME[kind]
    path = target_dir / f"{work_id} {safe_title}.md"
    if path.exists():
        raise WorkManagementError(f"Work path already exists: {_relative(root, path)}")

    metrics_path = _metrics_path(root)
    metrics_before = metrics_path.read_text(encoding="utf-8")
    anchor = target_dir / ".gitkeep"
    anchor_existed = anchor.exists()

    try:
        path.write_text(renderer(work_id, safe_title), encoding="utf-8")
        if anchor_existed:
            anchor.unlink()
        metrics["ids"][kind] = number + 1
        _write_metrics(root, metrics)
        _mint_project_uids(root)
        validate_project(root)
    except Exception:
        if path.exists():
            path.unlink()
        metrics_path.write_text(metrics_before, encoding="utf-8")
        if anchor_existed and not anchor.exists():
            anchor.write_text("", encoding="utf-8")
        raise

    parsed = load_frontmatter(path)
    uid = parsed.data.get("uid") if parsed is not None else None
    return {
        "work_id": work_id,
        "path": _relative(root, path),
        "uid": uid,
        "state": "captured",
        "metrics": metrics,
    }


def register_task(corpus_root: Path, title: str) -> dict[str, Any]:
    return _register(corpus_root, title, "task", _task_text)


def register_plan(corpus_root: Path, title: str) -> dict[str, Any]:
    return _register(corpus_root, title, "plan", _plan_text)
