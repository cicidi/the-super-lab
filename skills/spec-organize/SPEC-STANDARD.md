# Spec Standard (enforceable summary)

**Authoritative spec:** `docs/features/spec-driven-development/features/document-standard/design/document-standard-design.md` (**DSGN-A–M**). If this file and the design diverge, **fix the design first**, then update this summary.

## Committed types

`prd` | `design` | `impl-plan` | `test-plan` | `decision-history` | `how-to` — under `docs/features/<f>/`. Local only: `raw/**`, `.scratch/`.

## Path & filename (MUST)

- Root: `docs/features/<f>/` (sub: `docs/features/<parent>/features/<sub>/`, frontmatter `feature` = **sub** slug).
- Entry: `<f>-<type>.md` in `<type>/` directory.
- No committed `reference/` type; supporting files beside the citing doc.

## Frontmatter (MUST)

`feature`, `type`, `state` (`draft`|`final`), `final_date` when `final`. Use **`health`**, not `status`.

## Required sections (MUST)

Exact English heading text, unnumbered, `##` level. Add-only: never translate,
rename, or drop a required heading (`## 1. 概述` is a violation).

| Type | Required headings |
|---|---|
| `prd` | Overview, Goals and Success Metrics, User Stories, Functional Requirements, Out of Scope, Resources Needed |
| `design` | Problem Statement, Solution, User Stories, Implementation Decisions, Design, Testing Decisions, Out of Scope, Further Notes, Alternatives Considered, Drawbacks, Risks and Mitigations, Open Questions, Reversibility |
| `impl-plan` | Global Constraints, Acceptance Criteria |
| `test-plan` | Test Cases, Test Execution Order, Expected Pass Threshold |
| `decision-history` | Decision Log, Evidence Appendix |

`Alternatives Considered` lists rejected options and why. `Drawbacks` and
`Risks and Mitigations` are separate: the first is what is bad about the chosen
design, the second is what can go wrong in use. `Open Questions` carries
unresolved items with an owner. `Reversibility` covers undo/return/rollback.
`Acceptance Criteria` is the done bar (KEP's Graduation Criteria, generalized).

`how-to`: Overview, Prerequisites, Steps, Verification (not mechanically checked).

## IDs (MUST)

Prefix-letter IDs: `PRD-`, `DSGN-`, `ARD-`, `IMPL-`, `TST-`. No bare numeric permanent IDs — `IMPL-1`, `TST-3`, `PRD-2` are violations; use letters (`IMPL-A`, `TST-C`). IDs immutable, no reuse.
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
