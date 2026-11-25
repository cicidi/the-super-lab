---
feature: find-unknowns
type: design
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# research — 动手前找出未知

本篇说明 `research` 这个 skill 现在怎么工作。
源文件：`skills/research/SKILL.md`（commit 6086424 新建，c127ef7 改输出路径，2026-11-24 加 Branch C 和 Branch D，见 ARD-M）。

## Problem Statement

任务越复杂，用户没说出口的决定就越多；agent 碰到这些空白会自己猜（find-my-unknown 版的开篇，commit 9e4fb21）。
猜错的地方常在写完代码后才暴露，这时改起来代价高（PRD-F）。
另外，用户手上有 find-my-unknown 和 brainstorming 两个相近的 skill，不好管理（PRD-A）。
wayfinder 还需要一个不用人参与的调研能力，旧版每条路都要先问用户（PRD-M）。

## Solution

一个 skill，四条分支（PRD-A）。发现未知分支：先默默做功课，再一次一个问题地访谈。
写设计文档分支：一问一答澄清想法，比较几个方案，写成设计文档，再交给写实现计划的 skill。
无人值守调研分支：不问用户，查资料后交回一份每条都带出处的 markdown 文件（PRD-M）。
小测验分支：生成一份 HTML 报告，用几道题检查用户是否真懂了（PRD-N）。

## User Stories

- 作为开发者，我说"我不确定该怎么做"时，选发现未知分支。
- 作为开发者，我想从一个想法走到一份设计文档时，选写设计文档分支。
- 作为 wayfinder，我派 `/research` 子 agent 处理一条调研 brief，它直接走无人值守调研分支。
- 作为开发者，我说"考考我"时，走小测验分支。

## Implementation Decisions

本 skill 只有一个 SKILL.md，没有脚本，全靠 agent 读文字执行。
发现未知分支的规则来自 find-my-unknown（ARD-H、ARD-I）。
写设计文档分支沿用 superpowers:brainstorming 的清单，去掉了"视觉辅助"和"提交"两步（清单原文见 opencode 会话 ses_14bdec5d，2026-06-10）。
小测验分支照搬 find-my-unknown 的 Quiz 一节，只加了"没有代码改动时考刚讨论的话题"（ARD-M）。

## Design

**DSGN-A 选分支。** Step 0 先看是否有人在场（PRD-A、PRD-M）。
如果是子 agent、拿到了 wayfinder 的调研 brief，或者会话不能交互，就不问任何问题，直接进 Branch C（ARD-M）。
用户说"考考我"或"quiz me"时，直接进 Branch D（PRD-N）。
其他情况只问一句"你想做什么"，给两个选项：发现未知、写设计文档。
各分支除了入口外不共用逻辑；是否该更深地融合，见 QUES-I（PRD-B）。

**DSGN-B 默默扫描（A1）。** 提问前，先读相关代码和项目规则文件（CLAUDE.md、CONVENTIONS.md）。
弄清已有什么、有哪些约束、哪些决定还没做；这一步不问用户（PRD-E）。

**DSGN-C 访谈（A2）。** 一次只问一个问题，等用户回答后再问下一个（PRD-C、PRD-D）。
提问顺序：先问会改变架构的（数据模型、API 形状、权限），再问范围，再问沿用哪种约定，最后问优化选择（PRD-E）。

**DSGN-D 深度控制。** 判断标准是"这里错了，改起来多贵"：贵就深问 2 到 3 轮，便宜就问一轮（PRD-F）。
每个话题最多 2 到 3 轮，然后总结并换话题。用户答"不知道"时，agent 解释选项、选一个默认值，或去查资料。
停止条件：用户连续两次以上说"你看着办"（ARD-I，见 QUES-E）。

**DSGN-E 辅助工具。** 三个工具服务于访谈，不替代访谈（PRD-G）。
盲区扫描：用户似乎不了解代码库的约束时，agent 先自己查，再把发现变成一个问题。
原型：用户说"看到才知道"时，生成 2 到 3 个 HTML 原型让用户挑。
参考：用户说"做成像 X 那样"时，agent 读 X 并提取要点。

