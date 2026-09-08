# Purple Team Exercise Playbook

## Authorization

Every exercise requires a documented owner, approved scope, lab target, execution window, expected telemetry, stop conditions, and rollback path. Production targeting is out of scope for this portfolio.

## Exercise Design

For each ATT&CK technique, define:

- the defensive hypothesis;
- the safe lab action used to generate telemetry;
- the required log source;
- the expected detection or hunt query;
- analyst triage criteria;
- the remediation owner if a control gap is found.

## Validation States

- `validated`: telemetry was present and the expected control detected the simulated behavior.
- `partial`: telemetry existed but detection fidelity, context, or routing was incomplete.
- `gap`: expected telemetry or detection was absent.

## Lessons-Learned Output

A completed exercise should record evidence references, detection result, false-positive considerations, missing telemetry, tuning recommendations, ownership, target remediation date, and re-test outcome.

## Strategic Goal

Purple teaming is treated here as a feedback loop: emulate safely, observe, measure, improve, and re-test. ATT&CK coverage counts are not treated as proof of security effectiveness without validation evidence.
