---
name: spec-organize
description: |
  Not an entry skill (ARD-AJ). Standards live in SPEC-STANDARD.md and
  SPEC-PRESENTATION.md. Use spec-write to create or edit a spec. Use
  spec-review to review one. This file keeps organize modes as reference.
license: MIT
compatibility: claude-code,opencode
metadata:
  triggers:
    - organize docs
    - doc organize
    - where should this go
    - move document
    - rename document
    - merge docs
    - doc merge
    - consolidate docs
    - too many files
    - doc lint
    - check docs
    - sync docs
    - docs inconsistent
    - spec is stale
    - INDEX.md
    - feature docs
    - spec drift
    - source of truth
    - authority by concern
---

# spec-organize

**Not an entry skill (ARD-AJ).** Path, permission, scope, what to write, and evidence are in `SPEC-STANDARD.md`. Presentation is in `skills/spec-html-standard/SPEC-PRESENTATION.md`. To create or edit a spec, use **spec-write**. To review, use **spec-review**. The modes below are reference for those standards.

Lint wired in `tools/run_spec_checks.py`: Stale paired HTML, audience, Dead anchors, Unanchored code citations, Open-question tracker, Step drift, Diagram/step drift, impl-plan task lines, translation banner, resolved refs, counts. Do not number a required heading. A part file only needs a link back to the design entry.

Defines the project's documentation standard, then enforces it in four modes:
place a document, lint the tree against the standard, consolidate sprawl into one
file per type, and sync documents with each other and with the code.

## When to Use

- Creating a document and unsure where it belongs or what to call it
- A docs tree has grown files that do not match the standard
- Too many files were committed while writing a spec
- Documents disagree with each other on tone or on a decision
- A spec looks stale relative to the code it describes
- Regenerating or repairing INDEX.md

## When NOT to Use

- Writing document content — write it, then use Organize mode for placement
- Reviewing whether a design is sound — use spec-review
- Resolving git merge conflicts in code — use git, not this skill
- Deciding which of two conflicting decisions is correct — this skill reports
  the conflict, a human rules on it

## Example Domains

Illustrations, not gold. Gold lives outside this repo.

- **盖 shed**: the permit limit is `PRD-A` in `docs/features/garden-shed/prd/garden-shed-prd.md`. The build sequence is `design/`, not a second prd.
- **北京旅游**: the budget cap is a PRD requirement. The day-by-day route is `design/`. An undecided hotel stays in design `Open Questions`.
- **数学题**: the definition being learned is `prd`. The step order is `design/`. A lemma with no source is `UNKNOWN`, not a guessed proof.
- **股票**: the claim under analysis is `prd`. The filing URL or `raw/` note is evidence on `design/`. A missing 10-K is `UNKNOWN`.

## Authority by Concern

No single artifact is the source of truth for everything. Each concern has one
authoritative artifact:

| Concern | Authoritative artifact |
|---|---|
| Intended behavior | the feature's `design` |
| API contract | OpenAPI, protobuf, GraphQL, JSON Schema, event schema, AsyncAPI |
| Database structure | migrations and schema definitions |
| Current implementation | the code |
| Executable verification | the tests |

A spec is authoritative for what the system SHOULD do. Code is authoritative for
what the system CURRENTLY does. A disagreement is never resolved by assuming
`spec > code` or `code > spec` — establish the intended behavior first, and ask
when it cannot be established.

## Spec Scope and Size

A healthy spec is not a complete description of the code. It describes behavior,
contracts, invariants, constraints, error semantics, state transitions, and
architecture boundaries — not class hierarchies, private methods, or internal
algorithms. If the implementation can change while externally observable
behavior does not, the spec should not change.

A `design` or `impl-plan` must stay under 1,000 lines. `decision-history` is exempt
— it is append-only history, and history is never trimmed. Split on bounded
context, domain, ownership, or lifecycle boundaries, never on a line count.

## Content Priority

