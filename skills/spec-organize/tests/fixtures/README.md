# TST-B fixtures

| Dir | Role |
|---|---|
| `neg/<name>/` | Must trigger checker `{name}` (see `tools/run_neg_fixtures.py`) |
| `pos/<name>/` | Must pass all per-file checkers (`tools/run_pos_fixtures.py`) |

Neg folders are the `CASES` list in `tools/run_neg_fixtures.py`, including the 2026-11-07 checkers (`paired-html-stale`, `bad-audience`, `bad-open-questions`, `dead-anchor`, `unanchored-citation`, `impl-task-no-done`, `translation-no-banner`, `stale-section-ref`, `bad-tracker-counts`, `stale-question-status`, `diagram-step-mismatch`).

Pos folders: `clean-feature`, `valid-test-plan`, `valid-decision-history`.
