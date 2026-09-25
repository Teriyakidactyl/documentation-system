"""One canonical operation result with projection-neutral completion semantics."""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Any, Generic, Iterable, TypeVar
from .diagnostic import Diagnostic
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
    status: Status
    completion: Completion
    value: T | None = None
    diagnostics: tuple[Diagnostic, ...] = ()
    failures: tuple[Failure, ...] = ()
    stopped_at: str | None = None

    @classmethod
    def success(cls, value: T | None = None, *, diagnostics: Iterable[Diagnostic] = ()) -> "Result[T]":
        return cls(Status.SUCCESS, Completion.COMPLETE, value, tuple(diagnostics))

    @classmethod
    def failure(cls, failures: Iterable[Failure], *, completion: Completion = Completion.COMPLETE,
                value: T | None = None, diagnostics: Iterable[Diagnostic] = (),
                stopped_at: str | None = None) -> "Result[T]":
        ordered = tuple(sorted(failures, key=lambda item: item.canonical_key()))
        return cls(Status.FAILURE, completion, value, tuple(diagnostics), ordered, stopped_at)

    @property
    def ok(self) -> bool:
        return self.status is Status.SUCCESS

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status.value,
            "completion": self.completion.value,
            "value": self.value,
            "diagnostics": [item.to_dict() for item in self.diagnostics],
            "failures": [item.to_dict() for item in self.failures],
            "stopped_at": self.stopped_at,
        }
