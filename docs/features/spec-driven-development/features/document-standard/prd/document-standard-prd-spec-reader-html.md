---
feature: document-standard
type: prd
state: draft
final_date: 2026-11-03
health: active
owner: cicidi
last_verified: 2026-11-03
---

# Document Standard — Spec Reader HTML（PRD）

**Aspect PRD：** 人类可读的 **feature spec 汇编 HTML**（parent + child，Tab 浏览）。权威契约见 sibling design 篇 `../design/document-standard-design-spec-reader-html.md`（**DSGN-N**）。可执行摘要：`skills/spec-html-standard/SPEC-HTML-STANDARD.md`（**非**独立 skill）；**spec-pipeline** 触发时加载该标准。

## Overview

Committed feature spec 以 `.md` 为 source of truth，但 parent initiative 往往 **多篇、多层**（parent 五类 + `features/<sub>/`）。人需要 **一次打开、按 Tab 读完** 的视图，且 **不能** 因为「好读」而丢掉 spec 里的 MUST、表格行、条目 ID 与 L1 事实。

现有示例 `docs/features/spec-driven-development/spec-driven-development-reader.html` **过度精简**（大量章节被缩成几句），与「spec 可读」目标不符。本篇定义 **要什么、不要什么**；设计细则在 **DSGN-N**。

## Goals and Success Metrics

| ID | Goal | Success |
|---|---|---|
| **PRD-A** | **高保真阅读** | 读者在 HTML 里能看到与 `.md` **等价的 L1 信息**（MUST/禁止、表格主体行、前缀 ID 条目、Out of Scope、关键 diagram/流程）；**不得** 做成 executive summary |
| **PRD-B** | **富 HTML，非 MD 预览** | 卡片、callout、表格、可选 flow；**禁止** 仅 `fetch` + `<pre>` 或整页粘贴 raw markdown |
| **PRD-C** | **Parent + child 覆盖** | Parent：存在的五类 `prd` / `design` / `impl-plan` / `test-plan` / `decision-history` 各一 Tab（或等价分组）。Child：每个 `features/<sub>/` 至少纳入其 **design**；若另有 committed type 则一并纳入 |
| **PRD-D** | **可追溯** | 每个 Tab（或 major section）底部 **`Canonical: <path-to.md>`**；页头声明：改 spec 先改 `.md`，再更新 HTML |
| **PRD-E** | **位置与命名** | 输出 `docs/features/<parent>/<parent>-reader.html`（例：`spec-driven-development-reader.html`） |
| **PRD-F** | **可演进** | v0 可手维；后续可有 **md→html 机械契约** 或工具；本篇 + **DSGN-N** 在自动化之前仍是 norm |

## User Stories

- **PRD-G** — 作为 **reviewer**，我希望在 Tab 里看到 **完整 MUST 表与 TST/IMPL 条目**，以便不必来回开十个 md 也能审 spec。
- **PRD-H** — 作为 **feature owner**，我希望 HTML **排版更好读**（标题层级、表格、callout），但 **不丢** design 里的 **DSGN-*** / pipeline 的 **PIPE-*** 等锚点内容。
- **PRD-I** — 作为 **agent**，我希望有 **PRD + design + SPEC-HTML-STANDARD**，而不是散落在 spec-pipeline 里一句「rewrite」。

## Functional Requirements

| ID | Requirement |
|---|---|
| **PRD-J** | HTML 汇编 **MUST** 遵循 **DSGN-N** 保真规则（对齐 **DSGN-I**：L1 不删；L2 可压缩表述不可删事实；L3/L4 可摘要但 **MUST link** 到 canonical md） |
| **PRD-K** | **MUST NOT** 将整篇 design/prd 压成一段 overview；若某 Tab 因体量需 **part 文件**，HTML **MUST** 按 part 分 section 或子 Tab，仍保留各 part 的 L1 |
| **PRD-L** | 视觉语言 **SHOULD** 与 initiative 已有 summary HTML 一致（如 `spec-driven-development.html`、sub 的 `document-standard.html`：serif 标题、mono chip、soft callout） |
| **PRD-M** | **spec-pipeline** 在 Converge/Downstream 后或用户要求时 **SHOULD** 触发 reader 更新；agent **MUST** 按 **`skills/spec-html-standard/SPEC-HTML-STANDARD.md`** 汇编（无 spec-reader skill） |
| **PRD-N** | 发现 HTML 与 md 冲突或 HTML 暴露 spec 错误 → **Detect → Ask human** → 先修 **md** → 再 regenerate HTML（同 **DSGN-G** 精神） |

## Non-Functional Requirements

- **PRD-O** — 单文件 HTML（v0）：无构建步骤也可双击打开；不依赖 MkDocs 服务。
- **PRD-P** — 不含 secrets、不含 `raw/` 机器-only eval 正文（可 link 到路径）。

## Out of Scope

- 替换 `docs/book/` 或 MkDocs 导航。
- 每次 git commit 自动 sync（v0 无 hook 要求）。
- 用 reader HTML 作为 lint/oracle（oracle 仍是 `SPEC-STANDARD.md` 与 committed md）。

## Resources Needed

- 一个静态 HTML 构建脚本 + 一个本地静态服务器;无后端、无数据库。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-03 | Initial aspect PRD；强调禁止过度精简 |
| 2026-11-03 | 实现改为 **spec-html-standard**（SPEC-HTML-STANDARD.md），非 spec-reader skill |
