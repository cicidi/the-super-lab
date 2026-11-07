# spec-organize — SDD test harness

Oracle: `skills/spec-organize/SPEC-STANDARD.md`. Parent test plan: `docs/features/spec-driven-development/test-plan/spec-driven-development-test-plan.md`. Tool index: `tools/README-SDD.md`. Skills map: `skills/SDD-DELIVERABLES.md`.

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
| `fixtures/README.md` | Neg/pos catalog |
| `must_registry.yaml` | TST-A MUST index (`python` vs `llm`) |
| `tst_g_baselines.txt` / `TST-G.md` | Real-tree lint baselines |
| `gold/v1/` | TST-C–F eval assets |
| `eval.yaml` | Judge/checker config |
| `eval/TST-J-MATRIX.md` | Grill.skills run matrix |

## Tools (repo root)

- `python3 tools/run_spec_checks.py docs/features/<f>/`
- `python3 tools/run_gold_ref.py smb-balance` — TST-T; skip when `~/src/smb-balance` is absent
- `python3 tools/run_neg_fixtures.py` — every `fixtures/neg/*` must fail its check
- `python3 tools/run_pos_fixtures.py` — every `fixtures/pos/*` must pass per-file checks
- CI: `.github/workflows/sdd-mechanical.yml`
- `python3 tools/tag_must_registry_checks.py` — refresh `method`/`check` tags
- `python3 tools/tst_a_scan_must_registry.py` — draft registry from design (use with care)
- `python3 tools/tst_a_registry_stats.py` — registry vs scan candidate counts
- `python3 tools/eval_preflight.py` — gold v1 assets present before TST-C
- `python3 tools/check_gold_run_scaffold.py` — runbook + runs template

Pipeline recap: `skills/spec-pipeline/RECAP-TEMPLATE.md`.
