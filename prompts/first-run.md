# Первый запуск продуктового дела

Сначала прочитай `AGENTS.md`, `cases/<case-id>/brief.md`, `cases/<case-id>/README.md`, `case-protocol.json` и единственный канонический Skill текущего этапа. Для нового дела начни с `.agents/skills/intake/SKILL.md`; для продолжения существующего — до чтения/изменения mutable root files следуй `.agents/skills/resume-revise/SKILL.md`.

Работай только в новой копии `cases/_template/`, не в шаблоне и не в примере. Уточни решение, владельца, аудиторию, срок, цель, ограничения, разрешённые материалы и неизвестные, способные изменить следующий шаг. Задай только consequential вопросы; неизвестное запиши как `UNKNOWN`. Не исследуй и не рекомендуй до прояснения того, что влияет на направление.

Связывай источники и точные locators с evidence, claims и memo; различай `OBSERVED`, `DOCUMENTED`, `CLAIMED`, `INFERENCE`, `HYPOTHESIS`, `UNKNOWN`. Не выдавай synthetic input, модельные рассуждения, поиск или методическую статью за customer evidence. Рассмотри минимум три содержательно разных варианта, включая explicit status quo и stop/close; отрази возражения и условия пересмотра. Согласуй product strategy, аудиторию/обещание/канал и validation plan с метрикой, comparator, знаменателем, периодом, guardrails и decision rule. Не выдумывай пороги или экономику.

Сохраняй итог в файлах дела: короткий decision memo с claim IDs и ссылками на source locator, product и communication strategy, validation plan, activity receipt, state и exact next step. Время, model/tool names, вызовы и расходы укажи только если host реально их показывает; иначе `UNKNOWN`. Ошибки и повторы не скрывай.

Среда выполнения определяет доступные модели, файловые, сетевые и вычислительные инструменты, права, телеметрию и стоимость. Инструкции не предоставляют эти возможности, не изолируют host и не enforce approval. Web и вычислительные средства optional; если отсутствуют, помечай source/operation `NOT RUN`. Не используй закрытые данные, credentials или PII. Не отправляй сообщения, не публикуй, не трать, не набирай участников и не запускай deployment без точного человеческого разрешения.

В конце оставь ровно один рекомендуемый следующий шаг. При pause/revise сначала проверь unique complete checkpoint: exact snapshot/dependency hashes, ledger prefix integrity, selected revision/parent/active claims и selector consistency. При mismatch, stale approval, fork или ambiguous state остановись `INCOMPLETE/CONFLICT`; не восстанавливай смешанное состояние.
