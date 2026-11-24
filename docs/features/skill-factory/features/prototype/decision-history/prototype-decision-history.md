---
feature: prototype
type: decision-history
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# prototype — 决策记录

本篇按时间倒序记录 `prototype` 这个 skill 的关键决策。
需求见 [PRD](../prd/prototype-prd.md)，设计见 [design](../design/prototype-design.md)。
Claude Code 会话原文没有保留；下文引用 `~/.claude/history.jsonl` 里用户输入的会话 id 前缀和时间。

## Decision Log

| ID | Date | Decision |
|---|---|---|
| ARD-A | 2026-08-02 | 和其他 skill 一起从 `import-skills/` 移到 `skills/prototype/` |
| ARD-B | 2026-08-02 | 只导入 SKILL.md，没有导入它链接的 `LOGIC.md` 和 `UI.md` |
| ARD-C | 2026-08-02 | 正文原样导入，只改 frontmatter，并写上原作者和原文链接 |
| ARD-D | 2026-08-02 | 作为 wayfinder 的 prototype 接口默认实现；prototype brief 要人参与，且不过交付前审查 |
| ARD-E | 2026-08-02 | 直接导入 Matt Pocock 的版本，不自己从头写 |

## Evidence Appendix

### ARD-A

理由：commit 93d4a4a 把所有 skill 收进同一个 `skills/` 目录，prototype 只是其中之一。
被否决的方案：保留单独的 `import-skills/` 目录。这次移动的讨论没有找到，理由属于 UNKNOWN。
出处：commit 8d451059 先把 skill-factory 仓库的 import-skills 并入本仓库根目录，93d4a4a 再移到 `skills/`。

### ARD-B

理由：UNKNOWN。导入计划 Task 1 的第 4 步只用 curl 取了 SKILL.md 一个文件（.superpowers/sdd/wayfinder-import-plan/task-1-brief.md）。
上游目录里还有 `LOGIC.md`、`UI.md` 和 `agents/`（gh api 查询，2026-11-24）。同批的 domain-modeling 则连模板一起导入。
被否决的方案：整个目录一起导入。是有意省略还是漏掉，属于 UNKNOWN，见 design 的 QUES-A。

### ARD-C

理由：用户要求注明作者（PRD-B），没有替换的接口"就用matt 的ksill"（PRD-C）。
导入规格把这一条写成 Body preservation：grill-with-docs、domain-modeling、prototype 只改 frontmatter。
被否决的方案：像 wayfinder 那样改写正文。
出处：d8d2da7f（2026-08-02 17:22、17:27）；commit 78242fa；wayfinder-import-spec（commit 0f3ede7）。

### ARD-D

理由：用户要求 wayfinder 用到的 skill 都做成接口，安装时问用户，没给替换就用 matt 的（PRD-D）。
用户把 prototype 归为 HITL，即要人参与（d8d2da7f，17:12；PRD-E）。
"不过交付前审查"由 agent 写进导入规格；用户原话是每次交付前"所有的代码都需要review"（17:27 第 7 条），见 design 的 QUES-B。
被否决的方案：在 wayfinder 里写死 skill 名字。出处：wayfinder-import-spec 的接口表；skills/wayfinder/SKILL.md。

### ARD-E

理由：用户读完 wayfinder 及其依赖后说"这个wayfind 大部分我是同意的。 我也想使用"（d8d2da7f，17:22）。
导入前用户问过"what about prototype?"（同一会话 12:12），助手当时的回答没有保留。
被否决的方案：自己写一个原型 skill。用户为何认可这个版本，属于 UNKNOWN。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：从过去的对话和提交记录反推 prototype 的决策 |
