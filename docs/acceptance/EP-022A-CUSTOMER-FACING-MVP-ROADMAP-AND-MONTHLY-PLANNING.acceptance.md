# Acceptance Report — EP-022A-CUSTOMER-FACING-MVP-ROADMAP-AND-MONTHLY-PLANNING

## 1. Сводка

- Execution packet: EP-022A-CUSTOMER-FACING-MVP-ROADMAP-AND-MONTHLY-PLANNING
- Статус Codex: ready_for_acceptance
- Владелец приемки: Дмитрий
- Дата подготовки: 2026-06-13

EP-022A создает безопасную customer-facing рамку и структуру месячного планирования для прикладного прототипа ТАРТИП.
Пакет не реализует функциональность продукта, не создает legal/data policy notes, не создает data contribution layer и не меняет BIM-КСИ-ГЭСН методику.

## 2. Planning Override

Пользователь временно отложил EP-016 и запустил EP-022A для подготовки customer-facing/monthly planning рамки перед созданием документов для руководителя/Заказчика.

Planning override зафиксирован только во внутренних governance-файлах:

- `docs/acceptance/EP-022A-CUSTOMER-FACING-MVP-ROADMAP-AND-MONTHLY-PLANNING.acceptance.md`;
- `docs/status-report.md`;
- `docs/project-plan.md`;
- `docs/project-state.yml`.

Planning override не размещен в `docs/roadmap/2026-customer-facing-mvp-roadmap.md`.

## 3. Область изменений

- Создан `docs/monthly/README.md`.
- Создан `docs/roadmap/2026-customer-facing-mvp-roadmap.md`.
- Создан `docs/monthly/2026-06/monthly-plan.yml`.
- Создан `scripts/validate_monthly_planning.py`.
- Создан `tests/test_validate_monthly_planning.py`.
- Добавлен `validate-monthly-planning` в `Makefile`, `make verify` и `make check`.
- EP-022A зарегистрирован в `docs/grace/execution-packets.xml`.
- Добавлены verification scenarios `V-MONTHLY-PLANNING-001..006`.
- Обновлены `docs/project-state.yml`, `docs/project-plan.md`, `docs/status-report.md`, `docs/traceability-matrix.md` и `docs/artifact-registry.yml`.
- Dashboards/workbench могут быть регенерированы штатными генераторами через `make check`.

## 4. Артефакты

| Артефакт | Тип | Статус |
|---|---|---|
| `docs/monthly/README.md` | monthly planning policy | created |
| `docs/roadmap/2026-customer-facing-mvp-roadmap.md` | customer-facing roadmap | created |
| `docs/monthly/2026-06/monthly-plan.yml` | monthly plan | created |
| `scripts/validate_monthly_planning.py` | validator | created |
| `tests/test_validate_monthly_planning.py` | tests | created |
| `docs/acceptance/EP-022A-CUSTOMER-FACING-MVP-ROADMAP-AND-MONTHLY-PLANNING.acceptance.md` | acceptance report | created |
| `docs/project-state.yml` | project state | updated |
| `docs/grace/execution-packets.xml` | execution packet registry | updated |
| `docs/grace/verification-plan.xml` | verification plan | updated |
| `docs/artifact-registry.yml` | artifact registry | updated |
| `docs/project-plan.md` | project plan | updated |
| `docs/status-report.md` | status report | updated |
| `docs/traceability-matrix.md` | traceability matrix | updated |
| `Makefile` | verification commands | updated |

## 5. Проверки

```sh
PYTHONPYCACHEPREFIX=/private/tmp/tartip-pycache python3 -m py_compile scripts/validate_monthly_planning.py
PYTHONPYCACHEPREFIX=/private/tmp/tartip-pycache python3 -m pytest tests/test_validate_monthly_planning.py
python3 scripts/validate_monthly_planning.py
grep -n "SaaS\\|DaaS\\|freemium\\|bottom-up adoption\\|open-core\\|commercial data layer" docs/roadmap/2026-customer-facing-mvp-roadmap.md || true
make verify
make check
```

Результаты:

