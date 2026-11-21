# Исторический handoff и Git handoff

> **Архив, не инструкции следующей сессии.** Текущие пользовательские результаты — в [evaluation](evaluation.md), запуск — в [Quick Start](quickstart.md). Старые SHA и задачи ниже не подменяют актуальный release. [Архивный индекс](archive/README.md).

Этот файл сохраняет предыдущую операционную хронологию; он не источник текущего acceptance status. Текущий статус только в [`implementation-status.md`](implementation-status.md), конкурсные gates — в [`submission-checklist.md`](submission-checklist.md). Старые SHA/host paths ниже и в прежних записях исторические, не команды для текущего checkpoint.

## Для этой документационной работы

- Expected starting HEAD: `98cd57ef8d0ba5e919c505466fa82f4e4653b9fe`.
- Рабочая ветка по задаче: `docs/product-polish-20261114`; source: `codex/mgimo-hardening-20261114`.
- Audit reference: `audit/hardening-acceptance-20261114` at `672aa5c83616f813c7dd9dc0598a1c8e20f8e7e9`.
- Эти значения предоставлены пользователем; здесь не выполнялись Git-команды, branch/HEAD/status, diff, commit, push и PR не проверялись/не создавались.

## Текущий следующий шаг

1. На разрешённой Git-среде сверить локальный branch/HEAD с указанной основой, проверить полный diff и staged paths; остановиться при расхождении, не reset/rebase/overwrite чужую работу.
2. Просмотреть только разрешённый documentation change set. Не добавлять `.omp/profiles/product-build.yml`, сырые OMP/host JSONL, credentials, personal data и полный audit corpus без отдельной privacy review.
3. После reviewer, создать/сохранить локальный commit только в `docs/product-polish-20261114`; не менять `main`, не merge и не force push.
4. Опубликовать branch и открыть PR в `main` только с разрешённым GitHub-доступом; проверить remote tip/diff и реальные status checks.

Команды ниже — точная инструкция следующему оператору; **не исполнены** в этой сессии. Использовать только если worktree соответствует указанной базе. При любом mismatch, неожиданном staged/untracked file или user-owned change — остановиться и вручную разобрать; не reset/clean/rebase, не force push.

```powershell
$ErrorActionPreference = 'Stop'
$expectedBranch = 'docs/product-polish-20261114'
$expectedHead = '98cd57ef8d0ba5e919c505466fa82f4e4653b9fe'
$allow = @(
  'README.md',
  'START-HERE.txt',
  'docs/README.md',
  'docs/quickstart.md',
  'docs/architecture.md',
  'docs/submission-architecture.md',
  'docs/evaluation.md',
  'docs/implementation-status.md',
  'docs/submission-checklist.md',
  'docs/clean-host-e2e-runbook.md',
  'docs/next-session-handoff.md',
  'docs/repository-inventory.md',
  'cases/README.md',
  'research/README.md'
)

if ((git branch --show-current) -ne $expectedBranch) { throw 'Wrong branch; stop.' }
if ((git rev-parse HEAD) -ne $expectedHead) { throw 'HEAD differs from expected baseline; stop and reconcile.' }
git status --short --branch
if ($LASTEXITCODE -ne 0) { throw 'git status failed.' }
git status --porcelain=v1 -uall
if ($LASTEXITCODE -ne 0) { throw 'git status (including untracked) failed.' }
git diff --check
if ($LASTEXITCODE -ne 0) { throw 'Unstaged whitespace check failed.' }
git diff --cached --check
if ($LASTEXITCODE -ne 0) { throw 'Staged whitespace check failed.' }
git diff HEAD --stat
git diff HEAD --name-status
git diff HEAD

$changed = @(git diff HEAD --name-only)
if ($LASTEXITCODE -ne 0) { throw 'Changed-path lookup failed.' }
$unexpected = @($changed | Where-Object { $_ -notin $allow })
if ($unexpected.Count -gt 0) { throw "Unexpected changed paths: $($unexpected -join ', ')" }
if ($changed.Count -ne $allow.Count) { throw "Expected $($allow.Count) changed allowlist files; found $($changed.Count). Reconcile before staging." }

# Inspect every Markdown link target manually or with an approved checker.
# This allowlist contains Markdown/TXT only; no changed JSON/JSONL files require parsing.
git add -- $allow
if ($LASTEXITCODE -ne 0) { throw 'Staging failed; inspect status and preserve changes.' }
git diff --cached --check
if ($LASTEXITCODE -ne 0) { throw 'Staged whitespace check failed.' }
git diff --cached --stat
git diff --cached --name-status
git diff --cached
$unstaged = @(git diff --name-only)
if ($LASTEXITCODE -ne 0) { throw 'Unstaged path lookup failed.' }
if ($unstaged.Count -gt 0) { throw 'Unstaged tracked edits remain; review and stage only after reconciliation.' }


git commit -m "docs: finalize product documentation and repository presentation"
if ($LASTEXITCODE -ne 0) { throw 'Commit failed; preserve worktree and inspect status.' }
git push -u origin docs/product-polish-20261114
if ($LASTEXITCODE -ne 0) { throw 'Push failed; do not force-push. Preserve local commit and inspect remote.' }

$localShaOutput = @(git rev-parse HEAD)
if ($LASTEXITCODE -ne 0 -or $localShaOutput.Count -ne 1) { throw 'Local commit SHA lookup failed.' }
$localSha = $localShaOutput[0].Trim()
$remoteLine = @(git ls-remote origin refs/heads/docs/product-polish-20261114)
if ($LASTEXITCODE -ne 0) { throw 'Remote SHA lookup failed; publication is not independently confirmed.' }
if ($remoteLine.Count -ne 1) { throw 'Expected one remote branch ref; inspect destination manually.' }
$remoteSha = ($remoteLine[0] -split '\s+')[0]
if ($remoteSha -ne $localSha) { throw "Remote tip $remoteSha differs from local commit $localSha." }
Write-Output "Verified remote branch tip: $remoteSha"
```

The commands above are a guarded handoff, not executed in this session. The comparison allows only the 14 named tracked files and requires no extra changed paths; untracked paths still require manual inspection before staging. Inspect all Markdown links manually or with an approved checker before commit. No JSON/JSONL files are in the allowlist. Stop on any branch/HEAD mismatch, unrelated staged/untracked file, failed command, or remote divergence; never reset, clean, rebase, force-push, or publish to `main`. Do not create a PR unless separately requested.

## Историческая запись

Предыдущие Codex synthetic R1/R2 artifacts, Sol preprod audit, exploratory F runs, release report и прежние post-push/handoff notes оставлены в исходном виде в их собственных файлах. Их labels и dates относятся к их собственным scopes; текущий status table в implementation-status имеет приоритет как сводка.
