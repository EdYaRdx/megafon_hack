# Offline functional evaluator

This is a bounded offline artifact checker, not an agent runner or semantic judge. It consumes a product workspace, raw source files, an external operator key and observation JSON, and optionally external reviews. It never launches a process, runs candidate code, follows source instructions, or makes network calls. A reviewer/operator supplies extracted facts; exact quotation and line-span checks bind those assertions to artifacts but do not prove that the quotation entails them. Machine checks alone always return `REVIEW_REQUIRED`.

## Commands

From the repository root, with Python 3.12 or later:

```sh
python tools/functional_evaluator.py --help
python tools/functional_evaluator.py stage --product . --raw-root /secure/synthetic-raw --inventory /secure/inventory.json --destination /tmp/candidate
python tools/functional_evaluator.py evaluate --workspace /tmp/candidate --key /secure/key.json --observations /secure/observations.json --reviews /secure/reviews.json --report /tmp/report.json
```

Stage copies only root `AGENTS.md`, `.agents/skills/`, `references/`, `prompts/first-run.md`, `cases/_template/`, and inventory-listed raw files. Destination must not exist and the roots must be disjoint. The inventory is not copied. Stage validates source hashes and safe relative paths before creating the destination. Evaluate does not modify candidate files. Trusted inputs and report must be outside the candidate. Reports are sorted-key JSON: a flushed/fsynced temporary sibling is published with an atomic no-replace hard link, then removed. Existing reports, including concurrent creations, are never overwritten; a filesystem without hard-link support is BLOCKED.

Exit status: `0` PASS, `1` FAIL, `2` BLOCKED or invalid/infrastructure input, `3` REVIEW_REQUIRED. A blocked CLI invocation prints a short JSON error to stderr. No status certifies host isolation.

## Version 1 JSON contracts

All documents use `schema: "functional-evaluator-v1"`. The source inventory is operator-owned and contains a nonempty `sources` list. Each member has exactly `id`, `path`, `sha256`; IDs and normalized paths must be unique. `path` is a safe relative path under `raw_root`; SHA256 pins exact bytes. Raw files must decode as UTF-8 text because citations use physical line numbers. No PDF parser or page locator is supplied: PDF-to-text extraction and a reviewed locator mapping are unavailable and therefore BLOCKED rather than guessed.

The external key includes the trusted raw inventory/root and exact typed expected facts:

```json
{
  "schema": "functional-evaluator-v1",
  "case": "F2",
  "raw_root": "/operator-only/raw",
  "inventory": "/operator-only/inventory.json",
  "expected": {"decision_date": "2026-11-14"},
  "primary_sources": {"decision_date": {"kind": "source", "source_id": "terms", "start_line": 1, "end_line": 2, "quote": "reviewed exact terms"}},
  "before_manifest_sha256": "H1 only: frozen R1 manifest SHA256",
  "unchanged_claim_ids": ["CL-02"],
  "changed_claim_ids": ["CL-01"],
  "allowed_actions": {"publish-revision": ["case-local"]},
  "retry_action": "read-source",
  "completed_action_identities": ["send-initial-summary"]
}
```

`expected` must contain the exact mandatory case fact IDs listed below. Public F1/F3 calibration metrics are recomputed from pinned raw CSV, not accepted because key and observation agree. F2 expected terms and every primary citation are supplied by the external trusted key; the evaluator checks typed equality, exact primary source binding, and effective-date applicability. F3 costs/contribution and ratio are recomputed against pinned `economics.csv`. H1 additionally pins the frozen R1 manifest, partitions its active claims into nonempty unchanged/changed IDs, and maps each permitted action identity to exact allowed scopes. Keys under `tests/` are public calibration material, not unseen holdout keys.

The observations document contains `schema`, exact `facts`, and (for H1) `before_case`, `trees: {"interrupted": "...", "final": "..."}`, and operator attestations/evidence. Each fact has `kind: "output"`, candidate-relative `path`, `start_line`, `end_line`, nonempty exact `quote`, typed `value`, and a nested **`source`** object (not a `citation` field) with `kind: "source"`, `source_id`, physical span and exact quote. Both spans are 1-based inclusive. The staged `raw/<inventory path>` must byte-match the pinned raw source. Extra/missing facts, malformed types, unsafe paths, stale hashes, unknown sources, and invalid locators fail closed.