- `PYTHONPYCACHEPREFIX=/private/tmp/tartip-pycache python3 -m py_compile scripts/validate_monthly_planning.py`: passed.
- `PYTHONPYCACHEPREFIX=/private/tmp/tartip-pycache python3 -m pytest tests/test_validate_monthly_planning.py`: blocked in system Python because `pytest` is not installed for `/Library/Developer/CommandLineTools/usr/bin/python3`.
- `PYTHONPYCACHEPREFIX=/private/tmp/tartip-pycache .venv/bin/python -m pytest tests/test_validate_monthly_planning.py`: passed, 8 tests.
- `python3 scripts/validate_monthly_planning.py`: passed.
- `grep -n "SaaS\\|DaaS\\|freemium\\|bottom-up adoption\\|open-core\\|commercial data layer" docs/roadmap/2026-customer-facing-mvp-roadmap.md || true`: no matches.
- `make verify`: passed.
- `make check`: passed.

## 6. Критерии приемки

| ID | Критерий | Статус Codex | Решение пользователя |
|---|---|---|---|
| AC-EP-022A-001 | Strict baseline совпал с ожидаемым состоянием после EP-019. | ready_for_acceptance | pending |
| AC-EP-022A-002 | Создана политика месячного планирования. | ready_for_acceptance | pending |
| AC-EP-022A-003 | Создана customer-facing дорожная карта 2026. | ready_for_acceptance | pending |
| AC-EP-022A-004 | Создан `monthly-plan.yml` для 2026-06. | ready_for_acceptance | pending |
| AC-EP-022A-005 | Создан monthly planning validator. | ready_for_acceptance | pending |
| AC-EP-022A-006 | Созданы tests monthly planning validator. | ready_for_acceptance | pending |
| AC-EP-022A-007 | Planning override перед EP-016 зафиксирован только во внутренних governance-файлах. | ready_for_acceptance | pending |
| AC-EP-022A-008 | Planning override не размещен в customer-facing roadmap. | ready_for_acceptance | pending |
| AC-EP-022A-009 | Месячные блоки названы как прикладные контуры для Заказчика. | ready_for_acceptance | pending |
| AC-EP-022A-010 | В customer-facing roadmap нет forbidden customer-facing terms. | ready_for_acceptance | pending |
| AC-EP-022A-011 | БФТ/ТЗ/протоколы определены как итоговые документы, а prompt templates — как supporting artifacts. | ready_for_acceptance | pending |
| AC-EP-022A-012 | `make verify` и `make check` проходят. | ready_for_acceptance | pending |
| AC-EP-022A-013 | README.md, CHANGELOG.md и AGENTS.md не изменены. | ready_for_acceptance | pending |
| AC-EP-022A-014 | Accepted reports других EP не изменены. | ready_for_acceptance | pending |
| AC-EP-022A-015 | BIM-КСИ-ГЭСН методика не изменена. | ready_for_acceptance | pending |
| AC-EP-022A-016 | Реальные данные работодателя/Заказчика не добавлены. | ready_for_acceptance | pending |
| AC-EP-022A-017 | User-owned fields не заполнены Codex. | ready_for_acceptance | pending |

## 7. Блокеры

## 8. Риски

## 9. User-owned решение

```yaml
acceptance_decision: accepted
accepted_by: Дмитрий
accepted_at: 2026-06-13
comments: Принято. Проверено: создана customer-facing дорожная карта 2026; создана политика месячного планирования; создан monthly-plan.yml на июнь 2026; создан валидатор monthly planning и тесты; planning override по EP-016 зафиксирован только во внутренних governance-файлах; roadmap не содержит planning override и запрещенные customer-facing формулировки; protected/manual artifacts не изменены; accepted reports других EP не изменены; реальные данные работодателя/Заказчика не добавлены; user-owned поля Codex не заполнял; make verify и make check прошли.
```

## 10. Protected Artifact Discipline

- `README.md` не изменялся.
- `CHANGELOG.md` не изменялся из-за scope/protected-artifact ограничения текущего execution packet.
- `AGENTS.md` не изменялся.
- `docs/01-methodology.md` и `docs/02-domain-model.md` не изменялись.
- Accepted reports других EP не изменялись.
- DOCX/PDF не создавались и не изменялись.

## 11. Data Safety

- Реальные данные работодателя/Заказчика не добавлялись.
- Реальные названия организаций, ИНН, КПП, ОГРН, номера договоров, цены, адреса объектов, ФИО, телефоны, email, банковские реквизиты и customer-specific mapping tables не добавлялись.
- Customer-facing roadmap описывает прикладной прототип, локальное развертывание, модульное развитие, проверяемость и трассируемость.

## 12. Следующий шаг

Пользователь проверяет customer-facing roadmap, monthly planning policy, monthly-plan.yml, результаты проверок и вручную принимает EP-022A либо возвращает пакет на доработку.
