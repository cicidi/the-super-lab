---
feature: spec-ingest
type: decision-history
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# spec-ingest — 决策记录

本篇按时间倒序记录 `spec-ingest` 的关键决策。同一天的决策，编号靠后的排在上面。
需求见 [PRD](../prd/spec-ingest-prd.md)，设计见 [design](../design/spec-ingest-design.md)。
姊妹 skill 的决策见 [spec-ticket decision-history](../../spec-ticket/decision-history/spec-ticket-decision-history.md)。
"用户 2026-11-24（会话 80291c19）"指本次需求会话；标"agent 推荐"的决策用户还没有确认。

## Decision Log

| ID | Date | Decision |
|---|---|---|
| ARD-L | 2026-11-24 | 测试按与期望分拣的一致率打分（≥90%）；只有硬规则做精确检查 |
| ARD-K | 2026-11-24 | 改指清单是 `grep -rln 'to-spec\|to-tickets'` 找到的所有文件，改前改后各查一次 |
| ARD-J | 2026-11-24 | 分拣表存为 `docs/features/<f>/raw/state/spec-ingest/<date>-sort.md` |
| ARD-I | 2026-11-24 | spec-ingest 只出条目、出处、文档类型、目标 feature；写进哪个文件由 spec-write 定 |
| ARD-H | 2026-11-24 | spec-ingest 不在 tracker 上建 issue；spec 本身的工单已定：spec-ticket 的 ARD-O（每个 feature 一张母工单）（agent 推荐） |
| ARD-G | 2026-11-24 | 去掉 to-spec 的"测试接缝确认"一步；输入里提到的接缝照常分到 design（agent 推荐） |
| ARD-F | 2026-11-24 | 保留 to-spec 的"不访谈，只整理"；写入前只请用户确认一次分拣表 |
| ARD-E | 2026-11-24 | 新 skill 能用后删掉 to-spec，引用它的地方在同一个改动里改指 |
| ARD-D | 2026-11-24 | 名字定为 spec-ingest |
| ARD-C | 2026-11-24 | 第一版输入只有当前聊天和本地 md、pdf、txt 文件 |
| ARD-B | 2026-11-24 | spec-ingest 只读和分拣，spec-write 仍是唯一写提交文档的 skill |
| ARD-A | 2026-11-24 | 自建 skill 替代 Matt 的 to-spec，产出是用户自己的五类 spec 文档 |

## Evidence Appendix

### ARD-A

理由：Matt 的 to-spec 只产出一份 PRD 模板；用户要的是自己 spec 里的 design、prd、impl、test、decision history（PRD-A）。
被否决的方案：继续用导入的 to-spec，只在 SDD 仓库里交给 spec-write（to-spec 现状，见 [to-spec decision-history](../../to-spec/decision-history/to-spec-decision-history.md) 的 ARD-F）。
出处：用户 2026-11-24（会话 80291c19）原话"我认为我自己应该创建一个 skill"。

### ARD-B

理由：两个 skill 都写 spec，规则会分叉；to-spec 的 design 曾把这列为风险（[to-spec design](../../to-spec/design/to-spec-design.md) 的 QUES-C）。
SDD 的 ARD-AJ 已定 spec-write 是写 spec 的入口。
被否决的方案：spec-ingest 自己按模板写文档。出处：用户 2026-11-24（会话 80291c19），Q1 回答 yes。

### ARD-C

理由：先做最常见的两种来源，范围小，好测试（PRD-C）。
被否决的方案：第一版就支持网址、会议转写稿、从代码反推 spec；这些列为以后的方向。
出处：用户 2026-11-24（会话 80291c19），Q2 回答 yes。

### ARD-D

理由：ingest 意为"摄入"，说明它读进内容而不是写文档；以 spec- 开头，和 spec-write、spec-review 归为一组。
被否决的方案：沿用 to-spec 这个名字。名字已通过 document-standard 的 DSGN-K 重名检查。
出处：用户 2026-11-24（会话 80291c19），Q6 回答"可以"。

