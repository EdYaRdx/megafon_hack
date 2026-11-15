---
name: resume-revise
description: Продолжи дело из файлов и оцени влияние новых данных на старые выводы и решения.
---

# Resume and revise

## Classify the case before reading mutable roots

For a new case copied from `cases/_template/`, first read its root `case-protocol.json`. It must contain the supported `protocol_id: "checkpoint-v1"` and `checkpoint_state` of `UNINITIALIZED`, `CHECKPOINTING`, or `CHECKPOINTED`. Missing, malformed, unsupported, or ambiguous identity is `INCOMPLETE/CONFLICT` and means stop; missing `ACTIVE.json` never makes a case legacy.

- `UNINITIALIZED` with no `ACTIVE.json`, no revision manifest, and no files under `revisions/` is a fresh case. Intake/root working files may be populated; no saved decision checkpoint exists yet.
- Before writing any first-revision snapshot, change the marker to `CHECKPOINTING`. If the selector or any revision artifact then exists without one unique verified complete checkpoint, stop with `INCOMPLETE/CONFLICT`.
- A complete checkpoint is accepted only by the manifest/selector/hash/claim checks below. After the complete selector is verified, the marker may be set to `CHECKPOINTED`; a valid selector remains authoritative if a crash leaves the marker at `CHECKPOINTING`.
- A missing marker is eligible for legacy handling only for the exact pre-protocol case directories enumerated below, and only when no `ACTIVE.json` or revision manifest exists. Existing legacy snapshots may be read under their historical limitations; they are not certified complete. Any other missing-marker case, or any legacy-listed case with a selector/manifest but no valid new-protocol identity, is `INCOMPLETE/CONFLICT`. Do not infer legacy from timestamps, filenames, or absent files.

Bounded pre-protocol legacy directories: `fresh-start-demo`, `meal-planner-demo`, `offer-terms-demo`, `public-source-retention-smoke`, `resume-failure-demo`, `retention-demo`, `retention-f1-demo`, `service-launch-f3`, `source-injection-demo`, and `unseen-shelf-alerts-20261114`. This list identifies historical format only; it does not make an incomplete case complete or authorize edits to its history.

For a `checkpoint-v1` case, read root `ACTIVE.json` as the explicit active-revision selector. It must name a revision ID and SHA-256 matching that revision's `manifest.json`; verify manifest status and every listed file hash before using it. Root `state.md` and `decision.md` must name the same selected revision and active claims. Use only that revision's six snapshots (`options.md`, `decision.md`, `strategy-product.md`, `strategy-communication.md`, `test-plan.md`, `state.md`) plus listed immutable dependencies. A successor manifest is written and verified before `ACTIVE.json` selects it; update the selector last. A missing/torn/mismatched selector, inconsistent root state/decision, missing/hash-mismatched file, or multiple complete children is `INCOMPLETE/CONFLICT`. Stop; do not mix files or infer from timestamps/JSONL order. Recover manually from the prior immutable complete snapshot after verifying it. Legacy cases are limited to the explicit allowlist above and follow their existing state without retroactive certification.

Claim selection is explicit: use only `active_claim_ids` listed in the complete manifest and repeated in current state/decision. `supersedes` records graph edges, not an automatic winner. If two descendants compete and the active selection is missing or inconsistent, stop for owner/reviewer resolution.

Before changing an accepted decision or performing an external action, inspect the separate approval record. An approval applies only to its exact action/scope and revision ID plus complete-manifest SHA-256. Any new revision/hash, changed action/scope, expired approval, or changed decisive premise invalidates reuse; request a new human approval. No approval, recommendation, or checkpoint grants host permissions.

Create a new immutable revision ID with the verified parent. Save all required snapshots and hash every saved snapshot and decision dependency (source snapshots, inputs and ledgers actually used). Record exact active claim IDs. Write the manifest last with `status: "COMPLETE"` only after verifying completeness and hashes. Otherwise leave the candidate incomplete; the prior complete checkpoint remains the only resumable decision.

For legacy cases, retain existing append-only rules: do not rewrite prior files/journal entries; add new successor claims and explicitly select them in current state/decision. Do not retrofit a manifest or approval onto historical work.

Update state with work read, differences, claims revised, unknowns and one exact next action. In `activity.jsonl`, record each source attempt/result and case-file write/edit failures/retries. Unknown attempt outcomes remain `UNKNOWN`.
