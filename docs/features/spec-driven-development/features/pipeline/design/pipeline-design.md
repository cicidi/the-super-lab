---
feature: pipeline
type: design
state: draft
final_date: 2026-10-30
health: active
owner: cicidi
last_verified: 2026-11-04
---

# Spec-Driven Development — Pipeline

本篇定义 **spec-pipeline** 编排 skill：轻量 **guidance + 接口**。凡 **写/改 feature spec** 的工作 **先进 spec-pipeline**，由它按阶段 **推荐并调用** 其它 skill、维护 **轻量 state**、在提交前 **询问 review**、在迷路时 **recap**。

文档格式、路径、ID、体量见 sibling **`../document-standard/design/document-standard-design.md`**（**DSGN-A–M**）。本篇 **link，不 restate**。

## Problem Statement

Parent PRD 定义的四类上游问题见 `../../../prd/spec-driven-development-prd.md`。本篇补充 pipeline 要解决的 **流程** 问题：

- **大 feature / initiative** 难拆成可执行的 smaller feature，新人不知道顺序。
- 多个 skill 并存，调用方 **不知道何时用哪个**。
- 长会话后 **不知道进度**（做到哪、还剩什么）。
- **提交前** 容易跳过 review。

## Solution

**spec-pipeline** 为统一入口，驱动四阶段：

```
Create → Map → Converge ⇄ (PRD ↔ design ↔ decision-history) → Downstream (test-plan ∥ impl-plan)
```

- **Create：** 立项与 context（feature create、粗 PRD、搜索 → CLAUDE.local）。
- **Map：** **与人 interview**；AI 判断拆分/decision/scratch；**无** 固定 MUST 产物模板；可选 **可替换** map 工具（示例 wayfinder，**非** SDD deliverable）。
- **Converge：** 三角循环打磨；**收敛后** 才进入 Downstream。
- **Downstream：** **test-plan** 与 **impl-plan** **并行**，均自 **design 篇** 总结（对齐 parent PRD Solution）。

## User Stories

1. **拆分大需求：** 作为不熟悉 spec 的人，我希望经 pipeline **Map interview** 后，能拆出 smaller feature 并进入 spec-driven 写齐文稿。
2. **恢复上下文：** 作为中断后继续的人，我希望 pipeline **recap**：已做什么、state 字段、待办、建议下一步。
3. **提交前：** 作为提交者，我希望 pipeline 在「该提交了」时 **询问** 是否先跑 **spec-review**。

## Implementation Decisions

- **编排** = **spec-pipeline**；**标准** = **spec-organize**；**写** = **spec-write**；**审** = **spec-review**（提交前由 pipeline **询问**，非 silent 强制）。
- **Map** 以 **interview** 为主；**AI 判断** 是否记 decision、建议拆 feature、或仅 scratch task；**人确认** 后才创建 `docs/features/<f>/` 路径。
- Map 工具（示例 **wayfinder**）经 **推荐表** 调用，**可替换**；不在 SDD deliverable 清单。
- **State：** **feature create 完成、`<f>` 未确定前** — 进度只写在 **`CLAUDE.local.md`**（或项目 CLAUDE 层），**不** 创建 `raw/state/*.md`。**`<f>` 确定后** — 权威 state 在 **`docs/features/<f>/raw/state/state-<YYYY-MM-DD>.md`**（document-standard **DSGN-B/C**）。
- **Recap** 由 pipeline **生成**给人看；**不是** source of truth（SO T = state 文件 + committed 文稿）。
- 后期 task 管理：**plug-in** 其它 skill；本篇 **不** 引入 BMAD/GSD 级重框架。
- 协作：读上游 artifact，**禁止 silent 改**；冲突 **Detect → Report → Ask**（同 document-standard **DSGN-G**）。
- 本篇设计条目 ID 前缀 **`PIPE-*`**；**不** 用 **DSGN-*** 作 pipeline 内锚点（DSGN 保留给 document-standard）。

## Design

### PIPE-A — spec-pipeline 职责（MUST）

