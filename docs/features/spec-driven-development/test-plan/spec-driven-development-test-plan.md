---
feature: spec-driven-development
type: test-plan
state: draft
final_date: 2026-11-03
health: active
owner: cicidi
last_verified: 2026-11-03
---

# Spec-Driven Development — Test Plan

Initiative 级 test plan。**被测对象** = **spec-organize**（主）、**spec-review**、**spec-write**（write 由 organize 覆盖）；**spec-pipeline** 编排 **Out of scope** 本 harness（见 pipeline design / TST-J 可选矩阵）。**Oracle** = `skills/spec-organize/SPEC-STANDARD.md`（自 document-standard design）。Sub-feature 不另写 test-plan。

## Test Scope

**In scope：** 上列三 skill 在「装进任意项目」场景下的行为；输入三类——本 repo `docs/features/`、外部 repo（`eval.yaml` 指定路径）、人工 fixture。**Out of scope：** skill 正文改动（本 plan 只定义测什么）；设计合理性；merge 策略；**spec-pipeline** 阶段编排（除 TST-J 配置矩阵）。

**Parent vs sub（spec-review）：** 审 **parent**（`docs/features/spec-driven-development/` 根，不含 `features/<sub>/`）时须核对五篇均在：`prd`、`design`、`decision-history`、`impl-plan`、`test-plan`（见 parent HLD §8）。**Sub-feature** 不要求齐全，只审已有文件。

| 术语 | 含义 |
|---|---|
| **requirement** | 固定需求：「给我推荐一个 iPhone 并帮我购买」 |
| **context 包** | 模拟「人」的唯一答题来源；AI 反问时只从此取答案 |
| **gold set** | 模范 spec（`exemplar/`）+ good/bad 标注（`annotations.yaml`），带 **版本** |
| **judge** | 单一固定模型（`eval.yaml`），逐条 MUST / 对标打分 |
| **checker** | 3 个不同模型，读 HTML 报告 + diff，只做最终 PASS/FAIL |
| **eval 配置** | `skills/spec-organize/tests/eval.yaml`；**基线** = 只装 spec-organize + 裸模型，`grill.skills: []` |

## Test Assets

| 路径 | 内容 |
|---|---|
| `skills/spec-organize/tests/eval.yaml` | `judge.model`；`gold.version`；`gold.models`（3 provider）；`grill.skills`（基线 `[]`）；`target.repo`；`target.feature: iphone-purchase`；`checkers.models`（3） |
| `skills/spec-organize/tests/checks/` | Python：`paths` `size` `frontmatter` `sections` `ids` `decision_log` `change_log` `index_book` `collision` `no_commit` |
| `skills/spec-organize/tests/fixtures/neg/<check>/` | 每检查 ≥1 最小违规树 |
| `skills/spec-organize/tests/fixtures/pos/` | 不得误报：ID 缺口、豁免路径、raw 无 frontmatter |
| `skills/spec-organize/tests/must_registry.yaml` | 每条 MUST：`id`（`MUST-{字母}`）、`source`、`text`、`method`（`python` \| `llm`）、`check` |
| `skills/spec-organize/tests/gold/v1/` | `requirement.md`、`context.md`、`context-variants/<slug>.md`、`runs/<model>/`（产出 + `interview.md`）、`exemplar/`、`annotations.yaml` |
| `skills/spec-organize/tests/gold/v1/annotations.yaml` | `GOOD-*` / `BAD-*`；`where`、`text`；BAD 含 `expected_fix`；`added_in`（gold 版本） |
| `skills/spec-organize/tests/reports/<run_id>.html` | 单 HTML；`run_id = <YYYY-MM-DD>-<branch>` |
| `skills/spec-review/tests/cases/<slug>/` | `input/`（植入缺陷）、`expected.yaml`（应检出 id、应忽略 severity 1–2） |

**分支：** 产出在 `target.repo` 开 `eval/<gold-version>/<run_id>`，**不开 PR**；gold 目录可 push 进 the-super-lab。跨 skill 检查器、gold、报告均在 **spec-organize** 下。

## Scoring

**分数 1 — MUST 合规：** `x / total`，`total` = `must_registry.yaml` 条目数；`method: python` → 检查器；`method: llm` → `judge.model`；逐条 pass/fail。

**分数 2 — 对标 gold：** 对 `annotations.yaml` 每条——GOOD 相似命中 +1、未命中 0；BAD 未犯 0、相似犯 −1（judge 判相似）。`(Σ加分 − Σ减分) × 10 / annotations 条目总数`，满分 10，可为负；**仅同一 `gold.version` 内比较**。

**门槛：** 分数 1 = `total/total`；分数 2 ≥ 同 gold 版本**上一次** run。Checker：3 模型读报告，**不得推翻** python 项；**3/3** PASS。

**Gold 增长：** run 中发现新 good/bad → 追加 `annotations.yaml`，`gold.version` +1，`added_in` 标版本；报告须标 gold 版本。

## Test Cases

### TST-A — MUST registry 构建

**目标：** 扫描 document-standard design、pipeline design、parent HLD §4–§5 全部 MUST/禁止/必须 → `must_registry.yaml`；spec 定稿后重扫。**输入：** 三篇 design。**断言：** 覆盖率 100%；每条标 `python` 或 `llm`。**判定：** 锚点比对脚本。

### TST-B — 机械检查器 + 负向 fixture

