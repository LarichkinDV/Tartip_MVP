# Workflow добровольного data contribution

Workflow описывает будущий порядок обработки, но не включает runtime collection.

## Основная цепочка

```text
Raw customer data
-> consent check
-> field classification
-> removal of forbidden fields
-> pseudonymization
-> generalization
-> aggregation
-> re-identification risk check
-> dataset approval
-> aggregate candidate / AI training signal candidate
```

## Правила допуска

1. Product use не считается согласием на data contribution.
2. Raw customer data остается в локальном customer contour, пока нет отдельного approval.
3. Raw event с customer_ref или customer_name не может получить `commercial_use_allowed: true`.
4. Raw event с supplier_ref или supplier_name не может получить `ai_training_allowed: true`.
5. `external_upload_enabled` для raw event должен оставаться `false`.
6. Anonymized signal не должен содержать customer-specific identifiers.
7. Commercial aggregate допускается только после aggregation, low re-identification risk и explicit approval.
8. AI training signal candidate остается отдельным будущим типом и не включается в EP-024.

## Source Status

Допустимые безопасные состояния для текущего пакета:

- `synthetic`;
- `approved_aggregate`.

Все реальные источники, tenant-specific values и customer-owned fields остаются out of scope.

## Review Gates

Каждый будущий workflow должен иметь:

- consent source;
- source checksum;
- field classification report;
- anonymization log;
- aggregation proof;
- re-identification risk result;
- approval decision;
- rollback note.