**来源：PRD-A**（在既有 pipeline 上改进，不另造编排）。

- **PIPE-A1** 任意「写/改 spec」任务 **经 spec-pipeline 进入**（除非 human 显式跳过并记入 state/recap）。
- **PIPE-A2** 调用 **spec-organize** 执行标准、Lint、Organize（路径/格式以 organize 为准）。
- **PIPE-A3** 调用 **spec-write** 执行文稿增删改（含 parent HLD §4 小步编辑 norm）。
- **PIPE-A4** 在 **提交/推送 committed 变更前**，**询问** 是否 **spec-review**；用户拒绝则记录，不 silent 跳过审计痕迹。
- **PIPE-A5** 用户请求或会话丢失时 **recap**：已做、当前 state、待做、建议下一步（list）。
- **PIPE-A6** 维护/读取 **PIPE-H** 定义的 state；推荐 **PIPE-G** 表中的 skill。

### PIPE-B — 四阶段总览

| 阶段 | 目的 | 典型失败 |
|---|---|---|
| **Create** | 建立 feature/initiative 与 context | 无 PRD 锚点、context 只存在于聊天 |
| **Map** | 探已知/未知、判断是否拆分 |  silent 建目录、无 interview |
| **Converge** | PRD/design/decision 循环至够稳 | 在 open decision 上写死 design |
| **Downstream** | test-plan ∥ impl-plan | 只写 test 无 regression，或 impl 无顺序 |

### PIPE-C — Create

1. **feature create**（walter-worker）建立或选定 **`<f>`** / initiative 根（peer vs nested 见 parent HLD §3.1）。
2. **粗 PRD**（示例：「推荐 iPhone 并协助购买」)— 可 draft，不要求一次写齐六要素。
3. **搜索/调研** → 已知 context 写入 **`CLAUDE.local.md`**（或项目 CLAUDE 层）；**不** 替代 committed PRD。

### PIPE-D — Map

1. **Interview** 用户（及 context 包）；AI 归纳已知/未知。
2. **AI 判断**（无固定 MUST 文件类型）：是否建议 **新 feature**、是否写 **decision**、是否在 **scratch** 留 task 线索、或 **暂不拆** 进入 Converge。
3. **Recap** Map 结论：判断摘要、建议拆分、仍 open 项。
4. **可选** 调用 **pluggable map skill**（示例 wayfinder）；**不得** 替代 interview。
5. **禁止** 未经确认创建 `docs/features/<f>/` 或移动 committed 树（Organize 模式负责路径）。
6. **拆分标准（暂时）：** AI 先给几个拆法推荐。一个人 20 小时以内能搞清楚的，算一个 feature spec；AI 估算超过 20 小时的，拆成 peer 或 sub-feature。小时估算和拆不拆的评判都由 AI 做。
7. **子问题（PRD-L）：** 每个子问题标成 AI 查、人决定、或 AI 查完后人决定。人没问到的盲区和风险，AI 必须提出。

### PIPE-E — Converge

**循环：** PRD ↔ **design 篇** ↔ decision-history（parent PRD Solution）。

**收敛条件（MUST 全满足才进 Downstream）：**

- **PIPE-E1** 无未关闭的 blocking open decision；每条 open item 带 `blocking: true|false`，仍 open 的须在 design 中点名。`blocking: true` 不得进 Downstream（ARD-AG）。
- **PIPE-E2** PRD 写清 limitation、preference、timeline、resource、tool；没有的注明 not apply。design 篇与 decision history 都在，才进 Downstream。
- **PIPE-E3** design 篇列出 **依赖的 decision** 与 **仍 open** 项；含 implementation 所需的 contract/边界决策（impl 任务细节 **下一轮** 再定）。

### PIPE-F — Downstream

- **test-plan** 与 **impl-plan** **并行**启动；**互不** 串行依赖；均从 **design 篇** 总结。
- **test-plan：** 每项任务 **完成检查** + **regression guard**（PIPE-F1）。
- **impl-plan：** 每条任务写依赖与挡住谁；被挡住的后做，没被挡住的先做（PIPE-F2）。

