# Submission checklist — working draft

Do not mark an item PASS without a saved artifact or observed run. The official public page says partner assignments are in the personal cabinet; the exact MegaFon demo brief and its provenance remain `UNKNOWN` until an authorized team member obtains and verifies the file. See [`official-demo-brief-availability.md`](../research/qualification/official-demo-brief-availability.md).

## Repository and product

- [ ] Confirm the correct feature branch and commit; review all staged/tracked changes; exclude `.omp/profiles/product-build.yml`, credentials, personal data and raw session logs.
- [ ] Publish the reviewed feature branch without force-push; verify the repository link and jury access.
- [ ] Replace synthetic demo inputs only when an official brief is published; otherwise use clearly labeled public/open or fictional data.
- [ ] Follow root README from a clean checkout; verify file access, skill discovery, case creation, evidence locators, options, both strategies, validation, state save and resume.
- [ ] **Optional portability gate:** only if the product claim includes cross-host portability, test skill discovery/use in Cursor and a second compatible host. For a single-host demo, run one explicitly named host; a second host is not a general contest/demo prerequisite. In either host, distinguish normal discovery from manual fallback; names alone do not prove workflow use. If use cannot be observed, record `UNOBSERVED`, not PASS. Save host/version, trace/result and redacted evidence under `research/qualification/host-acceptance/<host>-<version>/`; omit account details, notifications, credentials and personal data.
- [ ] Exercise a genuinely new chat/session: pause, resume from files, continue one unfinished task, then ingest new synthetic/authorized data and revise without overwriting the previous decision.
- [ ] Reproduce any decision-critical calculation with a tool; preserve input locators, formula, units, output and narrow test. One synthetic retention calculation was executed via the internal JSON-reader jq selector and independently reviewed (`../research/sol-audit/eval-results/retention-calculation-20261113.md`); this verifies OMP/read-tool arithmetic only, not IDE/agent-tool availability. Current F1/F3 arithmetic has not been run through a calculation tool.
- [ ] Verify all claims against actual content, paths/locators, dates and denominators; independent reviewer checks the saved artifacts and response, not just the explanation.
- [ ] Confirm status quo, close/stop, tradeoffs, strong objections, product/communication alignment, comparator, metric denominator, period, guardrails and threshold/revisit are explicit or honestly `UNKNOWN` and gated.

## Manual clean-host acceptance runbook — Cursor pending; full checklist not yet executed

**State:** no Cursor GUI/model workflow has been observed. Actual Codex CLI R1/R2 synthetic runs were reported for versions 0.166.0 and 0.169.0 and independently audited as `PARTIAL PASS`; see [`acceptance-review.md`](../research/qualification/host-acceptance/codex-0.169.0/20261114-r1-r2/acceptance-review.md). The user-provided provenance summary reports separate sessions and structural log diagnostics, but raw logs were not reviewed and do not prove successful calls or automatic Skill activation. This stricter clean-worktree runbook has not been executed. A Codex replay is optional for the saved-artifact guided demo but can satisfy additional observable discovery/use checks; Cursor remains an optional portability check for Codex-demo readiness. The user reports remote branch `codex/megafon-mvp-file-agent` at `a7701a5e4352710df7dc86a54abb3aca22a783f3`; this is not evidence that the commands below were run. GitHub static reads returned 404 and local HEAD/status equality is unverified. The pre-created `1323f99` worktrees are older; do not use, modify, or delete them. Use the guarded setup below only if running the additional clean-host checks; initialize a separate run log and do not open the populated authoring worktree.

Before any model call, use only a host entitlement already authorized for this test. If the host requires a new purchase, unapproved pay-as-you-go usage, or enabling a paid service, stop and mark `BLOCKED`; do not purchase or assume the call is free. Record any observed charge, otherwise `UNKNOWN`.

- **Automated tests:** the overnight tracked-file inventory found no runnable test/build/lint harness. This checklist update changes documentation only; no application code changed and no suite was run. The PowerShell clean-worktree commands below are instructions only, not executed in this session. The prior real Codex R1/R2 run is documented separately and does not establish Cursor behavior or all gates in this runbook.

### 0. Optional cross-host portability runbook (Cursor + Codex)

