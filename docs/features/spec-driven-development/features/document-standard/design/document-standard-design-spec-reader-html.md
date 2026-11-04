---
feature: document-standard
type: design
state: draft
final_date: 2026-11-03
health: active
owner: cicidi
last_verified: 2026-11-03
---

# Document Standard — Spec Reader HTML（Design）

**Aspect design：** **DSGN-N**（spec reader / human HTML 汇编）。PRD：**PRD-A–P** 见 `../prd/document-standard-prd-spec-reader-html.md`。与 **DSGN-B** 路径、**DSGN-I** 优先级、**DSGN-F** ID 引用一致。**Implementation：** `skills/spec-html-standard/SPEC-HTML-STANDARD.md`（标准文件，**非** skill）；**spec-pipeline** 编排入口，加载该标准汇编 HTML。

## Problem Statement

1. Feature spec 多篇、多层，人类难以一次读全。
2. 「人类可读 HTML」若写成 **短摘要**，review 与 onboarding 会 **漏 MUST**，与 document-standard「L1 永不删」冲突。
3. 先前 v0 指引（spec-pipeline `SPEC-READER.md`）写「summarize and rephrase」易被理解成 **大幅删减** — **废止该解读**；以本篇 **DSGN-N** 为准。

## Solution

定义 **Spec Reader HTML** 产物：单文件、Tab 化、富排版、**保真优先** 的 derived view；canonical 永远是 committed `.md`。

---

## Design

### DSGN-N — Spec Reader HTML 契约

#### DSGN-N-A — 产物与路径

| 项 | Rule |
|---|---|
| **文件名** | `<parent>-reader.html` |
| **目录** | `docs/features/<parent>/`（与 parent initiative 同级，不在 `features/<sub>/` 内） |
| **Source of truth** | 各 Tab 对应的一篇或多篇 committed `.md`；HTML **derived** |
| **参考（待加料）** | `docs/features/spec-driven-development/spec-driven-development-reader.html` — 结构可参考，**内容须按 N-B 补全** |

#### DSGN-N-B — 保真（MUST — 回应「不要精简这么多」）

映射 **DSGN-I** 到 HTML 汇编：

| Level | 在 HTML 中 |
|---|---|
| **L1** | **全部呈现**：MUST/禁止/必须、functional req 表 **行**、test case **行**、impl task **条目**、decision-history **Log 行**（含 ID）、contract 表 **数据行**、Out of Scope 列表、assumption、boundary、security、error — **禁止** 用一段话代替整张表或整节 |
| **L2** | **保留事实**；表述可改写为更短句子或 callout，**不得** 删掉 rationale 中的结论 |
| **L3** | Alternatives 等 **可压缩** 为 bullet +「详见 canonical md」 |
| **L4** | 可省略正文，**MUST** footer/link 指向 md |

**条目 ID（DSGN-F）：** HTML 中 **MUST** 保留可见 ID 字符串（`PRD-A`、`DSGN-B`、`ARD-C`、`IMPL-3`/`IMPL-C`、`TST-A` 等 — 以 md 为准），便于与 review / registry 对齐。

**禁止（MUST NOT）：**

- 仅保留「Problem / Solution 各一段」而删掉 **Design** 下各 **DSGN-*** 小节主体。
- 用「见 md」代替 **整 Tab**（允许 **节内** L3/L4 指向 md）。
- Markdown 预览器模式：整页 `<pre>`、或未排版的 raw md 粘贴。

**允许：**

- 把 md 表格 **重排** 为 HTML `<table>`（列可合并显示，**行集合不得少**）。
- 把长 prose **分段**、加 callout、加 mini flow（Mermaid 或 ASCII），**不减少** L1 断言数量。
- 同一 type 多 part 文件 → 同一 Tab 内 **按 part 分 `<section>`** 或子 Tab。

#### DSGN-N-C — 结构与 Tab

**Page header（MUST）：** 说明本页为 **阅读用汇编**；权威修改在 `.md`；列出 parent slug。

