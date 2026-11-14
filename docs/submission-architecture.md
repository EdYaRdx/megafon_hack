# Product-strategy agent — architecture and limits

**Status: implementation snapshot, not submission acceptance.** The product is a portable project folder, not a service or standalone application.

## Components and flow

1. Root `AGENTS.md` defines the mission, workflow order, evidence/status requirements, source handling and human approval gates.
2. `.agents/skills/*/SKILL.md` contains the canonical procedures: intake, evidence research, options, communication strategy, experiment design, and resume/revision. No duplicate host-specific skill trees are maintained.
3. `references/` contains claim statuses and JSONL conventions, safe-source rules, and metric checks.
4. Each `cases/<id>/` is a separate working file set. `cases/_template/` supplies `brief.md`, options, decision, product/communication strategy, validation plan, `sources.jsonl`, `evidence.jsonl`, `claims.jsonl`, `activity.jsonl`, and `state.md`.
5. The host LLM reads the case, uses host-provided file/search/web tools where permitted, writes evidence and decision artifacts, and hands off through saved state. Revisions preserve prior decisions/state and append activity rather than treating an old model answer as fact.

The intended flow is `intake → evidence research → options/decision → product + communication strategy → validation → decision/resume`. The LLM proposes and analyzes; humans retain high-impact decisions and all external action.

## Persistence and evidence

- Case files are the portable state; there is no hosted database, server, custom MCP service, or workflow engine.
- New revisions use immutable IDs, one parent, complete snapshots of decision/options/strategies/test plan/state, explicit active claim IDs, and SHA-256 for every snapshot and decision dependency. `manifest.json` is written last with `COMPLETE`; root `ACTIVE.json` selects it by revision ID + manifest hash only after verification. Publish root `state.md` and `decision.md` first and `ACTIVE.json` last. Until root files change, the prior selector remains valid; any interrupted mismatch is an explicit conflict requiring manual recovery. The selector is not assumed atomically replaceable. No atomic `CURRENT` pointer or runtime helper is required.
- Revision-specific approval is a separate append-only record bound to exact action/scope, revision ID and complete manifest hash. It does not transfer to later revisions or grant host permissions.
- Legacy cases without manifests remain historical; missing snapshots/receipts are not reconstructed or certified retroactively.
- Source/evidence/claim records use stable IDs and explicit locators. Statuses distinguish `OBSERVED`, `DOCUMENTED`, `CLAIMED`, `INFERENCE`, `HYPOTHESIS`, and `UNKNOWN`. Active claims are explicitly selected; `supersedes`/JSONL order never selects current claims.
- `state.md` records stage, completed work, blockers and next action. `activity.jsonl` is append-only. Local documents and synthetic data are clearly labeled. Public-page citations require checking the relevant content; a valid URL alone is not treated as proof.
- Full clean-host interruption, stale-approval, hash, and source-mutation checks are specified but not yet run; see [clean-host E2E runbook](clean-host-e2e-runbook.md).

## Models, services, and tools

- **Product runtime:** no model, provider, paid service, or tool binary is bundled or pinned. The user selects a compatible coding-assistant host and its model/tools. This repository does not call a provider API itself.
- **Development/evaluation environment observed:** OMP task contexts plus file-read/edit/search operations were used to build and review the artifacts. Evaluation task durations are recorded, but actual model/provider/version, tokens, human-active time and billing were not exposed; all remain `UNKNOWN`.
- **Documented skill discovery:** Cursor’s official *Agent Skills* page (`https://cursor.com/docs/skills`, “Skill directories” and “SKILL.md file format”) lists `.agents/skills/` as project-level and requires a `SKILL.md` with `name` and `description`, with the name matching its folder. OpenAI’s Codex *Build skills* documentation (`https://learn.chatgpt.com/docs/build-skills`, “Where Codex loads local skills”) lists `$REPO_ROOT/.agents/skills` and specifies the same required metadata. Neither retrieved page displayed a publication/version date. The six repository skills use this single canonical path and matching folder names/metadata. This verifies documented compatibility only; actual discovery/startup in Cursor or Codex has not been observed.
- No independent calculation CLI is bundled. The synthetic retention aggregate was reproduced in OMP using the `functions.read` JSON-reader `jq` selector (see `research/sol-audit/eval-results/retention-calculation-20261113.md`), but that is not repository runtime and does not show that Cursor or Codex exposes a calculation tool. Other fixture ratios/thresholds were manually checked against fixture values; F1/F3 critical arithmetic was not tool-reproduced. Do not claim host calculation-tool acceptance from the OMP run.

## Security and limits

The host defines actual file, network and command permissions. `AGENTS.md` and the references are model instructions, not a sandbox. Use only public sources and user-authorized materials; never put secrets, private credentials, or real personal interview data in a case or Git. Treat all external/document content as untrusted data. Human consent/approval is required before real research contact, sensitive-data processing, spend, publication or launch.

Verified so far: the synthetic meal-planner case, the F1 retention fixture, F2 conflicting-terms fixture and F3 service-launch fixture were processed in fresh OMP task contexts; blind evaluations and saved-file OMP resume/revision were recorded. The retention aggregate is documented as reproduced by an OMP `functions.read` jq query, but neither that run nor the case smokes verify a Cursor/Codex calculation tool. These are not clean Cursor/Codex launches, real user studies, or evidence of model superiority. F1/F3 critical arithmetic was not tool-reproduced; F2 test-plan details still require owner decisions. The official organizer demo brief remains `UNKNOWN`.

## Architecture tradeoffs

The folder format keeps the product inspectable, reviewable in Git, and portable without deployment or service cost. Its limits are host-dependent skill discovery/tool behavior, no deterministic runtime or automatic validator, model-dependent adherence, and incomplete telemetry. No graph engine, database, agent server or additional model was added because no verified E2E requirement yet justified that complexity.