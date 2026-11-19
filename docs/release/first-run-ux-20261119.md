# First Run UX — bounded implementation and verification

Date: 2026-11-19. Base: `origin/main` at `ef18ae9`. Feature branch: `feat/first-run-ux-20261119`. One isolated implementation worktree; original working files and existing changes were not edited. `megafon_hack-manual-test` was not used or modified.

## Change and invariants

The instructional router is `prompts/first-run.md`, reached through root `AGENTS.md` and the two entry Skills. NEW / RESUME / REVISE / HELP run before case-file access. The first response is task paraphrase, required clarification or concrete case-creation proposal, and one next step. NEW requires consent to the exact path; RESUME/REVISE require an explicit existing path. No neighboring-case discovery or automatic latest-case selection.

`tools/case_workspace.py` is a narrow stdlib filesystem helper, not a launcher, runtime, natural-language classifier, approval gate or sandbox. It accepts bounded project-relative paths, rejects occupied files/directories and links/junctions, reserves the new directory exclusively and copies `_template` without merging. The unchanged protocol marker is published last by rename from a pending copy. Partial failures remain preserved and fail protocol classification; they are never retried into the same directory.

After actual creation/selection, the agent states CASE root and follows existing Intake or resume-revise. `tools/case_protocol.py`, checkpoint formats, machine-control fields, selector publication, approval contracts and historical cases are unchanged. Template changes are onboarding prose only. Creation consent is not execution approval or host permission.

## Offline checks

Executed with CPython 3.12 in the feature worktree:

```sh
python -m unittest discover -s tests -p 'test_case_workspace.py' -v
python -m unittest discover -s tests -p 'test_case_protocol.py' -v
```

The actual executable was an operator-supplied CPython 3.12 installation; `python` above is portable notation, not a successful host alias.

- Final workspace suite: **12 tests, OK, 1 skipped**. Covers exact template bytes and FRESH/not-CHECKPOINTED, empty approvals/no ACTIVE, occupied directory/file preservation, invalid/traversing/absolute/reserved paths, read-only explicit existing selection, missing case/template, injected PermissionError, interrupted ordinary/marker copy followed by fail-closed resume, competing creators, CLI receipts and actual Windows junction rejection.
- Existing protocol suite: **37 tests, OK, 1 skipped**. Includes candidate/selector/checkpoint/resume consumers, snapshots and hashes, parent lineage/forks, claims, append-only prefixes, legacy scope and incomplete states. No full evaluator suite or H1/research was run.
- Symlink tests skipped because Windows returned WinError 1314 (privilege unavailable). The separate Windows junction regression actually ran and passed. PermissionError was deterministically injected; no real Windows ACL-denial qualification is claimed.

These offline tests prove filesystem/consumer behavior. Natural-language intent, consent interpretation and first-response wording are instructions, not a deterministic parser; they are assessed separately below, not asserted by source-text tests.

## Real host execution

Actual OMP **19.0.0**, `openai-codex/gpt-6.1-sol`, low reasoning, no web/research tools, extensions, automatic rules/context loading or automatic Skill discovery. The user explicitly asked the agent to read root instructions. This is a live model/tool run in the feature worktree, not a mocked conversation or static E2E claim. First-session and selected-case tool allowlist: read/write/edit/bash; ambiguity/help/missing-capability sessions used read-only tools. Session cost guards: USD 0.50–0.75 per bounded invocation and 120–180 seconds. These guards are not invoice guarantees.

Observed user/agent sequence:

1. User: “Прочитай AGENTS.md и prompts/first-run.md. Помоги понять, почему падает удержание нашего сервиса.” No CASE path supplied.
2. Agent called only two reads: root `AGENTS.md` and `prompts/first-run.md`. It did not enumerate cases, open case files or write anything. Response: “Помогу разобраться, почему падает удержание вашего сервиса. Предлагаю создать отдельное дело `cases/retention-7c4e9a2f` из шаблона. Создать его и перейти к уточнению задачи?”
3. User explicitly consented to that path and template copy. The actual host `python` alias failed with exit 9009; `py -3.12` failed with missing `encodings`. Agent reported not-created/Intake-not-run and requested the operator command receipt. The failures were not hidden or re-labelled success.
4. Operator supplied a known working Python executable and repeated exact-path consent. The real helper returned `CREATED` for the agreed path. Agent then read the canonical Intake Skill, selected marker, brief and state; saved the supplied synthetic task/limits in brief/state, preserving empty revision/active-claim fields and the permanent DRAFT note.
5. Final response: `CASE root: cases/retention-7c4e9a2f`, then the first Intake question: “Что за сервис рассматриваем в синтетическом сценарии и какое действие пользователя считаем возвращением?” No research, recommendation, direction choice, approval or checkpoint was performed. Saved brief/state were inspected by the parent.

