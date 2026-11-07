---
feature: discovery-research
type: test-plan
state: draft
final_date: 2026-11-04
health: active
owner: cicidi
last_verified: 2026-11-04
---

# Discovery & Research — Test Plan

## Test Cases

| ID | Case | Oracle |
|---|---|---|
| **TST-A** | Each SKILL.md has valid frontmatter | manual lint |
| **TST-B** | spec-organize gold eval (iPhone) for grill/organize | `skills/spec-organize/tests/` |
| **TST-C** | wayfinder triggers documented | SKILL.md metadata |

## Test Execution Order

1. Static SKILL.md review  
2. Gold eval when changing organize skill  

## Expected Pass Threshold

Skills deploy to walter-worker install paths; gold eval unchanged unless intentional.

## Change Log

| Version | Date | Description |
|---|---|---|
| 0.1 | 2026-11-04 | Initial |
