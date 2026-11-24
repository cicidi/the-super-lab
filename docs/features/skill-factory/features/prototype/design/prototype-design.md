---
feature: prototype
type: design
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# prototype — 用完就扔的原型

本篇说明 `prototype` 这个 skill 现在怎么工作。源文件：`skills/prototype/SKILL.md`。
commit 78242fa 导入，8d451059 和 93d4a4a 移到现在的位置，之后内容没有改过。

## Problem Statement

有些设计问题在纸上想不清，例如状态机遇到少见的情况会怎么走，或者页面该长什么样。
wayfinder 定方向时，需要一种能做出具体东西、让人看了再判断的 brief（PRD-A、PRD-E）。

## Solution

一个只有 SKILL.md 的 skill：先判断问题属于逻辑还是 UI，再按六条共同规则做原型（PRD-C）。
它常由 wayfinder 的 prototype brief 调起，也可以单独使用（PRD-D）。

## User Stories

- 作为开发者，我想验证一个状态模型时，得到一个能在终端里一步步推动它的小程序。
- 作为开发者，我想决定页面样式时，在同一个页面上切换几种差别很大的方案。
- 作为后来的读者，我想在 issue 或提交里查到原型回答了什么问题、结论是什么。

## Implementation Decisions

全部行为写在 SKILL.md 里，没有脚本。正文与原版一致，本仓库只改了 frontmatter（PRD-B、PRD-C）。
SKILL.md 用相对链接指向 `LOGIC.md` 和 `UI.md`，但这两个文件没有导入，目录里只有 SKILL.md（decision-history 的 ARD-B）。

## Design

**DSGN-A 选分支。** 从用户的话和周围的代码判断问题类型；用户在场就直接问（PRD-E）。
问题含糊又问不到人时，后端模块走逻辑分支，页面或组件走 UI 分支，并把这个假设写在原型开头。

**DSGN-B 逻辑分支。** 回答"这个逻辑或状态模型对不对"。做一个很小的交互式终端程序，把状态机推过纸上难想清的情况。
细节本应写在 `LOGIC.md`，该文件缺失，见 QUES-A（PRD-C）。

**DSGN-C UI 分支。** 回答"这个应该长什么样"。在同一个路由上生成几种差别很大的 UI 变体。
用 URL 查询参数和页面底部的浮动切换条来切换变体。细节本应写在 `UI.md`，该文件缺失，见 QUES-A。

**DSGN-D 就近放置，一眼可辨。** 原型代码放在它服务的模块或页面旁边，名字要让人看出是原型（PRD-C）。
UI 路由沿用项目现有的路由约定，不新造顶层目录。

**DSGN-E 一条命令运行。** 用项目已有的任务命令，例如 `pnpm <name>` 或 `python <path>`，用户不用思考就能启动（PRD-E）。

**DSGN-F 默认不持久化。** 状态只放内存。问题本身涉及数据库时，用临时库或本地文件，名字写明"PROTOTYPE — wipe me"。
持久化正是原型要检验的东西，不该成为它的依赖（PRD-C）。

**DSGN-G 不打磨。** 不写测试，不做超出"能跑"所需的错误处理，不做抽象。目的是尽快学到东西（PRD-C）。

**DSGN-H 展示状态。** 逻辑分支每做一步、UI 分支每切一次变体，都打印或渲染全部相关状态，让用户看到变了什么（PRD-E）。

**DSGN-I 收尾留档。** 把验证过的决定并入正式代码；原型本身提交到一个临时分支，不进主分支（PRD-C）。
在实现 issue 上留一个指向该分支的链接，把结论和它回答的问题写进 issue 或提交。主分支只留结论。

**DSGN-J 在 wayfinder 里的位置。** wayfinder 的 prototype 接口默认用本 skill，安装时可换成别的实现（PRD-A、PRD-D）。
prototype brief 属于 HITL；它的产出是决定而不是交付物，所以跳过 wayfinder 的交付前审查（skills/wayfinder/SKILL.md），见 QUES-B。

**DSGN-K 出处与安装。** frontmatter 写有 `source_author: mattpocock` 和原文链接（PRD-B）。
`compatibility` 字段声明支持 Claude Code 和 OpenCode（PRD-F）。

## Testing Decisions

本 skill 没有自动测试或评测集。
导入时的测试计划只查 frontmatter、出处和正文是否原样（wayfinder-import-test-plan 的 TC-01 到 TC-03、TC-05）。
有记录的真实使用只有一次，在 2026-11-05（会话 1afe4b90）：agent 去读 `UI.md` 时发现文件不存在，只能按 SKILL.md 的概述做。

## Out of Scope

答案在文档里已经清楚，或直接写正式代码更快时，不用本 skill（SKILL.md 的 `when_not_to_use`）。
原型不写测试，也不追求能上线（DSGN-G）。

## Further Notes

需求见 [PRD](../prd/prototype-prd.md)，决策见 [decision-history](../decision-history/prototype-decision-history.md)。
2026-11-05 用户说"干净整洁 易读给我整5个styple 选一个"，agent 用本 skill 做了 5 种样式的对比页（1afe4b90）。
用户随后改要 Google Cloud 文档风格；对比页 proto-clean-styles.html 按用户的提交范围留在本地，没有提交（~/.coworker/memory 的 commit scope 一条）。

## Alternatives Considered

自己从头写原型 skill：被否决，直接导入 Matt Pocock 的版本（ARD-E）。
像 wayfinder 那样改写正文：被否决，只改 frontmatter（ARD-C）。
在 wayfinder 里写死 skill 名字：被否决，做成可替换的接口（ARD-D）。

## Drawbacks

两个分支的细节文件缺失，agent 只能凭 SKILL.md 的一句概述来做，结果因模型而异（QUES-A）。
DSGN-I 要求开临时分支，但 2026-11-05 的原型页实际留在本地、没有提交，两者不一致（QUES-C）。

## Risks and Mitigations

| 风险 | 缓解 |
|---|---|
| 原型代码被当成正式代码合进主分支 | 名字标明是原型；收尾时只把结论并入主分支（DSGN-D、DSGN-I） |
| 原型用的临时数据被当真 | 默认不持久化；必须用库时名字写明 wipe me（DSGN-F） |
| 上游更新了 LOGIC.md、UI.md，本地不知道 | 目前没有同步机制，见 QUES-A |

## Open Questions

| ID | 问题 | 目前答案 | Owner | Blocking |
|---|---|---|---|---|
| QUES-A | 要不要补导上游的 `LOGIC.md`、`UI.md` 和 `agents/` 目录？ | 导入时只取了 SKILL.md；上游三者都在（gh api，2026-11-24） | cicidi | no |
| QUES-B | prototype brief 要不要过交付前审查？ | wayfinder 让它跳过；用户原话是"所有的代码都需要review"（d8d2da7f，17:27） | cicidi | no |
| QUES-C | 收尾时原型放临时分支，还是留在本地不提交？ | SKILL.md 要求临时分支；2026-11-05 的原型页留在本地未提交 | cicidi | no |
| QUES-D | 支持 OpenCode 是用户的要求吗？ | 只见于导入规格，用户原话没有找到（PRD-F） | cicidi | no |

## Reversibility

所有改动都落在 git 跟踪的 `skills/prototype/SKILL.md`，用 `git revert` 即可撤回。
原版可从 `source_url` 重新取回。已安装到 `~/.claude/skills/` 的副本，须重跑 `install.sh` 才同步。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：按 SKILL.md 写出 prototype 的 design，引用 PRD-A 到 PRD-F |
