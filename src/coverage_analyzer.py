from __future__ import annotations

import csv
import sys
from collections import Counter
from pathlib import Path

VALID_STATUSES = {"validated", "gap", "partial"}


def load_exercises(path: str | Path) -> list[dict[str, str]]:
    with open(path, newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    for row in rows:
        if row["status"] not in VALID_STATUSES:
            raise ValueError(f"Unsupported status: {row['status']}")
    return rows


def summarize_coverage(rows: list[dict[str, str]]) -> dict[str, object]:
    counts = Counter(row["status"] for row in rows)
    total = len(rows)
    validated = counts["validated"]
    return {
        "total_exercises": total,
        "validated": validated,
        "gaps": counts["gap"],
        "partial": counts["partial"],
        "coverage_percent": round(validated / total * 100, 2) if total else 0.0,
        "gap_techniques": [row["technique_id"] for row in rows if row["status"] == "gap"],
    }


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python src/coverage_analyzer.py <exercise_matrix.csv>")
    print(summarize_coverage(load_exercises(sys.argv[1])))


if __name__ == "__main__":
    main()
