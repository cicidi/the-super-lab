---
feature: doc-protect
type: prd
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# doc-protect — 需求

本篇从过去的对话和提交记录里，整理用户对 `doc-protect` 这个 skill 的需求。
实现见 [design](../design/doc-protect-design.md)。
决策的来由见 [decision-history](../decision-history/doc-protect-decision-history.md)。
opencode 会话存在本机 opencode.db，下文按会话 id 前缀引用。

## Overview

受保护块（PROTECTED 块）指文档里用两行 HTML 注释包起来的一段内容，AI 不得改动。
`doc-protect` 帮用户给文档加上或去掉这种标记。
这套做法最早见于 2026-03-30 walter-worker 的首个提交（c3f771f），当时叫 doc-protection。
提出它的那段对话没有找到，属于 UNKNOWN。
2026-06-11 用户把它迁到 skill factory，归为个人 skill（ses_14a669c2）。

## Goals and Success Metrics

目标一：人写下的关键决定，不被 AI 在编辑或合并时悄悄改掉（c3f771f 原版 skill 的开头）。
目标二：加保护和解除保护都留下 git 提交，便于追溯（同上）。
成功指标：UNKNOWN。没有找到量化指标；SKILL.md 的两条 MUST 质量门见 design 的 DSGN-E。

## User Stories

- 作为文档作者，我想锁住一段内容，让 AI 以后只读不改。
- 作为文档作者，我想在需要时亲自解锁，AI 不能自己解锁。
- 作为文档作者，我希望 AI 看到关键内容时提醒我加保护，但不擅自加。

## Functional Requirements

**PRD-A 用成对的标记包住受保护内容。** 开始标记是 `<!-- PROTECTED -->`，结束标记是 `<!-- END PROTECTED -->`。
证据：walter-worker c3f771f 的原版 skill；本仓库 a5dcc4e 原样保留。用户提出这种格式的对话属于 UNKNOWN。

**PRD-B AI 不改、不移、不删、不重排块内内容。** AI 可以读块内内容作参考，也可以在块外加新内容（c3f771f）。

**PRD-C 只有人能解除保护。** 用户明确说"unprotect this section"时，才去掉标记（c3f771f）。

**PRD-D 加保护和解除保护各提交一次。** 提交信息是 `docs: protect {section name}` 和 `docs: unprotect {section name}`（c3f771f）。
2026-11-24 起，提交前先给用户看 diff，用户同意才提交（ARD-G）。

**PRD-E AI 可以建议加保护，但不能擅自加。** 适合保护的有 PRD 需求、架构决定、法律条款、安全策略（c3f771f）。
原版还列了团队约定和 SLA（服务等级协议），a5dcc4e 迁移时删去，原因 UNKNOWN。

**PRD-F 迁到 skill factory 的个人目录。** 用户指定 `coworker-meta-doc-protection.md -> personal/ai-coworker-doc-protect`。
出处：ses_14a669c2（2026-06-11）；迁移见 commit a5dcc4e。

**PRD-G 用 skill create 新建，不直接搬文件。** 用户说旧项目里的 skill "只是提供idea"（ses_14a669c2，2026-06-11）。
实际 a5dcc4e 的内容与原版几乎一致，见 design 的 QUES-D。

**PRD-H 名字要简短好记。** 用户问"这些命名 合理吗"，要求按讨论好的简化命名迁移（ses_1417bab9，2026-06-23）。
commit 3395648 去掉 `ai-coworker-` 前缀，改名为 `doc-protect`。

## Out of Scope

可以自由编辑的内容、不需要长期保护的临时笔记，都不用本 skill（SKILL.md 的 When NOT to Use 一节）。
对话里没找到用户划这条范围的原话，出处属于 UNKNOWN。

## Resources Needed

只需要 git 和一个能编辑文本的 agent，不调用模型 API。
人力上，用户决定保护哪一段，并亲自要求解除（PRD-C）。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：从过去的对话和提交记录反推 doc-protect 的 PRD |
| 2026-11-24 | PRD-D 补充提交前询问（ARD-G） |
