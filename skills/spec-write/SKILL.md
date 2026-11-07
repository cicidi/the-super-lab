---
name: spec-write
description: |
  Use when drafting or editing committed feature spec markdown — PRD, design,
  impl-plan, test-plan, decision-history — under docs/features/. Read
  SPEC-STANDARD.md, SPEC-PRESENTATION.md, and SPEC-HTML-STANDARD.md first.
  Decide new document or which existing documents to edit. Pair with
  spec-review before commit. HTML is one site: a directory of features,
  and inside a feature the left column is that feature's directory.
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

Writes and edits **committed** feature spec prose. Standards: `skills/spec-organize/SPEC-STANDARD.md`, `skills/spec-html-standard/SPEC-PRESENTATION.md`, and `skills/spec-html-standard/SPEC-HTML-STANDARD.md` (one site, ARD-BG).

## When to Use

- Creating or updating prd/design/impl-plan/test-plan/decision-history content
- Appending Decision Log / Change Log entries

## When NOT to Use

- Design adversarial review — **spec-review**
- Mechanical checks — `python3 tools/run_spec_checks.py`

SDD skill map: `skills/SDD-DELIVERABLES.md`.

## Example Domains

Illustrations, not gold. Each edit stays within 10 lines or 200 characters.

- **盖 shed**: one edit adds `PRD-A` for the permit limit. The design ownership row is `许可 | 人决定 | ARD-A`. If the setback distance was not looked up, write `UNKNOWN`.
- **北京旅游**: add the budget requirement. Evidence is a URL. Do not invent a hotel price.
- **数学题**: cite the definition's source. A lemma with no source is `UNKNOWN`.
- **股票**: the design `子问题归属` row cites the filing URL. No URL means `UNKNOWN`, not a guessed number.

## Process

1. Read `SPEC-STANDARD.md` chapters 1–3, `SPEC-PRESENTATION.md`, and `SPEC-HTML-STANDARD.md` (the **Site** section, ARD-BG).
2. Decide: create a new document from the path rules, or edit existing documents.
3. If editing, list every document that states the same fact. Edit the authority document. Replace the other copies with links.
4. Classify each edit as prose, format, style, table, or icon, then apply SPEC-PRESENTATION.
5. Edit with **≤10 lines or ≤200 characters per edit** under `docs/`; split or ask for `restructure`.
6. Use letter-prefix IDs only (**PRD-A**, **DSGN-B**, **ARD-C**, **IMPL-A**, **TST-A**, **QUES-A**). An Open Questions entry is `QUES-A`, not `OQ-1` or `QUES-1`.
7. After create/move: regenerate INDEX when the tree changes.
8. Cross-check before finishing: every `PRD-*` id appears in the design; every `TST-*` case names the requirement it covers.
9. On a design with sub-problems, write `子问题归属`: `| 子问题 | 归属 | 依据 |`. Owner is `AI 查`, `人决定`, or `AI 查完人决定`. 依据 is a `raw/` path, a URL, or an `ARD-*` id. If the fact was not found, write `UNKNOWN`. Do not guess.
10. A pure standard or orchestration design may say the ownership table does not apply. If every tracker row has Owner and Evidence, link to the tracker instead of copying the table.
11. A `file:line` citation names the commit. A renamed heading keeps the old anchor above the new title.
12. After a markdown edit, rebuild the one site with `python3 tools/build_sdd_site.py`. Each page is one directory line. A feature page keeps that feature's directory on the left and the page on the right. A hand-maintained HTML file keeps `spec-source-sha256` and a changelog row for every Change Log date.

### By type (quick)

| Type | Focus |
|---|---|
| **prd** | Problem, goals, requirements with **PRD-*** IDs; deferrals → **ARD-** in decision-history |
| **design** | Behavior, contracts, boundaries, ownership table or a link to the question tracker, evidence or `UNKNOWN`. Invariants as a table. One flow, one diagram |
| **decision-history** | New **ARD-*** row at **top** of Log; supersede = ~~strike~~ + link. Readiness in the row. Revise in place. Open items by owner |
| **impl-plan** | Each **IMPL-*** names its dependency, who it blocks, the step range, and a done line. Read side before write side. Mock a partner port that is not live |
| **any** | Dropping an old claim points at the new ARD. A typo may be edited in place. A translation is a local copy and names its source |
| **test-plan** | **TST-*** cases; execution order; pass threshold |

After substantive spec edits, rebuild the site with `python3 tools/build_sdd_site.py`. The reader assembly, when needed, is `python3 tools/build_sdd_reader.py`. HTML does not change the spec.

### Section headings (MUST)

Use the standard's exact English heading text, unnumbered: `## Overview`,
`## Goals and Success Metrics`, `## Test Cases`, … Never translate, rename, or
prefix a heading with a number — `## 1. 概述` is a violation. Sections may be
added; a required one is never dropped or renamed.

## Quality Gates

### MUST

- [ ] Frontmatter and required sections for the type
- [ ] Change Log last section; append only
- [ ] Decision-history: newest-first; supersede via strike + link
- [ ] No L1 deletion to meet size cap
- [ ] Sub-problem design has `子问题归属`; missing facts are `UNKNOWN`, not guesses
- [ ] impl-plan: every `IMPL-*` names its dependency and who it blocks; `Execution order` does blocked work later

### NICE

- [ ] Links instead of restating facts owned elsewhere (L4)

## Anti-Patterns

- Large single edits without restructure approval
- Writing implementation class detail into design (see **SPEC-SCOPE.md**)
