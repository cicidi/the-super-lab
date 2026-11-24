---
feature: tmux-status-bar
type: prd
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# tmux-status-bar — 需求

本篇从过去的对话和提交记录里，整理用户对 `tmux-status-bar` 这个 skill 的需求。
实现见 [design](../design/tmux-status-bar-design.md)，决策见 [decision-history](../decision-history/tmux-status-bar-decision-history.md)。
opencode 会话按 ses_ 前缀引用（本机 opencode.db）；Claude Code 会话按 id 前 8 位引用（history.jsonl、analytics.db）。

## Overview

tmux 是终端复用器，一个终端里可以开多个会话（session）和窗格；底部那一行叫状态栏（status bar）。
本 skill 把状态栏改成显示：会话名、项目文件夹、git 分支、git 状态、当前 coworker feature。
需求最早出现在 2026-06-09：用户要把状态栏改成灰色，并显示项目路径、分支和会话创建时间（ses_15012457）。
2026-07-01 用户再次提出，并说"把这个做成一个skill 放在coworker 里面"（ses_0e39cb88），当晚提交为 commit 5cc3d4b。
之后用户的要求又变了三次（PRD-I、PRD-J、PRD-K），但 SKILL.md 一直没有跟上，见 design 的 DSGN-H。

## Goals and Success Metrics

目标一：切换窗格时，不用敲命令就能看清自己在哪个项目、哪个分支（ses_1500d37d，2026-06-09）。
目标二：同时看到当前在做哪个 feature（当年叫 initiative）（ses_0e39cb88，2026-07-01）。
目标三：配置可以复用，重装或换机器时让 agent 照着 skill 重做一遍（同一会话，PRD-H）。
成功指标：UNKNOWN。对话里没有给出可量化的指标。

## User Stories

- 作为开发者，我开了很多 tmux 窗格，想一眼看出每个窗格所在的项目和分支。
- 作为开发者，我想在状态栏上看到有没有未提交、未推送的改动。
- 作为开发者，我只说一句"customize tmux"，agent 就能把状态栏配好。

## Functional Requirements

**PRD-A 显示项目文件夹。** 用户原话："显示当前project 的folder"（ses_0e39cb88，2026-07-01）。
更早时用户要的是完整路径（ses_1500d37d，2026-06-09）；7 月 1 日改成只显示文件夹名。

**PRD-B 显示 git 分支。** 用户说"在tmux bar 里面显示当前project 的branch"（ses_1500d37d，2026-06-09），7 月 1 日再次列入（ses_0e39cb88）。

**PRD-C 显示 git 状态。** 用户原话要的是"git tree"（ses_0e39cb88，2026-07-01）。
agent 认为完整的提交图太宽，改成显示领先、落后、暂存、未跟踪的文件计数，用户没有反对。
"git tree"的本意属于 UNKNOWN，见 design 的 QUES-A。

**PRD-D 显示当前 feature。** 用户要显示"intiative"（ses_0e39cb88，2026-07-01）；2026-09-24 全仓库把 initiative 改称 feature（commit c2b3f22）。
2026-07-13 用户要求"the initiative should read from claudel.local.md"（ses_0a12a0e1）。
当前 SKILL.md 仍读 `.coworker/features/.active` 文件，见 QUES-B。

**PRD-E 显示会话创建时间。** 2026-06-09（ses_15012457）和 2026-07-01（ses_0e39cb88）两次都提到"session 创建时间"。

**PRD-F 每个值前面带字段名。** 用户要显示会话名，"每一个value 前面也有一个 fieldname"，例如 `branch:master`（ses_0e39cb88，2026-07-01）。
会话本身不改名，而是像其他字段一样显示成 `tmux:名字`；用户说"不用tmux_ prefix"（同一会话）。

**PRD-G 状态栏用深灰底色。** 用户说"改成灰色的"，随后又说"再暗一点"（ses_15012457，2026-06-09）。

**PRD-H 做成个人 skill。** 用户说"把这个做成一个skill 放在coworker 里面"（ses_0e39cb88，2026-07-01）。
agent 问放在哪里、用什么触发词，用户选了 personal-skills 和"customize tmux"（同一会话）。

**PRD-I 在 worktree 里显示 worktree 名。** 用户要求"还要显示 worktree: {name} 放在project 下一个"（ses_0dc6469a，2026-07-02）。
worktree 指同一个 git 仓库在另一个目录里检出另一个分支。
这项只写进了 walter-worker 的脚本（commit 579ad50、9edd66d），SKILL.md 没有。

**PRD-J 显示 AI 会话信息，可分两行。** 用户要加上 Build/Plan 模式、模型、effort、ctx 百分比、cost 和当前路径（ses_0a12a0e1，2026-07-13）。
放不下就"go next line"，所有值动态刷新；随后又要了颜色和 emoji（同一会话；walter-worker commit 87f4413）。
SKILL.md 没有这些内容。

**PRD-K 状态栏只显示当前文件夹路径。** 2026-08-01 用户说"tmux 的bar 不用显示那么多数据了， 只要一个当前的 foder path 就行了"（c173b9ed）。
这是用户最新的要求，和 PRD-A 到 PRD-F 冲突；当前 SKILL.md 仍按 7 月 1 日的版本做，见 QUES-C。

**PRD-L 改外观前先征得同意。** 2026-08-01 用户要求安装 tmux 定制前"需要给用户提示确定才能安装"，且"对大家的claude tmux 没有影响"（13f2d9db）。
这句话针对的是 walter-worker 的安装脚本；是否也约束本 skill，属于 UNKNOWN，见 QUES-D。

## Out of Scope

通用 tmux 配置（快捷键、插件、配色）和 tmux 以外的提示符定制不归本 skill（SKILL.md 的 When NOT to Use 一节）。
会话保存插件另有安排：2026-05-06 用户要求把 tmux-resurrect 插件的安装做成单独的 tmux-setup skill（b2741719）。

## Resources Needed

需要 tmux 3.x、git 和 POSIX sh；feature 字段依赖 coworker 写出的 `.coworker/features/.active` 文件（SKILL.md）。
人力上，用户只需说一句触发词（PRD-H）；改完 `~/.tmux.conf` 后要重新加载配置才能看到效果。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：从过去的对话和提交记录反推 tmux-status-bar 的 PRD |
