# Remediation and Revalidation Workflow

A finding is not closed because a task or ticket moved to a completed state. Technical closure requires evidence that the control gap was corrected and the safe validation scenario was re-run.

## Workflow

1. **Classify the gap** – telemetry, detection, triage, response, or control weakness.
2. **Assign ownership** – identify the engineering or security owner responsible for the control.
3. **Record remediation** – capture the change reference and the control change actually implemented.
4. **Validate telemetry first** – confirm required source data is present and sufficiently complete.
5. **Re-run the controlled scenario** – use benign synthetic or lab activity only.
6. **Validate detection and handling** – confirm the expected alert/query, analyst triage, and response path.
7. **Capture evidence** – retain synthetic evidence identifiers in this portfolio; operational programs should follow their evidence-retention policy.
8. **Close only after re-test** – failed re-tests remain open and are classified as `revalidation_failed`.

## Closure Decision Matrix

| Condition | State | Action |
| --- | --- | --- |
| Required telemetry absent | `telemetry_gap` | Restore or onboard telemetry before judging detection efficacy |
| Telemetry present, expected detection absent | `detection_gap` | Tune/create the analytic and re-test |
| Core controls work but evidence/handling incomplete | `partial` | Resolve the missing validation gate and re-test |
| Remediation performed but re-test fails | `revalidation_failed` | Re-open engineering work; do not accept technical closure |
| All evidence gates satisfied | `validated` | Record evidence and retain for regression testing |

## Exception Handling

A documented risk exception can explain why remediation is deferred, but it does not convert an unvalidated technical state into `validated`. Exception governance and control efficacy should remain separate records.
