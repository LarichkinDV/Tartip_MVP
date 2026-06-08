# Acceptance Report — EP-005-ACCEPTANCE-AND-USER-ACTION-DASHBOARDS

## 1. Пакет

- Execution packet: EP-005-ACCEPTANCE-AND-USER-ACTION-DASHBOARDS
- Статус Codex: ready_for_acceptance
- Acceptance owner: Дмитрий
- Дата подготовки: 2026-06-05

## 2. Что реализовано

- `docs/acceptance-dashboard.md` как единое окно приемки.
- `docs/acceptance-dashboard.yml` как машинно-читаемый источник dashboard state.
- `docs/user-action-dashboard.md` как единое окно вопросов и действий пользователя.
- `docs/user-action-dashboard.yml` как машинно-читаемый список user actions.
- `scripts/generate_acceptance_dashboard.py`.
- `scripts/generate_user_action_dashboard.py`.
- Расширенные проверки dashboard и accepted artifact protection в `scripts/validate_project_plan.py`.
- Команды генерации dashboard в `Makefile`.
- Правила `Dashboard discipline` и `Accepted artifact protection` в `AGENTS.md`.

## 3. Источники dashboard

Acceptance dashboard агрегирует:

- `docs/grace/execution-packets.xml`
- `docs/artifact-registry.yml`
- `docs/acceptance/*.acceptance.md`
- `docs/status-report.md`

User action dashboard агрегирует:

- `data/questions/data-requirements.yml`
- `data/questions/unresolved-mapping-questions.yml`
- `data/questions/normative-review-questions.yml`
- `data/questions/project-decisions.yml`
- `data/questions/import-issues.yml`

## 4. Команды проверки

```sh
make generate-dashboards
make validate-plan
make check
make validate-reference
source .venv/bin/activate && python -m pytest
```

## 5. Критерии приемки

| ID | Критерий | Статус Codex | Статус пользователя |
|---|---|---|---|
| AC-EP-005-001 | создан acceptance-dashboard.md. | ready_for_acceptance | pending |
| AC-EP-005-002 | создан acceptance-dashboard.yml. | ready_for_acceptance | pending |
| AC-EP-005-003 | создан user-action-dashboard.md. | ready_for_acceptance | pending |
| AC-EP-005-004 | создан user-action-dashboard.yml. | ready_for_acceptance | pending |
| AC-EP-005-005 | ready_for_acceptance packets отражаются в acceptance dashboard. | ready_for_acceptance | pending |
| AC-EP-005-006 | open questions отражаются в user action dashboard. | ready_for_acceptance | pending |
| AC-EP-005-007 | Codex не может поставить accepted. | ready_for_acceptance | pending |
| AC-EP-005-008 | accepted_by / decided_by не может быть Codex. | ready_for_acceptance | pending |
| AC-EP-005-009 | добавлены команды генерации dashboards в Makefile. | ready_for_acceptance | pending |
| AC-EP-005-010 | validate_project_plan.py проверяет dashboards. | ready_for_acceptance | pending |
| AC-EP-005-011 | accepted artifacts отображаются как protected. | ready_for_acceptance | pending |
| AC-EP-005-012 | protected accepted artifacts нельзя изменять без user approval. | ready_for_acceptance | pending |
| AC-EP-005-013 | если требуется изменение accepted artifact, создается requires_user_approval action или change request. | ready_for_acceptance | pending |

## 6. Что нужно проверить пользователю

- Открыть `docs/acceptance-dashboard.md` и убедиться, что пакеты `ready_for_acceptance` видны в одном окне.
- Открыть `docs/user-action-dashboard.md` и проверить, что открытые вопросы пользователя видны как действия.
- Убедиться, что dashboard не заменяют детальные acceptance reports и source question files.
- Проверить, что пользовательские поля решения остаются пустыми или pending, если решение еще не принято.
- Убедиться, что `accepted_by` и `decided_by` не заполнены значением `Codex`.

## 7. Блокеры

- Docker Desktop установлен. Docker-зависимые проверки больше не пропускаются по причине отсутствия Docker; общая проверка `make check` выполнена успешно.
- User acceptance decision remains pending until Дмитрий reviews the packet.

## 8. Риски

- Dashboard files are generated from source files and must be regenerated after future packet or question updates.
- If source files and dashboards diverge, validation must fail or mark the state as requiring review.
- Accepted artifacts must not be materially changed without a separate user approval workflow.

## 9. Защита accepted artifacts

Accepted artifacts are protected when at least one source marks them as accepted or locked. Codex must not delete, rename, overwrite, or materially modify those artifacts without explicit user approval.

If an accepted artifact requires a change:

1. Do not change the artifact directly.
2. Create a change request or `requires_user_approval` action.
3. Describe the reason, impact, affected downstream artifacts, and compatibility.
4. Request user approval.
5. Prefer a new revision over overwriting the accepted artifact.
6. Run repeat acceptance after the approved change.

## 10. Спорные решения

- Dashboards are documentation artifacts, not web UI, frontend pages, or backend endpoints.
- Dashboard state is derived from source files; user decisions remain in acceptance reports and question registries.
- No accepted artifacts were detected during EP-005 preparation, so no new `protection.locked=true` entries were added.

## 11. Решение пользователя

acceptance_decision: pending
accepted_by:
accepted_at:
comments:
