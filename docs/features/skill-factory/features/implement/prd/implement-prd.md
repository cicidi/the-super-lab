---
feature: implement
type: prd
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# implement — 需求

本篇从过去的对话和提交记录里，整理用户对 `implement` 这个 skill 的需求。
实现见 [design](../design/implement-design.md)。
决策的来由见 [decision-history](../decision-history/implement-decision-history.md)。
Claude Code 会话原文没有保留；下文引用 `~/.claude/history.jsonl` 里的会话 id 前缀和时间。

## Overview

`implement` 让 agent 按已经写好的 spec 或 ticket 写代码。
spec 是需求和设计文档；ticket 是拆好的一张张执行工单。
做法是测试先行，边做边跑类型检查和测试，做完先做代码审查，再提交。
这个 skill 来自 Matt Pocock 的 mattpocock/skills，于 2026-08-02 导入（commit 12c7dce）。
导入发生在会话 d8d2da7f：用户当天先学习 wayfinder，再依次导入 to-spec、to-tickets 和 implement（18:34 到 18:36）。
导入一分钟后，用户说"implement 我的替代是auto-tdd"（18:37），见 PRD-D。

## Goals and Success Metrics

目标一：补齐 wayfinder 流水线的最后一步，把定好的 spec 和 ticket 变成代码（d8d2da7f，2026-08-02）。
目标二：沿用原作者的做法，并注明出处（同一会话 17:22 的第 1 条）。
目标三：写代码时不让 spec 和代码悄悄走偏（commit f67df5b，2026-09-25）。
成功指标：UNKNOWN。对话和提交里都没有可量化的指标。

## User Stories

- 作为开发者，spec 和 ticket 都定好后，我想让 agent 把代码写完、测完、审完。
- 作为开发者，我想在交付前让所有代码都经过审查。
- 作为 skill 仓库的维护者，我想看出这个 skill 来自谁，原文在哪里。
- 作为维护者，代码和 spec 不一致时，我想被告知，而不是被悄悄改掉一边。

## Functional Requirements

**PRD-A 作为 wayfinder 流水线的一环导入。** wayfinder 的导入规格先把 implement 列为"future imports"（commit 0f3ede7，18:21）。
随后用户说"continue importing to-spec"（18:34）和"continue with to-tickets"（18:35），commit 12c7dce 在 18:36 导入 implement。
要求导入 implement 的那句原话没有找到，属于 UNKNOWN。

**PRD-B 注明原作者。** 用户要求的第 1 条是"import 这个skill 著名作者"，即注明作者（d8d2da7f，17:22）。
commit 12c7dce 在 frontmatter 里写了 `source_author` 和 `source_url` 两个字段。
frontmatter 是 SKILL.md 开头两条 `---` 之间的元数据，记录名字、描述和触发词。

**PRD-C 沿用原版正文。** 用户说接口没有替换时"就用matt 的ksill"（d8d2da7f，17:27）。
12c7dce 导入的正文只有五句：按 spec 或 ticket 实现，用 /tdd，跑类型检查和测试，用 /code-review 审查，提交。
这五句是原作者的做法，用户没有逐条提出过。

**PRD-D 用户自己的替代是 auto-tdd。** 用户要求 wayfinder 用到的 skill 都是接口，"我自己要能提供impl 替代"（d8d2da7f，17:22）。
对 implement，用户说"implement 我的替代是auto-tdd"（同一会话 18:37）。
两分钟后，commit 43cb1ef 把 wayfinder 流水线的 build 一步写成 auto-tdd。
2026-11-24 起，implement 保留，TDD 一步转调 auto-tdd，见 design 的 DSGN-C 和 ARD-F。

**PRD-E 交付前所有代码都要审查。** 用户原话："每次delivery 以前，所有的代码都需要review 以下"（d8d2da7f，17:27 第 7 条）。
代码审查用 ai-coworker 自己的 code review；"如果没有实现， code review 用claude 自带的"（同一条）。
2026-11-24 起，SKILL.md 先用 `/matt-code-review`，没装再用通用的 `/code-review`（ARD-G）。

**PRD-F 先判断改动类型，再决定改不改 spec。** 行为改动指外部能看到的行为变了；实现改动指重构、改名、内部优化、换框架。
前者要改 spec，后者不用（commit f67df5b，2026-09-25）。
这一节加在会话 631b8662 里：用户用"skill edit doc-organize"贴入一份长文（2026-09-25 08:58）。贴入原文没有保留，用户原话属于 UNKNOWN。

**PRD-G 代码和 spec 冲突时，先报告再问。** 不悄悄改任何一边；先列出两边的证据，再问用户（commit f67df5b）。
出处同 PRD-F，用户原话属于 UNKNOWN。

## Out of Scope

spec 还含糊、决定还没做完时不用本 skill，先用 wayfinder 或 grill-with-docs；没有 ticket 可依据时也不用。
这条写在 SKILL.md 的 `when_not_to_use` 字段，由导入时写入（commit 12c7dce）；用户划这条范围的原话没有找到，属于 UNKNOWN。

## Resources Needed

被实现的项目要有类型检查和测试命令，能单独跑一个测试文件，也能跑全量（PRD-C）。
还需要能调用的 TDD skill 和代码审查 skill（PRD-C、PRD-E）：现在是 auto-tdd 和 matt-code-review（ARD-F、ARD-G）。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：从过去的对话和提交记录反推 implement 的 PRD |
| 2026-11-24 | PRD-D、PRD-E 和资源一节改为当前行为（ARD-F、ARD-G） |
