# External SDD — GitHub Spec Kit mapping

Reference: [github/spec-kit](https://github.com/github/spec-kit) (constitution → specify → plan → tasks → implement). **Do not** add Spec Kit artifact filenames under `docs/features/`; map phases to this repo only.

| Spec Kit step | Our pipeline | Committed artifacts |
|---|---|---|
| `/speckit.constitution` | **Create** (once per initiative) | Parent principles in **design** / **decision-history**, not a new “constitution.md” type |
| `/speckit.specify` | **Map → Converge** | **PRD** (what/why) |
| `/speckit.clarify` | **Map** interview | State / `CLAUDE.local.md`; optional **grill-with-docs** |
| `/speckit.plan` | **Converge** | **design** (how/stack) |
| `/speckit.tasks` | **Downstream** | **impl-plan** + **test-plan** (not standalone `tasks.md`) |
| `/speckit.implement` | Out of spec harness | Code; **spec-pipeline** does not run implement |
| `/speckit.checklist` / `analyze` | **spec-review** + TST-B | Mechanical MUST + future semantic judge |
| `/speckit.converge` | **Converge** loop | **PIPE-E** in pipeline design |

Quality gates in Spec Kit ≈ **run_spec_checks.py** before **spec-review**. Eval grill matrix: **`skills/spec-organize/tests/eval/TST-J-MATRIX.md`**.
