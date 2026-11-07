# spec-pipeline — sequence (operational)

Norm: **PIPE-*** in pipeline design. Diagrams for recap / onboarding only.

## Create → Map → Converge → Downstream

```mermaid
sequenceDiagram
  participant U as Human
  participant P as spec-pipeline
  participant W as spec-write
  participant O as spec-organize
  participant R as spec-review

  U->>P: start / lost context
  P->>P: read CLAUDE.local or raw/state
  alt Create
    P->>U: confirm feature slug
    P->>O: feature create (walter-worker)
  else Map
    P->>U: interview (MUST)
    opt pluggable map
      P->>P: wayfinder / grill-with-docs
    end
    P->>U: confirm before new paths
  else Converge
    loop PRD design decision-history
      P->>W: prose edits
      W->>O: Organize after move/create
    end
  else Downstream
    par impl-plan
      P->>W: from design
    and test-plan
      P->>W: from design
    end
  end
  P->>R: ask before commit
  R->>P: findings (suggest only)
  P->>U: recap (RECAP-TEMPLATE)
```

## Mechanical lint before review

```mermaid
sequenceDiagram
  participant P as spec-pipeline
  participant T as run_spec_checks.py
  participant R as spec-review

  P->>T: docs/features/<f>/
  T->>T: per-file + tree (collision, INDEX, no_commit)
  T-->>P: findings count
  P->>R: include mechanical ids in review
```

## HTML reader (derived)

```mermaid
sequenceDiagram
  participant P as spec-pipeline
  participant H as SPEC-HTML-STANDARD
  participant B as build_sdd_reader.py

  P->>H: fidelity rules (DSGN-N)
  P->>B: regen SDD parent bundle
  B-->>P: *-reader.html (not source of truth)
```

See **INTEGRATIONS.md** for skill routing table.
