---
feature: document-standard
type: prd
state: draft
final_date: 2026-11-03
health: active
owner: cicidi
last_verified: 2026-11-24
---

# Document Standard — 给人读的 HTML 页面（PRD）

本篇是 document-standard 的一个分篇 PRD（入口是 [document-standard-prd.md](document-standard-prd.md)），讲「给人读的 HTML 页面」要什么、不要什么。具体规则写在 [reader design](../design/document-standard-design-spec-reader-html.md)（DSGN-N）。生成 HTML 时要遵守的规则摘要在 `skills/spec-html-standard/SPEC-HTML-STANDARD.md`，它只是一份规则文件，不是 skill。术语见 [parent design 的术语表](../../../design/spec-driven-development-design.md#glossary)。

## Overview

spec 的正式版本是已提交的 markdown。但一个 parent feature 往往有很多篇、好几层文档：parent 自己的五篇，加上 `features/<sub>/` 下各个 sub-feature 的文档。人需要一个能一次浏览全部内容的网页，而且不能为了好读就丢掉 spec 里的 MUST 规则、表格的行、编号和 L1 内容。

早期手工写的汇编页删得太多，很多章节只剩几句话，和「spec 要让人读懂」的目标相反。本篇规定要什么、不要什么，细则见 DSGN-N。

## Goals and Success Metrics

| ID | 目标 | 怎么算达到 |
|---|---|---|
| PRD-A | 内容不丢 | 读者在 HTML 里看到的 L1 内容和 markdown 一样多：MUST 和禁止事项、表格的每一行、带编号的条目、Out of Scope、关键的流程图。不能做成高管摘要 |
| PRD-B | 是排好版的网页，不是 markdown 预览 | 有卡片、提示框、表格，可以有流程图。不能只是把 markdown 原文塞进 `<pre>`，也不能运行时读取 `.md` 文件来显示 |
| PRD-C | parent 和 sub-feature 都覆盖 | parent 的五篇文档，每篇存在的都有一页；每个 `features/<sub>/` 至少收录它的 design，有其他已提交的文档也一并收录。页面都能从左侧目录找到；pipeline 例外，它没有单独的页面，内容收在汇编页里（[ARD-BG](../../../decision-history/spec-driven-development-decision-history.md#ard-bg)、[ARD-BI](../../../decision-history/spec-driven-development-decision-history.md#ard-bi)） |
| PRD-D | 能追溯到原文 | 每一页（或每个大的部分）底部写明 `Canonical: <markdown 路径>`；页面顶部说明：要改 spec 先改 markdown，再重新生成 HTML |
| PRD-E | 位置和命名固定 | parent 的汇编页是 `docs/book/html/<parent>/<parent>-reader.html`；其他页面按它在 `docs/features/` 下的相对路径放在 `docs/book/html/`，扩展名换成 `.html`（[ARD-BF](../../../decision-history/spec-driven-development-decision-history.md#ard-bf)） |
| PRD-F | 能逐步改进 | 最早可以手工维护；之后改用脚本从 markdown 生成。改用脚本以后，本篇和 DSGN-N 仍然是要遵守的规则 |

## User Stories

- **PRD-G**：作为审查的人，我希望在网页里看到完整的 MUST 表和每个 TST、IMPL 条目，不用来回打开十几个 markdown 文件。
- **PRD-H**：作为 feature 的负责人，我希望网页排版更好读（标题层级清楚、有表格和提示框），但不丢 design 里的 DSGN、PIPE 这些编号和它们的内容。
- **PRD-I**：作为 AI，我希望有一份 PRD、一份 design 和一份 `SPEC-HTML-STANDARD.md` 告诉我怎么生成网页，而不是只有一句「重写一下」。

## Functional Requirements

| ID | 需求 |
|---|---|
| PRD-J | 生成 HTML 必须遵守 DSGN-N 的保真规则，和 document-standard 的 DSGN-I 一致：L1 不删；L2 可以写得更短，但不能删掉事实；L3、L4 可以概括，但必须链到原文 |
| PRD-K | 不能把整篇 design 或 PRD 压成一段概述。如果一种文档拆成了多个分篇，网页必须按分篇分开展示，每个分篇的 L1 都保留 |
| PRD-L | 全站视觉风格统一：衬线字体的标题、等宽字体的编号标签、浅色的提示框。这一条是 NICE：做不到只提醒，不算失败（[ARD-BY](../../../decision-history/spec-driven-development-decision-history.md#ard-by)） |
| PRD-M | spec-write 改完 markdown 后，应该提示重新生成网页；用户要求时也重新生成；commit 前必须重新生成（parent ARD-CF）。生成时必须按 `skills/spec-html-standard/SPEC-HTML-STANDARD.md` 做（没有单独的 reader skill） |
| PRD-N | 如果发现 HTML 和 markdown 说法不一致，或者 HTML 暴露出 spec 本身的错误：先报告并问人，先改 markdown，再重新生成 HTML（和 DSGN-G 的原则一样） |

## Non-Functional Requirements

- **PRD-O**：纯静态网页，阅读时不需要服务器，用浏览器直接打开文件就能看；发布时由 CI 生成（parent 的 ARD-CD），不依赖 MkDocs（一种把 markdown 生成网站的工具）的服务。
- **PRD-P**：页面里不能有密钥，也不能有 `raw/` 里给机器用的评测原文；需要的话只放路径链接。

## Out of Scope

- 替代 book 摘要或 MkDocs 的导航。网页放在 `docs/book/html/`（[ARD-BF](../../../decision-history/spec-driven-development-decision-history.md#ard-bf)）。
- 每次 git commit 自动同步网页。目前不要求 git hook（提交时自动运行的脚本）。
- 拿网页当检查的依据。判断对错仍以 `SPEC-STANDARD.md` 和已提交的 markdown 为准。

## Resources Needed

- 一个生成静态 HTML 的脚本，加一个本地静态文件服务器（可选）。不需要后端，也不需要数据库。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-03 | Initial aspect PRD；强调禁止过度精简 |
| 2026-11-03 | 实现改为 **spec-html-standard**（SPEC-HTML-STANDARD.md），非 spec-reader skill |
| 2026-11-07 | PRD-E：HTML 放到 docs/book/html/，按 feature 树建目录（ARD-BF） |
| 2026-11-20 | 从「单文件、按 Tab 浏览」改为全站左侧目录（PRD-C，ARD-BG、ARD-BI）；PRD-L 不再引用已删除的旧 HTML；PRD-M 由 spec-write 提示重新生成，不再由 spec-pipeline 触发（ARD-AJ）；PRD-O 改为静态网页；Overview 改正 reader 路径；全文改写为完整句子（ARD-BK） |
| 2026-11-20 | 第 1 轮审查后：链回新的入口文件 document-standard-prd.md（ARD-BQ）；PRD-C 写明 pipeline 没有单独页面（ARD-BI） |
| 2026-11-20 | 第 2 轮审查后：PRD-L 降为 NICE（ARD-BY）；MkDocs、git hook 第一次出现时解释 |
| 2026-11-24 | PRD-O：阅读时不需要服务器，发布由 CI 生成（ARD-CD） |
| 2026-11-24 | 第 14 轮审查后：PRD-M 加 commit 前必须重建（parent ARD-CF） |
