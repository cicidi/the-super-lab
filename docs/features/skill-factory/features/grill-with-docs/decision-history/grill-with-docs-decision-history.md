---
feature: grill-with-docs
type: decision-history
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# grill-with-docs — 决策记录

本篇按时间倒序记录 `grill-with-docs` 这个 skill 的关键决策。
需求见 [PRD](../prd/grill-with-docs-prd.md)，设计见 [design](../design/grill-with-docs-design.md)。
Claude Code 会话按 `~/.claude/history.jsonl` 里的会话 id 前缀引用；会话原文没有保留。

## Decision Log

| ID | Date | Decision |
|---|---|---|
| ARD-H | 2026-11-24 | 加 `disable-model-invocation: true`，只能由用户手动调用；wayfinder 的 interview 改为直接用 grilling 加 domain-modeling |
| ARD-G | 2026-11-24 | 补导上游 commit fa460cb 版的 `/grilling` 到 `skills/grilling/`，正文原样 |
| ARD-A | 2026-11-04 | SDD 流程把 grill-with-docs 列为 Map 阶段可选的压力测试，评测矩阵加 grill-docs 一行 |
| ARD-B | 2026-08-02 | 和其他 skill 一起从 `import-skills/` 移到 `skills/grill-with-docs/` |
| ~~ARD-C~~ | ~~2026-08-02~~ | ~~只导入 grill-with-docs 本身，不导入它调用的 `/grilling`~~ 已被 [ARD-G](#ard-g) 取代 |
| ARD-D | 2026-08-02 | 正文原样导入，只改 frontmatter，并写上原作者和原文链接 |
| ARD-E | 2026-08-02 | 和 domain-modeling 一起作为 wayfinder 的 interview 接口默认实现；用户可换成自己的实现 |
| ARD-F | 2026-08-02 | 直接导入 Matt Pocock 的版本，不自己从头写 |

## Evidence Appendix

### ARD-H

理由：与上游一致。上游写明设了这一项后别的 skill 也调不到它，所以 wayfinder 改成和上游一样直接调用两个 skill。
被否决：保持 agent 可自行触发。出处：用户 2026-11-24（会话 80291c19）"其他几个按照你说的修"。

### ARD-A

理由：SDD 的 PRD-H 要求每一步优先用已流行的 skill；其 ARD-L（2026-10-30）定下盲区由现有 skill 发现，点名 grill-with-docs。
SDD（spec-driven development）流程的 Map 阶段指写 spec 前的访谈；grill-with-docs 在这里是可选的压力测试。
被否决的方案：为发现盲区专门新建一个 skill（SDD ARD-L）。
出处：commit 7bacc64（skills/spec-pipeline/INTEGRATIONS.md）；commit 2eaa42d（skills/spec-organize/tests/eval/TST-J-MATRIX.md）。
SDD 决策见 docs/features/spec-driven-development/decision-history/spec-driven-development-decision-history.md。

### ARD-B

理由：commit 93d4a4a 把所有 skill 收进同一个 `skills/` 目录，grill-with-docs 只是其中之一。
被否决的方案：保留单独的 `import-skills/` 目录。这次移动的讨论没有找到，理由属于 UNKNOWN。
出处：commit 93d4a4a；之前的 commit 8d451059 先把 import-skills 并入根目录。

### ARD-C

理由：UNKNOWN。导入规格的 Files to Import 表只列了四个 skill，没有 `/grilling`，也没写为什么不列。
结果是正文调用的 `/grilling` 在 `skills/` 和 `~/.claude/skills/` 下都找不到（2026-11-24 核对）。
上游仓库现在有 `skills/productivity/grilling/SKILL.md`（2026-11-24 查看）；导入当时是否已有，属于 UNKNOWN。
被否决的方案：连同 `/grilling` 一起导入（未见讨论）。
出处：wayfinder-import-spec（commit 0f3ede7）的 Files to Import 表；commit 6835420。

### ARD-D

理由：用户要求注明作者（PRD-B），没有替换的接口"就用matt 的ksill"（PRD-C）。
导入规格把这一条写成 Body preservation：grill-with-docs、domain-modeling、prototype 只改 frontmatter。
被否决的方案：像 wayfinder 那样改写正文。
出处：d8d2da7f（2026-08-02 17:22、17:27）；commit 6835420；wayfinder-import-spec（commit 0f3ede7）。
docs/book/imported-skills.md 把导入日期写成 2026-07-25，与 commit 6835420 的 2026-08-02 不符，以 git 为准。

### ARD-E

理由：用户要求 wayfinder 用到的 skill 都做成接口，安装时问用户，没给替换就用 matt 的（PRD-D）。
用户只替换了 research，没有提 interview 的替代，所以默认值是 grill-with-docs 加 domain-modeling。
被否决的方案：在 wayfinder 里写死 skill 名字。
出处：d8d2da7f（17:22 第 4 条，17:27 第 4 条）；skills/wayfinder/SKILL.md 的接口表。

### ARD-F

理由：用户读完 wayfinder 及其依赖后说"这个wayfind 大部分我是同意的。 我也想使用"（d8d2da7f，17:22）。
导入前用户问过"grill with docs , what does this do?"（同一会话 10:15）。
被否决的方案：自己写一个访谈 skill。助手当时怎么回答的没有保留，用户为何满意属于 UNKNOWN。

### ARD-G

理由：正文调用的 `/grilling` 找不到。fa460cb 版一次问一个问题，与 wayfinder 的写法一致。
被否决的方案：取上游 HEAD。a4b2009（2026-07-16）起改为一轮问多个问题，与 wayfinder 不符。
出处：用户 2026-11-24 审阅回复（"D2 yes"）；mattpocock/skills 的 fa460cb。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：从过去的对话和提交记录反推 grill-with-docs 的决策 |
| 2026-11-24 | 加 ARD-G：补导 `/grilling`（fa460cb 版）；划掉 ARD-C |
| 2026-11-24 | 加 ARD-H：disable-model-invocation |
