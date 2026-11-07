# spec-pipeline — operations (commands)

Norm: `pipeline-design.md` (**PIPE-***). Routing table: **`INTEGRATIONS.md`**. Checklists: **`PHASE-CHECKLISTS.md`**.

## Phase → commands

| Phase | When | Command / skill | Pass signal |
|---|---|---|---|
| **Create** | New `<f>` | walter-worker feature create | Feature slug + placement agreed |
| **Create** | Context only | Notes in `CLAUDE.local.md` | No silent `docs/features/` tree |
| **Map** | After interview | Optional **wayfinder** / **grill-with-docs** | Human OK before paths |
| **Converge** | Edit prose | **spec-write** | ≤10 lines / 200 chars per edit |
| **Converge** | Moves / INDEX | **spec-organize** | `run_spec_checks.py` → 0 findings |
| **Converge** | Before commit | **spec-review** (offer) | User accept or decline recorded |
| **Downstream** | Post PIPE-E | **spec-write** impl + test plans | Both from design 篇 |
| **Any** | Initiative gate | `./tools/run_sdd_mechanical.sh` | pytest + catalogs green |
| **Any** | Real tree (TST-G) | `python3 tools/tst_g_real_tree.py` | baselines match `--summary` counts |
| **Any** | Registry drift | `python3 tools/must_registry_coverage.py` | no unmapped python MUST |
| **Any** | Reader | `build_sdd_reader.py` → `validate_sdd_reader.py` | validate exit 0 |
| **Any** | Gold prep | `eval_preflight.py` + `check_gold_run_scaffold.py` | ok lines |

## Recap command bundle

When user asks “where am I on spec?”:

1. Read state (`CLAUDE.local.md` or `docs/features/<f>/raw/state/state-*.md`).
2. Emit **`RECAP-TEMPLATE.md`** sections.
3. Optional lint: `python3 tools/run_spec_checks.py docs/features/<f>/ --summary`.

## Eval (optional, local models)

See **`skills/spec-organize/tests/gold/v1/TST-C-RUNBOOK.md`**. Pipeline does not invoke models; **spec-organize** owns the interview loop.

## External samples

Adopt patterns only into **`INTEGRATIONS.md`** / skills — not new committed spec types under `docs/features/`.
