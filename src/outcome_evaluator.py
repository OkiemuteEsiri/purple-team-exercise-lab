from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

REQUIRED_FIELDS = {
    "exercise_id",
    "technique_id",
    "scenario",
    "telemetry_observed",
    "detection_fired",
    "analyst_triage_completed",
    "response_action_validated",
    "remediation_applied",
    "retest_passed",
    "evidence_reference",
    "notes",
}
BOOLEAN_FIELDS = {
    "telemetry_observed",
    "detection_fired",
    "analyst_triage_completed",
    "response_action_validated",
    "remediation_applied",
    "retest_passed",
}


def load_results(path: str | Path) -> list[dict[str, Any]]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("Results document must contain a JSON array")

    seen: set[str] = set()
    for index, item in enumerate(data, start=1):
        if not isinstance(item, dict) or set(item) != REQUIRED_FIELDS:
            raise ValueError(f"Result {index} does not match the expected schema")
        if item["exercise_id"] in seen:
            raise ValueError(f"Duplicate exercise_id: {item['exercise_id']}")
        if not str(item["technique_id"]).startswith("T"):
            raise ValueError(f"Invalid ATT&CK technique identifier: {item['technique_id']}")
        if any(not isinstance(item[field], bool) for field in BOOLEAN_FIELDS):
            raise ValueError(f"Result {item['exercise_id']} contains a non-boolean control value")
        if not str(item["scenario"]).strip() or not str(item["evidence_reference"]).strip():
            raise ValueError(f"Result {item['exercise_id']} is missing scenario or evidence reference")
        seen.add(item["exercise_id"])
    return data


def stable_finding_id(result: dict[str, Any]) -> str:
    material = f"{result['exercise_id']}|{result['technique_id']}|{result['scenario']}"
    return "PT-" + hashlib.sha256(material.encode("utf-8")).hexdigest()[:12].upper()


def evaluate_result(result: dict[str, Any]) -> dict[str, Any]:
    score = 0
    score += 20 if result["telemetry_observed"] else 0
    score += 25 if result["detection_fired"] else 0
    score += 15 if result["analyst_triage_completed"] else 0
    score += 15 if result["response_action_validated"] else 0
    score += 10 if result["remediation_applied"] else 0
    score += 15 if result["retest_passed"] else 0

    if not result["telemetry_observed"]:
        status = "telemetry_gap"
    elif not result["detection_fired"]:
        status = "detection_gap"
    elif not result["retest_passed"] and result["remediation_applied"]:
        status = "revalidation_failed"
    elif score == 100:
        status = "validated"
    else:
        status = "partial"

    return {
        **result,
        "finding_id": stable_finding_id(result),
        "validation_score": score,
        "validation_status": status,
        "attack_mapping": {
            "technique_id": result["technique_id"],
            "interpretation": "Defensive validation context; not proof of compromise or attribution.",
        },
    }


def evaluate_all(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [evaluate_result(result) for result in results]


def summarize_results(results: list[dict[str, Any]]) -> dict[str, Any]:
    evaluated = evaluate_all(results)
    counts = Counter(item["validation_status"] for item in evaluated)
    average = round(sum(item["validation_score"] for item in evaluated) / len(evaluated), 2) if evaluated else 0.0
    return {
        "total_exercises": len(evaluated),
        "validated": counts["validated"],
        "partial": counts["partial"],
        "telemetry_gaps": counts["telemetry_gap"],
        "detection_gaps": counts["detection_gap"],
        "revalidation_failures": counts["revalidation_failed"],
        "average_validation_score": average,
    }
