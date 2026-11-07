---
feature: spec-driven-development
type: test-plan
state: draft
final_date: 2026-11-03
health: active
owner: cicidi
last_verified: 2026-11-04
---

# Spec-Driven Development — Test Plan

Initiative 级 test plan。**被测对象** = **spec-write** 与 **spec-review**。**Oracle** = `SPEC-STANDARD.md` 与 `SPEC-PRESENTATION.md`。organize / pipeline 旧测试仍在；编排 **Unverified**。Sub-feature 不另写 test-plan。

**验收：** 两个 skill 加两份标准是产出。人不读 skill 正文；好不好用只看本计划的测试结果。

## Test Scope

**In scope：** spec-write 与 spec-review 在「装进任意项目」场景下的行为；输入三类——本 repo `docs/features/`、外部 repo（`eval.yaml` 指定路径）、人工 fixture。**Out of scope / Unverified：** skill 正文改动（本 plan 只定义测什么）；设计合理性；merge 策略；**spec-pipeline 阶段编排**（Unverified，PRD-I）；单次编辑大小（PRD-C，Unverified）；可读性打分（PRD-M，在 spec-review 流程内，不作通过条件）；四套例子的 gold（PRD-K，放到别处；例子写进 skill 正文，由 TST-S 检查）。

**Parent vs sub（spec-review）：** 审 **parent**（`docs/features/spec-driven-development/` 根，不含 `features/<sub>/`）时须核对五篇均在：`prd`、`design`、`decision-history`、`impl-plan`、`test-plan`（见 parent HLD §8）。**Sub-feature** 不要求齐全，只审已有文件。

| 术语 | 含义 |
|---|---|
| **requirement** | 固定需求：「给我推荐一个 iPhone 并帮我购买」 |
| **context 包** | 模拟「人」的唯一答题来源；AI 反问时只从此取答案 |
| **gold case** | 一个输入案例：`requirement.md` + `context.md`，带独立版本 |
| **gold version** | 某个 gold case 的版本；分数只在同一 case/version 内比较 |
| **exemplar** | 被接受的模范产出 |
| **annotations** | `GOOD-*` / `BAD-*` 标注，含 `where` / `text` / `expected_fix` |
| **judge** | 单一固定模型 `deepseek-flash`，逐条 MUST / 对标打分 |
| **checker** | 3 次独立裁决；只有 `deepseek-flash` 时标 Unverified cross-model |
| **eval 配置** | `skills/spec-organize/tests/eval.yaml`；**基线** = 只装 spec-organize + 裸模型，`grill.skills: []` |

## Test Assets

| 路径 | 内容 |
|---|---|
| `skills/spec-organize/tests/eval.yaml` | `judge.model: deepseek-flash`；`gold.cases.iphone.version: v1`；`gold.repeats: 3`；`grill.skills`（基线 `[]`）；`target.repo`（默认 `../the-super-lab-eval`，`SDD_EVAL_REPO` 覆盖）；`checkers.models: [deepseek-flash]`；`checkers.repeats: 3`；`single_provider: true` |
| `skills/spec-organize/tests/checks/` | Python：`paths` `size` `frontmatter` `sections` `ids` `decision_log` `change_log` `index_book` `collision` `no_commit` |
| `skills/spec-organize/tests/mock-mcp/` | 共用一个 mock MCP client/server；固定工具；call 打出 stdout log，不真下单 |
| `skills/spec-organize/tests/fixtures/neg/<check>/` | 每检查 ≥1 最小违规树 |
| `skills/spec-organize/tests/fixtures/pos/` | 不得误报：ID 缺口、豁免路径、raw 无 frontmatter |
| `skills/spec-organize/tests/must_registry.yaml` | 每条 MUST：`id`（`MUST-{字母}`）、`source`、`text`、`method`（`python` \| `llm`）、`check` |
| `skills/spec-organize/tests/gold/iphone/v1/` | `requirement.md`、`context.md`、`context-variants/<slug>.md`、`runs/deepseek-flash/`（3 次产出 + `interview.md`）、`exemplar/`、`annotations.yaml`；PRD-K 四例的 gold 放到别处 |
| `skills/spec-organize/tests/gold/iphone/v1/annotations.yaml` | `GOOD-*` / `BAD-*`；`where`、`text`；BAD 含 `expected_fix`；`added_in`（gold 版本） |
| **当前状态** | gold 实际目录仍是 `gold/v1/`；IMPL-D 迁移到 `gold/iphone/v1/` |
| `skills/spec-organize/tests/reports/<run_id>.html` | 单 HTML；`run_id = <YYYY-MM-DD>-<branch>`；`tools/render_eval_report.py` 生成；不入库 |
| `skills/spec-review/tests/cases/<slug>/` | `input/`（植入缺陷）、`expected.yaml`（应检出 id、应忽略 severity 1–2）；11 机械 + 5 语义 |

