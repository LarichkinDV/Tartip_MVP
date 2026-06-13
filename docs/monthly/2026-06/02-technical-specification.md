# Техническое задание на разработку инфраструктурного контура прикладного прототипа ТАРТИП

## 1. Общие сведения

Настоящий документ определяет требования к инфраструктурному контуру подготовки, проверки и приемки артефактов прикладного прототипа. Документ не является утвержденным техническим заданием на промышленную эксплуатацию и подлежит уточнению перед началом договорной разработки.

Документ относится к первому месяцу работ и описывает только инфраструктурный контур.

## 2. Назначение и цели разработки

Назначение контура — обеспечить управляемую локальную основу для дальнейшей разработки прикладного прототипа ТАРТИП.

Цели:

- подготовить структуру репозитория и проверочные команды;
- обеспечить регистрацию артефактов и execution packets;
- обеспечить контролируемую приемку результатов пользователем;
- сохранить разделение source-of-truth, generated files и protected artifacts;
- подготовить основу для следующих контуров учета источников, сопоставления, фактического учета и план-фактного контроля.

## 3. Характеристика объекта автоматизации

Объект автоматизации — процесс подготовки и проверки локальных проектных артефактов для прикладного прототипа BIM5D cost-schedule matching.

Контур не автоматизирует промышленную эксплуатацию, не импортирует реальные нормативные базы и не выполняет активное нормативное сопоставление.

## 4. Состав инфраструктурного контура

В состав входят:

- структура backend/frontend/infrastructure проекта;
- Makefile-команды проверки;
- GRACE execution packets, module contracts и verification plan;
- artifact registry, project-state, project plan, status report и traceability matrix;
- acceptance reports;
- generated dashboards/workbench;
- validators для project plan, post-acceptance state, protected artifacts, monthly planning и legal/data boundary notes.

## 5. Требования к системе

Система должна:

1. работать в local-first режиме;
2. поддерживать воспроизводимые проверки через `make verify` и `make check`;
3. показывать текущий execution packet через `docs/project-state.yml`;
4. не принимать execution packets от имени Codex;
5. сохранять accepted reports как исторические записи;
6. не смешивать generated dashboards с source-of-truth files.

## 6. Требования к данным

Для первого месяца допускаются только служебные проектные данные и synthetic examples.

Для примеров должен применяться режим:

```yaml
data_classification: synthetic_example_only
source_status: synthetic
commercial_use_allowed: false
ai_training_allowed: false
```

Реальные сведения работодателя или Заказчика, реальные нормативные базы, customer-specific mapping tables и конфиденциальные материалы не добавляются.

## 7. Требования к защите accepted artifacts

Accepted source/manual artifacts должны быть защищены в `docs/artifact-registry.yml`.

Изменение protected artifacts допускается только через explicit user approval или approved protected artifact change request. Generated dashboards остаются derived artifacts и могут регенерироваться штатными генераторами.

## 8. Требования к проверкам

Контур должен проходить:

- `make verify`;
- `make check`;
- проверки отсутствия запрещенных customer-facing терминов в месячных документах;
- проверки отсутствия реальных customer/employer data;
- проверки user-owned fields.

## 9. Требования к ограничениям

Запрещено:

- создавать промышленную версию продукта;
- импортировать реальные КСИ, ФСНБ или ГЭСН источники;
- создавать active matching rules без evidence;
- вводить прямую связь `ModelElement -> GESNNorm`;
- создавать `ScheduleTask` по каждой норме ГЭСН;
- автоматически использовать данные Заказчика за пределами локального контура;
- создавать DOCX/PDF без отдельной команды пользователя.

## 10. Состав работ первого месяца

Первый месяц включает:

1. инфраструктуру репозитория и контур разработки;
2. контур управления артефактами, приемкой и проверками;
3. контур верификации, аудита и compact working context;
4. customer-facing roadmap и monthly planning;
5. legal/data boundary policy notes;
6. итоговые БФТ, ТЗ, протокол испытаний и presentation outline.

## 11. Порядок контроля и приемки

Codex готовит документы и запускает проверки.

Пользователь вручную проверяет результаты, при необходимости возвращает пакет на доработку и только затем заполняет user-owned acceptance fields.

Codex не заполняет `accepted_by`, `accepted_at`, `checked_by`, `checked_at`, `answered_by`, `decided_by` и не ставит `acceptance_decision: accepted`.

## 12. Требования к документации

Документация должна быть написана на русском языке там, где это возможно.

Технические идентификаторы, команды, пути, enum-статусы, YAML/XML keys и названия классов допускается оставлять на английском.

## 13. Приложение: связь требований с EP и артефактами

| Область | Execution packets | Артефакты |
|---|---|---|
| Инфраструктура | EP-001, EP-011, EP-021 | `Makefile`, backend/frontend skeleton, sync automation |
| Приемка и governance | EP-004, EP-005, EP-012, EP-013, EP-014, EP-018 | `docs/project-state.yml`, dashboards, workbench, artifact registry |
| Проверки и аудит | EP-007, EP-009, EP-015, EP-017, EP-019 | verification dashboard, audit reports, compact context |
| Месячная рамка | EP-022A, EP-022B, EP-023 | roadmap, monthly plan, legal/data boundary notes, BFT, TZ, test protocol |

