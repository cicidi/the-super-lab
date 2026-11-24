---
feature: luma-event-scout
type: design
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# luma-event-scout — Luma 湾区活动筛选

本篇说明 `luma-event-scout` 这个 skill 现在怎么工作。
源文件：`personal-skills/luma-event-scout/SKILL.md`，按 git 已提交的版本描述（最后改动是 commit 40a10e4）。

## Problem Statement

Luma 上湾区 AI 活动很多，质量参差，不少是小公司借活动推广产品（PRD-K）。
Luma 网页是 SPA（single-page application，单页应用，内容由浏览器里的 JavaScript 渲染）。
直接抓网页拿不到日期，而且只看一个社区的页面会漏掉很多活动（PRD-M）。

## Solution

一个 personal skill：用 Luma 网页自己调用的公开接口拉活动，按固定偏好过滤，再逐个查演讲人背景。
输出一份双清单：推荐，和强力不推荐。用户同意后，可以用 Playwright 代为报名。

## User Stories

- 作为用户，我说"scout Luma"或"find me events"，skill 自动跑完整个流程，写出清单。
- 作为用户，我回复 `+N` 或 `-N` 表示对第 N 场有兴趣或不去；回复 `+N register` 让 agent 报名。

## Implementation Decisions

skill 放在 `personal-skills/`，不在公共的 `skills/` 目录，因为标准是用户个人的（PRD-A）。
抓取用 Python 标准库 urllib 直接调接口，不需要登录或 API key（commit 24d4264）。
SKILL.md 里的代码是给 agent 照着写的示例，目录里没有可直接运行的脚本。

## Design

**DSGN-A 触发与依赖。** 用户要找湾区 AI 活动时触发（frontmatter 的 triggers）。默认偏好不再每次确认（PRD-A）。
唯一声明的外部依赖是 maigret，用 `pip install maigret` 安装（PRD-E）。

**DSGN-B 地点、窗口和时段。** SF 与半岛、南湾同等优先；东湾只在演讲人特别强时才考虑（PRD-B）。
偏好一节写只搜一个月内（PRD-D）；但过滤代码里是 `WINDOW_DAYS = 10`，两者不一致，见 QUES-A。
周末最优先，工作日下午 4 点以后其次；工作日 4 点前的活动，除非演讲人极强，否则跳过（PRD-C）。

**DSGN-C 活动类型和 hackathon。** 要讲座、炉边谈话、demo、论文讨论；不要纯社交活动和入门工作坊（PRD-G）。
hackathon 和讲座同一标准，演讲人或评委也要过硬门槛，另加三条（PRD-L）。
奖金必须有现金或礼品卡，只给平台或 API credit 的拒绝。
主办方须是大厂，或 B 轮以上、有知名产品的 startup。现金奖金池 1K 美元以上算加分信号。

**DSGN-D 演讲人硬门槛。** 每个演讲人和主办方必须满足一项：牛校、大厂，或有真实产品的公司的 VP 以上（PRD-E）。
背景检查分五步：maigret 用户名搜索、LinkedIn、GitHub、Google Scholar 或 arXiv、公司是否真实。
除 Luma 主页外查不到任何公开痕迹，或公司只有一个落地页，都直接判不通过。
通过的人要在卡片上写证据标签，例如"大厂 Google Director"。

**DSGN-E 产品分析。** 有产品演示的活动，要判断它是不是"AI 包装皮"，即只在 ChatGPT 或 Claude 的 API 外面套一层（PRD-K）。
降级信号有：能被 Claude 自定义指令或开源方案替代、用户极少、只有原型。
正面信号有：自有模型或数据、真实留存的用户、开源社区。SKILL.md 还列了几个过去被拒的例子。

**DSGN-F 话题、费用和文化过滤。** 话题须为中高级，分 8 类按优先级排：agent 类最高，其次是 LLM 架构、agent 记忆和 MCP（PRD-G）。
电影动画、医疗生物也在 8 类之中。这段话题规则前面缺了小节标题，读起来像接在产品分析后面，见 QUES-H。
只要免费活动（PRD-H）。标题或描述是中文的活动跳过（PRD-F）；这是否就是用户的原意，见 QUES-D。