**DSGN-F 总结（A3）。** 访谈结束后汇总所有决定，标出还没解决的问题（PRD-C）。
再问用户：接着写设计文档，还是直接开始实现。

**DSGN-G 写设计文档分支的前四步（PRD-H）。** B1 看文件、文档和最近的提交，了解项目现状。
B2 一次一个问题澄清目的、约束和成功标准，能出选择题就出选择题（PRD-D）。
B3 给出 2 到 3 个方案和取舍，推荐的放第一个；按 YAGNI（现在用不上的功能就不做）删掉多余功能。
B4 按复杂度分节展示设计，涵盖架构、组件、数据流、错误处理和测试，每节都请用户确认。

**DSGN-H 写设计文档分支的后三步（PRD-H、PRD-I、PRD-O）。** B5 写设计文档。
仓库里有 `docs/features/spec-driven-development/` 时，把 B4 批准的设计交给 spec-write 写，格式由它负责（ARD-M）。
其他仓库照旧写到 `docs/features/<feature>/design/<topic>-design.md`（ARD-A）。
B6 自查：有没有 TBD/TODO 占位、前后矛盾、范围膨胀、说法含糊。
B7 用户批准文档后，调用 superpowers:writing-plans 写实现计划。

**DSGN-I 给别的 skill 调用（PRD-J、PRD-K）。** wayfinder 的接口表把 research 列为调研接口的默认实现。
wayfinder 以子 agent 调用时走 Branch C（DSGN-K）。SDD 把它列为发现盲区的工具之一，走 Branch A。

**DSGN-J 名字和位置（PRD-L）。** skill 在本仓库 `skills/research/`，名字不带前缀。
正文写明方法来自 Thariq Shihipar 的 "Finding Your Unknowns"；`source` 出处字段在合并时被删（ARD-F），见 QUES-D。
规格所在的子 feature 名是 find-unknowns，不是 research，避免和 `docs/features/discovery-research` 撞车（ARD-L）。

**DSGN-K 无人值守调研（Branch C）。** 全程不问用户（PRD-M、ARD-M）。
第一步从 brief 或调用方的提示里读出问题；问题不清楚时，在文件开头写下自己的理解，然后继续。
第二步读文档、第三方 API 和本地资料（代码、文档、git 历史、知识库），优先用一手资料。
第三步写一个 markdown 文件，分四节：问题、简短答案、发现、未知。
每条说法都带出处：URL、`文件:行号` 或 commit 哈希；查不到的标 `UNKNOWN`，并写明试过什么。
文件写在调用方指定的位置，wayfinder 指定的是一次性的 `research/<name>` 分支；没指定就写到工作目录的 `research/<name>.md`。
最后交回文件路径和一句话答案。

**DSGN-L 小测验（Branch D）。** 生成一份 HTML 报告，内容照 find-my-unknown 的原文（PRD-N、ARD-M）。
四部分：背景（为什么改、解决什么问题）、思路（为什么选这个做法）、改动（逐个文件讲理由）、3 到 5 道考理解而不是考记忆的题。
考的对象是刚做的改动；没有代码改动时，考刚讨论的话题，"改动"一节改为讲这个话题的要点。
是代码改动时，用户应先答对再合并。

## Testing Decisions

本 skill 没有自动测试或评测集，`skills/research/` 下只有 SKILL.md 一个文件。
2026-07-18 用户让 agent 在空目录 `~/project/ideas` 里试跑 find-my-unknown 的流程（ca8d23f7）。
合并前的真实使用有：评审文档（30bed348，2026-07-18）、讨论 PRD（71979623，2026-07-24）、设计复杂流程（d6def41e，2026-08-01）。
合并后只找到一次使用："/research 你来考考我"（d8d2da7f，2026-08-02），它要的就是 Branch D 的小测验。
Branch C 还没有被 wayfinder 实际调用过的记录。

## Out of Scope

小任务、需求已完全清楚、用户说已经规划好，都不用本 skill；已在实现阶段时改用 `/bug`（SKILL.md 的 When NOT to Use 一节）。

## Further Notes

