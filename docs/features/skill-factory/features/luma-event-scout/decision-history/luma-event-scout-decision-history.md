---
feature: luma-event-scout
type: decision-history
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# luma-event-scout — 决策记录

本篇按时间倒序记录 `luma-event-scout` 这个 skill 的关键决策。
需求见 [PRD](../prd/luma-event-scout-prd.md)，设计见 [design](../design/luma-event-scout-design.md)。
skill-factory 层面按提交逐条记的旧决策（0069 到 0079）在 [parent decision history](../../../decision-history/skill-factory-decision-history.md)。
opencode 会话按 id 前缀引用；Claude 会话按 `~/.claude/history.jsonl` 和 analytics.db 里的会话 id 前缀引用。

## Decision Log

| ID | Date | Decision |
|---|---|---|
| ARD-A | 2026-08-02 | 从活动详情页挖新 calendar，每次发现都写回 SKILL.md；关键字命中的活动必抓详情 |
| ARD-B | 2026-07-23 | 报名成功以成功页面加 my-events 页面的状态为准，看不到就重报 |
| ARD-C | 2026-07-23 | 个人资料移出 SKILL.md，改从本机 `~/.person_info.md` 读 |
| ARD-D | 2026-07-23 | 抓取改用公开接口 `calendar/get-items` 加 calendar 链式发现，删掉失败的方法 |
| ~~ARD-E~~ | ~~2026-07-23~~ | ~~解析页面内嵌的 `__NEXT_DATA__`，再用 Playwright 下拉补全~~ 已被 [ARD-D](#ard-d) 取代 |
| ARD-F | 2026-07-23 | 接受 hackathon，另加奖金、主办方两道门槛，奖金门槛 1K 美元 |
| ARD-G | 2026-07-23 | 不用 Luma 官方付费 API，也不接 Luma MCP，继续抓取 |
| ARD-H | 2026-07-23 | 范围从 SF 扩到整个湾区，半岛和南湾与 SF 同等优先 |
| ARD-I | 2026-07-23 | 演讲人改为硬门槛（牛校、大厂或 VP 以上），加 maigret 检查、AI 包装皮过滤和双清单 |
| ARD-J | 2026-07-10 | 输出从一张宽表改成每场一张两列卡片 |
| ARD-K | 2026-07-10 | 用 Playwright 代为报名，但必须逐场得到 `+N register` 明确同意，绝不自主报名 |
| ~~ARD-L~~ | ~~2026-07-10~~ | ~~演讲人背景五项过一项即可，小公司 lead 也行~~ 已被 [ARD-I](#ard-i) 取代 |
| ARD-M | 2026-07-10 | 把七条标准写成 personal skill，只搜一个月内，用 preferences.json 记反馈 |

## Evidence Appendix

### ARD-A

理由：2026-07-30 用户运行 skill 后，拿 7 个被排除或漏掉的活动链接追问，要求修 skill（98e9087f，PRD-M）。
commit e5a4b84 加了 Strategy 0c、0d 和 5 个新 calendar，并写明"新 calendar 必须写回本文件"。
被否决的方案：只靠 Bond AI 链式发现；按报名人数跳过详情（需审批的活动人数显示为 0）。
出处：history.jsonl 的 98e9087f（2026-07-30）；commit e5a4b84（2026-08-02）。该会话的 agent 回复没有存下来，分析过程属于 UNKNOWN。

### ARD-B

理由：第一次代为报名用的是无界面浏览器，脚本"提交"了 6 场，但看不到结果，用户也没收到确认（1de9cb65，2026-07-23）。
用户随后定下成功标准：看到批准或待批准页面，并在自己的活动页面看到状态（PRD-P）。
被否决的方案：脚本跑完不报错就算成功。出处：1de9cb65（2026-07-23）；commit 04eb9ca。

### ARD-C

理由：用户要求个人资料"不要放在skill 里面"，改放本机 `~/.person_info.md`，专门用于填表（PRD-O）。
被否决的方案：把资料表写死在 SKILL.md 里（6f4608e 首版就是这样，资料进了 git 历史）。
出处：1de9cb65（2026-07-23）；commit e169832。

### ARD-D

理由：用户要求"不同方法便利"，直到抓到他给的几场活动，再总结为什么（PRD-M）。
agent 拦截 Luma 网页下拉时调的接口，发现 `api.luma.com/calendar/get-items` 不需登录，一次找回了全部 3 场。
被否决的方案：直接抓网页、`__NEXT_DATA__`、Playwright 下拉（见 ARD-E）。
出处：1de9cb65（2026-07-23）；commit 24d4264。
24d4264 说已删除 Playwright 下拉，但这段代码仍留在 Strategy 1 里，见 design 的 QUES-C。

### ARD-E

理由：Luma 网页是 SPA，日期由浏览器里的 JavaScript 渲染，直接抓网页拿不到；页面内嵌的 `__NEXT_DATA__` JSON 有日期（commit c4fe0ad）。
它只含首屏约 20 场。用户说页面"要往下拖拽"，要求"用playwright 一直往下load"（1de9cb65，2026-07-23；commit 9e4fb21）。
被取代的原因：下拉后日期标题和活动卡片在不同的 DOM 树里，脚本返回 0 场（SKILL.md 的方法演进表）。同晚被 ARD-D 取代。

### ARD-F

理由：用户说"hackathon 也可以取"，但不能是"给小公司做产品试验的"；只给产品 credit 的不去（PRD-L）。
agent 先把加分门槛写成 1 万美元，用户说"奖金超过1k都可以"，随即改为 1K（commit 0308f52、ff935e3）。
被否决的方案：完全不收 hackathon。出处：1de9cb65（2026-07-23）；commit c629b15、0308f52、ff935e3。

### ARD-G

理由：用户问"luma没有api吗？"和"或者mcp"。agent 查到官方 REST API 要 Luma Plus 订阅（约 59 美元每月）。
而且它只能查自己 calendar 下的活动，帮不了发现别人的活动。用户回答"不用写， 就抓吧"。
被否决的方案：官方 REST API；社区的 Luma MCP server。出处：1de9cb65（2026-07-23）。

### ARD-H

理由：用户说"search 整个湾区的包括sf 和南湾， 不光是sf"（PRD-B）。SKILL.md 写的原因是很多 AI 公司总部在半岛和南湾。
被否决的方案：只搜 SF。出处：1de9cb65（2026-07-23）；commit 74e78bc。

### ARD-I

理由：用户去过的两场活动产品太小、易被替代；要求每个 speaker 和 host 用 maigret 查，必须牛校或大厂（PRD-E、PRD-K）。
"知名独角兽或大公司的 VP 以上"这第三条路，由 agent 写入，用户没有逐条确认。
被否决的方案：五项背景过一项即可（ARD-L）。出处：1de9cb65（2026-07-23）；commit 0a50040。

### ARD-J

理由：8 列的宽表在终端里"column 有点太窄了"；改成每场一个小标题加一张两列表格，每个字段都能占满宽度（PRD-J）。
被否决的方案：一张 8 列的宽表。出处：ses_0b3308c4（2026-07-10）。
2026-07-17 用户又说缺字段（ses_08f79638）；那次之后卡片是否补齐，提交记录里看不出来，属于 UNKNOWN。

### ARD-K

理由：用户说"如果我同意了"才用 Playwright 报名（PRD-N）。agent 据此写成：只在用户回复 `+N register` 后报名。
被否决的方案：不经同意自动报名；完全不做自动报名。出处：ses_0b3308c4（2026-07-10）。

### ARD-L

理由：用户最初说"普通小公司的lead也可以， 最好是有点背景的"（ses_0b3308c4，2026-07-10）。
6f4608e 首版据此写成五项背景过一项即可，小公司 lead 有 GitHub 或论文就行。
2026-07-23 被 ARD-I 的硬门槛取代。出处：ses_0b3308c4；commit 6f4608e、0a50040。

### ARD-M

理由：用户一次给出七条标准，要求"写成一个skill"，清单放 `~/project/luma`，按兴趣反馈优化（PRD-A 到 PRD-I）。
一个月窗口来自用户紧接着的补充。用 preferences.json 存反馈，是 agent 的实现选择，用户没有指定格式。
被否决的方案：每次手动说明标准。出处：ses_0b3308c4（2026-07-10）；首次提交是 commit 6f4608e（2026-07-17）。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：从过去的对话和提交记录反推 luma-event-scout 的决策 |
