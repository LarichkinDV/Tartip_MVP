# БФТ: Контур сопоставления данных ЦИМ с видами работ

## 1. Назначение

Документ описывает бизнес-функциональные требования к draft workspace для проверки цепочки от группы ЦИМ до контрольного решения.

## 2. Пользовательская ценность

Контур должен показать руководителю и Заказчику, где именно нужны official sources, какие decisions остаются user-owned и почему draft не превращается в активное нормативное сопоставление без evidence.

## 3. MVP Scenario

MVP-элемент: кирпичная армированная перегородка 120 мм.

Сценарий является synthetic и draft-only. Все official classifier/normative fields остаются пустыми до предоставления source evidence.

## 4. Функциональные требования

- Workspace показывает свойства элемента и draft grouping.
- Workspace показывает calculation unit candidate как template.
- Workspace показывает candidate work type без нормативного подтверждения.
- Workspace создает evidence slots для missing official fields.
- WorkQuantity агрегируется в WorkPackage.
- ScheduleTask использует WorkPackage.
- ActualRecord использует WorkPackage / zone context.
- PlanFactComparison формирует `requires_review`.
- ControlDecision остается `requires_review`, пока evidence missing.

## 5. Non-Goals

Не реализуются runtime, web UI, database tables, active matching rules, real normative sources, production deployment или customer-specific datasets.
