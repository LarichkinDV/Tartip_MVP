# Re-Identification Risk Policy

Цель policy — не допустить публикацию или повторное использование signal, если по нему можно восстановить отдельного участника или сделку.

## Risk Levels

- `low` — aggregate содержит достаточное число независимых observations и участников, exact values заменены buckets.
- `medium` — есть признаки узкого среза, редкой позиции или малого числа независимых участников.
- `high` — aggregate может раскрыть отдельную сделку, участника или tenant-specific pattern.
- `blocked` — signal содержит restricted fields или не имеет approval path.

## Gate

Для commercial aggregate допустим только `reidentification_risk: low`.

## Запрещенные признаки aggregate

Commercial aggregate не должен содержать:

- exact day;
- exact settlement;
- contact attributes;
- customer-specific references;
- supplier-specific references;
- invoice-like or contract-like identifiers;
- free-text fields from source systems.

## Manual Review

Если validator не может доказать safe aggregate по структуре, результат остается `requires_user_approval` или `blocked`. Codex не может закрывать такой gate самостоятельно.
