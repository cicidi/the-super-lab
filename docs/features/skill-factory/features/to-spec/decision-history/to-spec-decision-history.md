---
feature: to-spec
type: decision-history
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# to-spec — 决策记录

本篇按时间倒序记录 `to-spec` 这个 skill 的关键决策。
需求见 [PRD](../prd/to-spec-prd.md)，设计见 [design](../design/to-spec-design.md)。
skill-factory 层面的旧决策在 [parent decision history](../../../decision-history/skill-factory-decision-history.md)。
会话按 `~/.claude/history.jsonl` 里的 id 前缀和时间引用。

## Decision Log

| ID | Date | Decision |
|---|---|---|
| ARD-F | 2026-11-24 | SDD 仓库里交给 spec-write 写，再发一个链接 issue；非 SDD 仓库仍按模板写 PRD 发到 tracker |
| ARD-A | 2026-09-25 | 模板每一节标上内容级别 L1 到 L4，加 Alternatives Considered 一节，并加 Skill Dependencies 指向文档标准 |
| ARD-B | 2026-08-02 | spec 发布后、to-tickets 之前设一道文档审查关口；关口写在 wayfinder，不写进 to-spec |
| ARD-C | 2026-08-02 | spec 自己作为一个 issue 发布，打 `ready-for-agent` 标签 |
| ARD-D | 2026-08-02 | 导入 mattpocock 的 to-spec：沿用原版正文，加 frontmatter 和作者出处 |
| ~~ARD-E~~ | ~~2026-08-02~~ | ~~to-spec 列为 wayfinder 导入的后续项，这次不导入~~ 已被 [ARD-D](#ard-d) 取代 |

## Evidence Appendix

### ARD-F

理由：c44e983 后没有 `spec` 类型，模板也对不上 prd 和 design；SDD 规定写 spec 只走 spec-write（ARD-AJ）。
被否决：改模板去凑现行标准。出处：用户 2026-11-24 审阅回复；SDD decision-history ARD-AJ。

### ARD-A

理由：用户在会话 631b8662 定了四级内容，要求先删四级和三级、文档小于 1000 行、重复的事实只放链接（09:26、09:37）。
commit f67df5b 把这套规则写进当时的 doc-organize，并在同一提交里改了 to-spec 的模板（PRD-F、PRD-G、PRD-H）。
被否决的方案：代码是唯一事实来源（commit f67df5b 的说明，改为按关注点分权威）。
把级别标到 to-spec 模板上，是用户点名要的还是 agent 顺带做的，对话里看不出，属于 UNKNOWN。
出处：commit f67df5b；会话 631b8662（2026-09-25）。

### ARD-B

理由：用户说"spec 一个文档不够"，在 to ticket 以前"还得有一个 doc-review 的过程"，审查所有文档（PRD-E）。
commit 7c11a7b 把这道关口写进 wayfinder 的 SKILL.md，排在 to-spec 和 to-tickets 之间；to-spec 正文没有改。
被否决的方案：spec 写完直接拆工单。把关口放进 to-spec 本身是否讨论过，属于 UNKNOWN。
出处：d8d2da7f（17:55）；commit 7c11a7b（18:20）。

### ARD-C

理由：用户说"spec 本身也得有一个ticket"（PRD-D）。wayfinder 的实体关系写明：spec 是 1 个 issue，标签 `ready-for-agent`，由 to-spec 建。
`ready-for-agent` 表示 agent 可以直接认领，不必再分诊。被否决的方案：只给执行工单建 issue，spec 不建。
这个标签是原版就有，还是导入时加的，属于 UNKNOWN，见 ARD-D。出处：d8d2da7f（17:55）；commit 7c11a7b、212aab5。

### ARD-D

理由：用户要求注明作者（PRD-B），没有替换的接口"就用matt 的ksill"（PRD-C）。
被否决的方案：像 wayfinder 那样改写正文；wayfinder 改了术语和接口，to-spec 没有。
导入时有没有改正文，属于 UNKNOWN：212aab5 只有一个提交，看不出和原版的差别。
`docs/book/imported-skills.md` 说导入时把 Jira 换成 issue tracker、加了 `ready-for-agent`，但它写的导入日期是 2026-07-25，与 git 的 2026-08-02 不符。
出处：commit 212aab5（18:34）；d8d2da7f（17:22 第 1 条，17:27 第 4 条，18:34）。

### ARD-E

理由：wayfinder 的导入规格只导入 wayfinder 直接依赖的 skill，把"to-spec、to-tickets、implement"列为后续导入。
被否决的方案：一次导入整条流水线。出处：commit 0f3ede7（18:21）的 wayfinder-import-spec，Out of Scope 一节。
13 分钟后（18:34）用户说"continue importing to-spec"，本决策被 ARD-D 取代。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：从过去的对话和提交记录反推 to-spec 的决策 |
| 2026-11-24 | 新增 ARD-F：SDD 仓库交给 spec-write |
