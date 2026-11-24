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

The spec-pipeline Downstream phase runs spec-ingest, then spec-write, then spec-review, then spec-ticket, then implement (skill-factory spec-ingest ARD-E, spec-ticket ARD-H).

### DSGN-B — Integration

See `skills/spec-pipeline/INTEGRATIONS.md` for phase gates.

## Out of Scope

CI deploy automation

## Change Log

| Version | Date | Description |
|---|---|---|
| 0.1 | 2026-11-04 | Initial design |
| 0.2 | 2026-11-24 | DSGN-A chain names spec-ingest, spec-ticket |