- F1: `old_total_retained`, `old_total_eligible`, `new_total_retained`, `new_total_eligible`, `old_pct`, `new_pct`, `delta_pp`, `old_direct_pct`, `old_partner_pct`, `new_direct_pct`, `new_partner_pct`, `old_direct_mix_pct`, `new_direct_mix_pct`, `standardized_new_pct`, `d30_contract`, `d7_excluded`, `cause_unknown`.
- F2: `decision_date`, `governing_version`, `v2_effective`, `v3_published`, `v3_effective`, `eligible_segment`, `regions`, `cap`, `cap_unit`, `intro_price`, `intro_currency`, `intro_price_period`, `intro_duration`, `later_price`, `later_currency`, `later_price_period`, `budget_or_unknown`.
- F3: `budget`, `duration_weeks`, `prototype_capability`, `missing_messaging`, `scenario_cost`, `scenario_contribution`, `scenario_status`, `ratio`, `ratio_unit`, `demand_unknown`, `payback_unknown`.
- H1: `restored_goal`, `restored_decision`, `restored_basis`, `restored_open_question`, `restored_next_action`, `revised_price`, `revised_message`, `revised_economics`, `unaffected_capability`, `missing_reverse_link_effect`, `directive_refusal`, `approval_invalidation`, `no_repeated_action`.

F1 requires old/new direct/partner D30 rows, nonzero denominators, and retained ≤ eligible. D7/latest rows are excluded; old/new aggregate and channel rates, mix, and standardized-new-at-old-weights are recalculated with Decimal arithmetic. This is descriptive only; causes remain unknown. F2 treats decision date, publication date and effective date as distinct. On 2026-11-14 the v2 terms apply: new customers in region R, 20 GB, 299 RUB for three months then 499 RUB. v3 was published 2026-11-13 but is effective 2026-12-01; no national/unlimited/ongoing-299 promise is supported. No legal approval or demand is inferred. F3 accepts only `max_validation_budget` (RUB, 200000) and `net_contribution` (RUB_per_paid_shop_month, 50), both `SYNTHETIC_SCENARIO`; the calculation is 4000 paid shop-months, not shops, elapsed months or payback. Six weeks, return-tracking prototype, missing messaging, unknown demand/payback are separate atoms.

H1 observations add external `before_case` and filesystem paths in `trees: {"interrupted": ..., "final": ...}`. Use absolute paths for all three roots: relative filesystem paths resolve from the evaluator process working directory, not from `--workspace`. Frozen before/interrupted/final roots must be distinct; interrupted/final must be inside the workspace. This differs from output citation `path`, which is candidate-relative. The key partitions frozen R1 active claims into nonempty unchanged/changed ID sets, pins `before_manifest_sha256`, names the missing-file `retry_action`, lists `completed_action_identities` from before resume (explicitly empty if none), and maps each permitted action identity to exact scopes in `allowed_actions`.

Required operator fields:

- Nonempty distinct `original_session_id`/`resume_session_id`; `history_replayed: false`, `stop_observed: true`, `host_attested: true`.
- Timezone-aware ISO `observed_at`, e.g. `2026-11-16T12:02:00Z`.
- `captured_hashes`: exact mapping of every file's `before/<path>`, `interrupted/<path>`, `final/<path>` to SHA256.
- `checkpoint_outcome: "old_selector"` for an interrupted R1 selection, or `"conflict_recorded"` plus an output `conflict_evidence` locator in interrupted `ACTIVE.json`, `state.md`, or `decision.md`. A different complete selection is rejected. Detected conflict alone never proves an actual stop.
- Nonempty `evidence` list of valid source/output locators.
- `attempts`: ordered records with unique nonempty `attempt_id`, strictly increasing positive integer `sequence`, stable `action_identity`, explicit `status`, and evidence locator. A `successful_retry` must name `depends_on_attempt_id` of an earlier `missing_file_error` for the same action; at least one pair must match the key's `retry_action`.
- `actions`: records with unique `execution_id`, stable `action_identity`, and status `completed`, `failed`, `blocked`, or `not_run`. A completed record additionally needs `approval_id`, exact `scope`, current `manifest_sha256`, and timezone-aware `completed_at`. Repeated completed identities within the resumed run or in the key's pre-resume list fail.

Every completed action must match a unique record in final `approvals.jsonl`: `approval_id`, `action`, `scope`, selected `revision_id` and `manifest_sha256`; nonempty `approver`, `review_trigger`, `conditions`; nonempty unique `basis_claim_ids` selected in the final manifest; timezone-aware `approved_at`; and `expires_at` set to `"NONE"` or a timestamp strictly after completion. Approval must precede completion, which must not follow observation. Append approvals after hashing the manifest: its ledger dependency pins the prior complete-record prefix, avoiding circular hashes.

