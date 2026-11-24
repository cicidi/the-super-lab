---
feature: wayfinder
type: design
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# wayfinder — 规划大任务的决策地图

本篇说明 `wayfinder` 这个 skill 现在怎么工作。
源文件：`skills/wayfinder/SKILL.md`（commit 43cb1ef 定稿，93d4a4a 移到现在的位置）。

## Problem Statement

一个大任务塞不进一个 agent 会话，而且从起点到终点的路还看不清。
直接动手容易冲错方向；换了会话，前面定下的决策又会丢（PRD 的目标一）。
用户学习时问过"how does the issue tracker persist state across sessions?"（d8d2da7f，2026-08-02 14:30）。

## Solution

把规划写成 tracker 上的一张地图（map）和一组决策问题（brief），每个会话只解决一个 brief。
brief 全部定完后，交给 to-spec、spec-review、to-tickets、auto-tdd 这条流水线（PRD-L）。

## User Stories

- 作为开发者，我带着一个模糊的大想法调用 wayfinder，它和我一起定下终点，画出第一版地图。
- 作为开发者，我在新会话里给出地图链接，它自己挑下一个能做的 brief。
- 作为开发者，我在安装时决定四个依赖分别用谁。

## Implementation Decisions

正文在 matt 原版上改写，只有 SKILL.md 一个文件（ARD-J）。兄弟 skill to-spec、to-tickets、implement 只加了 frontmatter。
导入后正文只改过一次：43cb1ef 加了 Pipeline 一节；8d451059、93d4a4a 只搬目录。
SKILL.md 说 research、matt-code-review 来自 ai-coworker；research 现在就在本仓库 `skills/research/`。

## Design

**DSGN-A 只规划，不执行。** 每个 brief 解决一个决定；没有要决定的事了，地图就算走完，交给下游（PRD 的 Out of Scope）。
地图的 Notes 一节可以写明例外，把执行也放进地图。

**DSGN-B 地图。** 地图是 tracker 上一个带 `wayfinder:map` 标签的 issue。它是索引：每个决策只存在它的 brief 里，地图只写一行要点加链接。
正文五节：Destination、Notes、Decisions so far、Not yet specified、Out of scope（PRD-C）。
打开的 brief 不列在地图上，靠查询找。给人看的地方都用 issue 标题称呼，不用裸编号。

**DSGN-C brief。** 每个 brief 是地图的子 issue，正文只有一个 Question，大小按一个 100K token 的会话来定（PRD-B）。
claim（占用）：开工前先把 brief 指派给自己，指派就是占用，别的会话会跳过它。
阻塞用 tracker 原生的依赖关系。frontier（前沿）指打开、没被阻塞、也没被占用的 brief。

**DSGN-D 四类 brief。** HITL（human in the loop）指要人在场回答；AFK 指 agent 单独完成（PRD-B）。
HITL 的 brief 里，agent 不能替人回答自己提的问题。
research（AFK）由 research 子 agent 查资料；prototype（HITL）做一个粗糙的原型给人看；
grilling（HITL）一次问一个问题地追问，是默认类型。
task（两种都可）是做决定前必须先完成的手工活，比如注册一个服务才能评估它的 API；它不交付终点本身。

**DSGN-E 迷雾和范围外。** 能把问题说精确，就建 brief，哪怕它暂时被阻塞；说不精确，就写进 Not yet specified（PRD-C）。
超出终点的工作写进 Out of scope，永远不会变成 brief。已建的 brief 若超出终点，就关闭它，并在这一节留一行。

**DSGN-F 可替换接口。** 四个接口和默认实现：interview 用 grill-with-docs 加 domain-modeling，investigate 用 research（PRD-E）。
prototype 用 prototype，tracker 用 `gh` 命令行操作 GitHub Issues。
首次安装时每个接口问一句，回答可以是 keep、use <name> 或 skip；skip 表示那类 brief 不可用。
SKILL.md 说选择会被记下，但没写记在哪里，见 QUES-C。

**DSGN-G 画地图（第一种调用）。** 用户带着模糊的想法调用。先用 grilling 和 domain-modeling 定下终点（PRD-D）。
再广度优先地追问一轮，找出所有待定的决策。没有迷雾、一个会话就能做完时，不建地图，停下问用户。
然后建地图和能说清的 brief，第二遍再连阻塞关系，因为 issue 要先有 id 才能互相引用。
最后为每个 research brief 并行启动子 agent，结果放在临时的 `research/<name>` 分支。到此停止，不亲手解决任何 brief。

**DSGN-H 走地图（第二种调用）。** 用户给出地图的链接或编号，brief 可给可不给；没给就取 frontier 上的第一个，先 claim（PRD-J）。
需要时读相关 brief 的全文，调用 Notes 里点名的 skill 来解决。
记录结果：在 issue 下评论答案，关闭它，在地图的 Decisions so far 追加一行。
接着建新浮现的 brief，把变清楚的迷雾升级成 brief。除 research 外，每个会话只解决一个 brief。

**DSGN-I 交付审查关口。** 走地图第 4a 步：task 类 brief 产出了文件、代码或文档时，关闭前必须过审查（PRD-F）。
`.md` 文件用 spec-review（688cace 起），代码用 matt-code-review，都没有时用 Claude 默认审查；没通过就修了再审。
其余三类 brief 跳过这一步，因为它们产出的是知识和决策。

**DSGN-J MkDocs-ready。** 每次建或移文档都顺手跑 doc-organize：维护 INDEX.md，文件名用 kebab-case（小写加连字符）（PRD-H）。
目录结构对应网站导航；加了新栏目就更新 `mkdocs.yml` 的导航。

