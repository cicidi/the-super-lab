---
name: spec-write
description: |
  Use when drafting or editing committed feature spec markdown — PRD, design,
  impl-plan, test-plan, decision-history — under docs/features/. Use after
  spec-pipeline has set phase; pair with spec-organize for placement and lint.
license: MIT
compatibility: claude-code,opencode
metadata:
  triggers:
    - write spec
    - edit spec
    - draft prd
    - draft design
    - append decision
    - spec write
---

# spec-write

Writes and edits **committed** feature spec prose. Standard and paths: **spec-organize** + `SPEC-STANDARD.md`.

## When to Use

- Creating or updating prd/design/impl-plan/test-plan/decision-history content
- Appending Decision Log / Change Log entries

## When NOT to Use

- Lint, rename, INDEX — **spec-organize**
- Design adversarial review — **spec-review**
- Orchestration / recap — **spec-pipeline**

## Process

1. Confirm `<f>`, type, and phase via **spec-pipeline** or user (see **spec-pipeline/INTEGRATIONS.md**).
2. Load `skills/spec-organize/SPEC-STANDARD.md` + `CONTENT-PRIORITY.md` / `SPEC-SCOPE.md` when trimming.
3. Edit with **≤10 lines or ≤200 characters per edit** (parent HLD §4); split or ask for `restructure`.
4. Use letter-prefix IDs only (**PRD-A**, **DSGN-B**, **ARD-C**, **IMPL-A**, **TST-A**).
5. After create/move: **spec-organize** Organize/Lint; regenerate INDEX when tree changes.

### By type (quick)

| Type | Focus |
|---|---|
| **prd** | Problem, goals, requirements with **PRD-*** IDs; deferrals → **ARD-** in decision-history |
| **design** | Behavior, contracts, boundaries — not class-level code (**SPEC-SCOPE.md**) |
| **decision-history** | New **ARD-*** row at **top** of Log; supersede = ~~strike~~ + link |
| **impl-plan** | Numbered tasks **IMPL-***; Global Constraints first |
| **test-plan** | **TST-*** cases; execution order; pass threshold |

After substantive spec edits on an initiative parent, **spec-pipeline** may run `python3 tools/build_sdd_reader.py` (no spec change in HTML itself).

## Quality Gates

### MUST

- [ ] Frontmatter and required sections for the type
- [ ] Change Log last section; append only
- [ ] Decision-history: newest-first; supersede via strike + link
- [ ] No L1 deletion to meet size cap

### NICE

- [ ] Links instead of restating facts owned elsewhere (L4)

## Anti-Patterns

- Large single edits without restructure approval
- Writing implementation class detail into design (see **SPEC-SCOPE.md**)
