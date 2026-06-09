# Единое окно приемки проекта Tartip

Дата обновления: 2026-06-09

## 1. Сводка

| Статус | Количество |
|---|---:|
| ready_for_acceptance | 10 |
| accepted | 4 |
| needs_revision | 0 |
| rejected | 0 |
| blocked | 0 |
| pending | 6 |
| protected_accepted_artifacts | 0 |

## 2. Требуют приемки

| Галочка | Пакет | Наименование | Что проверить | Артефакты | Команды | Детальный отчет |
|---|---|---|---|---|---|---|
| - [ ] требует проверки | EP-004-PROJECT-PLANNING-AND-ACCEPTANCE | Project planning and acceptance contour | Acceptance criteria and artifacts | AGENTS.md, docs/grace/execution-packets.xml, docs/grace/verification-plan.xml, docs/grace/README.md, ... | make validate-plan, make check, make validate-reference, source .venv/bin/activate && python -m pytest | [docs/acceptance/EP-004-PROJECT-PLANNING-AND-ACCEPTANCE.acceptance.md](docs/acceptance/EP-004-PROJECT-PLANNING-AND-ACCEPTANCE.acceptance.md) |
| - [ ] требует проверки | EP-005-ACCEPTANCE-AND-USER-ACTION-DASHBOARDS | Acceptance and user action dashboards | Acceptance criteria and artifacts | docs/grace/execution-packets.xml, docs/grace/verification-plan.xml, docs/grace/README.md, scripts/validate_project_plan.py, ... | make generate-dashboards, make validate-plan, make check, make validate-reference, source .venv/bin/activate && python -m pytest | [docs/acceptance/EP-005-ACCEPTANCE-AND-USER-ACTION-DASHBOARDS.acceptance.md](docs/acceptance/EP-005-ACCEPTANCE-AND-USER-ACTION-DASHBOARDS.acceptance.md) |
| - [ ] требует проверки | EP-007-VERIFICATION-DASHBOARD | Verification dashboard | Acceptance criteria and artifacts | docs/grace/execution-packets.xml, docs/grace/module-contracts.xml, docs/grace/verification-plan.xml, docs/grace/README.md, ... | - | [docs/acceptance/EP-007-VERIFICATION-DASHBOARD.acceptance.md](docs/acceptance/EP-007-VERIFICATION-DASHBOARD.acceptance.md) |
| - [ ] требует проверки | EP-008-DISSERTATION-PROMPT-GENERATION | Dissertation prompt generation contour | Acceptance criteria and artifacts | docs/dissertation/README.md, docs/dissertation/dissertation-sync-plan.md, docs/dissertation/dissertation-impact-log.yml, docs/dissertation/dissertation-artifact-map.yml, ... | make validate-dissertation-sync, make validate-dissertation-prompts, make generate-dissertation-prompts, make generate-dashboards, make generate-verification-dashboard, make validate-verification, make validate-plan, make check, source .venv/bin/activate && make lint, source .venv/bin/activate && make test | [docs/acceptance/EP-008-DISSERTATION-PROMPT-GENERATION.acceptance.md](docs/acceptance/EP-008-DISSERTATION-PROMPT-GENERATION.acceptance.md) |
| - [ ] требует проверки | EP-009-CODEX-SPEC-AUDIT | Codex specification audit and language policy | Acceptance criteria and artifacts | docs/audit/README.md, docs/audit/codex-spec-audit.md, docs/audit/codex-spec-audit.yml, docs/audit/language-policy.md, ... | make audit-codex-spec, make audit-language, make validate-audit, make audit, make generate-dashboards, make generate-verification-dashboard, make validate-verification, make validate-plan, make check, make validate-reference, pytest | [docs/acceptance/EP-009-CODEX-SPEC-AUDIT.acceptance.md](docs/acceptance/EP-009-CODEX-SPEC-AUDIT.acceptance.md) |
| - [ ] требует проверки | EP-011-GIT-WORKFLOW-DISCIPLINE | Git workflow discipline | Acceptance criteria and artifacts | docs/git-workflow.md, scripts/validate_git_workflow.py, docs/acceptance/EP-011-GIT-WORKFLOW-DISCIPLINE.acceptance.md | make validate-git-workflow, make audit, make validate-plan, make check | [docs/acceptance/EP-011-GIT-WORKFLOW-DISCIPLINE.acceptance.md](docs/acceptance/EP-011-GIT-WORKFLOW-DISCIPLINE.acceptance.md) |

