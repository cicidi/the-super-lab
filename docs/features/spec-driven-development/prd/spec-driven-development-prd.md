---
feature: spec-driven-development
type: prd
state: draft
health: active
owner: cicidi
last_verified: 2026-11-04
---

# Spec-Driven Development — PRD

## Overview

本 PRD 定义 spec-driven development：用 PRD、decision-history、design 篇、impl-plan、test-plan 五篇，把有门槛的问题分析清楚，并交给四个 skill（spec-pipeline、spec-organize、spec-review、spec-write）执行。

## Problem Statement

今天，AI 模型的能力已经非常强大。它们可以阅读、搜索最新、最前沿的技术，帮助我们解决问题。

但是，问题是什么？

### 1. Problem 经常没有被定义清楚，更何谈解决

比如这样一个问题：

> 嘿，AI，我买 iPhone 18 Duo 还是 iPhone 18 基础版？

看似是一个简单的问题，但实际上，我们并没有告诉 AI 我们的真实需求。

比如：我们买新的 iPhone 是用来做什么的？我们的 budget 是多少？我们之前是否一直使用 iPhone？我们喜欢 iPhone 的哪些优点，又有哪些缺点？

这些 context，AI 并不知道，因此 AI 的推荐肯定不会准确。

这正是很多人抱怨 AI 不好用的原因。事实上，对于我们自己来说，这看似是一个清楚的问题，但实际上，可能不是 AI 不好用，而是人没有把 problem 定义好。

### 2. AI 真正赋予我们的 superpower，是帮助我们发现 unknown

在我们把问题问清楚以后，AI 也提供了一些思路，甚至 solution。

但是，由于人的能力有限，我们可能根本没有见过某些解决方法或方案。

我们利用已知的信息，找到我们不知道自己知道的信息，同时学习我们知道自己不知道的知识，最后把我们不知道、甚至不知道自己不知道的 blind spot 发掘出来。

这才是 AI 真正赋予我们超能力的地方。

### 3. Decision 不断变化，AI 需要理解、记录并同步这些变化

经常，我们做了一段时间，或者和 team 里的其他人讨论后，会发现一些 decision 一直在改变。

比如：我们买 iPhone 的 budget，和父母、妻子商量未果。我们之前说买 iPhone 的 budget 是 2,000 美金，现在突然变成了 1,000 美金，那么 AI 整个 decision 的方向就会发生彻底的转变。

紧接着，一系列新的问题又会被引入：去哪里买？是不是能够接受二手 iPhone 18 Duo？

当然，随之而来的，去哪里买、如何找 deal 等具体实现方式都会发生改变。

今天的例子比较简单，以后可能会有更复杂的例子：多个人做出多个 decision，到底谁是真理？而这个真理，可能还需要 impact、覆盖其他一些之前的 decision。

比如：爸爸的 budget 是 1,800 美金，妈妈说 1,500 美金；爸爸说下个月可以买，妈妈说这个月可以买。

到底谁是真理？根据这个真理，我们又要如何修改之前的 decision？

这里真正的问题是：当多个参与者做出不同的 decision 时，AI 如何理解这些 decision 之间的关系，判断哪些 decision 是有效的，并根据最新的 decision 更新整个 decision-making process？

### 4. 即使 problem、solution、update、sync 都做好了，人依旧是整个 AI 世界最大的 bottleneck

首先是阅读。

怎么让文件好读、好懂？文件怎么好查找？如何清晰地知道每个文件是做什么的？如何做好 file management？

大的项目不可能只有一个 spec，那么如何切分 spec？如何让不同的 spec 之间保持清晰的关系？以后 AI 和人又该怎么读、怎么查找？

当项目越来越大，文件越来越多，spec 越来越复杂时，我们如何让人和 AI 都能够快速理解整个项目，并准确找到自己需要的信息？

这些都是 AI 真正落地到实际工作中，需要解决的问题。

### 5. 有门槛的难题不只在软件里