**DSGN-K spec 和文档审查关口。** 地图走完后先跑 to-spec，把所有 brief 的结论合成一份 spec，并为 spec 建一个 issue（PRD-G）。
接着 spec-review 审 spec、所有已关闭的 brief、CONTEXT.md 和 ADR，查一致、完整、无矛盾，并确认 MkDocs-ready。
通过后才能跑 to-tickets。数量关系是 N 个 brief 合成 1 份 spec，再拆成 M 张执行工单。

**DSGN-L 流水线。** 顺序是 wayfinder（决定）、to-spec（写）、spec-review（核对）、to-tickets（拆工单）、auto-tdd（实现）（PRD-L）。

**DSGN-M 出处。** frontmatter 写 `source_author: mattpocock` 和指向原文件的 `source_url`（PRD-A）。

**DSGN-N 只写在导入规格里的需求。** 完整生命周期示例只在导入规格第 8 节，SKILL.md 没有（PRD-I），见 QUES-F。
"先写测试计划，再写实现计划"只约束当时的导入工作，不是 skill 的行为（PRD-K）。
"定终点是第一个 challenge"写成了画地图的一步，不是一个 brief（PRD-D），见 QUES-A。

## Testing Decisions

`skills/wayfinder/` 下只有 SKILL.md，没有自动测试或评测集。
导入时写过 12 条检查用例，覆盖 frontmatter、出处、术语、接口、审查关口和冒烟测试（commit 0f3ede7 的 test plan）。
这些用例是否逐条跑过，git 里没有记录，属于 UNKNOWN。
SDD 的 [TST-J](../../../../spec-driven-development/test-plan/spec-driven-development-test-plan.md) 计划比较追问时加不加 wayfinder 的效果。

## Out of Scope

不执行（DSGN-A）；不写 spec（to-spec）；不拆执行工单（to-tickets）；不写代码（auto-tdd）。
一个会话能做完的工作、需求已完整且有工单的工作，都不用本 skill（`when_not_to_use` 字段）。

## Further Notes

需求见 [PRD](../prd/wayfinder-prd.md)，决策见 [decision-history](../decision-history/wayfinder-decision-history.md)。
导入规格、实现计划和测试计划已在 c44e983 删除，可用 `git show 0f3ede7` 查看。
用户后来真用过它：2026-08-25 规划一份硬件产品的 PRD 和交付合同（会话 09bbe239），2026-09-13 问"当前做到哪里了"（fbb18112）。
2026-09-25 用户发现已安装的 skill 里"wayfinder 有两个"，随后要求给 install.sh 加清理旧目录的 prune（631b8662）。

## Alternatives Considered

原样导入 matt 的 wayfinder：被否决，改写了术语、接口和关口（ARD-J）。
把术语整体换成《绝命毒师》的词：被否决（ARD-F、ARD-K）。
依赖写死为 matt 的 skill：被否决，改为可替换接口（ARD-H）。
spec 写完直接拆工单：被否决，中间加 spec-review 关口（ARD-E）。

## Drawbacks

tracker 的说法不统一：接口表默认 GitHub Issues，没配置时又默认 `.scratch/` 下的本地 markdown，审查关口图和实体关系却写 Jira，见 QUES-B。
SKILL.md 引用的 /grilling 曾找不到；2026-11-24 已补导到 `skills/grilling/`，见 QUES-D。

## Risks and Mitigations

| 风险 | 缓解 |
|---|---|
| 引用的 skill 改了名：本仓库的 doc-review 已改名 spec-review（c44e983） | 688cace 已改用新名；见 QUES-D |
| 安装时的接口选择没处保存，下次调用读不到 | 暂无；见 QUES-C |
| 多个会话同时编辑 tracker，抢同一个 brief | 开工前先 claim，指派即占用（DSGN-C） |

## Open Questions

| ID | 问题 | 目前答案 | Owner | Blocking |
|---|---|---|---|---|
| QUES-A | 定终点（讨论 PRD）要不要做成地图上的第一个 brief（PRD-D）？ | 用户 17:27 说"3 yes"，SKILL.md 仍写成一个步骤 | cicidi | no |
| QUES-B | 默认 tracker 是 GitHub Issues、本地 `.scratch/` 还是 Jira？ | SKILL.md 三种说法都有 | cicidi | no |
| QUES-C | 安装时的四个接口选择记在哪里（PRD-E）？ | SKILL.md 说"会记下"，仓库里没有对应配置文件 | cicidi | no |
| QUES-D | /grilling 和 doc-review 现在分别指哪个 skill？ | /grilling 指 `skills/grilling/`（2026-11-24 补导，grill-with-docs 的 ARD-G）；688cace 已把 doc-review 改成 spec-review | cicidi | no |
| QUES-E | spec 的 issue 该由 to-spec 还是 to-tickets 建（PRD-G）？ | SKILL.md 写 to-spec，与用户 17:55 原话不同；同 to-tickets 的 QUES-A | cicidi | no |
| QUES-F | 完整生命周期示例要不要放进 SKILL.md（PRD-I）？ | 只在已删除的导入规格第 8 节 | cicidi | no |

## Reversibility

所有改动都落在 git 跟踪的 `skills/wayfinder/SKILL.md`，用 `git revert` 即可撤回；matt 的原版见 `source_url`。
已安装到 `~/.claude/skills/` 的副本，须重跑 `install.sh` 才同步。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：按 SKILL.md 写出 wayfinder 的 design，引用 PRD-A 到 PRD-L |
| 2026-11-24 | QUES-D 有答案：`/grilling` 已补导；doc-review 已在 688cace 改为 spec-review |
| 2026-11-24 | 正文里的 doc-review 改为 spec-review，跟上 688cace |
