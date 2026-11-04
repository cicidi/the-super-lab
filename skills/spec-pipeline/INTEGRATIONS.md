# spec-pipeline — pluggable skill interfaces

**Norm (frozen):** `docs/features/spec-driven-development/features/pipeline/design/pipeline-design.md` (**PIPE-G**). This file is **operational** — update when repo skills change; do not restate PIPE-* rules here.

## Phase → skill routing

| Phase | Intent | Skill / tool | Required | Notes |
|---|---|---|---|---|
| **Create** | New initiative / `<f>` | walter-worker **feature create** | MUST | Peer vs nested: parent HLD §3.1 |
| **Create** | Background context | **research** (`skills/research/`) | optional | Put summaries in `CLAUDE.local.md`, not raw as PRD |
| **Map** | Explore splits / unknowns | **wayfinder** (`skills/wayfinder/`) | optional | Interview first; wayfinder **cannot** replace human Map |
| **Map** | Adversarial unknowns | **grill-with-docs** | optional | When user wants stress-test before Converge |
| **Converge** | Edit committed prose | **spec-write** | MUST if editing | ≤10 lines / 200 chars per edit (parent HLD §4) |
| **Converge** | Paths, Lint, INDEX | **spec-organize** | MUST after move/create | Modes A–D; oracle `SPEC-STANDARD.md` |
| **Any** | Before commit | **spec-review** | ask (PIPE-A4) | Mechanical MUST + semantic; suggest only |
| **Downstream** | impl-plan / test-plan | **spec-write** + **spec-organize** | MUST | Parallel, both from design 篇 |
| **Any** | Human reader HTML | **SPEC-HTML-STANDARD** + `tools/build_sdd_reader.py` | optional | No spec edits; derived HTML only |

## Recap payload (PIPE-A5)

When user asks recap, emit:

1. **phase** — Create | Map | Converge | Downstream  
2. **state location** — `CLAUDE.local.md` vs `docs/features/<f>/raw/state/state-*.md`  
3. **last actions** — from state + recent git/log if user allows  
4. **open_items** — blocking decisions, missing parent five-doc (if reviewing parent)  
5. **next skill** — one row from table above  

## External patterns (reference only)

- **Doc creation order** by change size (PRD → design → plan): see e.g. documentation-criteria workflows — map to **Converge → Downstream**, not new artifact types.  
- **Decision log + ADR split**: executive table + deep appendix — matches our **decision-history** + Evidence Appendix; IDs stay **ARD-*** per frozen document-standard.