### PIPE-G — Skill 推荐（接口）

| 阶段 | 场景 | 推荐 skill | 必选 |
|---|---|---|---|
| Create | 新 feature/initiative | feature create（walter-worker） | MUST |
| Create | 补 context | research（示例） | 可选 |
| Map | 探图/拆分辅助 | *pluggable map*（示例 wayfinder） | 可选 |
| Converge | 写/改文稿 | spec-write | MUST（有改动时） |
| Converge | 合规/路径 | spec-organize | MUST（create/move/merge 后） |
| 任意 | 提交 committed 前 | spec-review | 询问（PIPE-A4） |
| Downstream | test-plan / impl-plan 篇 | spec-write + spec-organize | MUST |

*wayfinder 等 map 工具 **可替换**，**非** SDD 必装 deliverable。*

### PIPE-H — State

| 时段 | 存储 | 内容 |
|---|---|---|
| **`<f>` 未确定** | **`CLAUDE.local.md`**（项目 CLAUDE 层） | phase、粗需求、Map 笔记、open items |
| **`<f>` 已确定** | **`docs/features/<f>/raw/state/state-<YYYY-MM-DD>.md`** | `phase`（Create/Map/Converge/Downstream）、`feature`、`open_items`、`last_action`、可选 `scratch_ref` |

- **Recap** 读取 state + committed 树；输出发给用户，**默认不 commit** recap 本身。
- 方向性结论 **升格** 进 decision-history / PRD / design，**不** 长期只留在 state。

### PIPE-I — 协作、血缘、齐备度

- **读上游、不 silent 改**；分歧 **report + ask**（**DSGN-G**）。
- **多人 decision：** 以 decision history 时间较晚的为准；看不出先后则问用户。AI 不猜测（**PRD-F**）。
- **decision 变更** → 点名需 review 的下游 artifact（PRD、design、impl-plan、test-plan）。
- **Parent vs sub 齐备：** parent initiative review 见 parent HLD **§8**；**sub-feature** 不要求五篇齐全 — **spec-review** 执行，pipeline **转发** 到 review，不 duplicate 规则。

### PIPE-J — 边界

| 本篇管 | 不管 |
|---|---|
| 阶段、入口、skill 推荐、state、recap、提交前 review 询问 | frontmatter、路径、ID 细则（document-standard） |
| 收敛条件、Downstream 并行 | map/research **skill 正文** |
| 轻量 state | 重 task/BMAD/GSD 框架 |

### PIPE-K — 非软件问题的五篇映射

**PRD-K / PRD-Q。** 非软件难题走同一套五篇；不新增文档类型。

| 内容 | 落点 |
|---|---|
| 调研、学习笔记、原始资料 | `raw/research/<topic>.md`（不 commit、不作权威） |
| 决策 | `decision-history`（`ARD-*`） |
| 方案、执行步骤 | `design` 篇；需要排序的执行步骤进 `impl-plan` |
| 验证 | `test-plan` |

`raw/` 结论升格进 committed 文档时只 link，不 restate。四个例子（shed、北京旅游、数学题、股票）写进 skill 正文，不在本仓库建 gold。

### PIPE-L — 子问题归属与证据

有子问题的 feature，其 **design 篇** 必须有「子问题归属」表；纯标准/编排 design 可注明 not apply。

| 子问题 | 归属 | 依据 |
|---|---|---|
| <问题> | `AI 查` / `人决定` / `AI 查完人决定` | `raw/` 路径、URL 或 `ARD-*` |

- 归属只取三值；人没问到的盲区与风险，AI 必须主动补行。
- 依据必须可追溯；查不到写 `UNKNOWN`，不得写推测。
- **spec-review** 检查「有结论但无依据」与「该标 UNKNOWN 却写了事实」。

## Testing Decisions

验证见 parent **`../../../test-plan/spec-driven-development-test-plan.md`**。本篇至少覆盖：

