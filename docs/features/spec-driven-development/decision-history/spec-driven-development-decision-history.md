---
feature: spec-driven-development
type: decision-history
state: final
final_date: 2026-09-25
health: active
owner: cicidi
last_verified: 2026-11-04
---

# Spec-Driven Development — Decision History

Decision Log uses **`ARD-{letter}`** IDs (document-standard **DSGN-F**, **DSGN-J**): newest entry **first**; supersede = ~~strikethrough~~ + link to the replacing **ARD** ID.

## Decision Log

| ID | Date | Decision |
|---|------|----------|
| ARD-BG | 2026-11-07 | One site at docs/book/html/index.html. Each spec page is one directory line. The directory opens a feature. Inside a feature the left side is that feature's directory and the right side is the page |
| ARD-BF | 2026-11-07 | Spec HTML lives under docs/book/html/ and mirrors docs/features/. Parent and sub-feature HTML both go there. Markdown stays in the feature tree |
| ARD-BE | 2026-11-07 | A diagram explains a flow prose cannot. One flow, one diagram. A steps a–b heading that contains a sequence diagram has b−a+1 messages |
| ARD-BD | 2026-11-07 | External gold is a manifest of commits and expected findings. The private spec text is not copied into this repo |
| ARD-BC | 2026-11-07 | A QUES citation's status mark matches the tracker. A closed item is not called open in the citing prose |
| ARD-BB | 2026-11-07 | Tracker counts match: all N questions equals the row count; each status tally equals rows with that status |
| ARD-BA | 2026-11-07 | A hand-maintained HTML changelog has one row for each date in the markdown Change Log |
| ARD-AZ | 2026-11-07 | A §N link lands on heading N or its parent or child. Steps ranges in one doc do not overlap |
| ARD-AY | 2026-11-07 | A design may link to a question tracker instead of copying the ownership table, when every tracker row has Owner and Evidence |
| ARD-AX | 2026-11-07 | Decision Log may add a Ready column. Status and Supersedes columns stay forbidden |
| ARD-AW | 2026-11-07 | Required headings stay English and unnumbered. A section added for an ordered procedure may be numbered |
| ARD-AV | 2026-11-07 | A split design requires the 13 sections only on the entry file. A part links back and covers its own aspect |
| ARD-AU | 2026-11-07 | A local translation is not committed. Its first lines name the source file as authoritative. Headings may be translated |
| ARD-AT | 2026-11-07 | Each IMPL task has a done line. Order is read side before write side. An unbuilt partner port has a mock |
| ARD-AS | 2026-11-07 | Body text that drops an old claim points at the new ARD. Strike stays for decision history. Typos may be edited in place |
| ARD-AR | 2026-11-07 | An invariant is a table of records or impossible states, not a slogan |
| ARD-AQ | 2026-11-07 | A file:line citation in design or impl-plan names the commit it was read at |
| ARD-AP | 2026-11-07 | An id migration keeps an old-to-new table. A renamed heading keeps the old anchor |
| ARD-AO | 2026-11-07 | One open-question tracker per feature. Other docs link to it. Entries are QUES-letter with Question, Answer, and Owner |
| ARD-AN | 2026-11-07 | Readiness may be recorded in the decision text or a Ready mark. A row may be revised in place. Open items group by owner |
| ARD-AM | 2026-11-07 | A procedure step number is a position, not a permanent id. Impl and test cite the same step range |
| ARD-AL | 2026-11-07 | Optional frontmatter audience is internal or external. Each section names its authoritative artifact. Design section ids need not match a partner design |
| ARD-AK | 2026-11-07 | Markdown is the full text. Hand-maintained HTML carries spec-source and sha256; a mismatch is paired_html_stale. Generated HTML is rebuilt |
| ARD-AJ | 2026-11-07 | Entry skills are spec-write and spec-review. Standards: SPEC-STANDARD.md and SPEC-PRESENTATION.md. spec-organize and spec-pipeline are not entry skills |
| ARD-AI | 2026-11-04 | This spec consolidation is an explicitly authorized restructure; larger-than-10-line edits are allowed for this batch |
| ARD-AH | 2026-11-04 | The human-readable reader is the only HTML deliverable; the legacy summary HTML is deleted |
| ARD-AG | 2026-11-04 | Convergence is auto-decided: open decisions must carry a structured `blocking` flag; AI does not self-declare "stable" |
| ARD-AF | 2026-11-04 | Deliberately undefined: failure policy, skill/spec versioning, source-trust grading, data cleanup; no legacy migration |
| ARD-AE | 2026-11-04 | Non-software problems map to the same five artifacts; design carries the ownership table; evidence is mandatory and unknowns are marked UNKNOWN |
| ARD-AD | 2026-11-04 | Eval uses deepseek-flash with 3 independent runs; gold has case/version/exemplar/annotations; runs and reports are not committed; four examples are skill-doc examples, not repo gold |
| ARD-AC | 2026-11-04 | PRD required sections drop NFR; IDs are scoped feature+type and cross-feature references use feature/ID; how-to stays unchecked |
| ~~ARD-AB~~ | 2026-11-04 | ~~Four deliverables: spec-pipeline, spec-organize, spec-review, spec-write~~ → [ARD-AJ](#ard-aj--entry-skills-are-spec-write-and-spec-review) |
| ARD-AA | 2026-11-04 | Multi-participant decisions use the latest decision-history entry; if order is unclear, ask the user; AI never guesses |
| ARD-Z | 2026-11-04 | Downstream waits until the PRD states limitation, preference, timeline, resource, and tool, each filled or marked not apply, and design plus decision history both exist |
| ARD-Y | 2026-11-04 | Map split: AI offers options; ≤20 hours for one person is one feature spec; over that, split into peer or sub-feature; AI estimates and judges |
| ARD-X | 2026-11-04 | Execution delivery is a mock MCP client call to a mock server; a printed log is success; no live booking or orders |
| ARD-W | 2026-11-04 | Readability is scored by an LLM playing a bachelor's-level programmer; pass means it understands |
| ~~ARD-V~~ | 2026-11-04 | ~~Hard non-software problems stay in this PRD and use the same five artifacts; four gold examples~~ → [ARD-AD](#ard-ad--eval-uses-deepseek-flash-with-3-independent-runs) |
| ~~ARD-U~~ | 2026-11-03 | ~~Pipeline deliverable is spec-pipeline orchestrator; Map is interview-led; state CLAUDE.local then raw/state/~~ → [ARD-AJ](#ard-aj--entry-skills-are-spec-write-and-spec-review) |
| ARD-T | 2026-11-03 | wayfinder-import is not an SDD sub-feature; its tree under `features/wayfinder-import/` is removed |
| ARD-S | 2026-11-03 | Gold set grows in both directions and is versioned; scores compare only within one gold version |
| ARD-R | 2026-11-03 | Two eval scores: MUST `x/total` must be full; exemplar score `(plus−minus)×10/total` must not regress |
| ARD-Q | 2026-11-03 | Tests live in `skills/<skill>/tests/`; cross-skill checks, gold, and reports in `spec-organize` |
| ARD-P | 2026-11-03 | `spec-review` detects mechanical MUST violations too; it outputs suggestions, never fixes |
| ~~ARD-O~~ | 2026-11-03 | ~~Skills are `spec-organize` (main), `spec-review`, `spec-write`; the standard file is `spec-organize/SPEC-STANDARD.md`~~ → [ARD-AB](#ard-ab--four-skills-including-spec-pipeline) |
| ARD-N | 2026-10-30 | Success-metric measurement and baseline are deferred to PRD-G |
| ~~ARD-M~~ | 2026-10-30 | ~~Multi-participant decision authority is deferred to PRD-F~~ → [ARD-AA](#ard-aa--multi-participant-decisions-use-the-latest-history-entry-otherwise-ask) |
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
repo-root BMAD-style state trees. Superseded as an entry skill by ARD-AJ.
Create, Map, Converge, and Downstream stay in pipeline-design as reference steps.

### ARD-T — wayfinder-import is not an SDD sub-feature

Wayfinder import is a separate skill-factory / import effort, not part of the
SDD deliverable (spec-organize, spec-review, spec-write). The nested tree under
`spec-driven-development/features/wayfinder-import/` is removed; wayfinder work
continues elsewhere if needed. ARD-I's multi-spec exception remains historical.

<a id="ard-o--skills-are-spec-organize-main-spec-review-spec-write-the-standard-file-is-spec-organizespec-standardmd"></a>

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

### ARD-AA — Multi-participant decisions use the latest history entry, otherwise ask

PRD-F is closed. When two decisions conflict, the later entry in decision-history wins; if the order cannot be established, ask the user. The AI never guesses who is authoritative. Supersedes ~~ARD-M~~.

### ARD-AB — Four skills including spec-pipeline

The deliverable is four skills: spec-pipeline (orchestrator), spec-organize (standard/lint), spec-review (findings), spec-write (edits). Supersedes ~~ARD-O~~, which listed three.

### ARD-AC — PRD and document standard changes

PRD required sections drop Non-Functional Requirements; the parent PRD fills Overview, Goals and Success Metrics, User Stories, Functional Requirements, and Out of Scope. IDs are scoped to feature + type; cross-feature references use `<feature>/<ID>`. HLD architecture sections do not require DSGN IDs; `how-to` stays defined but unchecked.

### ARD-AD — Eval uses deepseek-flash with 3 independent runs

Only the DeepSeek API is available, so gold generation and checker verdicts use three independent runs of `deepseek-flash`; cross-model bias is Unverified. Gold uses four terms: gold case, gold version, exemplar, annotations. `runs/` and `reports/` are not committed. The four non-software examples (shed, Beijing, math, stock) are skill-doc examples; their gold lives elsewhere. Supersedes the gold-example part of ~~ARD-V~~.

### ARD-AE — Non-software mapping, ownership, evidence, and UNKNOWN

Non-software problems use the same five artifacts: research in `raw/research/`, decisions in decision-history, execution in design/impl-plan, verification in test-plan. Each feature design carries a sub-question ownership table (AI查 / 人决定 / AI查完人决定); every claim cites a source; unknowns are marked `UNKNOWN`. Unverified items use `Unverified: <reason> (<condition>)`.

### ARD-AF — Deliberately undefined areas

Failure policy, skill/spec versioning, source-trust grading, and data cleanup are intentionally not defined. Existing non-compliant features are not migrated; only the SDD tree is fixed.

### ARD-AG — Convergence is auto-decided

PIPE-E1–E3 are checked automatically; every open decision must carry a structured `blocking` flag. The AI does not self-declare the spec "stable": the automatic check passes only when no blocking item remains.

### ARD-AH — Reader is the only HTML deliverable

`spec-driven-development-reader.html` is the human-readable deliverable. The legacy `spec-driven-development.html` summary is deleted; references point to the reader.

### ARD-AI — This consolidation is an authorized restructure

The human explicitly authorized a one-shot consolidation of the SDD spec docs. Edits larger than the normal 10-line / 200-character cap are allowed for this batch; the normal cap resumes afterward.

### ARD-AJ — Entry skills are spec-write and spec-review

Entry skills are spec-write and spec-review. Path, permission, scope, what to write, and evidence live in `skills/spec-organize/SPEC-STANDARD.md`. Prose, format, style, tables, and icons live in `skills/spec-html-standard/SPEC-PRESENTATION.md`. spec-organize and spec-pipeline are not entry skills. Supersedes ~~ARD-AB~~.

### ARD-AK — Markdown is the full text

A generated reader is rebuilt from markdown and carries no `spec-paired` meta. A hand-maintained HTML file names its markdown in `spec-source` and stores `spec-source-sha256`. If the hash differs, check `paired_html_stale` fails.

### ARD-AL — Audience and per-section authority

`audience` may be `internal` or `external`. A missing key is not a failure, so existing documents stay valid. Any other value fails `frontmatter`. A section states which artifact owns its facts. A partner design may use different section ids.

### ARD-AM — Step numbers are positions

A step number locates a procedure. It is not a permanent id. Inserting a step renumbers that section and the citations of it.

### ARD-AN — Readiness and in-place revision

A decision may say it is settled here and waiting on another team. Wording may be revised in the same row. Open items are grouped by owner.

### ARD-AO — One question tracker

When many docs cite the same questions, one tracker holds them. Other docs link. A tracker entry is `QUES-` plus a letter, with Question, Answer, and Owner.

### ARD-AP — Old anchors stay

An id migration keeps an old-to-new table. A renamed heading keeps the previous anchor.

### ARD-AQ — Cite the commit

A `file:line` citation in design or impl-plan names the commit it was read against.

### ARD-AR — Invariants as data

An invariant is a table of stored records, or of states that must not occur, with who guarantees each row.

### ARD-AS — Point at the new decision

Prose that drops an old claim points at the replacing ARD. A typo may be edited in place. Strike-through stays the decision-history form.

### ARD-AT — Done line, order, mock

Each `IMPL-*` has a done line. Work that reads runs before work that writes. A partner port that is not live has a mock.

### ARD-AU — Translation is a local copy

A `<name>.<lang>.md` copy is not committed. Its opening names `<name>.md` as the source. Headings in the copy may be translated.

### ARD-AV — Required sections on the entry

A design split into parts requires the full section list only on `<f>-design.md`. A part links back and writes only its aspect.

### ARD-AW — Number only a procedure

Required headings stay the English text, unnumbered. A section that exists to hold an ordered procedure may carry a number.

### ARD-AX — Optional Ready column

The Decision Log may add Ready. It still has no Status column and no Supersedes column.

### ARD-AY — Tracker may replace the ownership table

If every tracker row has Owner and Evidence, the design may link to that tracker instead of copying the ownership table.

### ARD-AZ — Section links and step ranges

A link written as §N lands on heading N or on its parent or child. Step ranges in one document do not overlap.

### ARD-BA — HTML changelog covers each md date

A hand-maintained reader has a changelog row for every date in the markdown Change Log.

### ARD-BB — Tracker counts match

`all N questions` equals the number of tracker rows. A status tally equals the rows that carry that status.

### ARD-BC — Cited status matches the tracker

The status next to a QUES link matches the tracker row. A closed row is not described as still open.

### ARD-BD — External gold stays outside

The manifest stores the repo path, the defect commit, the gold commit, expected findings, and allowed misses. The private spec text is not copied here.

### ARD-BE — Diagrams carry the flow

One flow, one diagram. A heading that says steps a–b and contains a sequence diagram has b−a+1 messages. State lives in a table. The diagram adds no fact the prose lacks.

### ARD-BF — Spec HTML under book

`docs/book/html/` repeats the `docs/features/` tree. A parent reader is `docs/book/html/<parent>/<parent>-reader.html`. Other spec HTML uses that same relative path with a `.html` suffix. Markdown stays in `docs/features/`.

### ARD-BG — One site, feature directory on the left

`docs/book/html/index.html` lists every feature. Each spec page is one line in that directory. Opening a feature shows that feature's pages on the left and the page body on the right.

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
| 2026-11-03 | 旧数字 ID → `ARD-A`–`ARD-N`; Log 倒序；格式对齐 document-standard **DSGN-E**/**DSGN-J** |
| 2026-11-03 | ARD-O–ARD-S：skill 命名、review 边界、测试位置、eval 评分与门槛、gold 版本化 |
| 2026-11-03 | ARD-T：移除 wayfinder-import sub-feature 树 |
| 2026-11-03 | ARD-U：spec-pipeline 编排；Map interview；state 两阶段 |
| 2026-11-04 | ARD-V–ARD-X：非软件难题留在本 PRD；可读性由本科程序员 LLM 打分；执行以 mock MCP log 为交付 |
| 2026-11-04 | ARD-Y：Map 拆分以一人 20 小时为界，估算和评判由 AI 做 |
| 2026-11-04 | ARD-Z：PRD 五项写明或 not apply；design 与 decision history 都在才进 Downstream |
| 2026-11-04 | PRD-F 关闭 ARD-M 的延期：按 history 时间，否则问用户。无新 ARD（A–Z 已用完） |
| 2026-11-04 | ARD-AA–AI：PRD-F 关闭、4 skill、文档标准、eval、非软件映射、未定义项、自动收敛、reader、restructure 授权 |
| 2026-11-07 | ARD-AJ：入口改为 spec-write 与 spec-review；标准两份文档；organize 与 pipeline 不再是入口 |
| 2026-11-07 | ARD-U 划掉并链到 ARD-AJ；四阶段名称留在 pipeline-design 作参考 |
| 2026-11-07 | ARD-AK：手写 HTML 用 spec-source 与 sha256；不一致则 paired_html_stale |
| 2026-11-07 | ARD-AL：audience 只允许 internal 或 external；缺省不算失败 |
| 2026-11-07 | ARD-AM–BE：步骤号、tracker、锚点、commit、图、外部 gold（逐字稿） |
| 2026-11-07 | 保留 ARD-O 旧锚点（ARD-AP） |
| 2026-11-07 | ARD-BF：spec HTML 统一放 docs/book/html/，目录与 features 同构 |
| 2026-11-07 | ARD-BG：全站一份目录；feature 页左目录右正文 |
