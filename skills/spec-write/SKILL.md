---
name: spec-write
description: |
  Use when drafting or editing committed feature spec markdown — PRD, design,
  impl-plan, test-plan, decision-history — under docs/features/. Read
  SPEC-STANDARD.md, SPEC-PRESENTATION.md, and SPEC-HTML-STANDARD.md first.
  Decide new document or which existing documents to edit. Write so an
  undergraduate can read it. Pair with spec-review before commit. HTML is one
  site: a directory of features, and inside a feature the left column is that
  feature's directory.
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
  spec_bundle_version: "1.0.4"
  spec_built_at: "2026-11-24"
  spec_git_sha: "ab9b322"
---
<!-- SPEC-BUNDLE-START -->
> **SDD spec bundle** `1.0.4` · built 2026-11-24 · git `ab9b322`
<!-- SPEC-BUNDLE-END -->

# spec-write

Writes and edits **committed** feature spec prose. Standards: `skills/spec-organize/SPEC-STANDARD.md`, `skills/spec-html-standard/SPEC-PRESENTATION.md`, and `skills/spec-html-standard/SPEC-HTML-STANDARD.md` (one site, ARD-BG). Contract: `docs/features/spec-driven-development/design/spec-driven-development-design-skill-contracts.md` — if this body and the contract disagree, the contract wins.

## When to Use

- Creating or updating prd/design/impl-plan/test-plan/decision-history content
- Appending Decision Log / Change Log entries

## When NOT to Use

- Design adversarial review — **spec-review**
- Mechanical checks — `python3 tools/run_spec_checks.py`

SDD skill map: `skills/SDD-DELIVERABLES.md`.

## Example Domains

Illustrations, not gold. Each edit stays within 10 lines and 200 characters.

- **盖 shed**: one edit adds `PRD-A` for the permit limit. The design ownership row is `许可 | 人决定 | ARD-A`. If the setback distance was not looked up, write `UNKNOWN`.
- **北京旅游**: add the budget requirement. Evidence is a URL. Do not invent a hotel price. The budget later drops: add a new ARD at the top of the Log, strike the old row and link the new one; in the PRD body, just rewrite the number and link the new ARD.
- **数学题**: cite the definition's source. A lemma with no source is `UNKNOWN`. Explain "lemma" at first use, or link the glossary.
- **股票**: the design `子问题归属` row cites the filing URL. No URL means `UNKNOWN`, not a guessed number. An open question "which fiscal year to use" is `QUES-A` in the one tracker, with owner and blocking yes/no.

## Process

1. Read `SPEC-STANDARD.md`, `SPEC-PRESENTATION.md`, and `SPEC-HTML-STANDARD.md` (the **Site** section, ARD-BG).
2. Decide: create a new document from the path rules, or edit existing documents. A new feature directory is created only after the human confirms its name and split in Map; before that, keep the working name, rough PRD and progress in the wayfinder map directory `docs/state/wayfinder-<working-name>/` (ARD-CH). On resume, read the map whose path the CLAUDE layer names.
3. If editing, list every document that states the same fact. Edit the authority document. Replace the other copies with links.
4. Classify each edit as prose, format, style, table, or icon, then apply SPEC-PRESENTATION.
5. Edit an existing file under `docs/` with **≤10 lines and ≤200 characters per edit** (both limits); a new file may be written in one go, but content moved out of an existing file counts as an edit (ARD-CE); split, or ask for a `restructure` and record the authorization as an ARD.
6. Use letter-prefix IDs only (**PRD-A**, **DSGN-B**, **ARD-C**, **IMPL-A**, **TST-A**, **QUES-A**). An Open Questions entry is `QUES-A`, not `OQ-1` or `QUES-1`, and carries question, answer so far, owner, and blocking yes/no.
7. After create/move: regenerate INDEX when the tree changes.
8. Cross-check before finishing: every `PRD-*` id appears in the design; every `TST-*` case names the requirement it covers; an ID from another feature names that feature ("parent test-plan 的 TST-V").
9. On a design with sub-problems, write `子问题归属`: `| 子问题 | 归属 | 依据 |`. Owner is `AI 查`, `人决定`, or `AI 查完人决定`. 依据 is a `raw/` path, a URL, or an `ARD-*` id. If the fact was not found, write `UNKNOWN`. Do not guess. Add rows for blind spots and risks the human did not ask about.
10. A pure standard or orchestration design may say the ownership table does not apply. If every tracker row has Owner and Evidence, link to the tracker instead of copying the table.
11. A `file:line` citation names the commit. A renamed heading keeps the old anchor above the new title.
12. **Readability pass.** Reread each changed section as an undergraduate programmer who has only this document and the glossary (parent design appendix). Rewrite any keyword list or arrow chain as sentences. Explain or link every term at first use; add missing terms to the glossary.
13. After a markdown edit, tell the user which HTML pages are now out of date and ask whether to rebuild now with `python3 tools/build_sdd_site.py`. Before any commit, rebuild so the committed HTML matches the markdown (ARD-CF). Each page is one directory line. A feature page keeps that feature's directory on the left and the page on the right. A hand-maintained HTML file keeps `spec-source-sha256`.
14. When the **diagram-design** skill is installed (it does not ship with SDD): if a section matches a shape in `SPEC-PRESENTATION.md` §Diagram and has no figure yet, add one and cite the SVG. Without it, keep existing figures and add none; do not redraw existing figures unless the user asks.

