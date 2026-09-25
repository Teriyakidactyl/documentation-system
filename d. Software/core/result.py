"""Canonical Software operation result."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Generic, TypeVar

from .failure import Failure

T = TypeVar("T")


class Status(str, Enum):
    SUCCESS = "success"
    FAILURE = "failure"


class Completion(str, Enum):
    COMPLETE = "complete"
    PARTIAL = "partial"


@dataclass(frozen=True)
class Result(Generic[T]):
    """One canonical result from which consumer projections can be derived."""

    status: Status
    completion: Completion
    value: T | None = None
    diagnostics: tuple[Any, ...] = ()
    failures: tuple[Failure, ...] = ()
    stopped_at: str | None = None

    def __post_init__(self) -> None:
        if self.status is Status.SUCCESS and self.failures:
            raise ValueError("successful Result cannot contain failures")
        if self.status is Status.FAILURE and not self.failures:
            raise ValueError("failed Result requires at least one failure")
        if self.completion is Completion.PARTIAL and not self.stopped_at:
            raise ValueError("partial Result requires stopped_at")

    @classmethod
    def success(
        cls,
        value: T | None = None,
        *,
        diagnostics: tuple[Any, ...] = (),
    ) -> "Result[T]":
        return cls(Status.SUCCESS, Completion.COMPLETE, value=value, diagnostics=diagnostics)

    @classmethod
    def failure(
        cls,
        *failures: Failure,
        completion: Completion = Completion.COMPLETE,
        stopped_at: str | None = None,
        value: T | None = None,
        diagnostics: tuple[Any, ...] = (),
    ) -> "Result[T]":
        return cls(
            Status.FAILURE,
            completion,
            value=value,
            diagnostics=diagnostics,
            failures=tuple(failures),
            stopped_at=stopped_at,
        )
