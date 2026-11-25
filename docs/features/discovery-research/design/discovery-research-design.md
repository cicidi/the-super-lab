---
feature: discovery-research
type: design
state: draft
final_date: 2026-11-04
health: active
owner: cicidi
last_verified: 2026-11-04
---

# Discovery & Research Skills — Design

## Problem Statement

Specs fail when problems and vocabulary are undefined.

## Solution

Skill bundle under `skills/{wayfinder,research,grill-with-docs,domain-modeling}/SKILL.md`.

## User Stories

See `## User Stories` in the [PRD](../prd/discovery-research-prd.md).

## Implementation Decisions

See `## Design` below: DSGN-A fixes the pipeline position and DSGN-B the pairing with spec-organize.

## Design

### DSGN-A — Pipeline position

Create / Map phases of **spec-pipeline**; outputs land in `raw/` or CONTEXT.

### DSGN-B — Dependencies

Pairs with **spec-organize** for placement after synthesis.

## Testing Decisions

See `## Test Cases` in the [test plan](../test-plan/discovery-research-test-plan.md).

## Out of Scope

Automated web crawling infrastructure

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
| 0.2 | 2026-11-24 | Added the standard's required sections (pointers only, no new facts) |
