# PowerShell discovery and operator Intake recovery

## Scope and baseline

PR [#23](https://github.com/EdYaRdx/megafon_hack/pull/23) was MERGED at `2026-11-19T20:59:12Z`. Remote main was `b9157f62578ce4ccf14f8e486bf532bbab537867`. This follow-up uses one separate clean clone and branch `fix/powershell-intake-recovery`. The original checkout, `megafon_hack-ux-test`, historical cases and SlotPilot were not edited. Diagnosis of the test checkout was read-only.

This is an instruction-level bugfix, not a launcher or architecture change. `tools/find_python.ps1`, `tools/case_workspace.py`, `tools/case_protocol.py`, `tools/resume_context.py`, the resume Skill, templates, checkpoint/approval formats and historical revisions are unchanged.

## Root cause: established facts versus unknown trigger

### Confirmed incident (user report)

- Codex tried `tools/find_python.ps1` and received `PSSecurityException` / `UnauthorizedAccess`.
- The user reports Windows PowerShell 5.1, CurrentUser `RemoteSigned`, a Store Python alias, broken launcher-selected Python 3.12.10 (`encodings` import failure), and working installed uv CPython 3.12.14.
- An operator invoked the normal `case_workspace.py create` with working Python for the previously agreed `cases/subscription-checkout-c0d2d587`; the helper returned `CREATED`.
- After that receipt, Codex retried the blocked discovery script and did not continue Intake.

The original full localized exception, exception details/inner error, outer Codex command line, PowerShell launch flags, effective policies/language mode and host permission decisions for that session were not supplied or available in the inspected repository material. The incident's exact OS/host policy trigger therefore remains **UNKNOWN**. The reported command and error class are established; reconstructing additional flags or declaring RemoteSigned the cause would be unsupported.

### Read-only observations in the current diagnostic session

`powershell.exe -NoProfile -Command ...` reported:

| Check | Observation |
|---|---|
| Windows PowerShell | Desktop 5.1.26100.9818 |
| Effective / CurrentUser execution policy | RemoteSigned / RemoteSigned |
| MachinePolicy, UserPolicy, Process, LocalMachine | Undefined |
| Language mode | FullLanguage |
| Test checkout script attributes | Archive |
| Alternate streams on test script | Only `:$DATA`; no current `Zone.Identifier` |
| Authenticode | NotSigned |
| Script provenance | Last script commit `eecdce305a4f535d1df7fa0c2e3882fad4aa52d3`, PR #23 |
| SHA-256 in test checkout and clean main clone | `050AFAE383549E81837490DD6D4D2CCBDC740FC1603885094F8576179C5DD26C` in both |
| Installed offline uv lookup / real import probe | CPython 3.12.14, imports encodings/json/pathlib succeed |

Commands inspected file metadata/streams/signature/hash, policy scopes, language mode, native command resolution and Git provenance. No policy, file blocking attribute, registry, PATH, alias configuration or user case was changed. Today's absence of MOTW does not establish its absence during the incident; today's interactive diagnostic session is not the original Codex session.

Microsoft's [PowerShell 5.1 execution-policy documentation](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies?view=powershell-5.1), sections **PowerShell execution policies**, **Execution policy scope and precedence**, **Set a different policy for one session** and **Manage signed and unsigned scripts** (publisher Microsoft; page date 2026-08-31), distinguishes RemoteSigned local/downloaded unsigned scripts, higher-precedence scopes and session-only policy. Possible incident explanations include a different effective Process/Group Policy, then-present MOTW, or a host permission restriction. These are **hypotheses, not findings**. No system-setting change or rerun of the original failure was used to claim a diagnosis.

### Confirmed product causes

1. **Discovery was coupled to script-file execution.** [Baseline first-run](https://github.com/EdYaRdx/megafon_hack/blob/b9157f62578ce4ccf14f8e486bf532bbab537867/prompts/first-run.md#L16-L32) required the PS1 helper on Windows and sent script-policy failures straight to operator receipts. It did not distinguish a blocked `.ps1` from separately permitted native interpreter discovery/probing. A healthy Python could remain unused.
2. **No explicit verified operator-created-case handoff.** [Baseline NEW/RESUME routing](https://github.com/EdYaRdx/megafon_hack/blob/b9157f62578ce4ccf14f8e486bf532bbab537867/prompts/first-run.md#L34-L48) required runtime discovery, treated occupied NEW paths as STOP, and lacked a dedicated recovery route for the already agreed operator-created case. That instruction gap allowed repeated discovery instead of read-only verification and Intake continuation. The model's internal reasoning is not observable.

## Fix and preserved boundaries

The canonical procedure remains [first-run](../../prompts/first-run.md):

- Try the normal PS1 helper when allowed. If only script-file execution is blocked and the host permits individual commands/native executables, use bounded native command/file discovery and the documented import/version/direct-executable probe. PATH, project environment, installed launcher paths, offline/no-download uv and operator-supplied paths remain bounded sources. Broken candidates and Store aliases are rejected. Decode UTF-8 discovery stdout using the documented process-local console encoding setting; retain the verified executable for the session.
- Never execute blocked script contents through eval/dot-sourcing/another loader; never bypass policy, unblock the file, install/download or change machine configuration. Separate host/native prohibition means STOP with actual errors, not an alternate route around the same prohibition.
- After operator assistance, verify one exact agreed/explicitly selected directory, its marker, and unchanged classifier output using a permitted verified interpreter or verifiable actual operator receipt. Do not rerun create or require a blocked discovery helper. Only FRESH/UNINITIALIZED permits Intake. Missing/corrupt identity or incomplete classification stops.
- Narrative success, pasted JSON, a different checkout/path or an old receipt are not independent proof. Receipt provenance and exact operation/cwd/case/exit/stdout/stderr must be checkable; if no runtime or verifiable receipt exists, stop. A foreign/ambiguous path requires explicit selection, not automatic adoption.
- FRESH/CREATED/EXISTS are not CHECKPOINTED or approval. Existing selector, immutable manifest/hash/claim, candidate gate and action-specific approval rules are unchanged. Read-only recovery grants no write permission.

## Regression verification

Executed with the offline-discovered CPython 3.12.14, from the feature clone:

```text
$Python -m unittest discover -s tests -v
$Python -m unittest discover -s tests -p test_runtime_fallback.py -v
$Python tools/check_repository.py
$Python tools/case_protocol.py classify cases/pantrypath-week4-20261115
```

`$Python` above denotes the actual verified executable passed as an argument, not a PATH alias.

| Check | Observed result and scope |
|---|---|
| Initial complete Python suite | 119 tests; one new fixture failure, five symlink-privilege skips. All existing suites, including Resume, immutable/checkpoint and evaluator regressions, passed. |
| Fixture corrections | PS5.1 `@(ConvertFrom-Json)` nested the multi-candidate input, giving one attempt instead of two. Direct assignment fixed it without weakening the assertion; the original two fallback tests then passed. A later Unicode test initially failed because PS5.1 stripped a nested native string quote; its locator now uses Python's default UTF-8 `encode()`. |
| Final targeted fallback suite | 3 tests, OK: real PS1 security block with permitted native Python; both invalid native launches refused → STOP; real Unicode-path interpreter discovered through UTF-8 native stdout under an initially forced legacy decoder, then directly import-probed. |
| Other 117 tests in complete run | No failures; five WinError 1314 symlink skips. Includes actual Windows junction checks. Not rerun after the fallback fixture/instruction changes. |
| Repository checker | Final PASS: 159 Markdown files including this report; file targets and indexed case JSON/JSONL syntax only. |
| Canonical historical demo classifier | CHECKPOINTED, read-only. No case repair or rewriting. |

During the final report check, an invocation without UTF-8 decoding mangled uv's Unicode interpreter path and failed executable lookup. This is a separately observed fallback defect, **not proof of the original PSSecurityException cause**. The canonical instructions now set `[Console]::OutputEncoding` only in the current process before UTF-8 native discovery output. The final native offline uv lookup and repository check succeeded using that setting. The added Unicode regression uses a real temporary venv without pip/downloads; no installed environment was modified.

Coverage added in [runtime fallback tests](../../tests/test_runtime_fallback.py), [discovery tests](../../tests/test_find_python.py) and [workspace tests](../../tests/test_case_workspace.py): blocked PS1/permitted native Python; broken `py -3.12` followed by working offline uv; all offered native launches refused; operator-created agreed case classified read-only without create; missing/corrupt markers; incomplete artifacts/invalid selector; missing/multiple case paths; narrative checkpoint claims unable to replace protocol evidence. Existing [Resume tests](../../tests/test_resume_context.py) and [protocol tests](../../tests/test_case_protocol.py) exercise read-only restoration, immutable bytes, hashes, ancestry/forks and approval-related state preservation.

Tests execute the actual documented setup/probe, not a second implementation or source-text assertions. Restricted is applied only to a fresh test child Process to tighten policy; no persistent policy changes. Invalid-PE fixtures test native launch refusal, **not actual corporate ACL/AppLocker qualification**. API tests validate filesystem/classifier contracts, not human consent or receipt authenticity. The current coverage comprises the other 117 tests from the full run plus the final three fallback tests; no final single full-suite PASS is claimed after the last edits.

## One bounded live model/tool smoke

A real OMP task agent (`RecoveryLiveSmoke`, session model `openai-codex/gpt-6.1-sol`) ran against a disposable synthetic fixture outside the checkouts. The parent first obtained an actual normal-helper CREATED receipt for `cases/subscription-checkout-smoke`. The agent received the original product question, same-dialogue exact-path consent and operator assistance context. Host contract: read-only case access; native commands/inline PowerShell allowed; PS1 execution forbidden.

Every native/helper command ran in a fresh PowerShell child with process-only **Restricted**, not an execution-policy relaxation. The agent did not rerun discovery PS1 or create. Actual results:

1. Located installed uv and used `uv python find --no-project --no-config --no-python-downloads --offline '>=3.12'`.
2. Ran the documented import/version/direct executable probe successfully.
3. `case_workspace.py existing cases/subscription-checkout-smoke` → EXISTS.
4. Read only that case's marker → checkpoint-v1 / UNINITIALIZED.
5. Same verified interpreter ran `case_protocol.py classify ...` → FRESH.
6. Only afterward read that case's brief/state and asked about product/users, abandonment step, anonymized evidence, decision owner and deadline. It explicitly said saving was blocked by read-only permissions.

Parent comparison: **35 files before/after, all byte-identical; no added files**. No neighboring case access, create rerun, revision/selector/approval write or checkpoint claim occurred. The disposable fixture was removed after verification.

Smoke limitations: the first uv invocation was malformed by outer-shell expansion of PowerShell `$` variables and unintentionally reached the Store alias; it failed and was corrected with proper quoting before the valid lookup. Initial receipt absolute-path display had legacy console mojibake; independent root/marker/classifier checks, not that display, established state. The harness also loaded mandated `skill://intake` from the original checkout in addition to the fixture's canonical Skill; no original case was accessed or edited. Thus this is a bounded OMP recovery observation, **not clean Codex GPT-6 Luna Medium E2E certification**.

Two subsequent reasoning-only negative prompts, without further file/native operations, produced STOP/explicit-path clarification for a foreign receipt plus ambiguous case choice, and rejection of an unsupported “checkpoint ready” claim. These are limited agent decisions, not independent live foreign-existing-case filesystem tests or an adversarial receipt-authenticity guarantee.

## Independent review

Read-only reviewer `RuntimeRecoveryReview` inspected saved instructions/tests and relevant unchanged consumers. Verdict: **correct; no actionable findings** (reported confidence 0.88). It confirmed policy boundaries, exact-case recovery and unchanged classifier/approval/history contracts. It explicitly limited coverage: probe tests do not automate fallback discovery orchestration; filesystem tests do not establish assistant rejection of forged receipts/foreign-but-valid roots; child Restricted/invalid-PE tests do not establish real corporate policy behavior. These limits remain disclosed, not certified away.

Report review identified one P3 cross-reference to an as-yet unrecorded final check; it was replaced with the actual final 159-file PASS above. A narrow review of the later process-local UTF-8 instruction and Unicode regression found no actionable issues (reported confidence 0.92). The test's subsequent native quote-only fixture correction was verified by the final three-test run.

The reviewer ran no checks and made no edits. Parent-observed runtime results are separate from static AI review. Session-local audit locators: `agent://RuntimeRecoveryReview`, `history://RuntimeRecoveryReview`, `history://RecoveryLiveSmoke`; only this curated report, not raw session files, is published.

## Short Codex retest

In an updated disposable checkout, explicitly select the operator-created agreed `cases/<id>` and say: “Продолжи Intake этого дела. find_python.ps1 уже заблокирован; не повторяй его и не создавай дело заново. Проверь разрешённый runtime, точный каталог, маркер и штатную классификацию”. Supply the real operator command/cwd/stdout/stderr/exit receipt. Expected: authorized native probe → exact-root/marker checks → FRESH → contextual Intake question; no duplicate create/discovery, CHECKPOINTED or approval claim. If safe checks are unavailable, expected result is an explicit STOP.

## Changed files

- `AGENTS.md`
- `prompts/first-run.md`
- `.agents/skills/intake/SKILL.md`
- `docs/quickstart.md`
- `docs/development.md`
- `tests/test_find_python.py`
- `tests/test_runtime_fallback.py` (new)
- `tests/test_case_workspace.py`
- `docs/release/runtime-intake-recovery-20261120.md` (this report)
