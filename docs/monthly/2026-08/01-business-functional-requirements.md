# БФТ: Контур добровольной передачи обезличенных и агрегированных данных

## 1. Назначение

Документ описывает бизнес-функциональные требования к будущему контуру data contribution в Tartip. В рамках EP-024 создаются только документы, схемы, synthetic examples и validator.

## 2. Пользовательская ценность

Контур должен заранее объяснять заказчику, какие данные могут быть рассмотрены как raw, какие должны быть удалены или обобщены, и какие aggregate candidates могут быть предложены для будущей аналитики после отдельного approval.

## 3. Функциональные границы

- Product use не является согласием на data contribution.
- Все default-off flags остаются `false`.
- Raw customer data не используется для commercial aggregate.
- AI training signal candidate не создается из customer data в текущем scope.
- Любой future use требует отдельного user decision, legal review и audit trail.

## 4. Минимальные сценарии

1. Пользователь видит, что data contribution выключен.
2. Система классифицирует поля как restricted, pseudonymous, generalized или aggregate-safe.
3. Restricted fields удаляются до signal stage.
4. Aggregate проходит пороги по observations и independent participants.
5. Re-identification risk должен быть `low`.
6. Dataset approval хранится как user-owned decision.

## 5. Что не реализуется

EP-024 не включает runtime collection, external upload, customer data reuse, real dataset import, commercial dataset delivery или normative matching.
