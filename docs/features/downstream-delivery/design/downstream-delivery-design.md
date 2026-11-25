---
feature: downstream-delivery
type: design
state: draft
final_date: 2026-11-04
health: active
owner: cicidi
last_verified: 2026-11-04
---

# Delivery Pipeline Skills — Design

## Problem Statement

Specs without delivery skills stall at markdown.

## Solution

Skills orchestrate spec-write → tickets → code changes with verification-before-completion.

## User Stories

See `## User Stories` in the [PRD](../prd/downstream-delivery-prd.md).

## Implementation Decisions

See `## Design` below: DSGN-A fixes the skill chain and DSGN-B points to the phase gates.

## Design

### DSGN-A — Chain

The spec-pipeline Downstream phase runs spec-ingest, then spec-write, then spec-review, then spec-ticket, then implement (skill-factory spec-ingest ARD-E, spec-ticket ARD-H).

### DSGN-B — Integration

See `skills/spec-pipeline/INTEGRATIONS.md` for phase gates.

## Testing Decisions

See `## Test Cases` in the [test plan](../test-plan/downstream-delivery-test-plan.md).

## Out of Scope

CI deploy automation

## Further Notes

Not applicable: this feature's docs record no further notes.

## Alternatives Considered

UNKNOWN: this feature's docs record no rejected options.

## Drawbacks

UNKNOWN: this feature's docs record no drawbacks of the chosen design.

## Risks and Mitigations

UNKNOWN: this feature's docs record no risks or mitigations.

## Open Questions

| ID | Question | Answer so far | Owner | Blocking |
|---|---|---|---|---|

No open questions are recorded for this feature.

## Reversibility

UNKNOWN: this feature's docs record no undo or rollback path.

## Change Log

| Version | Date | Description |
|---|---|---|
| 0.1 | 2026-11-04 | Initial design |
| 0.2 | 2026-11-24 | DSGN-A chain names spec-ingest, spec-ticket |
| 0.3 | 2026-11-24 | Added the standard's required sections (pointers only, no new facts) |
