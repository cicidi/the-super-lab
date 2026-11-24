# Spec Standard (enforceable summary)

**Authoritative spec:** `docs/features/spec-driven-development/features/document-standard/design/document-standard-design.md` (**DSGN-A–M**). If this file and the design diverge, **fix the design first**, then update this summary.

Rules are **MUST** (a violation is a failure) or **NICE** (a reminder, never a failure). The split is ARD-BN. Only MUST rules go into `must_registry.yaml`.

## Committed types

`prd` | `design` | `impl-plan` | `test-plan` | `decision-history` | `how-to` — under `docs/features/<f>/`. Local only: `raw/**`, `.scratch/`.

## Path & filename (MUST)

- Root: `docs/features/<f>/` (sub: `docs/features/<parent>/features/<sub>/`, frontmatter `feature` = **sub** slug).
- Entry: `<f>-<type>.md` in `<type>/` directory. Parts: `<f>-design-<noun>.md`; `<f>-impl-plan-<NN>-<phase>.md`.
- All six types may split into parts. When a type has parts, the entry file `<f>-<type>.md` must exist and link to each part (ARD-BQ).
- No committed `reference/` type; supporting files beside the citing doc. Figure SVG: `<doc-stem>-fig-<slug>.svg` next to the citing `.md` (ARD-CA).

## Frontmatter (MUST)

`feature`, `type`, `state` (`draft`|`final`), `final_date` when `final`. Use **`health`**, not `status`. Optional: `spec_id`, `version`, `owner`, `last_verified`, and `audience` (`internal` or `external`, ARD-AL); full list in document-standard **DSGN-E**.

## Required sections (MUST)

Exact English heading text, unnumbered, `##` level. Add-only: never translate,
rename, or drop a required heading (`## 1. 概述` is a violation). If a required
section does not apply, keep the heading and say why in one sentence, or link
to where the fact lives.

| Type | Required headings |
|---|---|
| `prd` | Overview, Goals and Success Metrics, User Stories, Functional Requirements, Out of Scope, Resources Needed |
| `design` | Problem Statement, Solution, User Stories, Implementation Decisions, Design, Testing Decisions, Out of Scope, Further Notes, Alternatives Considered, Drawbacks, Risks and Mitigations, Open Questions, Reversibility |
| `impl-plan` | Global Constraints, Acceptance Criteria, plus one `## IMPL-*` section per task |
| `test-plan` | Test Cases, Test Execution Order, Expected Pass Threshold |
| `decision-history` | Decision Log, Evidence Appendix |

`how-to`: Overview, Prerequisites, Steps, Verification (not mechanically checked).

A split design carries the 13 sections in the entry file only; each part links back to the entry (ARD-AV).

