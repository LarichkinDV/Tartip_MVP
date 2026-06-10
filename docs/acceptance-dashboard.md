# Единое окно приемки проекта Tartip

Дата обновления: 2026-06-10

## 1. Сводка

| Статус | Количество |
|---|---:|
| ready_for_acceptance | 0 |
| accepted | 14 |
| needs_revision | 0 |
| rejected | 0 |
| blocked | 0 |
| pending | 0 |
| protected_accepted_artifacts | 30 |

## 2. Требуют приемки

| Галочка | Пакет | Наименование | Что проверить | Артефакты | Команды | Детальный отчет |
|---|---|---|---|---|---|---|
| - | - | - | - | - | - | - |

## 3. Принятые задачи

| Пакет | Наименование | Принял | Дата | Комментарий | Защита |
|---|---|---|---|---|---|
| EP-001-INFRA | Prepare local infrastructure | Дмитрий | 2026-06-08 | Принято. Проверки make lint, make test и make check выполнены успешно. Pytest: 3 passed, 1 warning FastAPI/Starlette/httpx. Docker Desktop установлен. Базовые образы python:3.12-slim и node:22-alpine загружены. Docker Compose build backend/frontend выполнен успешно. Локальный стек поднят через docker compose up -d: postgres healthy, backend/frontend/adminer started. Endpoint /health проверен с хоста: HTTP 200 OK, service tartip-backend, environment local. После проверки стек корректно остановлен через docker compose down. | accepted/protected |
| EP-002-REFERENCE-GOVERNANCE | Reference data governance | Дмитрий | 2026-06-08 | Принято. Контур управления справочными данными реализован. Проверка make validate-reference выполнена успешно: Reference source validation passed. Команда make generate-data-questions выполнена успешно, новых вопросов не добавлено. Принцип No source — no rule принят: Codex не должен придумывать КСИ, ФСНБ, ГЭСН, единицы измерения, состав работ или нормативные значения. Отсутствие официальных локальных источников не блокирует приемку EP-002, но блокирует перевод конкретных правил сопоставления в активный статус до загрузки и регистрации источников. | accepted/protected |
| EP-003-REFERENCE-VERSIONING | Delta-based reference versioning | Дмитрий | 2026-06-08 | Принято. EP-003 принят как концептуально-проверочный пакет дельтового версионирования справочников: схема, hashing utility, release comparison utility и fixture-based verification проверены. Реализация рабочих DB migrations не входит в scope EP-003 и должна быть вынесена в отдельный execution packet. | accepted/protected |
| EP-004-PROJECT-PLANNING-AND-ACCEPTANCE | Project planning and acceptance contour | Дмитрий | 2026-06-08 | Принято. EP-004 принят как контур проектного планирования и приемки: project plan, artifact registry, traceability matrix, decision log, status report, acceptance reports и validate_project_plan.py проверены. Пункт о Docker Desktop переклассифицирован как риск/контекст проверки, а не блокер приемки. | accepted/protected |
| EP-005-ACCEPTANCE-AND-USER-ACTION-DASHBOARDS | Acceptance and user action dashboards | Дмитрий | 2026-06-08 | Принято. EP-005 принят как контур acceptance dashboard и user action dashboard: markdown/YAML dashboards, генераторы, Makefile targets, проверки validate_project_plan.py, запреты accepted_by/decided_by = Codex и правила защиты accepted artifacts проверены. Блокеры переклассифицированы как риски/контекст проверки. | accepted/protected |
| EP-007-VERIFICATION-DASHBOARD | Verification dashboard | Дмитрий | 2026-06-08 | Принято. EP-007 принят как контур verification dashboard: markdown/YAML окно ручной проверки, генератор, валидатор, Makefile targets, связь с месячным протоколом тестирования и запрет checked_by = Codex проверены. Ручные verification checks остаются отдельными пользовательскими проверками и не закрываются Codex. | accepted/protected |
| EP-008-DISSERTATION-PROMPT-GENERATION | Dissertation prompt generation contour | Дмитрий | 2026-06-08 | Принято. EP-008 принят как диссертационный prompt/synchronization contour: docs/dissertation, prompt profiles, forbidden claims, prompt templates, prompt queue, patches, validators and Makefile targets проверены. DOCX/PDF файлы не создавались; прямое редактирование DOCX, создание новой DOCX-версии, добавление источников без citation request и перенос инженерных деталей Tartip в научный результат запрещены. | accepted/protected |
| EP-009-CODEX-SPEC-AUDIT | Codex specification audit and language policy | Дмитрий | 2026-06-08 | Принято. EP-009 принят как audit contour и language policy: docs/audit, codex-spec audit, language audit, audit findings registry, validation scripts, Makefile targets и правила AGENTS.md проверены. Активных critical/high findings нет. Medium/low findings фиксируют риски аудита, языковой политики и workflow-контроля и не блокируют make check. Массовая русификация и исправление findings должны выполняться отдельными follow-up пакетами. | accepted/protected |
| EP-010-LANGUAGE-NORMALIZATION | Language normalization | Дмитрий | 2026-06-10 | Принято. Проверено: README.md и CHANGELOG.md нормализованы на русский язык в пределах approved CR-EP-010-README-CHANGELOG-LANGUAGE-NORMALIZATION; технические идентификаторы, команды, пути, enum-статусы, кодовые блоки и предметная методика не изменены; AUD-LANG-001 findings по README.md и CHANGELOG.md закрыты; AGENTS.md и ACCEPTANCE_TEMPLATE.md не изменялись; accepted reports других EP не изменялись; DOCX/PDF и нормативные данные не изменялись; проверки make audit-language, make validate-audit, make audit, make generate-dashboards, make validate-plan, make validate-accepted-artifact-protection, make validate-post-acceptance-state и make check выполнены успешно. | accepted/protected |
| EP-011-GIT-WORKFLOW-DISCIPLINE | Git workflow discipline | Дмитрий | 2026-06-08 | Принято. EP-011 принят как контур Git workflow discipline: docs/git-workflow.md, validate_git_workflow.py, Makefile targets, audit checks, branch/merge policy, запреты accepted_by=Codex и forbidden files проверены. Advisory warnings являются ожидаемым диагностическим поведением валидатора и не блокируют приемку. Merge остается допустимым только после пользовательской приемки, make check и явного решения пользователя. | accepted/protected |
| EP-012-USER-REVIEW-WORKBENCH-AND-ACCEPTANCE-STANDARD | User review workbench and acceptance standard | Дмитрий | 2026-06-08 | Принято. Единое активное окно проверки пользователем, стандарт пустых разделов блокеров/рисков и apply-скрипт для acceptance decisions проверены. EP-012 принят с учетом зафиксированных рисков первой версии. | accepted/protected |
| EP-013-POST-ACCEPTANCE-STATE-SYNC | Post-acceptance state sync | Дмитрий | 2026-06-09 | Принято. EP-013 принят как пакет синхронизации post-acceptance состояния: принятые EP отражены как accepted, устранен разрыв ready_for_acceptance/accepted, active acceptance queue для EP-001–EP-012 пуста, project_state=accepted_baseline зафиксирован. Verification checks, user actions, data requirements и audit findings оставлены открытыми follow-up. Protection flags вынесены в EP-014, verification reconciliation — в EP-015, reference intake — в EP-016, audit cleanup — в EP-017. | accepted/protected |
| EP-014-USER-REVIEW-DECISION-CLI-SAFETY | User review decision CLI safety | Дмитрий | 2026-06-10 | Принято. Проверено: make apply-user-review-decisions-dry-run и python3 scripts/apply_user_review_decisions.py --dry-run выполняются в non-writing режиме; сравнение git status до и после dry-run не выявило изменений. Режим --apply отделен от dry-run и защищен проверками обязательных user-owned полей, stale checksum, active blockers, запрета accepted_by = Codex и запрета перезаписи уже accepted reports. Manual verification и user_action решения в текущей версии не применяются автоматически. Accepted decisions EP-001–EP-013 не изменены. Planning decision DEC-EP-014-001 зафиксирован; перенос EP-014-ACCEPTED-ARTIFACT-PROTECTION на EP-018 подтвержден. | accepted/protected |
| EP-018-ACCEPTED-ARTIFACT-PROTECTION | Accepted artifact protection | Дмитрий | 2026-06-10 | Принято. Проверено: accepted artifacts классифицированы; accepted reports EP-001–EP-014 не изменены; generated dashboards не hard-lock; protection validator проходит; change request для будущей русификации README.md и CHANGELOG.md создан как CR-EP-010-README-CHANGELOG-LANGUAGE-NORMALIZATION со статусом requires_user_approval; EP-010 не выполнялся. | accepted/protected |

