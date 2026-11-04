# TST-G — real tree lint

**Goal:** Lint on committed `docs/features/` trees matches the harness (`checks/` + exemptions in `run_spec_checks.py`).

## Baselines

`tst_g_baselines.txt` lists `path<TAB>expected_findings`. Update only when spec changes are user-approved and lint expectations shift.

## Command

```bash
python3 tools/tst_g_real_tree.py
```

External repos (eval): point `eval.yaml` → `target.repo`, then run `python3 tools/run_spec_checks.py <external>/docs/features/<feature>/` and add a local baseline row (do not commit secrets or private paths).
