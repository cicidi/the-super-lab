---
feature: doc-protect
type: decision-history
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# doc-protect — 决策记录

本篇按时间倒序记录 `doc-protect` 这个 skill 的关键决策。
需求见 [PRD](../prd/doc-protect-prd.md)，设计见 [design](../design/doc-protect-design.md)。
skill-factory 层面的旧决策在 [parent decision history](../../../decision-history/skill-factory-decision-history.md)。
opencode 会话按会话 id 前缀引用，数据在本机 opencode.db；walter-worker 的提交注明仓库名。

## Decision Log

| ID | Date | Decision |
|---|---|---|
| ARD-A | 2026-09-25 | 标准写法定为 `<!-- PROTECTED -->` 和 `<!-- END PROTECTED -->`；合并工具也认 `PROTECTED END` |
| ARD-B | 2026-08-02 | 正文标题随全仓改名变为 `walter-worker-doc-protect`；`name` 字段不变 |
| ARD-C | 2026-06-23 | 去掉 `ai-coworker-` 前缀，skill 改名为 `doc-protect` |
| ARD-D | 2026-06-23 | 其他个人 skill 移走后，doc-protect 仍留在 `personal-skills/` |
| ARD-E | 2026-06-11 | 从 ai-coworker 迁到 skill factory，归入个人 skill |
| ARD-F | 2026-03-30 | 用 HTML 注释标记受保护块；只有人能解除；加、减保护各提交一次 |

## Evidence Appendix

### ARD-A

理由：本机文件里现行写法出现 181 次，另一种 `PROTECTED START`/`PROTECTED END` 只有 2 次（commit 488ef70 的说明）。
旧的合并工具把 `PROTECTED END` 当成开始标记，保护范围一直延伸到文件末尾，之后的内容再也更新不了。
被否决的方案：改用 `PROTECTED START`/`PROTECTED END` 作为标准写法。
出处：本仓库 488ef70（改 doc-organize 的说明）；walter-worker 0936956（修合并工具）；analytics 会话 1293fd4b（2026-09-25）。
doc-protect 本身没改，它一直用现行写法。用户是否亲自提出这次修复，属于 UNKNOWN。

### ARD-B

理由：commit 40a10e4 把全仓文字里的 ai-coworker 一律替换成 walter-worker，正文标题跟着变了。
`name` 字段在 ARD-C 已没有前缀，所以没被替换，两者从此不一致（见 design 的 QUES-E）。
被否决的方案：UNKNOWN。出处：commit 40a10e4（2026-08-02）。

### ARD-C

理由：用户问"这些命名 合理吗"，要求推荐好记的名字，并让 skill factory 也按讨论的命名改（PRD-H）。
被否决的方案：保留前缀。parent 决策 0082 曾要求个人 skill 的 `name` 加前缀，这次与它相反。
出处：ses_1417bab9（2026-06-23）；commit 3395648。

### ARD-D

理由：UNKNOWN。用户问"self analyze 和heal 怎么还在personal folder 里面"，这两个随后移走（parent 决策 0029）。
agent 回复说 `personal-skills/` 只剩 doc-protect 和 session-memory；用户没再要求移动 doc-protect。
被否决的方案：移到公开的 skill 目录。出处：ses_1417bab9（2026-06-23）。是否有意保留，见 design 的 QUES-F。

### ARD-E

理由：用户清理 ai-coworker 时要求所有 skill 搬到 skill factory，并逐个指定去处（PRD-F）。
同批的 doc-merge 进了公开目录，doc-protect 进了 personal；为什么这样分，属于 UNKNOWN。
被否决的方案：留在 ai-coworker 仓库。出处：ses_14a669c2（2026-06-11）；commit a5dcc4e；walter-worker c7b2ea3。

### ARD-F

理由：原版说受保护内容代表"human decisions with context AI doesn't have"，即人的决定带有 AI 不知道的背景（PRD-A 到 PRD-D）。
被否决的方案：UNKNOWN。出处：walter-worker c3f771f 的 `templates/team-common/skills/doc-protection.md`。
提出这套规则的对话没有找到，属于 UNKNOWN。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：从过去的对话和提交记录反推 doc-protect 的决策 |
