---
feature: tmux-status-bar
type: decision-history
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# tmux-status-bar — 决策记录

本篇按时间倒序记录 `tmux-status-bar` 这个 skill 的关键决策。
需求见 [PRD](../prd/tmux-status-bar-prd.md)，设计见 [design](../design/tmux-status-bar-design.md)。
skill-factory 层面只记了一条提交记录（编号 0044），见 [parent decision history](../../../decision-history/skill-factory-decision-history.md)。
opencode 会话按 ses_ 前缀引用（本机 opencode.db）；Claude Code 会话按 id 前 8 位引用（history.jsonl、analytics.db）。

## Decision Log

| ID | Date | Decision |
|---|---|---|
| ARD-M | 2026-11-24 | SKILL.md 改为照抄本机现行的单行路径状态栏；先备份、给用户看 diff，确认后才写，只替换状态栏那一段 |
| ~~ARD-A~~ | ~~2026-09-24~~ | ~~skill 里的 initiative 全部改称 feature，包括字段名和读取路径 `.coworker/features/.active`~~ 已被 [ARD-M](#ard-m) 取代 |
| ARD-B | 2026-08-01 | tmux 外观不再由 walter-worker 的安装脚本部署，改由独立的个人配置项目负责 |
| ARD-C | 2026-08-01 | 状态栏只显示当前文件夹路径；只改了本机配置，SKILL.md 没有改 |
| ~~ARD-D~~ | ~~2026-07-13~~ | ~~两行状态栏，加 AI 会话信息、颜色和 emoji；feature 改从 CLAUDE.local.md 读~~ 已被 [ARD-C](#ard-c) 取代 |
| ~~ARD-E~~ | ~~2026-07-02~~ | ~~加 worktree 字段，并由 walter-worker 的安装脚本部署状态栏脚本~~ 已被 [ARD-B](#ard-b) 取代 |
| ARD-F | 2026-07-01 | 把状态栏配置做成 personal skill，触发词选"customize tmux" |
| ~~ARD-G~~ | ~~2026-07-01~~ | ~~每个字段写成"名字:值"；会话名显示成 `tmux:名字`，不改会话本身的名字~~ 已被 [ARD-M](#ard-m) 取代 |
| ~~ARD-H~~ | ~~2026-07-01~~ | ~~用领先、落后、暂存、未跟踪的计数代替用户说的"git tree"~~ 已被 [ARD-M](#ard-m) 取代 |
| ~~ARD-I~~ | ~~2026-07-01~~ | ~~左侧只放会话创建时间，其余字段放右侧，由一个脚本输出~~ 已被 [ARD-M](#ard-m) 取代 |
| ~~ARD-J~~ | ~~2026-06-09~~ | ~~git 信息由辅助脚本取得：先进入当前窗格的目录，再跑 git 命令~~ 已被 [ARD-M](#ard-m) 取代 |
| ~~ARD-K~~ | ~~2026-06-09~~ | ~~状态栏底色用深灰 `colour236`~~ 已被 [ARD-M](#ard-m) 取代 |
| ARD-L | 2026-05-06 | 会话保存插件的安装另做成 tmux-setup skill，不放进状态栏 skill |

## Evidence Appendix

### ARD-M

理由：8 月 1 日起用户只要显示文件夹路径（ARD-C、PRD-K），SKILL.md 没跟上；照旧版执行会覆盖本机配置（design 的 QUES-C）。
写入前备份并征得同意，依据是用户 8 月 1 日"需要给用户提示确定才能安装"（PRD-L，QUES-D）。
被否决的方案：删掉本 skill；把五字段版留作选项；按 7 月 13 日从 CLAUDE.local.md 读 feature（ARD-D，已被 ARD-C 取代）。
出处：用户 2026-11-24 审阅回复"update but keep the skill"。状态栏段落和脚本照抄本机 `~/.tmux.conf` 与 `status_info.sh`。
本机配置同 computer-config commit eeba774 的 tmux-config spec。When NOT to Use 里的 tmux-setup 引用一并删掉（QUES-E）。

### ARD-A

理由：全仓库把 initiative 这个词改成 feature，本 skill 的描述、触发说明、脚本变量和图例一起改（PRD-D）。
被否决的方案：保留旧词。出处：commit c2b3f22（2026-09-24）。
这次只改了名字，没有顺带改成 7 月 13 日用户要的 CLAUDE.local.md 来源（见 ARD-D）。

### ARD-B

理由：用户问"是不是新建一个项目，专门就叫claude-tmux-config"，要求"对大家的claude tmux 没有影响"（13f2d9db，2026-08-01）。
被否决的方案：用户同日先提的"全部build 到ai-coworker 去"，即继续由 walter-worker 安装（同一会话）。
出处：walter-worker commit f251d61（设计）、fb943d4（删掉安装步骤和 status_info.sh）。
次日用户删掉了空的 claude-tmux-config 目录（13f2d9db，2026-08-02），tmux 配置改记在 computer-config 仓库（commit eeba774）。
本 skill 没有随之调整，见 design 的 QUES-D。

### ARD-C

理由：用户说"tmux 的bar 不用显示那么多数据了， 只要一个当前的 foder path 就行了"（c173b9ed，2026-08-01）（PRD-K）。
被否决的方案：7 月 13 日的两行十个字段版本（ARD-D）。
出处：f251d61 的设计文档记录，本机实际运行的是只输出文件夹路径的简单版脚本，并"已确认以简单版为准"。
computer-config 的 tmux-config spec（commit eeba774）也写明右侧只显示文件夹路径。SKILL.md 当时没有更新，2026-11-24 由 ARD-M 补上。

### ARD-D

理由：用户列出想要的字段，并说"if not enough space go next line"、"the initiative should read from claudel.local.md"（ses_0a12a0e1，2026-07-13）（PRD-J）。
被否决的方案：放不下时自动隐藏或截断字段；用户选了两行状态栏（同一会话）。
出处：walter-worker commit 87f4413（颜色和 emoji）。agent 当时把新版 SKILL.md 写进了 `~/.config/opencode/` 下的部署副本，没有提交到本仓库。
该副本现已不存在。2026-08-01 被 ARD-C 取代，walter-worker 的富版脚本也在 fb943d4 删除。

### ARD-E

理由：用户要求显示 worktree 名，并说"这里你需要先修ai-coworker 是不是有个tmux 的setup"（ses_0dc6469a，2026-07-02）（PRD-I）。
在 worktree 里，`git rev-parse --show-toplevel` 返回的是 worktree 目录，所以项目名改从主仓库推出（commit 9edd66d）。
被否决的方案：只改本 skill。出处：walter-worker commit 579ad50、9edd66d。部署方式被 ARD-B 取代，SKILL.md 从未加入 worktree 字段。

### ARD-F

理由：用户说"把这个做成一个skill 放在coworker 里面"，并在提问中选了 personal-skills 和"customize tmux"（ses_0e39cb88，2026-07-01）（PRD-H）。
被否决的方案：放进可复用的 ai-coworker-skills。出处：commit 5cc3d4b；parent decision history 的 0044。

### ARD-G

理由：用户说每个值前面要有字段名，像 `branch:master` 那样；会话名也要有 `tmux:` 标签（ses_0e39cb88，2026-07-01）（PRD-F）。
被否决的方案：把会话本身改名为 `tmux:opencode`；用户回"不用tmux_ prefix"，会话名改回原样，标签由脚本加（同一会话）。

### ARD-H

理由：agent 判断"a full git log graph would be too wide for the tmux bar"，改成状态计数（ses_0e39cb88，2026-07-01）（PRD-C）。
被否决的方案：在状态栏里画提交图。用户没有确认，只是没有反对，置信度低于 80%，见 design 的 QUES-A。

### ARD-I

理由：会话名挪到右侧并加了标签后，agent 把左侧简化为只显示创建时间（ses_0e39cb88，2026-07-01）（PRD-E）。
被否决的方案：6 月 9 日的左侧"Session: 名字 + 创建时间"（ses_15012457）。出处：同一会话对 `~/.tmux.conf` 的编辑；commit 5cc3d4b。

### ARD-J

理由：用户在 git 项目里却看不到分支，问"为什么不限时master"（ses_1500d37d，2026-06-09）（PRD-B）。
原因是 tmux 执行状态栏命令时不在窗格目录下。agent 改写成脚本，先读 `pane_current_path` 再进去跑 git。
被否决的方案：在 `~/.tmux.conf` 里直接内联 git 命令。出处：同一会话；7 月 1 日的 `status_info.sh` 沿用这个做法（commit 5cc3d4b）。

### ARD-K

理由：用户说"改成灰色的"，agent 先设 `bg=grey`；用户说"再暗一点"，改成 `colour236`（ses_15012457，2026-06-09）（PRD-G）。
被否决的方案：tmux 默认的绿色和较亮的 `grey`。出处：同一会话；commit 5cc3d4b。
本机现在用的是 Benjamin Blue 深蓝底（computer-config commit eeba774），何时由谁决定换色，属于 UNKNOWN。

### ARD-L

理由：用户要求"把当前的tmux 和tmux resurrect 插件的安装变成一个tmux-setup skill"（b2741719，2026-05-06）。
被否决的方案：UNKNOWN。出处：history.jsonl。本 SKILL.md 的 When NOT to Use 曾指向 tmux-setup，2026-11-24 删掉（ARD-M）。
parent design 的"已不存在"表把 tmux-setup 列为已不存在的 skill，见 design 的 QUES-E。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：从过去的对话和提交记录反推 tmux-status-bar 的决策 |
| 2026-11-24 | 加 ARD-M：SKILL.md 照抄本机单行路径状态栏，写前备份并确认；ARD-A、G 到 K 被取代 |
