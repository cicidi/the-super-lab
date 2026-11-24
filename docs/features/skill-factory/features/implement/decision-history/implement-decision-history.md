---
feature: implement
type: decision-history
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# implement — 决策记录

本篇按时间倒序记录 `implement` 这个 skill 的关键决策。
需求见 [PRD](../prd/implement-prd.md)，设计见 [design](../design/implement-design.md)。
skill-factory 层面的旧决策在 [parent decision history](../../../decision-history/skill-factory-decision-history.md)。
会话按 `~/.claude/history.jsonl` 里的 id 前缀和时间引用。

## Decision Log

| ID | Date | Decision |
|---|---|---|
| ARD-A | 2026-09-25 | 加一节 Skill Dependencies：动手前先判断是行为改动还是实现改动；代码和 spec 冲突时报告证据并问人 |
| ARD-B | 2026-08-02 | 用户把 implement 的替代指定为 auto-tdd；wayfinder 流水线的 build 一步写成 auto-tdd |
| ARD-C | 2026-08-02 | 原样导入 mattpocock 的 implement：正文不改，只加 frontmatter 和作者出处 |
| ~~ARD-D~~ | ~~2026-08-02~~ | ~~implement 列为 wayfinder 导入的后续项，这次不导入~~ 已被 [ARD-C](#ard-c) 取代 |
| ARD-E | 2026-08-02 | 交付前所有代码都要审查：优先用 ai-coworker 的 code review，没有就用 Claude 自带的 |

## Evidence Appendix

### ARD-A

理由：commit f67df5b 把三处"代码是唯一事实来源"改成按关注点分权威：想要的行为以 spec 为准，当前实现以代码为准。
同一提交给 to-spec、implement 和 doc-review 都加了 Skill Dependencies 一节（PRD-F、PRD-G）。
被否决的方案：代码是唯一事实来源，冲突时以代码为准改 spec（commit f67df5b 的说明）。
出处：commit f67df5b；会话 631b8662（2026-09-25 08:58 贴入长文，原文没有保留，属于 UNKNOWN）。

### ARD-B

理由：用户要求 matt 的 skill 都是接口，可以换成自己的实现（PRD-D）；对 implement 说"implement 我的替代是auto-tdd"（d8d2da7f，18:37）。
被否决的方案：流水线的 build 一步用 matt 的 implement。
出处：d8d2da7f（17:22 第 4 条，18:37）；commit 43cb1ef（18:39）给 wayfinder 加了以 auto-tdd 结尾的流水线图。
implement 本身没有删，也没有改成转调 auto-tdd；这是有意保留还是遗漏，属于 UNKNOWN，见 design 的 QUES-D。

### ARD-C

理由：用户要求注明作者（PRD-B），没有替换的接口"就用matt 的ksill"（PRD-C）。
被否决的方案：像 wayfinder 那样改写正文；wayfinder 改了术语和接口，implement 没有改。
出处：commit 12c7dce（18:36，加入 `source_author` 和 `source_url`）；d8d2da7f（17:22 第 1 条，17:27 第 4 条）。
正文后来只多了 ARD-A 那一节，原有五句至今未改（2026-11-24 对照 12c7dce 核对）。

### ARD-D

理由：wayfinder 的导入规格只导入 wayfinder 直接依赖的四个 skill，把"to-spec、to-tickets、implement"列为后续导入。
被否决的方案：一次导入整条流水线。出处：commit 0f3ede7（18:21）的 wayfinder-import-spec，Out of Scope 一节。
13 分钟后（18:34）用户接着导入 to-spec 和 to-tickets，implement 随即导入（PRD-A），本决策被 ARD-C 取代。

### ARD-E

理由：用户说"每次delivery 以前，所有的代码都需要review 以下"，代码用 ai-coworker 的 code review，没有实现就用 Claude 自带的（PRD-E）。
wayfinder 据此在 task 类 brief 关闭前加了 Delivery Review Gate：代码文件交给 `matt-code-review`（skills/wayfinder/SKILL.md）。
被否决的方案：交付不经审查。出处：d8d2da7f（17:27 第 7 条）。
implement 正文写的是 `/code-review`，没有点名 `matt-code-review`，见 design 的 QUES-C。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：从过去的对话和提交记录反推 implement 的决策 |
