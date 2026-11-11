@echo off
setlocal EnableExtensions
cd /d "%~dp0"

rem This launcher runs OMP read-only; Git publishing happens outside the agent.
if not exist "prompts\overnight-product-research-v3.md" (
  echo ERROR: research prompt missing.
  exit /b 2
)
if not exist ".omp\profiles\research-night.yml" (
  echo ERROR: research-night profile missing.
  exit /b 2
)
if not exist ".omp\profiles\research-luna.yml" (
  echo ERROR: research-luna profile missing.
  exit /b 2
)
if not exist "docs\contest-brief.md" (
  echo ERROR: contest brief missing.
  exit /b 2
)
if not exist ".local\omp\sessions" mkdir ".local\omp\sessions"
if not exist "research\product" mkdir "research\product"

rem Do not commit any unrelated files that may already be staged.
for /f "delims=" %%F in ('git diff --cached --name-only') do (
  echo ERROR: unrelated staged files exist; unstage or commit them before running.
  exit /b 4
)

set "REPORT=research\product\overnight-research-v3.md"
set "STDERR=.local\omp\overnight-v3.stderr.txt"
set "BRANCH=research/overnight-v3-20261111"

rem Refuse to clobber an existing curated report.
if exist "%REPORT%" (
  echo ERROR: %REPORT% already exists. Back it up or rename it first.
  exit /b 5
)

echo Starting autonomous OMP research. This run may take hours.
echo The final Markdown response will be written to %REPORT%
echo Tool progress goes to local session artifacts; stderr to %STDERR%
omp -p --wait-async ^
  --config .omp/profiles/research.yml ^
  --config .omp/profiles/research-luna.yml ^
  --config .omp/profiles/research-night.yml ^
  --model openai-codex/gpt-6-luna ^
  --thinking high ^
  --approval-mode always-ask ^
  --tools read,grep,glob,web_search,task,wait,todo ^
  --no-extensions --no-skills --no-rules --no-lsp --no-title ^
  --max-time 4h --warn-cost 3 --max-cost 5 ^
  --session-dir .local/omp/sessions ^
  "@prompts/overnight-product-research-v3.md" ^
  1> "%REPORT%" 2> "%STDERR%"
set "EXITCODE=%ERRORLEVEL%"
echo %EXITCODE%> ".local\omp\overnight-v3.exitcode.txt"
echo OMP exit code: %EXITCODE%
if not "%EXITCODE%"=="0" (
  echo Research did not finish cleanly. No commit or push. Inspect local session artifacts.
  exit /b %EXITCODE%
)

rem Avoid auto-publishing a blank/aborted/very short answer.
for %%F in ("%REPORT%") do if %%~zF LSS 6000 (
  echo ERROR: report too short to auto-publish; review it locally.
  exit /b 6
)
findstr /i /c:"EXECUTIVE DECISION" /c:"ARCHITECTURE COMPARISON" "%REPORT%" >nul
if errorlevel 1 (
  echo ERROR: report lacks expected architecture sections; manual review required.
  exit /b 7
)

rem Push only explicit public research artifacts. Never git add -A, never raw JSONL.
git add -- "research/product/overnight-research-v3.md" "prompts/overnight-product-research-v3.md" "docs/contest-brief.md"
if errorlevel 1 exit /b 8
git diff --cached --check
if errorlevel 1 (
  echo ERROR: staged patch fails whitespace check. Not committing.
  exit /b 9
)
git diff --cached --quiet
if not errorlevel 1 (
  echo Nothing to commit; skipping push.
  exit /b 0
)
git commit -m "research: save overnight product strategy study for review"
if errorlevel 1 (
  echo ERROR: git commit failed. No push.
  exit /b 10
)
git push origin HEAD:refs/heads/%BRANCH%
if errorlevel 1 (
  echo ERROR: git push failed. Local commit and report were kept.
  exit /b 11
)
echo Published research draft to branch %BRANCH%. Main branch was not pushed.
exit /b 0
