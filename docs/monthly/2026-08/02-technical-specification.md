# ТЗ: Data Contribution And Anonymization Layer

## 1. Scope

EP-024 создает локальный schema-first контур для future data contribution. Реализация ограничена YAML-схемами, synthetic examples, документацией и validator.

## 2. Схемы

- `data-contribution-consent.schema.yml` фиксирует default-off flags и user-owned approval model.
- `raw-purchase-event.schema.yml` описывает synthetic raw event без future external rights.
- `anonymized-purchase-signal.schema.yml` описывает generalized signal без restricted identifiers.
- `commercial-price-aggregate.schema.yml` описывает aggregate thresholds.

## 3. Validator

`scripts/validate_data_contribution.py` должен проверять:

- default-off flags;
- запрет commercial use для raw event с customer references;
- запрет AI training для raw event с supplier references;
- запрет external upload для raw event;
- отсутствие restricted fields в anonymized signal;
- минимальные aggregate thresholds;
- `reidentification_risk: low`;
- запрет exact values в commercial aggregate.

## 4. Integration

Makefile target `validate-data-contribution` подключается к `make verify` и `make check`.

## 5. Non-Goals

Не создаются API, БД-таблицы, external connectors, telemetry hooks, active datasets, active matching rules или real normative imports.
