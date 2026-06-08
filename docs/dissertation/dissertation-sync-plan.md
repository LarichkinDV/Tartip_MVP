# Dissertation Sync Plan

Цель контура: отделить изменения проекта Tartip от редакции диссертационного DOCX и обеспечить проверяемую цепочку принятия изменений.

## Workflow

1. Tartip execution packet фиксирует изменение проекта.
2. Dissertation impact classification определяет, затрагивает ли изменение научный текст.
3. Impact-log entry создается в `docs/dissertation/dissertation-impact-log.yml`.
4. Section-update-queue entry создается в `docs/dissertation/section-update-queue.yml`.
5. Prompt generation создает prompt в `docs/dissertation/prompt-queue/pending/`.
6. Prompt user review выполняет пользователь.
7. Patch generation создает markdown patch в `docs/dissertation/patches/pending/`.
8. Patch user acceptance выполняет пользователь.
9. DOCX update выполняется только по явному запросу пользователя.
10. Rendered review выполняется после DOCX update.
11. Dissertation version log обновляется после принятого изменения.

## Границы

- Tartip является прикладной программной реализацией и экспериментальной базой.
- Диссертация описывает научную методику, а не внутреннюю архитектуру разработки.
- GRACE, Codex, dashboards и execution packets не являются научным результатом.
- Фактические данные не заменяют нормативную базу.
- Снижение трудоемкости требует отдельного хронометражного исследования.

## Decision Gates

- `pending`: создано Codex и ожидает пользователя.
- `requires_review`: требуется ручная оценка влияния.
- `accepted`: только пользователь может присвоить этот статус.
- `rejected`: только пользователь может отклонить prompt или patch.
- `blocked`: дальнейшее действие требует данных, источников или явного решения.

## DOCX Policy

DOCX update не выполняется в рамках автоматической синхронизации. Для DOCX update нужны:

- accepted markdown patch;
- explicit user request;
- render/visual check;
- запрет автоматического изменения библиографической нумерации.
