# TST-K report schema (HTML)

Committed template: `tools/eval_report_template.html`. Generated reports live as `reports/<run_id>.html` (gitignored).

Each report must include HTML comments (one per field):

| Marker | Content |
|---|---|
| `eval-report:run_id=` | `YYYY-MM-DD-branch-slug` |
| `eval-report:branch=` | git branch name |
| `eval-report:gold_version=` | e.g. `v1` from `eval.yaml` |
| `eval-report:eval_config=` | JSON or YAML snapshot (no secrets) |
| `eval-report:score1=` | MUST registry python/llm line items |
| `eval-report:score2=` | Annotation GOOD/BAD delta |
| `eval-report:tst_f_variant=` | variant name or `baseline` |
| `eval-report:checker_verdicts=` | TST-L three-checker summary |

Validate template (and any local HTML):

```bash
python3 tools/check_eval_reports.py
```