**DSGN-G 抓取方法。** SKILL.md 记录了四种方法的演进，只有第四种管用（PRD-M）。
直接抓网页拿不到日期；页面内嵌的 `__NEXT_DATA__` JSON 只有首屏约 20 场；
Playwright 下拉后，日期标题和活动卡片在不同的 DOM 树里，对不上。
第四种是调公开接口 `calendar/get-items`，按游标分页拉某个 calendar 的全部活动。
请求要带 User-Agent 和 Referer 两个请求头，否则返回 403。

**DSGN-H calendar 链式发现。** Luma 的 calendar 是组织者或社区的页面，不是话题分类（1de9cb65，2026-07-23）。
做法是从湾区最大的聚合 calendar（Bond AI）出发，收集它的活动里出现的其他 calendar id（PRD-M）。
再加上一份手工维护的 EXTRA_CALENDARS 列表（已提交版本有 9 个），全部拉取，按活动 URL 去重。
抓活动详情页时，还要从 HTML 里提取新的 calendar id 并拉取（Strategy 0c）。
每次发现新 calendar，必须写回 SKILL.md 的 EXTRA_CALENDARS，供下次使用（commit e5a4b84）。

**DSGN-I 过滤和详情。** 接口数据按湾区城市名单和日期窗口过滤；城市为空的活动也保留（PRD-B、PRD-D）。
接口不给演讲人信息，所以每个候选都要再抓详情页，拿描述、演讲人和场地（Strategy 1）。
命中 agent、MCP、Claude Code 等关键字的活动，不管报名人数都要抓详情（Strategy 0d）。
原因是需审批的活动，接口里的报名人数显示为 0（commit e5a4b84）。

**DSGN-J 输出。** 清单写到 `~/project/luma/events-{YYYY}-{MM}.md`（PRD-I）。
每场一张卡片，用两列表格写：时间（含周几）、地点、内容、类型、演讲人和主办方背景、要做什么、报名人数（PRD-J）。
卡片后是两张汇总表：推荐（必须带演讲人证据标签）和强力不推荐（必须写具体理由）（PRD-K）。

**DSGN-K 偏好学习。** 偏好存在 `~/project/luma/preferences.json`，记喜欢和不喜欢的话题、演讲人、形式（PRD-I）。
出清单后请用户回复 `+N` 或 `-N`，记进文件；下次给相似的活动加分或减分。是否真在生效，见 QUES-F。

**DSGN-L 自动报名。** 只有用户回复 `+N register` 才报名，绝不自主报名（PRD-N）。
报名前再确认三件事：活动仍在一个月内、免费、这一场确实得到了同意。
表单数据从 `~/.person_info.md` 读，不写死在 skill 里（PRD-O）。
不认识的字段合理猜测或填 N/A，绝不留空；下拉框先按关键字匹配；条款勾选框一律勾上。
提交后必须看到"You're going"或待审批之类的页面，再到 Luma 的 my-events 页面确认状态；看不到就重报（PRD-P）。
示例脚本新开一个 Chromium 窗口，没有沿用用户已登录的 Chrome，见 QUES-E。

**DSGN-M 主流程。** Process 一节共 12 步：找候选、抓详情、查背景、过硬门槛、产品分析、其余过滤、分类。
然后写清单、应用偏好、请用户反馈、记录反馈（PRD-I、PRD-K）。
第 1 步仍写"先抓 `luma.com/sf/ai` 分类页"，与 DSGN-G 的结论矛盾，见 QUES-B。

## Testing Decisions

本 skill 没有自动测试或评测集；目录下只有 SKILL.md 一个文件。
SKILL.md 末尾列了 4 个手工测试场景，例如用户说"+1, +3, -5"时要记录反馈。
实际的验收是用户拿已知的好活动链接，问 skill 有没有搜到（PRD-M）。这组链接没有存成固定的测试集。

## Out of Scope