### By type (quick)

| Type | Focus |
|---|---|
| **prd** | Problem, goals, requirements with **PRD-*** IDs; deferrals → **ARD-** in decision-history |
| **design** | Behavior, contracts, boundaries, ownership table or a link to the question tracker, evidence or `UNKNOWN`. One Open Questions tracker per feature |
| **decision-history** | New **ARD-*** row at **top** of Log, plus an Evidence Appendix entry with the reason and rejected options; supersede = ~~strike~~ the old row + link. The only place strikethrough is used |
| **impl-plan** | Each **IMPL-*** names its dependency, who it blocks, and a done line. Read side before write side. Mock an interface owned by another team or service when it is not live yet |
| **test-plan** | **TST-*** cases; execution order; pass threshold; a Traceability table listing every `PRD-*` |
| **any** | Changing an existing sentence: write the current rule and link the ARD that changed it. No strikethrough outside decision-history (ARD-BM). A typo may be edited in place |

After substantive spec edits, say the HTML is out of date and ask whether to rebuild with `python3 tools/build_sdd_site.py`; rebuild before commit regardless (ARD-CF). The reader assembly, when needed, is `python3 tools/build_sdd_reader.py`. HTML does not change the spec.

### Section headings (MUST)

Use the standard's exact English heading text, unnumbered: `## Overview`,
`## Goals and Success Metrics`, `## Test Cases`, … Never translate, rename, or
prefix a heading with a number — `## 1. 概述` is a violation. Sections may be
added; a required one is never dropped or renamed.

## Quality Gates

### MUST

- [ ] Frontmatter and required sections for the type
- [ ] Change Log last section; append only
- [ ] Decision-history: newest-first; supersede via strike + link; every ARD has an Evidence Appendix entry
- [ ] No L1 deletion to meet size cap
- [ ] Sub-problem design has `子问题归属`; missing facts are `UNKNOWN`, not guesses
- [ ] impl-plan: every `IMPL-*` names its dependency, who it blocks, and a done line; `Execution order` does blocked work later
- [ ] Body text states the current rule and links the ARD that changed it; strikethrough only in decision-history
- [ ] Readable by an undergraduate: complete sentences; every term explained at first use or in the glossary

### NICE

- [ ] Links instead of restating facts owned elsewhere (L4)
- [ ] NICE format rules in SPEC-STANDARD (ARD-BN)

## Anti-Patterns

- Large single edits without restructure approval
- Writing implementation class detail into design (see **SPEC-SCOPE.md**)
- Telegraphic notes: keyword strings, `A → B` arrow chains, cells packed with abbreviations
- Satisfying a format rule by compressing prose until no one can read it
