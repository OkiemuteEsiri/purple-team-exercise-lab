import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from outcome_evaluator import evaluate_result, load_results, stable_finding_id, summarize_results
from reporting import render_markdown


def sample(**overrides):
    result = {
        "exercise_id": "PT-100",
        "technique_id": "T1059.001",
        "scenario": "Synthetic validation scenario",
        "telemetry_observed": True,
        "detection_fired": True,
        "analyst_triage_completed": True,
        "response_action_validated": True,
        "remediation_applied": True,
        "retest_passed": True,
        "evidence_reference": "SYN-TEST-100",
        "notes": "Synthetic test evidence.",
    }
    result.update(overrides)
    return result


class OutcomeEvaluatorTests(unittest.TestCase):
    def test_fully_validated_scores_100(self):
        result = evaluate_result(sample())
        self.assertEqual(result["validation_score"], 100)
        self.assertEqual(result["validation_status"], "validated")

    def test_telemetry_gap_takes_precedence(self):
        result = evaluate_result(sample(telemetry_observed=False, detection_fired=False))
        self.assertEqual(result["validation_status"], "telemetry_gap")

    def test_detection_gap_is_explicit(self):
        result = evaluate_result(sample(detection_fired=False))
        self.assertEqual(result["validation_status"], "detection_gap")

    def test_failed_retest_is_not_closed(self):
        result = evaluate_result(sample(retest_passed=False))
        self.assertEqual(result["validation_status"], "revalidation_failed")

    def test_finding_id_is_deterministic(self):
        self.assertEqual(stable_finding_id(sample()), stable_finding_id(sample()))

    def test_summary_aggregates_statuses(self):
        results = [
            sample(exercise_id="PT-101"),
            sample(exercise_id="PT-102", telemetry_observed=False, detection_fired=False),
            sample(exercise_id="PT-103", detection_fired=False),
        ]
        summary = summarize_results(results)
        self.assertEqual(summary["total_exercises"], 3)
        self.assertEqual(summary["validated"], 1)
        self.assertEqual(summary["telemetry_gaps"], 1)
        self.assertEqual(summary["detection_gaps"], 1)

    def test_duplicate_results_are_rejected(self):
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as handle:
            json.dump([sample(), sample()], handle)
            path = handle.name
        try:
            with self.assertRaisesRegex(ValueError, "Duplicate exercise_id"):
                load_results(path)
        finally:
            Path(path).unlink(missing_ok=True)

    def test_non_boolean_control_value_is_rejected(self):
        bad = sample(detection_fired="yes")
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as handle:
            json.dump([bad], handle)
            path = handle.name
        try:
            with self.assertRaisesRegex(ValueError, "non-boolean"):
                load_results(path)
        finally:
            Path(path).unlink(missing_ok=True)

    def test_report_contains_safety_and_gap_context(self):
        report = render_markdown([sample(detection_fired=False)])
        self.assertIn("not proof of compromise", report)
        self.assertIn("detection_gap", report)
        self.assertIn("Closure Standard", report)


if __name__ == "__main__":
    unittest.main()