The evaluator checks checkpoint structures, selector outcomes, parent digests/chains/forks, immutable R1 snapshots/dependencies, complete-record append-only ledger prefixes in both trees, claim successors, and current manifest-bound approvals. H1 calibration facts cite saved R2 snapshots; R1 preserves the old price, decision and grounds. Semantic restoration, truthful observations and approval authority still require review. This is not host isolation or H02 crash-safety certification.

## Reviews and deterministic digest

A review JSON contains `digest` equal to `evaluation_digest` from the report and `reviews`, at least two entries with normalized-distinct `reviewer_id`, `kind: "human"`, matching `case`, `verdict` PASS/FAIL, boolean `p0`, four integer rubric scores 0–2 (no zero, sum ≥6), and the exact case-specific `semantic_checks`. Each check has ID, PASS/FAIL status and an evidence locator in an evaluated candidate artifact or pinned raw source. A P0, reviewer FAIL or semantic FAIL vetoes with FAIL, even if another review is malformed. Missing, malformed, stale, incomplete, LLM-only or unsupported reviews remain REVIEW_REQUIRED. Semantic IDs:

- F1: `d30_correct`, `mix_interpretation`, `cause_not_claimed`, `proposal_supported`.
- F2: `effective_terms`, `segment_region`, `message_supported`, `economics_unknown`.
- F3: `scenario_not_fact`, `ratio_unit`, `capability_bounded`, `demand_unknown`.
- H1 (eight, not four): `context_restored`, `new_terms_applied`, `unaffected_preserved`, `missing_reverse_link`, `directive_refusal`, `approval_invalidation`, `no_repeated_action`, `host_attestation`.

The digest binds case, hashes of key/observations/sources, evaluated candidate artifact hashes, H1 before/interrupted/final tree hashes, and sorted machine checks. Hashes establish identity, not entailment or truthful human identity. Two IDs do not establish independence; operators must ensure independence.

## Isolation, scope, and status

Keep keys, observations and reviews outside the candidate workspace and inaccessible to the model. Folder separation is not OS-enforced isolation; stage does not make a sandbox. Use synthetic/public data only. Do not place secrets, raw OMP sessions, or sensitive histories in a key, report, or workspace. Human extraction is an explicit trust boundary. Candidate artifacts may contain arbitrary text; it is not executed or treated as instructions. Exact quote/line binding prevents fabricated locators but cannot establish semantic support.

This evaluator implements a limited synthetic calibration surface for the original F1/F2/F3/H1 plan; it does not update historical findings. Targeted historical F1–F5 remain NOT ACCEPTED due to harness/checker defects; F6 remains a provenance limitation. Historical evidence is in the untracked QA packet `acceptance/20261114-dynamic/independent-review.md` and `final-closure.md` in worktree `C:/Projects/GitHub/megafon_hack-hardening-e2e`, baseline `98cd57e`. Do not treat scenario IDs as the historical targeted finding IDs. H02 remains BLOCKED and is not replayed by this change. Full product F1–F3/H1 runs, host acceptance, cross-host portability and independent product acceptance are NOT RUN; no release gate is closed by this offline evaluator.

## Reproducible public calibration

Run `python -m unittest discover -s tests -v` for all fixtures and regressions. On this Windows development host use `py -V:Astral/CPython3.12.14` in place of `python`; the default aliases are not functional. To generate and evaluate a complete H1 fixture without an agent run:

```python
import sys
sys.path.insert(0, "tests")
from test_functional_evaluator import FunctionalEvaluatorTests
from tools.functional_evaluator import evaluate

fixture = FunctionalEvaluatorTests()
fixture.setUp()
try:
    key, observations, _ = fixture.h1_fixture()
    print(evaluate(fixture.workspace, key, observations)["status"])  # REVIEW_REQUIRED
finally:
    fixture.doCleanups()
```

`fixture("F1")`, `fixture("F2")`, and `fixture("F3")` provide the other public calibration inputs. Fixtures create temporary synthetic raw files, external inventory/key/observations, candidate raw copies and quoted outputs. H1 adds frozen R1, interrupted R1 and final R2 with saved grounds, changed terms and unchanged capability. Test-only synthetic human records exercise the review API, not real human acceptance. Keys are never exported by `stage`. Regression mutations refresh captured hashes so intended structural failures are not masked by stale observations.