Content sits at one of four levels, and the level decides what happens when a
document has to shrink:

| Level | Holds | On trim |
|---|---|---|
| L1 Decisive | Behavior, contracts, invariants, constraints, error semantics, security rules, architecture boundaries, out-of-scope, assumptions, compatibility constraints | Never deleted |
| L2 Rationale | Why this design, with evidence | Compressed |
| L3 Alternatives | Why not the other approach | Deleted |
| L4 Support | References, research, examples, raw output, links to facts owned elsewhere | Deleted first |

A fact whose authoritative home is another document is a link, never a
restatement — that copy is L4. Trim L4, then L3, then compress L2. If the
document is still over 1,000 lines, split it. Deleting L1 to fit the cap is a
defect, not an optimization. See `CONTENT-PRIORITY.md`.

## Spec Health

A `final` document is maintained rather than rewritten. An important spec may
carry `health` (`active` | `stale` | `deprecated`), `owner`, and `last_verified`.
`stale` means not recently verified, not wrong. Health tracks `last_verified`,
not `last_updated`.

## Change-Driven Sync

Sync on change of behavior, not on change of code:

```
Behavior changed -> identify the relevant spec -> review it ->
update it if intended behavior changed -> update code -> update tests -> verify
```

Refactoring, renaming, internal optimization, class restructuring, framework
migration, and swapping an implementation detail do not change the spec. Update
the spec because intended behavior changed, not merely because code changed.

## Reference Files

Sibling files in this skill's directory, loaded on demand:

| File | Read when |
|---|---|
| `AUTHORITY-BY-CONCERN.md` | Deciding which artifact owns a fact, or resolving a spec/code conflict |
| `SPEC-SCOPE.md` | Writing a spec, or deciding whether something belongs in one |
| `SPEC-HEALTH.md` | Auditing spec health, staleness, or drift |
| `CONTENT-PRIORITY.md` | Trimming or splitting a spec, or classifying a piece of content |
| `NAMING.md` | Placing, naming, or splitting a document, or resolving a name collision |

## The Standard

### Document types

Six committed types, one local type. Every document belongs to exactly one.

| Type | Holds | Committed |
|---|---|---|
| `prd` | What to build and why — product-level requirements | yes |
| `design` | How it is built — technical detail, interfaces, design decisions | yes |
| `impl-plan` | Tasks with dependencies and an execution order: what blocks what, what to do first | yes |
| `test-plan` | How the implementation is verified | yes |
| `decision-history` | Every decision ever made for the feature, in order | yes |
| `how-to` | Operational instructions for using the result | yes |
| `state` | Working progress, for compaction recovery | no — gitignored |

Architecture and design content belongs in a `## Design` section of `design`, not
in a separate `design` type. External material that a document cites belongs
beside that document, not in a separate `reference` type.

### Exempt from the standard

The standard governs documents under `docs/features/`. These are not typed
documents and carry no frontmatter, type, or Change Log:

| Path | Why exempt |
|---|---|
| `docs/INDEX.md` | Generated index, rewritten wholesale each time |
| `docs/book/**` | Assembled output, built from documents that are already `final` |
| `CONTEXT.md` | Domain glossary, owned by domain-modeling |
| `README.md` | Repository orientation, not a feature document |

Lint reports these only if their links break or they list a file that no longer
exists. Do not add frontmatter to them.

### Path and naming

```
docs/features/<feature>/<type>/<feature>-<type>.md
```

One file per type per feature by default. `prd`, `test-plan`, `decision-history`,
and `how-to` stay single-file. `design` and `impl-plan` may be split, because they
are the two types that grow without bound.

- `<feature>` is kebab-case, lowercase, no spaces or special characters
- The filename repeats the feature and the type, so a file is identifiable
  outside its directory
- A supporting file that a document cites sits in that document's folder:
  `docs/features/<feature>/design/<source-name>.md`
- A feature has at most one `decision-history`, and it is exempt from the
  1,000-line cap: it is append-only history, and history is never trimmed

