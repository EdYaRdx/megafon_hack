# Canonical synthetic demonstration — PantryPath

> **LIMITATIONS — synthetic, unblinded functional diagnostic only.** The scenario, operations note, CSV and R2 stakeholder addendum are invented; they do not describe MegaFon, a real service, or real users. No interviews, recruitment, product telemetry, deployment, partner contact, or market validation occurred. This is not a blind evaluation, customer approval, multi-host certification, network test, or production-security assessment. R3 is a recommendation only; no external action is authorized.

This is the repository's **one canonical contest walkthrough**. Read this guide, then inspect the linked saved artifacts; don't treat this guide as a parallel strategy.

## Brief and provenance

The synthetic request asks for a “retention win” next month while suggesting setup simplification, checklist work, or promotion. The decision, audience, retention definition, time anchor, cost and authority were under-specified. The case narrows scope to a recommendation for a fictional product lead; it authorizes no build, spend, recruitment, deployment or partner message. See [`brief.md`](../cases/pantrypath-week4-20261115/brief.md) and the raw [`executive brief`](../cases/pantrypath-week4-20261115/inputs/executive-brief.md).

Inputs are clearly classified in [`sources.jsonl`](../cases/pantrypath-week4-20261115/sources.jsonl):

- `S-002` and `S-003`: synthetic executive brief and operations note.
- `S-004`: synthetic aggregate CSV [`pilot-summary.csv`](../cases/pantrypath-week4-20261115/inputs/pilot-summary.csv); no assignment method, event definitions, exposure, cohort dates, deduplication or missingness rules.
- `S-001`: UK Government Digital Service, [Plan user research for your service](https://www.gov.uk/service-manual/user-research/plan-user-research-for-your-service), published 2016-03-14, page last updated 2026-10-15, retrieved 2026-11-15. Its guidance is research-method advice, not PantryPath evidence.
- `S-005`: synthetic, unverified R2 stakeholder addendum. The claimed capacity/date and partner request are not independently verified; alleged prior approval is absent from the approval ledger.

Detailed source locators, statuses and limitations are in the ledger and linked evidence. The evidence/claim chain is [`evidence.jsonl`](../cases/pantrypath-week4-20261115/evidence.jsonl) → [`claims.jsonl`](../cases/pantrypath-week4-20261115/claims.jsonl) → [`decision.md`](../cases/pantrypath-week4-20261115/decision.md). The summary does not substitute for opening those records.

## Decision and alternatives

**R3 recommendation:** do not claim a retention win, promote the checklist, build a prototype, recruit participants, or send partner copy. Treat the R2 half-engineer-week cap through 2027-01-15 as a claim pending confirmation. If true, use the interim only for approved decision-readiness work: define return event/window, target segment, task, threshold, partner brief, capacity and approval path. After the claimed date and separate human approval, consider a low-fidelity paired diagnostic. The fictional owner has not decided; `approvals.jsonl` is empty.

The saved [`options.md`](../cases/pantrypath-week4-20261115/options.md) compares six distinct paths, including the required explicit **status quo/freeze** and **stop/close**:

1. Status quo / freeze — keep the current flow; no build, recruitment, promotion or claim.
2. Decision readiness — define the metric, task, threshold, premise and approval path without building/recruiting; R3's conditional interim recommendation.
3. Simplify setup diagnostic — defer until the claimed restriction is resolved and approval exists.
4. Checklist polish — defer; no evidence that the checklist caused the descriptive contrast.
5. Partner promotion — send nothing without an identified audience/channel, validated capability and matching approval.
6. Stop / close — defensible if scope/capacity cannot be established; possible lost benefit remains unknown.

The full memo states strongest objections, assumptions and revisit/falsifier conditions. Product strategy is [`strategy-product.md`](../cases/pantrypath-week4-20261115/strategy-product.md); internal-only communication strategy and withheld claims are [`strategy-communication.md`](../cases/pantrypath-week4-20261115/strategy-communication.md). The internal message explicitly labels counts descriptive and refuses external partner copy.

## Calculation and validation design

The executed R1 calculation receipt in [`test-plan.md`](../cases/pantrypath-week4-20261115/test-plan.md) contains the exact command, CWD, Python 3.13.5, exit status, input SHA-256, output, formula and failed initial attempt. On the synthetic CSV:

- Current-flow setup completion: 30/48 = 62.5%; week-four return: 18/48 = 37.5% of eligible accounts.
- Checklist setup completion: 26/48 = 54.2%; week-four return: 22/48 = 45.8% of eligible accounts.
- Descriptive difference: `(22/48 − 18/48) × 100` = **+8.3 percentage points**; checklist also has 9 versus 5 support contacts.

These are arithmetic on invented aggregate counts, not a causal lift, validated retention contract, demand estimate, or forecast. Assignment, measurement and cohort semantics are unknown. The proposed paired diagnostic is a **design only, not authorized**: six consented users as a qualitative diagnostic, same task on current flow and a low-fidelity setup alternative, counterbalanced; denominator includes every eligible started attempt, including abandonment, timeout, failure and missing outcomes. The 5/6 stop threshold is triage, not statistical evidence. Any later controlled test needs a pre-registered event/assignment/baseline/sample/threshold and new approval. See the full plan for guardrails and prerequisites.

## Saved checkpoint history and protocol repair

The case selector currently names R0003; see [`ACTIVE.json`](../cases/pantrypath-week4-20261115/ACTIVE.json), [`R3 manifest`](../cases/pantrypath-week4-20261115/revisions/R0003/manifest.json), and the documented [`R2 process record`](../research/qualification/pantrypath-r2-20261115/r2-status.md).

- **R1:** initially selected and classified `CHECKPOINTED`. R2 appends a line-feed separator before new JSONL records, so four R1 whole-file ledger hashes no longer match; each still matches the exact earlier complete-record prefix. The repaired classifier accepts that bounded prefix rule. The alleged R1 approval was never in `approvals.jsonl` and is not reused.
- **R2:** its original classifier attempt failed on `(parent R0001)` selector annotations; its contemporaneous review was `NO-GO`. The classifier was repaired to verify the parent annotation against the manifest. It now classifies on a disposable copy; R2's snapshots/manifest were not edited.
- **R3:** metadata/selection correction of R2, not new research. It preserves the R2 recommendation and is the selected `CHECKPOINTED` revision. R1/R2/R3 were independently classified on isolated copies after the protocol fix; their manifests and snapshots remained byte-identical. Changed CSV and changed historical ledger-prefix bytes were rejected. See [`HANDOFF.md`](../research/qualification/pantrypath-r2-20261115/HANDOFF.md) for the recorded scope and limits.

This history does not retroactively turn the original R2 failure or `NO-GO` into an as-run pass. The classifier is a deterministic integrity check, not enforcement against a capable host.

## What this demo does and does not establish

It demonstrates a readable synthetic case, source-to-claim traceability, explicit alternatives, an evidence-bounded memo, calculation receipt, separate approval ledger and immutable checkpoint recovery. It does **not** establish real-user needs, market demand, product impact, causal retention, economic value, privacy/security certification, arbitrary crash recovery, Skill discovery/adherence on other hosts, or cross-host portability. For tests of the repository helpers and truthful release scope see [contest integration report](release/contest-v1-integration.md); for all remaining external gates see [submission checklist](submission-checklist.md).