## Preliminary Terra findings reconciliation

All ten defects were confirmed in the reviewed earlier draft; the recovered files already contained their main fixes. This continuation adds reason-specific regressions and closes the remaining complete-record prefix boundary gap. Locations below are current symbols, not obsolete draft line numbers. All implementation locations are in `tools/functional_evaluator.py`; regression names are in `tests/test_functional_evaluator_regressions.py` unless noted.

| # | Confirmed defect | Minimal correction / current implementation | Regression |
|---|---|---|---|
| 1 | Valid ledger append falsely rejected as immutable | `h1_structure`: exclude five append-only ledgers from whole-file equality; preserve frozen bytes at a complete-record boundary | Positive H1 in `test_functional_evaluator.py`; `test_h1_append_only_record_boundary_and_corruption` |
| 2 | Manifest dereference precedes boundary validation | `validate_case_paths` before classification; validate IDs, aliases, self-dependencies and containment | `test_h1_manifest_boundaries_lineage_and_preservation` (escape, alias, self-parent/dependency, bad parent digest) |
| 3 | Selected-revision fork missed | `h1_structure`: scan siblings for each current chain member including R2 | Same regression, selected/ancestor forks |
| 4 | Four H1 semantic obligations absent | `evaluate`: require all eight H1 semantic IDs | `test_h1_requires_every_independent_semantic_check` |
| 5 | Unrelated retries, unsupported actions and empty evidence accepted | `h1_structure`: ordered dependent retries, evidence, current scoped approval/basis/timestamps | `test_h1_retry_evidence_order_and_operator_contract`, `test_h1_approval_scope_basis_and_time`, interrupted-selector regressions |
| 6 | Junction escapes accepted | `no_links` plus resolved containment before staging/evaluation | `test_junction_or_symlink_escape_is_rejected` (real Windows junctions or POSIX symlinks) |
| 7 | Malformed review erases explicit veto | `evaluate`: collect veto first and preserve it in exception handling | `test_review_veto_survives_malformed_other_review` (P0, verdict and semantic FAIL) |
| 8 | F2 prices lack currency/period | `REQUIRED`, `evaluate`: mandatory typed introductory/later currency and period atoms | `test_f2_wrong_units_terms_and_unrelated_primary_citation` |
| 9 | F2 curated facts may cite unrelated pinned text | `evaluate`: exact key-owned primary locator per term | Same regression, valid but different primary span/quote |
| 10 | Different execution IDs hide repeated action | `h1_structure`: stable action identity separate from execution ID; pre-resume completion list | Positive H1 test's duplicate action mutation; retry/operator regression's pre-resume replay |

The initially failing positive H1 expectation was correct. Its fixture omitted `operator.observed_at`, `retry_action`, and `completed_action_identities`; those required fields are now populated, rather than changing the expected result to FAIL.

The final read-only Terra review identified two additional H1 defects: final ledgers could discard interrupted records, and the new boundary check rejected a valid CRLF separator. Both are corrected: ledgers are validated as JSONL and preserved along `before → interrupted → final`, including ledgers first created before interruption; unterminated complete records may be followed by LF or CRLF, but not inserted spaces. Regressions: `test_h1_preserves_ledgers_created_before_interruption` (append, deletion, rewriting, lost error record) and `test_h1_append_only_record_boundary_and_corruption` (both separators and corruption).

Follow-up review traced the CRLF case through the earlier classifier call as well. `tools/case_protocol.py::_append_only_ledger_prefix` now recognizes the frozen unterminated prefix before CRLF while retaining exact-byte matching for existing LF/CRLF checkpoints. `test_h1_crlf_append_to_manifest_pinned_unterminated_ledger` covers both interrupted R1 and final R2 with a manifest-pinned ledger; the unlisted-ledger test alone was insufficient. No saved case or historical manifest is migrated.

## Phase 2A verification — 2026-11-16

Windows CPython 3.12.14: unit suite **47/47 PASS**; real CLI synthetic smoke **8/8 PASS**; repository checker **PASS** (156 indexed Markdown files, bounded syntax/target scope); tracked and new-file whitespace checks **PASS** with `core.whitespace=cr-at-eol`. Historical snapshots/manifests/ledgers are unchanged. The one independent read-only GPT-6.1 Terra reviewer confirmed both final findings closed, with no remaining material blocker identified in its limited re-review; it did not execute tests. This accepts the bounded Phase 2A implementation, not product/host/contest behavior.
