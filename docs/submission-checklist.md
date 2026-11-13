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

## Prepared clean-host acceptance run

**Status:** not run in Cursor or Codex. The current environment has no `cursor` command in `PATH`; `codex-cli 0.163.0` and VS Code's `code` command are present. Two detached worktrees were created from product checkpoint `1323f992c86217730435a7074d823312268862c5`, at `C:\Projects\GitHub\megafon_hack-host-acceptance-1323f99` and `C:\Projects\GitHub\megafon_hack-host-acceptance-codex-1323f99`; they are refreshed to the same docs-only checkpoint as this checklist. Run `git log -1 --oneline` in each to confirm the current SHA. Both include the six canonical skill files. GUI skill discovery and host model calls remain unobserved.

1. Open the prepared folder in Cursor from the Start menu (**File → Open Folder**); do not open the populated authoring worktree. In **Customize → Skills**, capture the normally discovered skill list. If Cursor is installed elsewhere, open the folder manually; do not treat a missing CLI path as proof the app is absent.
2. In PowerShell, from the clean folder, prepare only a new case and raw synthetic inputs:

   ```powershell
   Set-Location 'C:\Projects\GitHub\megafon_hack-host-acceptance-1323f99'
   $repo = (Get-Location).Path
   $case = Join-Path $repo 'cases\host-acceptance-smoke'
   if (Test-Path $case) { throw "Choose a new, empty case path; do not overwrite." }
   Copy-Item (Join-Path $repo 'cases\_template') $case -Recurse
   New-Item -ItemType Directory -Path (Join-Path $case 'input') | Out-Null
   $source = Join-Path $repo 'cases\meal-planner-demo'
   Copy-Item (Join-Path $source 'brief.md') (Join-Path $case 'brief.md')
   Copy-Item (Join-Path $source 'input\concept-note.md') (Join-Path $case 'input\concept-note.md')
   Copy-Item (Join-Path $source 'input\beta-survey.csv') (Join-Path $case 'input\beta-survey.csv')
   ```

   Do **not** copy the populated case's sources, evidence, claims, options, decision, strategies, plan, state, activity, or revision notes into this new case. Ask the host to fetch/open the public method source `https://www.gov.uk/service-manual/user-research/user-research-in-discovery` directly. If the host cannot open it, record the failure rather than using the existing snapshot as a live fetch.
3. In the host's chat (Cursor Chat or the active Codex CLI session), use `prompts/first-run.md` and direct the agent to work only in `cases/host-acceptance-smoke/`, follow `AGENTS.md` and the canonical skill for each step, and complete the workflow from the supplied brief. Require source locators; for the CSV ratios, have the agent use a calculation tool available in that host and save its formula/query, input rows, units, and output. If the host exposes no permitted calculation tool, record `UNKNOWN/BLOCKED`; the existing OMP jq result does not count as host evidence. Also require three distinct options including status quo and stop, aligned product/communication strategies, a gated validation plan, and an exact next action in state. Do not give the result ratios as prompt answers; check the arithmetic independently afterward. No real data, contact, spending, build, or launch.
4. Pause after the full R1 artifacts are saved and one explicitly named case QA task remains in `state.md`. Copy the synthetic follow-up only after pausing:

   ```powershell
   Copy-Item (Join-Path $source 'input\revision-2-research-note.md') `
     (Join-Path $case 'input\revision-2-research-note.md')
   ```

   Open a genuinely new chat/session in the same host (for Codex, start a new `codex` CLI session). Ask it to resume from saved files, complete the named pending task, assess the new note, append successor claims/events, and preserve exact R1 decision/state snapshots. PASS only if it reads the saved state, does not silently repeat completed work, records the new input's synthetic provenance, and leaves real-world unknowns/gates intact.
5. For the second-host run, use the separate Codex worktree and its own case directory. In a new PowerShell session:

   ```powershell
   Set-Location 'C:\Projects\GitHub\megafon_hack-host-acceptance-codex-1323f99'
   git status --short --branch
   $repo = (Get-Location).Path
   $case = Join-Path $repo 'cases\host-acceptance-smoke'
   if (Test-Path $case) { throw "Choose a new, empty case path; do not overwrite." }
   Copy-Item (Join-Path $repo 'cases\_template') $case -Recurse
   New-Item -ItemType Directory -Path (Join-Path $case 'input') | Out-Null
   $source = Join-Path $repo 'cases\meal-planner-demo'
   Copy-Item (Join-Path $source 'brief.md') (Join-Path $case 'brief.md')
   Copy-Item (Join-Path $source 'input\concept-note.md') (Join-Path $case 'input\concept-note.md')
   Copy-Item (Join-Path $source 'input\beta-survey.csv') (Join-Path $case 'input\beta-survey.csv')
   ```

   This seeds only raw inputs in the Codex worktree; do not reuse Cursor outputs. Start `codex`, verify `/skills` normally, and repeat steps 3–4 using this worktree and case. Do not use explicit skill invocation to mask discovery failure.
6. For each host, record host/version, model/provider only if shown, discovered skill names, prompt, created files, source locators, one resumed incomplete task, revision/snapshot result, errors/retries, elapsed operator time, tool time, tokens/cost or `UNKNOWN`, and redacted screenshots in `research/qualification/host-acceptance/<host>-<version>/`.

**Pass gate:** both host listings and complete workflows are observed on separate clean copies of the same commit; source lookup is direct; output is newly generated; no manual writes substitute for agent work; saved-state resume and R1 preservation are verified. Missing GUI access, normal skill discovery, direct source access, or tool telemetry is a recorded FAIL/UNKNOWN, not a pass.


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