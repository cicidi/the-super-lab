---
feature: tmux-status-bar
type: design
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# tmux-status-bar — tmux 状态栏显示项目上下文

本篇说明 `tmux-status-bar` 这个 skill 现在怎么工作。
源文件：`personal-skills/tmux-status-bar/SKILL.md`（commit 5cc3d4b 加入，c2b3f22 把 initiative 改称 feature）。

## Problem Statement

开很多 tmux 窗格时，看不出每个窗格在哪个项目、哪个分支，也看不出有没有没提交的改动（PRD-A、PRD-B、PRD-C）。
在 `~/.tmux.conf` 里直接写 git 命令又不行：tmux 执行命令时不在当前窗格的目录下（decision-history 的 ARD-J）。

## Solution

一个 personal skill，分三步：写一个状态脚本，改 `~/.tmux.conf`，重新加载配置（PRD-H）。
脚本每次刷新时输出一行带颜色的文字，tmux 把它放在状态栏右侧。

## User Stories

- 作为开发者，我说"customize tmux"，agent 按三步把状态栏配好。
- 作为开发者，配完后看不到输出时，我按 SKILL.md 的 Fallback 一节逐项检查。

## Implementation Decisions

skill 只有一个 SKILL.md，脚本全文写在文中，agent 照抄到 `~/.tmux/scripts/status_info.sh`。
本仓库没有单独的脚本文件，也没有安装步骤；脚本只在 agent 执行 skill 时生成。
脚本只用 POSIX sh、tmux 和 git，不调用 coworker 命令；feature 只读一个文本文件（PRD-D）。

## Design

**DSGN-A 触发。** 用户说"customize tmux""tmux bar""tmux status"等短语时使用（PRD-H）。zsh 提示符和 tmux 插件安装不用本 skill。

**DSGN-B 先进入当前窗格目录。** 脚本用 `tmux display-message` 取会话名和当前窗格路径，`cd` 进去后再跑 git（ARD-J）。目录不存在时什么都不输出。

**DSGN-C 字段与格式。** 顺序是 tmux、project、branch、status、feature；每个值前都有灰色的字段名，例如 `branch:dev`（PRD-F）。
字段之间用 `|` 分隔，颜色用 tmux 的 `#[fg=colourN]` 写法。

**DSGN-D 项目和分支。** project 取 `git rev-parse --show-toplevel` 的目录名，不在 git 仓库时取当前目录名（PRD-A）。
branch 取当前分支名，不在仓库时显示 `--`（PRD-B）。

**DSGN-E git 状态。** 上游分支（upstream）指本地分支跟踪的远程分支。有上游时显示领先 `↑N` 和落后 `↓N`（PRD-C）。
工作区有改动时再显示暂存 `+N` 和未跟踪 `?N`；最后是 `*`（有改动）或 `✓`（干净）。

**DSGN-F feature。** 依次在窗格目录、仓库根目录、家目录下找 `.coworker/features/.active`，读到第一份就显示（PRD-D）。
SKILL.md 的 Sources 一节说"walks up from pane path"，实际只查这三个目录，不逐级往上找。

**DSGN-G 改 `~/.tmux.conf`。** 底色设为 `colour236`（PRD-G）；左侧显示会话创建时间（PRD-E、ARD-I）；右侧调用脚本，长度上限 250。
SKILL.md 要求替换已有的 `status-left` 和 `status-right` 行，不要追加；改完用 `tmux source-file` 重新加载。

**DSGN-H 尚未落地的需求。** worktree 字段（PRD-I）、AI 会话信息和两行显示（PRD-J）、只显示文件夹路径（PRD-K），SKILL.md 都没有。
PRD-D 要的 CLAUDE.local.md 来源也没落地；改 `~/.tmux.conf` 前不问用户（PRD-L）。见 QUES-B 到 QUES-D、QUES-F。

## Testing Decisions

