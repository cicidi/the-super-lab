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

## IDs (MUST)

Prefix-letter IDs: `PRD-`, `DSGN-`, `ARD-`, `IMPL-`, `TST-`. No bare numeric permanent IDs. IDs immutable, no reuse.

## Decision history (MUST)

Log: `ID | Date | Decision`, newest first. Supersede: ~~strike~~ + link to new **ARD**; old rows stay.

## Size (MUST)

Hard caps per **DSGN-B** table; never delete **L1** to fit. `decision-history` exempt from trim.

## INDEX / book

Committed tree changes → regenerate INDEX; no orphan/dead link (**DSGN-D**).

## Conflicts (MUST)

Detect → Report → Ask; no silent spec/code side pick (**DSGN-G**).