盖一个 shed、去北京旅游、看懂一道著名数学题、不靠猜地分析一只股票——人往往从没做过，不知道怎么拆、盲区在哪、哪些要自己拍板。

AI 要把大问题拆成小的：能查的 AI 自己查（合规、财报、交通），要选的人来选（预算、偏好、风险），人想不到的 AI 主动问。spec 既是学习笔记，也是决策记录，最后交给 AI 执行。

## Goals and Success Metrics

- 目标：任何有门槛的难题都能拆成可查、可决策、可执行的小问题。
- 验收：四个 skill 的测试结果（test-plan）；这不是产品 success metric。
- PRD-G 的产品级 success metric 与 baseline 仍 deferred（ARD-N）。

## User Stories

- 作为写 spec 的人，我希望先被 interview，把已知/未知/盲区问出来。
- 作为 reviewer，我希望机械 MUST 和语义缺陷都能检出，且建议可执行。
- 作为执行者，我希望 spec 能落到 design/impl-plan，并有 mock 执行与可追溯证据。

## Solution

**Spec-driven development**

我们不重复什么是 spec-driven。这里要做的是开发一些 skill；这些 skill 会在一起工作，而不是单个 skill。这些 skill 的目标是：通过一组 skill，把具体问题分析清楚。

**PRD、decision history、design 篇 是互相打磨的循环**，不是只走一遍的直线；循环收敛到「够稳」后，**impl plan** 与 **test plan** 各自独立：都从 **design 篇** 总结出来，彼此不串行依赖。

1. **PRD** — 我们到底要做什么、解决什么；当前的 limitation 是什么；preference 是什么；timeline、各种 resource、tool 都有什么。design 篇 或 decision 暴露缺口时，回到 PRD 改 requirement。
2. **Decision history** — 基于 PRD 作出 decision；任何跟产品方向相关的 decision 先 update decision history（约 50% AI、50% 人）。新 decision 可能改 PRD 范围；spec 里的 trade-off 也可能要求补 decision。
3. **Design 篇** — 与 PRD、decision 并行迭代：写设计（技术方案、contract、tool 等；HLD/LLD 不在此展开）。设计问清 problem、或发现 decision 不够，回到 1/2 继续磨。
4. **Impl plan** — 从 design 篇 总结实现：先做什么、后做什么；各个 task 的细节、准备工作等（不依赖 test plan 先写完）。
5. **Test plan** — 从 design 篇 总结验证：任务完成标准、可用性检查、regression guard（不依赖 impl plan 先写完）。

## Functional Requirements

**PRD-A** — 做一个 pipeline，基于现在现有的 pipeline 做一些改进。

**PRD-B** — 做一些 skill；这些 skill 其实就是优质 prompt，或其他 popular 的 prompt，引导 AI 怎么工作：完成 spec 的书写、命名、校验、更新。

**PRD-C** — 每次改动不超过 **10 行** **或** **200 字符**；超出拆多次，restructure 需 human 授权。

**PRD-D** — 文档大小限制在 1000 行；太大几乎没法 maintain。

**PRD-E** — 文档的文件组织架构、folder 关系。

Additional constraints:

**PRD-F** — 多人 decision 冲突时，以 decision history 里时间较晚的那条为准。看不出先后就问用户。AI 不猜测谁为准。

**PRD-G** — （open）产品级 success metric 与 baseline — deferred，见 **ARD-N**。test-plan 的分数是 eval 指标，不是产品 success metric。

**PRD-H** — Spec-driven development 的 workflow 尽量使用 popular skill，不要自己重新发明。

**PRD-I** — 修改需要验证；没有能验证的，都需要在 spec 里面标注上。标明后不作为 test plan 的通过条件。

**PRD-J** — 提供 **spec-pipeline** skill：凡写/改 feature spec 经 pipeline 进入；编排 spec-organize / spec-write，提交 committed 变更前询问 spec-review；支持 recap 与轻量 state（feature 确定前 CLAUDE.local，之后 `docs/features/<f>/raw/state/`）。

