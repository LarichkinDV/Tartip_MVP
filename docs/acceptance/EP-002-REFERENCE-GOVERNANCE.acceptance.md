# Acceptance Report — EP-002-REFERENCE-GOVERNANCE

## 1. Пакет

- Execution packet: EP-002-REFERENCE-GOVERNANCE
- Статус Codex: ready_for_acceptance
- Acceptance owner: Дмитрий
- Дата подготовки: 2026-06-05

## 2. Что реализовано

- Reference data lifecycle folders.
- Source manifest and import log.
- Question registries.
- `No source — no rule` policy.
- Validation script for reference evidence gates.

## 3. Артефакты для проверки

| Артефакт | Назначение | Что проверить |
|---|---|---|
| `docs/07-reference-data-policy.md` | Policy | LLM-generated evidence is forbidden. |
| `data/reference/manifests/source-manifest.yml` | Source registry | Allowed origins and authorities are present. |
| `data/questions/*.yml` | Structured questions | Missing sources are represented as open questions. |
| `scripts/validate_reference_sources.py` | Validation | `make validate-reference` passes. |

## 4. Команды проверки

```sh
make validate-reference
make generate-data-questions
```

## 5. Критерии приемки

| ID | Критерий | Статус Codex | Статус пользователя |
|---|---|---|---|
| AC-EP-002-001 | Reference governance folders exist. | ready_for_acceptance | pending |
| AC-EP-002-002 | Source manifest exists. | ready_for_acceptance | pending |
| AC-EP-002-003 | LLM-generated evidence is rejected. | ready_for_acceptance | pending |
| AC-EP-002-004 | Missing evidence blocks active rules. | ready_for_acceptance | pending |

## 6. Что нужно проверить пользователю

- Confirm that no real KSI/FSNB/GESN values were invented.
- Provide official local sources when ready.

## 7. Блокеры


## 8. Риски

- Конкретные правила сопоставления не могут переводиться в активный статус до загрузки, регистрации и проверки официальных источников с версией, происхождением и контрольной суммой.
- Официальные локальные источники КСИ/ФСНБ/ГЭСН пока отсутствуют; это ограничивает разработку активных правил сопоставления, но не блокирует приемку контура reference governance.

## 9. Спорные решения

- None.

## 10. Решение пользователя

acceptance_decision: accepted
accepted_by: Дмитрий
accepted_at: 2026-06-08
comments: Принято. Контур управления справочными данными реализован. Проверка make validate-reference выполнена успешно: Reference source validation passed. Команда make generate-data-questions выполнена успешно, новых вопросов не добавлено. Принцип No source — no rule принят: Codex не должен придумывать КСИ, ФСНБ, ГЭСН, единицы измерения, состав работ или нормативные значения. Отсутствие официальных локальных источников не блокирует приемку EP-002, но блокирует перевод конкретных правил сопоставления в активный статус до загрузки и регистрации источников.