The user reports that full SHA `a7701a5e4352710df7dc86a54abb3aca22a783f3` is the published branch HEAD. The old pre-created `1323f99` worktrees do not contain it. The guarded PowerShell 5.1 procedure fetches `codex/megafon-mvp-file-agent`, checks that the remote branch tip is exactly the reported SHA, then creates new detached worktrees at that SHA. If fetch fails, the tip differs, or a destination already exists, stop and preserve all existing worktrees; do not force, overwrite, or remove anything.

For a single-host product/demo acceptance, create one clean worktree for the named target host and run the single-host gates. Only if claiming cross-host portability, use the two-worktree procedure below and complete both host runs at the same full SHA:

```powershell
$ErrorActionPreference = 'Stop'
Get-Command git -ErrorAction Stop | Out-Null
$source = 'C:\Projects\GitHub\megafon_hack'
$branch = 'codex/megafon-mvp-file-agent'
$sha = 'a7701a5e4352710df7dc86a54abb3aca22a783f3'
$cursorRepo = 'C:\Projects\GitHub\megafon_hack-host-acceptance-cursor-a7701a5e'
$codexRepo = 'C:\Projects\GitHub\megafon_hack-host-acceptance-codex-a7701a5e'

foreach ($path in @($cursorRepo, $codexRepo)) {
    if (Test-Path $path) { throw "Path already exists; choose a new unused path: $path" }
}

$fetchOutput = & git -C $source fetch --no-tags origin $branch 2>&1
$fetchExit = $LASTEXITCODE
if ($fetchExit -ne 0) {
    $fetchOutput | Write-Output
    throw "Git fetch failed (exit code $fetchExit); record the output and stop."
}
$fetchOutput | Write-Output

$remoteShaOutput = & git -C $source rev-parse 'FETCH_HEAD^{commit}' 2>&1
$remoteShaExit = $LASTEXITCODE
if ($remoteShaExit -ne 0) {
    $remoteShaOutput | Write-Output
    throw "Fetched branch SHA lookup failed (exit code $remoteShaExit); stop."
}
$remoteSha = ($remoteShaOutput -join "`n").Trim()
if ($remoteSha -ne $sha) {
    throw "Fetched branch tip is $remoteSha, not the reported SHA $sha; stop and reconcile before testing."
}

$objectOutput = & git -C $source cat-file -e "$($sha)^{commit}" 2>&1
$objectExit = $LASTEXITCODE
if ($objectExit -ne 0) {
    $objectOutput | Write-Output
    throw "Published commit object is unavailable locally (exit code $objectExit); stop."
}

$cursorOutput = & git -C $source worktree add --detach $cursorRepo $sha 2>&1
$cursorExit = $LASTEXITCODE
if ($cursorExit -ne 0) {
    $cursorOutput | Write-Output
    throw "Cursor worktree creation failed (exit code $cursorExit); preserve any partial result and stop."
}
$cursorOutput | Write-Output

$codexOutput = & git -C $source worktree add --detach $codexRepo $sha 2>&1
$codexExit = $LASTEXITCODE
if ($codexExit -ne 0) {
    $codexOutput | Write-Output
    throw "Codex worktree creation failed (exit code $codexExit); preserve any partial result and stop."
}
$codexOutput | Write-Output

$cursorShaOutput = & git -C $cursorRepo rev-parse HEAD 2>&1
$cursorShaExit = $LASTEXITCODE
if ($cursorShaExit -ne 0) {
    $cursorShaOutput | Write-Output
    throw "Cursor worktree SHA check failed (exit code $cursorShaExit); stop."
}
$cursorSha = ($cursorShaOutput -join "`n").Trim()

$codexShaOutput = & git -C $codexRepo rev-parse HEAD 2>&1
$codexShaExit = $LASTEXITCODE
if ($codexShaExit -ne 0) {
    $codexShaOutput | Write-Output
    throw "Codex worktree SHA check failed (exit code $codexShaExit); stop."
}
$codexSha = ($codexShaOutput -join "`n").Trim()
if ($cursorSha -ne $sha -or $codexSha -ne $sha) { throw 'Worktrees do not match the intended full SHA.' }

