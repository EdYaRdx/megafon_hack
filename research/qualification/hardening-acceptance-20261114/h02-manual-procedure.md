# H02 one-boundary PowerShell procedure

Run from the acceptance worktree root in a disposable copy. Never run the 12-boundary loop to qualify the harness.

```powershell
$ErrorActionPreference = 'Stop'
Get-FileHash -Algorithm SHA256 -LiteralPath '.\acceptance\20261114-dynamic\fault-writer-exit.ps1'
powershell.exe -NoProfile -ExecutionPolicy Bypass -File '.\acceptance\20261114-dynamic\run-one-boundary.ps1' -Boundary 1 -TimeoutSeconds 12
$receipt = Get-Content -Raw -Encoding UTF8 '.\acceptance\20261114-dynamic\targeted\h02-boundary-01.json' | ConvertFrom-Json
$receipt | Select-Object test,started_utc,parent_pid,child_pid,child_exit_code,timeout_seconds,identity_confirmed,identity_error,result,cleanup
Get-FileHash -Algorithm SHA256 -LiteralPath '.\acceptance\20261114-dynamic\targeted\h02-boundary-01.json'
```

Expected PASS requires one receipt written for the boundary with child PID, UTC start, parent PID, executable, complete command line, verified CIM `ProcessId`, `ParentProcessId`, `CreationDate`, `ExecutablePath`, and `CommandLine`, matching exit 90/signal, no timeout, plus verified child exit. If CIM denies access, timeout expires, identity mismatches or receipt is incomplete, record BLOCKED and leave any live process running. Do not use `Stop-Process` unless all identity fields match the process just started and exact PID/time/parent/command in its immediate prewritten launch receipt; if that launch receipt is absent, stop is forbidden. Cleanup, if later explicitly tested, must be a separate one-boundary case and confirm that exact child PID disappears while parent/user processes remain. Never target PID 6568.

This environment's executed attempts returned `BLOCKED_IDENTITY_UNVERIFIED` with `CIM access denied`; the procedure is not a PASS and requires a host where scoped child-process metadata is available.
