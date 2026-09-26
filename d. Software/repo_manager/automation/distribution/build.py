"""Build the tracked consumer projection of a source repository."""
from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
import shutil
import subprocess


class DistributionError(RuntimeError):
    """Raised when a consumer distribution cannot be constructed deterministically."""


@dataclass(frozen=True)
class DistributionBuild:
    source_root: Path
    output_root: Path
    source_revision: str
    files: tuple[str, ...]


def _git(root: Path, *arguments: str) -> bytes:
    completed = subprocess.run(
        ["git", "-C", str(root), *arguments],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode != 0:
        message = os.fsdecode(completed.stderr).strip() or "git command failed"
        raise DistributionError(message)
    return completed.stdout


def _repository_root(path: Path) -> Path:
    root = os.fsdecode(_git(path, "rev-parse", "--show-toplevel")).strip()
    if not root:
        raise DistributionError(f"cannot determine Git repository root from {path}")
    return Path(root).resolve()


def _source_revision(root: Path) -> str:
    revision = os.fsdecode(_git(root, "rev-parse", "HEAD")).strip()
    if not revision:
        raise DistributionError(f"cannot determine source revision for {root}")
    return revision


def _tracked_paths(root: Path) -> tuple[Path, ...]:
    raw = _git(root, "ls-files", "-z")
    return tuple(
        Path(os.fsdecode(item))
        for item in raw.split(b"\0")
        if item
    )


def _consumer_visible(path: Path) -> bool:
    return not any(part.startswith(".") for part in path.parts)


def _reset_output(output_root: Path) -> None:
    if output_root.is_symlink() or output_root.is_file():
        output_root.unlink()
    elif output_root.exists():
        shutil.rmtree(output_root)
    output_root.mkdir(parents=True, exist_ok=True)


def _copy(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if source.is_symlink():
        destination.symlink_to(os.readlink(source))
        return
    if source.is_dir():
        shutil.copytree(source, destination, symlinks=True)
        return
    if not source.is_file():
        raise DistributionError(f"tracked source path does not exist: {source}")
    shutil.copy2(source, destination, follow_symlinks=False)


def build_distribution(source_root: Path, output_root: Path) -> DistributionBuild:
    """Build the consumer projection from tracked, non-dot-prefixed paths.

    The source repository's Git index defines membership. Any tracked path with
    a dot-prefixed path component is source-only and omitted. The destination is
    replaced on every build so stale files cannot survive from an earlier
    projection.
    """

    repository_root = _repository_root(source_root.resolve())
    output_root = output_root.resolve()
    if output_root == repository_root:
        raise DistributionError("distribution output cannot replace the source repository")

    source_revision = _source_revision(repository_root)
    tracked = _tracked_paths(repository_root)
    selected = tuple(path for path in tracked if _consumer_visible(path))

    _reset_output(output_root)
    for relative in selected:
        _copy(repository_root / relative, output_root / relative)

    return DistributionBuild(
        source_root=repository_root,
        output_root=output_root,
        source_revision=source_revision,
        files=tuple(path.as_posix() for path in selected),
    )