本 skill 没有自动测试或评测集，`personal-skills/tmux-status-bar/` 下只有 SKILL.md 一个文件。
SKILL.md 称脚本"verified working on Linux with tmux 3.x"，指 7 月 1 日在本机手动看过状态栏（ses_0e39cb88）。
验证方式就是看状态栏；没有输出时按 Fallback 一节检查窗格路径、脚本执行权限和右侧长度。

## Out of Scope

通用 tmux 配置、插件安装、非 tmux 的终端提示符，都不用本 skill（SKILL.md 的 When NOT to Use 一节）。

## Further Notes

需求见 [PRD](../prd/tmux-status-bar-prd.md)，决策见 [decision-history](../decision-history/tmux-status-bar-decision-history.md)。
本机现行的 tmux 配置记在 computer-config 仓库的 `docs/tmux-config/spec/tmux-config-spec.md`（commit eeba774）。
walter-worker 曾有带 worktree 和 emoji 的富版脚本，可用 `git show 87f4413:setup/status_info.sh` 查看（ARD-D、ARD-E）。

## Alternatives Considered

在 `~/.tmux.conf` 里内联 git 命令：被否决，取不到窗格目录（ARD-J）。
把会话本身改名为 `tmux:名字`：被否决，改由脚本加标签（ARD-G）。
在状态栏里画提交图：被否决，太宽（ARD-H）。
由 walter-worker 的安装脚本统一部署：先采纳，后撤回（ARD-E、ARD-B）。

## Drawbacks

状态栏每次刷新都要跑好几条 git 命令，大仓库里可能变慢；SKILL.md 没写刷新间隔。
脚本全文嵌在 SKILL.md 里，改字段时说明、脚本和图例要一起改。
执行 skill 会覆盖用户已有的状态栏设置和底色。

## Risks and Mitigations

| 风险 | 缓解 |
|---|---|
| 照 skill 执行会覆盖本机现行的简单版脚本和 Benjamin Blue 配色（ARD-C） | 执行前先对比 `~/.tmux.conf`；见 QUES-C、QUES-D |
| `.active` 文件不再更新，feature 显示过时的值 | 7 月 13 日的分析称该文件已弃用（ses_0a12a0e1）；见 QUES-B |
| When NOT to Use 指向的 tmux-setup skill 已不存在 | 见 QUES-E |

## Open Questions

| ID | 问题 | 目前答案 | Owner | Blocking |
|---|---|---|---|---|
| QUES-A | 用户说的"git tree"是状态计数，还是别的（比如 worktree 列表）（PRD-C）？ | 目前显示状态计数（ARD-H） | cicidi | no |
| QUES-B | feature 该读 `.coworker/features/.active` 还是 CLAUDE.local.md（PRD-D）？ | SKILL.md 读 `.active`；用户 7 月 13 日要 CLAUDE.local.md | cicidi | no |
| QUES-C | skill 要不要改成只显示文件夹路径（PRD-K），把五字段版留作选项？ | SKILL.md 仍是 7 月 1 日的五字段版 | cicidi | yes |
| QUES-D | 改 `~/.tmux.conf` 前要不要先征得用户同意（PRD-L）？ | SKILL.md 直接替换，不问 | cicidi | no |
| QUES-E | When NOT to Use 指向的 tmux-setup 已不存在，改指哪里？ | parent design 的"已不存在"表列出 tmux-setup | cicidi | no |
| QUES-F | worktree 字段（PRD-I）和 AI 会话信息（PRD-J）还要补进 skill 吗？ | 只存在于 walter-worker 的历史提交 | cicidi | no |

## Reversibility

skill 本身在 git 跟踪的 `personal-skills/tmux-status-bar/SKILL.md`，用 `git revert` 即可撤回。
执行 skill 会改写 `~/.tmux.conf` 和 `~/.tmux/scripts/status_info.sh`，两者不在 git 里；SKILL.md 没有备份步骤，只能手动恢复。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：按 SKILL.md 写出 tmux-status-bar 的 design，引用 PRD-A 到 PRD-L |
