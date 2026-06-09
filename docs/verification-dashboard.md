# Окно проверки работоспособности проекта Tartip

Дата обновления: 2026-06-09

## 1. Сводка

| Статус | Количество |
|---|---:|
| pending | 44 |
| in_progress | 0 |
| passed | 0 |
| failed | 0 |
| blocked | 0 |
| requires_user_action | 0 |
| not_applicable | 0 |

## 2. Проверки, ожидающие выполнения

| Галочка | ID | Проверка | Как проверить | Ожидаемый результат | Артефакты | Статус |
|---|---|---|---|---|---|---|
| - [ ] не проверено | VT-EP-004-001 | Проверить наличие docs/project-plan.md | Открыть docs/project-plan.md.; Проверить, что файл существует и содержит текущий execution packet. | docs/project-plan.md существует и доступен для ручной проверки. | docs/project-plan.md | pending |
| - [ ] не проверено | VT-EP-004-002 | Проверить наличие docs/artifact-registry.yml | Открыть docs/artifact-registry.yml.; Проверить, что реестр содержит созданные артефакты. | docs/artifact-registry.yml существует и содержит artifact registry. | docs/artifact-registry.yml | pending |
| - [ ] не проверено | VT-EP-004-003 | Проверить, что accepted_by не может быть Codex | Открыть scripts/validate_project_plan.py.; Проверить наличие запрета accepted_by=Codex. | Валидация запрещает accepted_by=Codex. | scripts/validate_project_plan.py | pending |
| - [ ] не проверено | VT-EP-004-004 | Проверить, что make validate-plan проходит | Запустить make validate-plan. | Команда завершается с кодом 0. | scripts/validate_project_plan.py | pending |
| - [ ] не проверено | VT-EP-005-001 | Проверить генерацию acceptance dashboard | Запустить make generate-acceptance-dashboard. | docs/acceptance-dashboard.md и docs/acceptance-dashboard.yml обновлены без accepted от Codex. | docs/acceptance-dashboard.md, docs/acceptance-dashboard.yml | pending |
| - [ ] не проверено | VT-EP-005-002 | Проверить генерацию user action dashboard | Запустить make generate-user-action-dashboard. | docs/user-action-dashboard.md и docs/user-action-dashboard.yml обновлены без закрытия вопросов за пользователя. | docs/user-action-dashboard.md, docs/user-action-dashboard.yml | pending |
| - [ ] не проверено | VT-EP-005-003 | Проверить, что accepted artifacts отображаются как protected | Открыть docs/acceptance-dashboard.md.; Проверить раздел защищенных принятых артефактов. | Accepted artifacts отображаются как protected или явно указано, что accepted artifacts отсутствуют. | docs/acceptance-dashboard.md, docs/acceptance-dashboard.yml | pending |
| - [ ] не проверено | VT-EP-005-004 | Проверить, что open questions отображаются в user-action-dashboard | Открыть docs/user-action-dashboard.md.; Сверить open вопросы с data/questions/*.yml. | Все open/high priority вопросы видны в user action dashboard. | docs/user-action-dashboard.md, data/questions/data-requirements.yml, data/questions/normative-review-questions.yml | pending |
| - [ ] не проверено | VT-EP-006-001 | Проверить наличие monthly-plan.yml | Открыть docs/monthly/monthly-plan.yml. | monthly-plan.yml существует и описывает блок 2026-06. | docs/monthly/monthly-plan.yml | pending |
| - [ ] не проверено | VT-EP-006-002 | Проверить, что месячный блок содержит ровно 3 задачи | Открыть docs/monthly/monthly-plan.yml.; Посчитать задачи в monthly_plan.tasks. | В блоке 2026-06 указано ровно 3 задачи. | docs/monthly/monthly-plan.yml | pending |
| - [ ] не проверено | VT-EP-006-003 | Проверить, что каждая задача имеет 15 человеко-часов | Открыть docs/monthly/monthly-plan.yml.; Проверить planned_hours у каждой задачи. | Каждая из 3 задач имеет planned_hours: 15. | docs/monthly/monthly-plan.yml | pending |
| - [ ] не проверено | VT-EP-006-004 | Проверить наличие БФТ | Открыть docs/monthly/2026-06/01-bft-reference-data-governance.md. | Документ БФТ существует и не содержит нормативных данных, придуманных Codex. | docs/monthly/2026-06/01-bft-reference-data-governance.md | pending |
| - [ ] не проверено | VT-EP-006-005 | Проверить наличие ТЗ | Открыть docs/monthly/2026-06/02-technical-task-reference-data-governance.md. | Документ ТЗ существует и фиксирует задачи проверки без изменения доменной методики. | docs/monthly/2026-06/02-technical-task-reference-data-governance.md | pending |
| - [ ] не проверено | VT-EP-006-006 | Проверить наличие протокола тестирования | Открыть docs/monthly/2026-06/03-test-protocol-reference-data-governance.md. | Протокол тестирования существует и связан с verification dashboard. | docs/monthly/2026-06/03-test-protocol-reference-data-governance.md | pending |
| - [ ] не проверено | VT-EP-007-001 | Проверить наличие verification-dashboard.md | Открыть docs/verification-dashboard.md. | verification-dashboard.md существует и содержит окно ручной проверки. | docs/verification-dashboard.md | pending |
| - [ ] не проверено | VT-EP-007-002 | Проверить наличие verification-dashboard.yml | Открыть docs/verification-dashboard.yml. | verification-dashboard.yml существует и содержит checks. | docs/verification-dashboard.yml | pending |
| - [ ] не проверено | VT-EP-007-003 | Проверить, что manual checks не отмечены Codex как passed | Открыть docs/verification-dashboard.yml.; Проверить manual_* checks и user_result. | Manual checks не имеют checked_by: Codex и не закрыты Codex. | docs/verification-dashboard.yml | pending |
| - [ ] не проверено | VT-EP-007-004 | Проверить, что checked_by не может быть Codex | Открыть scripts/validate_verification_dashboard.py.; Проверить запрет checked_by=Codex. | Валидатор запрещает checked_by=Codex. | scripts/validate_verification_dashboard.py | pending |
| - [ ] не проверено | VT-EP-007-005 | Проверить, что verification dashboard связан с протоколом тестирования | Открыть docs/monthly/2026-06/03-test-protocol-reference-data-governance.md.; Проверить ссылки на docs/verification-dashboard.md и check_id. | Протокол тестирования содержит раздел про окно ручной проверки и check_id. | docs/monthly/2026-06/03-test-protocol-reference-data-governance.md, docs/verification-dashboard.md | pending |
| - [ ] не проверено | VT-EP-008-001 | Проверить наличие docs/dissertation/README.md | Открыть docs/dissertation/README.md. | docs/dissertation/README.md существует и описывает dissertation sync workflow. | docs/dissertation/README.md | pending |
| - [ ] не проверено | VT-EP-008-002 | Проверить наличие forbidden-claims.yml | Открыть docs/dissertation/prompt-profiles/forbidden-claims.yml. | forbidden-claims.yml содержит FC-001..FC-007 и запрет автоматического выбора ГЭСН по BIM-элементу. | docs/dissertation/prompt-profiles/forbidden-claims.yml | pending |
| - [ ] не проверено | VT-EP-008-003 | Проверить запрет docx_update prompt без accepted patch | Запустить make validate-dissertation-prompts. | Валидатор запрещает docx_update prompt без accepted patch. | scripts/validate_dissertation_prompts.py | pending |
| - [ ] не проверено | VT-EP-008-004 | Проверить, что prompts не содержат forbidden claims | Запустить make validate-dissertation-prompts. | Валидатор запрещает generated prompts с forbidden claims. | scripts/validate_dissertation_prompts.py, docs/dissertation/prompt-profiles/forbidden-claims.yml | pending |
| - [ ] не проверено | VT-EP-008-005 | Проверить, что Codex не создал DOCX | Запустить make validate-dissertation-sync. | Валидатор не находит DOCX/PDF в thesis/. | scripts/validate_dissertation_sync.py, thesis/.gitkeep | pending |
| - [ ] не проверено | VT-EP-008-006 | Проверить, что acceptance_decision остается pending | Открыть docs/acceptance/EP-008-DISSERTATION-PROMPT-GENERATION.acceptance.md.; Проверить блок Решение пользователя. | acceptance_decision остается pending, accepted_by не заполнен Codex. | docs/acceptance/EP-008-DISSERTATION-PROMPT-GENERATION.acceptance.md | pending |
| - [ ] не проверено | VT-EP-008-007 | Проверить защиту accepted/protected artifacts | Открыть docs/acceptance-dashboard.md.; Проверить раздел защищенных принятых артефактов. | Accepted/protected artifacts не изменены без user approval или явно указано, что таких артефактов нет. | docs/acceptance-dashboard.md, docs/artifact-registry.yml | pending |
| - [ ] не проверено | VT-EP-009-001 | Проверить наличие audit contour | Запустить make validate-audit. | Все обязательные audit-файлы существуют и валидны. | docs/audit/README.md, docs/audit/codex-spec-audit.md, docs/audit/codex-spec-audit.yml, docs/audit/language-policy.md, docs/audit/language-audit-report.md, docs/audit/audit-findings.yml | pending |
| - [ ] не проверено | VT-EP-009-002 | Проверить Codex spec audit script | Запустить make audit-codex-spec. | Скрипт проверяет domain, acceptance, protection, dashboards, verification, monthly и dissertation guardrails. | scripts/audit_codex_spec.py, docs/audit/codex-spec-audit.md | pending |
| - [ ] не проверено | VT-EP-009-003 | Проверить language audit script | Запустить make audit-language. | Скрипт создает language findings и не падает на medium/low пользовательских англоязычных фрагментах. | scripts/audit_language_policy.py, docs/audit/language-audit-report.md | pending |
| - [ ] не проверено | VT-EP-009-004 | Проверить Language policy в AGENTS.md | Открыть AGENTS.md и найти раздел Language policy. | AGENTS.md содержит Language policy с исключениями для technical identifiers. | AGENTS.md | pending |
| - [ ] не проверено | VT-EP-009-005 | Проверить Audit discipline в AGENTS.md | Открыть AGENTS.md и найти раздел Audit discipline. | AGENTS.md содержит audit-first/read-mostly discipline и запрет mass rewrite. | AGENTS.md | pending |
| - [ ] не проверено | VT-EP-009-006 | Проверить запрет ModelElement -> GESNNorm в audit | Запустить make audit-codex-spec. | Отсутствие forbidden edge ModelElement -> GESNNorm создает critical finding. | scripts/audit_codex_spec.py, docs/grace/knowledge-graph.xml | pending |
| - [ ] не проверено | VT-EP-009-007 | Проверить запрет Codex в user-owned fields | Запустить make audit-codex-spec. | accepted_by, decided_by, checked_by и answered_by не могут быть Codex. | scripts/audit_codex_spec.py | pending |
| - [ ] не проверено | VT-EP-009-008 | Проверить preservation audit findings | Открыть scripts/audit_codex_spec.py и scripts/audit_language_policy.py.; Проверить, что merge_findings сохраняет status, resolution, resolved_by и resolved_at. | Audit scripts preserve existing user resolutions in audit-findings.yml. | scripts/audit_codex_spec.py, scripts/audit_language_policy.py, docs/audit/audit-findings.yml | pending |
| - [ ] не проверено | VT-EP-009-009 | Проверить, что language findings не блокируют make check | Запустить make check. | Medium/low AUD-LANG-001 findings фиксируются, но не блокируют make check. | Makefile, scripts/audit_language_policy.py | pending |
| - [ ] не проверено | VT-EP-009-010 | Проверить, что EP-009 не mass-rewrite packet | Проверить git diff.; Убедиться, что изменения ограничены audit contour, scripts, GRACE registration, dashboards, plans, README и CHANGELOG. | EP-009 не выполняет массовую русификацию существующих документов. | docs/audit/README.md, docs/audit/language-audit-report.md | pending |
| - [ ] не проверено | VT-EP-011-001 | Проверить Git workflow validator | Запустить make validate-git-workflow. | Advisory validator завершается с кодом 0 или фиксирует documented warning без Git mutations. | scripts/validate_git_workflow.py, Makefile | pending |
| - [ ] не проверено | VT-EP-011-002 | Проверить Git workflow discipline в AGENTS.md | Открыть AGENTS.md и найти раздел Git workflow discipline. | AGENTS.md описывает branch creation, dirty tree, merge gate и forbidden files. | AGENTS.md | pending |
| - [ ] не проверено | VT-EP-011-003 | Проверить branch naming policy | Открыть docs/git-workflow.md. | Документ фиксирует формат ep-<number>-<short-slug>. | docs/git-workflow.md | pending |
| - [ ] не проверено | VT-EP-011-004 | Проверить merge policy | Открыть docs/git-workflow.md и AGENTS.md. | Merge в main разрешен только после accepted packet, make check, audit gate и explicit user approval. | docs/git-workflow.md, AGENTS.md | pending |
| - [ ] не проверено | VT-EP-011-005 | Проверить запрет merge без acceptance | Запустить make audit-codex-spec. | Audit фиксирует merge forbidden, пока acceptance_decision не accepted. | scripts/audit_codex_spec.py, docs/audit/audit-findings.yml | pending |
| - [ ] не проверено | VT-EP-011-006 | Проверить запрет accepted_by = Codex | Запустить make audit-codex-spec. | Audit и validator запрещают accepted_by = Codex. | scripts/audit_codex_spec.py, scripts/validate_git_workflow.py | pending |
| - [ ] не проверено | VT-EP-011-007 | Проверить forbidden Git files | Запустить make validate-git-workflow. | Validator проверяет .env, .venv, node_modules, SQL/dump/backup files и реальные dissertation DOCX/PDF. | scripts/validate_git_workflow.py | pending |
| - [ ] не проверено | VT-EP-011-008 | Проверить, что validator не выполняет Git mutations | Открыть scripts/validate_git_workflow.py. | Скрипт не вызывает git add, git commit, git merge, git push или удаление веток. | scripts/validate_git_workflow.py | pending |

## 3. Автоматические проверки

| ID | Проверка | Команда | Ожидаемый результат | Статус |
|---|---|---|---|---|
| VT-EP-004-004 | Проверить, что make validate-plan проходит | make validate-plan | Команда завершается с кодом 0. | pending |
| VT-EP-005-001 | Проверить генерацию acceptance dashboard | make generate-acceptance-dashboard | docs/acceptance-dashboard.md и docs/acceptance-dashboard.yml обновлены без accepted от Codex. | pending |
| VT-EP-005-002 | Проверить генерацию user action dashboard | make generate-user-action-dashboard | docs/user-action-dashboard.md и docs/user-action-dashboard.yml обновлены без закрытия вопросов за пользователя. | pending |
| VT-EP-008-003 | Проверить запрет docx_update prompt без accepted patch | make validate-dissertation-prompts | Валидатор запрещает docx_update prompt без accepted patch. | pending |
| VT-EP-008-004 | Проверить, что prompts не содержат forbidden claims | make validate-dissertation-prompts | Валидатор запрещает generated prompts с forbidden claims. | pending |
| VT-EP-008-005 | Проверить, что Codex не создал DOCX | make validate-dissertation-sync | Валидатор не находит DOCX/PDF в thesis/. | pending |
| VT-EP-009-001 | Проверить наличие audit contour | make validate-audit | Все обязательные audit-файлы существуют и валидны. | pending |
| VT-EP-009-002 | Проверить Codex spec audit script | make audit-codex-spec | Скрипт проверяет domain, acceptance, protection, dashboards, verification, monthly и dissertation guardrails. | pending |
| VT-EP-009-003 | Проверить language audit script | make audit-language | Скрипт создает language findings и не падает на medium/low пользовательских англоязычных фрагментах. | pending |
| VT-EP-009-006 | Проверить запрет ModelElement -> GESNNorm в audit | make audit-codex-spec | Отсутствие forbidden edge ModelElement -> GESNNorm создает critical finding. | pending |
| VT-EP-009-007 | Проверить запрет Codex в user-owned fields | make audit-codex-spec | accepted_by, decided_by, checked_by и answered_by не могут быть Codex. | pending |
| VT-EP-009-009 | Проверить, что language findings не блокируют make check | make check | Medium/low AUD-LANG-001 findings фиксируются, но не блокируют make check. | pending |
| VT-EP-011-001 | Проверить Git workflow validator | make validate-git-workflow | Advisory validator завершается с кодом 0 или фиксирует documented warning без Git mutations. | pending |
| VT-EP-011-005 | Проверить запрет merge без acceptance | make audit-codex-spec | Audit фиксирует merge forbidden, пока acceptance_decision не accepted. | pending |
| VT-EP-011-006 | Проверить запрет accepted_by = Codex | make audit-codex-spec | Audit и validator запрещают accepted_by = Codex. | pending |
| VT-EP-011-007 | Проверить forbidden Git files | make validate-git-workflow | Validator проверяет .env, .venv, node_modules, SQL/dump/backup files и реальные dissertation DOCX/PDF. | pending |

## 4. Ручные проверки документов

| ID | Проверка | Документ | Что проверить | Статус |
|---|---|---|---|---|
| VT-EP-004-001 | Проверить наличие docs/project-plan.md | docs/project-plan.md | Открыть docs/project-plan.md.; Проверить, что файл существует и содержит текущий execution packet. | pending |
| VT-EP-004-002 | Проверить наличие docs/artifact-registry.yml | docs/artifact-registry.yml | Открыть docs/artifact-registry.yml.; Проверить, что реестр содержит созданные артефакты. | pending |
| VT-EP-004-003 | Проверить, что accepted_by не может быть Codex | scripts/validate_project_plan.py | Открыть scripts/validate_project_plan.py.; Проверить наличие запрета accepted_by=Codex. | pending |
| VT-EP-005-004 | Проверить, что open questions отображаются в user-action-dashboard | docs/user-action-dashboard.md, data/questions/data-requirements.yml, data/questions/normative-review-questions.yml | Открыть docs/user-action-dashboard.md.; Сверить open вопросы с data/questions/*.yml. | pending |
| VT-EP-006-001 | Проверить наличие monthly-plan.yml | docs/monthly/monthly-plan.yml | Открыть docs/monthly/monthly-plan.yml. | pending |
| VT-EP-006-002 | Проверить, что месячный блок содержит ровно 3 задачи | docs/monthly/monthly-plan.yml | Открыть docs/monthly/monthly-plan.yml.; Посчитать задачи в monthly_plan.tasks. | pending |
| VT-EP-006-003 | Проверить, что каждая задача имеет 15 человеко-часов | docs/monthly/monthly-plan.yml | Открыть docs/monthly/monthly-plan.yml.; Проверить planned_hours у каждой задачи. | pending |
| VT-EP-006-004 | Проверить наличие БФТ | docs/monthly/2026-06/01-bft-reference-data-governance.md | Открыть docs/monthly/2026-06/01-bft-reference-data-governance.md. | pending |
| VT-EP-006-005 | Проверить наличие ТЗ | docs/monthly/2026-06/02-technical-task-reference-data-governance.md | Открыть docs/monthly/2026-06/02-technical-task-reference-data-governance.md. | pending |
| VT-EP-006-006 | Проверить наличие протокола тестирования | docs/monthly/2026-06/03-test-protocol-reference-data-governance.md | Открыть docs/monthly/2026-06/03-test-protocol-reference-data-governance.md. | pending |
| VT-EP-007-001 | Проверить наличие verification-dashboard.md | docs/verification-dashboard.md | Открыть docs/verification-dashboard.md. | pending |
| VT-EP-007-002 | Проверить наличие verification-dashboard.yml | docs/verification-dashboard.yml | Открыть docs/verification-dashboard.yml. | pending |
| VT-EP-007-003 | Проверить, что manual checks не отмечены Codex как passed | docs/verification-dashboard.yml | Открыть docs/verification-dashboard.yml.; Проверить manual_* checks и user_result. | pending |
| VT-EP-007-004 | Проверить, что checked_by не может быть Codex | scripts/validate_verification_dashboard.py | Открыть scripts/validate_verification_dashboard.py.; Проверить запрет checked_by=Codex. | pending |
| VT-EP-007-005 | Проверить, что verification dashboard связан с протоколом тестирования | docs/monthly/2026-06/03-test-protocol-reference-data-governance.md, docs/verification-dashboard.md | Открыть docs/monthly/2026-06/03-test-protocol-reference-data-governance.md.; Проверить ссылки на docs/verification-dashboard.md и check_id. | pending |
| VT-EP-008-001 | Проверить наличие docs/dissertation/README.md | docs/dissertation/README.md | Открыть docs/dissertation/README.md. | pending |
| VT-EP-008-002 | Проверить наличие forbidden-claims.yml | docs/dissertation/prompt-profiles/forbidden-claims.yml | Открыть docs/dissertation/prompt-profiles/forbidden-claims.yml. | pending |
| VT-EP-009-004 | Проверить Language policy в AGENTS.md | AGENTS.md | Открыть AGENTS.md и найти раздел Language policy. | pending |
| VT-EP-009-005 | Проверить Audit discipline в AGENTS.md | AGENTS.md | Открыть AGENTS.md и найти раздел Audit discipline. | pending |
| VT-EP-009-008 | Проверить preservation audit findings | scripts/audit_codex_spec.py, scripts/audit_language_policy.py, docs/audit/audit-findings.yml | Открыть scripts/audit_codex_spec.py и scripts/audit_language_policy.py.; Проверить, что merge_findings сохраняет status, resolution, resolved_by и resolved_at. | pending |
| VT-EP-011-002 | Проверить Git workflow discipline в AGENTS.md | AGENTS.md | Открыть AGENTS.md и найти раздел Git workflow discipline. | pending |
| VT-EP-011-003 | Проверить branch naming policy | docs/git-workflow.md | Открыть docs/git-workflow.md. | pending |
| VT-EP-011-004 | Проверить merge policy | docs/git-workflow.md, AGENTS.md | Открыть docs/git-workflow.md и AGENTS.md. | pending |
| VT-EP-011-008 | Проверить, что validator не выполняет Git mutations | scripts/validate_git_workflow.py | Открыть scripts/validate_git_workflow.py. | pending |

## 5. Ручные функциональные проверки

| ID | Проверка | Как проверить | Ожидаемый результат | Статус |
|---|---|---|---|---|
| VT-EP-005-003 | Проверить, что accepted artifacts отображаются как protected | Открыть docs/acceptance-dashboard.md.; Проверить раздел защищенных принятых артефактов. | Accepted artifacts отображаются как protected или явно указано, что accepted artifacts отсутствуют. | pending |
| VT-EP-008-006 | Проверить, что acceptance_decision остается pending | Открыть docs/acceptance/EP-008-DISSERTATION-PROMPT-GENERATION.acceptance.md.; Проверить блок Решение пользователя. | acceptance_decision остается pending, accepted_by не заполнен Codex. | pending |
| VT-EP-008-007 | Проверить защиту accepted/protected artifacts | Открыть docs/acceptance-dashboard.md.; Проверить раздел защищенных принятых артефактов. | Accepted/protected artifacts не изменены без user approval или явно указано, что таких артефактов нет. | pending |
| VT-EP-009-010 | Проверить, что EP-009 не mass-rewrite packet | Проверить git diff.; Убедиться, что изменения ограничены audit contour, scripts, GRACE registration, dashboards, plans, README и CHANGELOG. | EP-009 не выполняет массовую русификацию существующих документов. | pending |

## 6. Нормативные проверки

| ID | Проверка | Что проверить | Требуемый источник | Статус |
|---|---|---|---|---|
| - | - | - | - | - |

## 7. Выполненные проверки

| ID | Проверка | Проверил | Дата | Результат | Комментарий |
|---|---|---|---|---|---|
| - | - | - | - | - | - |

## 8. Не пройдено

| ID | Проверка | Ошибка | Что требуется |
|---|---|---|---|
| - | - | - | - |

## 9. Заблокировано

| ID | Проверка | Причина блокировки | Что требуется |
|---|---|---|---|
| - | - | - | - |

## 10. Как отмечать проверку выполненной

1. Найти проверку в `docs/verification-dashboard.yml`.
2. Заполнить:
   - `checked: true`;
   - `checked_by: Дмитрий`;
   - `checked_at: YYYY-MM-DD`;
   - `result: passed` или `failed`;
   - `comments`.
3. Не указывать `Codex` в `checked_by`.
4. После изменения запустить `make validate-verification`.

Проверка работоспособности не равна приемке результата. Приемка остается в acceptance dashboard и acceptance reports.
