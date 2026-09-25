"""Source-addressable ownership values used by Software contracts."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class SourceAddress:
    """Stable source ownership without making line numbers part of identity."""

    module: str
    file: str
    symbol: str

    def to_dict(self) -> dict[str, str]:
        return {"module": self.module, "file": self.file, "symbol": self.symbol}
