---
feature: spec-driven-development
type: design
state: draft
health: active
owner: cicidi
last_verified: 2026-11-04
---

# Spec-Driven Development — Skill Contracts

入口文件：[spec-driven-development-design.md](spec-driven-development-design.md)。

## Problem Statement

spec-write 与 spec-review 的输入、输出和边界由本篇承载。标准在 SPEC-STANDARD.md 与 SPEC-PRESENTATION.md（ARD-AJ）。`SKILL.md` 不是权威。

## Solution

本篇定义 spec-write 与 spec-review 的**行为契约**；`SKILL.md` 只是实现。规则细节以 SPEC-STANDARD.md 与 SPEC-PRESENTATION.md 为准（ARD-AJ）。

## User Stories

- 作为调用方，我希望知道每个 skill 在什么阶段被调用、需要给什么、会产出什么。
- 作为 reviewer，我希望 write 与 review 的责任不重叠，标准条款有唯一文档地址。
- 作为维护者，我希望改 `SKILL.md` 时不改变契约；契约变了要先改本篇。

## Implementation Decisions

- **Authority：** 契约以本篇为准；`SKILL.md` 与正文冲突时，先改契约再改正文（`DSGN-G`）。
- **不定义：** 失败策略、版本/迁移、来源可信度分级、数据清理（`ARD-AF`）。
- **四例：** spec-write 与 spec-review 正文都要点名 shed、北京旅游、数学题、股票（PRD-Q）；它们是说明性例子，不是本仓库 gold。
- **Unverified：** pipeline 编排、单次编辑大小、可读性打分、跨模型偏差按 PRD-I 标 `Unverified`。

## Design

| Skill | 阶段 | 输入 | 输出 | 边界 |
|---|---|---|---|---|
| **spec-write** | 新建或修改 | 用户意图、SPEC-STANDARD、SPEC-PRESENTATION | 改后的文稿 | 先判断新建还是改哪些文；≤10 行/200 字符；不 silent 改上游 |
| **spec-review** | 提交前 / 设计审查 | diff 或树、两份标准 | 建议表；每次一个选择 | 不 fix、不改写；问完可有一个附加题 |

**共享能力落点：**

- 子问题归属表（PRD-L / PIPE-L）写在每个 feature 的 `design` 篇。
- 证据与 `UNKNOWN`（PRD-N）由 `spec-write` 写、`spec-review` 查。
- mock MCP client/server（PRD-O）仍放在 `skills/spec-organize/tests/mock-mcp/`。
- 四个例子（PRD-Q）写进 spec-write 与 spec-review 的 `SKILL.md`；由 TST-S 检查。

## Testing Decisions

- **TST-S：** spec-write 与 spec-review 的 `SKILL.md` 都包含四例。
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

- 合成单一 skill → 拒:write 与 review 必须分开。ARD-AJ 将入口收成这两个 skill。
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
| 2026-11-07 | 契约改为 spec-write 与 spec-review；标准两份文档（ARD-AJ） |
| 2026-11-07 | part 链回 spec-driven-development-design.md（ARD-AV） |
