# List Windows Terminal processes and their command lines
Get-Process -Name WindowsTerminal -ErrorAction SilentlyContinue |
    Select-Object Id, StartTime, MainWindowTitle |
    Format-Table -AutoSize

# List PowerShell sessions that could be nanobot-managed
Get-Process -Name pwsh, powershell -ErrorAction SilentlyContinue |
    Where-Object { $_.Id -ne $PID } |
    Select-Object Id, StartTime, Path |
    Format-Table -AutoSize
