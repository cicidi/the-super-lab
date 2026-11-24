---
feature: spec-ingest
type: design
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# spec-ingest — 把已有信息分拣进 spec

本篇说明 `spec-ingest` 打算怎么工作。skill 还不存在，`skills/spec-ingest/SKILL.md` 要等本篇审过后再写（PRD-F）。
需求见 [PRD](../prd/spec-ingest-prd.md)，决策见 [decision-history](../decision-history/spec-ingest-decision-history.md)。
姊妹 skill 见 [spec-ticket design](../../spec-ticket/design/spec-ticket-design.md)。

## Problem Statement

讨论有了结论，或者手上有一份旧文档，用户想把内容并进某个 feature 的 spec。
现在只能用 Matt 的 to-spec，它按一份 PRD 模板整理，不认识用户的五类文档（PRD-A）。
如果另做一个会写文档的 skill，又会和 spec-write 形成两条写入路径，规则分叉（PRD-B）。

## Solution

spec-ingest 读输入，把内容切成一条条"条目"（item，即一句能单独成立的事实），给每条找出处、定文档类型、定目标 feature。
结果是一张分拣表。用户确认后，整张表交给 spec-write 去写（PRD-B）。
spec-ingest 自己不改任何提交进仓库的文档。

## User Stories

- 作为开发者，我说"把刚才聊的分拣进 spec"，agent 给我一张表：每条内容去哪个文档，出处是哪句话。
- 作为开发者，我给一个 pdf 路径，agent 读完后同样给我一张表，没出处的条目标 UNKNOWN。
- 作为维护者，我希望写进哪个文件只由 spec-write 一处决定，规则不分叉。

## Implementation Decisions

skill 只有一个 SKILL.md，不带脚本。分类、找出处由 agent 按本篇的规则做。
pdf 用 agent 的文件读取工具读，不另装解析库（PRD-C）。
分拣表存为 `docs/features/<f>/raw/state/spec-ingest/<date>-sort.md`；`raw/` 被 `.gitignore` 忽略，不会提交（ARD-J）。

## Design

**DSGN-A 输入。** 第一版只接受两种输入（PRD-C）。
一是当前聊天的上下文：从用户指定的起点到现在的消息；没指定起点就用整段会话。
二是本地文件：扩展名为 `.md`、`.pdf`、`.txt` 的路径，可以一次给多个。
给了网址、音视频、代码目录等其他输入时，spec-ingest 停下，说明第一版不支持，并列出以后的方向。
pdf 没有文字层（例如扫描件）读不出字时，同样停下报告，不猜内容（QUES-C）。

**DSGN-B 切条目，带出处。** 每个条目只说一件事。一句话同时含需求和理由时，拆成两条：需求归 PRD，理由作为背后的决定归 decision-history。
出处的写法：聊天消息写"用户 日期（会话 id 前缀）"；文件写行里点名的人或引用，再加路径和行号（pdf 加页码）。
文件里既没点名也没引用的事实，出处写 UNKNOWN 并附位置；待定问题不需要依据，只写位置。
找不到出处的条目，出处写 UNKNOWN，内容照样保留（PRD-G）。
agent 自己推出来、输入里没有明说的内容，不算条目，不进表。

**DSGN-C 分类规则。** 每个条目按下表归到一种文档类型。类型和 ID 前缀见 `skills/spec-organize/SPEC-STANDARD.md`。

| 条目是什么 | 去向 | ID 前缀 |
|---|---|---|
| 需求：用户要系统做什么、不做什么 | PRD | PRD- |
| 带理由的决定：选了什么、为什么、否了什么 | decision-history | ARD- |
| 行为或约定：系统怎么表现、接口长什么样 | design | DSGN- |
| 实现步骤：先做什么后做什么、谁依赖谁 | impl-plan | IMPL- |
| 测试用例：给定什么输入、期望什么结果 | test-plan | TST- |
| 还没答案的问题 | design 的 Open Questions | QUES- |

