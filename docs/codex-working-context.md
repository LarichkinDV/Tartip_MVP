# Рабочий контекст Codex

## 1. Назначение проекта

`Tartip` — local-first система BIM5D cost-schedule matching.

Система разделяет:

- BIM model elements;
- KSI classification;
- calculation units;
- GESN norm candidates;
- work quantities;
- work packages;
- schedule tasks;
- actual records;
- plan-fact comparisons;
- control decisions.

Этот файл является компактным рабочим контекстом Codex.
Он не заменяет source-of-truth files и не отменяет `AGENTS.md`.

## 2. Текущее состояние проекта

Source of truth: `docs/project-state.yml`.

В первую очередь проверять:

- `state_mode`;
- `active_execution_packet`;
- `last_accepted_execution_packet`;
- `last_completed_execution_packet`;
- `next_recommended_packet`;
- `accepted_packets`;
- `monthly_scopes`.

`docs/project-plan.md` и `docs/status-report.md` являются человекочитаемыми сводками.
Если они конфликтуют с `docs/project-state.yml`, сначала исправляется source-of-truth состояние.

## 3. Обязательные доменные инварианты

- BIM element не равен construction work.
- Запрещена прямая связь `ModelElement -> GESNNorm`.
- Запрещен прямой выбор `GESNNorm` через `KSIResultCode`.
- Запрещена прямая связь `GESNNorm -> ScheduleTask`.
- `CalculationUnit` является normative-calculation template, а не универсальным контейнером.
- `ActualRecord` преимущественно связывается через `WorkPackage` / zone.
- `ScheduleTask` создается для `WorkPackage`, а не для каждой `GESNNorm`.
- Каждый classifier, norm, matching rule и calculation unit имеет version и status.
- Неоднозначные сопоставления возвращают `requires_review`.
- No source — no rule.
- LLM-generated content не является evidence.
- Official KSI/FSNB/GESN fields требуют official или project-authorized evidence.

## 4. Дисциплина приемки

- Codex не принимает execution packets.
- Codex может подготовить `ready_for_acceptance`.
- Источник пользовательской приемки: `docs/acceptance/*.acceptance.md`.
- `acceptance_decision: accepted` является user-owned полем.
- `accepted_by`, `accepted_at`, `comments` являются user-owned полями.
- `checked_by`, `answered_by`, `decided_by` являются user-owned полями.
- User-owned fields не должны быть равны `Codex`.
- Пустые разделы blockers и risks остаются пустыми.
- Нельзя писать псевдоблокеры вроде `Нет`, `Отсутствуют`, `None`.
- Accepted reports являются историческими записями.
- Accepted packets не должны попадать в active review queues.

## 5. Дисциплина protected artifacts

- Accepted/protected artifacts требуют approved change request перед material change.
- Protected artifact requests ведутся в `docs/protected-artifact-change-requests.yml`.
- Generated dashboards являются derived artifacts, а не source-of-truth records.
- Generated files не должны изменять user-owned fields в source files.
- Historical acceptance reports не являются cleanup targets.
- Нельзя переформатировать protected source/manual artifacts без explicit approval.

## 6. Source-of-truth files

Использовать как первичные записи:

- `AGENTS.md` для agent discipline и mandatory policy.
- `docs/project-state.yml` для текущего состояния проекта.
- `docs/grace/execution-packets.xml` для packet definitions и statuses.
- `docs/grace/knowledge-graph.xml` для allowed и forbidden domain edges.
- `docs/grace/module-contracts.xml` для module contracts.
- `docs/grace/verification-plan.xml` для verification scenarios.
- `docs/artifact-registry.yml` для artifact metadata и protection classification.
- `docs/protected-artifact-change-requests.yml` для protected change approvals.
- `docs/acceptance/*.acceptance.md` для user acceptance decisions.
- `data/questions/*.yml` для user/data requirements.

## 7. Generated files

Generated files регенерируются из source files и scripts:

- `docs/acceptance-dashboard.md`;
- `docs/acceptance-dashboard.yml`;
- `docs/user-action-dashboard.md`;
- `docs/user-action-dashboard.yml`;
- `docs/user-review-workbench.md`;
- `docs/user-review-workbench.yml`;
- `docs/verification-dashboard.md`;
- `docs/verification-dashboard.yml`;
- `docs/audit/codex-spec-audit.md`;
- `docs/audit/language-audit-report.md`.

Не использовать generated files как единственное evidence, если существуют source files.

## 8. Файлы только для выборочного чтения

Не читать полностью по умолчанию:

- `docs/audit/audit-findings.yml`;
- `docs/audit/codex-spec-audit.md`;
- `docs/audit/language-audit-report.md`;
- `docs/acceptance-dashboard.yml`;
- `docs/user-action-dashboard.yml`;
- `docs/user-review-workbench.yml`;
- `docs/user-review-workbench.md`;
- `docs/verification-dashboard.yml`;
- `docs/artifact-registry.yml`.

Использовать `rg`, `sed`, `yq` или небольшие Python parsers для targeted inspection.

## 9. Что читать по типу задачи

Domain change:

- `docs/grace/knowledge-graph.xml`;
- `docs/grace/module-contracts.xml`;
- relevant rules and data files.

State или packet change:

- `docs/project-state.yml`;
- `docs/grace/execution-packets.xml`;
- target acceptance report.

Verification change:

- `docs/project-state.yml`;
- `docs/grace/verification-plan.xml`;
- `scripts/generate_verification_dashboard.py`;
- `scripts/validate_verification_dashboard.py`.

Audit или workbench change:

- current audit/workbench index;
- выборочные `rg`/`sed` из audit findings и workbench YAML;
- relevant generator и validator.

Protected artifact change:

- target entry в `docs/artifact-registry.yml`;
- `docs/protected-artifact-change-requests.yml`;
- target file только после approved CR.

## 10. Команды

Read-only verification:

```sh
make verify
```

Writing regeneration:

```sh
make regenerate
```

Full compatibility workflow:

```sh
make check
```

`make check` может регенерировать dashboards и audit files.

## 11. Алгоритм старта нового EP

1. Проверить текущую ветку.
2. Проверить clean working tree.
3. Прочитать `docs/project-state.yml`.
4. Прочитать этот файл.
5. Читать только task-specific source files.
6. Не открывать generated snapshots без конкретной причины.
7. Проверить protected artifact status перед изменением accepted/protected files.
8. Не начинать новый EP поверх dirty state от другого packet.

## 12. Алгоритм post-acceptance sync

1. Пользователь обновляет target acceptance report.
2. Проверить `acceptance_decision: accepted`.
3. Проверить, что `accepted_by` заполнен и не равен `Codex`.
4. Синхронизировать `docs/project-state.yml`.
5. Синхронизировать `docs/grace/execution-packets.xml`.
6. Регенерировать derived dashboards.
7. Запустить `make verify`.
8. Не заполнять user-owned fields как Codex.
