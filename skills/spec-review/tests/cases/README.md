# spec-review mechanical cases (TST-H scaffold)

| Case | Intent |
|---|---|
| `mechanical-clean-pos` | `max_findings: 0` on valid test-plan tree |
| `mechanical-missing-test-cases` | Missing required `## Test Cases` |
| `mechanical-bad-ids` | Forbidden numeric-style ID |
| `mechanical-missing-frontmatter` | No YAML frontmatter block |
| `mechanical-bad-change-log` | Change Log not last `##` section |

Run: `python3 skills/spec-review/tests/run_case_checks.py` (expect **5** mechanical cases).

Semantic / severity cases (TST-H full) add `expected.yaml` fields later; see parent test plan.
