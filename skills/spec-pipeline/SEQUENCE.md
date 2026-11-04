# spec-pipeline — sequence diagrams

Operational view of **PIPE-*** flows. Normative rules stay in `pipeline-design.md`; routing in **`INTEGRATIONS.md`**. Sample Mermaid for `.md`/reader: `skills/spec-html-standard/MERMAID-PATTERNS.md`.

## Phase loop (Create → Downstream)

```mermaid
sequenceDiagram
    participant U as Human
    participant P as spec-pipeline
    participant W as spec-write
    participant O as spec-organize
    participant R as spec-review

    U->>P: start / continue feature
    P->>P: read CLAUDE.local or state-*.md
    alt Create
        P->>U: feature create / rough PRD
    else Map
        P->>U: interview splits / unknowns
        opt pluggable map skill
            P->>U: wayfinder / grill (optional)
        end
    else Converge
        loop PRD ↔ design ↔ decision-history
            P->>W: prose edits
            P->>O: paths / lint / INDEX
        end
    else Downstream
        par impl-plan
            P->>W: impl-plan from design
        and test-plan
            P->>W: test-plan from design
        end
    end
    P->>U: prompt spec-review before commit?
    opt user agrees
        P->>R: mechanical + semantic review
    end
```

## Mechanical lint before review

```mermaid
sequenceDiagram
    participant P as spec-pipeline
    participant L as run_spec_checks.py
    participant C as TST-B checkers
    participant R as spec-review

    P->>L: docs/features/<f>/
    L->>C: per-file + tree (collision, INDEX, no_commit)
    C-->>L: findings (check id + path)
    L-->>P: exit 0 | nonzero
    P->>R: cite findings; suggest only
```

## Human-readable reader (derived HTML)

```mermaid
sequenceDiagram
    participant U as Human
    participant P as spec-pipeline
    participant H as SPEC-HTML-STANDARD
    participant B as build_sdd_reader.py

    U->>P: reader / HTML bundle
    P->>H: layout + DSGN-N fidelity
    alt SDD parent (this repo)
        P->>B: regenerate reader.html
        B-->>P: docs/features/.../-reader.html
    else other parent
        P->>P: assemble tabs/cards from canonical .md
    end
    P->>U: open HTML (not source of truth)
    Note over P,U: spec error → ask human → fix .md → regen
```

## Gold eval prep (TST-C scaffold)

```mermaid
sequenceDiagram
    participant U as Human
    participant P as spec-pipeline
    participant O as spec-organize
    participant G as gold v1 assets

    U->>P: eval / gold iPhone scenario
    P->>G: eval_preflight + check_gold_run_scaffold
    G-->>P: TST-C-RUNBOOK.md + runs/_template
    P->>O: interview (context.md only)
    O->>G: runs/<model>/interview.md (local)
    Note over P,G: exemplar/ after TST-D; no model calls in CI
```
