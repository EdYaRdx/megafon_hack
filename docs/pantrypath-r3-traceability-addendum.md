# PantryPath R3 — traceability-addendum

**Дата аннотации: 16 ноября 2026 года.** Это позднейшая навигационная аннотация, не historical R3, не новая ревизия и не новое исследование. Сохранённые снимки, manifests и checksum-pinned журналы не изменяются. [Назад к demo guide](pantrypath-demo.md).

## Какая версия и где проверять

[ACTIVE.json](../cases/pantrypath-week4-20261115/ACTIVE.json), строка 1, выбирает `R0003`. [Manifest R3](../cases/pantrypath-week4-20261115/revisions/R0003/manifest.json), строки 2–5: `R0003`, parent `R0002`, `COMPLETE`, active claims `C-01`–`C-09`; строки 22–24 и 27–31 фиксируют CSV, source snapshots и журналы через SHA-256. Это декларация manifest, а не самостоятельное доказательство успешной проверки hashes.

Далее locators относятся к файлам внутри `cases/pantrypath-week4-20261115/`. Строки — физические строки файлов. Общие журналы: [sources.jsonl](../cases/pantrypath-week4-20261115/sources.jsonl), [evidence.jsonl](../cases/pantrypath-week4-20261115/evidence.jsonl), [claims.jsonl](../cases/pantrypath-week4-20261115/claims.jsonl). Конечный документ — immutable [решение R3](../cases/pantrypath-week4-20261115/revisions/R0003/decision.md), а не только текущий корневой memo.

| Исходник и source locator | Evidence → claim (строки журналов) | Locator в решении R3 |
|---|---|---|
| [pilot-summary.csv](../cases/pantrypath-week4-20261115/inputs/pilot-summary.csv), заголовок 1, `current_flow` 2, `prep_checklist` 3; `S-004`, sources:4 | `E-001`/`E-002`, evidence:1–2 → `C-01`, claims:1, `OBSERVED` | Строки 9, 18: описательные counts и разница |
| Те же CSV-строки + [ops-note.md](../cases/pantrypath-week4-20261115/inputs/ops-note.md):3; `S-003`, sources:3 | `E-001`–`E-003`, evidence:1–3 → `C-02`, claims:2, `INFERENCE` | Строки 8–9, 17–19: нет оснований обещать retention win |
| `ops-note.md`:5; `S-003` | `E-003`, evidence:3 → `C-03`, claims:3, `CLAIMED` | Строки 12, 18–19: трудозатраты не подтверждены |
| [Снимок GOV.UK](../cases/pantrypath-week4-20261115/sources/S-001-govuk-user-research.md), разделы “Choose relevant research activities”, “Work out participant numbers”, “Map out rounds of research”; `S-001`, sources:1 | `E-004`, evidence:4 → `C-04`, claims:4, `DOCUMENTED` | Строки 18, 20: методика, не продуктовый эффект или power calculation |
| Источника и evidence нет | `C-05`, claims:5, `HYPOTHESIS`, `evidence_ids: []` | Строки 12, 16, 20: будущая диагностика, не установленная причина |
| [S-005-r2-addendum.md](../cases/pantrypath-week4-20261115/sources/S-005-r2-addendum.md):6, “Finance has capped…”; `S-005`, sources:5 | `E-005`, evidence:5 → `C-06` (`CLAIMED`), `C-07` (`INFERENCE`), claims:6–7 | Строки 8, 11–12, 16, 20, 22: условное ограничение ресурсов и подготовки решения |
| Тот же source:6, “The partnerships group wants copy…” | `E-006`, evidence:6 → `C-08`, claims:8, `CLAIMED` | Строки 14, 17, 19: заявлен срок, но нет контекста и разрешения |
| Тот же source:8 + пустой [approvals.jsonl](../cases/pantrypath-week4-20261115/approvals.jsonl) | `E-007`, evidence:7 → `C-09`, claims:9, `OBSERVED` | Строки 14, 21–22: воспоминание о согласовании не разрешает действие |

`S-002` (sources:2, [executive-brief.md](../cases/pantrypath-week4-20261115/inputs/executive-brief.md)) задаёт исходный запрос; отдельного evidence/claim-ребра для него в журналах нет.

## Формула и границы интерпретации

CSV: строка 2, `returned_week4=18`, `eligible_accounts=48`; строка 3, `returned_week4=22`, `eligible_accounts=48`.

`(22/48 - 18/48) * 100 = 8.33 п.п.` — округлено до двух знаков; исторические `+8.3 п.п.` в `C-01` и memo округлены до одного. Знаменатель — все `eligible_accounts` каждой группы, **не** `started_week1` (44/43) и не завершившие настройку. Исторический receipt расчёта R1 сохранён в [test-plan R3](../cases/pantrypath-week4-20261115/revisions/R0003/test-plan.md), строки 19–44, формула — строка 43; эта аннотация не заменяет receipt и не утверждает новый запуск.

Все counts синтетические. Неизвестны определения события/окна возврата, распределение групп, даты и зрелость когорт, экспозиция, дедупликация и полнота исходов. Разница не доказывает причинный эффект, retention lift или D30-семантику. Ресурсы и сроки R2 остаются `CLAIMED`; `C-07` условен. Решение владельца отсутствует, approvals пуст: R3 не разрешает разработку, набор участников, расходы или внешнее сообщение. Остальные варианты, стратегии и история уже описаны в demo guide и здесь не повторяются.
