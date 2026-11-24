---
feature: spec-ticket
type: design
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# spec-ticket — 把 impl-plan 的每一步发成工单

本篇说明新 skill `spec-ticket` 打算怎么工作。skill 还没有实现，本篇是前瞻式设计。
需求见 [PRD](../prd/spec-ticket-prd.md)，决策见 [decision-history](../decision-history/spec-ticket-decision-history.md)。
审查报告指 `docs/features/skill-factory/raw/review/2026-11-24-spec-review-spec-ingest-spec-ticket-gaps.md`。

## Problem Statement

impl-plan 已经把工作切成一条条 `IMPL-*`，但它们只在 markdown 里，tracker 上看不到（PRD-A）。
用户想用 GitHub issue 或 Jira 演示和跟踪这些步骤，并由自己的配置决定用哪个（PRD-B）。
现有的 to-tickets 会重新切分工作，并且每次都要用户审拆法，和 impl-plan 的切分重复（ARD-B）。

## Solution

一个只做"搬运"的 skill：读 impl-plan，一条 IMPL 开一张工单，照 IMPL 写的依赖连阻塞边（PRD-A、PRD-C）。
它把 IMPL 和工单的对应关系记在本机，重跑时只加新的（PRD-D、PRD-E）。
它只往 tracker 写，不往 spec 写回（PRD-F）。

## User Stories

- 作为开发者，spec-review 通过后，我对一个 feature 运行 spec-ticket，tracker 上出现每条 IMPL 的工单（PRD-A）。
- 作为开发者，我没配置 tracker 时，工单写成本地 markdown 文件，不会意外发到网上（PRD-B）。
- 作为开发者，design 里还有 blocking 的问题时，spec-ticket 拒绝运行并告诉我是哪几条（PRD-H）。

## Implementation Decisions

skill 由一份 SKILL.md 加三个 tracker 适配器组成；适配器指把同一套操作翻译成某个 tracker 的具体命令的部分。
三个适配器提供同一组操作：查找已有工单、创建工单、加阻塞边（DSGN-I、DSGN-J、DSGN-K）。
发到 GitHub 或 Jira 之前，先列出将要创建的工单并请用户确认一次；写本地文件不用确认。
这是本设计自己的选择，不是用户的决定：发到网上的工单删起来麻烦（见 Reversibility），见 QUES-F。
spec-ingest 的 spec 用 `docs/features/skill-factory/features/spec-ingest/design/spec-ingest-design.md`；两者不共享代码。

## Design

**DSGN-A 触发与流水线位置。** 输入是一个 feature 名，或一份 impl-plan 的路径（PRD-A）。
在流水线里，它排在 spec-review 通过之后、implement 之前，占的是 to-tickets 原来的位置（PRD-I）。
上游是 spec-ingest 和 spec-write 写好的 spec；spec-ticket 自己不写任何 spec 文档（PRD-F）。
找不到 impl-plan，或 impl-plan 里没有 `IMPL-*` 时，停下并提示先用 spec-write 写 impl-plan。

**DSGN-B 阻塞问题闸（PIPE-E-A）。** 开工单前，读该 feature design 的 Open Questions 表（PRD-H）。
只要有一行 `QUES-*` 的 Blocking 列是 `yes` 或 `是`，就停下（不看目前答案一栏，ARD-M），列出这些 QUES，不开任何工单。
这条规则来自 `skills/wayfinder/SKILL.md`；spec-ticket 自己再查一次，因为它可能不经 wayfinder 被直接调用。

**DSGN-C 读 tracker 配置。** 在项目的 CLAUDE.local.md 里找一行 `tracker: github | jira | local`（PRD-B、ARD-C）。
找不到这一行或这个文件时，用 local。值不是这三个之一时，停下报错，不猜。
这一行与 wayfinder 共用；DSGN-M 改指向时，wayfinder 的 tracker 说明也改成读这一行（ARD-J）。
本条是协调者的推荐，用户还没确认（QUES-C）。

**DSGN-D 解析 IMPL。** impl-plan 里每个 `## IMPL-X — 标题` 小节算一条 IMPL（PRD-A）。
每条读出：ID、标题、正文、依赖、挡住、完成标准（`Verify:` 或 `完成标准`，见 `skills/spec-organize/SPEC-STANDARD.md`）。
在整个 IMPL 小节里找 `依赖`、`挡住` 标签（或英文 Depends on、Blocks），不限行首，取其后的所有 `IMPL-*` ID（ARD-L）。
带条件的依赖（如"报告部分还依赖 IMPL-L"）也算依赖，宁可多连，不漏连。
写"无"的，就没有这一项。
不是 IMPL ID 的依赖文字（如"本批 spec 修改完成"）不丢，原样列进报告。
小节写明已完成（"已完成""已经完成""已于…完成"，或英文 `Status: done`）的 IMPL 不开工单，列进报告（ARD-L）。