一个决定没有说理由时，仍归 decision-history，理由写 UNKNOWN。
一个条目归不进任何一行，或同时像两行时，标"待定"，在分拣表里请用户选（DSGN-H）。

**DSGN-D 目标 feature。** 先找条目属于哪个已有的 `docs/features/<f>/`。
没有合适的 feature 时，spec-ingest 不建新目录；它提议一个暂定名，等人确认（SDD 的 ARD-CH）。
确认前，分拣表放在 wayfinder 的地图目录 `docs/state/wayfinder-<暂定名>/spec-ingest/` 下（SDD 的 ARD-CH，ARD-J）。
仓库里还没有 `docs/features/` 时走同一条路：人确认名字后，由 spec-write 建第一个 feature 目录；人不想在这个仓库放 spec 就停（ARD-M）。

**DSGN-E 新文档还是改旧文档：由 spec-write 定。** spec-ingest 只定文档类型和目标 feature，不定写进哪个文件（ARD-I）。
新建还是改旧、哪份是权威文档、冲突怎么办，都由 spec-write 按它的第 2、3 步决定（PRD-B）。
所以 spec-write 的 SKILL.md 不用改。

**DSGN-F 交给 spec-write 的内容。** 交接物就是分拣表，每行一个条目，列为：
条目编号（I-1、I-2 这样的临时号，不是永久 ID）、原文、出处、文档类型、目标 feature。没有目标文件和动作列（ARD-I）。
另附三项：目标 feature 名（或暂定名）、输入清单、本次的 UNKNOWN 清单。
永久 ID（PRD-A 这类）由 spec-write 按现有文档的下一个空字母分配，spec-ingest 不分配。
spec-write 照常遵守每次编辑不超过 10 行、200 字符的规则；表很长时，它分多次编辑（SDD 的 ARD-CE）。

**DSGN-G 不访谈，不设计接缝。** spec-ingest 不向用户追问新内容，只整理输入里已有的东西（PRD-D、ARD-F）。
to-spec 第 2 步的"测试接缝确认"去掉（ARD-G）：设计接缝是新的设计工作，不是分拣。
输入里已有的接缝或测试说法，按 DSGN-C 分到 design 的 Testing Decisions 或 test-plan。

**DSGN-H 写入前确认一次。** spec-ingest 把分拣表给用户看，只问一件事：分得对不对。
用户可以改某行的去向、删行、裁定"待定"的行。确认后才交给 spec-write（ARD-F）。
用户不确认，spec-ingest 就停在这里，什么都不写。

**DSGN-I 报告。** 交接完成后，spec-ingest 向用户报告：
各文档类型分到几条；spec-write 新建和改了哪些文档；UNKNOWN 清单；新开的 QUES；被拒绝的输入及原因。
它不建 tracker 上的 issue（ARD-H）。要建工单，用户接着跑 [spec-ticket](../../spec-ticket/design/spec-ticket-design.md)。

**DSGN-J 名字和替换 to-spec。** skill 名为 spec-ingest（PRD-E）。
`skills/to-spec/` 已在 commit `5370f61` 删掉；同一个改动里改指了 `grep -rln 'to-spec\|to-tickets'` 找到的每个文件，改前改后各查一次（PRD-F、ARD-K）。
顺序：本 spec、spec-review、用户审阅、SKILL.md、删旧并改指（ARD-E）。

## Testing Decisions

用一个固定的测试 feature 做夹具（fixture，即内容已知、每次都一样的测试输入）。
夹具含一段写好的聊天记录和一个 md、一个 txt、一个带文字层的 pdf，每条内容的正确去向事先写在期望表里。
跑 spec-ingest 只到分拣表为止，按文档类型和目标 feature 算与期望表的一致率，≥90% 算过，"待定"行不算错（ARD-L）。
必须覆盖的情况：六种类型各至少一条；一句话含需求和理由要拆成两条；无出处要标 UNKNOWN；不支持的输入（网址）要被拒绝；扫描版 pdf 要停下报告。
硬规则做精确检查，一次不过就算失败：不经 spec-write 不写；无出处标 UNKNOWN；
跑完后 `git status` 里没有 spec-ingest 改动的提交文档（PRD-B、ARD-L）。
评测可以复用 `skills/spec-organize/tests/gold/` 的金标形式，具体放哪里由 SKILL.md 阶段定。

