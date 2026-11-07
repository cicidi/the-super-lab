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

## Numbered sequence with a state note (ARD-BE)

One flow, one diagram. `autonumber` matches the heading's step range. A Note names the decision or question that blocks a step. Participants stay at or under 9.

```mermaid
sequenceDiagram
  autonumber
  participant C as Client
  participant G as Gate
  C->>G: open
  Note over G: blocked by ARD-AN until the partner delivers
  G-->>C: ready
```
