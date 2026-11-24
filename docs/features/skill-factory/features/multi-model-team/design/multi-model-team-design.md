---
feature: multi-model-team
type: design
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# multi-model-team — 多模型团队编排

本篇说明 `multi-model-team` 这个 skill 现在怎么工作。
源文件：`skills/multi-model-team/SKILL.md`（commit 56f3e00 创建，93d4a4a 移到现在的位置，内容未改）。

## Problem Statement

一个大任务若由一个 agent 从头做到尾，拆分、实现、审查都落在同一个模型上。
用户希望 GLM 5.2 只做分析、拆分和审查，DeepSeek v4 Pro 负责实现（PRD-A、PRD-B、PRD-C）。

SKILL.md 的说法是：架构师负责推理和判断，工人负责机械的实现。用户为何这样分工没有明说（decision-history 的 ARD-I）。

## Solution

一个 skill，五个阶段：分析、拆分、分派、审查、整合。
架构师是 opencode 里的主 agent，工人是它派生的子 agent，两者在配置里各配一个模型（PRD-D）。

## User Stories

- 作为开发者，我说"build a full feature"后，架构师先给我一份拆分方案，我批准后工人才开工。
- 作为开发者，任务很小时，我希望它不开工人，直接改。

## Implementation Decisions

两个角色靠 `opencode.json` 的 agent 配置实现。architect 是 primary（主 agent），模型 `zai-coding-plan/glm-5.2`，temperature 0.1（ARD-J）。
worker 是 subagent（子 agent），模型 `deepseek/deepseek-v4-pro`，temperature 0.2。

temperature 是控制输出随机性的参数，越低越稳定。架构师用 opencode 的 Task tool（开子 agent 的工具）分派工人。
SKILL.md 提醒模型 id 因 provider 而异，要用 `opencode models` 核对。

GLM 的 provider 是用户在用的 `zai-coding-plan`，用 `opencode auth login` 登录（ARD-J）。
两个 agent 不随 skill 安装生成；SKILL.md 给出配置块，要用户自己加进 opencode.json（ARD-J）。

## Design

**DSGN-A 检查前提。** 没有配好 architect 和 worker 两个 agent 时，不开工，而是告诉用户并给出配置块（PRD-D）。
这一条写在 When NOT to Use 和测试场景 5 里，Process 各阶段没有单独的步骤。

**DSGN-B 阶段一：分析。** 架构师找出目标和验收标准、子任务间的先后依赖、可以并行的部分（PRD-A）。
子任务数估计为 2 到 5 个，最多 8 个。

拆不出独立的子任务时，架构师自己直接做。分析不清楚时，只问用户一个问题。

**DSGN-C 阶段二：拆分。** 每个子任务写清描述、预期产出（改哪些文件、测试覆盖）、依赖和优先级（PRD-A）。
方案交用户批准后才继续；被否决就按反馈改一次，然后继续。

**DSGN-D 阶段三：分派。** 互不依赖的子任务用 Task tool 并行派给工人（PRD-B）。有依赖的，等前置子任务成功后再派。
每个工人的 prompt 自成一体，包含子任务描述和预期产出、相关文件路径。

prompt 还规定：不许改分配范围以外的文件，做完返回改动摘要和顾虑。

**DSGN-E 工人自我纠错。** 工人报告失败时，用同一个 prompt 重试，最多 3 次（PRD-F）。
第 3 次仍失败，就带着失败经过上报架构师。架构师重新分析后，改写 prompt 再派，或自己接手。

**DSGN-F 阶段四：审查。** 架构师逐个核对产出是否符合描述，检查并行工人之间的冲突（PRD-C）。
然后跑项目的测试，以及 lint 和类型检查。lint 指检查代码风格和常见错误的工具。

小问题架构师自己修；中等问题带具体反馈重派工人一次；大问题上报用户。
3 个以上子任务都有问题时，说明是整体问题，架构师带着新信息回到阶段一。

**DSGN-G 阶段五：整合。** 架构师检查所有改动文件是否一致（import、命名、写法），再跑一次完整测试（PRD-C）。
最后向用户报告：做了什么、哪个工人做的、还有什么顾虑。

**DSGN-H 何时触发。** 任务涉及 3 个以上文件、跨多个关注点、或能拆成可并行的子任务时使用（PRD-E）。
触发语有大任务说法，也有"use the team""orchestrate this""break this down"等显式说法。

**DSGN-I 质量门。** 必须满足：拆分先批准、工人 prompt 自成一体、工人返回摘要、全量测试、向用户报告（PRD-G）。
建议满足：工人产出合并无冲突、测试覆盖率不降、lint 和类型检查一次通过。