**分支：** 产出在 `target.repo` 开 `eval/<gold-version>/<run_id>`，**不开 PR**；`runs/` 和 `reports/` 不入库；gold 的 requirement/context/exemplar/annotations 可 push。跨 skill 检查器、gold、报告均在 **spec-organize** 下。

## Scoring

**分数 1 — MUST 合规：** `x / total`，`total` = `must_registry.yaml` 条目数；`method: python` → 检查器；`method: llm` → `judge.model`；逐条 pass/fail。

**分数 2 — 对标 gold：** 对 `annotations.yaml` 每条——GOOD 相似命中 +1、未命中 0；BAD 未犯 0、相似犯 −1（judge 判相似）。`(Σ加分 − Σ减分) × 10 / annotations 条目总数`，满分 10，可为负；**仅同一 `gold.version` 内比较**。

**门槛：** 分数 1 = `total/total`；分数 2 ≥ 同 gold 版本**上一次** run。Checker：3 次独立裁决（同一 `deepseek-flash`），**不得推翻** python 项；**3/3** PASS。跨模型偏差标 **Unverified cross-model**。

**指标边界：** 分数 1/2 是 **eval 指标**，不是产品 success metric（PRD-G / ARD-N）。

**Gold 增长：** run 中发现新 good/bad → 追加 `annotations.yaml`，`gold.version` +1，`added_in` 标版本；报告须标 gold 版本。

## Test Cases

### TST-A — MUST registry 构建

**目标：** 扫描 document-standard design、pipeline design、parent HLD §4–§5 全部 MUST/禁止/必须 → `must_registry.yaml`；spec 定稿后重扫。**输入：** 三篇 design。**断言：** 覆盖率 100%；每条标 `python` 或 `llm`。**判定：** 锚点比对脚本。

### TST-B — 机械检查器 + 负向 fixture

**目标：** 检查器有效。**输入：** `fixtures/neg/*`、`fixtures/pos/*`。**断言：** neg 必 fail；pos 必 pass。**判定：** pytest。

### TST-C — Gold 生成（3 次 run）

**目标：** 基线下 3 次 iPhone feature spec。**输入：** `gold/iphone/v1/requirement.md` + `context.md`；`grill.skills: []`；只装 spec-organize；`deepseek-flash`。**断言：** 每次含 prd/design/decision-history/impl-plan/test-plan；`interview.md` 中模拟人回答均出自 context 或「未提供」。**判定：** Python（文件）+ judge（出处）。跨模型偏差 **Unverified**。

### TST-D — Gold 提炼

**目标：** 3 次 run → `exemplar/` + `annotations.yaml` v1。**输入：** TST-C 产出。**断言：** exemplar 过 TST-B、分数 1 全过；annotation 有 `where`/`text`；BAD 有 `expected_fix`。**判定：** Python + 人工认可（Change Log 记录）。

### TST-E — spec-organize happy path

**目标：** 改 skill 后同需求重跑。**输入：** 同 TST-C。**断言：** 分数 1 全过；分数 2 不退步。**判定：** Python + judge。

### TST-F — spec-organize unhappy（输入侧）

**目标：** context 带坑时不自猜。**输入：** `context-variants/`：`budget-conflict`、`family-disagree`、`missing-info`、`midway-change`。**断言：** 须 report/ask；budget/family 已有 decision history 先后则取较晚者，否则问用户，不得猜；midway-change 须新 ARD + strike+link；missing-info 不得编造。**判定：** judge + Python（ARD 结构）。

### TST-G — 真实树 Lint

