# Расчёты beta-survey.csv

Источник: input/beta-survey.csv, header строка 1, единственная запись строка 2. Единица — счётчики одной синтетической когорты prototype_testers; период неизвестен. Повторно выполнено PowerShell Import-Csv, 2026-11-14:
- responded / invited = 24 / 120 = 0.20 = 20% (доля ответов по представленным счётчикам; eligibility и disposition остальных UNKNOWN).
- clicked_interested / responded = 15 / 24 = 0.625 = 62.5% (интерес среди ответивших).
- clicked_interested / invited = 15 / 120 = 0.125 = 12.5% (приглашённые с отметкой).
Входные флаги: synthetic=true, random_sample=false, question_wording_known=false. Это только описательные отношения, не оценка спроса; доверительный интервал/экстраполяция не рассчитывались.
Команда: $surveyRows = @(Import-Csv -LiteralPath 'cases/codex-e2e-run1-20261114/input/beta-survey.csv'); $row = $surveyRows[0]; $invitedCount=[int]$row.invited; $respondentCount=[int]$row.responded; $interestedCount=[int]$row.clicked_interested; вычислить 100*$respondentCount/$invitedCount; 100*$interestedCount/$respondentCount; 100*$interestedCount/$invitedCount.
