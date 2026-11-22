# Test investigation and changes

## Observed baseline vs earlier report

Earlier owner-provided result: 121 tests, 26 failures, 4 errors, 5 skips, exit1. The raw log for that exact run was not found; it cannot be matched failure-by-failure or silently treated as the rerun.

Fresh baseline on fetched main code: 121 tests, 10 failures, 1 error, 5 skips, exit1; 2026-11-22 17:04:05.9907368Z–17:05:12.3471604Z (66.3564236 s). Python CPython3.12.14, invoking shell PowerShell7.6.9; the test harness selected Windows PowerShell5.1 for legacy fallback tests. FullLanguage; Process/User/Machine policies Undefined, LocalMachine RemoteSigned. No host policy was changed. Private raw logs contain machine paths and are deliberately not included in the public release.

## Classified causes

| Cause | Category | Evidence and minimal correction |
|---|---|---|
| Windows TEMP uses an 8.3 profile alias; helpers resolve to canonical long Unicode paths | B — test infrastructure | Raw fixture Path equality, unreadable-file mock and race predicate did not match canonical paths. Resolve fixture roots in test_case_workspace, test_find_python and test_resume_context. Assertions unchanged |
| Child CLI emits locale bytes while parent expects UTF-8 | B — subprocess test infrastructure | UnicodeDecodeError on non-UTF8 byte; invoke child with -X utf8 and decode UTF-8 explicitly in test_case_workspace |
| Windows PowerShell5.1 Security module autoload fails only with captured Python subprocess streams | C — host-specific limit; B — harness host choice | Minimal captured subprocess reproduces CLIXML/CouldNotAutoloadMatchingModule and duplicate type data; direct PS5.1 probes can import/read policy. Prefer installed pwsh7 in test_runtime_fallback, retain PS5.1 fallback. All three assertions/tests still execute; no new skip |
| Symlink creation denied, WinError1314 | C — OS privilege limitation | Five existing skips retained; not passed. Junction coverage runs |
| Exact earlier 26/4 distribution | D — unavailable raw evidence | Counts are an owner report. We do not claim the fresh 10/1 baseline accounts for every earlier failure |

No confirmed runtime/checkpoint defect was found from these failures; tools, Skills, protocol and assertions are unchanged. The change makes the harness explicit about host/encoding/canonical paths. Passing PowerShell7 tests does not certify Windows PowerShell5.1 under captured streams.

## Controlled run

Existing focused suites passed with ASCII TEMP/TMP and PYTHONUTF8=1. Final integrated full-suite result is in [unit-tests.json](unit-tests.json). Private raw log digests and exact path-bearing logs remain locally retained; public receipts redact interpreter/cwd paths.

Reproduction uses an installed Python3.12+ with -X utf8, an ASCII process-local TEMP/TMP, PYTHONUTF8=1, then -m unittest discover -s tests -v. This does not change execution policy or system-wide environment settings. Unicode fixture tests still run; an ASCII outer temp is not removal of Unicode coverage.

Baseline CI on exact origin/main ed42fef was green; it is Ubuntu/Python3.12 coverage, a different environment. A release-branch CI run is not claimed unless actually triggered and recorded.
