"""Projection helpers over the canonical Result."""
from __future__ import annotations
import json
from typing import Any
from .result import Result

def json_text(result: Result[Any]) -> str:
    return json.dumps(result.to_dict(), indent=2, ensure_ascii=False, default=str)

def first_failure_message(result: Result[Any]) -> str:
    return result.failures[0].message if result.failures else "operation failed"
