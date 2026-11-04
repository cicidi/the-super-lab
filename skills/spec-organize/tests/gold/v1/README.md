# Gold set v1 — iPhone purchase eval

**Requirement:** `requirement.md`  
**Simulated human:** `context.md` only (answer **「未提供」** when absent).

## Layout (test plan)

| Path | Purpose |
|---|---|
| `context-variants/` | TST-F unhappy inputs (`budget-conflict`, etc.) |
| `runs/<model>/` | TST-C outputs + `interview.md` (see `runs/README.md`, `_template/`) |
| `exemplar/` | TST-D consolidated good spec tree |
| `annotations.yaml` | GOOD/BAD labels for score 2 |

## Commands (this repo)

```bash
skills/spec-organize/tests/run_mechanical.sh
python3 tools/build_sdd_reader.py   # after approved .md changes
```

Configure models in `skills/spec-organize/tests/eval.yaml` before judge/checker runs.