**目标：** 检查器有效。**输入：** `fixtures/neg/*`、`fixtures/pos/*`。**断言：** neg 必 fail；pos 必 pass。**判定：** pytest。

### TST-C — Gold 生成（3 模型）

**目标：** 基线下 3 套 iPhone feature spec。**输入：** `requirement.md` + `context.md`；`grill.skills: []`；只装 spec-organize。**断言：** 每套含 prd/design/decision-history/impl-plan/test-plan；`interview.md` 中模拟人回答均出自 context 或「未提供」。**判定：** Python（文件）+ judge（出处）。

### TST-D — Gold 提炼

**目标：** 3 套 → `exemplar/` + `annotations.yaml` v1。**输入：** TST-C 产出。**断言：** exemplar 过 TST-B、分数 1 全过；annotation 有 `where`/`text`；BAD 有 `expected_fix`。**判定：** Python + 人工认可（Change Log 记录）。

### TST-E — spec-organize happy path

**目标：** 改 skill 后同需求重跑。**输入：** 同 TST-C。**断言：** 分数 1 全过；分数 2 不退步。**判定：** Python + judge。

### TST-F — spec-organize unhappy（输入侧）

**目标：** context 带坑时不自猜。**输入：** `context-variants/`：`budget-conflict`、`family-disagree`、`missing-info`、`midway-change`。**断言：** 须 report/ask；budget/family 不得选一侧；midway-change 须新 ARD + strike+link；missing-info 不得编造。**判定：** judge + Python（ARD 结构）。

### TST-G — 真实树 Lint

**目标：** 别人写的 spec 是否合规。**输入：** 本 repo `docs/features/`；外部 repo 路径。**断言：** spec-organize Lint 与 `checks/` 一致；豁免不报。**判定：** Python 对比。

### TST-H — spec-review 检出率

**目标：** 找全缺陷、不误报。**输入：** exemplar 植入全部 BAD；每条 MUST 一违规样本；干净 exemplar。**断言：** 植入项均检出并引用 DSGN/MUST id；干净零 3+ 发现；1–2 不进讨论。**判定：** id 集合比对。

### TST-I — spec-review 建议质量

**目标：** 修改建议正确。**输入：** TST-H 检出项。**断言：** 建议 vs `expected_fix`：照改后缺陷消除且无新 MUST 违规。**判定：** judge；报 `x / 检出数`。

### TST-J — Eval 配置矩阵

**目标：** 不同 grill 组合。**输入：** `grill.skills`: `[]`、`[wayfinder]`、`[grill-with-docs]`、两者。**断言：** 每配置一份报告；基线先跑；只报分不设门槛。**判定：** 同 TST-E。

### TST-K — 报告

**目标：** 单 HTML。**输入：** 任一 run。**断言：** run_id、分支、gold 版本、eval 配置、分数 1 逐条（python/llm）、分数 2 ±、TST-F 变体、3 checker。**判定：** 生成 + schema。

### TST-L — 3 checker 裁决

**目标：** 最终 PASS/FAIL。**输入：** HTML + diff。**断言：** 3/3；不推翻 python。**判定：** 3 模型。

### TST-M — 变更联动

**目标：** 标准或 gold 变更后测试同步。**输入：** 改 SPEC-STANDARD / design；或 run 中新 good/bad。**断言：** design 改 → TST-A + registry/fixtures 同批；新标注 → gold.version +1。**判定：** 流程 + 覆盖率。

### TST-N — Parent 齐备 / sub 豁免

**目标：** parent 五篇齐全；sub 不因缺篇 fail。**输入：** SDD parent 根 + `features/pipeline/`、`features/document-standard/`。**断言：** parent 缺任一篇 → spec-review ≥3；sub 仅 design 等仍 pass。**判定：** Python（路径）+ spec-review 报告。

## Test Execution Order

1. **TST-A**（registry 不足 100% 则停）
2. **TST-B**（检查器失效则停）
3. **TST-C** → **TST-D**（首次或 gold 升版）
4. **TST-G**、**TST-N**
5. **TST-E**、**TST-F**
6. **TST-H** → **TST-I**
7. **TST-K** → **TST-L**
8. **TST-J**（可选）
9. 改动 → **TST-M** → 1

## Expected Pass Threshold

| Gate | 条件 |
|---|---|
| 测试框架可用 | TST-A 100%；TST-B 全过 |
| Gold v1 冻结 | TST-D：exemplar 分数 1 全过；annotations 人工认可 |
| spec-organize 可发布 | TST-E 分数 1 全过、分数 2 不退步；TST-F 四变体全过；TST-G 零差异；TST-L 3/3 |
| spec-review 可发布 | TST-H 检出 100%、误报 0；TST-I ≥ 上一次；TST-L 3/3 |
| Gold 升版 | TST-M 追加后重跑 TST-E/H 建新基线 |

## Change Log

| Date | Change |
|------|--------|
| 2026-11-03 | Initiative harness only；Phase 1 测例在 document-standard test-plan |
| 2026-11-03 | document-standard 改回 feature 级 test plan |
| 2026-11-03 | 重写为 initiative 级：被测 = spec-organize / spec-review；两分制；gold 版本化；资产在 skills/<skill>/tests |
| 2026-11-03 | 移除 wayfinder-import 例外与 out-of-scope 项 |
| 2026-11-03 | §8 对齐：parent 五篇齐备（TST-N）；sub 豁免 |
| 2026-11-04 | 被测三 skill + spec-pipeline 编排 out of scope（HLD §7） |
