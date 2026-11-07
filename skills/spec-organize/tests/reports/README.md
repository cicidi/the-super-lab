# Eval reports (TST-K)

Write HTML reports here as `reports/<run_id>.html` where `run_id = <YYYY-MM-DD>-<branch>`.

Reports must include: gold version, eval config snapshot, score 1 line items, score 2 delta, checker verdicts (TST-L).

Schema: **`REPORT-SCHEMA.md`**. Template: `tools/eval_report_template.html`. Gate: `python3 tools/check_eval_reports.py`.
