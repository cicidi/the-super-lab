# Expected routing — fixture-notes.md

Run: `/spec-ingest skills/spec-ingest/tests/fixture-notes.md https://example.com/shed-rules`
Stop before the spec-write hand-off (step 7). Target feature for every item: `backyard-shed`
(proposed working name; no such `docs/features/` directory exists).

## Expected items

| Item | Fixture line | Doc type | Source | Notes |
|---|---|---|---|---|
| E-1 | L5 占地不超过 10 平方米 | prd | 用户 2026-11-20 | requirement |
| E-2 | L6 选木结构，因为便宜能加工 | decision-history | 用户 2026-11-20 | decision with reason |
| E-3 | L7 屋顶用沥青瓦 | decision-history | 用户 2026-11-21 | decision, reason UNKNOWN |
| E-4 | L8 门向外开，宽 90 厘米，带锁 | design | 用户 2026-11-21 | behavior |
| E-5 | L9 先打地基，干透后立墙架 | impl-plan | 用户 2026-11-21 | step with dependency |
| E-6 | L10 浇水后地面干燥 | test-plan | 用户 2026-11-22 | test case |
| E-7 | L11 工具要能锁起来 | prd | 用户 2026-11-22 | split part 1: requirement |
| E-8 | L11 因为邻居小孩常来 | decision-history | 用户 2026-11-22 | split part 2: reason |
| E-9 | L12 要不要接电 | design (QUES) | fixture L12 | open question |
| E-10 | L13 离围栏至少 1.5 米 | prd (待定 allowed) | **UNKNOWN** | unsourced claim |

Rejected inputs: the URL (v1 does not read URLs).

## Scoring

- Agreement = items whose doc type and target feature match ÷ 10. A `待定` row counts as a match
  (it is not wrong). Pass: ≥ 90%.
- Hard rules (any failure = fail):
  1. E-10's source is `UNKNOWN` (location may be appended).
  2. E-3's reason is `UNKNOWN`.
  3. The URL is listed under Rejected inputs.
  4. `git status --porcelain docs/` shows no change made by the run.
  5. The run stops before invoking spec-write (dry run).
- E-7/E-8 may be one row only if the reason is still recorded; if not split, count E-8 as a miss.
