# Spec HTML Standard (enforceable summary)

**Authoritative spec:** `docs/features/spec-driven-development/features/document-standard/design/document-standard-design-spec-reader-html.md` (**DSGN-N**). PRD: `docs/features/spec-driven-development/features/document-standard/prd/document-standard-prd-spec-reader-html.md` (**PRD-A–P**). If this file and **DSGN-N** diverge, **fix the design first**, then update this summary.

**Not a skill.** Expression rules: `SPEC-PRESENTATION.md`. Agents assemble reader HTML from this standard. spec-write edits markdown; spec-review checks fidelity. No separate `spec-reader` skill.

Hand-maintained HTML (ARD-AK) sets `spec-paired` to `hand-maintained`, `spec-source` to the repo path of the markdown, and `spec-source-sha256` to that file's hash. A mismatch fails `paired_html_stale`. Generated readers omit this meta and are rebuilt. Its changelog has one row for every date in the markdown Change Log (ARD-BA). `<!-- html-skip -->` may wrap L4 or struck history, not L1.

## Output (MUST)

- Path: `docs/book/html/<parent>/<parent>-reader.html`. Other spec HTML mirrors `docs/features/` under `docs/book/html/` (ARD-BF)
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

## Site (MUST, ARD-BG)

One website for the whole project. Entry: `docs/book/html/index.html`.

- Each spec HTML page is one line in the directory.
- The directory opens a feature. It does not dump every feature's pages into one flat list with no feature.
- Inside a feature, the left column is that feature's directory. The right column is the page.
- The left directory lists only the five entry pages: prd, design, impl-plan, test-plan, decision-history. Design parts and the reader expand under design. A sub-feature is one line in that layer, and its own pages expand under that line (DSGN-N-L). Pipeline has no HTML page.
- spec-write rebuilds this site after a spec edit. It does not invent a second layout.

Rebuild: `python3 tools/build_sdd_site.py`

## Links (MUST, DSGN-N-K)

- An ID (`PRD-`, `DSGN-`, `ARD-`, `IMPL-`, `TST-`, `PIPE-`, `QUES-`) links to its definition in the same feature. If a sub-feature does not define that ID, the link goes to the parent.
- A path written in the body is a link. A `.md` under `docs/features/` links to the same path under `docs/book/html/` with `.html`. Any other file that exists links to that file.

## Visual (SHOULD)

Match initiative summary HTML (e.g. `spec-driven-development.html`): self-contained CSS v0; no runtime md fetch for delivery.

## Workflow

- **spec-pipeline:** prompt/trigger after major spec changes or on user request
- **spec-write:** after the markdown edit, rebuild the one site from this standard (`python3 tools/build_sdd_site.py`)
- Conflict or spec bug found while assembling → **Ask human** → fix md → regenerate HTML
- SDD parent: `python3 tools/build_sdd_reader.py` then `python3 tools/validate_sdd_reader.py`

## Sequence / flow diagrams

- Prefer **Mermaid** fenced blocks in `.md`; reader build renders them (`MERMAID-PATTERNS.md` samples).
- ASCII flows acceptable; do not drop L1 labels when converting.

## Reference (structure OK, content must meet fidelity)

`docs/book/html/spec-driven-development/spec-driven-development-reader.html`
