# Codex Spec Audit

Дата обновления: 2026-06-11

## 1. Сводка

| Severity | Количество |
|---|---:|
| critical | 171 |
| high | 0 |
| medium | 245 |
| low | 16 |

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

## 9. Открытые findings

| ID | Severity | Check | File | Issue | Recommendation | Status |
|---|---|---|---|---|---|---|
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1001 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1041 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1061 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1141 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1161 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1181 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1201 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1241 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1261 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1281 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1301 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1321 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1361 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1381 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1401 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1441 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1461 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1481 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1501 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1521 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1541 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1601 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1621 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1641 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1661 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1681 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1701 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1721 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1741 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1761 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1781 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1801 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1821 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1841 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1861 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1901 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1961 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1981 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2001 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2041 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2081 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2101 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2121 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2141 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2161 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2181 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2201 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2241 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2261 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2281 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2301 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2321 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2341 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2361 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2381 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2401 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2501 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2541 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2561 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2581 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2601 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2641 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2681 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2701 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2721 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2741 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2761 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2781 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2801 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2821 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2841 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2861 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2881 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2921 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2941 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-301 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-3041 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-3061 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-3081 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-3101 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-3121 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-3141 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-3161 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-3181 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-3261 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-3281 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-3321 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-3341 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-341 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-3421 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-3441 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-3461 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-3481 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-3501 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-3521 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-3541 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-3561 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-3601 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-361 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-3641 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-3661 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-3701 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-3761 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-3801 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-381 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-3821 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-3861 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-3881 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-3921 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-3961 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4021 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4041 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4081 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4121 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4141 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4161 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4181 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4201 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-421 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4241 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4261 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4281 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4301 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4361 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4381 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4401 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-441 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4421 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4461 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4481 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4501 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4521 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4561 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4621 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4641 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4661 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4681 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4701 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4721 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4761 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4781 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4821 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4841 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4881 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4901 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4921 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4941 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4961 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-5021 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-5041 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-5061 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-5081 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-5141 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-5161 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-5201 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-5221 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-5261 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-5281 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-5301 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-561 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-581 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-621 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-681 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-721 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-741 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-781 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-881 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-901 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-941 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-961 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-981 | critical | AUD-ACCEPT-001 | docs/user-action-dashboard.yml | Поле answered_by установлено в Codex. | Заменить только после user-owned correction; Codex не может быть владельцем решения. | open |
| AUD-GIT-001-BRANCH-NAME-MISMATCH | medium | AUD-GIT-001 | .git | Имя ветки ep-015-verification-dashboard-reconciliation не соответствует packet EP-017-AUDIT-FINDINGS-CLEANUP. | Использовать формат ep-017-<short-slug>. | open |
| AUD-GIT-001-CURRENT-BRANCH-MAIN | medium | AUD-GIT-001 | .git | Текущая ветка main не соответствует EP-010-LANGUAGE-NORMALIZATION. | Создавать новую packet-ветку для новых EP; текущий dirty baseline требует user approval перед переключением. | open |
| AUD-GIT-005-MIXED-EP-SCOPES | medium | AUD-GIT-005 | .git | Working tree содержит изменения нескольких EP scopes: EP-005, EP-007, EP-009, governance | Не выполнять commit/merge до ручного разделения изменений или явного user approval. | open |
| AUD-GIT-006-NO-MAIN-MERGE-APPROVAL-EP-010-LANGUAGE-NORMALIZATION | medium | AUD-GIT-006 | docs/git-workflow.md | Для EP-010-LANGUAGE-NORMALIZATION нет явного user approval на merge в main. | Получить явное разрешение пользователя после приемки и успешных проверок. | open |
| AUD-GIT-006-NO-MAIN-MERGE-APPROVAL-EP-011-GIT-WORKFLOW-DISCIPLINE | medium | AUD-GIT-006 | docs/git-workflow.md | Для EP-011-GIT-WORKFLOW-DISCIPLINE нет явного user approval на merge в main. | Получить явное разрешение пользователя после приемки и успешных проверок. | open |
| AUD-GIT-006-NO-MAIN-MERGE-APPROVAL-EP-012-USER-REVIEW-WORKBENCH-AND-ACCEPTANCE-STANDARD | medium | AUD-GIT-006 | docs/git-workflow.md | Для EP-012-USER-REVIEW-WORKBENCH-AND-ACCEPTANCE-STANDARD нет явного user approval на merge в main. | Получить явное разрешение пользователя после приемки и успешных проверок. | open |
| AUD-GIT-006-NO-MAIN-MERGE-APPROVAL-EP-013-POST-ACCEPTANCE-STATE-SYNC | medium | AUD-GIT-006 | docs/git-workflow.md | Для EP-013-POST-ACCEPTANCE-STATE-SYNC нет явного user approval на merge в main. | Получить явное разрешение пользователя после приемки и успешных проверок. | open |
| AUD-GIT-006-NO-MAIN-MERGE-APPROVAL-EP-014-USER-REVIEW-DECISION-CLI-SAFETY | medium | AUD-GIT-006 | docs/git-workflow.md | Для EP-014-USER-REVIEW-DECISION-CLI-SAFETY нет явного user approval на merge в main. | Получить явное разрешение пользователя после приемки и успешных проверок. | open |
| AUD-GIT-006-NO-MAIN-MERGE-APPROVAL-EP-015-VERIFICATION-DASHBOARD-RECONCILIATION | medium | AUD-GIT-006 | docs/git-workflow.md | Для EP-015-VERIFICATION-DASHBOARD-RECONCILIATION нет явного user approval на merge в main. | Получить явное разрешение пользователя после приемки и успешных проверок. | open |
| AUD-GIT-006-NO-MAIN-MERGE-APPROVAL-EP-018-ACCEPTED-ARTIFACT-PROTECTION | medium | AUD-GIT-006 | docs/git-workflow.md | Для EP-018-ACCEPTED-ARTIFACT-PROTECTION нет явного user approval на merge в main. | Получить явное разрешение пользователя после приемки и успешных проверок. | open |
| AUD-LANG-001-0403b9742d | medium | AUD-LANG-001 | docs/07-reference-data-policy.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-0584b2a838 | medium | AUD-LANG-001 | docs/07-reference-data-policy.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-08e52774da | medium | AUD-LANG-001 | docs/07-reference-data-policy.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-0b144b99ab | medium | AUD-LANG-001 | docs/acceptance/EP-003-REFERENCE-VERSIONING.acceptance.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-0b2052d5df | medium | AUD-LANG-001 | docs/acceptance/EP-002-REFERENCE-GOVERNANCE.acceptance.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-0b243217e0 | medium | AUD-LANG-001 | docs/07-reference-data-policy.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-0ba615d854 | medium | AUD-LANG-001 | docs/acceptance/EP-002-REFERENCE-GOVERNANCE.acceptance.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-0ee5c2d891 | medium | AUD-LANG-001 | docs/acceptance/EP-003-REFERENCE-VERSIONING.acceptance.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-140fc5b5da | medium | AUD-LANG-001 | docs/acceptance/EP-003-REFERENCE-VERSIONING.acceptance.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-160edcdf15 | medium | AUD-LANG-001 | docs/acceptance/EP-003-REFERENCE-VERSIONING.acceptance.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-17931122a9 | medium | AUD-LANG-001 | docs/acceptance/EP-001-INFRA.acceptance.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-1993d93ded | medium | AUD-LANG-001 | docs/acceptance/EP-003-REFERENCE-VERSIONING.acceptance.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-1c2a65340e | medium | AUD-LANG-001 | docs/acceptance/EP-003-REFERENCE-VERSIONING.acceptance.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-1c6c2352c8 | medium | AUD-LANG-001 | docs/acceptance/EP-002-REFERENCE-GOVERNANCE.acceptance.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-1c9d128591 | medium | AUD-LANG-001 | docs/acceptance/EP-001-INFRA.acceptance.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-1ca0c9ad14 | medium | AUD-LANG-001 | docs/acceptance/EP-001-INFRA.acceptance.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-203660d971 | medium | AUD-LANG-001 | docs/acceptance/EP-001-INFRA.acceptance.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-237e9a0b6d | medium | AUD-LANG-001 | docs/07-reference-data-policy.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-2752cb38a8 | medium | AUD-LANG-001 | docs/07-reference-data-policy.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-284b1971ac | medium | AUD-LANG-001 | docs/07-reference-data-policy.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-2863e088cc | medium | AUD-LANG-001 | docs/acceptance/EP-002-REFERENCE-GOVERNANCE.acceptance.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-2b927a8c93 | medium | AUD-LANG-001 | docs/acceptance/EP-001-INFRA.acceptance.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-322d7641c0 | medium | AUD-LANG-001 | docs/07-reference-data-policy.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-391503f660 | medium | AUD-LANG-001 | docs/07-reference-data-policy.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-4066fb8d18 | medium | AUD-LANG-001 | docs/07-reference-data-policy.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-408cae52d8 | medium | AUD-LANG-001 | docs/07-reference-data-policy.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-4a895008f0 | medium | AUD-LANG-001 | docs/acceptance/EP-002-REFERENCE-GOVERNANCE.acceptance.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-4dc57e4b82 | medium | AUD-LANG-001 | docs/07-reference-data-policy.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-4e190036af | medium | AUD-LANG-001 | docs/acceptance/EP-001-INFRA.acceptance.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-539f295b1d | medium | AUD-LANG-001 | docs/acceptance/EP-003-REFERENCE-VERSIONING.acceptance.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-55388c287d | medium | AUD-LANG-001 | docs/acceptance/EP-002-REFERENCE-GOVERNANCE.acceptance.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-590d7770a6 | low | AUD-LANG-001 | docs/acceptance/EP-004-PROJECT-PLANNING-AND-ACCEPTANCE.acceptance.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-6529bcdc65 | medium | AUD-LANG-001 | docs/acceptance/EP-003-REFERENCE-VERSIONING.acceptance.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-65902480da | medium | AUD-LANG-001 | docs/07-reference-data-policy.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-662bc1efaa | medium | AUD-LANG-001 | docs/acceptance/EP-004-PROJECT-PLANNING-AND-ACCEPTANCE.acceptance.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-664f61b6bc | medium | AUD-LANG-001 | docs/acceptance/EP-004-PROJECT-PLANNING-AND-ACCEPTANCE.acceptance.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-696f7f1dec | medium | AUD-LANG-001 | docs/acceptance/EP-003-REFERENCE-VERSIONING.acceptance.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-72ded86315 | medium | AUD-LANG-001 | docs/07-reference-data-policy.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-76253fff5b | medium | AUD-LANG-001 | docs/acceptance/EP-004-PROJECT-PLANNING-AND-ACCEPTANCE.acceptance.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-84bd776410 | medium | AUD-LANG-001 | docs/07-reference-data-policy.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-85bb19af87 | medium | AUD-LANG-001 | docs/acceptance/EP-002-REFERENCE-GOVERNANCE.acceptance.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-85c871c337 | medium | AUD-LANG-001 | docs/07-reference-data-policy.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-88016cdc2a | medium | AUD-LANG-001 | docs/acceptance/EP-003-REFERENCE-VERSIONING.acceptance.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-891fe56c1e | medium | AUD-LANG-001 | docs/acceptance/EP-003-REFERENCE-VERSIONING.acceptance.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-9404737958 | medium | AUD-LANG-001 | docs/07-reference-data-policy.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-968c5d281c | medium | AUD-LANG-001 | docs/acceptance/EP-003-REFERENCE-VERSIONING.acceptance.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-96f06d57c4 | medium | AUD-LANG-001 | docs/07-reference-data-policy.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-9b0d0c9ced | medium | AUD-LANG-001 | docs/07-reference-data-policy.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-9f5e6b3e61 | medium | AUD-LANG-001 | docs/acceptance/EP-001-INFRA.acceptance.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-a000dddb0f | medium | AUD-LANG-001 | docs/acceptance/EP-004-PROJECT-PLANNING-AND-ACCEPTANCE.acceptance.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-a149677283 | medium | AUD-LANG-001 | docs/07-reference-data-policy.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-a58cccb460 | medium | AUD-LANG-001 | docs/acceptance/EP-003-REFERENCE-VERSIONING.acceptance.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-a61b931b31 | medium | AUD-LANG-001 | docs/07-reference-data-policy.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-a751af8091 | medium | AUD-LANG-001 | docs/07-reference-data-policy.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-a8fe4c398a | medium | AUD-LANG-001 | docs/acceptance/EP-002-REFERENCE-GOVERNANCE.acceptance.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-aad7f3cfe0 | medium | AUD-LANG-001 | docs/acceptance/EP-004-PROJECT-PLANNING-AND-ACCEPTANCE.acceptance.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-ad4f53f83b | medium | AUD-LANG-001 | docs/07-reference-data-policy.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-af6cd13752 | medium | AUD-LANG-001 | docs/acceptance/EP-003-REFERENCE-VERSIONING.acceptance.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-b25d5b3569 | medium | AUD-LANG-001 | docs/07-reference-data-policy.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-b43f7cd30a | medium | AUD-LANG-001 | docs/07-reference-data-policy.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-b54388e917 | medium | AUD-LANG-001 | docs/acceptance/EP-004-PROJECT-PLANNING-AND-ACCEPTANCE.acceptance.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-b5e844dc84 | medium | AUD-LANG-001 | docs/07-reference-data-policy.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-b80b176d2d | medium | AUD-LANG-001 | docs/acceptance/EP-001-INFRA.acceptance.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-b856004edd | medium | AUD-LANG-001 | docs/07-reference-data-policy.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-c2fc52453a | medium | AUD-LANG-001 | docs/07-reference-data-policy.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-c7e4c6a4d2 | medium | AUD-LANG-001 | docs/acceptance/EP-002-REFERENCE-GOVERNANCE.acceptance.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-c882327c71 | medium | AUD-LANG-001 | docs/07-reference-data-policy.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-cc0512c192 | medium | AUD-LANG-001 | docs/07-reference-data-policy.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-d3f78ad666 | medium | AUD-LANG-001 | docs/07-reference-data-policy.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-d4c4421471 | medium | AUD-LANG-001 | docs/07-reference-data-policy.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-d4dd8fec13 | medium | AUD-LANG-001 | docs/07-reference-data-policy.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-dcd6a88329 | medium | AUD-LANG-001 | docs/07-reference-data-policy.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-df602b0d72 | medium | AUD-LANG-001 | docs/07-reference-data-policy.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-e366604e83 | medium | AUD-LANG-001 | docs/acceptance/EP-004-PROJECT-PLANNING-AND-ACCEPTANCE.acceptance.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-f1060c8fb3 | medium | AUD-LANG-001 | docs/acceptance/EP-002-REFERENCE-GOVERNANCE.acceptance.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-f19dc9a207 | medium | AUD-LANG-001 | docs/acceptance/EP-004-PROJECT-PLANNING-AND-ACCEPTANCE.acceptance.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-f5f0484374 | medium | AUD-LANG-001 | docs/acceptance/EP-003-REFERENCE-VERSIONING.acceptance.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-f5f7163b46 | medium | AUD-LANG-001 | docs/acceptance/EP-002-REFERENCE-GOVERNANCE.acceptance.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-f7f501c85b | medium | AUD-LANG-001 | docs/07-reference-data-policy.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |
| AUD-LANG-001-fde0672e17 | medium | AUD-LANG-001 | docs/acceptance/EP-001-INFRA.acceptance.md | Найден вероятный англоязычный пользовательский фрагмент. | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. | open |

