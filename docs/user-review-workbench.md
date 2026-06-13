# Единое активное окно проверки пользователем

Дата обновления: 2026-06-13

## 1. Сводка

| Раздел | Количество |
|---|---:|
| Активные элементы проверки | 32 |
| Пакеты готовы к приемке | 0 |
| Ручные проверки ожидают выполнения | 28 |
| Вопросы требуют ответа | 4 |
| Требуют user approval | 0 |
| Critical audit findings | 0 |
| High audit findings | 0 |
| Активные блокеры | 4 |
| Historical audit findings | 364 |
| Audit finding groups | 6 |
| Принятые пакеты скрыты из активной очереди | 21 |

## 2. Что требует моего решения сейчас

| Приоритет | Тип | ID | EP | Что проверить | Где источник | Действие |
|---|---|---|---|---|---|---|
| high | manual_verification | VERIFICATION-VT-EP-004-001 | EP-004-PROJECT-PLANNING-AND-ACCEPTANCE | Проверить наличие docs/project-plan.md | docs/verification-dashboard.yml | Выполнить ручную проверку и заполнить user_result в verification dashboard. |
| high | manual_verification | VERIFICATION-VT-EP-004-002 | EP-004-PROJECT-PLANNING-AND-ACCEPTANCE | Проверить наличие docs/artifact-registry.yml | docs/verification-dashboard.yml | Выполнить ручную проверку и заполнить user_result в verification dashboard. |
| high | manual_verification | VERIFICATION-VT-EP-004-003 | EP-004-PROJECT-PLANNING-AND-ACCEPTANCE | Проверить, что accepted_by не может быть Codex | docs/verification-dashboard.yml | Выполнить ручную проверку и заполнить user_result в verification dashboard. |
| high | manual_verification | VERIFICATION-VT-EP-005-004 | EP-005-ACCEPTANCE-AND-USER-ACTION-DASHBOARDS | Проверить, что open questions отображаются в user-action-dashboard | docs/verification-dashboard.yml | Выполнить ручную проверку и заполнить user_result в verification dashboard. |
| high | manual_verification | VERIFICATION-VT-EP-007-001 | EP-007-VERIFICATION-DASHBOARD | Проверить наличие verification-dashboard.md | docs/verification-dashboard.yml | Выполнить ручную проверку и заполнить user_result в verification dashboard. |
| high | manual_verification | VERIFICATION-VT-EP-007-002 | EP-007-VERIFICATION-DASHBOARD | Проверить наличие verification-dashboard.yml | docs/verification-dashboard.yml | Выполнить ручную проверку и заполнить user_result в verification dashboard. |
| high | manual_verification | VERIFICATION-VT-EP-007-003 | EP-007-VERIFICATION-DASHBOARD | Проверить, что manual checks не отмечены Codex как passed | docs/verification-dashboard.yml | Выполнить ручную проверку и заполнить user_result в verification dashboard. |
| high | manual_verification | VERIFICATION-VT-EP-007-004 | EP-007-VERIFICATION-DASHBOARD | Проверить, что checked_by не может быть Codex | docs/verification-dashboard.yml | Выполнить ручную проверку и заполнить user_result в verification dashboard. |
| high | manual_verification | VERIFICATION-VT-EP-007-005 | EP-007-VERIFICATION-DASHBOARD | Проверить, что verification dashboard связан с протоколом тестирования | docs/verification-dashboard.yml | Выполнить ручную проверку и заполнить user_result в verification dashboard. |
| high | manual_verification | VERIFICATION-VT-EP-008-001 | EP-008-DISSERTATION-PROMPT-GENERATION | Проверить наличие docs/dissertation/README.md | docs/verification-dashboard.yml | Выполнить ручную проверку и заполнить user_result в verification dashboard. |
| high | manual_verification | VERIFICATION-VT-EP-008-002 | EP-008-DISSERTATION-PROMPT-GENERATION | Проверить наличие forbidden-claims.yml | docs/verification-dashboard.yml | Выполнить ручную проверку и заполнить user_result в verification dashboard. |
| high | manual_verification | VERIFICATION-VT-EP-008-006 | EP-008-DISSERTATION-PROMPT-GENERATION | Проверить, что acceptance_decision остается pending | docs/verification-dashboard.yml | Выполнить ручную проверку и заполнить user_result в verification dashboard. |
| high | manual_verification | VERIFICATION-VT-EP-009-004 | EP-009-CODEX-SPEC-AUDIT | Проверить Language policy в AGENTS.md | docs/verification-dashboard.yml | Выполнить ручную проверку и заполнить user_result в verification dashboard. |
| high | manual_verification | VERIFICATION-VT-EP-009-005 | EP-009-CODEX-SPEC-AUDIT | Проверить Audit discipline в AGENTS.md | docs/verification-dashboard.yml | Выполнить ручную проверку и заполнить user_result в verification dashboard. |
| high | manual_verification | VERIFICATION-VT-EP-009-008 | EP-009-CODEX-SPEC-AUDIT | Проверить preservation audit findings | docs/verification-dashboard.yml | Выполнить ручную проверку и заполнить user_result в verification dashboard. |
| high | manual_verification | VERIFICATION-VT-EP-011-002 | EP-011-GIT-WORKFLOW-DISCIPLINE | Проверить Git workflow discipline в AGENTS.md | docs/verification-dashboard.yml | Выполнить ручную проверку и заполнить user_result в verification dashboard. |
| high | manual_verification | VERIFICATION-VT-EP-011-003 | EP-011-GIT-WORKFLOW-DISCIPLINE | Проверить branch naming policy | docs/verification-dashboard.yml | Выполнить ручную проверку и заполнить user_result в verification dashboard. |
| high | manual_verification | VERIFICATION-VT-EP-011-004 | EP-011-GIT-WORKFLOW-DISCIPLINE | Проверить merge policy | docs/verification-dashboard.yml | Выполнить ручную проверку и заполнить user_result в verification dashboard. |
| high | manual_verification | VERIFICATION-VT-EP-011-008 | EP-011-GIT-WORKFLOW-DISCIPLINE | Проверить, что validator не выполняет Git mutations | docs/verification-dashboard.yml | Выполнить ручную проверку и заполнить user_result в verification dashboard. |
| high | user_action | USER-ACTION-DR-REF-FSNB-001 | - | Требуется локальный официальный или проектно разрешенный источник ФСНБ | data/questions/data-requirements.yml | Поместить файл источника в `data/reference/inbox/fsnb/` и указать authority, version, acquisition date и usage note. |
| high | user_action | USER-ACTION-DR-REF-KSI-001 | - | Требуется локальный официальный или проектно разрешенный источник КСИ | data/questions/data-requirements.yml | Поместить файл источника в `data/reference/inbox/ksi/` и указать authority, version, acquisition date и usage note. |
| high | user_action | USER-ACTION-DR-REF-WORK-TYPES-001 | - | Требуется локальный официальный или проектно разрешенный источник видов работ | data/questions/data-requirements.yml | Поместить файл источника в `data/reference/inbox/work_types/` и указать authority, version, acquisition date и usage note. |
| high | user_action | USER-ACTION-NR-RULE-PARTITION-BRICK-120-REINF-001 | - | Требуются официальные evidence references для правила сопоставления | data/questions/normative-review-questions.yml | Указать `source_id` и `normalized_record_id` для недостающих evidence fields: excluded_works, gesn_norm, included_works, ksi_process_code, ksi_result_code, norm_unit, resource_composition, technical_part_reference, work_type. |
| medium | manual_verification | VERIFICATION-VT-EP-005-003 | EP-005-ACCEPTANCE-AND-USER-ACTION-DASHBOARDS | Проверить, что accepted artifacts отображаются как protected | docs/verification-dashboard.yml | Выполнить ручную проверку и заполнить user_result в verification dashboard. |
| medium | manual_verification | VERIFICATION-VT-EP-006-001 | - | Проверить наличие monthly-plan.yml | docs/verification-dashboard.yml | Выполнить ручную проверку и заполнить user_result в verification dashboard. |
| medium | manual_verification | VERIFICATION-VT-EP-006-002 | - | Проверить, что месячный блок содержит ровно 3 задачи | docs/verification-dashboard.yml | Выполнить ручную проверку и заполнить user_result в verification dashboard. |
| medium | manual_verification | VERIFICATION-VT-EP-006-003 | - | Проверить, что каждая задача имеет 15 человеко-часов | docs/verification-dashboard.yml | Выполнить ручную проверку и заполнить user_result в verification dashboard. |
| medium | manual_verification | VERIFICATION-VT-EP-006-004 | - | Проверить наличие БФТ | docs/verification-dashboard.yml | Выполнить ручную проверку и заполнить user_result в verification dashboard. |
| medium | manual_verification | VERIFICATION-VT-EP-006-005 | - | Проверить наличие ТЗ | docs/verification-dashboard.yml | Выполнить ручную проверку и заполнить user_result в verification dashboard. |
| medium | manual_verification | VERIFICATION-VT-EP-006-006 | - | Проверить наличие протокола тестирования | docs/verification-dashboard.yml | Выполнить ручную проверку и заполнить user_result в verification dashboard. |
| medium | manual_verification | VERIFICATION-VT-EP-008-007 | EP-008-DISSERTATION-PROMPT-GENERATION | Проверить защиту accepted/protected artifacts | docs/verification-dashboard.yml | Выполнить ручную проверку и заполнить user_result в verification dashboard. |
| medium | manual_verification | VERIFICATION-VT-EP-009-010 | EP-009-CODEX-SPEC-AUDIT | Проверить, что EP-009 не mass-rewrite packet | docs/verification-dashboard.yml | Выполнить ручную проверку и заполнить user_result в verification dashboard. |

## 3. Пакеты ready_for_acceptance

| EP | Название | Команды | Блокеры | Риски | Где заполнить решение |
|---|---|---|---|---|---|
| - | - | - | - | - | - |

## 4. Ручные проверки

| ID | EP | Проверка | Как проверить | Где отметить |
|---|---|---|---|---|
| VT-EP-004-001 | EP-004-PROJECT-PLANNING-AND-ACCEPTANCE | Проверить наличие docs/project-plan.md | Открыть docs/project-plan.md. | docs/verification-dashboard.yml |
| VT-EP-004-002 | EP-004-PROJECT-PLANNING-AND-ACCEPTANCE | Проверить наличие docs/artifact-registry.yml | Открыть docs/artifact-registry.yml. | docs/verification-dashboard.yml |
| VT-EP-004-003 | EP-004-PROJECT-PLANNING-AND-ACCEPTANCE | Проверить, что accepted_by не может быть Codex | Открыть scripts/validate_project_plan.py. | docs/verification-dashboard.yml |
| VT-EP-005-004 | EP-005-ACCEPTANCE-AND-USER-ACTION-DASHBOARDS | Проверить, что open questions отображаются в user-action-dashboard | Открыть docs/user-action-dashboard.md. | docs/verification-dashboard.yml |
| VT-EP-007-001 | EP-007-VERIFICATION-DASHBOARD | Проверить наличие verification-dashboard.md | Открыть docs/verification-dashboard.md. | docs/verification-dashboard.yml |
| VT-EP-007-002 | EP-007-VERIFICATION-DASHBOARD | Проверить наличие verification-dashboard.yml | Открыть docs/verification-dashboard.yml. | docs/verification-dashboard.yml |
| VT-EP-007-003 | EP-007-VERIFICATION-DASHBOARD | Проверить, что manual checks не отмечены Codex как passed | Открыть docs/verification-dashboard.yml. | docs/verification-dashboard.yml |
| VT-EP-007-004 | EP-007-VERIFICATION-DASHBOARD | Проверить, что checked_by не может быть Codex | Открыть scripts/validate_verification_dashboard.py. | docs/verification-dashboard.yml |
| VT-EP-007-005 | EP-007-VERIFICATION-DASHBOARD | Проверить, что verification dashboard связан с протоколом тестирования | Открыть docs/monthly/2026-06/03-test-protocol-reference-data-governance.md. | docs/verification-dashboard.yml |
| VT-EP-008-001 | EP-008-DISSERTATION-PROMPT-GENERATION | Проверить наличие docs/dissertation/README.md | Открыть docs/dissertation/README.md. | docs/verification-dashboard.yml |
| VT-EP-008-002 | EP-008-DISSERTATION-PROMPT-GENERATION | Проверить наличие forbidden-claims.yml | Открыть docs/dissertation/prompt-profiles/forbidden-claims.yml. | docs/verification-dashboard.yml |
| VT-EP-008-006 | EP-008-DISSERTATION-PROMPT-GENERATION | Проверить, что acceptance_decision остается pending | Открыть docs/acceptance/EP-008-DISSERTATION-PROMPT-GENERATION.acceptance.md. | docs/verification-dashboard.yml |
| VT-EP-009-004 | EP-009-CODEX-SPEC-AUDIT | Проверить Language policy в AGENTS.md | Открыть AGENTS.md и найти раздел Language policy. | docs/verification-dashboard.yml |
| VT-EP-009-005 | EP-009-CODEX-SPEC-AUDIT | Проверить Audit discipline в AGENTS.md | Открыть AGENTS.md и найти раздел Audit discipline. | docs/verification-dashboard.yml |
| VT-EP-009-008 | EP-009-CODEX-SPEC-AUDIT | Проверить preservation audit findings | Открыть scripts/audit_codex_spec.py и scripts/audit_language_policy.py. | docs/verification-dashboard.yml |
| VT-EP-011-002 | EP-011-GIT-WORKFLOW-DISCIPLINE | Проверить Git workflow discipline в AGENTS.md | Открыть AGENTS.md и найти раздел Git workflow discipline. | docs/verification-dashboard.yml |
| VT-EP-011-003 | EP-011-GIT-WORKFLOW-DISCIPLINE | Проверить branch naming policy | Открыть docs/git-workflow.md. | docs/verification-dashboard.yml |
| VT-EP-011-004 | EP-011-GIT-WORKFLOW-DISCIPLINE | Проверить merge policy | Открыть docs/git-workflow.md и AGENTS.md. | docs/verification-dashboard.yml |
| VT-EP-011-008 | EP-011-GIT-WORKFLOW-DISCIPLINE | Проверить, что validator не выполняет Git mutations | Открыть scripts/validate_git_workflow.py. | docs/verification-dashboard.yml |
| VT-EP-005-003 | EP-005-ACCEPTANCE-AND-USER-ACTION-DASHBOARDS | Проверить, что accepted artifacts отображаются как protected | Открыть docs/acceptance-dashboard.md. | docs/verification-dashboard.yml |
| VT-EP-006-001 | - | Проверить наличие monthly-plan.yml | Открыть docs/monthly/monthly-plan.yml. | docs/verification-dashboard.yml |
| VT-EP-006-002 | - | Проверить, что месячный блок содержит ровно 3 задачи | Открыть docs/monthly/monthly-plan.yml. | docs/verification-dashboard.yml |
| VT-EP-006-003 | - | Проверить, что каждая задача имеет 15 человеко-часов | Открыть docs/monthly/monthly-plan.yml. | docs/verification-dashboard.yml |
| VT-EP-006-004 | - | Проверить наличие БФТ | Открыть docs/monthly/2026-06/01-bft-reference-data-governance.md. | docs/verification-dashboard.yml |
| VT-EP-006-005 | - | Проверить наличие ТЗ | Открыть docs/monthly/2026-06/02-technical-task-reference-data-governance.md. | docs/verification-dashboard.yml |
| VT-EP-006-006 | - | Проверить наличие протокола тестирования | Открыть docs/monthly/2026-06/03-test-protocol-reference-data-governance.md. | docs/verification-dashboard.yml |
| VT-EP-008-007 | EP-008-DISSERTATION-PROMPT-GENERATION | Проверить защиту accepted/protected artifacts | Открыть docs/acceptance-dashboard.md. | docs/verification-dashboard.yml |
| VT-EP-009-010 | EP-009-CODEX-SPEC-AUDIT | Проверить, что EP-009 не mass-rewrite packet | Проверить git diff. | docs/verification-dashboard.yml |

## 5. Вопросы и user actions

| ID | Вопрос | Что требуется | Блокирует | Где ответить |
|---|---|---|---|---|
| DR-REF-FSNB-001 | Требуется локальный официальный или проектно разрешенный источник ФСНБ | Поместить файл источника в `data/reference/inbox/fsnb/` и указать authority, version, acquisition date и usage note. | активацию правил сопоставления, которым нужен этот тип справочного источника | data/questions/data-requirements.yml |
| DR-REF-KSI-001 | Требуется локальный официальный или проектно разрешенный источник КСИ | Поместить файл источника в `data/reference/inbox/ksi/` и указать authority, version, acquisition date и usage note. | активацию правил сопоставления, которым нужен этот тип справочного источника | data/questions/data-requirements.yml |
| DR-REF-WORK-TYPES-001 | Требуется локальный официальный или проектно разрешенный источник видов работ | Поместить файл источника в `data/reference/inbox/work_types/` и указать authority, version, acquisition date и usage note. | активацию правил сопоставления, которым нужен этот тип справочного источника | data/questions/data-requirements.yml |
| NR-RULE-PARTITION-BRICK-120-REINF-001 | Требуются официальные evidence references для правила сопоставления | Указать `source_id` и `normalized_record_id` для недостающих evidence fields: excluded_works, gesn_norm, included_works, ksi_process_code, ksi_result_code, norm_unit, resource_composition, technical_part_reference, work_type. | активацию правила | data/questions/normative-review-questions.yml |

## 6. Requires user approval

| ID | Объект | Причина | Что требуется |
|---|---|---|---|
| - | - | - | - |

## 7. Audit findings critical/high

| ID | Severity | Файл | Проблема | Рекомендация |
|---|---|---|---|---|
| - | - | - | - | - |

## 7.1. Grouped historical audit findings

| Group | Severity | Total | Current | Historical | Active blocking | Recommendation |
|---|---|---:|---:|---:|---|---|
| AUD-ACCEPT-CODEX-USER-FIELD | critical | 171 | 0 | 171 | False | Historical findings are preserved but hidden from active_review_items while current_detected=false. |
| AUD-GIT-001 | medium | 2 | 0 | 2 | False | Historical findings are preserved but hidden from active_review_items while current_detected=false. |
| AUD-GIT-002 | medium | 6 | 0 | 6 | False | Historical findings are preserved but hidden from active_review_items while current_detected=false. |
| AUD-GIT-005 | medium | 1 | 0 | 1 | False | Historical findings are preserved but hidden from active_review_items while current_detected=false. |
| AUD-GIT-006 | medium | 13 | 0 | 13 | False | Historical findings are preserved but hidden from active_review_items while current_detected=false. |
| AUD-LANG-001 | medium | 251 | 80 | 171 | False | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. |

## 8. Как принять EP через единое окно

1. Выполнить команды проверки, указанные для EP.
2. Проверить blockers и risks.
3. Заполнить `user_decision` в `docs/user-review-workbench.yml`.
4. Запустить `make apply-user-review-decisions-dry-run`.
5. Проверить dry-run diff, список affected files и reasons.
6. Убедиться, что dry-run не меняет чужие acceptance reports и Codex не заполняет user-owned поля.
7. Только после просмотра dry-run diff запустить `make apply-user-review-decisions`.
8. Запустить `make generate-dashboards`.
9. Запустить `make validate-plan`.
10. Запустить `make check`.
11. Убедиться, что принятый EP исчез из `active_review_items`, но сохранился в acceptance report и dashboards.

## 9. Post-acceptance baseline

Accepted packets are hidden from `active_review_items`; acceptance reports remain the source of truth.

Accepted artifact protection is deferred to `EP-018-ACCEPTED-ARTIFACT-PROTECTION`.

## 10. Недавно принятые пакеты

| EP | Дата | Кем | Acceptance report |
|---|---|---|---|
| EP-001-INFRA | 2026-06-08 | Дмитрий | docs/acceptance/EP-001-INFRA.acceptance.md |
| EP-002-REFERENCE-GOVERNANCE | 2026-06-08 | Дмитрий | docs/acceptance/EP-002-REFERENCE-GOVERNANCE.acceptance.md |
| EP-003-REFERENCE-VERSIONING | 2026-06-08 | Дмитрий | docs/acceptance/EP-003-REFERENCE-VERSIONING.acceptance.md |
| EP-004-PROJECT-PLANNING-AND-ACCEPTANCE | 2026-06-08 | Дмитрий | docs/acceptance/EP-004-PROJECT-PLANNING-AND-ACCEPTANCE.acceptance.md |
| EP-005-ACCEPTANCE-AND-USER-ACTION-DASHBOARDS | 2026-06-08 | Дмитрий | docs/acceptance/EP-005-ACCEPTANCE-AND-USER-ACTION-DASHBOARDS.acceptance.md |
| EP-007-VERIFICATION-DASHBOARD | 2026-06-08 | Дмитрий | docs/acceptance/EP-007-VERIFICATION-DASHBOARD.acceptance.md |
| EP-008-DISSERTATION-PROMPT-GENERATION | 2026-06-08 | Дмитрий | docs/acceptance/EP-008-DISSERTATION-PROMPT-GENERATION.acceptance.md |
| EP-009-CODEX-SPEC-AUDIT | 2026-06-08 | Дмитрий | docs/acceptance/EP-009-CODEX-SPEC-AUDIT.acceptance.md |
| EP-010-LANGUAGE-NORMALIZATION | 2026-06-10 | Дмитрий | docs/acceptance/EP-010-LANGUAGE-NORMALIZATION.acceptance.md |
| EP-011-GIT-WORKFLOW-DISCIPLINE | 2026-06-08 | Дмитрий | docs/acceptance/EP-011-GIT-WORKFLOW-DISCIPLINE.acceptance.md |
| EP-012-USER-REVIEW-WORKBENCH-AND-ACCEPTANCE-STANDARD | 2026-06-08 | Дмитрий | docs/acceptance/EP-012-USER-REVIEW-WORKBENCH-AND-ACCEPTANCE-STANDARD.acceptance.md |
| EP-013-POST-ACCEPTANCE-STATE-SYNC | 2026-06-09 | Дмитрий | docs/acceptance/EP-013-POST-ACCEPTANCE-STATE-SYNC.acceptance.md |
| EP-014-USER-REVIEW-DECISION-CLI-SAFETY | 2026-06-10 | Дмитрий | docs/acceptance/EP-014-USER-REVIEW-DECISION-CLI-SAFETY.acceptance.md |
| EP-015-VERIFICATION-DASHBOARD-RECONCILIATION | 2026-06-11 | Дмитрий | docs/acceptance/EP-015-VERIFICATION-DASHBOARD-RECONCILIATION.acceptance.md |
| EP-017-AUDIT-FINDINGS-CLEANUP | 2026-06-12 | Дмитрий | docs/acceptance/EP-017-AUDIT-FINDINGS-CLEANUP.acceptance.md |
| EP-018-ACCEPTED-ARTIFACT-PROTECTION | 2026-06-10 | Дмитрий | docs/acceptance/EP-018-ACCEPTED-ARTIFACT-PROTECTION.acceptance.md |
| EP-019-CODEX-CONTEXT-COMPACTION | 2026-06-12 | Дмитрий | docs/acceptance/EP-019-CODEX-CONTEXT-COMPACTION.acceptance.md |
| EP-021-POST-ACCEPTANCE-SYNC-AUTOMATION | 2026-06-12 | Дмитрий | docs/acceptance/EP-021-POST-ACCEPTANCE-SYNC-AUTOMATION.acceptance.md |
| EP-022A-CUSTOMER-FACING-MVP-ROADMAP-AND-MONTHLY-PLANNING | 2026-06-13 | Дмитрий | docs/acceptance/EP-022A-CUSTOMER-FACING-MVP-ROADMAP-AND-MONTHLY-PLANNING.acceptance.md |
| EP-022B-LEGAL-DATA-BOUNDARY-POLICY-NOTES | 2026-06-13 | Дмитрий | docs/acceptance/EP-022B-LEGAL-DATA-BOUNDARY-POLICY-NOTES.acceptance.md |
| EP-023-MONTH-01-INFRASTRUCTURE-CUSTOMER-DOCUMENTS | 2026-06-13 | Дмитрий | docs/acceptance/EP-023-MONTH-01-INFRASTRUCTURE-CUSTOMER-DOCUMENTS.acceptance.md |
