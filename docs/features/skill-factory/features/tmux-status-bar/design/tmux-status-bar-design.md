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
源文件：`personal-skills/tmux-status-bar/SKILL.md`（commit 5cc3d4b 加入，c2b3f22 把 initiative 改称 feature，2026-11-24 改成单行路径版，见 ARD-M）。

## Problem Statement

用户 8 月 1 日起只要状态栏显示当前文件夹路径（PRD-K），本机配置已改，旧版 SKILL.md 却仍是五字段版。
照旧版执行会不备份、不询问就覆盖 `~/.tmux.conf`（PRD-L）。本 skill 要能原样重建本机现行的状态栏（ARD-M）。

## Solution

一个 personal skill，分四步：备份，在临时目录生成新文件，给用户看 diff，确认后写入并重新加载（PRD-H、ARD-M）。
脚本每次刷新时输出当前窗格的路径，tmux 把它放在状态栏右侧。

## User Stories

- 作为开发者，我说"customize tmux"，agent 先备份、给我看 diff，我确认后才把状态栏配好。
- 作为开发者，配完后看不到输出时，我按 SKILL.md 的 Fallback 一节逐项检查。

## Implementation Decisions

skill 只有一个 SKILL.md，脚本和状态栏段落全文写在文中，逐字照抄本机现行文件（ARD-M）。
本仓库没有单独的脚本文件，也没有安装步骤；脚本只在 agent 执行 skill 时生成。
脚本只用 POSIX sh 和 tmux，不调用 git 和 coworker 命令，也不读 feature（ARD-M）。

## Design

**DSGN-A 触发。** 用户说"customize tmux""tmux bar""tmux status"等短语时使用（PRD-H）。zsh 提示符和 tmux 插件安装不用本 skill。

**DSGN-B 右侧路径脚本。** `status_info.sh` 用 `tmux display-message` 取当前窗格路径（PRD-K）。家目录开头换成 `~`；取不到路径时输出 `~`（ARD-M）。

**DSGN-C 状态栏样式。** 单行，底色 `#102D46`（Benjamin Blue 的 Deep Ocean），文字 `#EAE7DD`（ARD-M）。
右侧是黄色 📂 加白色路径，长度上限 200。

**DSGN-D 左侧和窗口列表。** 左侧是黄色会话名加绿色 `●`。当前窗口黄底深字加粗，其他窗口灰蓝字（ARD-M）。
消息和活动窗格的边框也用黄色 `#F2C94C`。

**DSGN-E 先备份。** 写任何文件前，把 `~/.tmux.conf` 和 `status_info.sh` 复制成带时间戳的副本。
副本名形如 `~/.tmux.conf.bak-YYYYmmdd-HHMMSS`（PRD-L、ARD-M）。

**DSGN-F 先给用户看 diff。** 新文件先写到临时目录，再用 `diff -u` 和现有文件对比（PRD-L）。
用户说"是"才写入；两份 diff 都为空就说明已是最新，直接结束（ARD-M）。

**DSGN-G 只替换状态栏那一段。** 从 `# --- Status Bar` 起到最后一条状态栏设置为止，整段替换（ARD-M）。
真彩色、鼠标、插件等其他行一律不动；写完用 `tmux source-file` 重新加载。

**DSGN-H 不再显示的字段。** 项目名（PRD-A）、分支（PRD-B）、git 状态（PRD-C）、feature（PRD-D）、创建时间（PRD-E）、字段名（PRD-F）、深灰底（PRD-G）都已去掉。
worktree（PRD-I）和 AI 会话信息（PRD-J）也不加。依据是用户最新的要求 PRD-K（ARD-C、ARD-M）。

## Testing Decisions

本 skill 没有自动测试或评测集，`personal-skills/tmux-status-bar/` 下只有 SKILL.md 一个文件。
2026-11-24 核对过：SKILL.md 里的脚本和状态栏段落与本机文件逐字一致，`diff` 没有输出（ARD-M）。
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
把五字段版留作选项：被否决，用户最新只要路径（ARD-M）。

## Drawbacks

脚本不读 git，状态栏上看不出分支和未提交的改动（PRD-B、PRD-C 已被 PRD-K 取代）。
脚本全文嵌在 SKILL.md 里，改字段时说明、脚本和图例要一起改。
执行 skill 仍会换掉用户手改过的状态栏段落；有备份和确认，但要用户自己看懂 diff。

## Risks and Mitigations

| 风险 | 缓解 |
|---|---|
| 用户以后又改了本机状态栏，SKILL.md 再次过时 | 写前看 diff；本机改动后同步更新 SKILL.md（ARD-M） |
| 找旧状态栏段落时多删或漏删了行 | diff 里只能出现状态栏相关的行，否则不写（DSGN-F、DSGN-G） |
| `~/.tmux.conf` 里没有 `# --- Status Bar` 标记 | 按选项名找旧行；都没有就插到第一行 `run-shell` 之前（DSGN-G） |

## Open Questions

| ID | 问题 | 目前答案 | Owner | Blocking |
|---|---|---|---|---|
| QUES-A | 用户说的"git tree"是状态计数，还是别的（比如 worktree 列表）（PRD-C）？ | 不再显示 git 信息，问题不再适用（ARD-M） | cicidi | no |
| QUES-B | feature 该读 `.coworker/features/.active` 还是 CLAUDE.local.md（PRD-D）？ | 两者都不读，feature 字段已去掉（ARD-M） | cicidi | no |
| QUES-C | skill 要不要改成只显示文件夹路径（PRD-K），把五字段版留作选项？ | 改成只显示文件夹路径，不留五字段选项（ARD-M） | cicidi | no |
| QUES-D | 改 `~/.tmux.conf` 前要不要先征得用户同意（PRD-L）？ | 要。先备份、给用户看 diff，确认后才写（ARD-M） | cicidi | no |
| QUES-E | When NOT to Use 指向的 tmux-setup 已不存在，改指哪里？ | 删掉这条引用，不改指别处（ARD-M） | cicidi | no |
| QUES-F | worktree 字段（PRD-I）和 AI 会话信息（PRD-J）还要补进 skill 吗？ | 不补，用户最新要求只显示路径（PRD-K、ARD-M） | cicidi | no |

## Reversibility

skill 本身在 git 跟踪的 `personal-skills/tmux-status-bar/SKILL.md`，用 `git revert` 即可撤回。
执行 skill 会改写 `~/.tmux.conf` 和 `~/.tmux/scripts/status_info.sh`，两者不在 git 里；写前留有 `.bak-时间戳` 副本，复制回去再重新加载即可恢复（DSGN-E）。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：按 SKILL.md 写出 tmux-status-bar 的 design，引用 PRD-A 到 PRD-L |
| 2026-11-24 | 按 ARD-M 改写：单行路径版、写前备份并确认、只换状态栏段落；QUES-A 到 QUES-F 已答 |
