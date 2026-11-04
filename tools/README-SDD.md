# SDD tooling index

Mechanical gate: `./tools/run_sdd_mechanical.sh` (alias for `skills/spec-organize/tests/run_mechanical.sh`; see `skills/spec-organize/tests/README.md`).

**Scope:** Improve skills, tools, tests, and derived HTML only — not committed feature spec under `docs/features/` unless the user explicitly approves (document-standard / DSGN-N frozen).

| Script | Role |
|---|---|
| `run_spec_checks.py` | Lint `docs/features/` (`--summary`, `--help`; tree checks when path under `docs/features/`) |
| `run_neg_fixtures.py` / `run_pos_fixtures.py` | TST-B fixture gates |
| `check_neg_fixture_catalog.py` | `neg/*` dirs ↔ runner `CASES` |
| `check_pos_fixture_catalog.py` | `pos/*` ↔ `fixtures/README.md` |
| `check_review_case_catalog.py` | spec-review `cases/*` ↔ `cases/README.md` |
| `must_registry_coverage.py` | Registry vs checker mapping |
| `tst_a_anchor_check.py` | Registry source line anchors |
| `tst_a_registry_stats.py` | Registry vs scan candidate counts |
| `tst_a_scan_must_registry.py` | Draft registry from design (destructive with `--write`) |
| `tag_must_registry_checks.py` | Heuristic `method`/`check` tags |
| `build_sdd_reader.py` | Regenerate `*-reader.html` (`--check-sources`) |
| `verify_sdd_skills_map.py` | `SDD-DELIVERABLES.md` links exist |
| `validate_sdd_reader.py` | Reader smoke test |
| `eval_preflight.py` | Gold v1 asset check before TST-C |
| `check_gold_run_scaffold.py` | Gold runs template + TST-C runbook present |
| `eval_next_steps.py` | Preflight + printed TST-C+ checklist (no API) |
| `verify_sdd_tools_manifest.py` | README-SDD tool files exist |
| `skills/spec-review/tests/run_case_checks.py` | TST-H mechanical cases |

CI: `.github/workflows/sdd-mechanical.yml`.
