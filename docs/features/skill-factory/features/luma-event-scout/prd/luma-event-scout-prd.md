---
feature: luma-event-scout
type: prd
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# luma-event-scout — 需求

本篇从过去的对话和提交记录里，整理用户对 `luma-event-scout` 这个 skill 的需求。
实现见 [design](../design/luma-event-scout-design.md)。
决策的来由见 [decision-history](../decision-history/luma-event-scout-decision-history.md)。
opencode 会话按 id 前缀引用（数据在本机 opencode.db）。
Claude 会话按 `~/.claude/history.jsonl` 里的会话 id 前缀引用。

## Overview

Luma（lu.ma）是一个活动发布和报名网站，湾区很多 AI 技术活动发在上面。
`luma-event-scout` 按用户的固定标准，在 Luma 上找值得去的湾区 AI 活动，写成清单。
需求起点是 2026-07-10 的 opencode 会话 ses_0b3308c4。
用户要求"帮我搜一下最近一个月，哪些event 适合我"，并"把我的标准写成一个skill"。
2026-07-23 的 Claude 会话 1de9cb65 大幅收紧了标准，并重做了抓取方法。

## Goals and Success Metrics

目标一：不用自己翻 Luma，就拿到一份符合标准的活动清单（ses_0b3308c4，2026-07-10）。
目标二：只推荐演讲人背景过硬的活动，并列出"去了就是浪费时间"的活动（1de9cb65，2026-07-23）。
目标三：用户知道的好活动，skill 都要能搜到，不漏（1de9cb65，2026-07-23；98e9087f，2026-07-30）。
成功指标：UNKNOWN。用户没有给出可量化的指标。
实际的验收方式是：用户拿漏掉的活动链接追问，见 PRD-M。

## User Stories

- 作为湾区工程师，我想一次拿到未来一段时间内值得去的 AI 活动，不用自己筛。
- 作为听众，我只想听真有背景的人讲，不想给小公司当试用产品的"小白鼠"。
- 作为用户，我选定活动后，想让 agent 替我填表报名，但每一场都要我先同意。

## Functional Requirements

**PRD-A 标准写成 skill。** 用户要求把筛选标准"写成一个skill 放在coworker"（ses_0b3308c4，2026-07-10）。
标准要长期保存，下次不用再确认。当时的 coworker 指 ai-coworker，后改名 walter-worker（commit 40a10e4）。

**PRD-B 地点在湾区。** 最初要求"在bayarea， sf"（ses_0b3308c4，2026-07-10）。
2026-07-23 用户要求"search 整个湾区的包括sf 和南湾， 不光是sf"（1de9cb65）。

**PRD-C 时段。** 周末，或周一到周五下午 4 点以后（ses_0b3308c4，2026-07-10）。

**PRD-D 搜索窗口。** 用户要求"搜索之间限定在1隔越之内的"，即只看一个月内（ses_0b3308c4，2026-07-10）。
之后每次运行，用户会临时给更短的窗口，如"未来10天"（1de9cb65，2026-07-23）、"未来7天"（98e9087f，2026-07-30）。

**PRD-E 演讲人必须是牛人。** 2026-07-10 用户要求查演讲人的 GitHub、LinkedIn、学历，"普通小公司的lead也可以"。
2026-07-23 收紧：每个 speaker 和 host 都要用 maigret 查，"必须需属于要不牛校， 或者在大厂工作过"（1de9cb65）。
maigret 是一个开源工具，按用户名在几百个网站上搜公开账号。不符合标准的活动不推荐。
用户同时说，背景是大牛的话，"产品目前小众一点也没事"（同一会话）。

**PRD-F 不要纯中国人的活动。** 用户原话"不要纯中国人的"（ses_0b3308c4，2026-07-10）。
它指中文活动，还是参加者全是华人的活动，对话里没有再确认，见 design 的 QUES-D。