### Splitting and collisions

Split parts take an aspect noun for `design` (`payment-design-authorization.md`) and
a zero-padded sequence plus a phase name for `impl-plan`
(`payment-impl-plan-01-schema.md`). Check every new feature and file name against
what already exists before creating it, and log a rename rather than performing
it silently.

See `NAMING.md` for the boundary rules, the collision signals, and how to resolve
each case.

### Frontmatter

Every document carries these four fields:

```yaml
---
feature: <feature-name>
type: prd | design | impl-plan | test-plan | decision-history | how-to
state: draft | final
final_date: YYYY-MM-DD
---
```

`final_date` is required when `state` is `final`. A document becomes `final` when
its content is settled; after that it is maintained rather than rewritten, and
authority follows the concern table above rather than defaulting to the code.

An important spec may additionally carry `spec_id`, `version`, `health`, `owner`,
and `last_verified`. All five are optional — see `SPEC-HEALTH.md`. `health` is
deliberately not called `status`: `state` already tracks the authoring state
(`draft` or `final`), and two fields named for "state" invite confusion.

### Required sections

Each type has a fixed section set. Sections may be added, never renamed or
dropped.

| Type | Required sections |
|---|---|
| `prd` | Overview, Goals and Success Metrics, User Stories, Functional Requirements, Out of Scope, Resources Needed |
| `design` | Problem Statement, Solution, User Stories, Implementation Decisions, Design, Testing Decisions, Out of Scope, Further Notes, Alternatives Considered, Drawbacks, Risks and Mitigations, Open Questions, Reversibility |
| `impl-plan` | Global Constraints, Acceptance Criteria |
| `test-plan` | Test Cases, Test Execution Order, Expected Pass Threshold |
| `decision-history` | Decision Log, Evidence Appendix |
| `how-to` | Overview, Prerequisites, Steps, Verification |

`prd` carries product intent. `design` carries technical intent.
`Implementation Decisions` records architecture-level choices and their
rationale — not class structure, private methods, or internal algorithms. See
`SPEC-SCOPE.md`.

On `design`, `Alternatives Considered` lists rejected approaches and why each
lost. `Drawbacks` is what is bad about the chosen design. `Risks and
Mitigations` is what can go wrong in use. `Open Questions` lists unresolved
items with an owner. `Reversibility` covers undo, return, and rollback.

### Decision history

The `decision-history` file is a tracking history, not a curated summary. It
keeps every decision ever made for the feature, including ones later superseded
and ones that turned out wrong. Nothing is deleted.

The Decision Log is a table, newest first:

```markdown
| ID | Date | Decision |
|----|------|----------|
| ARD-B | 2026-07-22 | Store state per feature, not per project |
| ARD-A | 2026-07-14 | Adopt kebab-case for feature directories |
```

A superseded decision stays in the log and keeps its evidence entry: strike the
old row and link the entry that replaces it. There is no Status or Supersedes
column, no bare numeric id, and an id is never reused.

The Evidence Appendix holds one numbered entry per decision, preserving the
original rationale and supporting content:

```markdown
### ARD-A — Adopt kebab-case for feature directories

Rationale as originally recorded, including any alternatives that were
considered and why they were rejected. Support content belongs here: benchmark
output, links to the discussion that produced the decision, quoted constraints.
```

### Change Log

Every document ends with a Change Log, as its final section. It is appended to,
never prepended, and existing entries are never removed.

```markdown
## Change Log

| Date | Change |
|------|--------|
| 2026-08-02 | Initial creation |
| 2026-08-14 | Moved from docs/initiatives/ to docs/features/ |
```

### Scratch — not committed

Research, discussion, and adversarial-review artifacts are working material, not
documents. They live under the feature but are gitignored and never committed:

```
docs/features/<feature>/raw/research/<topic>.md
docs/features/<feature>/raw/discussion/<topic>.md
docs/features/<feature>/raw/state/state-<YYYY-MM-DD>.md
```