$cursorStatus = & git -C $cursorRepo status --porcelain 2>&1
$cursorStatusExit = $LASTEXITCODE
if ($cursorStatusExit -ne 0) {
    $cursorStatus | Write-Output
    throw "Cursor worktree status check failed (exit code $cursorStatusExit); stop."
}
if (($cursorStatus -join "`n").Trim()) { throw 'Cursor worktree is not clean; preserve it and stop.' }

$codexStatus = & git -C $codexRepo status --porcelain 2>&1
$codexStatusExit = $LASTEXITCODE
if ($codexStatusExit -ne 0) {
    $codexStatus | Write-Output
    throw "Codex worktree status check failed (exit code $codexStatusExit); stop."
}
if (($codexStatus -join "`n").Trim()) { throw 'Codex worktree is not clean; preserve it and stop.' }
Write-Output "Both clean worktrees verified at $sha"
```

PowerShell 5.1-compatible. Every native Git call is followed immediately by an exit-code check. On any failure, preserve partial results and old worktrees; do not retry over or delete them. The setup commands are instructions only and have not been executed in this session.

### 1. Cursor — clean copy, ordinary skill discovery

1. In PowerShell, verify the prepared Cursor worktree before opening it:

   ```powershell
   $ErrorActionPreference = 'Stop'
   $repo = 'C:\Projects\GitHub\megafon_hack-host-acceptance-cursor-a7701a5e'
   $expectedSha = 'a7701a5e4352710df7dc86a54abb3aca22a783f3'
   Get-Command git -ErrorAction Stop | Out-Null
   if (-not (Test-Path -LiteralPath $repo -PathType Container)) { throw "Cursor worktree does not exist: $repo" }
   $statusLine = & git -C $repo status --short --branch 2>&1
   $statusLineExit = $LASTEXITCODE
   if ($statusLineExit -ne 0) { $statusLine | Write-Output; throw "Cursor status failed ($statusLineExit)." }
   $statusLine | Write-Output
   $headOutput = & git -C $repo rev-parse HEAD 2>&1
   $headExit = $LASTEXITCODE
   if ($headExit -ne 0) { $headOutput | Write-Output; throw "Cursor SHA lookup failed ($headExit)." }
   $head = ($headOutput -join "`n").Trim()
   if ($head -ne $expectedSha) { throw "Cursor worktree is $head, not $expectedSha." }
   $statusOutput = & git -C $repo status --porcelain 2>&1
   $statusExit = $LASTEXITCODE
   if ($statusExit -ne 0) { $statusOutput | Write-Output; throw "Cursor cleanliness check failed ($statusExit)." }
   if (($statusOutput -join "`n").Trim()) { throw 'Cursor worktree is not clean; preserve it and stop.' }
   ```

   Record the checked full SHA and clean status. In Windows Start, launch Cursor → **File → Open Folder** → select this exact `$repo`; do not open the authoring checkout. Record the exact Cursor version from **Help → About**. In **Customize → Skills**, save the normally discovered names and redacted evidence. The six names are `intake`, `evidence-research`, `options-decision`, `strategy-communication`, `experiment-design`, `resume-revise`. Do not invoke skills manually. If Cursor cannot open or discovery/use cannot be observed, record `BLOCKED` or `UNOBSERVED`, not PASS.
   Before creating the case or making any model call, run the Section 4 run-log setup with a `cursor-<version>` slug while the verified worktree is still clean.

2. In the Cursor worktree, create a new blank case with fictional raw inputs only. Do not reuse any populated case outputs:

   ```powershell
   $caseRelative = 'cases/host-acceptance-cursor-a7701a5e'
   $case = Join-Path $repo $caseRelative
   if (Test-Path $case) { throw 'Cursor case already exists; choose a new unused case path.' }
   Copy-Item (Join-Path $repo 'cases\_template') $case -Recurse
   $input = Join-Path $case 'input'
   New-Item -ItemType Directory -Path $input | Out-Null
   $brief = @'
   # Synthetic dinner-planning launch decision

   All names, responses and product details below are fictional test data, not evidence about a real company, product, or users.

   Decision: should a hypothetical team launch a paid dinner-planning add-on next month, first authorize bounded discovery/validation, keep the current product unchanged, or stop this direction?

   Available material: input/concept-note.md and input/survey.csv. The survey is a deliberately small non-random synthetic exercise. Its question wording, recruitment, product cost, dietary-safety process, price, support load, owner and deadline are UNKNOWN. No user contact, spend, build, launch, or public communication is authorized.

   The actual decision owner and audience are UNKNOWN. Do not infer population demand from respondent counts or click interest.
   '@
   $concept = @'
   # Fictional concept note

   A hypothetical team is considering three dinner suggestions each week based on a user's time limit and dietary preferences. The feature is not built. There is no validated recipe catalogue, dietary-safety review, price, delivery estimate, support plan, or approval.
   '@
   $survey = @'
   channel,invited,responded,clicked_interested,random_sample,question_wording_known,synthetic
   newsletter,80,20,11,false,false,true
   beta_users,40,16,9,false,false,true
   '@
   Set-Content -Path (Join-Path $case 'brief.md') -Value $brief -Encoding UTF8
   Set-Content -Path (Join-Path $input 'concept-note.md') -Value $concept -Encoding UTF8
   Set-Content -Path (Join-Path $input 'survey.csv') -Value $survey -Encoding UTF8
   ```

   Only the blank template, this brief and these raw inputs are seeded. Do not copy source/evidence/claim journals, options, decisions, strategies, test plans, states, activity or revisions from any prior case.

3. In Cursor Chat, send this **single ordinary request**. Do not name, select, or invoke individual skills:

   ```text
   Проведи сквозную приёмку синтетического дела только в cases/host-acceptance-cursor-a7701a5e/. Прочитай brief, исходные input-файлы, AGENTS.md и prompts/first-run.md; соблюдай проектные инструкции и штатное обнаружение возможностей. Не называй, не выбирай и не вызывай отдельные skills вручную; не используй готовые ответы или результаты других дел.

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
| Skill discovery/use | Host UI listing plus host-visible trace or runtime evidence | All six canonical names appear in normal discovery; relevant skill use is evidenced by host-visible selection/loading or comparable trace without manual invocation. | Listing-only, model self-report or manual invocation is not proof; no observable use is `UNOBSERVED`, so the gate remains unverified and overall acceptance cannot PASS. |
| Evidence/research | `sources.jsonl`, `evidence.jsonl`, `claims.jsonl`; source snapshot under `sources/` when available | Direct page attempt; publisher/date/version where displayed; relevant content checked and exact locator recorded; source/evidence/claim references resolve; claim statuses distinguish observation, documentation, claim, inference, hypothesis and unknown; CSV calculation includes input rows, formula, numerator, denominator, units and host-tool result. | URL-only citation, unchecked page content, wrong denominator, invented source content; tool/site unavailable is `BLOCKED`, never PASS. |
| Alternatives/decision | `options.md`, `decision.md`, updated `claims.jsonl` and `state.md` | At least three materially different options, including status quo and stop; tradeoffs and strong objections; conditional, human-review-only recommendation. | Fewer or cosmetic options, omitted stop/status quo, no serious objection, or launch presented as approved. |
| Strategy/validation | `strategy-product.md`, `strategy-communication.md`, `test-plan.md` | Strategies agree on audience, value, evidence, promise and limits. Plan names comparator, metric/denominator, period, guardrails, owner, decision rule and revisit trigger; unknowns remain gated. | Contradictory promise/strategy or missing comparator, metric/guardrail/decision rule. |
| R1 pause | `revisions/state-r1.md`, `revisions/decision-r1.md`, current `state.md`, appended `activity.jsonl` | Exact snapshots saved; one named unfinished task and one exact next action; no real-world validation or launch approval claimed. | No snapshots/pending task, or case says complete despite unfinished work. |
| New-chat resume/revise | `input/revision-2-research-note.md`, current `state.md`/`decision.md`, appended ledgers as warranted | New session reads saved state, finishes the named task, labels note synthetic, appends only justified successors/events, and preserves both R1 snapshots byte-for-byte. | Snapshot hash changes, silent repetition, lost provenance, or synthetic claims promoted to real evidence. |

