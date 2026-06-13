# Codex Spec Audit

Дата обновления: 2026-06-13

## 1. Сводка

| Severity | Всего | Current | Historical |
|---|---:|---:|---:|
| critical | 171 | 0 | 171 |
| high | 0 | 0 | 0 |
| medium | 261 | 3 | 258 |
| low | 16 | 0 | 16 |

Всего findings: 448
Current findings: 3
Historical/stale findings: 445
Активных critical findings: 0

## 2. Проверка доменной логики

- Проверен запрет прямой связи `ModelElement -> GESNNorm` в `docs/grace/knowledge-graph.xml`.
- Прямая доменная методика не изменялась.

## 3. Проверка reference data discipline

- Проверено наличие `No source — no rule` в `AGENTS.md` через обязательный раздел Reference data discipline.
- Нормативные данные не создавались и не подключались.

## 4. Проверка accepted artifact protection

- Проверен `docs/artifact-registry.yml`.
- Accepted/protected artifacts не изменялись автоматически.

## 5. Проверка dashboards

- Проверены acceptance, user-action и verification dashboards.
- User-owned поля не закрывались от имени Codex.

## 6. Проверка monthly defense layer

- Проверен active monthly block на 3 задачи по 15 часов.

## 7. Проверка dissertation sync

- Проверено отсутствие прямого DOCX/PDF update artifact в `thesis/`.
- Проверены базовые guardrails для forbidden claims.

## 8. Проверка языковой политики

- Детальная языковая проверка выполняется `make audit-language`.

## 8.1. Проверка Git workflow

- Проверены branch naming, forbidden staged/untracked files, merge acceptance gates и mixed EP scopes.
- Advisory findings по текущему dirty baseline не блокируют `make check`.

## 9. Active findings

| ID | Severity | Check | File | Issue | Recommendation | Status |
|---|---|---|---|---|---|---|
| AUD-GIT-002-MERGE-FORBIDDEN-EP-024-DATA-CONTRIBUTION-AND-ANONYMIZATION-LAYER | medium | AUD-GIT-002 | docs/acceptance/EP-024-DATA-CONTRIBUTION-AND-ANONYMIZATION-LAYER.acceptance.md | Merge запрещен для EP-024-DATA-CONTRIBUTION-AND-ANONYMIZATION-LAYER: status=ready_for_acceptance, acceptance_decision=pending, accepted_by=empty. | Не готовить merge, пока пользователь не поставит accepted и accepted_by. | open |
| AUD-GIT-005-MIXED-EP-SCOPES | medium | AUD-GIT-005 | .git | Working tree содержит изменения нескольких EP scopes: EP-005, EP-006, EP-007, EP-009, governance | Не выполнять commit/merge до ручного разделения изменений или явного user approval. | open |
| AUD-GIT-006-NO-MAIN-MERGE-APPROVAL-EP-024-DATA-CONTRIBUTION-AND-ANONYMIZATION-LAYER | medium | AUD-GIT-006 | docs/git-workflow.md | Для EP-024-DATA-CONTRIBUTION-AND-ANONYMIZATION-LAYER нет явного user approval на merge в main. | Получить явное разрешение пользователя после приемки и успешных проверок. | open |

## 10. Critical findings

- Активных critical findings нет.

## 11. Historical/stale finding groups (`audit_finding_groups`)

| Group | Severity | Category | Total | Current | Historical | Active blocking | Recommendation |
|---|---|---|---:|---:|---:|---|---|
| AUD-ACCEPT-CODEX-USER-FIELD | critical | acceptance | 171 | 0 | 171 | False | Historical findings are preserved but hidden from active_review_items while current_detected=false. |
| AUD-GIT-001 | medium | git_workflow | 2 | 0 | 2 | False | Historical findings are preserved but hidden from active_review_items while current_detected=false. |
| AUD-GIT-002 | medium | git_workflow | 8 | 1 | 7 | False | Не готовить merge, пока пользователь не поставит accepted и accepted_by. |
| AUD-GIT-006 | medium | git_workflow | 15 | 1 | 14 | False | Получить явное разрешение пользователя после приемки и успешных проверок. |
| AUD-LANG-001 | medium | language_policy | 251 | 0 | 251 | False | Historical findings are preserved but hidden from active_review_items while current_detected=false. |

## 12. Findings, требующие решения пользователя

- Нет findings, требующих решения пользователя.

## 13. Команды проверки

```sh
make audit-codex-spec
make audit-language
make validate-audit
make audit
make validate-plan
make check
```

## 14. Что не исправлялось автоматически

- Не выполнялась массовая русификация.
- Не переписывались существующие документы вне audit-контура.
- Не менялись accepted/protected artifacts без user approval.
- Findings не закрывались как `fixed` автоматически.
- Historical findings с `current_detected: false` сохранялись как история и не считались active blockers.
