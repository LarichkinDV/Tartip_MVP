# Anonymization Pipeline

Pipeline описывает минимальный порядок подготовки signal data. Он не является юридическим заключением и не заменяет review специалистом.

## Этапы

1. `consent check` — подтверждается, что data contribution явно разрешен.
2. `field classification` — поля делятся на operational, restricted, pseudonymous, generalized и aggregate-safe.
3. `removal of forbidden fields` — customer-specific identifiers и прямые supplier-specific identifiers удаляются до публикации signal.
4. `pseudonymization` — внутренние references заменяются transient pseudonyms, если они нужны для промежуточной обработки.
5. `generalization` — точные значения заменяются buckets: period, material class, size bucket, zone bucket.
6. `aggregation` — записи объединяются так, чтобы не раскрывать отдельную сделку или участника.
7. `re-identification risk check` — результат должен быть `low`.
8. `dataset approval` — отдельное пользовательское approval перед future use.

## Минимальные пороги aggregation

Commercial aggregate должен иметь:

- `observations_count >= 10`;
- `independent_customers_count >= 5`;
- `independent_suppliers_count >= 5`;
- `reidentification_risk: low`;
- `aggregate_approved: true`.

## Запреты текущего пакета

EP-024 не разрешает future use сам по себе. Он только фиксирует схемы, примеры и local validator. Любая обработка реальных customer data требует отдельного packet, отдельного approval и юридической проверки.
