# Handoff — READY_FOR_HUMAN_ACCEPTANCE

**Date:** 2026-11-14. **Goal:** still active; awaiting human host acceptance, not complete.

## Git snapshot

- Branch `codex/megafon-mvp-file-agent`; last product/artifact checkpoint `1323f992c86217730435a7074d823312268862c5`. This follow-up checkpoint contains docs-only host runbook/status/handoff updates; run `git log -1 --oneline` for its exact tip SHA.
- At phase start, local `origin/codex/megafon-mvp-file-agent` matched HEAD 1323f992 (0 ahead/behind). An unauthenticated `git ls-remote` with credential helpers and prompts disabled failed: `could not read Username for 'https://github.com': terminal prompts disabled`. No credentials were accessed; fresh remote confirmation and push remain blocked.
- Two detached clean worktrees are prepared at `C:\Projects\GitHub\megafon_hack-host-acceptance-1323f99` and `C:\Projects\GitHub\megafon_hack-host-acceptance-codex-1323f99`. Before use, verify both are clean and `git rev-parse HEAD` matches the runbook commit you intend to test. The first supports Cursor; the second is isolated for Codex.
- Current environment: no `cursor` command or executable was found in the standard locations checked; `codex-cli 0.163.0` is present. A read-only `codex debug prompt-input` diagnostic from the Codex worktree, with config/home variables pointed at a temporary directory, showed all six skill names in the generated prompt input; temporary data was removed and no model call occurred. This is not the normal `/skills` listing, GUI discovery, or workflow acceptance. No GUI or model call was run.

## Current state and evidence

- Stage F; README, architecture, video run sheet, and checklist are drafts. Product acceptance is incomplete.
- The video run sheet now warns that populated repository outputs must not be presented as live-generated; it calls for a separate fresh output folder and stages synthetic R2 then R3 around the new-chat resume. It remains an unexecuted plan, not video or host acceptance.
- `retention-demo` is R2. Exact R1 state/decision snapshots are in `cases/retention-demo/revisions/`. R2 appends E-008 and C-008 (`supersedes: C-001`); recommendation stays `HUMAN_REVIEW_REQUIRED`. A fresh OMP task resumed the case from saved files, resolved the active pointers and next action without re-running the calculation, and an independent reviewer passed the artifacts and trace.
- The internal jq/read-tool calculation returned April `620/1000 = 62%`, May `380/1000 = 38%`, `−24 pp`; immature June was excluded. Independent review passed the arithmetic and source locators. Operational definitions of the D30 return event and `eligible_users` remain `UNKNOWN`; this is not semantic validation or IDE acceptance.
- Independent reviewer examined the 75-file checkpoint; no P0/P1/P2 findings in scope. 15 changed JSONL files parsed; cross-reference checks passed for four changed case ledgers. Common credential-pattern scan found no matches (not a comprehensive secret audit). No build/unit suite or IDE run was performed.
- `docs/submission-checklist.md` contains exact Cursor/Codex setup, neutral first-run request, expected artifacts and PASS/FAIL/BLOCKED gates, new-chat revision-2 resume, R1 hash checks, cost-authorization boundary, and run-log template. A tracked-file inventory found no automated test harness; prior successful smoke checks and synthetic evaluations were not rerun. An independent reviewer passed the expanded instructions with no P0/P1/P2. No real host workflow was executed.
- Codex prompt-input check: `codex debug prompt-input "Use the relevant project skills to plan a synthetic product strategy workflow. Do not run tools or execute a model."` from the clean Codex worktree, with `CODEX_HOME`, `USERPROFILE`, `HOME`, `APPDATA`, and `LOCALAPPDATA` redirected to a temporary directory. The emitted prompt-input included all six canonical names; temp data was removed. This diagnostic does not satisfy the checklist’s normal `/skills` listing or full workflow gate.

## Checkpoint contents

- Commit `4813ae217d8ef1a8b2324d5d16d4c846e1e4974d` contains 75 reviewed project artifacts: case studies, templates, evidence/claim guidance, evaluation records, and updated status/demo docs.
- `.omp/profiles/product-build.yml` remains untracked and user-owned; it was expressly excluded.

## Blockers and next action

- Unverified: clean launch/skill discovery and new-chat resume in Cursor plus a second host; calculation-tool availability in those hosts; final acceptance.
- External: authorized captain must supply the official MegaFon demo brief; an authorized metric owner must define the D30 event and eligibility contract and provide an approved cohort export before real-data use.
- **Next action:** the human opens the clean Cursor worktree and follows the manual run in `docs/submission-checklist.md`; then repeats in the separate Codex worktree at the same commit. Record normal skill discovery, generated files, direct source/calculation evidence, pause/new-chat resume, R1 hashes, time/cost/errors, and redacted screenshots in the specified run folder. Return the run logs for review. Keep the Goal at `READY_FOR_HUMAN_ACCEPTANCE`; do not wait for a host here or mark host acceptance PASS before the logs exist. Research Tool `deep_research action=status` schema defect remains recorded; no code change or paid Polza call.
