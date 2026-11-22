> Historical release snapshot — superseded for current submission status by [22 November final readiness](../submission-ready-20261122/README.md). The PRIVATE/public-history NO-GO and v3 PDF statements below describe the earlier release time. Current GitHub metadata confirms PUBLIC; the owner-supplied final PDF is included. Original report body retained unchanged.

# Release verification results

Base: fetched origin/main ed42fef67451ba48a5c6827f5f67cfef015996d3.
Branch: codex/mgimo-final-release-20261122. The final commit SHA is reported by Git in the handoff; embedding its own hash into a commit would be circular.

## Completed

- Final integrated full unit suite: **121 tests, 0 failures, 0 errors, 5 skips, exit0**. Unittest 64.024 s; captured command wall span 64.750723 s. [Actual receipt](unit-tests.json).
- Baseline rerun: 121 tests,10 failures,1 error,5 skips. [Observed receipt](baseline-tests.json) and [investigation/fixes](TEST_INVESTIGATION.md). The exact earlier26/4 raw log was unavailable; not retrospectively relabeled.
- Only test fixture canonicalization, explicit CLI UTF-8 and preference for installed PowerShell7 in captured fallback tests changed. Assertions/skip conditions/runtime/Skills/checkpoint protocol unchanged. Symlink skips are OS privilege limits, not passed checks.
- Privacy-safe derivative D0001: real shared [gate](linguastep-export-gate.json), [classify](linguastep-export-classify.json), [inventory](linguastep-export-inventory.json), all exit0. [Original preservation and provenance](export-provenance-check.json).
- Separate read-only content/privacy and jury reviews. No new product E2E, real diagnosis or fresh model Resume was run in this release session.
- Current PDF v3 hash matched; pages14/15 rendered and visually checked for insertion location. No PDF bytes changed; exact editable v3 layout not found.

## Final checklist

Repository/link/hash/privacy/diff results are recorded in final-checks.json after the last content edits. External links are listed as provided, not described as anonymously accessible. No release-branch CI result is invented; main CI is a separate prior result.

## Release decision

**GO for the locally verified release candidate**, subject to the actual final-checks receipt.
**CONDITIONAL GO for distribution/submission:** owner confirms rights, whole video, exact duration, recipient access, final PDF/version and portal submission. Existing private Git visibility is retained; public history exposure is NO-GO pending owner review of identifying historical paths. A history-free checked archive is prepared as the safe distribution candidate. Do not expose raw qualification originals or account telemetry.

No business lift, comparative superiority, autonomous free-form NEW or Cursor certification is asserted.
