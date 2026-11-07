# Spec Standard (enforceable summary)

**Authoritative spec:** `docs/features/spec-driven-development/features/document-standard/design/document-standard-design.md` (**DSGN-A–M**). If this file and the design diverge, **fix the design first**, then update this summary.

## Committed types

`prd` | `design` | `impl-plan` | `test-plan` | `decision-history` | `how-to` — under `docs/features/<f>/`. Local only: `raw/**`, `.scratch/`.

## Path & filename (MUST)

- Root: `docs/features/<f>/` (sub: `docs/features/<parent>/features/<sub>/`, frontmatter `feature` = **sub** slug).
- Entry: `<f>-<type>.md` in `<type>/` directory.
- No committed `reference/` type; supporting files beside the citing doc.

## Frontmatter (MUST)

`feature`, `type`, `state` (`draft`|`final`), `final_date` when `final`. Use **`health`**, not `status`. Optional `audience` is `internal` or `external` (ARD-AL). Each section names the artifact that is authoritative for that fact.

## Required sections (MUST)

Exact English heading text, unnumbered, `##` level. Add-only: never translate,
rename, or drop a required heading (`## 1. 概述` is a violation).

| Type | Required headings |
|---|---|
| `prd` | Overview, Goals and Success Metrics, User Stories, Functional Requirements, Out of Scope, Resources Needed |
| `design` | Problem Statement, Solution, User Stories, Implementation Decisions, Design, Testing Decisions, Out of Scope, Further Notes, Alternatives Considered, Drawbacks, Risks and Mitigations, Open Questions, Reversibility |
| `impl-plan` | Global Constraints, Acceptance Criteria |

Each `IMPL-*` names what it depends on and what it blocks. `Execution order` puts blocked work later (change the DB before the API that uses it). High-priority unblocked work goes first. Unblocked work can proceed in parallel. spec-write enforces this when drafting.
| `test-plan` | Test Cases, Test Execution Order, Expected Pass Threshold |
| `decision-history` | Decision Log, Evidence Appendix |

`Alternatives Considered` lists rejected options and why. `Drawbacks` and
`Risks and Mitigations` are separate: the first is what is bad about the chosen
design, the second is what can go wrong in use. `Open Questions` carries
unresolved items with an owner. `Reversibility` covers undo/return/rollback.
`Acceptance Criteria` is the done bar (KEP's Graduation Criteria, generalized).

`how-to`: Overview, Prerequisites, Steps, Verification (not mechanically checked).

## IDs (MUST)

Prefix-letter IDs: `PRD-`, `DSGN-`, `ARD-`, `IMPL-`, `TST-`, `QUES-`. Open questions use `QUES-A`, not `OQ-1` or `QUES-1`. No bare numeric permanent IDs — `IMPL-1`, `TST-3`, `PRD-2` are violations; use letters (`IMPL-A`, `TST-C`, `QUES-A`). IDs immutable, no reuse.
Every `PRD-*` id must be anchored in at least one design clause (TST-O).

## Sub-problem ownership (MUST, PRD-L / PIPE-L)

A design for a feature with sub-problems carries a `子问题归属` table:
`| 子问题 | 归属 | 依据 |`. Owner is one of `AI 查`, `人决定`, `AI 查完人决定`;
evidence is a `raw/` path, a URL, or an `ARD-*` id. Unknowns are written
`UNKNOWN`, never guessed. A pure standard/orchestration design may state not apply.

## Decision history (MUST)

Log: `ID | Date | Decision`, newest first. Supersede: ~~strike~~ + link to new **ARD**; old rows stay.

## Size (MUST)

Hard caps per **DSGN-B** table; never delete **L1** to fit. `decision-history` has no hard cap.

## INDEX / book

Committed tree changes → regenerate INDEX; no orphan/dead link (**DSGN-D**).
MkDocs / Pages 发布 nav 属 impl；不得与 feature 树、INDEX 矛盾（**DSGN-D**）。

## Conflicts (MUST)

Detect → Report → Ask; no silent spec/code side pick (**DSGN-G**).

## Chapter 1 — Path, permission, scope

**spec-write** may create or edit committed spec markdown. **spec-review** reports only. Paths and filenames follow **Path & filename** above. One fact has one home; other docs link to it. Before editing, list every doc that states the same fact and change those to links.

Each section states which artifact is authoritative for that fact (ARD-A). A design's 13 required sections apply when the design is a procedural aspect. A pure standard or orchestration design may say a section does not apply. Old heading anchors stay so existing links keep working.

## Chapter 2 — What to write, what to skip, how to say it

Write behavior, contracts, invariants, constraints, error semantics, and boundaries. Do not write class hierarchies, private methods, or internal algorithms (`SPEC-SCOPE.md`). Levels L1–L4: never delete L1.

Invariants are a table or a named value, not a slogan. Strikethrough is only for a superseded decision-history row. Body text that changes points at the new ARD. A translation is a copy; the source-language document stays authoritative. Required headings stay English and unnumbered. Numbered headings are only for an ordered procedure.

Each `IMPL-*` states its done bar. When the step cannot run live, state the mock. Expression form is `skills/spec-html-standard/SPEC-PRESENTATION.md`.

## Chapter 3 — Evidence, citation, reference, commit

A conclusion cites a `raw/` path, a URL, an `ARD-*` id, or a commit. If the fact was not found, write `UNKNOWN`. Do not guess. A code citation names the commit.

One open problem has one tracker row (`QUES-*` or the `子问题归属` table), not a second copy. Decision-history rows may be revised in place; when listing open items, group them by owner. `reference/` is not a committed type.

## Before create or edit (MUST)

1. Read chapters 1–3 and SPEC-PRESENTATION.md.
2. Decide: new document from the path rules, or edit existing documents.
3. If editing, name every document that states the same fact. Edit the authority document. Replace the other copies with links.
4. Classify the edit as prose, format, style, table, or icon, then apply SPEC-PRESENTATION.md.

## Review rules (ARD-AM–BE)

These restate the design. If they diverge, fix the design first.

- Step numbers are positions, not permanent ids (ARD-AM). A task names the step range it implements.
- Readiness may be written in the decision row. Revise in place. Group open items by owner (ARD-AN).
- One open-question tracker per feature. Other docs link. `QUES-` plus a letter, with Question, Answer, Owner (ARD-AO).
- Keep an old-to-new table when ids move. Keep the old anchor when a heading is renamed (ARD-AP).
- A `file:line` citation names its commit (ARD-AQ).
- An invariant is a table (ARD-AR). Body text that drops a claim points at the new ARD (ARD-AS).
- Each `IMPL-*` has a done line, read-before-write order, and a mock when the partner port is not live (ARD-AT).
- A local `<name>.<lang>.md` is not committed. Its opening names the source (ARD-AU).
- Required sections apply to the design entry. A part links back (ARD-AV). Required headings stay unnumbered; a procedure section may be numbered (ARD-AW).
- Decision Log may add Ready. No Status column. No Supersedes column (ARD-AX).
- A tracker with Owner and Evidence on every row may replace the ownership table (ARD-AY).
- A §N link lands on N or its parent or child. Step ranges do not overlap (ARD-AZ).
- A hand-maintained HTML changelog has a row for every markdown Change Log date (ARD-BA).
- Tracker counts match the rows (ARD-BB). A QUES citation's status matches the tracker (ARD-BC).
- External gold is a manifest only (ARD-BD). One flow, one diagram; message count equals the step range (ARD-BE).
