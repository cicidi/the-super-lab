# spec-review mechanical cases (TST-H scaffold)

| Case | Intent |
|---|---|
| `mechanical-clean-pos` | `max_findings: 0` on valid test-plan tree |
| `mechanical-missing-test-cases` | Missing required `## Test Cases` |
| `mechanical-bad-ids` | Forbidden numeric-style ID |
| `mechanical-missing-frontmatter` | No YAML frontmatter block |

Run: `python3 skills/spec-review/tests/run_case_checks.py`

Semantic / severity cases (TST-H full) add `expected.yaml` fields later; see parent test plan.
