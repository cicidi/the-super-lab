# TST-C runbook — gold v1 (iPhone purchase)

Mechanical prep only; model runs stay local (configure `skills/spec-organize/tests/eval.yaml`).

## Preflight (repo)

```bash
python3 tools/eval_preflight.py
python3 tools/check_gold_run_scaffold.py
python3 tools/eval_next_steps.py   # preflight + printed checklist
```

## Baseline run (one model)

1. Read **`requirement.md`** and **`context.md`** only for simulated human answers (**「未提供」** when absent).
2. Run **spec-organize** Map interview; log Q/A in `runs/<model-slug>/interview.md` (copy from `runs/_template/interview.md`).
3. Converge toward feature slug **`iphone-purchase`** under `docs/features/` only when human approves committed spec (eval may keep outputs under `runs/` until TST-D).
4. Do not commit API keys; keep `eval.yaml` models empty in git.

## Parallel runs (TST-C)

- Set three entries in `eval.yaml` → `gold.models`.
- Same requirement/context; separate `runs/<model>/` trees.
- Compare only within the same `gold.version` in `annotations.yaml`.

## Variants (TST-F)

Re-run interview using one file under `context-variants/` instead of `context.md`; note variant path in interview header.

## After runs (TST-D+)

- Distill passing tree into **`exemplar/`** (see `exemplar/README.md`).
- Extend **`annotations.yaml`**; bump `gold.version` in `eval.yaml` when labels change.
- Mechanical shape reference (not the eval target): **`POS-FIXTURE-REFERENCE.md`**.

## Gate

```bash
./tools/run_sdd_mechanical.sh
```
