# Validation Methodology

## Objective

This project measures whether defensive controls produce observable, reviewable outcomes during safe synthetic purple-team exercises. It does not measure offensive success and does not contain exploit or evasion payloads.

## Validation Model

Each exercise is assessed across six evidence gates:

| Gate | Weight | Validation question |
| --- | ---: | --- |
| Telemetry | 20 | Was the expected source telemetry observable? |
| Detection | 25 | Did the expected analytic or alert fire? |
| Analyst triage | 15 | Could an analyst interpret and classify the signal? |
| Response | 15 | Was the expected response decision/path validated? |
| Remediation | 10 | Was a required control improvement implemented? |
| Re-test | 15 | Did a controlled re-test validate the resulting state? |

The numeric score is a compact evidence summary, not a substitute for analyst judgment. Status precedence prevents a high aggregate score from hiding foundational gaps: missing telemetry becomes `telemetry_gap`; missing detection becomes `detection_gap`; a failed post-remediation re-test becomes `revalidation_failed`.

## ATT&CK Mapping

The synthetic exercises currently use:

- `T1059.001` – PowerShell
- `T1053.005` – Scheduled Task/Job: Scheduled Task
- `T1098` – Account Manipulation
- `T1021.001` – Remote Services: Remote Desktop Protocol

ATT&CK mappings are used to organize defensive hypotheses and coverage. They do not prove compromise, technique execution in a production environment, or attribution.

## Evidence Standard

Evidence references in this repository are synthetic identifiers. In a real defensive program, evidence would normally include approved exercise identifiers, log/search references, rule versions, case/ticket references, timestamps, screenshots or exported query results where policy permits, remediation change references, and re-test evidence.

## Trust Boundaries

- Inputs are local synthetic CSV/JSON files.
- The evaluator performs no network access, scanning, credential use, remote execution, or endpoint modification.
- Invalid schemas, duplicate exercise identifiers, malformed ATT&CK identifiers, and non-boolean control values fail closed.
- Administrative closure is kept separate from technical validation.

## Limitations

The project is intentionally offline and provider-neutral. It does not connect to a SIEM, EDR, identity provider, cloud tenant, or production endpoint. Scores are portfolio demonstration logic and should be calibrated before use in an operational security program.
