# Recruiter / Technical Reviewer Guide

## Five-Minute Review Path

1. Start with `README.md` for the problem statement and architecture.
2. Review `src/outcome_evaluator.py` for validation-state logic, deterministic finding IDs, and fail-closed input handling.
3. Review `src/reporting.py` and `reports/example-purple-team-assessment.md` for analyst-facing output.
4. Review `tests/` for negative validation cases and control-state tests.
5. Review `docs/methodology.md` and `docs/remediation-revalidation.md` for evidence standards, limitations, and closure criteria.

## Capabilities Demonstrated

| Capability | Repository evidence |
| --- | --- |
| Purple-team program design | `docs/exercise-playbook.md`, `exercises/exercise_matrix.csv` |
| Detection validation | `src/coverage_analyzer.py`, `src/outcome_evaluator.py` |
| Evidence quality controls | strict JSON/CSV validation and duplicate rejection |
| ATT&CK-informed engineering | T1059.001, T1053.005, T1098, T1021.001 mappings |
| Remediation governance | explicit gap states and revalidation workflow |
| Security reporting | deterministic findings and Markdown assessment output |
| Software quality | unit tests and GitHub Actions quality gate |

## What This Project Does Not Claim

It does not claim production exploitation, customer testing, credential access, endpoint compromise, or employer/client experience. All records are synthetic and all ATT&CK references are defensive validation context.
