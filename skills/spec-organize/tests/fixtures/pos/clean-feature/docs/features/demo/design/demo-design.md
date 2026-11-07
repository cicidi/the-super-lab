---
feature: demo
type: design
state: draft
---

# Demo Design

## Problem Statement

The demo needs one decision and one observable outcome.

## Solution

A single command that runs the thing and prints the result.

## User Stories

- As a user, I get one line of output.

## Design

| Concern | Choice |
|---|---|
| Input | one argument |
| Output | one line |

## Implementation Decisions

- One command, no subcommands.

## Testing Decisions

- TST-A and TST-B in the test plan.

## Out of Scope

- Anything not listed above.

## Further Notes

- None.

## Alternatives Considered

- Two commands instead of one → rejected: extra step for no gain.

## Drawbacks

- One command hides its steps from the user.

## Risks and Mitigations

- Risk: an argument is mistyped → validate and fail loudly.

## Open Questions

- Whether to add a `--quiet` flag.

## Reversibility

- The command can be removed without data migration.

## Change Log

| Date | Change |
|------|--------|
| 2026-11-05 | Initial |
