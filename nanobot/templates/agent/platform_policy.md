{% if system == 'Windows' %}
## Platform Policy (Windows)
- You are running on Windows. Paths use forward slashes (C:/Users/...).
- Do not assume GNU tools like `grep`, `sed`, `awk`, `cat`, `find`, `xargs` exist in the shell.
- Use PowerShell cmdlets: `Get-Content` (cat), `Set-Location` (cd), `Get-ChildItem` (ls/dir), `Copy-Item` (cp), `Remove-Item` (rm), `Move-Item` (mv), `Select-String` (grep).
- Prefer built-in file tools (read_file, write_file, edit_file, grep, glob) over shell commands.
- Temp files: use `$env:TEMP` not `/tmp`.
- Env vars: use `$env:NAME` syntax, not `$NAME` or `%NAME%`.
- To find executables: use `where.exe` (not `which` or `command -v`).
- PATH separator is `;` (not `:`). Example: `$env:PATH -split ';'`.
- The filesystem is case-insensitive (README.md == readme.md).
- PowerShell accepts both `/` and `\` in paths; `cmd.exe` only accepts `\`.
- There is no `chmod`/`chown`. Use `icacls` for file permissions.
- There is no `exec`, `fork`, or job control in the usual Unix sense.
- If terminal output is garbled, retry with `[Console]::OutputEncoding = [Text.Encoding]::UTF8`.
- Line endings are CRLF by default; prefer the built-in file tools which handle this automatically.
{% else %}
## Platform Policy (POSIX)
- You are running on a POSIX system. Prefer UTF-8 and standard shell tools.
- Use file tools when they are simpler or more reliable than shell commands.
{% endif %}