**DSGN-E 工单内容。** 标题是 `[<feature>] IMPL-X — <IMPL 标题>`；带上 feature 和 IMPL ID，重跑时能按标题找回（PRD-A、PRD-E）。
正文有三部分：IMPL 的原文（含完成标准），impl-plan 的仓库内路径和小节锚点，以及"Blocked by"一行（本地必写；GitHub 只作退路，见 DSGN-I；Jira 用链接，见 DSGN-K）。
正文末尾注明"由 spec-ticket 生成，以 impl-plan 为准，工单上的修改不会写回"（PRD-F）。
沿用 to-tickets 的 `ready-for-agent` 标签，表示 agent 可以直接认领；仓库里没有这个标签时不打，并在报告里说明。

**DSGN-F 阻塞边。** 甲挡住乙，条件是乙的依赖里写了甲，或者甲的挡住里写了乙；两边取并集（PRD-C）。
两边写得不一致时照样连，并在报告里列出不一致的地方，供作者修 impl-plan。
依赖指向一个不存在的 IMPL ID 时，跳过这条边并报告。被依赖的 IMPL 已完成时，它不再挡人，这条边也跳过并报告。依赖成环时，停下并报告环上的 IMPL，不开工单。
按依赖顺序一遍开完：被依赖的先开，开后面的工单时前面的编号已经有了，当场就能连边（ARD-K）。

**DSGN-G 对应表。** 只在 github、jira 模式下用（本地模式见 DSGN-J）；每个 feature 一份，放在 `docs/features/<f>/raw/state/spec-ticket-map.md`（PRD-D、ARD-E）。
内容是一张表，列为 IMPL、tracker、工单号或路径、标题、创建日期。
每开成一张工单就立即写一行，所以中途失败后重跑，也不会给已开的再开一张。
这个目录被 git 忽略，换一台机器或重新 clone 时表会丢；丢了靠 DSGN-H 的按标题查找兜底。

**DSGN-H 幂等重跑。** 幂等指同样的输入跑多少次，结果都和跑一次一样（PRD-E）。
对每条 IMPL，先查对应表；表里没有，再让适配器按 DSGN-E 的标题去 tracker 上找。
两处都没有才新开。找到的补写进对应表。
已有的工单一律不改，包括标题和正文；只在新 IMPL 挡住旧 IMPL 时，给旧工单补一条阻塞边（见 QUES-E）。
impl-plan 里被删掉或改了文字的 IMPL，只在报告里列出，不关闭也不修改它的工单（PRD-F）。

**DSGN-I GitHub 适配器。** 用 gh 命令行（2.94 以上，本机 2.101）操作当前仓库（PRD-B、ARD-K）。
查找：`gh issue list --state all --json number,title --limit 1000` 取全部 issue，按标题精确匹配。
创建：`gh issue create --parent <母工单号> --blocked-by <编号>`，创建时直接带上子工单和依赖关系（DSGN-N）。
只有旧的自建 GitHub（GHES）不认这个参数时，才退回在正文 "Blocked by" 行写 `#编号`。
gh 没装或没登录时，停下并提示，不自动退回本地。

**DSGN-J 本地适配器。** 每张工单一个文件：`docs/features/<f>/raw/state/spec-ticket/issues/IMPL-X-<slug>.md`，和 wayfinder 的进度图同在 `raw/state/` 下（PRD-B、ARD-J）。
slug 是标题转小写后，非 `a-z0-9` 的连续字符换成一个短横线、去掉首尾短横线；结果为空（如纯中文标题）就省略，文件名为 `IMPL-X.md`。文件名带 IMPL ID，所以文件名本身就是对应关系，本地模式不用对应表；"查找"就是看文件在不在。
母工单是同目录的 `_feature.md`；每个 IMPL 文件带一行 `Parent: _feature`（DSGN-N）。
"Blocked by"行写被依赖工单的 IMPL ID 和文件名。`docs/features/**/raw/` 被 git 忽略（`.gitignore`）。