Missing files, invented source content, wrong denominator, forced/manual skill invocation, hand-written outputs standing in for agent work, overwritten R1 snapshots, or unlogged retries are `FAIL`. If a host tool or public page is unavailable, record `BLOCKED` with the exact attempt and error; do not report a full PASS. Immediately after the R1 gate and before adding R2 input, record the snapshot hashes:

```powershell
$ErrorActionPreference = 'Stop'
$r1Snapshots = @((Join-Path $case 'revisions\state-r1.md'), (Join-Path $case 'revisions\decision-r1.md'))
foreach ($path in $r1Snapshots) { if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { throw "Missing R1 snapshot: $path" } }
   $hashLabel = Read-Host 'Type before resume or after resume'
   if ($hashLabel -notin @('before resume', 'after resume')) { throw 'Use exactly before resume or after resume.' }
   Write-Output "R1 snapshot hashes — $hashLabel"
Get-FileHash -Algorithm SHA256 -Path $r1Snapshots
```

After the new chat finishes, run the same block again and enter “after resume.” Both hashes must match exactly. Append both outputs to the run log. If using a new PowerShell session, set `$case` to the exact host-specific case path first.

3. After the R1 gate passes, pause the first chat. Only then create the R2 synthetic input:

   ```powershell
   $revision = @'
   # Synthetic R2 interview summary

   Suppose eight purposively selected fictional participants discussed a recent dinner-planning episode: five described a recurring planning difficulty and three described no meaningful difficulty. Recruitment, interview wording, coding and profiles are not independently observed. Do not extrapolate to a population or treat this as real demand. This changes only the fictional scenario-level hypothesis; no launch or external research is authorized.
   '@
   Set-Content -Path (Join-Path $case 'input\revision-2-research-note.md') -Value $revision -Encoding UTF8
   ```

   Open a genuinely new Cursor chat in the same worktree and send:

   ```text
   Continue this case from its saved files. First read state.md and identify the current revision and exact next action; do not rely on the previous chat. Complete the named pending task, inspect the new input/revision-2-research-note.md as synthetic evidence, and update only the successor evidence/claims/decision/state needed. Do not repeat completed source lookup or calculations without a recorded reason. Preserve revisions/state-r1.md and revisions/decision-r1.md byte-for-byte; append the event and record provenance, limits, errors and the next action. Do not invoke a skill explicitly or treat synthetic reports as real-world evidence.
   ```

