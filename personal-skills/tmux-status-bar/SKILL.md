---
name: tmux-status-bar
description: |
  Use when setting up or restoring the tmux status bar: one line, Benjamin Blue
  colors, session name on the left, the current pane's folder path on the right.
  Backs up ~/.tmux.conf first and writes only after the user confirms the diff.
  Triggered by phrases like "tmux bar", "tmux status", "customize tmux",
  "setup tmux display".
license: MIT
compatibility: opencode
metadata:
  triggers:
    - customize tmux
    - tmux bar
    - tmux status
    - tmux display
    - setup tmux
    - configure tmux
  when_to_use: |
    When the user wants their tmux status bar set up or restored to the
    single-line, folder-path-only Benjamin Blue bar. Use this skill to create
    or update only the status-bar block of ~/.tmux.conf and the path script.
  when_not_to_use: |
    For general tmux configuration (keybinds, plugins, truecolor, mouse,
    session save/restore) — leave those lines alone. For tmux session
    management only.
---

# tmux-status-bar

Set up the tmux status bar the way the user runs it today: one line, Benjamin
Blue colors, session name plus a green dot on the left, and the current pane's
folder path on the right (`~` stands for the home directory). No git fields,
no feature field.

## When to Use

- Setting up the status bar on a new machine or after a reinstall
- Restoring the bar after something overwrote it
- User asks to "show the folder path in tmux" or "customize tmux"

## When NOT to Use

- Non-tmux terminal setups (zsh prompt, starship, etc.)
- tmux plugin installation or other non-status-bar tmux settings
- General shell prompt customization

## Safety Rules

- Never write `~/.tmux.conf` or `~/.tmux/scripts/status_info.sh` before the
  user has seen the diff and said yes.
- Back up both files first. Replace only the status-bar block; every other
  line of `~/.tmux.conf` (truecolor, mouse, clipboard, popup keybind,
  resurrect/continuum plugins) stays byte-for-byte the same.

## Process

### Step 1: Back up

```sh
TS=$(date +%Y%m%d-%H%M%S)
[ -f ~/.tmux.conf ] && cp ~/.tmux.conf ~/.tmux.conf.bak-$TS
[ -f ~/.tmux/scripts/status_info.sh ] && \
  cp ~/.tmux/scripts/status_info.sh ~/.tmux/scripts/status_info.sh.bak-$TS
```

Tell the user the backup paths.

### Step 2: Build the new files in a temp directory

Write the proposed files to a temp directory (`mktemp -d`), not to their
real paths yet.

**Proposed `status_info.sh`** — exactly this:

```sh
#!/bin/sh
# Simple status: current folder path only

PANE_PATH=$(tmux display-message -p -F '#{pane_current_path}' 2>/dev/null)

if [ -z "$PANE_PATH" ]; then
  echo "~"
  exit 0
fi

HOME_PFX="$HOME/"
case "$PANE_PATH" in
  "$HOME_PFX"*) echo "~/${PANE_PATH#$HOME_PFX}" ;;
  *) echo "$PANE_PATH" ;;
esac
```

**Proposed `~/.tmux.conf`** — a copy of the current file where only the
status-bar block is swapped for this block:

```
# --- Status Bar (single-line, folder path only) ---
set -g status on
set -g status-style 'bg=#102D46,fg=#EAE7DD'
set -g message-style 'bg=#F2C94C,fg=#102D46'
set -g pane-border-style 'fg=#30506B'
set -g pane-active-border-style 'fg=#F2C94C'

set -g status-left-length 40
set -g status-left "#[fg=#F2C94C]#{session_name} #[fg=#5F8D4E]● "

set -g status-right-length 200
set -g status-right "#[fg=#F2C94C]📂 #[fg=brightwhite]#(~/.tmux/scripts/status_info.sh) "

setw -g window-status-current-style 'fg=#102D46,bg=#F2C94C,bold'
setw -g window-status-current-format ' #I:#W#F '
setw -g window-status-style 'fg=#8EA2AF,bg=#102D46'
setw -g window-status-format ' #I:#W#F '
```

How to find the old block:

- If the file has a `# --- Status Bar` line, the old block runs from that
  line through the last `status*`, `message-style`, `pane-*border-style`
  or `window-status*` line that follows it. Replace that range.
- Otherwise, remove each existing line that sets one of those options, and
  insert the block where the first removed line was. If there was none,
  insert it before the first `run-shell` line (plugins must stay last), or
  at the end of the file.
- If `~/.tmux.conf` does not exist, the proposed file is the block alone.

### Step 3: Show the diff and ask

```sh
diff -u ~/.tmux.conf "$TMP/tmux.conf"
diff -u ~/.tmux/scripts/status_info.sh "$TMP/status_info.sh"
```

Show both diffs (or "new file") to the user. Check that the conf diff only
touches status-bar lines. If both diffs are empty, say the bar is already
up to date and stop. Otherwise ask: "Apply these changes?" Stop here and
change nothing if the user does not say yes.

### Step 4: Write and reload (only after yes)

```sh
mkdir -p ~/.tmux/scripts
cp "$TMP/status_info.sh" ~/.tmux/scripts/status_info.sh
chmod +x ~/.tmux/scripts/status_info.sh
cp "$TMP/tmux.conf" ~/.tmux.conf
tmux source-file ~/.tmux.conf
```

To undo, copy the `.bak-$TS` files back and run `tmux source-file` again.

### Fallback

If the right side shows nothing or only `~`, check:
- `tmux display-message -p -F '#{pane_current_path}'` returns a path
- The script has execute permission
- `status-right-length` is 200

## Status Bar Layout

```
 main ●  1:zsh*  2:vim                                  📂 ~/project/the-super-lab
```

| Part | Color | Meaning |
|------|-------|---------|
| Bar background / text | `#102D46` / `#EAE7DD` | Deep Ocean background, light text |
| Session name | `#F2C94C` yellow | `#{session_name}` |
| `●` | `#5F8D4E` green | Separator dot after the session name |
| Current window | `#102D46` on `#F2C94C`, bold | ` index:name flags ` |
| Other windows | `#8EA2AF` on `#102D46` | ` index:name flags ` |
| `📂` + path | `#F2C94C` / brightwhite | Current pane's folder, `~` for home |
| Messages / active pane border | `#F2C94C` | Prompts and the active pane stand out in yellow |

## Sources

- Live setup on the user's machine, copied verbatim: the `# --- Status Bar`
  block of `~/.tmux.conf` and `~/.tmux/scripts/status_info.sh` (2026-08-01)
- User request 2026-08-01: the bar should show only the current folder path
- Spec: `docs/features/skill-factory/features/tmux-status-bar/` (ARD-C, ARD-M)