### ARD-E

理由：两个 skill 做同一件事会让 agent 选错入口（PRD-F）。
顺序是：spec、spec-review、用户审阅、SKILL.md，最后删旧 skill 并改指所有引用（清单见 ARD-K）。
被否决的方案：长期保留 to-spec 作为非 SDD 仓库的入口。出处：用户 2026-11-24（会话 80291c19），Q5"可以去掉"、Q9。

### ARD-F

理由：to-spec 的核心想法是只整理、不访谈（PRD-D）。spec-ingest 只分拣，不需要向用户要新内容。
分拣表的确认不是访谈：它只问"这样分对不对"，不问新事实。
被否决的方案：像 grill-with-docs 一样逐条访谈补齐。出处：`skills/to-spec/SKILL.md`；协调方的需求简报（2026-11-24）。

### ARD-G

理由：to-spec 的第 2 步让 agent 自己设计测试接缝（seam，即测试从哪一层接入代码）并找用户确认。
这是新的设计工作，和"只读和分拣"（ARD-B）矛盾。输入里已有的接缝说法，照常分到 design 的 Testing Decisions。
被否决的方案：保留这一步。把握约 80%，用户还没确认。出处：agent 推荐（2026-11-24）；`skills/to-spec/SKILL.md` 第 2 步。

### ARD-H

理由：to-spec 在 SDD 仓库里写完后会发一个链接 issue（to-spec 第 3a 步）。
建工单是 spec-ticket 的职责，放在 spec-ingest 里会让两个 skill 都碰 tracker。
"spec 本身也得有一个ticket"（[to-spec PRD](../../to-spec/prd/to-spec-prd.md) 的 PRD-D）已定：spec-ticket 的 ARD-O（每个 feature 一张母工单），见 [spec-ticket decision-history](../../spec-ticket/decision-history/spec-ticket-decision-history.md)。
被否决的方案：照搬 to-spec 第 3a 步。出处：agent 推荐（2026-11-24）。

### ARD-I

理由：spec-write 的第 2、3 步已经决定新建还是改旧、哪份是权威文档；spec-ingest 再定一次，规则就在两处（ARD-B）。
被否决的方案：spec-ingest 给出动作列，并改 spec-write 让它照单执行。采用本决定后，spec-write 的 SKILL.md 不用改。
出处：用户 2026-11-24"是的 spec write 决定文件在哪里写"；spec-review 报告第 1 条。

### ARD-J

理由：有固定文件名，spec-write 和用户都找得到；`raw/` 被 `.gitignore` 忽略，不会提交。
feature 还没确认时，放在 wayfinder 地图目录下（SDD 的 ARD-CH）。被否决的方案：只说放在 `raw/state/`，不给文件名。
出处：用户 2026-11-24 同意；spec-review 报告第 6 条。

### ARD-K

理由：原先写的"wayfinder、implement、README"不对，`skills/implement/` 里没有对 to-spec 的引用。
用 grep 定义清单，和 spec-ticket 的写法一致。被否决的方案：手写一份固定清单。
出处：spec-review 报告第 8 条（2026-11-24）。

### ARD-L

理由：分类靠 agent 判断，两次运行可能不同，逐行完全一致的要求做不到。
精确检查只留给硬规则：不经 spec-write 不写、无出处标 UNKNOWN、不改提交文档。
被否决的方案：逐行完全一致。出处：spec-review 报告第 10 条（2026-11-24）。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：记录会话 80291c19 的用户决定和两条 agent 推荐 |
| 2026-11-24 | 按 spec-review 加 ARD-I 到 ARD-L；ARD-H 指向 spec-ticket 的 QUES-A；ARD-D、ARD-E 修正 |
| 2026-11-24 | ARD-H 改为已定：spec-ticket 的 ARD-O（每个 feature 一张母工单） |
