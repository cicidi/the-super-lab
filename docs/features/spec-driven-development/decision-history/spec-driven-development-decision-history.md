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

Append-only. Superseded and wrong decisions stay in the log; a decision that is
overturned gets a new numbered entry that supersedes it, never an edit.

## Decision Log

| # | Date | Decision | Status | Supersedes |
|---|------|----------|--------|------------|
| 0001 | 2026-09-25 | Authority by concern replaces a single global source of truth | accepted | — |
| 0002 | 2026-09-25 | The standard lives in `doc-organize`, not a new skill | accepted | — |
| 0003 | 2026-09-25 | Detail is carried in sibling files, not inline in `SKILL.md` | accepted | — |
| 0004 | 2026-09-25 | The health field is named `health`, not `status` | accepted | — |
| 0005 | 2026-09-25 | `spec` and `impl-plan` cap at 1,000 lines; `decision-history` is exempt | accepted | — |
| 0006 | 2026-09-25 | A feature folder may hold more than one `spec` or `impl-plan` | accepted | — |
| 0007 | 2026-09-25 | Spec parts take an aspect noun, plan parts take a number plus phase | accepted | — |
| 0008 | 2026-09-25 | Four content priority levels; L1 is never deleted | accepted | — |
| 0009 | 2026-09-25 | This feature carries two `spec` documents, against the one-per-type rule | accepted | — |

## Evidence Appendix

### 0001 — Authority by concern replaces a single global source of truth

Status: accepted

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

### 0002 — The standard lives in `doc-organize`, not a new skill

Status: accepted

Placement, linting, and consolidation already belong to `doc-organize`, and its
Sync mode is where drift is detected. A separate skill would have to duplicate
the document standard to know what a spec is.

Considered and rejected: a new `spec-driven-development` skill with
`doc-organize` keeping only a pointer. Rejected because the two would share the
type list, the frontmatter contract, and the required sections, and the copy
would drift.

### 0003 — Detail is carried in sibling files, not inline in `SKILL.md`

Status: accepted

The material is seventeen sections. Inline it would have taken `SKILL.md` past
700 lines, and a skill that must be read in one pass cannot afford that.

Follows the existing pattern: `domain-modeling/ADR-FORMAT.md` and
`domain-modeling/CONTEXT-FORMAT.md`. Sibling files travel with the directory, so
the skill stays portable — it must not point at this repository's `docs/`, which
does not exist in the projects the skill is deployed to.

### 0004 — The health field is named `health`, not `status`

Status: accepted

`state` already tracks the authoring state (`draft` or `final`). A second field
named `status` would be read as the same concept, and it accepted an overlapping
vocabulary (`draft`, `active`, `stale`, `deprecated`) that made the overlap
worse.

Considered and rejected: replacing `state`'s vocabulary with
`draft | active | stale | deprecated`. Rejected because it would invalidate every
existing document to gain a distinction that a second field provides for free.

### 0005 — `spec` and `impl-plan` cap at 1,000 lines; `decision-history` is exempt

Status: accepted

The earlier guideline said feature specs run 500-1,500 lines, which contradicts a
1,000-line ceiling. The ceiling wins; the guideline is removed.

`decision-history` is exempt because it is append-only history. Trimming it would
destroy the record that is its entire purpose. Exempting it also means the cap
never creates pressure to delete a superseded decision.

### 0006 — A feature folder may hold more than one `spec` or `impl-plan`

Status: accepted

Supersedes the earlier rule "one file per type per feature" for these two types
only, and removes the anti-pattern that forbade a second spec file.

`prd`, `test-plan`, `decision-history`, and `how-to` stay single-file: none of
them grows without bound. `spec` and `impl-plan` do, and capping them at 1,000
lines without allowing a second file would have made the cap unmeetable.

### 0007 — Spec parts take an aspect noun, plan parts take a number plus phase

Status: accepted

```
payment-spec-authorization.md        aspect noun, unordered
payment-impl-plan-01-schema.md       number plus phase, ordered
```

Considered and rejected: numbering both (`payment-spec-01.md`). A number says
nothing about the contents, and inserting a part forces a renumber across the
set. A plan is genuinely ordered, so a number carries meaning there; a spec is
cut by bounded context, so a noun carries meaning there.

### 0008 — Four content priority levels; L1 is never deleted

Status: accepted

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

### 0009 — This feature carries two `spec` documents

Status: accepted

Deliberate exception to decision 0006's one-`spec`-per-feature default, recorded
here because the rule requires a logged reason rather than a silent breach.

This feature is named for the standard itself, so the standard's own spec belongs
to it. `wayfinder-import-spec.md` already occupied
`spec-driven-development/spec/`, and the wayfinder import is a distinct effort
with its own lifecycle.

Considered and rejected:

- *Rename the feature* — rejected because the initiative name is established in
  the project's working context.
- *Put the standard's spec in its own feature* — rejected because the standard
  and the import are the same initiative; splitting them into two features would
  misrepresent the work.
- *Fold the standard into `wayfinder-import-spec.md`* — rejected as a
  restatement: two unrelated documents in one file.

The two files are distinguished by name, following decision 0007's aspect rule:
`spec-driven-development-spec.md` for the standard, `wayfinder-import-spec.md`
for the import.

## Change Log

| Date | Change |
|------|--------|
| 2026-09-25 | Initial creation; records the SDD standard's adoption and the two-spec exception |