`raw/**` is local only. Do not commit it. `.scratch/<feature-slug>/` holds
tickets and issues, not spec prose. Do not move `raw/` into `.scratch/`. Lint
does not report either tree.

### INDEX.md

Regenerate after every create, move, rename, or delete. Walk the docs tree and
read each file's frontmatter, first heading, and first paragraph. A file that is
not listed is an orphan; a listed file that does not exist is a dead link.

### PROTECTED blocks

Content between `<!-- PROTECTED -->` and `<!-- END PROTECTED -->` is never
modified by any mode. The `<!-- PROTECTED START -->` / `<!-- PROTECTED END -->`
spelling is also recognised, but prefer the shorter form, which is what the rest
of the tooling uses.

## Process

### Step 0: Determine the mode

Infer from what the user asked. Ask one question only when genuinely ambiguous.

| Signal | Mode |
|---|---|
| "where should this go", a new document | A — Organize |
| "check the docs", "is this valid", reviewing a file | B — Lint |
| "too many files", "merge these", "consolidate" | C — Consolidate |
| "docs disagree", "spec is stale", "out of sync" | D — Sync |

If the user asks to "review the file and fix the format", that is B — Lint.
If they ask to "review the file" meaning whether its content is any good, that
is spec-review, not this skill.

---

### Mode A: Organize

1. Identify the feature. If it is not obvious from context, ask.
2. Identify the type from the six committed types. If the content spans types —
   product intent and technical detail together — split it: intent goes to `prd`,
   technical detail to `design`.
3. Check the feature name and the intended filename against what already exists
   (`NAMING.md` lists the collision signals). Merge, rename, or confirm with the
   user before going further.
4. Compute the path: `docs/features/<feature>/<type>/<feature>-<type>.md`.
5. If that file already exists, do not create a second one — unless the type is
   `design` or `impl-plan` and the existing file is at the 1,000-line cap. Prefer
   merging into the existing file in the right section and appending a Change Log
   entry. Split only when the cap forces it, and name the parts by the rules
   above.
6. Write the frontmatter and required sections for the type.
7. Append the Change Log entry.
8. Regenerate INDEX.md.

### Mode B: Lint

Audit the docs tree against the standard. Applies mechanical fixes; reports the
rest.

**SDD harness (this repo):** `./tools/run_sdd_mechanical.sh` — lint, neg/pos fixtures, registry anchors, gold/reader smoke, spec-review cases, pytest (`skills/spec-organize/tests/README.md`). Skill map: `skills/SDD-DELIVERABLES.md`.

1. Walk `docs/features/` and collect every markdown file.
2. Check each file against the standard:
   - **Wrong root** — a doc tree under `docs/initiatives/` or `docs/<feature>/`,
     outside `docs/features/`
   - **Wrong type directory** — a committed directory other than the six types
     `prd/`, `design/`, `impl-plan/`, `test-plan/`, `decision-history/`,
     `how-to/`. Wrong examples: `plan/`, `reference/`, `mockups/`,
     `work-review/`, `issues-found/`, `devil-advocate/`. `raw/` and `.scratch/`
     are local-only; they are not wrong directories.
   - **Wrong filename** — not `<feature>-<type>.md`
   - **Missing or invalid frontmatter** — any of the four fields absent, or
     `state` outside `draft|final`, or `final` without `final_date`
   - **Missing required sections** for the type
   - **Change Log** missing, misplaced (not last), or containing a non-table
     section after it
   - **Heading skips** — an `##` under no `#`, an `####` under an `##`
   - **Dead links** — a relative link whose target does not exist
   - **Orphan or dangling INDEX.md entries**
   - **`docs/adr/`** — legacy layout; fold into the feature's `decision-history`
   - **Stale verification** — `last_verified` older than roughly 90 days; report
     only, never edit a file to move a timestamp
   - **Excessive implementation detail** — a spec describing class structure,
     private methods, or internal algorithms rather than behavior
   - **Reference drift** — a spec citing an API, component, or file that no
     longer exists; report it, do not guess the replacement
   - **Oversized document** — a `design` or `impl-plan` over 1,000 lines; report it
     for splitting. `decision-history` is exempt
   - **Name collision** — two features or two files whose names trip a collision
     signal from `NAMING.md`
   - **Restated fact** — the same fact written out in two documents; the second
     occurrence should be a link