## Out of Scope

网址、会议转写稿、从代码反推 spec（PRD-C）；直接写提交文档（PRD-B）；建工单（ARD-H）；对抗式审查，那是 spec-review 的事。

## Further Notes

Matt 原版见 `skills/to-spec/SKILL.md`；它的旧需求见 [to-spec PRD](../../to-spec/prd/to-spec-prd.md)。
spec-ticket 读的是 spec-write 写好的 impl-plan，所以两者的顺序是：spec-ingest、spec-write、spec-review、spec-ticket。

## Alternatives Considered

spec-ingest 自己写文档：被否决，会出现第二条写入路径（ARD-B）。
保留 to-spec 不删：被否决（ARD-E）。
保留接缝确认：被否决，它是设计而不是分拣（ARD-G）。
按条目逐条问用户：被否决，改为整张表确认一次（ARD-F）。

## Drawbacks

分类靠 agent 判断，同一输入跑两次，"待定"行可能不同。
多一道确认，比 to-spec 直接写慢一步。
长聊天会产生很长的表，用户审起来费力。

## Risks and Mitigations

| 风险 | 缓解 |
|---|---|
| agent 把自己的推测当成条目写进表 | DSGN-B 规定输入里没明说的不进表；每条必须带出处或 UNKNOWN |
| 两个 skill 都判断写进哪个文件，规则分叉 | DSGN-E 规定只有 spec-write 判断（ARD-I） |
| `docs/features/downstream-delivery/` 仍把 to-spec 写成下游 skill，删 to-spec 后它成了过时的重复文档 | 已原地改写，指向新 skill（ARD-N） |
| 删 to-spec 时漏改某个引用，留下断链 | 删除和改指在同一个改动里做，改完用 `grep -rn to-spec` 查一遍（ARD-E） |

## Open Questions

| ID | 问题 | 目前答案 | Owner | Blocking |
|---|---|---|---|---|
| QUES-A | spec-ingest 和 spec-ticket 上线后，`docs/features/downstream-delivery/` 怎么处理：删、合并进 skill-factory，还是标成废弃？ | 已定：原地改写，discovery-research 的 PRD-B 一并改（ARD-N） | cicidi | no |
| QUES-B | 去掉接缝确认（ARD-G）、不建 issue（ARD-H）这两条 agent 推荐，用户是否同意？ | agent 推荐，待审；spec 本身的工单已定：spec-ticket 的 ARD-O（每个 feature 一张母工单） | cicidi | no |
| QUES-C | 扫描版 pdf 要不要先交给 pic-to-txt 做 OCR 再分拣？ | 第一版停下报告（DSGN-A） | cicidi | no |
| QUES-D | 分拣表在 spec-write 写完后保留还是删除？ | 留在 `raw/state/spec-ingest/`，不提交（ARD-J） | cicidi | no |

## Reversibility

本 skill 不改提交文档，分拣表在被忽略的目录里，用户不确认就什么都不发生。
spec-write 写入的改动是普通的 git 改动，可用 `git revert` 撤回。
删 to-spec 是一个独立的提交，可以单独 revert 恢复；已安装到 `~/.claude/skills/` 的副本须重跑 `install.sh` 才同步。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：spec-ingest 的正向 design，覆盖 PRD-A 到 PRD-G |
| 2026-11-24 | 按 spec-review 改 DSGN-D、E、F、H、I、J、测试和风险（ARD-I 到 ARD-L）；QUES-B 指向 spec-ticket |
| 2026-11-24 | QUES-B：spec 本身的工单已定，见 spec-ticket 的 ARD-O |
| 2026-11-24 | DSGN-B 写明理由条目的去向和文件内出处规则（写 SKILL.md 时补） |
| 2026-11-24 | DSGN-D 加无 spec 目录的仓库（ARD-M）；QUES-A 已定（ARD-N） |
