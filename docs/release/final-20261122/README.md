> **Исторический срез — промежуточная упаковка 22.11.2026 до PR32/34. Примечание 22.11.2026:** PRIVATE, неподтверждённый доступ, ожидание PDF/merge и прежние рекомендации о публикации ниже относятся к моменту этой записи. [Актуальная готовность](../submission-ready-20261122/README.md) фиксирует PUBLIC, опубликованный финальный PDF, normal merge и CI SUCCESS релиза 3005460. Это не новая проверка старых испытаний: их FAIL / BLOCKED / REVIEW_REQUIRED и неизвестное сохраняются в исходном scope. Права передачи, полный просмотр видео и отправка формы остаются действиями владельца.

# Final release evidence — 22 November 2026

[Four criteria](CRITERIA.md) · [Privacy and distribution](PRIVACY.md) · [PDF insertion](PDF_UPDATE.md)

## Two cases and three distinct evidence claims

| Evidence | Primary artifact | Scope |
|---|---|---|
| Megafon recorded case | [Video route](../../video-e2e.md), [family D0001–D0003](../../../cases/family-multinumber-video/README.md) | Owner-reported recorded live workflow, two strategies, Resume and critical review; educational data |
| LinguaStep original R0001 | [Limited Resume receipt](source-resume-receipt.json) | Owner confirms genuine new-chat Resume; recorded tool outputs restored R0001 at source manifest f5d178602d01c186428e2fd775efe16aafc5cc1f430fa6cf593c05f6af6df618. Unsigned limited transcription, not complete platform session export |
| LinguaStep privacy-safe derivative D0001 | [Case](../../../cases/linguastep-retention/README.md), [provenance](../../../cases/linguastep-retention/EXPORT.md), [map](../../../cases/linguastep-retention/export-map.json) | Newly hashed export; actual CLI checks below validate exported bytes, not a new model E2E/Resume |

Original R0001 and ACTIVE/manifest remain unchanged in the retained private source copy. Export strips local machine paths, account quota/credit snapshots, raw host activity, unnecessary command traces and raw public-page HTML (parsed method text retained). Source human choice B is preserved as historical normalized input; no execution approval transfers to D0001.

## Inspect the result

- [Five alternatives](../../../cases/linguastep-retention/options.md), [decision](../../../cases/linguastep-retention/decision.md), [product strategy](../../../cases/linguastep-retention/strategy-product.md), [communication strategy](../../../cases/linguastep-retention/strategy-communication.md), [validation plan](../../../cases/linguastep-retention/test-plan.md).
- [Brief](../../../cases/linguastep-retention/inputs/brief-source.md), [CSV](../../../cases/linguastep-retention/inputs/cohorts.csv), [method text](../../../cases/linguastep-retention/sources/S-003-amplitude-text.txt).
- Supplied-count ratios: January 1100/2000=55%, February 1000/2000=50%; both segments +5 percentage points; paid share 50%→75%. February standardized to January shares =0.5×40%+0.5×80%=60%; January-reference within +5 pp and mix at February rates −10 pp total −5 pp. Descriptive, reference-dependent, not causal; true operational D30 contract UNKNOWN.
- [F9 ordinary/structured/file-agent comparison](../../../research/sol-audit/eval-results/F9-resume-comparison-20261113.md): persistence differs; no established speed, cost or accuracy superiority.

## Actual exported-byte checks

[Shared candidate gate](linguastep-export-gate.json): VALIDATED_CANDIDATE, exit0.
[Actual classify](linguastep-export-classify.json): CHECKPOINTED, exit0.
[File inventory](linguastep-export-inventory.json): D0001, no unfinished drafts; file inventory is not model Resume.
Command paths in public receipts are explicitly redacted; full local originals are retained privately.

## Limits and release gates

The case was operator-created. No independent free-form NEW creation, Cursor E2E, real retention diagnosis, user research, product/budget change, pilot or causal/business effect was run. Full task wall-clock, human active time, model calls/tokens and direct billing are UNKNOWN. No account quota is interpreted as case spend.

Latest test outcomes and release commit are in [release results](RELEASE_RESULTS.md). Repo/video recipient access, rights to materials, complete video review and final contest submission require the owner. A locally checked branch is not proof of access or submission.

Final release also includes the [test investigation](TEST_INVESTIGATION.md), [actual unit receipt](unit-tests.json), [current-tree privacy scan](privacy-check.json), [external HTTP checks](external-links.json) and [final local checks](final-checks.json). Public Git history contains identifying path references and is held for owner approval; prefer the checked history-free archive.