**DSGN-K Jira 适配器。** 用 Jira REST API v3（curl 调用），连接信息来自环境变量（PRD-G、ARD-I）：
JIRA_BASE_URL、JIRA_EMAIL、JIRA_API_TOKEN、JIRA_PROJECT_KEY；缺任何一个就停下，不退回本地。
查找：`POST /rest/api/3/search/jql` 按项目和标题搜，再按标题精确匹配。
母工单建成 Epic；每张 IMPL 工单的 `parent` 字段设为这个 Epic（DSGN-N）。
创建：`POST /rest/api/3/issue`，正文用 ADF（Atlassian 的 JSON 文档格式），标签 `ready-for-agent`。
阻塞边：开完被挡住的工单，立即用 `POST /rest/api/3/issueLink` 建类型为 Blocks 的链接。
本机没有 Jira，这一路没有实测过，链接方向要先在测试项目里核对（见 Risks）。v3 只适用于云版，自建版见 QUES-B。

**DSGN-L 运行报告。** 结束时在对话里报告，不写进任何 spec 文档（PRD-F）。
内容有：用了哪个 tracker；新开了哪些工单（IMPL 对工单号）；跳过了哪些已有的；
依赖不一致、指向不存在 ID、被删或改动的 IMPL；以及没打上的标签。

**DSGN-M 取代 to-tickets。** SKILL.md 写好、用户确认可用后，在同一次改动里删除 `skills/to-tickets/`（PRD-I、ARD-H）。
要改的文件就是 `grep -rln 'to-spec\|to-tickets'` 找到的每一个（to-spec 同时由 spec-ingest 取代）。
改前搜一次定清单，逐处改；改完再搜一次，确认没有残留。

**DSGN-N 母工单。** 每个 feature 一张，标题 `[<f>] feature`，正文只放 PRD 和 design 的仓库路径（PRD-J、ARD-O）。
最先建它，之后每张 IMPL 工单建时都挂在它下面。重跑时按对应表或标题找回它，不重建。

## Testing Decisions

只测外部行为：给定 impl-plan 和配置，看 tracker 上（或本地 issues 目录里）出现了什么，不测内部怎么解析。
主要测试用一个固定的小 feature 做夹具（fixture，即事先准备好的测试输入），放在 `skills/spec-ticket/tests/` 下。
夹具的 impl-plan 有四条 IMPL：一条无依赖，两条依赖它，一条依赖那两条；其中一处只在一边写了依赖。
用 `tracker: local` 跑一次，期望得到 `_feature.md` 加四个 IMPL 文件、正确的 "Blocked by" 行，报告里列出那处不一致。
再跑一次，期望文件都不变。加一条新 IMPL 后再跑，期望只多一个文件。
第二个夹具是真实的 `docs/features/spec-driven-development/impl-plan/`：期望已完成的 IMPL（如 IMPL-A）不开工单，非 IMPL 的依赖文字都进报告。
另备两份反例夹具：design 里有一行 Blocking 写 `是` 的中文 QUES，期望拒绝运行；依赖成环，期望停下并报出环。
`tracker: jira` 但缺环境变量时，期望停下报错、不产生任何文件；真正的 Jira 没有测试环境（见 Risks）。
GitHub 适配器只在一个专门的测试仓库里人工跑一次，不进自动测试，因为它会在网上真的开 issue；人工跑时删掉对应表再跑一次，期望不开重复 issue（DSGN-H）。
本地结果由 `tools/check_spec_ticket_fixture.py` 检查：agent 跑完后，它把 issues 目录的文件名和 Blocked by 行与夹具的期望清单比对（ARD-N）。
选脚本不选人工清单：重跑、删表这类检查要反复做，人工逐个比对容易漏。

## Out of Scope

双向同步、把工单状态写回 spec（PRD-F）。
重新切分工作（纵向切片）；写 spec 文档（spec-ingest、spec-write）；写代码（implement）。
`docs/features/downstream-delivery/` 已原地改写为新 skill（spec-ingest 的 ARD-N）。

## Further Notes

用户对本 skill 的定位是演示和跟踪，还没发现效率或准确度上的实际收益（PRD 的 Goals 一节）。
上游 skill 的需求见 `docs/features/skill-factory/features/spec-ingest/prd/spec-ingest-prd.md`。
被取代的旧 skill 的现状见 [to-tickets design](../../to-tickets/design/to-tickets-design.md)。

## Alternatives Considered

沿用 to-tickets 的纵向切片加用户审拆法：被否决，impl-plan 已切好（ARD-B）。
把工单号写回 impl-plan，或同步工单状态：被否决，用途只是演示，同步代价大（ARD-D）。
Jira 只留接口（ARD-F）：被取代，用户要保留给其他人用，改为真实适配器（ARD-I）。
Jira 改用 ankitpokhrel/jira-cli：没采用，要多装一个工具；REST API 只要 curl（ARD-I）。
没配置 tracker 时报错停下：被否决，改为缺省写本地（ARD-C）。

