# Контур data contribution

Этот каталог описывает schema-first и documentation-first контур добровольной передачи, обезличивания, обобщения и агрегации данных для будущих аналитических сценариев Tartip.

EP-024 не включает сбор реальных данных, telemetry, внешний upload, commercial use или AI-training. Все такие возможности остаются выключенными по умолчанию и требуют отдельного пользовательского approval, legal review и проверяемого workflow.

## Назначение

Контур нужен, чтобы заранее определить безопасные границы между:

- raw customer data;
- consent check;
- field classification;
- removal of forbidden fields;
- pseudonymization;
- generalization;
- aggregation;
- re-identification risk check;
- dataset approval;
- aggregate candidate;
- AI training signal candidate.

## Default-Off Flags

```yaml
telemetry_enabled: false
dataset_contribution_enabled: false
external_upload_enabled: false
ai_training_allowed: false
commercial_use_allowed: false
```

Использование продукта не является согласием на data transfer. Любой будущий workflow должен проверять явное решение пользователя до обработки customer data вне локального контура.

## Артефакты

- [data-contribution-workflow.md](data-contribution-workflow.md) — lifecycle от raw data до approved aggregate candidate.
- [anonymization-pipeline.md](anonymization-pipeline.md) — этапы удаления, pseudonymization, generalization и aggregation.
- [reidentification-risk-policy.md](reidentification-risk-policy.md) — policy оценки re-identification risk.
- [commercial-aggregate-policy.md](commercial-aggregate-policy.md) — условия для synthetic/approved aggregate.
- [schemas/data-contribution](../../schemas/data-contribution) — YAML-схемы для consent, raw event, anonymized signal и aggregate.
- [examples/data-contribution](../../examples/data-contribution) — только synthetic examples.

## Границы EP-024

EP-024 не меняет BIM-КСИ-ГЭСН методику, не создает active matching rules и не подключает внешние базы. Созданные схемы описывают будущий governance-контур и валидируются локально.