非技术活动、湾区以外的活动、纯社交活动都不管（frontmatter 的 when_not_to_use）。
不用 Luma 官方付费 API，也不接 Luma 的 MCP server（decision-history 的 ARD-G）。

## Further Notes

需求见 [PRD](../prd/luma-event-scout-prd.md)，决策见 [decision-history](../decision-history/luma-event-scout-decision-history.md)。
工作区里的 SKILL.md 有一处未提交的改动（来自另一个会话）：在 EXTRA_CALENDARS 里多加了一个 MongoDB calendar。
本篇按已提交版本描述，见 QUES-G。
`~/project/luma/docs/` 下有一份 2026-07-26 自动生成的 PRD 和决策时间线，可作旁证；它由 LLM 生成，不是用户原话。

## Alternatives Considered

直接抓网页、解析 `__NEXT_DATA__`、Playwright 下拉：都被否决，换成公开接口（ARD-D、ARD-E）。
Luma 官方 REST API：要付费订阅，而且只能查自己的 calendar，被否决（ARD-G）。
只从一个聚合 calendar 搜：会漏掉独立社区的活动，被否决（ARD-A、ARD-D）。

## Drawbacks

链式发现靠社交关系：没跟任何已知 calendar 交叉挂载的独立社区仍会漏（1de9cb65，2026-07-23）。
公开接口没有文档，Luma 改版就可能失效。
每次运行都要改写 SKILL.md 自身（写回新 calendar），skill 文件会一直变；工作区里那处未提交改动就属于这种写回。

## Risks and Mitigations

| 风险 | 缓解 |
|---|---|
| 公开接口加了鉴权或改了格式 | 没有自动缓解；SKILL.md 保留了方法演进表，可以参考 |
| 代为报名时填错信息或报错活动 | 只在用户逐场同意后报名，并要求看到成功页面（PRD-N、PRD-P） |
| 个人资料进入仓库 | 资料改放 `~/.person_info.md`（PRD-O）；但首版资料仍在 git 历史里，preferences.json 也还有资料字段，见 QUES-F |
| 背景检查要搜他人的公开信息 | SKILL.md 只要求在卡片上记职业证据标签；没写其他限制 |

## Open Questions

| ID | 问题 | 目前答案 | Owner | Blocking |
|---|---|---|---|---|
| QUES-A | 搜索窗口是一个月，还是 10 天（PRD-D）？ | 偏好一节写一个月，过滤代码写 10 天 | cicidi | no |
| QUES-B | Process 第 1 步要不要改成先调接口（PRD-M）？ | 仍写先抓 `luma.com/sf/ai` 分类页 | cicidi | no |
| QUES-C | Strategy 1 里残留的 Playwright 下拉代码要不要删？ | 24d4264 说已删，代码还在；代码块没闭合，吞掉了 Preference Learning 标题 | cicidi | no |
| QUES-D | "不要纯中国人的"是指中文活动吗（PRD-F）？ | SKILL.md 按中文标题或描述过滤 | cicidi | no |
| QUES-E | 报名要不要用用户已登录的 Chrome（PRD-N）？ | 示例脚本新开 Chromium；当晚用户选了"方案a"，即自己在有显示器的机器上跑 | cicidi | no |
| QUES-F | 偏好学习真的在用吗（PRD-I）？ | preferences.json 反馈列表为空，最后更新 2026-07-10；文件里还留着资料字段 | cicidi | no |
| QUES-G | 工作区里未提交的 MongoDB calendar 要不要提交（PRD-M）？ | 只在工作区，未提交 | cicidi | no |
| QUES-H | 话题规则要不要补回小节标题（PRD-G）？ | 0a50040 删掉了 "Topic Requirements" 标题，正文留了下来 | cicidi | no |

## Reversibility

对 skill 的改动都在 git 跟踪的 SKILL.md 里，用 `git revert` 即可撤回。
清单、偏好和报名脚本在 `~/project/luma/`，那里不是 git 仓库，删了无法恢复。
已完成的报名，skill 撤不回，需要用户自己在 Luma 上取消。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：按已提交的 SKILL.md 写出 luma-event-scout 的 design，引用 PRD-A 到 PRD-P |
