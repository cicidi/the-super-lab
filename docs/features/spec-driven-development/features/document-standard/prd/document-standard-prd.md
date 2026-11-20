---
feature: document-standard
type: prd
state: draft
final_date: 2026-11-20
health: active
owner: cicidi
last_verified: 2026-11-20
---

# Document Standard（PRD 入口）

## Overview

document-standard 规定 spec 文档怎么写：有哪几种文档、放在哪里、文件怎么命名、编号怎么起、什么内容不能删。这些要求本身已经写在 [parent PRD](../../../prd/spec-driven-development-prd.md) 里（PRD-B 到 PRD-F，以及 PRD-M 的可读性要求），具体做法写在 [document-standard design](../design/document-standard-design.md)。

本篇是入口文件。按 [ARD-BQ](../../../decision-history/spec-driven-development-decision-history.md#ard-bq)，一种文档拆成分篇时，必须有一个入口文件链到各分篇。

## Goals and Success Metrics

本篇没有单独的目标，目标见各分篇和 parent PRD。

## User Stories

见分篇。

## Functional Requirements

本篇不新增需求。分篇如下：

| 分篇 | 讲什么 |
|---|---|
| [给人读的 HTML 页面](document-standard-prd-spec-reader-html.md) | 把已提交的 spec 生成一个网站，左侧目录列出所有 feature，读者不用打开 markdown 也能读懂 |

## Non-Functional Requirements

见分篇。

## Out of Scope

- 把 parent PRD 里的文档标准要求在这里再抄一遍。

## Resources Needed

无。

## Change Log

| 日期 | 改了什么 |
|---|---|
| 2026-11-20 | 新建入口文件，链到 reader HTML 分篇（ARD-BQ） |
