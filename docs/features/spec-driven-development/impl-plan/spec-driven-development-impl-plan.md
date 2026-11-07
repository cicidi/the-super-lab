---
feature: spec-driven-development
type: impl-plan
state: draft
final_date: 2026-11-03
health: active
owner: cicidi
last_verified: 2026-11-04
---

# Spec-Driven Development — Implementation Plan

## Global Constraints

- **Spec before skill:** If spec error blocks work, **ask human** → update spec → then skills/tests.
- **Skills:** Use `skill create` / `skill edit` (`skills/skill/SKILL.md`) for SKILL.md bodies; this plan defines order only.
- **Tests:** Parent `test-plan/spec-driven-development-test-plan.md`; assets under `skills/spec-organize/tests/`.
- **No wayfinder-import** sub-feature (ARD-T).
- **Eval:** deepseek-flash, 3 runs; runs/reports not committed (ARD-AD).
- **No legacy migration** (ARD-AF); only the SDD tree is fixed.

## IMPL-A — Skill directory migration (DONE baseline)

**Goal:** `doc-organize` → `spec-organize`, `doc-review` → `spec-review`.

**Steps:** `git mv` directories; update `name:` and cross-refs in SKILL.md; update `~/.coworker/project.yaml` skill list when deploying.

**Verify:** `ls skills/spec-organize skills/spec-review`; triggers resolve.

## IMPL-B — New skills: spec-pipeline, spec-write

**Goal:** SKILL.md stubs aligned with pipeline design and HLD §7.

**Steps:** Refine via `skill create` / `skill edit` if process changes; keep in sync with `features/pipeline/design/pipeline-design.md`.

**Verify:** Description starts with "Use when"; MUST gates present.

## IMPL-C — SPEC-STANDARD.md

**Goal:** Enforceable summary in `skills/spec-organize/SPEC-STANDARD.md`; full rules stay in document-standard design.

**Steps:** On DSGN change, update summary in same PR as design diff.

**Verify:** spec-organize Lint references SPEC-STANDARD.

## IMPL-D — Test skeleton & iPhone gold inputs

**Goal:** `skills/spec-organize/tests/` per parent test plan.

**Deliverables:**

- `eval.yaml`, `must_registry.yaml` (populate via TST-A scan)
- `gold/iphone/v1/requirement.md`, `gold/iphone/v1/context.md`
- `fixtures/neg/`, `fixtures/pos/` (grow with TST-B)
- `checks/` Python package (implement TST-B)

**Verify:** Run TST-B when checks exist; gold inputs present.

## IMPL-E — Self-run eval (agent)

**Goal:** Baseline eval: `grill.skills: []`, spec-organize only, iPhone requirement + context.

**Steps:** New branch `eval/v1/<run_id>`; run spec-pipeline → write feature spec; TST-E/F/K; fix **spec first** on failure.

**Verify:** HTML report; scores per test plan.

## IMPL-F — Tabbed reader HTML

**Goal:** `spec-driven-development-reader.html` — **human-readable** HTML (cards, tables, flows), not a markdown viewer. Tabs: parent (PRD, design, impl, test, decision history) + children (pipeline, document-standard).

**Steps:** Rewrite prose when canonical `.md` changes; each panel links to source path in footer.

**Verify:** Open file in browser; all canonical paths exist.

## IMPL-G — CLAUDE.local / managed block

**Goal:** Pipeline Create/Map progress before `<f>` exists (PIPE-H).

**Steps:** Add SDD block to project `CLAUDE.local.md`: phase, rough PRD pointer, link to reader HTML.

**Verify:** spec-pipeline Step 0 reads block.

## IMPL-H — Docs hygiene

**Goal:** INDEX lists parent impl-plan and new aspect design; delete legacy summary HTML.

**Steps:** Regenerate or hand-update `docs/INDEX.md`; delete `spec-driven-development.html`; keep `spec-driven-development-reader.html` only.

**Verify:** No links to removed summary HTML or wayfinder-import paths under SDD.

## IMPL-I — spec-review mechanical MUST alignment

**Goal:** SKILL matches test plan (detect MUST violations + suggestions).

**Steps:** Edit `skills/spec-review/SKILL.md` after spec-review section in document-standard / test plan stable.

**Verify:** TST-H fixtures pass when implemented.

## IMPL-J — Eval config & schema test

**Goal:** `eval.yaml` runnable with `deepseek-flash`; 3 runs; target repo env override; `test_eval_config.py` fails on missing config.

**Verify:** `pytest test_eval_config.py`; `eval.yaml` has all required keys.

## IMPL-K — Fixtures & review cases

**Goal:** 11 neg + pos fixtures; 16 spec-review cases (11 mechanical + 5 semantic).

**Verify:** TST-B green; TST-H/I assets present.

## IMPL-L — Eval report script

**Goal:** `tools/render_eval_report.py` generates a single HTML with score 1/2 and run metadata.

**Verify:** TST-K on a sample run.

## IMPL-M — Checker updates

**Goal:** `sections.py` checks 5 types; `ids.py` enforces title patterns; remove exemptions.

**Verify:** TST-B; `run_spec_checks.py` on SDD tree.

## IMPL-N — Skill contracts & four examples

**Goal:** `design/spec-driven-development-design-skill-contracts.md`; each skill body names shed / 北京旅游 / 数学题 / 股票 (PRD-Q).

**Verify:** TST-S; spec-review reads contracts.

## IMPL-O — Reader freshness & summary removal

**Goal:** regenerate reader after spec changes; delete `spec-driven-development.html`.

**Verify:** TST-R; no dead links.

## Execution order

IMPL-A → B → C → D → J → K → M → N → F → G → H → O → E → I (eval after readable spec + skeleton).

## Acceptance Criteria

- score 1 = `total/total`,且 judge 3/3 一致。
- score 2 ≥ 6,annotations v1。
- 可执行的 TST-A–S 全绿;`run_spec_checks.py` 0 findings。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-03 | Initial parent impl-plan; tasks 1–9 |
| 2026-11-03 | Task 6：Reader 改为富格式汇编，非 MD fetch |
| 2026-11-04 | Task 1–9 → IMPL-A–I；新增 IMPL-J–O：eval 配置、fixtures/cases、报告、检查器、skill 契约、reader |
| 2026-11-04 | Global Constraints 加 eval/no-migration；IMPL-D gold 路径改 iphone/v1 |
