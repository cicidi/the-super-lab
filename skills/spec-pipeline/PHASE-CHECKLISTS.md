# spec-pipeline — phase checklists (operational)

Normative rules: `pipeline-design.md` (**PIPE-***). Routing: **`INTEGRATIONS.md`**. Sequences: **`SEQUENCE.md`**.

## Create

- [ ] Confirm `<feature-slug>` and nested vs peer placement (parent HLD §3.1)
- [ ] Rough PRD in `CLAUDE.local.md` or first `prd/` draft after human OK
- [ ] No committed tree until Map/Converge confirms structure

## Map

- [ ] Interview complete; splits/decisions recorded (state or CLAUDE.local)
- [ ] Optional map skill invoked **after** interview (never instead)
- [ ] Human confirms before **spec-organize** creates paths

## Converge

- [ ] PRD ↔ design ↔ decision-history loop until PIPE-E satisfied
- [ ] **spec-write** for prose; **spec-organize** after moves/INDEX
- [ ] `python3 tools/run_spec_checks.py docs/features/<f>/` before review prompt

## Downstream

- [ ] **impl-plan** and **test-plan** from design (parallel)
- [ ] Parent five-doc complete if reviewing initiative root

## Reader (optional)

- [ ] Load **SPEC-HTML-STANDARD** / **DSGN-N**
- [ ] `python3 tools/build_sdd_reader.py` then `python3 tools/validate_sdd_reader.py`

## Before commit (committed spec)

- [ ] Offer **spec-review**; note if user declines
- [ ] No edits to frozen document-standard / DSGN-N unless user approves