需求见 [PRD](../prd/find-unknowns-prd.md)，决策见 [decision-history](../decision-history/find-unknowns-decision-history.md)。
2026-08-02 的合并表见 [parent design](../../../design/skill-factory-design.md)。
find-my-unknown 完整版（264 行）可用 `git show 9e4fb21:ai-coworker-skills/find-my-unknown/SKILL.md` 查看。

## Alternatives Considered

五种技巧按情况五选一：被否决，改为访谈做主线、三种技巧做辅助（ARD-H）。
find-my-unknown 和 brainstorming 各自独立：被否决，2026-08-02 合成一个 skill（ARD-E）。
所有问题同样深度：被否决，改为按改错代价决定（ARD-I）。为 SDD 新建盲区 skill：被否决（ARD-B）。
给 wayfinder 另造一个调研 skill：被否决，改为在本 skill 里加 Branch C（ARD-M）。

## Drawbacks

深度控制和轮数上限只写在发现未知分支；写设计文档分支的提问没有上限（DSGN-D、DSGN-G）。
B7 依赖外部的 superpowers 插件，没装时最后一步无法执行。
触发词里有 prototype，和独立的 prototype skill 重叠，见 QUES-H。
Branch C 靠 agent 自己判断"是否有人在场"，判断错了会在有人时不问，或在无人时卡住（DSGN-A）。

## Risks and Mitigations

| 风险 | 缓解 |
|---|---|
| wayfinder 用无人值守的子 agent 调用 research，子 agent 卡在提问上或替用户作答 | Step 0 先判断是否无人值守，是就走 Branch C，不提问（ARD-M） |
| B5 直接写 `docs/features/` 下的设计文档，格式不符合 SPEC-STANDARD.md | SDD 仓库里 B5 交给 spec-write（ARD-M） |
| Branch C 的结论没有出处，或把猜测写成事实 | 每条说法必须带出处，查不到的标 UNKNOWN（DSGN-K） |

## Open Questions

| ID | 问题 | 目前答案 | Owner | Blocking |
|---|---|---|---|---|
| QUES-A | 要不要加一条无人值守的"查资料"分支，产出带出处的 markdown，供 wayfinder 调用（PRD-J）？ | 已加 Branch C（ARD-M） | cicidi | no |
| QUES-B | 要不要恢复实现后的小测验？ | 已照原样恢复为 Branch D，也可考刚讨论的话题（ARD-M） | cicidi | no |
| QUES-C | 要不要恢复"实现中遇到偏差时再访谈"这一阶段（PRD-C 说每个阶段都访谈）？ | 合并时删除（ARD-F） | cicidi | no |
| QUES-D | 要不要恢复 `source` 和 `source_url` 出处字段？ | 只在正文提到作者；用户对外来内容要求注明出处（ses_14b5b4b7） | cicidi | no |
| QUES-E | 停止条件"连续两次你看着办"要不要保留？ | agent 写入，用户没有确认（ARD-I） | cicidi | no |
| QUES-F | B5 要不要改为交给 spec-write 写？ | SDD 仓库里交给 spec-write，其他仓库照旧（ARD-M） | cicidi | no |
| QUES-G | B7 要不要先写 test plan 再写 impl plan？ | 用户要求"先写test plan 在写impl plan"（d8d2da7f）；B7 直接调 writing-plans | cicidi | no |
| QUES-H | 触发词 prototype 和 prototype skill 重叠，归谁？ | SKILL.md 没有说 | cicidi | no |
| QUES-I | 各分支要不要共用一套访谈规则（PRD-B）？ | 各写一套，只共用入口 | cicidi | no |

## Reversibility

所有改动都落在 git 跟踪的 `skills/research/SKILL.md`，用 `git revert` 即可撤回。
被删的 find-my-unknown 完整版可从 commit 9e4fb21 取回。已安装的副本须重跑 `install.sh` 才同步。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：按 SKILL.md 写出 research 的 design，引用 PRD-A 到 PRD-L |
| 2026-11-24 | 加 DSGN-K（Branch C）、DSGN-L（Branch D），改 DSGN-A、DSGN-H、DSGN-I；QUES-A、QUES-B、QUES-F 已解决（ARD-M） |
