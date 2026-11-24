---
feature: downstream-delivery
type: test-plan
state: draft
final_date: 2026-11-04
health: active
owner: cicidi
last_verified: 2026-11-04
---

# Downstream Delivery — Test Plan

## Test Cases

| ID | Case | Oracle |
|---|---|---|
| **TST-A** | spec-write output after spec-ingest passes spec-organize lint | run_spec_checks on sample |
| **TST-B** | implement skill references verification-before-completion | SKILL.md |
| **TST-C** | spec-ticket opens one ticket per IMPL | `tools/check_spec_ticket_fixture.py` |

## Test Execution Order

1. Lint generated specs in fixture repo  
2. Pipeline integration doc review  

## Expected Pass Threshold

New specs from spec-write meet SPEC-STANDARD frontmatter + Change Log.

## Change Log

| Version | Date | Description |
|---|---|---|
| 0.1 | 2026-11-04 | Initial |
| 0.2 | 2026-11-24 | TST-A, TST-C name spec-write, spec-ticket |