## 10. Critical findings

- Активных critical findings нет.

## 11. Findings, требующие решения пользователя

- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1001`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1041`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1061`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1141`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1161`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1181`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1201`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1241`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1261`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1281`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1301`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1321`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1361`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1381`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1401`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1441`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1461`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1481`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1501`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1521`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1541`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1601`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1621`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1641`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1661`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1681`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1701`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1721`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1741`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1761`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1781`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1801`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1821`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1841`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1861`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1901`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1961`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-1981`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2001`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2041`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2081`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2101`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2121`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2141`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2161`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2181`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2201`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2241`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2261`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2281`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2301`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2321`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2341`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2361`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2381`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2401`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2501`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2541`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2561`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2581`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2601`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2641`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2681`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2701`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2721`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2741`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2761`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2781`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2801`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2821`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2841`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2861`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2881`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2921`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-2941`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-301`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-3041`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-3061`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-3081`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-3101`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-3121`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-3141`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-3161`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-3181`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-3261`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-3281`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-3321`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-3341`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-341`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-3421`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-3441`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-3461`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-3481`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-3501`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-3521`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-3541`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-3561`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-3601`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-361`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-3641`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-3661`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-3701`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-3761`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-3801`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-381`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-3821`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-3861`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-3881`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-3921`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-3961`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4021`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4041`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4081`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4121`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4141`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4161`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4181`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4201`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-421`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4241`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4261`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4281`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4301`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4361`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4381`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4401`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-441`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4421`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4461`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4481`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4501`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4521`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4561`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4621`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4641`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4661`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4681`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4701`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4721`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4761`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4781`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4821`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4841`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4881`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4901`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4921`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4941`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-4961`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-5021`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-5041`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-5061`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-5081`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-5141`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-5161`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-5201`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-5221`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-5261`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-5281`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-5301`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-561`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-581`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-621`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-681`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-721`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-741`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-781`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-881`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-901`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-941`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-961`: Поле answered_by установлено в Codex.
- `AUD-ACCEPT-CODEX-USER-FIELD-docs-user-action-dashboard.yml-981`: Поле answered_by установлено в Codex.

## 12. Команды проверки

```sh
make audit-codex-spec
make audit-language
make validate-audit
make audit
make validate-plan
make check
```

## 13. Что не исправлялось автоматически

- Не выполнялась массовая русификация.
- Не переписывались существующие документы вне audit-контура.
- Не менялись accepted/protected artifacts без user approval.
- Findings не закрывались как `fixed` автоматически.