**PRD-K** — 范围不限软件：任何有门槛的难题走同一套 spec。例子四个：盖 shed（合规、成本、施工）、北京旅游（行程、住宿、风险、预算）、看懂著名数学题（零基础逐步学）、分析股票（基本面、财报、新闻，有理有据）。这轮不在本仓库建 gold，放到别处。

**PRD-L** — 每个子问题标明归属：AI 查、人决定、或 AI 查完后人决定。人没问到的盲区和风险，AI 必须主动提出。

**PRD-M** — 把人讲明白是硬需求。交付前由一个 LLM 打分：它假设自己是一个本科水平的程序员真人，只按能不能看懂来判；看不懂不算交付。测试验不了，不作为通过条件。

**PRD-N** — 正式 spec 的结论必须能追溯到查到的事实（合规条文、财报、新闻、定义），不靠猜；查不到的标成未知。评测时答案只能来自 context 包。

**PRD-O** — 执行不真下单、不订票。一个共用 mock MCP server，若干固定工具；client call 打出 log 即算交付成功。

**PRD-P** — 最终交付是这一系列 skill（spec-organize、spec-review、spec-write、spec-pipeline）。它们引导人写出的 spec，要满足 PRD-K 到 PRD-O。

**PRD-Q** — 书写、命名、校验、更新，以及 PRD-K 到 PRD-O，都是需求。四个 skill 不限于这几件事，以后的新题也要能做。skill 正文要写出四个例子：盖 shed、北京旅游、数学题、股票。好不好用只看测试。

## Out of Scope

- 真实下单、订票、交易；执行只到 mock MCP log。
- 多人 decision 的仲裁细则；按 decision-history 时间，仍看不出则问用户。
- 本仓库不建非软件四例的 gold；例子写进 skill 正文，gold 放到别处。
- 存量不合规文档的批量迁移。
- skill / spec 的版本与迁移策略。

## Resources Needed

- 四个 skill + 一份 test plan;无外部服务、无数据库。
- 评测需 `deepseek-flash` API 与 3 次 run 的预算;runs/reports 不入库(ARD-AD)。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-04 | 新增 Problem 5：有门槛的非软件难题（shed、北京旅游、数学题、股票）要拆成可查/可决策的小问题，spec 兼学习、决策与执行 |
| 2026-11-04 | 新增 PRD-K：范围覆盖非软件难题，四个 gold example |
| 2026-11-04 | 新增 PRD-L：子问题归属（AI 查 / 人决定 / 查完再决定）；AI 主动暴露盲区与风险 |
| 2026-11-04 | 新增 PRD-M：可读性硬需求，LLM 以本科程序员真人身份按「能不能看懂」打分 |
| 2026-11-04 | 新增 PRD-N：结论必须追溯到查到的事实；查不到标未知 |
| 2026-11-04 | 新增 PRD-O：执行用 mock MCP client/server，call 打出 log 即成功 |
| 2026-11-04 | 新增 PRD-P：交付是 spec-organize / spec-review / spec-write / spec-pipeline，写出的 spec 满足 PRD-K 到 PRD-O |
| 2026-11-04 | 新增 PRD-Q：skill 不绑定具体题目，以后的新题也要能做；正文是否点名例子未定，验收只看测试 |
| 2026-11-04 | PRD-F 关闭延期：按 decision history 时间较晚者；看不出先后则问用户；AI 不猜测 |
| 2026-11-04 | 选择题：G/H/J 维持；I 验不了的不进测试；K 的 gold 放到别处；M 测不了；N 评测只用 context；O 共用一个 mock server；Q 正文写出四个例子 |
| 2026-11-04 | 补 frontmatter、Overview、Goals and Success Metrics、User Stories、Out of Scope；Requirements → Functional Requirements |
| 2026-11-04 | PRD-C 改为硬上限 10 行或 200 字符；PRD-G 区分 eval 分数与产品 metric；Solution 术语改 design 篇 |
