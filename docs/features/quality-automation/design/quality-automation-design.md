---
feature: quality-automation
type: design
state: draft
final_date: 2026-11-04
health: active
owner: cicidi
last_verified: 2026-11-04
---

# Quality Automation Skills — Design

## Problem Statement

Specs and code drift without automated review and tests.

## Solution

Skill trio plus deterministic markdown linters (frontmatter, sections, IDs, size).

## Design

### DSGN-A — spec checks

`tools/run_spec_checks.py` loads checks from `skills/spec-organize/tests/checks/`.

### DSGN-B — Human+agent review

spec-review before marking docs `final`; auto-tdd during implement phase.

## Out of Scope

Full mkdocs build in check runner

## Change Log

| Version | Date | Description |
|---|---|---|
| 0.1 | 2026-11-04 | Initial design |
