---
feature: downstream-delivery
type: prd
state: draft
final_date: 2026-11-04
health: active
owner: cicidi
last_verified: 2026-11-04
---

# Delivery Pipeline Skills — PRD

## Overview

Downstream SDD skills: **spec-ingest**, **spec-ticket**, **implement** — from converged spec to shipped code. They replace to-spec and to-tickets (skill-factory spec-ingest ARD-E, spec-ticket ARD-H).

## Goals and Success Metrics

| Goal | Metric |
|---|---|
| **PRD-A** | spec-ingest sorts input and spec-write emits docs per SPEC-STANDARD |
| **PRD-B** | implement respects impl-plan tasks |

## User Stories

1. As a developer, I want spec-ingest after design freeze, so that conclusions land in spec docs.
2. As a developer, I want spec-ticket, so that each IMPL becomes a ticket.

## Functional Requirements

| ID | Requirement |
|---|---|
| **PRD-F1** | spec-ingest sorts chat or files into doc types; spec-write writes the spec markdown |
| **PRD-F2** | spec-ticket opens one ticket per impl-plan IMPL |
| **PRD-F3** | implement executes tasks with verification skill |

## Non-Functional Requirements

| ID | Requirement |
|---|---|
| **PRD-N1** | Uses spec-write / spec-organize, not ad hoc paths |

## Out of Scope

Issue tracker vendor lock-in (local markdown default)

## Resources Needed

UNKNOWN: the docs name no resources beyond the three skills listed in `## Overview`.

## Change Log

| Version | Date | Description |
|---|---|---|
| 0.1 | 2026-11-04 | SDD delivery bundle |
| 0.2 | 2026-11-24 | to-spec, to-tickets replaced by spec-ingest, spec-ticket |
| 0.3 | 2026-11-24 | Added the standard's required sections (pointers only, no new facts) |