## 4. Защищенные принятые артефакты

| Артефакт | Пакет | Принял | Дата | Политика изменения |
|---|---|---|---|---|
| docs/grace/execution-packets.xml | EP-001-INFRA | Дмитрий | 2026-06-08 | Изменение требует user approval и новой ревизии |
| docs/grace/knowledge-graph.xml | EP-001-INFRA | Дмитрий | 2026-06-08 | Изменение требует user approval и новой ревизии |
| docs/acceptance/EP-001-INFRA.acceptance.md | EP-001-INFRA | Дмитрий | 2026-06-08 | Изменение требует user approval и новой ревизии |
| README.md | EP-001-INFRA | Дмитрий | 2026-06-08 | Изменение требует user approval и новой ревизии |
| CHANGELOG.md | EP-001-INFRA | Дмитрий | 2026-06-08 | Изменение требует user approval и новой ревизии |
| docs/grace/execution-packets.xml | EP-002-REFERENCE-GOVERNANCE | Дмитрий | 2026-06-08 | Изменение требует user approval и новой ревизии |
| docs/grace/knowledge-graph.xml | EP-002-REFERENCE-GOVERNANCE | Дмитрий | 2026-06-08 | Изменение требует user approval и новой ревизии |
| docs/grace/module-contracts.xml | EP-002-REFERENCE-GOVERNANCE | Дмитрий | 2026-06-08 | Изменение требует user approval и новой ревизии |
| docs/grace/verification-plan.xml | EP-002-REFERENCE-GOVERNANCE | Дмитрий | 2026-06-08 | Изменение требует user approval и новой ревизии |
| docs/acceptance/EP-002-REFERENCE-GOVERNANCE.acceptance.md | EP-002-REFERENCE-GOVERNANCE | Дмитрий | 2026-06-08 | Изменение требует user approval и новой ревизии |
| CHANGELOG.md | EP-002-REFERENCE-GOVERNANCE | Дмитрий | 2026-06-08 | Изменение требует user approval и новой ревизии |
| docs/07-reference-data-policy.md | EP-002-REFERENCE-GOVERNANCE | Дмитрий | 2026-06-08 | Изменение требует user approval и новой ревизии |
| docs/grace/execution-packets.xml | EP-003-REFERENCE-VERSIONING | Дмитрий | 2026-06-08 | Изменение требует user approval и новой ревизии |
| docs/grace/module-contracts.xml | EP-003-REFERENCE-VERSIONING | Дмитрий | 2026-06-08 | Изменение требует user approval и новой ревизии |
| docs/grace/verification-plan.xml | EP-003-REFERENCE-VERSIONING | Дмитрий | 2026-06-08 | Изменение требует user approval и новой ревизии |
| docs/acceptance/EP-003-REFERENCE-VERSIONING.acceptance.md | EP-003-REFERENCE-VERSIONING | Дмитрий | 2026-06-08 | Изменение требует user approval и новой ревизии |
| CHANGELOG.md | EP-003-REFERENCE-VERSIONING | Дмитрий | 2026-06-08 | Изменение требует user approval и новой ревизии |
| AGENTS.md | EP-004-PROJECT-PLANNING-AND-ACCEPTANCE | Дмитрий | 2026-06-08 | Изменение требует user approval и новой ревизии |
| docs/grace/execution-packets.xml | EP-004-PROJECT-PLANNING-AND-ACCEPTANCE | Дмитрий | 2026-06-08 | Изменение требует user approval и новой ревизии |
| docs/grace/verification-plan.xml | EP-004-PROJECT-PLANNING-AND-ACCEPTANCE | Дмитрий | 2026-06-08 | Изменение требует user approval и новой ревизии |
| docs/project-plan.md | EP-004-PROJECT-PLANNING-AND-ACCEPTANCE | Дмитрий | 2026-06-08 | Изменение требует user approval и новой ревизии |
| docs/artifact-registry.yml | EP-004-PROJECT-PLANNING-AND-ACCEPTANCE | Дмитрий | 2026-06-08 | Изменение требует user approval и новой ревизии |
| docs/traceability-matrix.md | EP-004-PROJECT-PLANNING-AND-ACCEPTANCE | Дмитрий | 2026-06-08 | Изменение требует user approval и новой ревизии |
| docs/decision-log.md | EP-004-PROJECT-PLANNING-AND-ACCEPTANCE | Дмитрий | 2026-06-08 | Изменение требует user approval и новой ревизии |
| docs/status-report.md | EP-004-PROJECT-PLANNING-AND-ACCEPTANCE | Дмитрий | 2026-06-08 | Изменение требует user approval и новой ревизии |
| docs/acceptance/README.md | EP-004-PROJECT-PLANNING-AND-ACCEPTANCE | Дмитрий | 2026-06-08 | Изменение требует user approval и новой ревизии |
| docs/acceptance/ACCEPTANCE_TEMPLATE.md | EP-004-PROJECT-PLANNING-AND-ACCEPTANCE | Дмитрий | 2026-06-08 | Изменение требует user approval и новой ревизии |
| docs/acceptance/EP-004-PROJECT-PLANNING-AND-ACCEPTANCE.acceptance.md | EP-004-PROJECT-PLANNING-AND-ACCEPTANCE | Дмитрий | 2026-06-08 | Изменение требует user approval и новой ревизии |
| README.md | EP-004-PROJECT-PLANNING-AND-ACCEPTANCE | Дмитрий | 2026-06-08 | Изменение требует user approval и новой ревизии |
| CHANGELOG.md | EP-004-PROJECT-PLANNING-AND-ACCEPTANCE | Дмитрий | 2026-06-08 | Изменение требует user approval и новой ревизии |
| docs/grace/execution-packets.xml | EP-005-ACCEPTANCE-AND-USER-ACTION-DASHBOARDS | Дмитрий | 2026-06-08 | Изменение требует user approval и новой ревизии |
| docs/grace/verification-plan.xml | EP-005-ACCEPTANCE-AND-USER-ACTION-DASHBOARDS | Дмитрий | 2026-06-08 | Изменение требует user approval и новой ревизии |
| docs/acceptance/EP-005-ACCEPTANCE-AND-USER-ACTION-DASHBOARDS.acceptance.md | EP-005-ACCEPTANCE-AND-USER-ACTION-DASHBOARDS | Дмитрий | 2026-06-08 | Изменение требует user approval и новой ревизии |
| docs/grace/execution-packets.xml | EP-007-VERIFICATION-DASHBOARD | Дмитрий | 2026-06-08 | Изменение требует user approval и новой ревизии |
| docs/grace/module-contracts.xml | EP-007-VERIFICATION-DASHBOARD | Дмитрий | 2026-06-08 | Изменение требует user approval и новой ревизии |
| docs/grace/verification-plan.xml | EP-007-VERIFICATION-DASHBOARD | Дмитрий | 2026-06-08 | Изменение требует user approval и новой ревизии |
| docs/acceptance/EP-007-VERIFICATION-DASHBOARD.acceptance.md | EP-007-VERIFICATION-DASHBOARD | Дмитрий | 2026-06-08 | Изменение требует user approval и новой ревизии |
| docs/acceptance/EP-008-DISSERTATION-PROMPT-GENERATION.acceptance.md | EP-008-DISSERTATION-PROMPT-GENERATION | Дмитрий | 2026-06-08 | Изменение требует user approval и новой ревизии |
| docs/acceptance/EP-009-CODEX-SPEC-AUDIT.acceptance.md | EP-009-CODEX-SPEC-AUDIT | Дмитрий | 2026-06-08 | Изменение требует user approval и новой ревизии |
| README.md | EP-010-LANGUAGE-NORMALIZATION | Дмитрий | 2026-06-10 | Изменение требует user approval и новой ревизии |
| CHANGELOG.md | EP-010-LANGUAGE-NORMALIZATION | Дмитрий | 2026-06-10 | Изменение требует user approval и новой ревизии |
| docs/acceptance/EP-010-LANGUAGE-NORMALIZATION.acceptance.md | EP-010-LANGUAGE-NORMALIZATION | Дмитрий | 2026-06-10 | Изменение требует user approval и новой ревизии |
| docs/git-workflow.md | EP-011-GIT-WORKFLOW-DISCIPLINE | Дмитрий | 2026-06-08 | Изменение требует user approval и новой ревизии |
| docs/acceptance/EP-011-GIT-WORKFLOW-DISCIPLINE.acceptance.md | EP-011-GIT-WORKFLOW-DISCIPLINE | Дмитрий | 2026-06-08 | Изменение требует user approval и новой ревизии |
| docs/acceptance/EP-012-USER-REVIEW-WORKBENCH-AND-ACCEPTANCE-STANDARD.acceptance.md | EP-012-USER-REVIEW-WORKBENCH-AND-ACCEPTANCE-STANDARD | Дмитрий | 2026-06-08 | Изменение требует user approval и новой ревизии |
| docs/acceptance/EP-013-POST-ACCEPTANCE-STATE-SYNC.acceptance.md | EP-013-POST-ACCEPTANCE-STATE-SYNC | Дмитрий | 2026-06-09 | Изменение требует user approval и новой ревизии |
| docs/grace/execution-packets.xml | EP-014-USER-REVIEW-DECISION-CLI-SAFETY | Дмитрий | 2026-06-10 | Изменение требует user approval и новой ревизии |
| docs/grace/module-contracts.xml | EP-014-USER-REVIEW-DECISION-CLI-SAFETY | Дмитрий | 2026-06-10 | Изменение требует user approval и новой ревизии |
| docs/grace/verification-plan.xml | EP-014-USER-REVIEW-DECISION-CLI-SAFETY | Дмитрий | 2026-06-10 | Изменение требует user approval и новой ревизии |
| README.md | EP-014-USER-REVIEW-DECISION-CLI-SAFETY | Дмитрий | 2026-06-10 | Изменение требует user approval и новой ревизии |
| docs/acceptance/EP-014-USER-REVIEW-DECISION-CLI-SAFETY.acceptance.md | EP-014-USER-REVIEW-DECISION-CLI-SAFETY | Дмитрий | 2026-06-10 | Изменение требует user approval и новой ревизии |
| AGENTS.md | EP-018-ACCEPTED-ARTIFACT-PROTECTION | Дмитрий | 2026-06-10 | Изменение требует user approval и новой ревизии |
| docs/grace/execution-packets.xml | EP-018-ACCEPTED-ARTIFACT-PROTECTION | Дмитрий | 2026-06-10 | Изменение требует user approval и новой ревизии |
| docs/grace/module-contracts.xml | EP-018-ACCEPTED-ARTIFACT-PROTECTION | Дмитрий | 2026-06-10 | Изменение требует user approval и новой ревизии |
| docs/grace/verification-plan.xml | EP-018-ACCEPTED-ARTIFACT-PROTECTION | Дмитрий | 2026-06-10 | Изменение требует user approval и новой ревизии |
| docs/project-plan.md | EP-018-ACCEPTED-ARTIFACT-PROTECTION | Дмитрий | 2026-06-10 | Изменение требует user approval и новой ревизии |
| docs/artifact-registry.yml | EP-018-ACCEPTED-ARTIFACT-PROTECTION | Дмитрий | 2026-06-10 | Изменение требует user approval и новой ревизии |
| docs/traceability-matrix.md | EP-018-ACCEPTED-ARTIFACT-PROTECTION | Дмитрий | 2026-06-10 | Изменение требует user approval и новой ревизии |
| docs/decision-log.md | EP-018-ACCEPTED-ARTIFACT-PROTECTION | Дмитрий | 2026-06-10 | Изменение требует user approval и новой ревизии |
| docs/status-report.md | EP-018-ACCEPTED-ARTIFACT-PROTECTION | Дмитрий | 2026-06-10 | Изменение требует user approval и новой ревизии |
| docs/acceptance/EP-018-ACCEPTED-ARTIFACT-PROTECTION.acceptance.md | EP-018-ACCEPTED-ARTIFACT-PROTECTION | Дмитрий | 2026-06-10 | Изменение требует user approval и новой ревизии |

Historical accepted comments may mention earlier EP-014 protection planning; the current accepted artifact protection packet is `EP-018-ACCEPTED-ARTIFACT-PROTECTION`.

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
