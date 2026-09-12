import csv
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from coverage_analyzer import load_exercises, summarize_coverage


class CoverageAnalyzerTests(unittest.TestCase):
    def test_summary_counts_gaps_validated_and_partial(self):
        rows = [
            {"status": "validated", "technique_id": "T1059.001"},
            {"status": "gap", "technique_id": "T1053.005"},
            {"status": "partial", "technique_id": "T1098"},
        ]
        result = summarize_coverage(rows)
        self.assertEqual(result["validated"], 1)
        self.assertEqual(result["gaps"], 1)
        self.assertEqual(result["partial"], 1)
        self.assertEqual(result["coverage_percent"], 50.0)
        self.assertEqual(result["gap_techniques"], ["T1053.005"])
        self.assertEqual(result["partial_techniques"], ["T1098"])

    def test_empty_matrix(self):
        result = summarize_coverage([])
        self.assertEqual(result["coverage_percent"], 0.0)

    def test_duplicate_exercise_ids_are_rejected(self):
        fields = [
            "exercise_id", "technique_id", "technique_name", "telemetry_source",
            "expected_detection", "status",
        ]
        rows = [
            ["PT-001", "T1059.001", "PowerShell", "process", "alert", "validated"],
            ["PT-001", "T1098", "Account Manipulation", "directory", "alert", "gap"],
        ]
        with tempfile.NamedTemporaryFile("w", newline="", suffix=".csv", delete=False) as handle:
            writer = csv.writer(handle)
            writer.writerow(fields)
            writer.writerows(rows)
            path = handle.name
        try:
            with self.assertRaisesRegex(ValueError, "Duplicate exercise_id"):
                load_exercises(path)
        finally:
            Path(path).unlink(missing_ok=True)

    def test_invalid_schema_is_rejected(self):
        with tempfile.NamedTemporaryFile("w", newline="", suffix=".csv", delete=False) as handle:
            handle.write("exercise_id,status\nPT-001,validated\n")
            path = handle.name
        try:
            with self.assertRaisesRegex(ValueError, "schema"):
                load_exercises(path)
        finally:
            Path(path).unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
