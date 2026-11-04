---
name: spec-pipeline
description: |
  Use when starting or continuing spec-driven work on a feature — creating a
  feature, mapping a large requirement, converging PRD/design/decision-history,
  or before committing spec changes. Use when the user needs recap, state, skill
  recommendations for the SDD pipeline, or a human-readable HTML spec reader
  (parent + child tabs, not a markdown preview).
license: MIT
compatibility: claude-code,opencode
metadata:
  triggers:
    - spec pipeline
    - sdd pipeline
    - write spec
    - update spec
    - spec driven
    - where am I on spec
    - recap spec
    - spec reader
    - human readable spec
    - spec html
---

# spec-pipeline

Orchestrates spec-driven development: **Create → Map → Converge → Downstream**.
Entry point before **spec-organize** / **spec-write**; prompts for **spec-review** before commit.

Design: `docs/features/spec-driven-development/features/pipeline/design/pipeline-design.md` (**PIPE-***). Skill routing table: **`INTEGRATIONS.md`** (this directory).

## When to Use

- Any task that creates or changes feature spec under `docs/features/`
- Lost context: need recap of phase, state, and next steps
- Before git commit of committed spec files

## When NOT to Use

- Pure code implementation with no spec impact
- Lint-only pass — invoke **spec-organize** Mode B directly
- Adversarial design review only — invoke **spec-review** directly

## Process

### Step 0: Phase & state

1. If `<f>` not created: read/write progress in **`CLAUDE.local.md`** only (**PIPE-H**).
2. If `<f>` exists: read `docs/features/<f>/raw/state/state-<YYYY-MM-DD>.md`.
3. Infer phase: Create | Map | Converge | Downstream.

### Step 1: Create (when needed)

- Run **feature create** (walter-worker) or confirm existing `<f>`.
- Capture rough PRD; put search/context in **CLAUDE.local.md**.

### Step 2: Map (when splitting or unknowns)

- **Interview** the user; optional pluggable map skill (e.g. wayfinder) — **not required**.
- AI judges splits/decisions/scratch; **confirm** before creating paths.
- Summarize in recap; do not silently create `docs/features/` trees.

### Step 3: Converge

- Loop **PRD ↔ design ↔ decision-history** until **PIPE-E** convergence in pipeline design.
- Call **spec-write** for edits; **spec-organize** after create/move/rename.

### Step 4: Downstream

- When converged: **test-plan** and **impl-plan** in **parallel** from design.

### Step 5: Before commit

Ask: run **spec-review** on changed spec? Record if user declines.

### Recap (on request)

List: phase, last actions, open items, recommended next skill (**INTEGRATIONS.md** table). Use **`RECAP-TEMPLATE.md`** format. Optionally run `python3 tools/run_spec_checks.py docs/features/<f>/` before review.

### Step 6: Human-readable HTML reader (optional)

When the user wants a **readable spec bundle** or after major spec updates:

1. Load **`skills/spec-html-standard/SPEC-HTML-STANDARD.md`** (**DSGN-N** fidelity — no executive-summary trimming).
2. Gather canonical paths: parent five types; each `features/<sub>/` (at least `design/`).
3. Assemble rich HTML (tabs, cards, tables, flows) — **not** md fetch/preview.
4. Write `docs/features/<parent>/<parent>-reader.html`; canonical footers per tab.
5. Match initiative summary HTML styling when present.
6. For SDD parent, may run `python3 tools/build_sdd_reader.py` after `.md` updates.

Do not treat the HTML as source of truth. If assembly exposes a spec error, **ask the human** → update **spec** first → regenerate reader → then skills.

## Quality Gates

### MUST

- [ ] Spec changes go through this skill unless user explicitly skips (note in state)
- [ ] **spec-organize** owns standard; **spec-write** owns prose edits
- [ ] No silent rewrite of upstream artifacts (**PIPE-I**)
- [ ] Submit prompt for **spec-review** before committed spec push/commit
- [ ] HTML reader (when built): follows **SPEC-HTML-STANDARD** — high fidelity L1, tabs, canonical footers

### NICE

- [ ] Phase recorded in state file or CLAUDE.local
- [ ] Map interview notes captured before structural splits

## Anti-Patterns

- Calling **spec-write** without pipeline phase awareness on large initiatives
- Creating feature directories without human confirmation after Map
- Skipping review prompt before every committed spec batch
- Shipping a “reader” that only embeds or fetches `.md` without human-oriented layout
