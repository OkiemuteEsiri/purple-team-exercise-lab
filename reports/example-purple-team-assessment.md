# Purple Team Validation Assessment

> Synthetic defensive validation output. ATT&CK mappings provide threat-model context and do not establish compromise or attribution.

## Executive Summary

- Exercises evaluated: **4**
- Fully validated: **1**
- Partial: **1**
- Telemetry gaps: **1**
- Detection gaps: **1**
- Revalidation failures: **0**
- Average validation score: **55.0 / 100**

## Exercise Outcomes

| Exercise | ATT&CK | Status | Score | Evidence |
| --- | --- | --- | ---: | --- |
| PT-004 – Unusual remote interactive logon visibility | T1021.001 | `telemetry_gap` | 0 | SYN-EVID-004 |
| PT-002 – Scheduled task creation monitoring | T1053.005 | `detection_gap` | 30 | SYN-EVID-002 |
| PT-001 – Suspicious PowerShell execution telemetry | T1059.001 | `partial` | 90 | SYN-EVID-001 |
| PT-003 – Privileged group membership change monitoring | T1098 | `validated` | 100 | SYN-EVID-003 |

## Priority Findings

### PT-004 – Telemetry coverage gap

The synthetic remote-interactive-logon scenario has no observable source telemetry. Detection efficacy cannot be assessed until the required authentication/session telemetry is available. Remediation priority is telemetry onboarding and data-quality validation before detection tuning.

### PT-002 – Detection gap

The expected scheduled-task source event was present, but the expected analytic did not fire. The control remains open until the detection is tuned or corrected and a controlled re-test succeeds.

### PT-001 – Partial validation

Telemetry, detection, analyst triage, response path, and re-test evidence are present. The portfolio fixture intentionally records no remediation action because none was required for this validated control path; the generic scoring model therefore reports a partial score. This illustrates an explicit model limitation that would be calibrated in an operational program.

## Closure Standard

Administrative task completion is not treated as technical closure. Gap closure requires appropriate source telemetry, the expected detection behavior, analyst/response validation where applicable, documented control changes when remediation is required, and a passing controlled re-test.
