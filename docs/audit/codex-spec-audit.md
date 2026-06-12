# Codex Spec Audit

Дата обновления: 2026-06-12

## 1. Сводка

| Severity | Всего | Current | Historical |
|---|---:|---:|---:|
| critical | 171 | 0 | 171 |
| high | 0 | 0 | 0 |
| medium | 247 | 2 | 245 |
| low | 16 | 0 | 16 |

Всего findings: 434
Current findings: 2
Historical/stale findings: 432
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
| AUD-GIT-001-BRANCH-NAME-MISMATCH | medium | AUD-GIT-001 | .git | Имя ветки ep-017-audit-findings-cleanup не соответствует packet EP-021-POST-ACCEPTANCE-SYNC-AUTOMATION. | Использовать формат ep-021-<short-slug>. | open |
| AUD-GIT-005-MIXED-EP-SCOPES | medium | AUD-GIT-005 | .git | Working tree содержит изменения нескольких EP scopes: EP-005, EP-007, EP-009, governance | Не выполнять commit/merge до ручного разделения изменений или явного user approval. | open |

## 10. Critical findings

- Активных critical findings нет.

## 11. Historical/stale finding groups (`audit_finding_groups`)

| Group | Severity | Category | Total | Current | Historical | Active blocking | Recommendation |
|---|---|---|---:|---:|---:|---|---|
| AUD-ACCEPT-CODEX-USER-FIELD | critical | acceptance | 171 | 0 | 171 | False | Historical findings are preserved but hidden from active_review_items while current_detected=false. |
| AUD-GIT-001 | medium | git_workflow | 2 | 1 | 1 | False | Использовать формат ep-021-<short-slug>. |
| AUD-GIT-002 | medium | git_workflow | 1 | 0 | 1 | False | Historical findings are preserved but hidden from active_review_items while current_detected=false. |
| AUD-GIT-006 | medium | git_workflow | 8 | 0 | 8 | False | Historical findings are preserved but hidden from active_review_items while current_detected=false. |
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
