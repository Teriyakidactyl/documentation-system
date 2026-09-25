"""Shared Software contracts with no representation or workflow semantics."""

from .diagnostic import Diagnostic, Severity
from .execution import invoke
from .failure import ExpectedFailure, Failure, Recovery
from .operation import Effects, Operation, Probe, Verification
from .registry import all_operations, register
from .result import Completion, Result, Status
from .schema import Field, InputSchema
from .source import Source

__all__ = [
    "Completion", "Diagnostic", "Effects", "ExpectedFailure", "Failure",
    "Field", "InputSchema", "Operation", "Probe", "Recovery", "Result",
    "Severity", "Source", "Status", "Verification", "all_operations",
    "invoke", "register",
]
