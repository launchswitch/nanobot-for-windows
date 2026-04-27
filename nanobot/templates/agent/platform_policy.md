{% if system == 'Windows' %}
## Platform Policy (Windows)
- You are running on Windows. Paths use forward slashes (C:/Users/...).
- Do not assume GNU tools like `grep`, `sed`, `awk`, `cat` exist in the shell.
- Use PowerShell cmdlets: `Get-Content` (cat), `Set-Location` (cd), `Get-ChildItem` (ls), `Copy-Item` (cp), `Remove-Item` (rm).
- Prefer built-in file tools (read_file, write_file, edit_file, grep, glob) over shell commands.
- Temp files: use `$env:TEMP` not `/tmp`.
- Env vars: use `$env:NAME` syntax, not `$NAME` or `%NAME%`.
- If terminal output is garbled, retry with `[Console]::OutputEncoding = [Text.Encoding]::UTF8`.
{% else %}
## Platform Policy (POSIX)
- You are running on a POSIX system. Prefer UTF-8 and standard shell tools.
- Use file tools when they are simpler or more reliable than shell commands.
{% endif %}