**目标：** 别人写的 spec 是否合规。**输入：** 本 repo `docs/features/`；外部 repo 路径。**断言：** spec-organize Lint 与 `checks/` 一致；豁免不报。**判定：** Python 对比。

### TST-H — spec-review 检出率

**目标：** 找全缺陷、不误报。**输入：** 11 个机械检查案例 + 5 个语义案例；干净 exemplar。**断言：** 植入项均检出并引用 DSGN/MUST id；干净零 3+ 发现；1–2 不进讨论。**判定：** id 集合比对。

### TST-I — spec-review 建议质量

**目标：** 修改建议正确。**输入：** TST-H 检出项。**断言：** 建议 vs `expected_fix`：照改后缺陷消除且无新 MUST 违规。**判定：** judge；报 `x / 检出数`。

### TST-J — Eval 配置矩阵

**目标：** 不同 grill 组合。**输入：** `grill.skills`: `[]`、`[wayfinder]`、`[grill-with-docs]`、两者。**断言：** 每配置一份报告；基线先跑；只报分不设门槛。**判定：** 同 TST-E。

### TST-K — 报告

**目标：** 单 HTML。**输入：** 任一 run。**断言：** run_id、分支、gold 版本、eval 配置、分数 1 逐条（python/llm）、分数 2 ±、TST-F 变体、3 次 checker。**判定：** 生成 + schema。

### TST-L — 3 次独立裁决

**目标：** 最终 PASS/FAIL。**输入：** HTML + diff。**断言：** 3/3；不推翻 python；同一 `deepseek-flash` 的 3 次独立 run。**判定：** 3 次；跨模型偏差 **Unverified**。

### TST-M — 变更联动

**目标：** 标准或 gold 变更后测试同步。**输入：** 改 SPEC-STANDARD / design；或 run 中新 good/bad。**断言：** design 改 → TST-A + registry/fixtures 同批；新标注 → gold.version +1。**判定：** 流程 + 覆盖率。

### TST-N — Parent 齐备 / sub 豁免

**目标：** parent 五篇齐全；sub 不因缺篇 fail。**输入：** SDD parent 根 + `features/pipeline/`、`features/document-standard/`。**断言：** parent 缺任一篇 → spec-review ≥3；sub 仅 design 等仍 pass。**判定：** Python（路径）+ spec-review 报告。

### TST-O — PRD → design 追溯

**目标：** 每条 PRD 需求都有 design 锚点。**输入：** 父 PRD、parent HLD、pipeline/document-standard design。**断言：** 每个 `PRD-*` ID 映射到至少一个 `DSGN-*` / `PIPE-*`；未映射 fail。**判定：** Python（ID 集合比对）。

### TST-P — 归属 / 证据 / UNKNOWN

**目标：** design 篇有「子问题归属」表且结论可追溯。**输入：** 含归属表的 design；无依据结论；UNKNOWN 样例。**断言：** 缺表 fail；有结论无依据 fail；UNKNOWN 当事实 fail。**判定：** Python（表结构）+ judge（依据质量）。

### TST-Q — mock MCP log

**目标：** 执行只到 mock。**输入：** `skills/spec-organize/tests/mock-mcp/` 的 client/server。**断言：** call 打出 stdout log（tool/args/result）；无真实下单/订票。**判定：** Python（log 存在 + 无真实副作用）。

### TST-R — reader 新鲜度

**目标：** reader 不落后于 source。**输入：** `docs/book/html/spec-driven-development/spec-driven-development-reader.html` + 所有 source `.md`。**断言：** reader mtime ≥ 每个 source mtime；否则 fail。**判定：** Python。

### TST-T — 外部参照 gold

**目标：** defect 快照上每条 expect 都被报出；gold 快照上除 allow 外 0 finding。源仓库不在本机时跳过。**输入：** `gold/refs/<slug>/manifest.yaml`（ARD-BD）。**判定：** Python。不把私有 spec 正文复制进本仓库。

### TST-S — skill 正文四例

**目标：** spec-write 与 spec-review 正文包含 PRD-Q 四例。**输入：** 这两份 SKILL.md。**断言：** 每个至少提到 shed、北京旅游、数学题、股票；缺 fail。**判定：** Python（关键词）+ judge（是否只是点名）。

## Test Execution Order