- **spec-pipeline：** 进门、recap、提交前 review 询问、state 切换 — **Unverified**（暂无可执行测试；PRD-I）。
- **PRD：** limitation、preference、timeline、resource、tool 均写明或注明 not apply。
- **decision-history：** 产品方向 decision 有 **ARD-** ID；supersede = strike + link（**DSGN-J**）。
- **design 篇：** 依赖 decision；open decision 已命名。
- **test-plan / impl-plan：** 并行存在；test 含 completion + regression guard。
- **Cross-artifact：** 测试可追溯到 PRD 要求（TST-O 新增）。
- **PRD-N：** 正式 spec 结论链到事实；本 harness 评测答案只来自 context 包。
- **PRD-O：** 一个共用 mock MCP server，call 打出 log 即通过。
- **PRD-M：** 可读性打分在 spec-review 流程内，不作为测试通过条件。

## Out of Scope

- **wayfinder**、feature create、research 等 **skill 正文**与部署。
- BMAD/GSD 式 **重** state/task 框架与满 repo 模板文件。
- **spec-pipeline** 实现（prompt、代码、hook）。
- **impl-plan** 阶段 **task 粒度与 parent impl-plan 文稿**（**下一轮 impl 讨论**）。
- document-standard 条文 duplicate。

## Further Notes

- As-is 技能安装图：`../../../design/spec-driven-development-workflow.html`（对照，非 target pipeline 唯一来源）。
- Open：plug-in task skill；收敛条件自动化检查。Map 拆分见 **PIPE-D** 第 6 点。

## Alternatives Considered

- 把 wayfinder-import 作为 sub-feature 固化 → 拒(**ARD-T**):map 工具须可替换。
- 每阶段一个 skill → 拒:四个 skill 已覆盖(ARD-AB),按阶段拆会重复职责。
- 固定五阶段瀑布、跳过 Map → 拒:未知多的题目会漏拆。

## Drawbacks

- Interview 贵且慢,小改动也要走一遍。
- Map 的产物不可机械验证,只能靠人确认。

## Risks and Mitigations

- 风险:AI 未经确认创建 `docs/features/<f>/` → Step 2 强制 confirm + 反模式清单。
- 风险:相位判断错 → 读 `raw/state/state-<date>.md` 与 CLAUDE.local,以文件为准。

## Open Questions

- 阶段编排本身无执行测试(**PRD-I**,Unverified)。
- recap 模板是否所有项目都适用。

## Reversibility

- 阶段是叠加的:去掉 Map 不影响 Create/Converge/Downstream。
- state 文件可弃用,回到 CLAUDE.local 记录。

## Change Log

| Date | Change |
|------|--------|
| 2026-10-30 | Initial creation; pipeline split out of parent design |
| 2026-10-30 | Problem/Solution link to parent PRD; D1–D8 artifact stages |
| 2026-11-03 | document-standard 引用 DSGN-A–M；移除 wayfinder-import 引用 |
| 2026-11-03 | 重写：spec-pipeline 编排；四阶段；PIPE-*；Map interview；state CLAUDE.local → raw/state |
| 2026-11-04 | PIPE-D 第 6 点：20 小时内一个 feature spec，超出拆 peer 或 sub；估算和评判由 AI 做 |
| 2026-11-04 | PIPE-E2：PRD 写清五项，没有则 not apply；design 与 decision history 都在才进 Downstream |
| 2026-11-04 | PIPE-I：多人 decision 按 history 时间，否则问用户，AI 不猜测 |
| 2026-11-04 | PIPE-D 第 7 点：子问题标归属，AI 必须提出人没问的风险 |
| 2026-11-04 | PIPE-K 非软件五篇映射；PIPE-L 归属与证据；spec-pipeline 标 Unverified |
| 2026-11-04 | PIPE-E1 加 blocking 字段；PIPE-L 标注纯标准/编排 design 可 not apply |
| 2026-11-06 | PIPE-F2：impl 写依赖与挡住谁；被挡住的后做 |
