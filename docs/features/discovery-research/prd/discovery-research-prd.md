---
feature: discovery-research
type: prd
state: draft
final_date: 2026-11-04
health: active
owner: cicidi
last_verified: 2026-11-04
---

# Discovery & Research Skills — PRD

## Overview

Completed agent skills in `skills/`: **wayfinder**, **research**, **grill-with-docs**, **domain-modeling** — problem framing before specs.

## Goals and Success Metrics

| Goal | Metric |
|---|---|
| **PRD-A** | Each skill has SKILL.md with triggers and workflow |
| **PRD-B** | Outputs feed SDD pipeline (spec-pipeline / to-spec) |

## User Stories

1. As a PM, I want wayfinder import, so that messy inputs become structured context.
2. As an architect, I want grill-with-docs, so that gaps surface before PRD.

## Functional Requirements

| ID | Requirement |
|---|---|
| **PRD-F1** | wayfinder: ingest + map conversation to docs |
| **PRD-F2** | research: structured external lookup |
| **PRD-F3** | grill-with-docs: interview against CONTEXT |
| **PRD-F4** | domain-modeling: glossary / CONTEXT.md |

## Non-Functional Requirements

| ID | Requirement |
|---|---|
| **PRD-N1** | Skills copy cleanly into consumer projects |

## Out of Scope

Runtime code beyond SKILL.md orchestration

## Change Log

| Version | Date | Description |
|---|---|---|
| 0.1 | 2026-11-04 | SDD feature bundle for discovery skills |
