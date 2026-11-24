---
feature: wayfinder
type: decision-history
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# wayfinder — 决策记录

本篇按时间倒序记录 `wayfinder` 这个 skill 的关键决策。
需求见 [PRD](../prd/wayfinder-prd.md)，设计见 [design](../design/wayfinder-design.md)。
2026-08-02 的决策都出自 Claude Code 会话 d8d2da7f，下文只写当天时间。
skill-factory 层面的决策在 [parent decision history](../../../decision-history/skill-factory-decision-history.md)。

## Decision Log

| ID | Date | Decision |
|---|---|---|
| ARD-L | 2026-11-24 | 流水线改指 spec-ingest、spec-write、spec-review、spec-ticket、auto-tdd；spec 是文档，母工单由 spec-ticket 建 |
| ARD-A | 2026-11-03 | wayfinder 导入不再是 spec-driven-development 的 sub-feature，归属 skill-factory |
| ARD-B | 2026-08-02 | 流水线的 build 一步用 auto-tdd；SKILL.md 加一张流水线图 |
| ARD-C | 2026-08-02 | 导入工作先写测试计划，再写实现计划 |
| ARD-D | 2026-08-02 | 产出的文档都要 MkDocs-ready；doc-organize 随写随做，不单设关口 |
| ARD-E | 2026-08-02 | to-spec 之后、to-tickets 之前设 doc-review 关口；spec 本身是一个 issue，由 to-spec 建 |
| ARD-F | 2026-08-02 | map、fog of war 等原术语都保留，不按《绝命毒师》改名 |
| ARD-G | 2026-08-02 | task brief 有交付物时，关闭前先审查：文档用 doc-review，代码用 matt-code-review，都没有就用 Claude 默认审查 |
| ARD-H | 2026-08-02 | 四个依赖做成可替换接口，安装时逐个问；investigate 用自己的 research，其余用 matt 的默认 |
| ARD-I | 2026-08-02 | 决策用的 ticket 改叫 brief；ticket 一词只留给 to-tickets 的执行工单 |
| ARD-J | 2026-08-02 | 导入 mattpocock 的 wayfinder 并注明出处，改写正文；只连带导入它直接依赖的三个 skill |
| ~~ARD-K~~ | ~~2026-08-02~~ | ~~把 wayfinder 的术语整体换成《绝命毒师》的词~~ 已被 [ARD-F](#ard-f) 取代 |

## Evidence Appendix

### ARD-L

理由：用户说 Matt 的 to-spec 和 to-tickets"可以去掉"（Q5），先建新 skill 再删旧的（Q9）。
ARD-E 里"spec 是一个 issue，由 to-spec 建"不再成立：spec 写进 `docs/features/<f>/`，spec-ticket 开一张只放链接的母工单。
被否决：保留 to-spec、to-tickets 与新 skill 并存。出处：用户 2026-11-24 审阅回复（会话 80291c19）；commit 5370f61；
[spec-ingest ARD-E](../../spec-ingest/decision-history/spec-ingest-decision-history.md#ard-e)；
[spec-ticket ARD-H](../../spec-ticket/decision-history/spec-ticket-decision-history.md#ard-h)。

### ARD-A

理由：wayfinder 导入是另一项工作，属于 skill-factory，不是 SDD 的交付物。
SDD（spec-driven-development）是本仓库从 spec 驱动开发的 feature。导入文档最初按用户要求放在它下面（17:58 到 18:01）。
被否决的方案：继续把导入当作 SDD 的 sub-feature。
出处：[SDD 的 ARD-T](../../../../spec-driven-development/decision-history/spec-driven-development-decision-history.md#ard-t)。

### ARD-B

理由：用户说"implement 我的替代是auto-tdd"（18:37）（PRD-L）。commit 43cb1ef（18:39）加了 Pipeline 一节。
被否决的方案：用导入的 implement 做 build 一步。经过见 [implement 的 ARD-B](../../implement/decision-history/implement-decision-history.md#ard-b)。

### ARD-C

理由：agent 准备直接写实现计划时，用户说"改一下， 应该先写test plan 在写impl plan"（18:02），并要求写进 spec（18:04）（PRD-K）。
被否决的方案：先写实现计划。出处：commit 0f3ede7 导入规格第 9.1 节和 test plan 文件。

### ARD-D

理由：用户问 doc-organize 能不能保证"所有文档 mkdoc ready to deploy as github webpage"（17:57）（PRD-H）。
导入规格第 6 节写明这是随写随做的纪律，每次建或移文档都跑 doc-organize，不是单独一道关口。
被否决的方案：单独设一道整理关口（导入规格第 6 节 "NOT a separate checkpoint"）。"随写随做"的形式由 agent 写入，用户没有逐条确认。出处：commit 0f3ede7、7c11a7b。

### ARD-E

理由：用户说"spec 本身也得有一个ticket"，to-tickets 以前"还得有一个 doc-review 的过程"（17:55）（PRD-G）。
用户原话把建 spec 工单交给 toTicket；7c11a7b 写成由 to-spec 建，见 design 的 QUES-E。
被否决的方案：spec 写完直接拆工单。完整经过见 [to-spec 的 ARD-B](../../to-spec/decision-history/to-spec-decision-history.md#ard-b)。

### ARD-F

理由：agent 逐节展示导入规格时，用户说"map 不改， 还是这个名字""fog of war 也不该"（17:47）（PRD-C）。
用户又说"Breaking Bad terminology 不用提这个"（17:49），"不用非要按照break bad 来"（17:50）。
被否决的方案：ARD-K 的整体改名。导入规格只改 ticket 一个词，但第 11 节仍把这次改名列为"separate future map"（commit 0f3ede7）。

### ARD-G

理由：用户要求"每次delivery 以前"都审查：文档用 doc-review，代码用 code review，没有就用 Claude 默认的（17:27 第 7 条）（PRD-F）。
只拦 task 类 brief，研究、访谈、原型三类跳过，因为它们产出的是知识和决策（导入规格第 5 节）。这条范围由 agent 写入。
被否决的方案：不设审查直接关闭 brief。出处：commit 0f3ede7、7c11a7b。

### ARD-H

理由：用户要求依赖的 skill 都是接口（17:22 第 4 条），安装时问用户，不替换就用 matt 的；research 用自己的（17:27 第 4 条）（PRD-E）。
四个接口是 interview、investigate、prototype、tracker（导入规格第 4 节）。被否决的方案：写死 matt 的 skill。
"选择要记下来"写进了 SKILL.md，但仓库里没有对应的配置文件，见 design 的 QUES-C。出处：commit 0f3ede7、7c11a7b。

### ARD-I

理由：用户说 ticket 用得混乱，后面的 to ticket 保留，前面的应叫 challenge、question 或 query（17:22 第 2 条），17:27 回复"2 ok"（PRD-B）。
被否决的方案：challenge、question、query。经过见 [to-tickets 的 ARD-E](../../to-tickets/decision-history/to-tickets-decision-history.md#ard-e)。
agent 为什么推荐 brief，会话记录已不在本机，属于 UNKNOWN。

### ARD-J

理由：用户学完后说"大部分我是同意的。 我也想使用"，并要求"import 这个skill 著名作者"（17:22 第 1 条）（PRD-A）。
导入规格第 10 节连带导入 grill-with-docs、domain-modeling、prototype；research 不导入，用 ai-coworker 自己的。
被否决的方案：原样导入不改，或一次导入整条流水线。出处：commit 7c11a7b（18:20）、0f3ede7（18:21）。

### ARD-K

理由：用户想把 matt 的 skill 转成自己的，"rename to breaking bad words"（14:25），先让 agent 找对应的词（14:27）。
17:47 到 17:50 用户放弃了这个想法，被 ARD-F 取代。当时找到哪些词，会话记录已不在本机，属于 UNKNOWN。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：从过去的对话和提交记录反推 wayfinder 的决策 |
| 2026-11-24 | 新增 ARD-L：流水线改指 spec-ingest / spec-ticket，母工单由 spec-ticket 建 |
