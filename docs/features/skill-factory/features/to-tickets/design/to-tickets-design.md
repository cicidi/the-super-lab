---
feature: to-tickets
type: design
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# to-tickets — 把 spec 拆成执行工单

本篇说明 `to-tickets` 这个 skill 现在怎么工作。
源文件：`skills/to-tickets/SKILL.md`（commit 8730941 导入，之后只搬过两次目录）。

## Problem Statement

spec 定下之后，下游实现需要一组大小合适、能逐张完成的工单（PRD-A）。
工单之间有先后；不写清谁挡住谁，就看不出哪些现在能开工（PRD-C）。

## Solution

一个拆工单的 skill：读 spec 和代码库，按纵向切片起草工单，请用户审拆法，再发布到 tracker（PRD-C）。
每张工单写明被哪些工单挡住；发布顺序是被依赖的在前（PRD-C）。

## User Stories

- 作为开发者，spec 过了文档审查后，我调用 to-tickets，得到一组编号的工单（PRD-F）。
- 作为开发者，我在发布前看到拆法清单，可以要求合并或再拆（PRD-C）。

## Implementation Decisions

`skills/to-tickets/` 下只有一个 SKILL.md，没有脚本或其他文件；整个 skill 就是给 agent 读的说明。
frontmatter 保留了原作者的 MIT 许可（`license: MIT`），`compatibility` 写的是 claude-code 和 opencode。
发布前必须经用户认可拆法，这是全程唯一的提问点（SKILL.md Process 第 4 步）。

## Design

**DSGN-A 触发与出处。** spec 或计划已经可以拆分时触发（PRD-C）。
没有 spec 或计划、一张工单就够、或决策还没定时不用；决策没定先用 wayfinder（`when_not_to_use` 字段）。
frontmatter 的 `source_author: mattpocock` 和 `source_url` 注明原作者和原文地址（PRD-B）。

**DSGN-B 收集上下文。** 先用对话里已有的内容；用户给了 spec 路径或 issue 编号时，读全文和评论（PRD-C）。
可选地读代码库：工单用项目术语表（glossary）里的词，并遵守相关的 ADR（architecture decision record，架构决策记录）。
如果先重构能让实现变简单，就先重构，即"先让改动变容易，再做容易的改动"（PRD-C）。

**DSGN-C 纵向切片。** tracer bullet（曳光弹）指先打通全程的一条细线；每张工单都是这样一条线（PRD-C）。
它窄但完整地穿过每一层：schema、API、界面、测试；不是只做一层的横向切片。
每张完成后能单独演示或验证，大小放得进一个新的上下文窗口；需要的预重构排在最前。

**DSGN-D 阻塞边。** 每张工单列出必须先完成的工单，叫阻塞边（blocking edge）；没有阻塞的可以马上开工（PRD-C）。
阻塞全部完成的工单构成 frontier（前沿）。按前沿推进；纯线性的一串工单就是从上到下。

**DSGN-E 大范围重构的例外。** 一处机械改动（例如改列名）会波及整个代码库，叫 wide refactor（PRD-C）。
它没法切成能单独通过测试的纵向切片，于是改用 expand–contract（先扩展、后收缩）。
先 expand：在旧形式旁加上新形式，什么都不坏。再按包或目录分批迁移调用方，每批一张工单，都被 expand 挡住。
最后 contract：没有调用方后删掉旧形式，这张工单被所有迁移批次挡住。
批次单独过不了 CI（持续集成）时，让它们共用一个集成分支，只在最后一张"集成并验证"工单上保证全绿。

**DSGN-F 请用户审拆法。** 以编号列表展示每张工单的标题、被谁挡住、交付什么端到端行为（PRD-C）。
问用户三件事：粒度是否合适，阻塞边是否正确，要不要合并或再拆。反复修改，直到用户认可。

**DSGN-G 发布到 tracker。** tracker 配置来自项目的 init 流程；没有配置时用本地文件（PRD-C）。
本地文件：每张工单一个文件，放在 `.scratch/<feature-slug>/issues/<NN>-<slug>.md`，按依赖顺序从 01 编号。
被依赖的排在前面；每张一个文件，不许合成一个大文件。
真实 tracker（GitHub、Linear 等）：每张工单一个 issue，按依赖顺序发，用平台自带的阻塞关系，打 `ready-for-agent` 标签。
`ready-for-agent` 表示 agent 可以直接认领，不用再分诊。不关闭、也不修改父 issue（PRD-C）。

**DSGN-H 工单模板。** 本地模板有：标题、要做什么、被谁挡住、状态 `ready-for-agent`、验收清单（PRD-C）。
issue 模板有四节：Parent（父 issue，没有可省）、What to build、Acceptance criteria、Blocked by。
"要做什么"写用户看得到的端到端行为，不写逐层的实现清单。不写文件路径和代码片段，它们很快过时。
例外：原型产出的状态机、schema、类型这类片段比文字更准时，可摘关键部分，并注明来自原型。

