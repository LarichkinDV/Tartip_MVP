# Протокол испытаний контура reference intake

## 1. Общие сведения

Протокол проверяет структуру контура reference intake, наличие manifest-файлов, работу валидатора и соблюдение запретов. Ручное решение о принятии источника заполняется пользователем; Codex не заполняет accepted_by, accepted_at, checked_by, checked_at и result: passed.

## 2. Объект испытаний

Объект испытаний — documentation-first/schema-first контур учета и проверки нормативно-справочных источников.

## 3. Проверяемые артефакты

- `docs/reference-intake/README.md`;
- `docs/reference-intake/source-intake-policy.md`;
- `docs/reference-intake/source-authority-model.md`;
- `docs/reference-intake/intake-workflow.md`;
- `data/reference/manifests/intake-manifest.schema.yml`;
- `data/reference/manifests/intake-log.yml`;
- `data/reference/manifests/source-authority-catalog.yml`;
- `scripts/validate_reference_intake.py`;
- `tests/test_validate_reference_intake.py`.

## 4. Команды проверки

```sh
PYTHONPYCACHEPREFIX=/private/tmp/tartip-pycache python3 -m py_compile scripts/validate_reference_intake.py
PYTHONPYCACHEPREFIX=/private/tmp/tartip-pycache python3 -m pytest tests/test_validate_reference_intake.py
python3 scripts/validate_reference_intake.py
make verify
make check
```

## 5. Таблица испытаний

| ID | Проверка | Тип | Ожидаемый результат | User result |
|---|---|---|---|---|
| VT-EP-016-001 | Reference-intake docs существуют | automated/manual | файлы существуют и содержат границы контура | pending_user_check |
| VT-EP-016-002 | Manifest schema существует | automated | schema содержит обязательные поля и enum values | pending_user_check |
| VT-EP-016-003 | Initial manifests не содержат реальных нормативных записей | automated/manual | `sources: []`, data requirements pending | pending_user_check |
| VT-EP-016-004 | Validator проходит на текущем контуре | automated | `python3 scripts/validate_reference_intake.py` завершается успешно | pending_user_check |
| VT-EP-016-005 | Tests validator проходят | automated | pytest для `tests/test_validate_reference_intake.py` проходит | pending_user_check |
| VT-EP-016-006 | User-owned fields не заполнены Codex | manual | ручные поля остаются пустыми или pending | pending_user_check |
| VT-EP-016-007 | `make verify` проходит | automated | команда завершается успешно | pending_user_check |
| VT-EP-016-008 | `make check` проходит | automated | команда завершается успешно | pending_user_check |

## 6. Запреты

В рамках испытаний не проверяется содержание реальных нормативных источников и не принимается ни один источник.

Не создаются official KSI/GESN/FSNB records, active matching rules или customer-specific datasets.

## 7. User-owned поля

```yaml
manual_verification:
  result: pending_user_check
  checked_by:
  checked_at:
  comments:
```