`Alternatives Considered` lists rejected options and why. `Drawbacks` and
`Risks and Mitigations` are separate: the first is what is bad about the chosen
design, the second is what can go wrong in use. `Open Questions` carries
unresolved items with an owner. `Reversibility` covers undo/return/rollback.
`Acceptance Criteria` is the done bar (KEP's Graduation Criteria, generalized).

## impl-plan tasks (MUST)

Each `IMPL-*` names what it depends on, what it blocks, and a done line (`Verify:` or `完成标准`). `Execution order` puts blocked work later (change the DB before the API that uses it). High-priority unblocked work goes first; unblocked work can proceed in parallel. Read side before write side; when a partner port is not live, state the mock (ARD-AT).

## IDs (MUST)

Prefix-letter IDs: `PRD-`, `DSGN-` (`PIPE-` in the pipeline design), `ARD-`, `IMPL-`, `TST-`, `QUES-`. Open questions use `QUES-A`, not `OQ-1` or `QUES-1`. No bare numeric permanent IDs — `IMPL-1`, `TST-3`, `PRD-2` are violations; use letters (`IMPL-A`, `TST-C`, `QUES-A`). A sub-clause may add one more letter (`DSGN-N-A`, `PIPE-E-A`), never a digit (`PIPE-E1` is a violation; ARD-BR). IDs are immutable and never reused; when ids move, keep an old-to-new table, and keep the old anchor above a renamed heading (ARD-AP).
IDs are unique within one feature and one doc type; cite another feature's id as `<feature>/<id>` or name the feature in the sentence.
Every `PRD-*` id must be anchored in at least one design clause (TST-O).

## Edits to existing prose (MUST)

Body text states the current rule only. When a sentence no longer holds, rewrite it and link the ARD that changed it. Strikethrough appears **only** in decision-history (a superseded row, struck and linked to the new ARD). Older body wording lives in git history. A typo is fixed in place (ARD-BM, ARD-AS).

Edit size for AI edits under `docs/`: at most 10 lines **and** at most 200 characters per edit to an existing file, both limits at once (ARD-BP); creating a new file is exempt but still meets **Size** (ARD-CE); a larger change needs explicit human authorization recorded as an ARD (parent design DSGN-A). Content edits go through spec-write; spec-organize Lint may fix format-class MUST violations directly, under the same cap (ARD-BV).

## Readability (MUST)

An undergraduate programmer who reads only this one document must understand it (PRD-M, ARD-BO; tested by TST-V).

- Write complete sentences. A keyword list, a chain of arrows (`A → B → fails`), or a cell full of abbreviations is not a sentence.
- Explain every term or abbreviation at first use, or link it to the glossary. The glossary lives in one place: the parent design's appendix (`#glossary`). Add new terms there.
- Body text may mix Chinese and English when it reads smoothly; an author's own words (such as a Problem Statement) keep their voice. Required headings and IDs stay English (ARD-BS).
- Prefer the plain word over the coined one. If a sentence needs an ID to make sense, say in words what the ID means the first time.

## Open questions (MUST)

One tracker per feature, usually the design's `## Open Questions`. Other docs link to it, never copy it (ARD-AO). Each entry: `QUES-` plus a letter, the question, the answer so far, the owner, and **blocking** yes/no (ARD-AG). A blocking open question stops Downstream (pipeline PIPE-E-A). A citation's open/closed status matches the tracker (ARD-BC).

## Sub-problem ownership (MUST, PRD-L / PIPE-L)

A design for a feature with sub-problems carries a `子问题归属` table:
`| 子问题 | 归属 | 依据 |`. Owner is one of `AI 查`, `人决定`, `AI 查完人决定`;
evidence is a `raw/` path, a URL, or an `ARD-*` id. Unknowns are written
`UNKNOWN`, never guessed. A pure standard/orchestration design may state not apply.
The AI must add rows for blind spots and risks the human did not ask about (PIPE-L).
If every tracker row has Owner and Evidence, the design may link the tracker instead (ARD-AY).

## Decision history (MUST)

Log: `ID | Date | Decision` (optional 4th column `Ready`; no Status, no Supersedes column), newest first. Each ARD has an Evidence Appendix entry with its reason and rejected options. Supersede: ~~strike~~ the old row + link to the new **ARD**; old rows stay. When only part of an old decision is overturned, still strike the whole row, and restate the parts that still hold in the new ARD (ARD-BT).

## Size (MUST)

Hard caps per **DSGN-B** table (prd 800, design 1000, impl-plan 1000, test-plan 800, how-to 600); never delete **L1** to fit. `decision-history` has no hard cap. Struck decision-log rows are kept; when a document must shrink, compress struck content first (ARD-CL).

## INDEX / book (MUST)

When the committed tree changes, regenerate INDEX. A `final` or merged change must reach the book; a `draft` source may skip the summary update (**DSGN-D**). No orphan, no dead link, no dead anchor (**DSGN-D**, ARD-AP). A link into `raw/` is not a dead link, even though `raw/` is never committed (ARD-BW).
Before a commit that changes markdown, rebuild the site so committed HTML matches it (ARD-CF). MkDocs / Pages nav is implementation; it must not contradict the feature tree or INDEX (**DSGN-D**).

## Conflicts (MUST)

Detect, then report, then ask; never silently pick the spec side or the code side (**DSGN-G**). Multi-person decisions: the later decision-history entry wins; if the order is unclear, ask the user (PRD-F).

## Figures (MUST, ARD-CA)

A figure states no fact that prose does not state, and never contradicts prose; L1 text never lives only in a figure. spec-review reports a break at severity 3 and names the SVG file. The SVG is static (no script); its file name and place are in Path & filename.

## Chapter 1 — Path, permission, scope

**spec-write** may create or edit committed spec markdown. **spec-review** reports only. Paths and filenames follow **Path & filename** above. One fact has one home; other docs link to it. Before editing, list every doc that states the same fact and change those to links.

## Chapter 2 — What to write, what to skip, how to say it

Write behavior, contracts, invariants, constraints, error semantics, and boundaries. Do not write class hierarchies, private methods, or internal algorithms (`SPEC-SCOPE.md`). Levels L1–L4: never delete L1.

A translation copy `<name>.<lang>.md` is local only and names the source (ARD-AU). Required headings stay English and unnumbered. Numbered headings are only for an ordered procedure; the one exception is the author's own numbered subheadings under Problem Statement (ARD-BS, which restates ARD-AW). Expression form is `skills/spec-html-standard/SPEC-PRESENTATION.md`.

## Chapter 3 — Evidence, citation, reference, commit

A conclusion is stated in the committed document and cites a `raw/` path, a URL, an `ARD-*` id, or a commit. A `raw/` path alone is valid evidence, even though other readers cannot open it (ARD-BW). If the fact was not found, write `UNKNOWN`. Do not guess. A `file:line` citation names the commit (ARD-AQ). An external gold is a manifest only, never a copy of someone else's spec (ARD-BD).

## Before create or edit (MUST)

1. Read this file and SPEC-PRESENTATION.md; for HTML pages, also `skills/spec-html-standard/SPEC-HTML-STANDARD.md` (three standard files, ARD-BX).
2. Decide: new document from the path rules, or edit existing documents.
3. If editing, name every document that states the same fact. Edit the authority document. Replace the other copies with links.
4. Classify the edit as prose, format, style, table, or icon, then apply SPEC-PRESENTATION.md.
5. Reread the result as an undergraduate who has only this document and the glossary.

## NICE rules (reminders, not failures — ARD-BN)

- Each section may say which artifact is authoritative for its facts (ARD-AL, second half).
- Step numbers are positions, not permanent ids; a task names the step range it implements (ARD-AM).
- Readiness may be written in the decision row; rows may be revised in place; group open items by owner (ARD-AN).
- An invariant is a table (ARD-AR).
- A §N link lands on N or its parent or child; step ranges do not overlap (ARD-AZ).
- A hand-maintained HTML changelog has a row for every markdown Change Log date (ARD-BA).
- Tracker counts match the rows (ARD-BB).
- ≤9 nodes and ≤12 edges per figure; diagram-design default fonts and skin (ARD-CA).
- Heading levels do not skip; terms match `CONTEXT.md`; `last_verified` is recent.
