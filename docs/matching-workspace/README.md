# Evidence-Gated Matching Workspace

Этот каталог описывает первый schema-first и documentation-first контур сопоставления данных ЦИМ с видами работ для одного draft-only сценария.

MVP-элемент: кирпичная армированная перегородка 120 мм.

EP-025 не создает backend runtime, web UI, database tables, active matching rules или нормативный справочник. Все официальные classifier/normative fields остаются пустыми до предоставления источника, checksum, authority, review и пользовательского решения.

## Цепочка

```text
ЦИМ-группа / BIM-группа
-> свойства элемента
-> КСИ результата
-> расчетная единица
-> вид работ
-> кандидатная норма
-> evidence slots
-> ВОР / WorkQuantity
-> WorkPackage
-> ScheduleTask
-> ActualRecord
-> PlanFactComparison
-> ControlDecision
```

## Evidence Gate

Каждое потенциально официальное поле должно иметь:

- `requires_official_source: true`;
- `value: null`, если источник отсутствует;
- `question_id`;
- `review_status: pending_user_input`;
- `activation_allowed: false`.

No source — no rule. LLM-generated content не является evidence.

## Draft-Only Status

Базовый сценарий использует:

```yaml
status: draft_requires_data
normative_status: not_active
evidence_status: missing_official_sources
activation_allowed: false
```

## Границы

ЦИМ-элемент не равен строительной работе. Фактические записи связываются с `WorkPackage` / zone / захваткой, а календарные задачи создаются через `WorkPackage`.
