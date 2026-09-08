import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from coverage_analyzer import summarize_coverage


class CoverageAnalyzerTests(unittest.TestCase):
    def test_summary_counts_gaps_and_validated(self):
        rows = [
            {"status": "validated", "technique_id": "T1059.001"},
            {"status": "gap", "technique_id": "T1053.005"},
            {"status": "validated", "technique_id": "T1098"},
        ]
        result = summarize_coverage(rows)
        self.assertEqual(result["validated"], 2)
        self.assertEqual(result["gaps"], 1)
        self.assertEqual(result["coverage_percent"], 66.67)
        self.assertEqual(result["gap_techniques"], ["T1053.005"])

    def test_empty_matrix(self):
        result = summarize_coverage([])
        self.assertEqual(result["coverage_percent"], 0.0)


if __name__ == "__main__":
    unittest.main()
