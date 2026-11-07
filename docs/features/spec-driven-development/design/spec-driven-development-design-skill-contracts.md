---
feature: spec-driven-development
type: design
state: draft
health: active
owner: cicidi
last_verified: 2026-11-04
---

# Spec-Driven Development — Skill Contracts

## Problem Statement

四个 skill 各自的输入、输出和边界没有单独一篇设计承载。结果是 `SKILL.md` 成了事实权威，pipeline、organize、review、write 之间容易重叠或漏责；PRD-B / PRD-P / PRD-Q 无法被 review 和测试直接检查。

## Solution

本篇定义四个 skill 的**行为契约**；`SKILL.md` 只是实现。规则细节仍以 `document-standard` 的 `DSGN-*` 和 `pipeline` 的 `PIPE-*` 为准，本篇只定接口与边界。

## User Stories

- 作为调用方，我希望知道每个 skill 在什么阶段被调用、需要给什么、会产出什么。
- 作为 reviewer，我希望四个 skill 的责任不重叠，缺一条能找到唯一负责的 skill。
- 作为维护者，我希望改 `SKILL.md` 时不改变契约；契约变了要先改本篇。

## Implementation Decisions

- **Authority：** 契约以本篇为准；`SKILL.md` 与正文冲突时，先改契约再改正文（`DSGN-G`）。
- **不定义：** 失败策略、版本/迁移、来源可信度分级、数据清理（`ARD-AF`）。
- **四例：** 四个 skill 正文都要点名 shed、北京旅游、数学题、股票（PRD-Q）；它们是**说明性例子**，不是本仓库 gold。
- **Unverified：** pipeline 编排、单次编辑大小、可读性打分、跨模型偏差按 PRD-I 标 `Unverified`。

## Design

| Skill | 阶段 | 输入 | 输出 | 边界 |
|---|---|---|---|---|
| **spec-pipeline** | 任意入口 | 用户请求、`CLAUDE.local` / `raw/state`、PRD/design/decision | phase、recap、state、review 询问 | 不写正文；不 silent 改上游；不自行宣布收敛 |
| **spec-organize** | create / move / merge / lint | feature 树、`SPEC-STANDARD.md` | 路径/格式修正、findings | 机械 MUST 可 fix；semantic 只 report |
| **spec-review** | 提交前 / 设计审查 | diff 或树、PRD/design/test-plan | 带 severity 的 findings + 修改建议 | 不 fix、不改写；可读性 gate 在此流程内跑，但不作通过条件 |
| **spec-write** | Converge / Downstream | 已确认的修改意图 | 改后的文稿 | 默认 ≤10 行/200 字符；restructure 需 human 授权；不 silent 改上游 |

**共享能力落点：**

- 子问题归属表（PRD-L / PIPE-L）写在每个 feature 的 `design` 篇。
- 证据与 `UNKNOWN`（PRD-N）由 `spec-write` 写、`spec-review` 查。
- mock MCP client/server（PRD-O）放在 `skills/spec-organize/tests/mock-mcp/`；pipeline 在 Downstream 后调用。
- 四个例子（PRD-Q）写进四个 `SKILL.md` 正文；由 TST-S 检查。

## Testing Decisions

- **TST-S：** 四个 `SKILL.md` 都包含四例。
- **TST-O / TST-P：** PRD → design 追溯；归属/证据/UNKNOWN。
- **TST-Q：** mock MCP call 打出 log，且无真实副作用。
- **Unverified：** spec-pipeline 编排（PIPE-A4/A5/H）、单次编辑大小（PRD-C）、可读性打分（PRD-M）、跨模型偏差（ARD-AD）。

## Out of Scope

- 失败策略、版本/迁移、来源可信度分级、数据清理（`ARD-AF`）。
- 存量不合规文档的迁移。
- 各 skill 的具体 prompt 文案；由 `SKILL.md` 实现。

## Further Notes

- 新增 skill 时先补本表，再写 `SKILL.md`。
- 契约变更需同步 `document-standard` / `pipeline` 的对应 `DSGN-*` / `PIPE-*`。

## Reversibility

- 契约变更可回退:改本篇 + `SKILL.md`,无数据迁移。
- 新增 skill 只需追加一行;移除 skill 须同批改 pipeline 与 test plan。

## Alternatives Considered

- 四个 skill 合成一个 → 拒:职责重叠,review 无法独立。
- 契约直接写进 `SKILL.md` → 拒:正文变权威,契约失去独立地址(**ARD-AB** / **DSGN-G**)。

## Drawbacks

- 多一层间接:改行为要同时动契约与正文。

## Risks and Mitigations

- 风险:正文与契约漂移 → 冲突时契约优先,`spec-review` 检查引用。

## Open Questions

- 新 skill(如可替换的 map 工具)是否要进契约表。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-04 | Initial creation; four skill contracts, shared capabilities, testing pointers |
