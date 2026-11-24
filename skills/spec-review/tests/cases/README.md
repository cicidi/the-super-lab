# spec-review mechanical cases (TST-H scaffold)

| Case | Intent |
|---|---|
| `mechanical-clean-pos` | `max_findings: 0` on valid test-plan tree |
| `mechanical-missing-test-cases` | Missing required `## Test Cases` |
| `mechanical-bad-ids` | Forbidden numeric-style ID |
| `mechanical-missing-frontmatter` | No YAML frontmatter block |
| `mechanical-bad-change-log` | Change Log not last `##` section |
| `mechanical-parent-incomplete` | Parent missing five-doc directories (`tree:` block) |
| `mechanical-bad-decision-log` | Decision Log table shape |
| `mechanical-bad-open-questions` | Open-question tracker shape (`QUES-A`, owner, blocking) |
| `mechanical-unanchored-citation` | `file:line` citation without a commit |
| `mechanical-impl-task-no-done` | `IMPL-*` task without a done line |
| `mechanical-bad-size` | Document over its hard line cap |

Run: `python3 skills/spec-review/tests/run_case_checks.py` (expect **11** mechanical cases; TST-H).

Semantic / severity cases (TST-H full, 5 planned): **`../EXPECTED-YAML.md`** (`semantic:` block); not written yet — they need a judge runner that runs spec-review on the input.
