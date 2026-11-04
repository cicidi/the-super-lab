# Spec HTML Standard (enforceable summary)

**Authoritative spec:** `docs/features/spec-driven-development/features/document-standard/design/document-standard-design-spec-reader-html.md` (**DSGN-N**). PRD: `docs/features/spec-driven-development/features/document-standard/prd/document-standard-prd-spec-reader-html.md` (**PRD-A–P**). If this file and **DSGN-N** diverge, **fix the design first**, then update this summary.

**Not a skill.** Agents assemble or update reader HTML by loading this standard (often via **spec-pipeline** Step 6). No separate `spec-reader` skill.

## Output (MUST)

- Path: `docs/features/<parent>/<parent>-reader.html`
- Source of truth: committed `.md` only; HTML is **derived**
- Scope: parent types present (`prd`, `design`, `impl-plan`, `test-plan`, `decision-history`; `how-to` optional); each `features/<sub>/` at least **design** (+ other types if committed)

## Fidelity (MUST — no over-trimming)

Align with document-standard **DSGN-I**:

| Level | In HTML |
|---|---|
| **L1** | Full: MUST/forbidden rows, req/test/impl/decision **table rows**, contract table rows, Out of Scope, IDs — **not** one-paragraph substitutes for whole sections |
| **L2** | Keep facts; may shorten wording, not drop conclusions |
| **L3** | May compress + link to canonical md |
| **L4** | Omit body; **MUST** link to md |

**IDs (**DSGN-F**):** Visible in HTML (`PRD-`, `DSGN-`, `ARD-`, `IMPL-`, `TST-` as in md).

**MUST NOT:** executive-summary-only tabs; fetch + raw md in `<pre>` as main UI; drop **DSGN-***/**PIPE-*** section bodies while keeping headers only.

**MAY:** HTML tables with same row set; callouts; flows; part files as sections/sub-tabs inside one tab.

## Structure (MUST)

- Page header: reading assembly; edit `.md` first; parent slug
- Tabs: parent (one per type); children (per sub-feature)
- Per tab footer: `Canonical:` path(s); all parts listed if split

## Visual (SHOULD)

Match initiative summary HTML (e.g. `spec-driven-development.html`): self-contained CSS v0; no runtime md fetch for delivery.

## Workflow

- **spec-pipeline:** prompt/trigger after major spec changes or on user request
- **spec-write / spec-organize:** md and paths only — not HTML template owner
- Conflict or spec bug found while assembling → **Ask human** → fix md → regenerate HTML
- SDD parent: `python3 tools/build_sdd_reader.py` then `python3 tools/validate_sdd_reader.py`

## Sequence / flow diagrams

- Prefer **Mermaid** fenced blocks in `.md`; reader build renders them (`MERMAID-PATTERNS.md` samples).
- ASCII flows acceptable; do not drop L1 labels when converting.

## Reference (structure OK, content must meet fidelity)

`docs/features/spec-driven-development/spec-driven-development-reader.html`
