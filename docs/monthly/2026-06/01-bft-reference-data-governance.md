# БФТ — Reference Data Governance

Дата: 2026-06-05

## Назначение

Зафиксировать базовые функциональные требования к проверяемому контуру reference data governance без ввода реальных нормативных баз и без изменения доменной методики BIM-КСИ-ГЭСН.

## Границы

- Проверяется локальная дисциплина `No source — no rule`.
- Проверяются source manifests, question registries, draft matching rule gates и dashboard-контуры.
- Не проверяется импорт реальных КСИ, ФСНБ, ГЭСН или нормативных значений.
- Не выполняется приемка результата; приемка остается в `docs/acceptance-dashboard.md` и acceptance reports.

## Функциональные ожидания

- Проект должен показывать отсутствующие источники как вопросы к пользователю.
- Draft matching rules не должны становиться active без evidence.
- Пользовательские решения не должны подтверждать официальные нормативные поля.
- Ручные проверки должны фиксироваться отдельно от acceptance decision.

## Связанные артефакты

- `docs/monthly/monthly-plan.yml`
- `docs/monthly/2026-06/03-test-protocol-reference-data-governance.md`
- `docs/verification-dashboard.md`

