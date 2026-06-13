# Commercial Aggregate Policy

Commercial aggregate в текущем пакете допускается только как synthetic example или future approved aggregate. EP-024 не создает коммерческий dataset и не разрешает использовать реальные customer data.

## Условия допуска

Aggregate может иметь `commercial_use_allowed: true` только если одновременно выполнено:

- `data_classification: synthetic_aggregate_example`;
- `aggregate_approved: true`;
- `source_status` равен `synthetic` или `approved_aggregate`;
- `derived_from_real_customer_data: false`;
- `observations_count >= 10`;
- `independent_customers_count >= 5`;
- `independent_suppliers_count >= 5`;
- `reidentification_risk: low`.

## Что не считается approval

Не являются approval:

- установка продукта;
- локальный запуск;
- импорт пользовательского файла;
- просмотр отчета;
- заполнение рабочей формы без явного dataset decision.

## Future Work

Будущий packet должен отдельно описать consent UX, журнал решений, protected artifact change request, legal review и технический механизм rollback.