**DSGN-I 词汇与流水线位置。** 本 skill 里 ticket 只指执行工单；wayfinder 的决策工单叫 brief（PRD-D）。
wayfinder 写的顺序是 wayfinder、to-spec、spec-review、to-tickets、auto-tdd（PRD-A、PRD-G）。
spec-review 关口必须先通过才能运行 to-tickets；它写在 wayfinder 里，不在本 skill 里（PRD-F）。
spec 自己的 issue 由 to-spec 建，本 skill 不建；这与用户的原话不同，见 QUES-A（PRD-E）。

## Testing Decisions

本 skill 没有自动测试或评测集，`skills/to-tickets/` 下只有 SKILL.md 一个文件。
downstream-delivery 的 test-plan 列了 TST-C：to-tickets 产出工单大小的块，靠人工审查；没找到运行记录，见 QUES-E。

## Out of Scope

不做决策（那是 wayfinder 的事）；不写 spec（to-spec）；不写代码（auto-tdd）；不关闭或修改父 issue。

## Further Notes

需求见 [PRD](../prd/to-tickets-prd.md)，决策见 [decision-history](../decision-history/to-tickets-decision-history.md)。
downstream-delivery 的 PRD-F2 说 to-tickets 把 impl-plan 拆成工单（commit 65c2634）；SKILL.md 的输入是计划、spec 或对话，没有专门提 impl-plan。
导入前用户问过工单大小一般怎么定（d8d2da7f，17:05）；当时的回答没有保留。SKILL.md 的标准是放得进一个新的上下文窗口。

## Alternatives Considered

像 wayfinder 那样改写正文：没有采用，只加 frontmatter 和出处（ARD-F）。
spec 写完直接拆工单：被否决，先过 spec-review 关口（ARD-C）。
由 implement 接手工单：被否决，改为 auto-tdd（ARD-B）。
把本地工单放进 `docs/features/`：被否决，放在 `.scratch/`（ARD-A）。

## Drawbacks

拆法要等用户认可才发布（DSGN-F），无人值守的流水线会停在这一步。
本地工单放在 `.scratch/`；它在 2026-11-24 才加入 .gitignore，此前可能被误提交，见 QUES-D。
工单发到 tracker，和 `docs/features/` 下的 impl-plan 是两条路；同一份计划可能两处各存一份。

## Risks and Mitigations

| 风险 | 缓解 |
|---|---|
| 用户要 to-tickets 为 spec 建 ticket，现在落在 to-spec，职责可能两边都漏 | 确认分工，见 QUES-A |
| 本仓库找不到 init 流程写的 tracker 配置，agent 只能落到本地文件 | 写明配置位置，见 QUES-B |
| `.scratch/` 没被 git 忽略，临时工单可能被提交 | 2026-11-24 已补 `.gitignore` 规则，见 QUES-D |

## Open Questions

| ID | 问题 | 目前答案 | Owner | Blocking |
|---|---|---|---|---|
| QUES-A | spec 的 ticket 该由 to-tickets 还是 to-spec 建（PRD-E）？ | wayfinder 写的是 to-spec（7c11a7b），与用户 17:55 原话不同 | cicidi | no |
| QUES-B | tracker 配置放在哪（PRD-C）？ | SKILL.md 说来自 init 流程；本仓库没找到配置文件 | cicidi | no |
| QUES-C | implement 要不要移除（PRD-G）？ | 用户说用 auto-tdd 替代，implement 仍在 `skills/` 里 | cicidi | no |
| QUES-D | `.scratch/` 要不要加进 `.gitignore`（ARD-A）？ | 要。2026-11-24 已加入 .gitignore | cicidi | no |
| QUES-E | downstream-delivery 的 TST-C 跑过吗？ | 没找到运行记录 | cicidi | no |
| QUES-F | 关口用 doc-review 还是 spec-review（PRD-F）？ | spec-review。688cace（2026-11-24）已把 wayfinder 里的 doc-review 改成 spec-review | cicidi | no |

## Reversibility

所有改动都落在 git 跟踪的 `skills/to-tickets/SKILL.md`，用 `git revert` 即可撤回；导入时的原样可从 commit 8730941 取回。
已安装到 `~/.claude/skills/` 的副本，须重跑 `install.sh` 才同步。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：按 SKILL.md 写出 to-tickets 的 design，引用 PRD-A 到 PRD-G |
| 2026-11-24 | QUES-D、QUES-F 有答案：`.scratch/` 已加入 .gitignore；wayfinder 已在 688cace 改用 spec-review |
| 2026-11-24 | 正文里的 doc-review 改为 spec-review，跟上 688cace |
