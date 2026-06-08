# Acceptance Report — EP-007-VERIFICATION-DASHBOARD

## 1. Пакет

- Execution packet: EP-007-VERIFICATION-DASHBOARD
- Статус Codex: ready_for_acceptance
- Acceptance owner: Дмитрий
- Дата подготовки: 2026-06-05

## 2. Что реализовано

- `docs/verification-dashboard.md` как человекочитаемое окно ручной проверки работоспособности.
- `docs/verification-dashboard.yml` как машинно-читаемый реестр проверочных задач.
- `scripts/generate_verification_dashboard.py`.
- `scripts/validate_verification_dashboard.py`.
- Расширение `scripts/validate_project_plan.py` для проверки verification dashboard.
- Команды `make generate-verification-dashboard` и `make validate-verification`.
- Связь verification dashboard с monthly test protocol и acceptance dashboard.

## 3. Источники dashboard

Verification dashboard агрегирует:

- `docs/grace/verification-plan.xml`
- `docs/monthly/2026-06/03-test-protocol-reference-data-governance.md`
- `docs/acceptance-dashboard.yml`
- `docs/artifact-registry.yml`

## 4. Проверочные задачи

- `VT-EP-004-001..004`: project planning and acceptance contour checks.
- `VT-EP-005-001..004`: acceptance and user action dashboard checks.
- `VT-EP-006-001..006`: monthly plan, БФТ, ТЗ, and protocol checks.
- `VT-EP-007-001..005`: verification dashboard checks.

## 5. Команды проверки

```sh
make generate-verification-dashboard
make validate-verification
make generate-dashboards
make validate-plan
make check
make validate-reference
source .venv/bin/activate && python -m pytest
```

## 6. Критерии приемки

| ID | Критерий | Статус Codex | Статус пользователя |
|---|---|---|---|
| AC-EP-007-001 | создан verification-dashboard.md. | ready_for_acceptance | pending |
| AC-EP-007-002 | создан verification-dashboard.yml. | ready_for_acceptance | pending |
| AC-EP-007-003 | verification dashboard содержит проверки из протокола тестирования. | ready_for_acceptance | pending |
| AC-EP-007-004 | каждая проверка имеет инструкцию how_to_check. | ready_for_acceptance | pending |
| AC-EP-007-005 | каждая проверка имеет expected_result. | ready_for_acceptance | pending |
| AC-EP-007-006 | manual checks не могут быть отмечены Codex как passed. | ready_for_acceptance | pending |
| AC-EP-007-007 | checked_by не может быть Codex. | ready_for_acceptance | pending |
| AC-EP-007-008 | добавлена команда make generate-verification-dashboard. | ready_for_acceptance | pending |
| AC-EP-007-009 | добавлена команда make validate-verification. | ready_for_acceptance | pending |
| AC-EP-007-010 | verification dashboard связан с acceptance dashboard и monthly test protocol. | ready_for_acceptance | pending |

## 7. Что нужно проверить пользователю

- Открыть `docs/verification-dashboard.md` и проверить полноту чек-листа.
- Открыть `docs/verification-dashboard.yml` и убедиться, что ручные проверки не отмечены Codex.
- Сверить `VT-*` checks с `docs/monthly/2026-06/03-test-protocol-reference-data-governance.md`.
- Запустить команды проверки.
- Вручную заполнить `user_result` только после фактической проверки.

## 8. Как вручную отмечать проверки выполненными

1. Найти проверку в `docs/verification-dashboard.yml`.
2. Заполнить `checked: true`.
3. Заполнить `checked_by: Дмитрий`.
4. Заполнить `checked_at: YYYY-MM-DD`.
5. Заполнить `result: passed` или `failed`.
6. Добавить `comments` при необходимости.
7. Запустить `make validate-verification`.

## 9. Почему Codex не ставит галки

Проверка работоспособности требует пользовательского подтверждения. Codex может подготовить чек-лист и выполнить автоматические команды, но не может закрывать manual checks, не может указывать `checked_by: Codex` и не может превращать проверку в acceptance decision.

## 10. Блокеры

- Docker Desktop установлен. Docker-зависимые проверки больше не пропускаются по причине отсутствия Docker; общая проверка `make check` выполнена успешно.
- User manual verification remains pending until Дмитрий fills `user_result`.

## 11. Риски

- Verification dashboard must be regenerated after changes to monthly protocol, verification plan, acceptance dashboard, project plan, or verification scripts.
- Passing verification checks does not mean packet acceptance; acceptance remains a separate user decision.

## 12. Решение пользователя

acceptance_decision: pending
accepted_by:
accepted_at:
comments:
