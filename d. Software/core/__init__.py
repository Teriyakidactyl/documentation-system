"""Shared Software contracts with no domain-specific semantics."""

from .failure import Failure
from .operation import Operation
from .registry import operations, register
from .result import Completion, Result, Status
from .source import SourceAddress

__all__ = [
    "Completion",
    "Failure",
    "Operation",
    "Result",
    "SourceAddress",
    "Status",
    "operations",
    "register",
]
