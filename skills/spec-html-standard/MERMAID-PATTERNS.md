# Mermaid patterns for spec reader HTML

Use in committed `.md` **fenced blocks**; `tools/build_sdd_reader.py` renders ` ```mermaid ` as diagrams (requires network for CDN in browser).

## SDD artifact loop (parent PRD)

```mermaid
flowchart LR
  PRD["PRD"] <-->|scope| DH["decision-history"]
  DH <-->|direction| D["design 篇"]
  PRD <-->|requirements| D
  D --> IMPL["impl-plan"]
  D --> TEST["test-plan"]
```

## Pipeline phases

```mermaid
flowchart LR
  C[Create] --> M[Map]
  M --> V[Converge]
  V --> P[Downstream]
  P --> I[impl-plan]
  P --> T[test-plan]
```

## Authority by concern (read-only summary)

```mermaid
flowchart TB
  subgraph authoritative
    S[design 篇 — intended behavior]
    C[contracts — OpenAPI etc.]
    CODE[code — current impl]
    X[tests — verification]
  end
```

Copy into **design** or **pipeline** prose only when user approves **spec** edits; otherwise embed in HTML reader assembly from this file.
