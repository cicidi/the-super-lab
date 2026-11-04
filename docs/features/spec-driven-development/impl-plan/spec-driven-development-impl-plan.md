---
feature: spec-driven-development
type: impl-plan
state: draft
final_date: 2026-11-03
health: active
owner: cicidi
last_verified: 2026-11-03
---

# Spec-Driven Development — Implementation Plan

## Global Constraints

- **Spec before skill:** If spec error blocks work, **ask human** → update spec → then skills/tests.
- **Skills:** Use `skill create` / `skill edit` (`skills/skill/SKILL.md`) for SKILL.md bodies; this plan defines order only.
- **Tests:** Parent `test-plan/spec-driven-development-test-plan.md`; assets under `skills/spec-organize/tests/`.
- **No wayfinder-import** sub-feature (ARD-T).

## Task 1 — Skill directory migration (DONE baseline)

**Goal:** `doc-organize` → `spec-organize`, `doc-review` → `spec-review`.

**Steps:** `git mv` directories; update `name:` and cross-refs in SKILL.md; update `~/.coworker/project.yaml` skill list when deploying.

**Verify:** `ls skills/spec-organize skills/spec-review`; triggers resolve.

## Task 2 — New skills: spec-pipeline, spec-write

**Goal:** SKILL.md stubs aligned with pipeline design and HLD §7.

**Steps:** Refine via `skill create` / `skill edit` if process changes; keep in sync with `features/pipeline/design/pipeline-design.md`.

**Verify:** Description starts with "Use when"; MUST gates present.

## Task 3 — SPEC-STANDARD.md

**Goal:** Enforceable summary in `skills/spec-organize/SPEC-STANDARD.md`; full rules stay in document-standard design.

**Steps:** On DSGN change, update summary in same PR as design diff.

**Verify:** spec-organize Lint references SPEC-STANDARD.

## Task 4 — Test skeleton & iPhone gold inputs

**Goal:** `skills/spec-organize/tests/` per parent test plan.

**Deliverables:**

- `eval.yaml`, `must_registry.yaml` (populate via TST-A scan)
- `gold/v1/requirement.md`, `gold/v1/context.md`
- `fixtures/neg/`, `fixtures/pos/` (grow with TST-B)
- `checks/` Python package (implement TST-B)

**Verify:** Run TST-B when checks exist; gold inputs present.

## Task 5 — Self-run eval (agent)

**Goal:** Baseline eval: `grill.skills: []`, spec-organize only, iPhone requirement + context.

**Steps:** New branch `eval/v1/<run_id>`; run spec-pipeline → write feature spec; TST-E/F/K; fix **spec first** on failure.

**Verify:** HTML report; scores per test plan.

## Task 6 — Tabbed reader HTML

**Goal:** `spec-driven-development-reader.html` — **human-readable** HTML (cards, tables, flows), not a markdown viewer. Tabs: parent (PRD, design, impl, test, decision history) + children (pipeline, document-standard).

**Steps:** Rewrite prose when canonical `.md` changes; each panel links to source path in footer.

**Verify:** Open file in browser; all canonical paths exist.

## Task 7 — CLAUDE.local / managed block

**Goal:** Pipeline Create/Map progress before `<f>` exists (PIPE-H).

**Steps:** Add SDD block to project `CLAUDE.local.md`: phase, rough PRD pointer, link to reader HTML.

**Verify:** spec-pipeline Step 0 reads block.

## Task 8 — Docs hygiene

**Goal:** INDEX lists parent impl-plan; fix SDD HTML dead links where touched.

**Steps:** Regenerate or hand-update `docs/INDEX.md`; pipeline.html / spec-driven-development.html consistent with two sub-features.

**Verify:** No links to removed wayfinder-import paths under SDD.

## Task 9 — spec-review mechanical MUST alignment

**Goal:** SKILL matches test plan (detect MUST violations + suggestions).

**Steps:** Edit `skills/spec-review/SKILL.md` after spec-review section in document-standard / test plan stable.

**Verify:** TST-H fixtures pass when implemented.

## Execution order

1 → 2 → 3 → 4 → 6 → 7 → 8 → 5 → 9 (eval after readable spec + skeleton).

## Change Log

| Date | Change |
|------|--------|
| 2026-11-03 | Initial parent impl-plan; tasks 1–9 |
| 2026-11-03 | Task 6：Reader 改为富格式汇编，非 MD fetch |