**PRD-G 话题不太初级，并贴近用户的项目。** 用户已经做过 ai-coworker 这类 deterministic workflow 项目（ses_0b3308c4，2026-07-10）。
话题要尽量贴近这个方向，但"也可以是电影，动画，医疗"（同一会话）。

**PRD-H 只要免费活动。** 用户原话"免费的， 付费的不去"（ses_0b3308c4，2026-07-10）。

**PRD-I 清单落盘，按反馈学习。** 每次的清单写到 `~/project/luma`（ses_0b3308c4，2026-07-10）。
用户会说哪些有兴趣、哪些不去，"以后根绝我的兴趣做优化"（同一会话）。

**PRD-J 输出格式。** 用户要一个表格，列有名字、时间、地点、内容、类型、演讲人和主办方背景、要做什么、报名人数（ses_0b3308c4，2026-07-10）。
随后用户嫌"column 有点太窄了"，于是改成每场一张卡片（同一会话）。
2026-07-17 用户追问，输出里为什么缺"地点，周几， 内容，主办方"（ses_08f79638）。

**PRD-K 产品分析和强力不推荐清单。** 用户要求看活动背后的产品有没有潜力，而不是"单独一层ai包装的皮"（1de9cb65，2026-07-23）。
用户举了刚去过的两场：产品小、用户少，容易被 Claude 或开源方案替代（同一会话）。
清单里还要给出"强力不推荐的， 去了就是浪费时间的"（同一会话）。

**PRD-L hackathon 可以去，但有门槛。** 用户说"hackathon 也可以取"（1de9cb65，2026-07-23）。
主办方要是大厂或明星 startup；奖金要有现金或 gift card，"只给产品credit 的不去"（同一会话）。
奖金门槛是"奖金超过1k都可以"（同一会话）。

**PRD-M 搜全，不漏。** 用户要求"搜luma 的完成的ai topic 而不是某个组织者的"，也"不光是bond ai"（1de9cb65，2026-07-23）。
用户拿漏掉的活动链接追问，要求"不同方法便利"，直到抓到这些活动，再总结原因并 clean up skill（同一会话）。
Bond AI 是湾区最大的 AI 社区 calendar。2026-07-30 又漏了多场，用户要求"hacknight 为什么漏掉了 修一下skill"（98e9087f）。

**PRD-N 同意后才自动报名。** 用户说"如果我同意了，可以利用playwright 帮我报名"（ses_0b3308c4，2026-07-10）。
Playwright 是一个用代码控制浏览器的工具。
用户后来要求用自己已登录的 Chrome 报名，"不要用新的chrome"（1de9cb65，2026-07-23）。

**PRD-O 个人信息不放在 skill 里。** 用户要求个人信息"不要放在skill 里面而是去我本地 ~/.person_info.md 里面拿"（1de9cb65，2026-07-23）。
不知道的字段"猜着填或者就是NA"；简历链接用 LinkedIn（同一会话）。

**PRD-P 报名成功要看到证据。** 用户要求"必须得看到最后的approval 或者pending approval 页面"（1de9cb65，2026-07-23）。
还要在自己的活动页面看到已批准或待批准，"才算成功注册了"（同一会话）。

## Out of Scope

SKILL.md 的 when_not_to_use 写明：非技术活动、湾区以外的活动、纯社交活动都不管。
对话里没找到用户划这条范围的原话，出处属于 UNKNOWN。
用户明确不要接 Luma 官方 API，原话"不用写， 就抓吧"（1de9cb65，2026-07-23）。

## Resources Needed

背景检查要在本机装 maigret（PRD-E）。自动报名要 Playwright 和一个登录过 Luma 的浏览器（PRD-N）。
个人信息在本机 `~/.person_info.md`（PRD-O），清单和偏好在 `~/project/luma/`（PRD-I）。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：从过去的对话和提交记录反推 luma-event-scout 的 PRD |
