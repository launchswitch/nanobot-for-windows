---
name: windows-terminal
description: Manage Windows Terminal tabs and panes for interactive CLI sessions on Windows.
metadata: {"nanobot":{"emoji":"🖥️","os":["win32"],"requires":{"bins":["powershell"]}}}
---

# Windows Terminal Skill

Use this skill on Windows to manage interactive CLI sessions in Windows Terminal. Prefer exec background mode for long-running, non-interactive tasks.

## Limitations

Windows Terminal does not offer the same programmatic control as tmux. You cannot:
- Send keystrokes to a running process in another tab
- Capture output from another tab
- Programmatically split panes and target them by ID

For full session control, consider using WSL with the tmux skill instead.

## What You Can Do

### Launch a new Windows Terminal tab

```powershell
wt -w 0 new-tab -p "PowerShell" powershell -NoExit -Command "python -q"
```

### Launch multiple tabs

```powershell
wt -w 0 new-tab -p "PowerShell" --title "agent-1" powershell -NoExit -Command "cd C:\workspace\project1; python -q" ; new-tab -p "PowerShell" --title "agent-2" powershell -NoExit -Command "cd C:\workspace\project2; python -q"
```

### Split panes

```powershell
wt -w 0 split-pane -V powershell -NoExit -Command "python -q"
```

## Alternative: ConPTY with PowerShell background jobs

For programmatic control similar to tmux, use PowerShell background jobs:

```powershell
# Start a background job
$job = Start-Job -ScriptBlock { python -c "print('hello')" }

# Check status
Receive-Job $job
Get-Job

# Wait for completion
Wait-Job $job -Timeout 60
```

## Helper: find-tabs.ps1

`{baseDir}/scripts/find-tabs.ps1` lists running Windows Terminal processes:

```powershell
{baseDir}/scripts/find-tabs.ps1
```

## Windows / WSL

If you need full tmux-style control, install WSL and use the tmux skill inside WSL instead. This skill is gated to Windows (`win32`).

## Cleanup

- Close a specific tab: focus it and press `Ctrl+Shift+W`
- Close all: `taskkill /im WindowsTerminal.exe /f`
