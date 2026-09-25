"""Source-addressable ownership facts."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True, order=True)
class Source:
    module: str
    file: str
    symbol: str | None = None

    def to_dict(self) -> dict[str, str | None]:
        return {"module": self.module, "file": self.file, "symbol": self.symbol}