**Tab 组 1 — Parent：** 每存在一类 committed 文档一个 Tab：`PRD` | `Design` | `Impl plan` | `Test plan` | `Decision history`（`how-to` 可选 Tab）。

**Tab 组 2+ — Children：** 每个 `docs/features/<parent>/features/<sub>/` 一组 Tab（或一组内 section per type）。**至少** 纳入 `<sub>` 的 `design/<sub>-design.md` 及 design part 文件。

**每 Tab footer（MUST）：** `Canonical:` + 相对 repo 路径；多 part 时 **列出全部** part 路径。

#### DSGN-N-D — 视觉与 HTML 技术

- **SHOULD** 复用 initiative 已有 CSS 模式（参考 `spec-driven-development.html`、`document-standard.html`：layout、chip、card、callout）。
- **SHOULD** 单文件自包含 CSS（v0），便于 `file://` 或静态托管。
- **MAY** 内联 Mermaid（若 initiative 已有先例）；否则 ASCII flow。
- **MUST NOT** 依赖运行时 fetch 加载 `.md` 作为主内容（可 fetch 仅作 debug，非交付形态）。

#### DSGN-N-E — 流程与标准边界

| 角色 | 职责 |
|---|---|
| **spec-pipeline** | 阶段感知；用户要 reader 或 major spec 更新后 **提示/触发**；指示加载 **SPEC-HTML-STANDARD** |
| **spec-html-standard** | `skills/spec-html-standard/SPEC-HTML-STANDARD.md` — **DSGN-N** 可执行摘要；**无** SKILL.md |
| **spec-write** | 只改 **md** 正文，不拥有 HTML 模板 |
| **spec-organize** | 路径、INDEX；不替代 reader 汇编 |

**spec-pipeline `SPEC-READER.md`（若仍存在）：** 仅 pointer 至本篇 + **SPEC-HTML-STANDARD**，避免双契约。

#### DSGN-N-F — 何时更新 reader

- Parent 或 child 任一 committed spec **实质变更**（尤其 L1/L2）后 **SHOULD** 更新 reader。
- 用户显式：「生成 reader」「human html」「spec 汇编」「reader 太简了补全」。
- **不必** 每次 typo 级 commit 都 regenerate（NICE）。

#### DSGN-N-G — 未来 md→html

可增 **mechanical contract**（例如 design part `document-standard-design-md-to-html.md`）：映射 md AST → HTML 组件。自动化 **仍 MUST** 满足 **DSGN-N-B**；本篇 + **SPEC-HTML-STANDARD** 为 semantic norm。

---

## User Stories

（与 PRD **PRD-G–I** 相同意图；实现验收以 **DSGN-N-B** 为准。）

## Implementation Decisions

| ID | Decision |
|---|---|
| **DSGN-N-H** | Reader 契约挂在 **document-standard** sub-feature（非 pipeline design），因属 **文档形态 / 阅读标准**，与 **DSGN-A** 并列扩展 |
| **DSGN-N-I** | v0 手维 HTML；保真规则先写进 spec，避免 agent 再产出「极简 reader」 |
| **DSGN-N-J** | 可执行层 **`skills/spec-html-standard/SPEC-HTML-STANDARD.md`**；main design 索引链到 aspect 篇 **DSGN-N**；**不** 新增 spec-reader skill |

## Testing Decisions

Initiative test plan 暂不单独为 reader 开 TST；**NICE：** spec-review 抽检「reader Tab 是否含 md 中全部 **PRD-*/DSGN-*/TST-*** ID」。

## Out of Scope

- CI 阻塞「reader 与 md 逐字一致」。
- 替代 spec-organize lint。

## Further Notes

- **反例：** 当前 `spec-driven-development-reader.html` 多处 child/parent design 仅留 slogan — regenerate 时按 **DSGN-N-B** 补全。
- Parent HLD 已指 reader 路径；deliverable skills 仍为四个；HTML 规范在 **spec-html-standard**。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-03 | Initial aspect design **DSGN-N**；保真规则 |
| 2026-11-03 | **spec-html-standard** 替代 spec-reader skill（**DSGN-N-E/J**） |
