# spec-organize — SDD test harness

Oracle: `skills/spec-organize/SPEC-STANDARD.md`. Parent test plan: `docs/features/spec-driven-development/test-plan/spec-driven-development-test-plan.md`.

## Quick gate

```bash
./skills/spec-organize/tests/run_mechanical.sh
```

Runs: `run_spec_checks.py` (SDD tree), `must_registry_coverage.py`, `tst_a_anchor_check.py`, gold/reader smoke scripts, `spec-review` case checks, pytest on `test_checks.py`.

## Layout

| Path | Role |
|---|---|
| `checks/` | TST-B Python checkers |
| `fixtures/neg/<check>/` | Must fail |
| `fixtures/pos/` | Must pass |
| `must_registry.yaml` | TST-A MUST index (`python` vs `llm`) |
| `gold/v1/` | TST-C–F eval assets |
| `eval.yaml` | Judge/checker config |

## Tools (repo root)

- `python3 tools/run_spec_checks.py docs/features/<f>/`
- `python3 tools/run_neg_fixtures.py` — every `fixtures/neg/*` must fail its check
- `python3 tools/run_pos_fixtures.py` — every `fixtures/pos/*` must pass per-file checks
- CI: `.github/workflows/sdd-mechanical.yml`
- `python3 tools/tag_must_registry_checks.py` — refresh `method`/`check` tags
- `python3 tools/tst_a_scan_must_registry.py` — draft registry from design (use with care)
- `python3 tools/tst_a_registry_stats.py` — registry vs scan candidate counts
- `python3 tools/eval_preflight.py` — gold v1 assets present before TST-C

Pipeline recap: `skills/spec-pipeline/RECAP-TEMPLATE.md`.
