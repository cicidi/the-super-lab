# TST-J — grill.skills matrix

Configure in `skills/spec-organize/tests/eval.yaml`. Each row is one eval run → one TST-K report.

| Run label | `grill.skills` | Phase emphasis |
|---|---|---|
| baseline | `[]` | Map interview only (default gold v1) |
| wayfinder | `[wayfinder]` | Optional map skill after interview |
| grill-docs | `[grill-with-docs]` | Adversarial unknowns before Converge |
| both | `[wayfinder, grill-with-docs]` | Combined (order: interview → wayfinder → grill) |

**Rules:** Baseline first; compare score 1/2 within same `gold.version`. No pass/fail threshold in harness — report only.

Preflight: `python3 tools/check_eval_config.py` · Procedure: `gold/v1/TST-C-RUNBOOK.md`.
