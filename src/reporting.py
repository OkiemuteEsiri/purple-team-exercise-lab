from __future__ import annotations

from typing import Any

from outcome_evaluator import evaluate_all, summarize_results


def render_markdown(results: list[dict[str, Any]]) -> str:
    evaluated = evaluate_all(results)
    summary = summarize_results(results)
    lines = [
        "# Purple Team Validation Assessment",
        "",
        "> Synthetic defensive validation output. ATT&CK mappings provide threat-model context and do not establish compromise or attribution.",
        "",
        "## Executive Summary",
        "",
        f"- Exercises evaluated: **{summary['total_exercises']}**",
        f"- Fully validated: **{summary['validated']}**",
        f"- Partial: **{summary['partial']}**",
        f"- Telemetry gaps: **{summary['telemetry_gaps']}**",
        f"- Detection gaps: **{summary['detection_gaps']}**",
        f"- Revalidation failures: **{summary['revalidation_failures']}**",
        f"- Average validation score: **{summary['average_validation_score']} / 100**",
        "",
        "## Exercise Outcomes",
        "",
        "| Finding | Exercise | ATT&CK | Status | Score | Evidence |",
        "| --- | --- | --- | --- | ---: | --- |",
    ]
    for item in sorted(evaluated, key=lambda row: (row["validation_score"], row["exercise_id"])):
        lines.append(
            f"| `{item['finding_id']}` | {item['exercise_id']} – {item['scenario']} | "
            f"{item['technique_id']} | `{item['validation_status']}` | {item['validation_score']} | "
            f"{item['evidence_reference']} |"
        )

    lines.extend(["", "## Gap Interpretation", ""])
    for item in evaluated:
        if item["validation_status"] == "validated":
            continue
        lines.append(f"### {item['exercise_id']} – {item['scenario']}")
        lines.append("")
        lines.append(f"- **ATT&CK:** {item['technique_id']}")
        lines.append(f"- **Status:** `{item['validation_status']}`")
        lines.append(f"- **Evidence:** {item['evidence_reference']}")
        lines.append(f"- **Notes:** {item['notes'] or 'No additional analyst note.'}")
        lines.append("- **Required action:** close the identified telemetry/detection/response gap, capture evidence, and re-run the safe validation scenario.")
        lines.append("")

    lines.extend([
        "## Closure Standard",
        "",
        "An exercise is not treated as technically closed because a ticket was updated. Closure requires evidence that telemetry is present, the expected detection fires, analyst handling is validated, remediation is applied where required, and the controlled re-test passes.",
        "",
    ])
    return "\n".join(lines)