**DSGN-J 存放和部署。** skill 放在本仓库的 `skills/multi-model-team/SKILL.md`，由安装脚本部署到各 AI 工具（PRD-H）。
2026-07-14 首次部署时，复制到了 opencode 和 Claude Code 的配置目录（ses_0a0d1e98）。

## Testing Decisions

SKILL.md 有 5 个文字测试场景：完整功能、单个小修、工人失败自我纠错、并行冲突、缺少模型配置。
没有自动测试或评测集，`skills/multi-model-team/` 下只有 SKILL.md 一个文件。

opencode.db 和 Claude 会话记录里，只找到创建它的那次会话，没有找到实际调用记录。

## Out of Scope

单文件小改或少于 3 步的小修、没有独立子任务的任务、没配好两个模型时，都不用本 skill（SKILL.md 的 When NOT to Use）。

## Further Notes

需求见 [PRD](../prd/multi-model-team-prd.md)，决策见 [decision-history](../decision-history/multi-model-team-decision-history.md)。

SKILL.md 的 Sources 说：阶段一、二参考 subagent-driven-development，阶段四参考 verification-before-completion。
skill-factory 整体设计见 [parent design](../../../design/skill-factory-design.md)。

## Alternatives Considered

失败时由架构师重派、退回单 agent、或直接上报用户：用户没选，改为工人自己重试 3 次（ARD-E）。
所有任务默认走团队流程：用户没选，只在大任务时触发（ARD-G）。

并入别的 skill：2026-08-02 合并时被否决，保持独立（ARD-A）。

## Drawbacks

SKILL.md 只写了 opencode 的配置方法；它也被装进 Claude Code，但在那里怎么用没有说，见 QUES-D。
模型名写死在 description 和配置示例里，模型换代就要改 skill。

阶段三说工人用"同一个 prompt"重试，测试场景 3 却说"逐步调整做法"重试，两处不一致，见 QUES-E。

## Risks and Mitigations

| 风险 | 缓解 |
|---|---|
| 并行的工人改到同一个文件，互相冲突 | 按依赖错开分派；阶段四审查和测试会发现冲突（DSGN-D、DSGN-F） |
| 本机没配 architect 和 worker，skill 跑不起来 | 本机 opencode.json 目前没有这两个 agent；SKILL.md 要求先报告缺失配置（DSGN-A） |
| 重试、重派、回到阶段一层层叠加，花费失控 | 工人重试上限 3 次，重派一次；但没有总花费或总时长上限 |

## Open Questions

| ID | 问题 | 目前答案 | Owner | Blocking |
|---|---|---|---|---|
| QUES-A | 触发语要不要只留用户选的大任务一类（PRD-E）？ | SKILL.md 还列了"use the team"等显式说法 | cicidi | no |
| QUES-B | 失败处理只要工人重试（PRD-F），还是保留重派、接手、上报用户等多级后备？ | SKILL.md 全都写了（ARD-E） | cicidi | no |
| QUES-C | 配置示例要不要改成用户实际用的 `zai-coding-plan/glm-5.2`？ | 已改为 `zai-coding-plan/glm-5.2`（ARD-J） | cicidi | no |
| QUES-D | 在 Claude Code 里怎么用这个 skill？ | SKILL.md 只写了 opencode | cicidi | no |
| QUES-E | 工人重试时用同一个 prompt，还是调整做法？ | 阶段三和测试场景 3 说法不一致 | cicidi | no |
| QUES-F | 拆分后先让用户批准，是否符合用户意图？ | agent 写入，用户没有逐条确认（ARD-C） | cicidi | no |
| QUES-G | 用什么可量化的指标判断这个 skill 好用？ | UNKNOWN，也没有实际调用记录 | cicidi | no |
| QUES-H | 架构师模型要不要换成 glm-5.3 或 glm-5.4？ | 2026-11-24 的 `opencode models` 在 zai-coding-plan 下只列出 5.3、5.4，没有 5.2 | cicidi | no |

## Reversibility

所有改动都落在 git 跟踪的 `skills/multi-model-team/SKILL.md`，用 `git revert` 即可撤回。
已安装到各工具配置目录的副本，须重跑 `install.sh` 才同步。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：按 SKILL.md 写出 multi-model-team 的 design，引用 PRD-A 到 PRD-H |
| 2026-11-24 | 按 ARD-J 改写 provider 和 agent 配置说明，QUES-C 已答，新增 QUES-H |
