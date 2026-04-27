"""Sandbox backends for shell command execution.

To add a new backend, implement a function with the signature:
    _wrap_<name>(command: str, workspace: str, cwd: str) -> str
and register it in _BACKENDS below.
"""

import os
import shlex
import shutil
import sys
from pathlib import Path

from nanobot.config.paths import get_media_dir


def _bwrap(command: str, workspace: str, cwd: str) -> str:
    """Wrap command in a bubblewrap sandbox (requires bwrap in container).

    Only the workspace is bind-mounted read-write; its parent dir (which holds
    config.json) is hidden behind a fresh tmpfs.  The media directory is
    bind-mounted read-only so exec commands can read uploaded attachments.
    """
    ws = Path(workspace).resolve()
    media = get_media_dir().resolve()

    try:
        sandbox_cwd = str(ws / Path(cwd).resolve().relative_to(ws))
    except ValueError:
        sandbox_cwd = str(ws)

    required  = ["/usr"]
    optional  = ["/bin", "/lib", "/lib64", "/etc/alternatives",
                 "/etc/ssl/certs", "/etc/resolv.conf", "/etc/ld.so.cache"]

    args = ["bwrap", "--new-session", "--die-with-parent"]
    for p in required: args += ["--ro-bind",     p, p]
    for p in optional: args += ["--ro-bind-try", p, p]
    args += [
        "--proc", "/proc", "--dev", "/dev", "--tmpfs", "/tmp",
        "--tmpfs", str(ws.parent),        # mask config dir
        "--dir", str(ws),                 # recreate workspace mount point
        "--bind", str(ws), str(ws),
        "--ro-bind-try", str(media), str(media),  # read-only access to media
        "--chdir", sandbox_cwd,
        "--", "sh", "-c", command,
    ]
    return shlex.join(args)


def _windows_restricted(command: str, workspace: str, cwd: str) -> str:
    """Wrap command for restricted execution on Windows.

    Uses PowerShell with constrained env and workspace-scoped working directory.
    This is NOT a true container sandbox — it restricts the environment and
    working directory but does not provide filesystem isolation or network
    restrictions. Best-effort hardening for Windows where bwrap is unavailable.
    """
    ws = Path(workspace).resolve()
    sandbox_cwd = str(ws)
    try:
        resolved_cwd = Path(cwd).resolve()
        resolved_cwd.relative_to(ws)
        sandbox_cwd = str(resolved_cwd)
    except ValueError:
        pass

    # Strip dangerous env vars and set minimal env via PowerShell prefix
    restricted_env = " ".join(
        f'$env:{k} = {repr(v)};'
        for k, v in {
            "PATH": os.environ.get("PATH", ""),
            "SYSTEMROOT": os.environ.get("SYSTEMROOT", r"C:\Windows"),
            "TEMP": str(ws / ".tmp"),
            "TMP": str(ws / ".tmp"),
            "USERPROFILE": os.environ.get("USERPROFILE", ""),
        }.items()
    )
    shell_exe = shutil.which("pwsh") or shutil.which("powershell") or "powershell"
    return (
        f"{shell_exe} -NoProfile -Command "
        f"Set-Location {repr(sandbox_cwd)}; "
        f"{restricted_env} "
        f"& {{ {command} }}"
    )


_BACKENDS = {"bwrap": _bwrap, "windows-restricted": _windows_restricted}


def wrap_command(sandbox: str, command: str, workspace: str, cwd: str) -> str:
    """Wrap *command* using the named sandbox backend."""
    if backend := _BACKENDS.get(sandbox):
        return backend(command, workspace, cwd)
    raise ValueError(f"Unknown sandbox backend {sandbox!r}. Available: {list(_BACKENDS)}")
