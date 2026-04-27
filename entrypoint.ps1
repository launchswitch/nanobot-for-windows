# Nanobot Windows entrypoint for Docker Windows containers
$dir = Join-Path $env:APPDATA "nanobot"

if (Test-Path $dir) {
    $testFile = Join-Path $dir ".write-test-$$"
    try {
        New-Item -Path $testFile -ItemType File -Force | Out-Null
        Remove-Item -Path $testFile -Force
    } catch {
        $acl = (Get-Acl $dir).Access | Where-Object { $_.IdentityReference -match $env:USERNAME }
        Write-Error "Error: $dir is not writable by $($env:USERNAME)."
        Write-Error "Fix: icacls `"$dir`" /grant `${env:USERNAME}:(OI)(CI)F /T"
        exit 1
    }
}

nanobot @args
