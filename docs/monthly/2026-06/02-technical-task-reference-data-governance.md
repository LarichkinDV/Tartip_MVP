# ТЗ — Reference Data Governance Verification

Дата: 2026-06-05

## Цель

Подготовить проверочный контур для ручного подтверждения работоспособности reference data governance без веб-интерфейса, backend endpoints и frontend routes.

## Требования

- Создать машинно-читаемый и человекочитаемый verification dashboard.
- Связать verification dashboard с monthly test protocol.
- Проверять, что manual checks не закрываются Codex.
- Проверять, что `checked_by` не может быть `Codex`.
- Сохранять разделение: проверка работоспособности не равна приемке результата.

## Ограничения

- Не создавать прямую связь `ModelElement -> GESNNorm`.
- Не выбирать ГЭСН через КСИ.
- Не добавлять реальные нормативные базы.
- Не заполнять пользовательские поля проверки от имени Codex.

## Ожидаемый результат

- `docs/verification-dashboard.md`
- `docs/verification-dashboard.yml`
- `scripts/generate_verification_dashboard.py`
- `scripts/validate_verification_dashboard.py`

