---
feature: english-grammar-fix
type: prd
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# english-grammar-fix — 需求

本篇从过去的对话和提交记录里，整理用户对 `english-grammar-fix` 这个 skill 的需求。
实现见 [design](../design/english-grammar-fix-design.md)。
决策的来由见 [decision-history](../decision-history/english-grammar-fix-decision-history.md)。
opencode 会话存在本机 opencode.db，下文按会话 id 前缀引用。
Claude Code 的输入记录在 `~/.claude/history.jsonl`，按会话 id 前 8 位引用。

## Overview

`english-grammar-fix` 帮英语不是母语的用户，修正 AI 写出的英文里的小语法错误。
适用的文字有代码注释、commit message、PR 描述和文档（SKILL.md 开头一段）。
它最早叫 `auto-patches`，2026-03-30 随 ai-coworker 的第一个提交出现（walter-worker commit c3f771f）。
当天用户在 Claude Code 里手动调用过一次 `/dev-ai-tool-auto-patches`（会话 e6c678f2）。
最初提出这个需求的那段对话没有找到，属于 UNKNOWN。

## Goals and Success Metrics

目标：AI 写出的英文没有明显的语法小错，用户不必逐句检查（SKILL.md 的 description）。
成功指标：UNKNOWN。对话和提交里都没有给出可量化的指标。

## User Stories

- 作为英语不是母语的开发者，我想让 AI 写的 commit message、PR 描述和文档先过一遍语法检查再发布。
- 作为开发者，我想让语法小错直接改掉，措辞上的改动先给我看，由我决定。

## Functional Requirements

**PRD-A 修正 AI 写的英文小错。** 首版的 description 是
"Auto-correct minor English grammar errors in AI responses for non-native speakers"（c3f771f）。
2026-11-24 起 description 改为写明只能手动调用（ARD-G）。
范围是语法和措辞，不改写内容本身。
"for non-native speakers" 是否也包括修正用户自己写的英文，属于 UNKNOWN，见 design 的 QUES-B。

**PRD-B 语法静默改，风格先给人看。** 首版写明：语法小错直接改，不加说明（c3f771f 的 How It Works 一节）。
措辞和句子结构这类风格改动，用斜体显示并附上原文，供用户审阅（同一节）。
同一提交的 ai-coworker 蓝图却写"Minor in italics"，两处说法不一致，见 design 的 QUES-E。

**PRD-C 不碰术语和代码名。** 技术术语、变量名和函数名、故意写得简短的注释、正确但口语化的表达，都不改。
出处：c3f771f 的 What It Does NOT Change 一节，至今未变。

**PRD-D commit message 的写法。** 用祈使语气，如 "Add feature" 而不是 "Added feature"。
格式用 Conventional Commits，即 `type(scope): description`；标题不超过 72 个字符（c3f771f）。

**PRD-E 由用户手动触发。** 首版写的是对一段文字手动运行 `/auto-patches`，
或在发布前用于 commit message、PR 描述和文档（c3f771f 的 Trigger 一节）。
2026-03-30 用户手动调用过一次（会话 e6c678f2）。之后的对话里没有找到再次调用的记录。

**PRD-F 名字直接说明用途。** 2026-06-23 的批量改名把 `auto-patches` 改成 `self-patch`（ses_1417bab9，skill-factory commit 3395648）。
约一小时后用户说"self-patch 改名english-grammar-fix"（同一会话；commit 7226d53、c329159）。
用户没有说理由，属于 UNKNOWN。

## Out of Scope

不改代码，只改英文文字（PRD-C）。用户想自己审阅时，不用本 skill（SKILL.md 的 When NOT to Use 一节）。
这一节由 agent 在 2026-06-24 的全面检查里补写（ses_107972d8，commit cca25cd），不是用户逐字提出的。

## Resources Needed

不需要外部服务或 API key，只用当前对话里的 LLM。
人力上，风格类改动需要用户逐条确认（PRD-B）。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：从过去的对话和提交记录反推 english-grammar-fix 的 PRD |
| 2026-11-24 | PRD-A 补充 description 的改动（ARD-G） |