## 3. Принятые задачи

| Пакет | Наименование | Принял | Дата | Комментарий | Защита |
|---|---|---|---|---|---|
| EP-001-INFRA | Prepare local infrastructure | Дмитрий | 2026-06-08 | Принято. Проверки make lint, make test и make check выполнены успешно. Pytest: 3 passed, 1 warning FastAPI/Starlette/httpx. Docker Desktop установлен. Базовые образы python:3.12-slim и node:22-alpine загружены. Docker Compose build backend/frontend выполнен успешно. Локальный стек поднят через docker compose up -d: postgres healthy, backend/frontend/adminer started. Endpoint /health проверен с хоста: HTTP 200 OK, service tartip-backend, environment local. После проверки стек корректно остановлен через docker compose down. | protected |
| EP-002-REFERENCE-GOVERNANCE | Reference data governance | Дмитрий | 2026-06-08 | Принято. Контур управления справочными данными реализован. Проверка make validate-reference выполнена успешно: Reference source validation passed. Команда make generate-data-questions выполнена успешно, новых вопросов не добавлено. Принцип No source — no rule принят: Codex не должен придумывать КСИ, ФСНБ, ГЭСН, единицы измерения, состав работ или нормативные значения. Отсутствие официальных локальных источников не блокирует приемку EP-002, но блокирует перевод конкретных правил сопоставления в активный статус до загрузки и регистрации источников. | protected |
| EP-003-REFERENCE-VERSIONING | Delta-based reference versioning | Дмитрий | 2026-06-08 | Принято. EP-003 принят как концептуально-проверочный пакет дельтового версионирования справочников: схема, hashing utility, release comparison utility и fixture-based verification проверены. Реализация рабочих DB migrations не входит в scope EP-003 и должна быть вынесена в отдельный execution packet. | protected |
| EP-012-USER-REVIEW-WORKBENCH-AND-ACCEPTANCE-STANDARD | User review workbench and acceptance standard | Дмитрий | 2026-06-08 | Принято. Единое активное окно проверки пользователем, стандарт пустых разделов блокеров/рисков и apply-скрипт для acceptance decisions проверены. EP-012 принят с учетом зафиксированных рисков первой версии. | protected |

## 4. Защищенные принятые артефакты

| Артефакт | Пакет | Принял | Дата | Политика изменения |
|---|---|---|---|---|
| - | - | - | - | Нет accepted artifacts |

## 5. Требуют доработки

| Пакет | Причина | Что доработать | Детальный отчет |
|---|---|---|---|
| - | - | - | - |

## 6. Заблокированные задачи

| Пакет | Причина блокировки | Что требуется | Детальный отчет |
|---|---|---|---|
| - | - | - | - |

## 7. Как принять задачу

1. Открыть детальный acceptance report.
2. Проверить артефакты.
3. Запустить команды проверки.
4. Заполнить решение пользователя.
5. Не указывать Codex в качестве accepted_by / decided_by.

## 8. Как изменить принятый артефакт

1. Не изменять accepted artifact напрямую.
2. Создать change request.
3. Указать причину изменения.
4. Указать impact analysis.
5. Получить согласование пользователя.
6. Создать новую ревизию или отдельный пакет изменения.
7. Провести повторную приемку.

Состояние хранится в YAML dashboard и acceptance reports, а не только в Markdown-чекбоксах.
