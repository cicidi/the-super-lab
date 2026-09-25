---
feature: spec-driven-development
type: spec
state: final
final_date: 2026-09-25
status: active
owner: cicidi
last_verified: 2026-09-25
---

# Spec-Driven Development Standard

Defines how spec, code, tests, and machine-readable artifacts stay consistent
over time.

The normative text lives in the `doc-organize` skill so it travels with the
skill into every project. This document records the adoption and the reasoning;
it does not restate the rules.

| Topic | Authoritative file |
|---|---|
| Authority by concern, conflict handling | `skills/doc-organize/AUTHORITY-BY-CONCERN.md` |
| Spec scope, size, agent context | `skills/doc-organize/SPEC-SCOPE.md` |
| Metadata, staleness, drift, checklists | `skills/doc-organize/SPEC-HEALTH.md` |
| Enforcement modes | `skills/doc-organize/SKILL.md` |

## Problem Statement

Documentation and code drift apart because the obvious rule — "keep them in
sync" — is not actionable. It does not say which artifact wins, when a document
must change, or what to do when two artifacts disagree. The previous
`doc-organize` rule said "code is the source of truth", which silently resolves
every conflict in one direction and makes a spec unable to protect intended
behavior.

## Solution

Replace the single-source-of-truth rule with authority by concern: intended
behavior belongs to the spec, current implementation to the code, contracts to
the machine-readable artifact, database structure to migrations, and executable
verification to the tests. Synchronization becomes change-driven — a spec is
updated when intended behavior changes, not when code changes.

## User Stories

- As a developer, when code and spec disagree, I get a reported conflict with
  evidence rather than a silent rewrite in one direction.
- As an agent, I can find the authoritative artifact for a concern without
  loading the entire documentation tree.
- As a maintainer, I can tell a spec that is stale from a spec that is wrong.

## Implementation Decisions

- The rules live in `doc-organize` rather than a new skill, because placement,
  linting, and consolidation already belong there and the sync mode is where
  drift is detected.
- Detail is carried in three sibling reference files rather than inline, so
  `SKILL.md` stays loadable in one pass. This is the same pattern as
  `domain-modeling/ADR-FORMAT.md`.
- `state` keeps its `draft` / `final` vocabulary. Health is a separate optional
  `status` field, so existing documents stay valid and no migration is required.
- No rule is enforced by a timestamp edit. `last_verified` moves only when a real
  verification happened.

## Design

Four surfaces change: `## Authority by Concern` and three sibling sections are
added to `SKILL.md`; Lint gains stale-verification, excessive-implementation-
detail, and reference-drift checks; Sync resolves by concern instead of
defaulting to code; Quality Gates gain the change checklist.

## Testing Decisions

Verified by reading the modified skill end to end against the seventeen source
rules, and by confirming no remaining instance of the replaced rule
(`grep -i "code is the source of truth"` returns nothing). A full Lint run over
`docs/features/` is the follow-up check; the tree currently does not pass it —
see Further Notes.

## Out of Scope

- Migrating existing documents to the new optional metadata fields.
- Bringing `docs/features/` into compliance with the existing standard. The tree
  predates it and fails Lint on several counts.
- Automating drift detection in CI.

## Further Notes

Known non-compliance in the tree, observed while writing this document and not
addressed here:

- `docs/features/spec-driven-development/spec/wayfinder-import-spec.md` and its
  siblings do not follow `<feature>-<type>.md`.
- These documents carry only `state` and `final_date`; `feature` and `type` are
  absent, so Lint reports them.
- `docs/features/skill-factory/` has a `design/` directory, which is not one of
  the six types, and fourteen separate `decision-history` files where the
  standard allows one.
- Adding this file gives `spec-driven-development` two `spec` documents, which
  the one-file-per-type rule forbids. The exception is deliberate; the feature
  name is the standard's own name.

## Change Log

| Date | Change |
|------|--------|
| 2026-09-25 | Initial creation; records adoption of the SDD standard in `doc-organize` |
