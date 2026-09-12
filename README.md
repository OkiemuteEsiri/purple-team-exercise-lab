# Purple Team Exercise Lab

A defensive purple-team validation project that converts controlled, synthetic ATT&CK-aligned exercises into measurable evidence about telemetry, detection, analyst triage, response handling, remediation, and revalidation.

This repository is designed for recruiter and technical-review use: it demonstrates how purple-team activity can become a repeatable security-engineering feedback loop without relying on uncontrolled exploitation or production targeting.

## Problem Statement

ATT&CK coverage counts alone do not show that a security control works. A useful purple-team program must answer harder questions:

- Was the required telemetry actually present?
- Did the intended detection fire?
- Could an analyst triage the signal correctly?
- Was the expected response path usable?
- If a gap was remediated, did a controlled re-test prove the new state?

This project models those questions explicitly and keeps administrative closure separate from technical validation.

## Recruiter Signal at a Glance

| Capability | Evidence in this repository |
| --- | --- |
| Purple-team program design | exercise matrix and authorization/validation playbook |
| Detection engineering | telemetry/detection gap classification and ATT&CK-aligned hypotheses |
| Security automation | deterministic Python evaluators and Markdown report generation |
| Evidence governance | strict schemas, duplicate rejection, evidence references, fail-closed validation |
| Remediation validation | explicit re-test requirements and `revalidation_failed` state |
| Defensive reporting | synthetic executive/analyst assessment output |
| Software quality | unit tests, compilation checks, least-privilege GitHub Actions workflow |

For a fast technical review, see [`docs/recruiter-review.md`](docs/recruiter-review.md).

## Architecture

```text
exercises/exercise_matrix.csv        data/synthetic_results.json
            |                                  |
            v                                  v
   coverage_analyzer.py              outcome_evaluator.py
            |                                  |
            +---------------+------------------+
                            v
                      reporting.py
                            |
                            v
              Markdown assessment / CLI
                            |
                            v
             remediation + controlled re-test
```

The implementation is deliberately offline. It does not authenticate to endpoints, query production SIEMs, execute payloads, scan networks, or modify remote systems.

## Validation States

The outcome evaluator uses evidence-aware states:

- `telemetry_gap` – the required source data is absent, so detection efficacy cannot be judged;
- `detection_gap` – telemetry exists but the expected analytic does not fire;
- `partial` – important validation gates remain incomplete;
- `revalidation_failed` – remediation was attempted but the controlled re-test failed;
- `validated` – all modeled evidence gates are satisfied.

The generic validation score is bounded from 0–100 and weights telemetry, detection, analyst triage, response handling, remediation, and re-test evidence. The score is a compact summary, not a substitute for analyst judgment.

## Current Synthetic Scenarios

| Exercise | ATT&CK | Defensive objective |
| --- | --- | --- |
| PT-001 | T1059.001 – PowerShell | Validate process/script telemetry and alert/triage workflow |
| PT-002 | T1053.005 – Scheduled Task | Identify a detection gap when source telemetry exists |
| PT-003 | T1098 – Account Manipulation | Validate identity-change detection, response, remediation, and re-test |
| PT-004 | T1021.001 – RDP | Demonstrate that missing telemetry blocks detection validation |

ATT&CK mappings are defensive threat-model context. They do **not** prove compromise, production technique execution, or attribution.

## Repository Structure

```text
.github/workflows/security-quality.yml   CI quality gate

data/synthetic_results.json              fictional validation evidence

docs/exercise-playbook.md                authorization and exercise lifecycle

docs/methodology.md                      scoring, evidence model, trust boundaries

docs/remediation-revalidation.md         technical closure workflow

docs/recruiter-review.md                 five-minute reviewer path

exercises/exercise_matrix.csv            synthetic ATT&CK-aligned catalogue

reports/example-purple-team-assessment.md recruiter-facing example output

src/coverage_analyzer.py                 matrix coverage validation
src/outcome_evaluator.py                 evidence-based outcome engine
src/reporting.py                         Markdown reporting
src/cli.py                               offline report CLI

tests/                                   positive and negative unit tests
```

## Usage

Run the unit tests:

```bash
python -m unittest discover -s tests -v
```

Validate the exercise matrix:

```bash
python src/coverage_analyzer.py exercises/exercise_matrix.csv
```

Generate a synthetic assessment:

```bash
python src/cli.py data/synthetic_results.json --output reports/generated-assessment.md
```

No third-party Python packages are required.

## Methodology

Each exercise starts with authorization, scope, a defensive hypothesis, expected telemetry, expected detection behavior, analyst decision criteria, stop conditions, and a remediation owner. Synthetic or benign lab evidence is then evaluated across six gates:

1. telemetry availability;
2. detection behavior;
3. analyst triage;
4. response-path validation;
5. remediation evidence where required;
6. controlled re-test.

See [`docs/methodology.md`](docs/methodology.md) for scoring and trust boundaries.

## Remediation and Revalidation

A closed task is not treated as proof that a control is fixed. Technical closure requires evidence appropriate to the gap and a successful controlled re-test. Risk acceptance, if used in a real program, should remain separate from technical control state.

See [`docs/remediation-revalidation.md`](docs/remediation-revalidation.md).

## Design Decisions

- **Synthetic data only:** prevents confidential or production evidence from entering the portfolio.
- **Fail-closed validation:** malformed schemas, duplicate exercise IDs, invalid ATT&CK identifiers, and non-boolean control values are rejected.
- **Deterministic finding IDs:** SHA-256-derived IDs support stable reporting without external state.
- **Telemetry-first logic:** a detection cannot be called effective when the source data required to evaluate it is missing.
- **Re-test required:** remediation is not considered technically validated until the controlled scenario succeeds.
- **Provider-neutral architecture:** the project demonstrates engineering logic without claiming integration with a specific employer or customer environment.

## CI / Quality Gate

The least-privilege GitHub Actions workflow uses `contents: read` and performs:

- Python compilation;
- unit-test discovery;
- exercise-matrix validation;
- synthetic report generation;
- expected output/safety assertions.

CI status should always be verified against the **exact commit** being reviewed; a historical green run is not treated as evidence for a newer commit.

## Limitations

This is a portfolio reference implementation, not a production purple-team platform. The scoring weights are illustrative and would require organizational calibration. The project does not connect to EDR, SIEM, identity, cloud, ticketing, or orchestration platforms, and it intentionally does not include offensive execution tooling.

## Skills Demonstrated

Purple teaming, detection validation, security engineering, MITRE ATT&CK mapping, telemetry reasoning, evidence governance, remediation validation, Python automation, deterministic reporting, unit testing, CI/CD security controls, and risk communication.

## Roadmap

- add detection-rule version metadata and regression history;
- model false-positive/false-negative observations separately from control state;
- add schema versioning for exercise evidence;
- add provider-neutral adapters for exported SIEM/EDR test fixtures only;
- add trend reporting across repeated validation cycles.

## Safety

All scenarios, identities, evidence references, and results are fictional or synthetic. The repository contains no credentials, malware, destructive actions, credential theft, persistence payloads, bypass instructions, production targeting, employer/client data, or claims of real-world compromise.