1. **TST-A**（registry 不足 100% 则停）
2. **TST-B**（检查器失效则停）
3. **TST-O**、**TST-P**（设计覆盖/证据）
4. **TST-C** → **TST-D**（首次或 gold 升版）
5. **TST-G**、**TST-N**、**TST-R**、**TST-S**、**TST-T**
6. **TST-E**、**TST-F**
7. **TST-H** → **TST-I**
8. **TST-Q**（mock 执行）
9. **TST-K** → **TST-L**
10. **TST-J**（可选）
11. 改动 → **TST-M** → 1

## Expected Pass Threshold

| Gate | 条件 |
|---|---|
| 测试框架可用 | TST-A 100%；TST-B 全过 |
| 设计完整 | TST-O 100%；TST-P 全过 |
| 执行 mock | TST-Q log 存在且无真实副作用 |
| reader / skill 正文 | TST-R 新鲜；TST-S 四例齐全 |
| 外部 gold | TST-T：defect 的 expect 全报出；gold 除 allow 外 0 条；源不在本机则跳过 |
| Gold v1 冻结 | TST-D：exemplar 分数 1 全过；annotations 人工认可 |
| spec-organize 可发布 | TST-E 分数 1 全过、分数 2 不退步；TST-F 四变体全过；TST-G 零差异；TST-L 3/3 |
| spec-review 可发布 | TST-H 检出 100%、误报 0；TST-I ≥ 上一次；TST-L 3/3 |
| Gold 升版 | TST-M 追加后重跑 TST-E/H 建新基线 |

## Traceability — PRD → TST

| PRD | Covered by |
|---|---|
| PRD-A | Unverified |
| PRD-B | Unverified |
| PRD-D | TST-B（size cap） |
| PRD-E | TST-B（paths） |
| PRD-F | TST-B（decision_log） |
| PRD-H | TST-M；TST-S |
| PRD-J | Unverified（spec-pipeline 编排，PRD-I） |
| PRD-L | TST-P |
| PRD-O | TST-Q |
| PRD-P | TST-S；Expected Pass Threshold 表 |
| PRD-C | Unverified |
| PRD-G | Unverified（ARD-N） |
| PRD-I | Unverified |
| PRD-K | Unverified |
| PRD-M | Unverified |
| PRD-N | Unverified |
| PRD-Q | Unverified |

## Change Log

| Date | Change |
|------|--------|
| 2026-11-03 | Initiative harness only；Phase 1 测例在 document-standard test-plan |
| 2026-11-03 | document-standard 改回 feature 级 test plan |
| 2026-11-03 | 重写为 initiative 级：被测 = spec-organize / spec-review；两分制；gold 版本化；资产在 skills/<skill>/tests |
| 2026-11-03 | 移除 wayfinder-import 例外与 out-of-scope 项 |
| 2026-11-03 | §8 对齐：parent 五篇齐备（TST-N）；sub 豁免 |
| 2026-11-04 | 被测三 skill + spec-pipeline 编排 out of scope（HLD §7） |
| 2026-11-04 | 验收：四个 skill 是产出；人不读正文，只看测试结果 |
| 2026-11-04 | PRD-C 单次编辑大小列为测不了，移出 test plan |
| 2026-11-04 | TST-F：多人冲突取 decision history 较晚者，否则问用户，不得猜 |
| 2026-11-04 | 选择题：PRD-M 与四套 gold 移出本计划；PRD-N 评测只用 context |
| 2026-11-04 | 单模型 deepseek-flash 3 次 run；gold case/version/exemplar/annotations 四词；runs/reports 不入库 |
| 2026-11-04 | 新增 TST-O PRD→design、TST-P 归属/证据、TST-Q mock MCP、TST-R reader、TST-S 四例 |
| 2026-11-04 | TST-D/TST-K 改为 3 次 run/checker；TST-H 改为 11 机械 + 5 语义案例 |
| 2026-11-04 | 标注 gold 实际目录 v1 与目标 iphone/v1 的迁移 |
| 2026-11-07 | 被测改为 spec-write 与 spec-review；TST-S 只查这两份（ARD-AJ） |
| 2026-11-07 | TST-T：外部 gold 只留 manifest，不复制私有正文（ARD-BD） |
| 2026-11-07 | TST-R 输入改为 docs/book/html/ 下的 reader（ARD-BF） |