3. Apply the mechanical fixes directly: rename to the standard filename, move to
   the standard directory, add missing frontmatter, move Change Log to the end.
4. Report what was applied and what needs a human decision — content that must be
   split across types, or a section that has no counterpart in the standard.
5. Regenerate INDEX.md.
6. Append a Change Log entry to every file touched.

### Mode C: Consolidate

Reduce many files to one per type per feature. This mode deletes and merges, so
it proposes and waits — it never applies without approval.

1. For each feature, list the files by type.
2. Identify what consolidates:
   - Multiple `prd`, `design`, `impl-plan`, `test-plan`, or `how-to` files for the
     same feature become one file per type.
   - Multiple decision records become one `decision-history`, with the Decision
     Log in chronological order and every original preserved in the Evidence
     Appendix. Nothing is dropped, including superseded and incorrect decisions.
   - Top-level `research/`, `discussion/`, and `devil-advocate/` move under
     `raw/`. Do not move `raw/` into `.scratch/`. Cite what a deleted note
     supported before removing it.
   - A `reference/` file is not a committed type. Move it next to the document
     that cites it, or under `raw/` if it must stay uncommitted.
3. Present the plan: every move, merge, and deletion, with the target of each.
4. On approval, apply it, regenerate INDEX.md, and append Change Log entries.
5. If a decision is being overwritten by consolidation, add a superseding entry
   rather than editing the original.

### Mode D: Sync

Reconcile documents with each other and with the code.

1. Read each feature's documents.
2. Check for drift within and across documents:
   - **Tone and terminology** — the same concept named differently in two places,
     or a glossary term from CONTEXT.md not used
   - **Decision conflict** — two documents asserting different decisions
   - **Spec drift** — a document and the code disagreeing about the same concern,
     or a document describing behavior the code no longer has
   - **Reference drift** — a document citing an API, component, or file that no
     longer exists
   - **Duplicated facts** — the same fact maintained by hand in two places
3. Classify each drift by the concern it touches, then resolve by authority:
   - **Change Log first.** If one document records a later change than another,
     the later one wins — a document-to-document question.
   - **Intended behavior** — the spec is authoritative. If the code contradicts
     the intended behavior, the code is what changes.
   - **Current implementation** — the code is authoritative. If the spec
     describes an implementation difference, the spec is what changes.
   - **Contract or schema** — the machine-readable artifact is authoritative.
     Never hand-edit a spec to mirror it.
   - **Report what cannot be resolved.** Which decision or which behavior is
     correct is a human decision. Detect, explain, show the evidence from both
     sides, and ask. Never silently pick one, and never rewrite the spec to match
     the code by default. See `AUTHORITY-BY-CONCERN.md`.
4. Auto-fix formatting, tone, terminology, links, and heading hierarchy directly.
5. Report every semantic conflict with the two positions and the evidence from
   each side. Do not rewrite a decision.
6. Append a Change Log entry to every file changed.

## Quality Gates

MUST:

- [ ] Every document is under `docs/features/` with a type from the six
- [ ] Filename is `<feature>-<type>.md` and matches its directory
- [ ] Frontmatter carries all four fields; `final` has `final_date`
- [ ] Required sections for the type are present and correctly named
- [ ] Change Log present, last in the file, appended to only
- [ ] PROTECTED blocks intact
- [ ] INDEX.md regenerated after any create, move, rename, or delete
- [ ] Consolidation preserved every decision, including superseded ones
- [ ] Scratch content is gitignored and not committed
- [ ] No content lost — every unique section from a merged file has a home
- [ ] Spec changes trace to a change in intended behavior, not to a code change
- [ ] Authority for each affected concern identified before resolving a conflict
- [ ] No spec/code conflict resolved silently
- [ ] No fact maintained by hand in two places
- [ ] `design` and `impl-plan` under 1,000 lines, or split on a bounded context
- [ ] Feature and file names checked for collisions before creation
- [ ] No L1 content dropped to meet the size cap