### 3. Codex — repeat independently on its clean copy

1. In a new PowerShell session, verify the separate Codex worktree:

   ```powershell
   $ErrorActionPreference = 'Stop'
   $repo = 'C:\Projects\GitHub\megafon_hack-host-acceptance-codex-a7701a5e'
   $expectedSha = 'a7701a5e4352710df7dc86a54abb3aca22a783f3'
   Get-Command git -ErrorAction Stop | Out-Null
   Get-Command codex -ErrorAction Stop | Out-Null
   if (-not (Test-Path -LiteralPath $repo -PathType Container)) { throw "Codex worktree does not exist: $repo" }
   $statusLine = & git -C $repo status --short --branch 2>&1
   $statusLineExit = $LASTEXITCODE
   if ($statusLineExit -ne 0) { $statusLine | Write-Output; throw "Codex status failed ($statusLineExit)." }
   $statusLine | Write-Output
   $headOutput = & git -C $repo rev-parse HEAD 2>&1
   $headExit = $LASTEXITCODE
   if ($headExit -ne 0) { $headOutput | Write-Output; throw "Codex SHA lookup failed ($headExit)." }
   $head = ($headOutput -join "`n").Trim()
   if ($head -ne $expectedSha) { throw "Codex worktree is $head, not $expectedSha." }
   $statusOutput = & git -C $repo status --porcelain 2>&1
   $statusExit = $LASTEXITCODE
   if ($statusExit -ne 0) { $statusOutput | Write-Output; throw "Codex cleanliness check failed ($statusExit)." }
   if (($statusOutput -join "`n").Trim()) { throw 'Codex worktree is not clean; preserve it and stop.' }
   Set-Location -LiteralPath $repo
   $versionOutput = & codex --version 2>&1
   $versionExit = $LASTEXITCODE
   if ($versionExit -ne 0) { $versionOutput | Write-Output; throw "Codex version check failed ($versionExit)." }
   $versionOutput | Write-Output
   ```
   Require the same full SHA as the Cursor worktree and record the displayed Codex version. Seed the new case below before starting a model session.
   Before creating the case or launching a model, run the Section 4 run-log setup with a `codex-<version>` slug while the verified worktree is still clean.

   Create a separate blank Codex case with a different fictional brief and dataset:

   ```powershell
   $caseRelative = 'cases/host-acceptance-codex-a7701a5e'
   $case = Join-Path $repo $caseRelative
   if (Test-Path $case) { throw 'Codex case already exists; choose a new unused case path.' }
   Copy-Item (Join-Path $repo 'cases\_template') $case -Recurse
   $input = Join-Path $case 'input'
   New-Item -ItemType Directory -Path $input | Out-Null
   $brief = @'
   # Synthetic library reminder decision

   Fictional exercise only. Should a hypothetical library team keep the status quo, authorize bounded discovery, consider an SMS reminder, or stop this direction? No real library, patrons or usage are represented. Owner, deadline, SMS capability, cost, consent, privacy review and authority are UNKNOWN. No contact, spend, build, message or external action is authorized.

   `input/loan-reminders.csv` contains a small fictional, non-random summary. Its counts do not establish causality or population impact. `input/concept-note.md` records the unbuilt concept. Treat every source as synthetic.
   '@
   $concept = @'
   # Synthetic concept note

   A hypothetical library app team is considering an SMS due-date reminder. No SMS service is integrated; delivery, consent, privacy review, costs, user need and any operational owner are unknown.
   '@
   $data = @'
   group,eligible_loans,reminders_sent,delivered,opened,returned_by_due,randomized,synthetic
   reminder,18,18,16,8,11,false,true
   comparison,18,0,0,0,10,false,true
   '@
   $vendor = @'
   # Fictional vendor note

   A fictional supplier asserts “20% fewer late returns” but supplies no definition, denominator, period, comparator or method. This is an unsupported claim, not a measured result.
   '@
   Set-Content -Path (Join-Path $case 'brief.md') -Value $brief -Encoding UTF8
   Set-Content -Path (Join-Path $input 'concept-note.md') -Value $concept -Encoding UTF8
   Set-Content -Path (Join-Path $input 'loan-reminders.csv') -Value $data -Encoding UTF8
   Set-Content -Path (Join-Path $input 'vendor-note.md') -Value $vendor -Encoding UTF8
   ```

After the brief and raw inputs above exist, start `codex` from this PowerShell session (current directory is the verified `$repo`), save the ordinary `/skills` listing, then send the single first-run request from the Cursor section with only the case path changed to `cases/host-acceptance-codex-a7701a5e/`. Do not invoke `$intake` or any skill manually. Record host-visible use evidence or `UNOBSERVED`; apply the same stage gates and log errors, time, cost and output files.

After the first-run R1 gates pass, record both R1 hashes with the command above, label them “before resume,” and pause/close the first Codex chat. Create the synthetic R2 input below only after that pause:

   ```powershell
   $revision = @'
   # Synthetic R2 consent constraint

   In this fictional scenario, a hypothetical review says a reminder may be sent only after explicit individual patron opt-in. This is not a real law, policy, review or approval and does not authorize contact or implementation. Reassess options and communication; do not repeat completed research or calculations without a recorded reason.
   '@
   Set-Content -Path (Join-Path $case 'input\revision-2-research-note.md') -Value $revision -Encoding UTF8
   ```

After creating the R2 input, start a genuinely new `codex` session and send the same resume request shown in the Cursor section, with this Codex case selected; do not force skills or reuse Cursor outputs. After the new chat finishes, run the R1 hash command again, label the output “after resume,” and require both hashes to match.

### 4. Run records, PASS/FAIL, and evidence

For each host/run create `research/qualification/host-acceptance/<host>-<version>/<run-id>/run-log.md`. Record: local start/end timestamps per stage; host/version; full worktree SHA and clean status; normal skill list plus host-visible evidence of actual skill use or `UNOBSERVED`; exact prompts; generated-file manifest; public URL and opened locator; calculation tool/formula/input rows/output or `BLOCKED`; new-chat result; retries/errors and resolutions; operator/tool time; tokens/charges only from host telemetry. Unavailable values are `UNKNOWN`, never guessed. Redact account identifiers and secrets. Do not save credentials, cookies, personal data, raw OMP logs, or unredacted desktop transcripts.

Run this once per host **after noting its displayed version but before seeding its case or making a model call**, while the tested worktree is clean. It stores the redacted run log under the authoring checkout, not in the tested worktree; do not commit logs without review. Use an exact version slug (e.g. `codex-0.163.0`; for Cursor, the value from **Help → About**) with only letters, digits, dot, underscore or hyphen.

```powershell
$ErrorActionPreference = 'Stop'
Get-Command git -ErrorAction Stop | Out-Null
$hostKey = Read-Host 'Host and version slug, e.g. codex-0.163.0'
if ($hostKey -notmatch '^(cursor|codex)-[A-Za-z0-9._-]+$') { throw 'Use a cursor- or codex- version slug with letters, digits, dot, underscore or hyphen.' }
$base = 'C:\Projects\GitHub\megafon_hack\research\qualification\host-acceptance'
New-Item -ItemType Directory -Path $base -Force | Out-Null
$runId = Get-Date -Format 'yyyyMMdd-HHmmss'
$hostRoot = Join-Path $base $hostKey
New-Item -ItemType Directory -Path $hostRoot -Force | Out-Null
$runDir = Join-Path $hostRoot $runId
if (Test-Path $runDir) { throw 'Run folder already exists; choose a new runId.' }
if ($hostKey -like 'cursor-*') { $repo = 'C:\Projects\GitHub\megafon_hack-host-acceptance-cursor-a7701a5e' }
elseif ($hostKey -like 'codex-*') { $repo = 'C:\Projects\GitHub\megafon_hack-host-acceptance-codex-a7701a5e' }
else { throw 'Host/version slug must start with cursor- or codex-.' }
$expectedSha = 'a7701a5e4352710df7dc86a54abb3aca22a783f3'
$shaOutput = & git -C $repo rev-parse HEAD 2>&1
$shaExit = $LASTEXITCODE
if ($shaExit -ne 0) {
    $shaOutput | Write-Output
    throw "git rev-parse HEAD failed (exit code $shaExit); record the output and stop."
}
$sha = ($shaOutput -join "`n").Trim()
if ($sha -ne $expectedSha) { throw "Worktree is $sha, not expected $expectedSha." }
$statusOutput = & git -C $repo status --porcelain 2>&1
$statusExit = $LASTEXITCODE
if ($statusExit -ne 0) {
    $statusOutput | Write-Output
    throw "git status failed (exit code $statusExit); record the output and stop."
}
if (($statusOutput -join "`n").Trim()) { throw 'Worktree is not clean before the case run; preserve it and stop.' }
New-Item -ItemType Directory -Path $runDir | Out-Null
$startedAt = Get-Date -Format o
$log = Join-Path $runDir 'run-log.md'
@"
# Host acceptance run
Host/version: $hostKey
Commit: $sha
Initial status: clean
Worktree: $repo
Started (local ISO-8601): $startedAt
Model/provider: UNKNOWN until displayed
Skills discovered normally:
Skill-use evidence (or UNOBSERVED):
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


Capture redacted screenshots of the normal skills listing and generated case/resume evidence. Log each failure before retrying; manual edits to product outputs invalidate the “agent-generated workflow” PASS. Record R1 SHA-256 outputs before and after resume. If host-visible skill-use evidence is unavailable, record `UNOBSERVED` and do not pass the skills-use gate. A host-specific workflow passes only if all stage gates pass without forced skill calls or manual output substitution. **Single-host acceptance** requires all stage gates to pass for one named host. **Cross-host portability** requires both hosts to pass on separate cases at the same full SHA. Unknown costs remain an explicit limitation, not a measured cost.

The Codex `debug prompt-input` diagnostic previously showed all six names in the generated prompt input; it is not a normal `/skills` listing or workflow PASS. No **clean-host acceptance** is claimed until the selected host's real run is recorded; historical reported Codex R1/R2 remains `PARTIAL PASS`, not a clean-host or cross-host PASS.


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