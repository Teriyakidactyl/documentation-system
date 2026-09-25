"""Canonical diagnostic representation."""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping
from .source import Source

class Severity(str, Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"

@dataclass(frozen=True)
class Diagnostic:
    code: str
    severity: Severity
    message: str
    subject: Mapping[str, Any] = field(default_factory=dict)
    origin: Source | None = None
    details: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "severity": self.severity.value,
            "message": self.message,
            "subject": dict(self.subject),
            "origin": self.origin.to_dict() if self.origin else None,
            "details": dict(self.details),
        }
