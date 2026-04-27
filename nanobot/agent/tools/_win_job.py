"""Windows Job Object wrapper for process tree management.

Creates a Job Object with JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE so that
when the handle is closed (timeout, cancellation, parent exit), Windows
automatically terminates the entire process tree — no orphan processes.
"""

import sys

if sys.platform == "win32":
    import ctypes
    from ctypes import wintypes

    kernel32 = ctypes.windll.kernel32

    # Constants
    JOB_OBJECT_EXTENDED_LIMIT_INFORMATION = 9
    JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE = 0x2000
    JOB_OBJECT_LIMIT_PRIORITY_CLASS = 0x0020
    PROCESS_ALL_ACCESS = 0x001FFFFF  # noqa: S105

    # HANDLE = wintypes.HANDLE
    # BOOL = wintypes.BOOL
    # DWORD = wintypes.DWORD

    class IO_COUNTERS(ctypes.Structure):
        _fields_ = [
            ("ReadOperationCount", ctypes.c_uint64),
            ("WriteOperationCount", ctypes.c_uint64),
            ("OtherOperationCount", ctypes.c_uint64),
            ("ReadTransferCount", ctypes.c_uint64),
            ("WriteTransferCount", ctypes.c_uint64),
            ("OtherTransferCount", ctypes.c_uint64),
        ]

    class JOBOBJECT_BASIC_LIMIT_INFORMATION(ctypes.Structure):
        _fields_ = [
            ("PerProcessUserTimeLimit", ctypes.c_int64),
            ("PerJobUserTimeLimit", ctypes.c_int64),
            ("LimitFlags", wintypes.DWORD),
            ("MinimumWorkingSetSize", ctypes.c_size_t),
            ("MaximumWorkingSetSize", ctypes.c_size_t),
            ("ActiveProcessLimit", wintypes.DWORD),
            ("Affinity", ctypes.c_size_t),
            ("PriorityClass", wintypes.DWORD),
            ("SchedulingClass", wintypes.DWORD),
        ]

    class JOBOBJECT_EXTENDED_LIMIT_INFORMATION(ctypes.Structure):
        _fields_ = [
            ("BasicLimitInformation", JOBOBJECT_BASIC_LIMIT_INFORMATION),
            ("IoInfo", IO_COUNTERS),
            ("ProcessMemoryLimit", ctypes.c_size_t),
            ("JobMemoryLimit", ctypes.c_size_t),
            ("PeakProcessMemoryUsed", ctypes.c_size_t),
            ("PeakJobMemoryUsed", ctypes.c_size_t),
        ]

    def create_kill_on_close_job() -> wintypes.HANDLE:
        """Create a Job Object that kills all child processes when closed."""
        job = kernel32.CreateJobObjectW(None, None)
        if not job:
            return None

        info = JOBOBJECT_EXTENDED_LIMIT_INFORMATION()
        info.BasicLimitInformation.LimitFlags = JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE

        ok = kernel32.SetInformationJobObject(
            job,
            JOB_OBJECT_EXTENDED_LIMIT_INFORMATION,
            ctypes.byref(info),
            ctypes.sizeof(info),
        )
        if not ok:
            kernel32.CloseHandle(job)
            return None

        return job

    def assign_process(job: wintypes.HANDLE, pid: int) -> bool:
        """Assign a process (by PID) to a Job Object."""
        proc = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
        if not proc:
            return False
        try:
            return bool(kernel32.AssignProcessToJobObject(job, proc))
        finally:
            kernel32.CloseHandle(proc)

    def close_job(job: wintypes.HANDLE) -> None:
        """Close the job handle, triggering KILL_ON_JOB_CLOSE."""
        if job:
            kernel32.CloseHandle(job)
