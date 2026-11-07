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

## Design

### DSGN-A — Chain

spec-pipeline Downstream phase → to-spec → to-tickets → implement.

### DSGN-B — Integration

See `skills/spec-pipeline/INTEGRATIONS.md` for phase gates.

## Out of Scope

CI deploy automation

## Change Log

| Version | Date | Description |
|---|---|---|
| 0.1 | 2026-11-04 | Initial design |
