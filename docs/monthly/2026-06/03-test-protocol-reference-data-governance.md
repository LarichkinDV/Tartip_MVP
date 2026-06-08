# Протокол тестирования — Reference Data Governance

Дата: 2026-06-05

## Назначение

Протокол описывает ручные и командные проверки работоспособности проектного контура reference data governance, acceptance dashboards, monthly artifacts и verification dashboard.

Проверка работоспособности не равна приемке результата. Приемка выполняется отдельно через `docs/acceptance-dashboard.md` и packet acceptance reports.

## Окно ручной проверки

Детальное окно ручной проверки работоспособности функционала ведется в:

- `docs/verification-dashboard.md`
- `docs/verification-dashboard.yml`

## Проверочные задачи

| Check ID | Что проверяется | Источник |
|---|---|---|
| VT-EP-004-001 | Наличие `docs/project-plan.md` | EP-004 |
| VT-EP-004-002 | Наличие `docs/artifact-registry.yml` | EP-004 |
| VT-EP-004-003 | Запрет `accepted_by=Codex` | EP-004 |
| VT-EP-004-004 | Прохождение `make validate-plan` | EP-004 |
| VT-EP-005-001 | Генерация acceptance dashboard | EP-005 |
| VT-EP-005-002 | Генерация user action dashboard | EP-005 |
| VT-EP-005-003 | Accepted artifacts отображаются как protected | EP-005 |
| VT-EP-005-004 | Open questions отображаются в user action dashboard | EP-005 |
| VT-EP-006-001 | Наличие `monthly-plan.yml` | EP-006 |
| VT-EP-006-002 | Ровно 3 месячные задачи | EP-006 |
| VT-EP-006-003 | Каждая задача имеет 15 человеко-часов | EP-006 |
| VT-EP-006-004 | Наличие БФТ | EP-006 |
| VT-EP-006-005 | Наличие ТЗ | EP-006 |
| VT-EP-006-006 | Наличие протокола тестирования | EP-006 |
| VT-EP-007-001 | Наличие `verification-dashboard.md` | EP-007 |
| VT-EP-007-002 | Наличие `verification-dashboard.yml` | EP-007 |
| VT-EP-007-003 | Manual checks не отмечены Codex как passed | EP-007 |
| VT-EP-007-004 | `checked_by` не может быть `Codex` | EP-007 |
| VT-EP-007-005 | Verification dashboard связан с протоколом тестирования | EP-007 |

## Команды

```sh
make generate-verification-dashboard
make validate-verification
make generate-dashboards
make validate-plan
make check
```

## Правила ручной фиксации

- Codex не отмечает ручные проверки выполненными.
- Пользователь заполняет `checked_by`, `checked_at`, `result` и `comments` в `docs/verification-dashboard.yml` вручную.
- `checked_by` не может быть `Codex`.

