# Submission checklist — working draft

Do not mark an item PASS without a saved artifact or observed run. The official public page says partner assignments are in the personal cabinet; the exact MegaFon demo brief and its provenance remain `UNKNOWN` until an authorized team member obtains and verifies the file. See [`official-demo-brief-availability.md`](../research/qualification/official-demo-brief-availability.md).

## Repository and product

- [ ] Confirm the correct feature branch and commit; review all staged/tracked changes; exclude `.omp/profiles/product-build.yml`, credentials, personal data and raw session logs.
- [ ] Publish the reviewed feature branch without force-push; verify the repository link and jury access.
- [ ] Replace synthetic demo inputs only when an official brief is published; otherwise use clearly labeled public/open or fictional data.
- [ ] Follow root README from a clean checkout; verify file access, skill discovery, case creation, evidence locators, options, both strategies, validation, state save and resume.
- [ ] Open the project root in Cursor and one other compatible host. In Cursor, first check **Customize → Skills**; in Codex CLI, run `codex` then `/skills`. A PASS requires all six names (`intake`, `evidence-research`, `options-decision`, `strategy-communication`, `experiment-design`, `resume-revise`) to be discovered normally and used from the clean project. Explicit invocation (`/intake`, `$intake`) is diagnostic only, never a discovery PASS. Restart/rescan once if needed, then record PASS/FAIL. Save host/version, exact list, prompt/result and redacted evidence under `research/qualification/host-acceptance/<host>-<version>/`; omit account details, notifications, credentials and personal data. Skill listing alone does not pass clean-case or new-chat acceptance.
- [ ] Exercise a genuinely new chat/session: pause, resume from files, continue one unfinished task, then ingest new synthetic/authorized data and revise without overwriting the previous decision.
- [ ] Reproduce any decision-critical calculation with a tool; preserve input locators, formula, units, output and narrow test. One synthetic retention calculation was executed via the internal JSON-reader jq selector and independently reviewed (`../research/sol-audit/eval-results/retention-calculation-20261113.md`); this verifies OMP/read-tool arithmetic only, not IDE/agent-tool availability. Current F1/F3 arithmetic has not been run through a calculation tool.
- [ ] Verify all claims against actual content, paths/locators, dates and denominators; independent reviewer checks the saved artifacts and response, not just the explanation.
- [ ] Confirm status quo, close/stop, tradeoffs, strong objections, product/communication alignment, comparator, metric denominator, period, guardrails and threshold/revisit are explicit or honestly `UNKNOWN` and gated.

## Manual clean-host acceptance — human-run, not yet executed

**State:** no Cursor GUI/model run or Codex workflow run has been observed. The previously prepared detached worktrees are at commit prefix `1323f99`, older than this phase’s last verified baseline `f621e0b9f9a0401910c28c5789a3d11d6f310b72`; they do not contain the uncommitted overnight case/report/status edits. Do not treat them as acceptance copies for the current reviewed state. Before each host, create/refresh a clean copy at one exact reviewed commit and verify both hosts use that same SHA; the overnight edits have no committed SHA yet. Initialize a separate run log, record start time, verify clean status and commit. Do not open the populated authoring worktree.

Before any model call, use only a host entitlement already authorized for this test. If the host requires a new purchase, unapproved pay-as-you-go usage, or enabling a paid service, stop and mark `BLOCKED`; do not purchase or assume the call is free. Record any observed charge, otherwise `UNKNOWN`.

**Automated tests:** the tracked-file inventory found no `tests/`, `scripts/`, `pyproject.toml`, `package.json`, `Makefile`, `tox.ini`, or `pytest.ini` runner. No code changed in this docs-only update, so do not rerun the earlier case-copy smoke checks or synthetic evaluations. This is not an automated host E2E.

### 0. Create identical clean worktrees for host acceptance

The last verified committed baseline is `f621e0b9f9a0401910c28c5789a3d11d6f310b72`. The older pre-created `1323f99` worktrees do not match it. Overnight case/report/status edits remain uncommitted and are not present in either worktree; this run tests the committed product baseline, not those uncommitted artifacts. Use a separate human-reviewed commit if acceptance must include them.

In PowerShell, create two new detached worktrees without overwriting existing paths:

```powershell
$source = 'C:\Projects\GitHub\megafon_hack'
$sha = 'f621e0b9f9a0401910c28c5789a3d11d6f310b72'
$cursorRepo = 'C:\Projects\GitHub\megafon_hack-host-acceptance-f621e0b'
$codexRepo = 'C:\Projects\GitHub\megafon_hack-host-acceptance-codex-f621e0b'
foreach ($path in @($cursorRepo, $codexRepo)) {
    if (Test-Path $path) { throw "Path already exists; choose a new empty folder: $path" }
}
$cursorOutput = & git -C $source worktree add --detach $cursorRepo $sha 2>&1
$cursorExit = $LASTEXITCODE
if ($cursorExit -ne 0) {
    $cursorOutput | Write-Output
    throw "Cursor worktree add failed (exit code $cursorExit); record the output and stop."
}
$cursorOutput | Write-Output
$codexOutput = & git -C $source worktree add --detach $codexRepo $sha 2>&1
$codexExit = $LASTEXITCODE
if ($codexExit -ne 0) {
    $codexOutput | Write-Output
    throw "Codex worktree add failed (exit code $codexExit); record the output and stop."
}
$codexOutput | Write-Output
$cursorShaOutput = & git -C $cursorRepo rev-parse HEAD 2>&1
$cursorShaExit = $LASTEXITCODE
if ($cursorShaExit -ne 0) {
    $cursorShaOutput | Write-Output
    throw "Cursor worktree rev-parse failed (exit code $cursorShaExit); record the output and stop."
}
$cursorSha = ($cursorShaOutput -join "`n").Trim()
$codexShaOutput = & git -C $codexRepo rev-parse HEAD 2>&1
$codexShaExit = $LASTEXITCODE
if ($codexShaExit -ne 0) {
    $codexShaOutput | Write-Output
    throw "Codex worktree rev-parse failed (exit code $codexShaExit); record the output and stop."
}
$codexSha = ($codexShaOutput -join "`n").Trim()
if ($cursorSha -ne $sha -or $codexSha -ne $sha) { throw 'Worktrees do not match the intended commit.' }
```

If any Git command fails, record its exact printed output and exit code, then stop; do not run the next command, force, or overwrite. Use the same source commit in both hosts.

### 1. Cursor — clean copy, ordinary skill discovery

1. In PowerShell, verify the prepared Cursor worktree before opening it:

   ```powershell
   $repo = 'C:\Projects\GitHub\megafon_hack-host-acceptance-f621e0b'
   Set-Location $repo
   git status --short --branch
   git rev-parse HEAD
   if (git status --porcelain) { throw 'Worktree is not clean; stop and use a clean copy.' }
   ```

   Record the SHA and clean status. In Windows Start, launch Cursor → **File → Open Folder** → select this exact `$repo`. Do not open the authoring checkout. Record Cursor’s exact version from **Help → About**. In **Customize → Skills**, record the normally discovered list and capture a redacted screenshot. Required names: `intake`, `evidence-research`, `options-decision`, `strategy-communication`, `experiment-design`, `resume-revise`. Do not invoke `/skill` commands to make discovery pass. If Cursor cannot be opened, record `BLOCKED`; the missing CLI alone is not a host test.

2. In the same PowerShell session, create an empty case containing only the brief and raw synthetic inputs:

   ```powershell
   $case = Join-Path $repo 'cases\host-acceptance-smoke'
   if (Test-Path $case) { throw 'Case path already exists; choose a new empty path, never overwrite.' }
   Copy-Item (Join-Path $repo 'cases\_template') $case -Recurse
   New-Item -ItemType Directory -Path (Join-Path $case 'input') | Out-Null
   $source = Join-Path $repo 'cases\meal-planner-demo'
   Copy-Item (Join-Path $source 'brief.md') (Join-Path $case 'brief.md')
   Copy-Item (Join-Path $source 'input\concept-note.md') (Join-Path $case 'input\concept-note.md')
   Copy-Item (Join-Path $source 'input\beta-survey.csv') (Join-Path $case 'input\beta-survey.csv')
   ```

   Do not copy any populated case sources, journals, claims, options, decisions, strategies, test plan, state, activity, or revisions. Leave the copied template placeholders and empty ledgers unchanged before the first chat. The brief and inputs are wholly synthetic.

3. In Cursor Chat, send this **single ordinary request**. Do not name, select, or invoke individual skills:

   ```text
   Проведи сквозную приёмку синтетического дела только в cases/host-acceptance-smoke/. Прочитай brief, исходные input-файлы, AGENTS.md и prompts/first-run.md; соблюдай проектные инструкции и штатное обнаружение возможностей. Не называй, не выбирай и не вызывай отдельные skills вручную; не подставляй готовые ответы.

   Начни с решения, которое надо принять, владельца решения, аудитории, срока, цели, ограничений и неизвестного. Задай только вопросы, ответы на которые действительно меняют следующий шаг. Не придумывай отсутствующие сведения: если ответ не дан в brief, зафиксируй UNKNOWN и продолжай только до безопасного, явно ограниченного вывода; никакой реальный запуск не разрешён.

   Затем исследуй предоставленные материалы и напрямую открой публичную методическую страницу https://www.gov.uk/service-manual/user-research/user-research-in-discovery через доступный host-инструмент. Запиши проверяемые источники, точные локаторы, доказательства, утверждения, знаменатели и ограничения; используй статусы OBSERVED, DOCUMENTED, CLAIMED, INFERENCE, HYPOTHESIS и UNKNOWN в соответствии с references/. Пересчитай релевантные показатели CSV доступным расчётным инструментом и сохрани формулу/запрос, входные строки, единицы и результат. Не используй в ответе заранее подставленные результаты из других дел. Если нужный инструмент или сайт недоступен, зафиксируй попытку и ошибку и не называй расчёт/источник проверенным.

   Подготовь не менее трёх содержательно разных вариантов, включая status quo и остановку направления; укажи сильные возражения и условную рекомендацию. Свяжи продуктовую стратегию с коммуникационной: аудитория, проверяемое обещание, доказательства/запреты, каналы и риски должны быть согласованы. Подготовь план проверки с comparator, метриками и знаменателями, периодом, guardrails, владельцем, порогами или явными UNKNOWN и правилом решения/пересмотра.

   Сохраняй результат в файлах дела и журналах по существующей структуре. Перед завершением проверь согласованность источников, evidence, claims и ссылок на файлы; обнови state.md и activity.jsonl с текущим этапом, человеческими гейтами и одним точным следующим действием. До паузы создай revisions/ и точные снимки revisions/state-r1.md и revisions/decision-r1.md. Не используй закрытые данные, не связывайся с людьми, не трать деньги, не публикуй и не запускай продукт. В конце перечисли созданные/обновлённые файлы, непроверенное, ошибки, повторы и время/расходы со статусом UNKNOWN, если телеметрия недоступна.
   ```

   If the agent asks for missing decision facts, answer `UNKNOWN — not supplied; do not invent; continue only with the bounded synthetic analysis above.` Do not supply the desired recommendation or calculated ratios.

### 2. First-run stage gates and expected files

| Stage | Required case files | PASS | FAIL / BLOCKED |
|---|---|---|---|
| Intake | `brief.md`, `state.md`, appended `activity.jsonl` | Decision, owner, audience, deadline and constraints captured; only decision-changing questions; missing answers remain `UNKNOWN`. | Fabricated facts, skipped material questions, or unsupported certainty. |
| Evidence/research | `sources.jsonl`, `evidence.jsonl`, `claims.jsonl`; source snapshot under `sources/` when available | Direct page attempt and exact locator; source/evidence/claim references resolve; claim statuses distinguish observation, documentation, claim, inference, hypothesis and unknown; CSV calculation includes input rows, formula, numerator, denominator, units and host-tool result. | URL-only citation, wrong denominator, invented source content; tool/site unavailable is `BLOCKED`, never PASS. |
| Alternatives/decision | `options.md`, `decision.md`, updated `claims.jsonl` and `state.md` | At least three materially different options, including status quo and stop; tradeoffs and strong objections; conditional, human-review-only recommendation. | Fewer or cosmetic options, omitted stop/status quo, no serious objection, or launch presented as approved. |
| Strategy/validation | `strategy-product.md`, `strategy-communication.md`, `test-plan.md` | Strategies agree on audience, value, evidence, promise and limits. Plan names comparator, metric/denominator, period, guardrails, owner, decision rule and revisit trigger; unknowns remain gated. | Contradictory promise/strategy or missing comparator, metric/guardrail/decision rule. |
| R1 pause | `revisions/state-r1.md`, `revisions/decision-r1.md`, current `state.md`, appended `activity.jsonl` | Exact snapshots saved; one named unfinished task and one exact next action; no real-world validation or launch approval claimed. | No snapshots/pending task, or case says complete despite unfinished work. |
| New-chat resume/revise | `input/revision-2-research-note.md`, current `state.md`/`decision.md`, appended ledgers as warranted | New session reads saved state, finishes the named task, labels note synthetic, appends only justified successors/events, and preserves both R1 snapshots byte-for-byte. | Snapshot hash changes, silent repetition, lost provenance, or synthetic claims promoted to real evidence. |

Missing files, invented source content, wrong denominator, forced/manual skill invocation, hand-written outputs standing in for agent work, overwritten R1 snapshots, or unlogged retries are `FAIL`. If a host tool or public page is unavailable, record `BLOCKED` with the exact attempt and error; do not report a full PASS. Verify R1 hashes before and after resume:

```powershell
Get-FileHash -Algorithm SHA256 -Path (Join-Path $case 'revisions\state-r1.md'), (Join-Path $case 'revisions\decision-r1.md')
```

Append both hash outputs, labeled “before resume” and “after resume,” to the run log.

3. After the R1 gate passes, pause the first chat. Only then copy the new synthetic input:

   ```powershell
   Copy-Item (Join-Path $source 'input\revision-2-research-note.md') `
     (Join-Path $case 'input\revision-2-research-note.md')
   ```

   Open a genuinely new Cursor chat in the same worktree and send:

   ```text
   Continue this case from its saved files. First read state.md and identify the current revision and exact next action; do not rely on the previous chat. Complete the named pending task, inspect the new input/revision-2-research-note.md as synthetic evidence, and update only the successor evidence/claims/decision/state needed. Do not repeat completed source lookup or calculations without a recorded reason. Preserve revisions/state-r1.md and revisions/decision-r1.md byte-for-byte; append the event and record provenance, limits, errors and the next action. Do not invoke a skill explicitly or treat synthetic reports as real-world evidence.
   ```

### 3. Codex — repeat independently on its clean copy

1. Open a new PowerShell session and verify the separate Codex worktree:

   ```powershell
   $repo = 'C:\Projects\GitHub\megafon_hack-host-acceptance-codex-f621e0b'
   Set-Location $repo
   git status --short --branch
   git rev-parse HEAD
   if (git status --porcelain) { throw 'Worktree is not clean; stop and use a clean copy.' }
   ```

   Require the same commit SHA as the Cursor copy. Use the setup block below to seed a separate empty case, then run `codex --version`, start `codex`, and run `/skills`; save the ordinary listing before sending the exact first-run request. Do not type `$intake` or otherwise force a skill. Apply the same stage gates above.

   ```powershell
   $case = Join-Path $repo 'cases\host-acceptance-smoke'
   if (Test-Path $case) { throw 'Case path already exists; choose a new empty path, never overwrite.' }
   Copy-Item (Join-Path $repo 'cases\_template') $case -Recurse
   New-Item -ItemType Directory -Path (Join-Path $case 'input') | Out-Null
   $source = Join-Path $repo 'cases\meal-planner-demo'
   Copy-Item (Join-Path $source 'brief.md') $case
   Copy-Item (Join-Path $source 'input\concept-note.md') (Join-Path $case 'input\concept-note.md')
   Copy-Item (Join-Path $source 'input\beta-survey.csv') (Join-Path $case 'input\beta-survey.csv')
   ```

   After R1 is complete and paused, copy the same revision-2 note:

   ```powershell
   Copy-Item (Join-Path $source 'input\revision-2-research-note.md') `
     (Join-Path $case 'input\revision-2-research-note.md')
   ```

   Save the R1 hashes, exit the current Codex session, and start a genuinely new `codex` session from the same worktree. Send the same resume request as in Cursor. Do not reuse Cursor’s case outputs.

### 4. Run records, PASS/FAIL, and evidence

For each host/run create `research/qualification/host-acceptance/<host>-<version>/<run-id>/run-log.md`. Record: local start/end timestamps for each stage; host/version; worktree commit SHA and clean status; normally discovered skill names; model/provider only if displayed; exact prompts; generated-file manifest; public URL plus opened locator; calculation tool/formula/output or `BLOCKED`; new-chat result; retries/errors and their resolution; operator elapsed time; tool time; tokens/charges only from host telemetry. Unavailable values are `UNKNOWN`, never guessed. Redact account identifiers and all secrets. Do not save credentials, cookies, personal information, raw OMP logs, or an unredacted desktop transcript.

Use this PowerShell setup once per run. Enter the exact host version in the slug (e.g. `codex-0.163.0`; for Cursor, use the version from **Help → About**) and use only letters, digits, dot, underscore or hyphen.

```powershell
$hostKey = Read-Host 'Host and version slug, e.g. codex-0.163.0'
if ($hostKey -notmatch '^[A-Za-z0-9._-]+$') { throw 'Use only letters, digits, dot, underscore or hyphen.' }
$base = 'C:\Projects\GitHub\megafon_hack\research\qualification\host-acceptance'
New-Item -ItemType Directory -Path $base -Force | Out-Null
$runId = Get-Date -Format 'yyyyMMdd-HHmmss'
$hostRoot = Join-Path $base $hostKey
New-Item -ItemType Directory -Path $hostRoot -Force | Out-Null
$runDir = Join-Path $hostRoot $runId
if (Test-Path $runDir) { throw 'Run folder already exists; choose a new runId.' }
$repo = (Get-Location).Path
$shaOutput = & git rev-parse HEAD 2>&1
$shaExit = $LASTEXITCODE
if ($shaExit -ne 0) {
    $shaOutput | Write-Output
    throw "git rev-parse HEAD failed (exit code $shaExit); record the output and stop."
}
$sha = ($shaOutput -join "`n").Trim()
if (-not $sha) { throw 'git rev-parse returned an empty commit SHA; stop.' }
New-Item -ItemType Directory -Path $runDir | Out-Null
$startedAt = Get-Date -Format o
$log = Join-Path $runDir 'run-log.md'
@"
# Host acceptance run
Host/version: $hostKey
Commit: $sha
Worktree: $repo
Started (local ISO-8601): $startedAt
Model/provider: UNKNOWN until displayed
Skills shown normally:
Stages (start/end, elapsed, PASS/FAIL/BLOCKED):
Errors/retries (append before retry):
Human time:
Tool time:
Tokens/observed charges: UNKNOWN until host telemetry is visible
Generated file manifest and redacted evidence:
"@ | Set-Content -Encoding utf8 $log
Write-Output $log
```

For each stage, capture start/end with `Get-Date -Format o`; calculate elapsed with `New-TimeSpan -Start $stageStart -End $stageEnd`. Append errors, retries and any manual assistance immediately. Use application telemetry for model/provider/tokens/charges; do not estimate. Never use `Start-Transcript` around account or credential screens.


Capture redacted screenshots of the normal skills listing and the generated case/resume evidence. Log each failure before retrying; manual edits to product outputs invalidate the “agent-generated workflow” PASS. Record the R1 SHA-256 output both before and after resume. A host-specific workflow passes only if all stage gates pass without forced skill calls or manual output substitution. Overall manual acceptance passes only when both hosts pass on separate cases at the same commit. Unknown cost remains an explicit cost limitation, not a measured cost.

The Codex `debug prompt-input` diagnostic previously showed all six names in the generated prompt input; it is not a normal `/skills` listing or workflow PASS. No host E2E is claimed until the above real run is recorded.


## Security, costs, and limitations

- [ ] Confirm no private MegaFon/customer data, real interview personal data, credentials, cookies or secrets are included.
- [ ] Confirm untrusted-source policy and host permission boundaries; instructions are not a sandbox.
- [ ] Record actual host/model/provider versions, services/tools, human time, tool time, retries/errors, token use and observed charges where available; label every unavailable value `UNKNOWN`.
- [ ] Distinguish synthetic/fixture-only evaluations from real user evidence; do not claim significance or superiority from one response per arm.
- [ ] Human owner approves any real interview, sensitive-data handling, external contact, spend, publication or launch.

## Demo and deliverables

- [ ] The public contest page says partner assignments are in the personal cabinet. Have the authorized team captain obtain the actual MegaFon brief through the account, verify the file/version, and share only the brief through an approved channel (never account credentials). Then confirm deadline, file/upload requirements and owner; do not replace the user-supplied working contract until verified.
- [ ] Complete the demo case using only allowed/open materials; preserve source-to-claim locators and reviewer notes.
- [ ] Record and watch the full video: no more than 10 minutes; includes intake, research, alternatives, strategy, validation and real pause/new-chat/resume/revision.
- [ ] Check video link access; preserve the original capture and final link.
- [ ] Prepare PDF/document with screenshots: architecture/context flow, all models/services/tools and their purpose, key instructions, additional capabilities, measured time/cost, errors/human assistance, and limitations.
- [ ] Ensure README, demo case, architecture/limitations, video script and checklist agree; remove stale “PASS” claims.
- [ ] Final human review; submit through the authorized account. No submission has been made by this agent.