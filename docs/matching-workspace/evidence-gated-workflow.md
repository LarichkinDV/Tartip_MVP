# Evidence-Gated Workflow

Workflow нужен для безопасной подготовки draft workspace до появления official или project-authorized evidence.

## Этапы

1. Создать ЦИМ-группу и список свойств элемента.
2. Сформировать draft candidate для classifier layer без выбора нормы.
3. Сформировать calculation unit candidate как template, а не контейнер факта.
4. Сформировать draft work type candidate.
5. Добавить candidate norm placeholder без кода и без состава работ.
6. Создать evidence slots для каждого отсутствующего official field.
7. Сформировать WorkQuantity как проектную величину.
8. Сгруппировать WorkQuantity в WorkPackage.
9. Связать ScheduleTask с WorkPackage.
10. Связать ActualRecord с WorkPackage / zone / захваткой.
11. Выполнить PlanFactComparison на основе plan source и fact source.
12. Сформировать ControlDecision со статусом `requires_review`.

## Activation Gate

Workspace не может быть активирован, если:

- есть missing official sources;
- есть pending evidence slots;
- official classifier/normative fields не имеют accepted source review;
- любой source имеет `source_origin: llm_generated`;
- user decision пытается подтвердить official classifier/normative field.

## Result

Выход EP-025 — проверяемый draft workspace и validator. Нормативное сопоставление не включается.