NICE:

- [ ] Heading hierarchy has no skipped levels
- [ ] All relative links resolve
- [ ] Terminology matches CONTEXT.md
- [ ] `last_verified` present and current on important specs
- [ ] Spec stays within a useful context boundary

## Anti-Patterns

- **Creating a second file for a type that already exists.** A feature has one
  `design` until it crosses the 1,000-line cap. Add to the existing file rather
  than creating `design-v2.md`, and split only on a real boundary.
- **Splitting a spec to dodge the cap without a boundary.** A split part is a
  bounded context, not a page break.
- **Numbering spec parts.** A number says nothing about the contents. Plans are
  numbered because a plan is ordered; specs are named by their aspect.
- **Deleting L1 content to fit the cap.** L1 is never deleted. Trim L4, then L3,
  and split if it is still too long.
- **Restating a fact that already has a home.** The second occurrence is a link,
  and a link is L4.
- **Letting two features carry confusable names.** Merge them, or rename both so
  each is distinguishable.
- **Deleting a superseded decision.** Superseded and wrong decisions stay in the
  log. That history is the point.
- **Committing scratch.** Research and discussion are working material. If it
  matters enough to commit, it belongs in the document it supports.
- **Silently resolving a decision conflict.** Report it and let a human rule.
- **Rewriting a `final` document.** After `final`, maintain it; authority follows
  the concern, not the code by default.
- **Consolidating without approval.** Mode C deletes files. Always propose first.
- **Treating a content review as a lint.** Judging whether a design is sound is
  spec-review, not this skill.
- **Treating code as the source of truth for everything.** Code answers what the
  system currently does. It does not answer what the system should do.
- **Treating the spec as the source of truth for everything.** A spec is not a
  description of the current implementation, and code that diverges from it is
  not automatically wrong.
- **Editing a spec to prove it is in sync.** Update the spec because intended
  behavior changed, not because code changed.
- **Maintaining the same fact in two places by hand.** Pick the authoritative
  artifact and generate or delete the copy.
- **Splitting a spec to satisfy a line count.** Split on bounded context.

## Sources

- Existing doc-organize skill: two-branch structure (organize, merge) and
  PROTECTED block handling, carried forward
- to-spec (mattpocock): the `design` required-section template, reused verbatim
- domain-modeling (mattpocock): ADR status vocabulary and evidence format
- write-doc (walter-worker): Change Log format and append-only rule
- Observed in skill-factory and wayfinder-import documents: the `prd`, `design`,
  `impl-plan`, and `test-plan` section sets
- User requirement: one file per type per feature, feature vocabulary, scratch
  gitignored, decision history kept whole, Lint applies while Consolidate
  proposes
- User requirement (2026-09-25): authority by concern in place of a single global
  source of truth, behavior described over implementation, change-driven sync,
  spec size and agent-context guidance, spec health metadata, and drift
  detection. Detail carried in `AUTHORITY-BY-CONCERN.md`, `SPEC-SCOPE.md`, and
  `SPEC-HEALTH.md` so SKILL.md stays loadable in one pass.
- User requirement (2026-09-25, second pass): four content priority levels with
  L1 undeletable, trim order L4 then L3, a hard 1,000-line cap exempting
  `decision-history`, a feature folder allowed more than one `design` or
  `impl-plan`, aspect names for spec parts and numbered phase names for plan
  parts, and a name-collision check on every placement. Detail in
  `CONTENT-PRIORITY.md`.
