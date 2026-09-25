"""Command entry point for self-assembling verification."""

from __future__ import annotations

import json

from .runner import verify


def main() -> None:
    report = verify()
    print(
        json.dumps(
            {
                "operations": report.operations,
                "boundary_verified": report.boundary_verified,
                "generated_operations": report.generated_operations,
                "cases": report.cases,
                "gaps": list(report.gaps),
                "findings": [finding.__dict__ for finding in report.findings],
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    raise SystemExit(0 if report.passed else 1)


if __name__ == "__main__":
    main()