## Drawbacks

依赖是从中文或英文的散文行里读出来的，写法稍有变化就可能漏读（DSGN-D）。
对应表不进 git，多台机器各有一份；只能靠按标题查找来避免重复（DSGN-G、DSGN-H）。
工单不跟着 impl-plan 更新：IMPL 改了文字，工单上还是旧的（DSGN-H）。
用户自己说还没看到实际收益；维护这个 skill 的成本可能高于它的价值。

## Risks and Mitigations

| 风险 | 缓解 |
|---|---|
| 依赖读错，阻塞边连错或漏连 | 两边取并集，不一致的地方写进报告（DSGN-F）；夹具专门测单边依赖 |
| 换机器后对应表丢失，GitHub 上开出重复 issue | 开新工单前按带 feature 和 IMPL ID 的标题查找（DSGN-E、DSGN-H） |
| 误把工单发到公开仓库 | 缺省写本地（DSGN-C）；发到网上前请用户确认一次（QUES-F） |
| `docs/features/downstream-delivery/` 还描述 to-spec 和 to-tickets，新 skill 上线后成为过时的重复文档 | 已原地改写（spec-ingest 的 ARD-N） |
| Jira 这一路本机没有实测（没有 Jira），链接方向或字段格式可能不对 | 第一次用真实 Jira 时，先在测试项目开两张票核对（DSGN-K） |
| 移除 to-tickets 后有残留引用，形成断链 | 改前改后各全仓搜索一次（DSGN-M） |

## Open Questions

| ID | 问题 | 目前答案 | Owner | Blocking |
|---|---|---|---|---|
| QUES-A | 除了每条 IMPL，要不要也为 spec 本身开一张工单？用户以前说过"spec 本身也得有一个ticket"（to-spec PRD-D） | 已定：每个 feature 一张只放链接的母工单（ARD-O、DSGN-N）；spec 仍是文档（`skills/wayfinder/SKILL.md` 第 282、292 行） | cicidi | no |
| QUES-B | 将来接的 Jira 是云版（Jira Cloud）还是自建（Data Center）？ | UNKNOWN；DSGN-K 按云版的 REST API v3 写 | cicidi | no |
| QUES-C | tracker 配置放在 CLAUDE.local.md 的一行 `tracker:`、缺省用本地，用户同意吗（Q4 未答）？ | 按协调者推荐暂定（ARD-C），信心中等 | cicidi | no |
| QUES-D | downstream-delivery 的 spec 在新 skill 上线后怎么处理：删除、标为过时，还是改写？ | 已定：原地改写（spec-ingest 的 ARD-N） | cicidi | no |
| QUES-E | 新 IMPL 挡住旧 IMPL 时，给旧工单补阻塞边，算不算违反"不改已有工单"？ | 暂定补边，只加边，不改标题和正文（DSGN-H） | cicidi | no |
| QUES-F | 发到 GitHub 或 Jira 前，要不要先请用户确认一次清单？ | 暂定要（本设计自己的选择，见 Implementation Decisions） | cicidi | no |

## Reversibility

本 spec 只新增文档，还没有任何代码；删掉 `docs/features/skill-factory/features/spec-ticket/` 即可撤回。
将来的 SKILL.md 和移除 to-tickets 的那次改动都在 git 里，用 `git revert` 可撤回，to-tickets 可从历史取回。
本地工单和对应表在被忽略的目录里，直接删文件即可。
GitHub 和 Jira 上已开的工单通常只能关闭，删除需要管理员权限，这是最难撤回的一步，所以缺省不发到网上（DSGN-C）。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：spec-ticket 的前瞻式 design，DSGN-A 到 DSGN-M，引用 PRD-A 到 PRD-I |
| 2026-11-24 | 按审查报告改 DSGN-B、C、D、E、F、G、I、J、K、M，测试与风险；Jira 改真实适配器（ARD-I 到 ARD-N） |
| 2026-11-24 | 加 DSGN-N 母工单，改 DSGN-I、J、K；QUES-A 由 ARD-O 回答 |
| 2026-11-24 | 写 SKILL.md 时补：已完成的判定和它的边（DSGN-D、F）、slug 规则（DSGN-J）；本地测试去掉对应表 |
| 2026-11-24 | QUES-D 已定：downstream-delivery 原地改写（spec-ingest 的 ARD-N） |
