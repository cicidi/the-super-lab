# SDD tooling index

Mechanical gate: `./tools/run_sdd_mechanical.sh` (alias for `skills/spec-organize/tests/run_mechanical.sh`; see `skills/spec-organize/tests/README.md`).

| Script | Role |
|---|---|
| `run_spec_checks.py` | Lint `docs/features/` (`--summary`, `--help`; tree checks when path under `docs/features/`) |
| `run_neg_fixtures.py` / `run_pos_fixtures.py` | TST-B fixture gates |
| `must_registry_coverage.py` | Registry vs checker mapping |
| `tst_a_anchor_check.py` | Registry source line anchors |
| `tst_a_registry_stats.py` | Registry vs scan candidate counts |
| `tst_a_scan_must_registry.py` | Draft registry from design (destructive with `--write`) |
| `tag_must_registry_checks.py` | Heuristic `method`/`check` tags |
| `build_sdd_reader.py` | Regenerate `*-reader.html` |
| `validate_sdd_reader.py` | Reader smoke test |
| `eval_preflight.py` | Gold v1 asset check before TST-C |
| `skills/spec-review/tests/run_case_checks.py` | TST-H mechanical cases |

CI: `.github/workflows/sdd-mechanical.yml`.
