"""Canonical failure identity and propagation facts."""
from __future__ import annotations
from dataclasses import dataclass, field, replace
from typing import Any, Mapping
from .source import Source

@dataclass(frozen=True)
class Recovery:
    action: str
    arguments: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {"action": self.action, "arguments": dict(self.arguments)}

@dataclass(frozen=True)
class Failure:
    origin: Source
    name: str
    classification: str
    subject: Mapping[str, Any]
    message: str
    details: Mapping[str, Any] = field(default_factory=dict)
    recovery: tuple[Recovery, ...] = ()
    provenance: tuple[str, ...] = ()
    caused_by: str | None = None
    blocking: tuple[str, ...] = ()

    def with_provenance(self, operation_id: str) -> "Failure":
        if self.provenance and self.provenance[-1] == operation_id:
            return self
        return replace(self, provenance=(*self.provenance, operation_id))

    def canonical_key(self) -> tuple[str, str, str, str, str]:
        subject = repr(sorted((str(k), repr(v)) for k, v in self.subject.items()))
        return (self.origin.file, self.origin.symbol or "", self.name, subject, self.message)

    def to_dict(self) -> dict[str, Any]:
        return {
            "origin": self.origin.to_dict(),
            "name": self.name,
            "classification": self.classification,
            "subject": dict(self.subject),
            "message": self.message,
            "details": dict(self.details),
            "recovery": [item.to_dict() for item in self.recovery],
            "provenance": list(self.provenance),
            "caused_by": self.caused_by,
            "blocking": list(self.blocking),
        }

class ExpectedFailure(Exception):
    def __init__(self, failure: Failure):
        super().__init__(failure.message)
        self.failure = failure
