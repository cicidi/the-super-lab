---
feature: bug
type: prd
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# bug — 需求

本篇从过去的对话和提交记录里，整理用户对 `bug` 这个 skill 的需求。
实现见 [design](../design/bug-design.md)。
决策的来由见 [decision-history](../decision-history/bug-decision-history.md)。
opencode 会话存在本机 opencode.db，下文按会话 id 前缀引用。

## Overview

`bug` 管一个 bug 从发现到预防的全过程，分三条分支。
Hunt 指找出并修好 bug 的根因（root cause，问题最初的源头）。
Report 指把问题写成 GitHub issue。Heal 指记下用户对 AI 的纠正，再从中总结预防规则。
它由四个旧 skill 合成：bug-hunt、bug-report、self-heal、self-analyze（commit 6086424，2026-08-02）。
Heal 的起因：用户问 self-heal 和 self-analyze"为什么之前我从来没见claude code 调用过他们"（ses_1417bab9，2026-06-23）。

## Goals and Success Metrics

目标一：debug 时先收集证据再推理，不靠猜（ses_1417bab9，2026-06-23）。
目标二：同一类错误不再重犯，纠正要被记下并变成规则（同一会话）。
目标三：任何 GitHub 仓库的问题，都能从同一个入口提 issue（同一会话）。
成功指标：UNKNOWN。对话里没有给出可量化的指标。

## User Stories

- 作为开发者，遇到报错时，我想让 agent 先收集证据、列出假设，再动手修。
- 作为开发者，生产出事又不知道原因时，我想让 agent 按时间线深挖。
- 作为开发者，我想把问题提到我选定的 GitHub 仓库，而不只是 walter-worker。
- 作为用户，我纠正过 AI 的事，希望它记住；同类纠正重复出现时，变成规则。

## Functional Requirements

**PRD-A 一个 skill，三条分支，先问再分。** 开始只问用户一个问题：Hunt、Report 还是 Heal。
证据：commit 6086424 把四个 skill 合成 `bug`；parent design 合并表的 `/bug` 一行。
提出这次合并的那段对话没有找到，属于 UNKNOWN。

**PRD-B Hunt 按假设驱动，不猜。** 先列 3 到 5 个可能的根因，逐个用最小测试验证，确认了才修。
这一做法来自 2026-06-23 从 ai-coworker IDE 规则迁来的 bug-hunt（commit 3395648）。
迁移是用户要求的："其他的都迁移到skill factory"（ses_1417bab9，2026-06-23）。

**PRD-C 先收集，后推理。** 用户原话："收集所有信息，只要可能相关的，先不分析"。
第二步是"推理，并列证据， 不管是log ，代码，还是message"（ses_1417bab9，2026-06-23）。
落地为 walter-worker commit f8b7ffb；2026-11-24 已恢复，见 decision-history 的 ARD-K。

**PRD-D 原因不明时深挖。** bug-sleuth 管"出事不知道原因"的深入追查，bug-hunt 管已知的代码 bug。
用户听完两者的区别后说"合并"（ses_1417bab9，2026-06-23；walter-worker commit af88df6）。
2026-11-24 已恢复深挖模式，见 decision-history 的 ARD-K。

**PRD-E Report 只留一个提 issue 的入口。** 用户说"bug-create 和bug-report 重复了， merge成一个"。
出处：ses_1417bab9（2026-06-23）；walter-worker commit 4285718。

**PRD-F Report 面向所有 GitHub 仓库。** 用户原话："bug report 应该是通过对于所有github"（ses_1417bab9，2026-06-23）。
落地为 walter-worker commit 6511f37：先列项目目录（project catalog）里的仓库让用户选。
2026-11-24 起默认当前仓库，提交前请用户确认，见 decision-history 的 ARD-L。

**PRD-G Heal 把纠正记成 trace。** trace 指一条纠正记录。
数据存在当前项目的 `.self-healing/traces/{date}.yaml`（ses_1417bab9，2026-06-23）。

**PRD-H 触发时检查 hook。** hook 指 IDE 在固定时机自动运行的脚本。
用户要求两个 skill"trigger 的时候都默认检查有没有hook"，没有就提示用户安装（ses_1417bab9，2026-06-23）。
用户补充：hook 是全局的，Claude Code 和 OpenCode 都要装；数据是项目级的（同一会话）。
2026-11-24 起 Heal 先检查并告诉用户；要不要注册仍待用户决定，见 design 的 QUES-D。

**PRD-I 分析结果写进项目的 CLAUDE.md。** 用户要求 self-analyze"分析当前project 下面的trace 然后总结"。
总结要"放到当前project level 的claude.md"（ses_1417bab9，2026-06-23）。

**PRD-J 放在 skill 仓库，不放 personal。** 用户说"这个self healing move 到skill-factory/ai-coworker-skill factory 里面"。
又问"self analyze 和heal 怎么还在personal folder 里面"，随后 commit bd9bb02 从 personal-skills 删除（2026-06-23）。
现在这个 skill 位于本仓库的 `skills/bug/`（commit 93d4a4a）。

## Out of Scope

功能需求、代码评审和一般性提问，都不用本 skill（SKILL.md 的 When NOT to Use 一节）。
对话里没找到用户划这条范围的原话，出处属于 UNKNOWN。

## Resources Needed

Report 需要已登录的 `gh` 命令行，以及目标仓库的写权限（PRD-F）。
Heal 需要在 Claude Code 和 OpenCode 里各装一个全局 hook（PRD-H）。
人力上，用户开始时选一次分支（PRD-A）。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：从过去的对话和提交记录反推 bug 的 PRD |
| 2026-11-24 | PRD-C、D、F、H 的现状句改为已恢复（ARD-K、ARD-L、ARD-M） |
