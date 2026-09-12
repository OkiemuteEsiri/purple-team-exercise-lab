from __future__ import annotations

import csv
import sys
from collections import Counter
from pathlib import Path

VALID_STATUSES = {"validated", "gap", "partial"}
EXPECTED_FIELDS = {
    "exercise_id",
    "technique_id",
    "technique_name",
    "telemetry_source",
    "expected_detection",
    "status",
}


def load_exercises(path: str | Path) -> list[dict[str, str]]:
    with open(path, newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if set(reader.fieldnames or []) != EXPECTED_FIELDS:
            raise ValueError("Exercise matrix schema does not match the expected fields")
        rows = list(reader)

    seen_ids: set[str] = set()
    for index, row in enumerate(rows, start=2):
        if any(not str(row[field]).strip() for field in EXPECTED_FIELDS):
            raise ValueError(f"Blank required value on CSV row {index}")
        if row["status"] not in VALID_STATUSES:
            raise ValueError(f"Unsupported status: {row['status']}")
        if row["exercise_id"] in seen_ids:
            raise ValueError(f"Duplicate exercise_id: {row['exercise_id']}")
        if not row["technique_id"].startswith("T"):
            raise ValueError(f"Invalid ATT&CK technique identifier: {row['technique_id']}")
        seen_ids.add(row["exercise_id"])
    return rows


def summarize_coverage(rows: list[dict[str, str]]) -> dict[str, object]:
    counts = Counter(row["status"] for row in rows)
    total = len(rows)
    validated = counts["validated"]
    scored = validated + (0.5 * counts["partial"])
    return {
        "total_exercises": total,
        "validated": validated,
        "gaps": counts["gap"],
        "partial": counts["partial"],
        "coverage_percent": round(scored / total * 100, 2) if total else 0.0,
        "gap_techniques": sorted({row["technique_id"] for row in rows if row["status"] == "gap"}),
        "partial_techniques": sorted({row["technique_id"] for row in rows if row["status"] == "partial"}),
    }


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python src/coverage_analyzer.py <exercise_matrix.csv>")
    print(summarize_coverage(load_exercises(sys.argv[1])))


if __name__ == "__main__":
    main()
