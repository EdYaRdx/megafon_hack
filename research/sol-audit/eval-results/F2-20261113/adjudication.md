# F2 adjudication — exploratory only

## Result

Two separate task contexts assigned the same descriptive scores. Reviewer model/provider identity and cross-family independence are `UNKNOWN`; scores are not human adjudication. No P0 was found.

| Arm (mapping held by run log) | Output | Score / 8 | Critical terms correct? | Principal omission |
|---|---|---:|---|---|
| B0 plain chat | run-17 | 3 | Yes | No locators, three distinct options, or validation plan. |
| B1 structured prompt | run-28 | 5 | Yes | No explicit status quo; communication and validation audience/barrier/comparator details incomplete. |
| A file-agent instructions/skills | run-43 | 5 | Yes | No explicit status quo; validation comparator, audience, and threshold not fully specified. |

**P0:** 0/3. All reject unsupported “unlimited,” nationwide, and flat ongoing 299 ₽ claims, distinguish v3 publication from its 2026-12-01 effective date, and avoid claims of real economics, demand, legal approval, or campaign effect.

## Reviewer disagreements and resolution

Reviewer 1 alleged the product name “Beacon” in run-43 was unsupported. The frozen local materials identify the fictional offer as Beacon in `input/promo.html` title and both terms §4; this finding is rejected. Reviewer 2 treated the v2 publication date as unverified; direct read of `input/terms-v2.md:3` confirms 2026-10-30. No scoring change follows.

Both reviewers agree on the totals. The structured and file-agent outputs were more complete than plain chat on this single scenario, but both scored 5/8 and missed an explicit status quo. This does not establish superiority: one fixture, one run per arm, model/provider/resource equivalence unknown, concurrent rather than randomized execution, no human scorer, and the A arm was read-only (no persistence or case-file writes). Token use, human-active time and billing cost remain UNKNOWN. Only task durations are logged; they are not comparable labor or total latency measures.

## Decision

Treat F2 as a useful exploratory diagnostic, not a release gate. Follow-up: fix the agent procedure/output contract to require explicit status quo and a validation comparator/population/metric/time/guardrails; rerun on held-out F1 and F3 before crediting any improvement. Do not change the frozen F2 input or key.