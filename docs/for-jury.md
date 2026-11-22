# Для жюри: проверка за несколько минут

[Главная](../README.md) · [Все функции и статусы](capabilities.md) · [Quick Start](quickstart.md)

## Четыре обязательных материала

| Материал | Открыть | Статус и граница |
|---|---|---|
| Единственный конкурсный репозиторий | [GitHub main](https://github.com/EdYaRdx/megafon_hack/tree/main) | PUBLIC подтверждён API 22.11.2026; эта проверка права доступа не меняет |
| Демонстрационный проект | [МегаФон: короткая продуктовая история](demos/megafon.md) · [LinguaStep](demos/linguastep.md) | Прямые ссылки на задачи, учебные входы, альтернативы, решения PO, четыре стратегии и два плана; защищённые папки дел доступны внутри |
| Запись работы | [Видео E2E](https://drive.google.com/file/d/1kDBIVW_hgRwh2WnttYouUtfnlhtD27P_/view), [папка Drive](https://drive.google.com/drive/folders/12ZOJFDD96tkRtEe0D5MGdJh69ypJ0irE?usp=sharing), [этапы](video-e2e.md) | anyone / reader подтверждён metadata для файла и папки; полный просмотр записи этой проверкой не выполнялся |
| Финальное описание | [PDF «Ромашка MISIS», 17 страниц A4](MGIMO_FINAL_REPORT.pdf), [подробное описание](submission-description.md) | Предоставленный MGIMO_Romashka_MISIS.pdf включён без изменения байтов; [проверка страниц, ссылок и области заявлений](release/submission-ready-20261122/README.md) |

## Четыре критерия — конкретные доказательства

| Критерий | Что посмотреть | Что подтверждено | Предел |
|---|---|---|---|
| Проработанность | [Семейные альтернативы](../cases/family-multinumber-video/options.md), [пересмотр](../cases/family-multinumber-video/research/D0003/review.md), [LinguaStep decision](../cases/linguastep-retention/decision.md) | Шесть и пять разных направлений со статус-кво/остановкой, возражения, выбор PO, согласованные стратегии, validation design | Нет полевого спроса/причинного или финансового эффекта; неизвестные входы не придуманы |
| Масштаб использования нейротехнологий | [Карта возможностей](capabilities.md), [архитектура](architecture.md), [шесть Skills](../.agents/skills/) | File-first workflow, контекст/знания, PDF/CSV/web evidence, CLI, fallback, память/Resume/Revise | Skills — процедуры; hooks/MCP/subagent runtime/router/мониторинг не заявлены без реализации |
| Имплементация | [Оригинальный новый чат LinguaStep](release/final-20261122/source-resume-receipt.json), [проверки D0001](release/final-20261122/README.md), [CI main](https://github.com/EdYaRdx/megafon_hack/actions?query=branch%3Amain) | Второй synthetic workflow до R0001 и owner-confirmed genuine Resume; отдельно checked derivative D0001; штатные gates и реальные unit/CI | Case создан оператором; Cursor/свободный NEW целиком не квалифицированы; receipt unsigned/limited, не полный platform export |
| Качество | [Test receipt](release/final-20261122/unit-tests.json), [F9 comparison](../research/sol-audit/eval-results/F9-resume-comparison-20261113.md), [правила метрик](../references/metrics.md) | Ясный следующий шаг, ограничения/PO gates, воспроизводимые формулы, ошибки/повторы и explicit UNKNOWN | Full task elapsed, активное время PO, calls/tokens/billing UNKNOWN. F9 не доказывает точность/скорость/стоимость superiority |

Это связь требований с доказательствами, не прогноз баллов жюри.

Два независимых учебных кейса дают 11 альтернатив, четыре стратегии и два плана проверки. Основу составляют 6 Skills, PDF / CSV / Web, evidence / claims / UNKNOWN, воспроизводимые вычисления и управляемые человеком checkpoint / Resume / Revise. [CI опубликованного PDF-релиза 3005460](https://github.com/EdYaRdx/megafon_hack/actions/runs/45060829339): 121 тест, 116 passed + 5 skipped; [актуальный CI main](https://github.com/EdYaRdx/megafon_hack/actions?query=branch%3Amain).

## Две продуктовые и две коммуникационные стратегии

| Кейс | Продуктовая | Коммуникационная | План проверки |
|---|---|---|---|
| Семейная помощь | [Продуктовая D0003](../cases/family-multinumber-video/strategy-product.md) | [Коммуникационная D0003](../cases/family-multinumber-video/strategy-communication.md) | [P0–P3](../cases/family-multinumber-video/test-plan.md) |
| LinguaStep | [Продуктовая D0001](../cases/linguastep-retention/strategy-product.md) | [Коммуникационная D0001](../cases/linguastep-retention/strategy-communication.md) | [Ограниченная диагностика B](../cases/linguastep-retention/test-plan.md) |

## Быстрый маршрут проверки

1. Открыть видео и соответствующий этап семейного кейса.
2. В LinguaStep сопоставить CSV строки2–5 с saved calculation: 1100/2000=55% →1000/2000=50%, оба сегмента +5 п.п. При январских весах февраль=60%; within +5 и mix-at-Feb −10 п.п. Это описательная, зависящая от reference декомпозиция.
3. Сверить реальный выбор B и две стратегии; operational D30 contract, сроки/пороги и ресурсы UNKNOWN. Диагностика/продуктовый эксперимент не запускались.
4. Проверить [исторический source Resume](release/final-20261122/source-resume-receipt.json) и [отдельный экспорт](../cases/linguastep-retention/EXPORT.md): оригинальный R0001 и опубликованный D0001 — разные байты.
5. Открыть CI main и конкретные receipts. Не приравнивать Python inventory к ответу модели в новом чате.

## Инженерная проверка файлов

Из корня clone с рабочим Python3.12+ (python ниже — обозначение найденного executable):

    python -B tools/case_protocol.py check-candidate cases/family-multinumber-video --revision D0003
    python -B tools/case_protocol.py check-candidate cases/linguastep-retention --revision D0001
    python -B tools/case_protocol.py classify cases/linguastep-retention

Доступ к файлам/exec задаёт host. Эти read-only команды проверяют hashes/ancestry/current views, не качество стратегии или live E2E. Новый эксперимент не требуется для чтения результатов. [Полный контракт](../cases/_template/README.md).

[Доступы и категории публичных сведений](publication-safety.md) · [Evaluation с историческими ограничениями](evaluation.md).
