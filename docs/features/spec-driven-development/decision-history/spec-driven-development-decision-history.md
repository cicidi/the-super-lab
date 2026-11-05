---
feature: spec-driven-development
type: decision-history
state: final
final_date: 2026-09-25
health: active
owner: cicidi
last_verified: 2026-09-25
---

# Spec-Driven Development — Decision History

Decision Log uses **`ARD-{letter}`** IDs (document-standard **DSGN-F**, **DSGN-J**): newest entry **first**; supersede = ~~strikethrough~~ + link to the replacing **ARD** ID.

## Decision Log

| ID | Date | Decision |
|---|------|----------|
| ARD-Z | 2026-11-04 | Downstream waits until the PRD states limitation, preference, timeline, resource, and tool, each filled or marked not apply, and design plus decision history both exist |
| ARD-Y | 2026-11-04 | Map split: AI offers options; ≤20 hours for one person is one feature spec; over that, split into peer or sub-feature; AI estimates and judges |
| ARD-X | 2026-11-04 | Execution delivery is a mock MCP client call to a mock server; a printed log is success; no live booking or orders |
| ARD-W | 2026-11-04 | Readability is scored by an LLM playing a bachelor's-level programmer; pass means it understands |
| ARD-V | 2026-11-04 | Hard non-software problems stay in this PRD and use the same five artifacts; four gold examples |
| ARD-U | 2026-11-03 | Pipeline deliverable is **spec-pipeline** orchestrator; Map is interview-led with AI-judged outputs; state CLAUDE.local then `raw/state/` |
| ARD-T | 2026-11-03 | wayfinder-import is not an SDD sub-feature; its tree under `features/wayfinder-import/` is removed |
| ARD-S | 2026-11-03 | Gold set grows in both directions and is versioned; scores compare only within one gold version |
| ARD-R | 2026-11-03 | Two eval scores: MUST `x/total` must be full; exemplar score `(plus−minus)×10/total` must not regress |
| ARD-Q | 2026-11-03 | Tests live in `skills/<skill>/tests/`; cross-skill checks, gold, and reports in `spec-organize` |
| ARD-P | 2026-11-03 | `spec-review` detects mechanical MUST violations too; it outputs suggestions, never fixes |
| ARD-O | 2026-11-03 | Skills are `spec-organize` (main), `spec-review`, `spec-write`; the standard file is `spec-organize/SPEC-STANDARD.md` |
| ARD-N | 2026-10-30 | Success-metric measurement and baseline are deferred to PRD-G |
| ARD-M | 2026-10-30 | Multi-participant decision authority is deferred to PRD-F |
| ARD-L | 2026-10-30 | Blind spots are surfaced by existing skills, not a new mechanism |
| ARD-K | 2026-10-30 | Every AI edit to a `.md` under `docs/` is ≤10 lines or ≤200 characters; larger changes split |
| ARD-J | 2026-10-30 | Five stages plus an optional `how-to`; `how-to` is not a stage |
| ARD-I | 2026-09-25 | This feature carries two `spec` documents, against the one-per-type rule |
| ARD-H | 2026-09-25 | Four content priority levels; L1 is never deleted |
| ARD-G | 2026-09-25 | Spec parts take an aspect noun, plan parts take a number plus phase |
| ARD-F | 2026-09-25 | A feature folder may hold more than one `design` or `impl-plan` |
| ARD-E | 2026-09-25 | `design` and `impl-plan` cap at 1,000 lines; `decision-history` is exempt |
| ARD-D | 2026-09-25 | The health field is named `health`, not `status` |
| ARD-C | 2026-09-25 | Detail is carried in sibling files, not inline in `SKILL.md` |
| ARD-B | 2026-09-25 | The standard lives in ~~`doc-organize`~~ `spec-organize` (→ [ARD-O](#ard-o--skills-are-spec-organize-main-spec-review-spec-write-the-standard-file-is-spec-organizespec-standardmd)), not a new skill |
| ARD-A | 2026-09-25 | Authority by concern replaces a single global source of truth |

## Evidence Appendix

### ARD-A — Authority by concern replaces a single global source of truth

The previous rule was "code is the source of truth", stated in three places in
`doc-organize`. It resolves every conflict in one direction and leaves a spec
unable to protect intended behavior: under it, a spec that states a retry count
of 3 while the code retries 5 is simply wrong, even when 3 was the requirement.

Considered and rejected:

- *Keep "code is the source of truth"* — rejected because it makes the spec
  unenforceable precisely where enforcement matters, and because a passing test
  would then also count as a requirement.
- *Declare "spec is the source of truth"* — rejected for the mirror reason: a
  spec cannot answer what the code currently does, and treating it as
  authoritative for implementation would force spec edits for every refactor.
- *Single source with an exception list* — rejected as an unmaintainable middle
  ground that still names one winner by default.

Adopted instead: authority by concern. Intended behavior belongs to the spec,
current implementation to the code, contracts to the machine-readable artifact,
database structure to migrations, and executable verification to the tests.

### ARD-B — The standard lives in `doc-organize`, not a new skill

Placement, linting, and consolidation already belong to `doc-organize`, and its
Sync mode is where drift is detected. A separate skill would have to duplicate
the document standard to know what a spec is.

Considered and rejected: a new `spec-driven-development` skill with
`doc-organize` keeping only a pointer. Rejected because the two would share the
type list, the frontmatter contract, and the required sections, and the copy
would drift.

### ARD-C — Detail is carried in sibling files, not inline in `SKILL.md`

The material is seventeen sections. Inline it would have taken `SKILL.md` past
700 lines, and a skill that must be read in one pass cannot afford that.

Follows the existing pattern: `domain-modeling/ADR-FORMAT.md` and
`domain-modeling/CONTEXT-FORMAT.md`. Sibling files travel with the directory, so
the skill stays portable — it must not point at this repository's `docs/`, which
does not exist in the projects the skill is deployed to.

### ARD-D — The health field is named `health`, not `status`

`state` already tracks the authoring state (`draft` or `final`). A second field
named `status` would be read as the same concept, and it accepted an overlapping
vocabulary (`draft`, `active`, `stale`, `deprecated`) that made the overlap
worse.

Considered and rejected: replacing `state`'s vocabulary with
`draft | active | stale | deprecated`. Rejected because it would invalidate every
existing document to gain a distinction that a second field provides for free.

### ARD-E — `design` and `impl-plan` cap at 1,000 lines; `decision-history` is exempt

The earlier guideline said feature specs run 500-1,500 lines, which contradicts a
1,000-line ceiling. The ceiling wins; the guideline is removed.

`decision-history` is exempt because it is append-only history. Trimming it would
destroy the record that is its entire purpose. Exempting it also means the cap
never creates pressure to delete a superseded decision.

### ARD-F — A feature folder may hold more than one `design` or `impl-plan`

Supersedes the earlier rule "one file per type per feature" for these two types
only, and removes the anti-pattern that forbade a second spec file.

`prd`, `test-plan`, `decision-history`, and `how-to` stay single-file: none of
them grows without bound. `design` and `impl-plan` do, and capping them at 1,000
lines without allowing a second file would have made the cap unmeetable.

### ARD-G — Spec parts take an aspect noun, plan parts take a number plus phase

```
payment-design-authorization.md        aspect noun, unordered
payment-impl-plan-01-schema.md       number plus phase, ordered
```

Considered and rejected: numbering both (`payment-design-01.md`). A number says
nothing about the contents, and inserting a part forces a renumber across the
set. A plan is genuinely ordered, so a number carries meaning there; a spec is
cut by bounded context, so a noun carries meaning there.

### ARD-H — Four content priority levels; L1 is never deleted

L1 decisive (behavior, contracts, invariants, constraints, error semantics,
security rules, architecture boundaries, out of scope, assumptions, compatibility
constraints, open questions), L2 rationale, L3 alternatives, L4 support. Trim L4,
then L3, then compress L2. Never delete L1.

`out of scope`, `assumptions`, `compatibility constraints`, and `open questions`
are filed at L1 rather than L2 because dropping any of them breaks the
implementation in the same way as dropping a stated requirement.

A fact whose authoritative home is another document is L4 as a link, never a
restated copy. This connects the level model to the duplication rule: restating a
fact is a defect, not a level.

### ARD-I — This feature carries two `spec` documents

Deliberate exception to decision ARD-F's one-`spec`-per-feature default, recorded
here because the rule requires a logged reason rather than a silent breach.

This feature is named for the standard itself, so the standard's own spec belongs
to it. `wayfinder-import-design.md` already occupied
`spec-driven-development/design/`, and the wayfinder import is a distinct effort
with its own lifecycle.

Considered and rejected:

- *Rename the feature* — rejected because the initiative name is established in
  the project's working context.
- *Put the standard's spec in its own feature* — rejected because the standard
  and the import are the same initiative; splitting them into two features would
  misrepresent the work.
- *Fold the standard into `wayfinder-import-design.md`* — rejected as a
  restatement: two unrelated documents in one file.

The two files are distinguished by name, following decision ARD-G's aspect rule:
`spec-driven-development-design.md` for the standard, `wayfinder-import-design.md`
for the import.

### ARD-J — Five stages plus an optional `how-to`

The PRD said six artifacts; `pipeline-design.md` and the document standard said
five. The pipeline spec is right about stages: `how-to` is an output for the
case where a human must operate the result, not a step every feature runs.

Considered and rejected: keeping six to match the PRD — rejected because it
invents a stage most features never execute.

### ARD-K — Every AI edit to a docs file is small

A large edit lands unreviewed and is hard to attribute when it breaks something.
The limit is 10 lines or 200 characters; satisfying either is enough. A larger
change is split into sequential edits. A restructure needs explicit human
instruction, which is how this PRD's own revision was applied.

Considered and rejected: hard rejection of oversized edits — rejected because it
blocks a legitimate restructure; warning only — rejected because nothing stops
the edit.

### ARD-L — Blind spots come from existing skills

`research` already has a Discover Unknowns branch and `grill-with-docs` already
runs an adversarial interview. P4 says to use the current tools first.

Considered and rejected: a new dedicated skill — rejected while the existing
mechanism works. A future skill may replace them without changing the
requirement that the step runs.

### ARD-Z — Five PRD fields, then design and decision history

Replaces the undefined six inputs in PIPE-E2. The PRD must state limitation, preference, timeline, resource, and tool. A missing one is marked not apply, not left blank. Downstream starts only after that PRD, the design, and the decision history all exist. Rejected: the word building, and a pointer at PIPE-F for a definition PIPE-F does not hold.

### ARD-Y — Map split uses a 20-hour estimate

Provisional rule (PIPE-D item 6). AI shows several split options. One person able to understand the work within 20 hours stays one feature spec. AI estimates above 20 hours, so it splits into a peer or a sub-feature. AI both estimates and judges. Creating directories still waits for human confirmation (PIPE-D item 5).

### ARD-X — Execution delivery is a mock MCP log

No live booking or trading. A mock MCP client calls a mock MCP server; the printed call log is success (PRD-O). Rejected: real side effects.

### ARD-W — Readability judge is an undergraduate programmer

A second LLM plays a bachelor's-level programmer. Pass only if it understands; otherwise not delivery (PRD-M). ISO 24495-1 was found and not used as the score.

### ARD-V — Hard problems stay on the same five artifacts

Shed, Beijing, a famous math problem, and a stock stay in this PRD (PRD-K) on the same five artifacts. Sub-problems name who acts; claims cite a found fact (PRD-L, PRD-N). Rejected: a new feature.

### ARD-U — spec-pipeline orchestrator and Map/state model

SDD adds **spec-pipeline** as the entry skill that calls spec-organize and
spec-write and prompts for spec-review before commit. **Map** relies on human
interview; outputs (split, decision, scratch) are **AI-judged**, not a fixed
file template. **State** lives in CLAUDE.local until feature create sets `<f>`,
then in `docs/features/<f>/raw/state/`. Rejected: rigid Map MUST artifacts and
repo-root BMAD-style state trees.

### ARD-T — wayfinder-import is not an SDD sub-feature

Wayfinder import is a separate skill-factory / import effort, not part of the
SDD deliverable (spec-organize, spec-review, spec-write). The nested tree under
`spec-driven-development/features/wayfinder-import/` is removed; wayfinder work
continues elsewhere if needed. ARD-I's multi-spec exception remains historical.

### ARD-O — Skills are spec-organize (main), spec-review, spec-write

Deliverable skills use the `spec-` prefix because they serve spec-driven
development, not generic document editing. The standard file stays inside the
main skill as `SPEC-STANDARD.md`, continuing ARD-B's placement rule. Rejected: a
separate `spec-standard` skill — three consumers, one extra copy to drift.

### ARD-P — spec-review detects mechanical MUST violations too

Review outputs modification suggestions, not fixes. Mechanical MUST gaps must
appear in that list or the user gets an incomplete review. Organize Lint may
fix; review detects and suggests. Rejected: semantic-only review — gold-based
eval cannot score review against the same MUST set as organize.

### ARD-Q — Tests live under skills/<skill>/tests/

Skills ship to arbitrary projects; tests must travel with them. Cross-skill
checks, gold, and HTML reports live under `spec-organize` as the main skill.
Rejected: repo-root `tests/sdd/` — assets would not deploy with the skill bundle.

### ARD-R — Two eval scores and gates

MUST compliance is a hard floor (`x/total` full pass). Exemplar comparison uses
`(plus−minus)×10/total` and must not regress within one gold version. Rejected: a
fixed exemplar cutoff — gold version bumps change the denominator.

### ARD-S — Gold set grows and is versioned

New good and bad examples from runs append to `annotations.yaml`; `gold.version`
increments. Scores compare only within one version. Rejected: frozen gold — no
accumulation of review findings.

## Path Update — 2026-10-30

The feature was restructured into sub-features. The paths referenced in the
historical entries now resolve as follows:

| Old path | New path |
|---|---|
| `spec-driven-development-design.md` | `features/pipeline/design/pipeline-design.md` |

The historical entries are preserved as written; this note is the current
pointer. No decision was changed.

## Change Log

| Date | Change |
|------|--------|
| 2026-09-25 | Initial creation; records the SDD standard's adoption and the two-spec exception |
| 2026-10-30 | Added a path-update note after the feature was split into sub-features |
| 2026-10-30 | Added decisions ARD-J–ARD-N from the PRD revision: five stages, small edits, existing-skill blind spots, two deferrals |
| 2026-11-03 | IDs `0001–0014` → `ARD-A`–`ARD-N`; Log 倒序；格式对齐 document-standard **DSGN-E**/**DSGN-J** |
| 2026-11-03 | ARD-O–ARD-S：skill 命名、review 边界、测试位置、eval 评分与门槛、gold 版本化 |
| 2026-11-03 | ARD-T：移除 wayfinder-import sub-feature 树 |
| 2026-11-03 | ARD-U：spec-pipeline 编排；Map interview；state 两阶段 |
| 2026-11-04 | ARD-V–ARD-X：非软件难题留在本 PRD；可读性由本科程序员 LLM 打分；执行以 mock MCP log 为交付 |
| 2026-11-04 | ARD-Y：Map 拆分以一人 20 小时为界，估算和评判由 AI 做 |
| 2026-11-04 | ARD-Z：PRD 五项写明或 not apply；design 与 decision history 都在才进 Downstream |
| 2026-11-04 | PRD-F 关闭 ARD-M 的延期：按 history 时间，否则问用户。无新 ARD（A–Z 已用完） |