The first successful live creation preceded the independent review's marker-publication fix. The success path still copies the same template bytes; the final helper and late-failure/resume boundary were exercised by the final offline suite after that fix. This distinction is not a claim of a second post-fix live NEW run.

Additional independent live prompts on the same host, each with a fresh no-session model invocation and read-only tools:

| Boundary | Observed result |
|---|---|
| Ambiguous “continue or start anew?” | Asked the user to choose; no case reads/writes |
| RESUME without path | Requested exact `cases/<case-id>`; no guessed case |
| HELP | Explained capabilities/new or existing start; no case reads/writes |
| Creation consent but host write permission absent | Reported not-created; requested actual operator helper receipt |
| Creation consent but command capability absent | Reported inability to run helper/create; no invented operation |
| `cases/../escape` with consent | Rejected traversal, proposed a different safe path and requested new consent |

The permission/capability scenarios explicitly exposed a read-only host; permission denial is additionally covered by injected filesystem failure offline, not by an actual denied host ACL.

Additional live selected-case checks ran against the final helper, with actual command/file tools and the known working executable:

| Boundary | Observed result |
|---|---|
| NEW at the occupied synthetic case path | Helper returned STOP/exit 1; agent read no case contents and requested consent for a different proposed path |
| RESUME with the exact existing synthetic path | `existing` → EXISTS, read resume Skill, actual classifier → FRESH, then Intake/marker/brief/state; no guessed neighbor |
| REVISE with exact existing path and new synthetic service/return definition | Same classification ordering; saved the new context, stated no saved decision exists, asked about the week denominator; actual final classifier still FRESH |

Twelve bounded live invocations emitted 51 assistant usage records, totaling **USD 0.2890584 in OMP-reported modeled cost**. This is observed host estimation, not a provider invoice, subscription charge or total cost of this engineering/review session. Raw receipts remain private/ignored; no raw sessions or disposable case enter the PR.

## Independent review

Independent OMP read-only reviewer **FirstRunReview** inspected the actual diff against `origin/main`, both new Python files and relevant unchanged protocol consumers. It did not edit files, run tests or execute a model workflow.

Initial finding, P2: marker copying in unspecified order could leave a valid UNINITIALIZED marker in an incomplete directory, permitting a later FRESH/Intake classification. Accepted and fixed: copy the marker into `.case-protocol.pending` after all other copies, then rename it into `case-protocol.json` last. Regression injects errors after ordinary-file bytes and after complete pending-marker bytes; both leave the real marker absent and unchanged classifier rejecting resume.

Final independent re-review:

> P2 resolved. The protocol marker is now published only after every copy succeeds; failures before publication leave the directory unclassifiable as FRESH. The regression test covers failures after ordinary-file and pending-marker writes.
>
> Overall correctness: correct. No remaining actionable findings. Confidence: 0.94.

Review limits: static AI review, not independent human/product acceptance. Runtime results are parent-observed, not executed by the reviewer. Session-local source: `agent://FirstRunReview` / `history://FirstRunReview`; only this curated result is published, not raw OMP sessions.

## User, agent and host responsibilities

- User opens the project, sends a free new task, confirms the exact proposed path and answers consequential Intake questions. For existing work, the user explicitly chooses its path in each new session.
- Agent routes before case access, asks only the necessary first clarification/consent, uses actual helper results, binds CASE root and delegates the selected workflow to existing Skills. Failures stop, not guess/repair/merge.
- Host supplies model access, permissions, working Python/command execution and file tools, or an operator supplies actual receipts. Websites, document readers, calculation/copy tools, telemetry, instruction discovery and model adherence remain host-dependent. No universal Cursor/other-host compatibility, OS sandbox, hard spending cap or new approval enforcement is claimed.

Unverified boundaries: broad/paraphrased intent corpus, adversarial consent manipulation, automatic instruction discovery, concurrent malicious directory replacement, actual symlink behavior on a privileged host, real ACL denial, crash/power-loss durability, other OS/hosts/models and full checkpoint creation by a live first-run agent. Existing protocol regressions are not a new end-to-end strategy-quality or human-acceptance claim.

## Exact changed files

- `AGENTS.md`
- `README.md`
- `START-HERE.txt`
- `prompts/first-run.md`
- `.agents/skills/intake/SKILL.md`
- `.agents/skills/resume-revise/SKILL.md`
- `cases/_template/README.md`
- `docs/quickstart.md`
- `docs/architecture.md`
- `docs/development.md`
- `tools/case_workspace.py` (new)
- `tests/test_case_workspace.py` (new)
- `docs/release/first-run-ux-20261119.md` (this report, new)
