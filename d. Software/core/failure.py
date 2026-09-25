"""Canonical semantic failure values."""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Any, Mapping

from .source import SourceAddress


@dataclass(frozen=True)
class Failure:
    """One semantic failure whose origin survives propagation."""

    origin: SourceAddress
    name: str
    message: str
    classification: str | None = None
    subject: Mapping[str, Any] = field(default_factory=dict)
    details: Mapping[str, Any] = field(default_factory=dict)
    recovery: Mapping[str, Any] = field(default_factory=dict)
    provenance: tuple[str, ...] = ()

    @property
    def identity(self) -> tuple[SourceAddress, str]:
        return self.origin, self.name

    def through(self, operation: str) -> "Failure":
        """Append one meaningful operation boundary without changing origin."""

        if self.provenance and self.provenance[-1] == operation:
            return self
        return replace(self, provenance=(*self.provenance, operation))

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "origin": self.origin.to_dict(),
            "name": self.name,
            "message": self.message,
            "subject": dict(self.subject),
            "details": dict(self.details),
            "recovery": dict(self.recovery),
            "provenance": list(self.provenance),
        }
        if self.classification is not None:
            payload["classification"] = self.classification
        return payload
