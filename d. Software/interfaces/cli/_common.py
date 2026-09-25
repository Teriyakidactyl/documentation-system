"""Common CLI projection behavior."""
from __future__ import annotations
import sys
from typing import Any
from core.projection import json_text
from core.result import Result

def require_success(result: Result[Any]) -> Any:
    if result.ok:
        return result.value
    print(json_text(result), file=sys.stderr)
    raise SystemExit(1)
