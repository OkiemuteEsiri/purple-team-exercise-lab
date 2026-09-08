# Purple Team Exercise Lab

A controlled, defensive purple-team project that links authorized adversary simulation to telemetry, detection validation, response decisions, and remediation outcomes.

## Purpose

The lab demonstrates how red-team techniques can be converted into measurable defensive improvements without relying on uncontrolled exploitation. Each exercise defines an expected behavior, required telemetry, detection hypothesis, analyst decision path, and remediation action.

## Exercise Workflow

1. Define authorization, scope, objectives, and stop conditions.
2. Select a MITRE ATT&CK technique relevant to the defensive hypothesis.
3. Generate safe synthetic or benign lab activity.
4. Verify telemetry collection.
5. Evaluate whether the expected detection fires.
6. Record analyst triage and response decisions.
7. Identify detection, logging, or hardening gaps.
8. Re-test after remediation.

## Current Scenarios

| Scenario | ATT&CK | Defensive objective |
| --- | --- | --- |
| Suspicious PowerShell execution | T1059.001 | Validate process/script telemetry and alert logic |
| New scheduled task | T1053.005 | Validate persistence-oriented monitoring |
| Privileged group membership change | T1098 | Validate identity-change detection and escalation |

## Repository Structure

- `exercises/exercise_matrix.csv` - synthetic exercise catalogue
- `src/coverage_analyzer.py` - detection-coverage scoring utility
- `tests/test_coverage_analyzer.py` - unit tests
- `docs/exercise-playbook.md` - authorization, execution, validation, and lessons-learned process

## Safety

This repository is for authorized lab validation and defensive engineering. It does not include credential theft, destructive actions, production targeting, persistence payloads, or instructions intended to bypass security controls.
