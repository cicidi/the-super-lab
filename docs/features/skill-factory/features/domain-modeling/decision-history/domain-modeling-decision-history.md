---
feature: domain-modeling
type: decision-history
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# domain-modeling — 决策记录

本篇按时间倒序记录 `domain-modeling` 这个 skill 的关键决策。
需求见 [PRD](../prd/domain-modeling-prd.md)，设计见 [design](../design/domain-modeling-design.md)。
skill-factory 层面的旧决策在 [parent decision history](../../../decision-history/skill-factory-decision-history.md)。
Claude Code 会话按 `~/.claude/history.jsonl` 里的会话 id 前缀引用；会话原文没有保留。

## Decision Log

| ID | Date | Decision |
|---|---|---|
| ARD-A | 2026-08-02 | 和其他 skill 一起从 `import-skills/` 移到 `skills/domain-modeling/` |
| ARD-B | 2026-08-02 | 正文和两个模板原样导入，只改 frontmatter，并写上原作者和原文链接 |
| ARD-C | 2026-08-02 | 作为 wayfinder 的 interview 接口默认实现，和 grill-with-docs 搭配；用户可换成自己的实现 |
| ARD-D | 2026-08-02 | 直接导入 Matt Pocock 的版本，不自己从头写 |

## Evidence Appendix

### ARD-A

理由：commit 93d4a4a 把所有 skill 收进同一个 `skills/` 目录，domain-modeling 只是其中之一。
被否决的方案：保留单独的 `import-skills/` 目录。这次移动的讨论没有找到，理由属于 UNKNOWN。
出处：commit 93d4a4a；之前的 commit 8d451059 先把 import-skills 并入根目录。

### ARD-B

理由：用户要求注明作者（PRD-B），没有替换的接口"就用matt 的skill"（PRD-C）。
导入规格把这一条写成 Body preservation：grill-with-docs、domain-modeling、prototype 只改 frontmatter。
被否决的方案：像 wayfinder 那样改写正文。wayfinder 改了术语和接口，domain-modeling 没有改。
出处：d8d2da7f（2026-08-02 17:22、17:27）；commit f6255af；wayfinder-import-spec（commit 0f3ede7）。

### ARD-C

理由：用户要求 wayfinder 用到的 skill 都做成接口，安装时问用户，没给替换就用 matt 的（PRD-D）。
用户只说"对于ai -cowork 我有自己的research"，没有提 interview 的替代，所以默认值是 grill-with-docs 加 domain-modeling。
被否决的方案：在 wayfinder 里写死 skill 名字。
出处：d8d2da7f（17:22 第 4 条，17:27 第 4 条）；skills/wayfinder/SKILL.md 的接口表。

### ARD-D

理由：用户读完 wayfinder 及其依赖后说"这个wayfind 大部分我是同意的。 我也想使用"（d8d2da7f，17:22）。
导入前用户问过 domain-modeling 做什么、glossary 怎么维护、定义由谁给（同一会话 10:19 到 10:25）。
被否决的方案：自己写一个术语表 skill。助手当时怎么回答的没有保留，用户为何满意属于 UNKNOWN。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：从过去的对话和提交记录反推 domain-modeling 的决策 |
