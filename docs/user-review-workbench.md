# Единое активное окно проверки пользователем

Дата обновления: 2026-06-09

## 1. Сводка

| Раздел | Количество |
|---|---:|
| Активные элементы проверки | 34 |
| Пакеты готовы к приемке | 2 |
| Ручные проверки ожидают выполнения | 28 |
| Вопросы требуют ответа | 4 |
| Требуют user approval | 0 |
| Critical audit findings | 0 |
| High audit findings | 0 |
| Активные блокеры | 9 |
| Принятые пакеты скрыты из активной очереди | 8 |

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
| medium | acceptance | ACCEPTANCE-EP-009-CODEX-SPEC-AUDIT | EP-009-CODEX-SPEC-AUDIT | Codex specification audit and language policy | docs/acceptance/EP-009-CODEX-SPEC-AUDIT.acceptance.md | Проверить acceptance report, выполнить команды и заполнить решение пользователя. |
| medium | acceptance | ACCEPTANCE-EP-011-GIT-WORKFLOW-DISCIPLINE | EP-011-GIT-WORKFLOW-DISCIPLINE | Git workflow discipline | docs/acceptance/EP-011-GIT-WORKFLOW-DISCIPLINE.acceptance.md | Проверить acceptance report, выполнить команды и заполнить решение пользователя. |
| medium | manual_verification | VERIFICATION-VT-EP-005-003 | EP-005-ACCEPTANCE-AND-USER-ACTION-DASHBOARDS | Проверить, что accepted artifacts отображаются как protected | docs/verification-dashboard.yml | Выполнить ручную проверку и заполнить user_result в verification dashboard. |
| medium | manual_verification | VERIFICATION-VT-EP-006-001 | EP-006-MONTHLY-PLANNING-AND-DEFENSE | Проверить наличие monthly-plan.yml | docs/verification-dashboard.yml | Выполнить ручную проверку и заполнить user_result в verification dashboard. |
| medium | manual_verification | VERIFICATION-VT-EP-006-002 | EP-006-MONTHLY-PLANNING-AND-DEFENSE | Проверить, что месячный блок содержит ровно 3 задачи | docs/verification-dashboard.yml | Выполнить ручную проверку и заполнить user_result в verification dashboard. |
| medium | manual_verification | VERIFICATION-VT-EP-006-003 | EP-006-MONTHLY-PLANNING-AND-DEFENSE | Проверить, что каждая задача имеет 15 человеко-часов | docs/verification-dashboard.yml | Выполнить ручную проверку и заполнить user_result в verification dashboard. |
| medium | manual_verification | VERIFICATION-VT-EP-006-004 | EP-006-MONTHLY-PLANNING-AND-DEFENSE | Проверить наличие БФТ | docs/verification-dashboard.yml | Выполнить ручную проверку и заполнить user_result в verification dashboard. |
| medium | manual_verification | VERIFICATION-VT-EP-006-005 | EP-006-MONTHLY-PLANNING-AND-DEFENSE | Проверить наличие ТЗ | docs/verification-dashboard.yml | Выполнить ручную проверку и заполнить user_result в verification dashboard. |
| medium | manual_verification | VERIFICATION-VT-EP-006-006 | EP-006-MONTHLY-PLANNING-AND-DEFENSE | Проверить наличие протокола тестирования | docs/verification-dashboard.yml | Выполнить ручную проверку и заполнить user_result в verification dashboard. |
| medium | manual_verification | VERIFICATION-VT-EP-008-007 | EP-008-DISSERTATION-PROMPT-GENERATION | Проверить защиту accepted/protected artifacts | docs/verification-dashboard.yml | Выполнить ручную проверку и заполнить user_result в verification dashboard. |
| medium | manual_verification | VERIFICATION-VT-EP-009-010 | EP-009-CODEX-SPEC-AUDIT | Проверить, что EP-009 не mass-rewrite packet | docs/verification-dashboard.yml | Выполнить ручную проверку и заполнить user_result в verification dashboard. |

## 3. Пакеты ready_for_acceptance

| EP | Название | Команды | Блокеры | Риски | Где заполнить решение |
|---|---|---|---|---|---|
| EP-009-CODEX-SPEC-AUDIT | Codex specification audit and language policy | make audit-codex-spec, make audit-language, make validate-audit, make audit, make generate-dashboards, make generate-verification-dashboard, make validate-verification, make validate-plan, make check, make validate-reference, pytest | User acceptance decision remains pending until Дмитрий reviews the audit contour.; Future fixes for language findings require a separate follow-up packet; EP-009 intentionally does not mass-russify existing documents. | Existing user-facing documents contain English text; EP-009 records this as language findings instead of mass translation.; If a future packet changes accepted/protected artifacts, it must create a change request or requires_user_approval action first.; Audit heuristics for language detection may produce false positives and require user review. | docs/acceptance/EP-009-CODEX-SPEC-AUDIT.acceptance.md |
| EP-011-GIT-WORKFLOW-DISCIPLINE | Git workflow discipline | make validate-git-workflow, make audit, make validate-plan, make check | Current working tree already contains pre-existing uncommitted changes from earlier packets on `main`.; EP-011 acceptance decision remains pending until Дмитрий reviews the packet.; Merge is forbidden until user acceptance and explicit merge approval exist. | Existing dirty baseline makes branch creation/switching unsafe without user approval.; Advisory validator intentionally reports warnings for current baseline without failing.; Strict validator is expected to fail while branch mismatch, mixed EP scopes, or merge blockers remain. | docs/acceptance/EP-011-GIT-WORKFLOW-DISCIPLINE.acceptance.md |

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
| VT-EP-006-001 | EP-006-MONTHLY-PLANNING-AND-DEFENSE | Проверить наличие monthly-plan.yml | Открыть docs/monthly/monthly-plan.yml. | docs/verification-dashboard.yml |
| VT-EP-006-002 | EP-006-MONTHLY-PLANNING-AND-DEFENSE | Проверить, что месячный блок содержит ровно 3 задачи | Открыть docs/monthly/monthly-plan.yml. | docs/verification-dashboard.yml |
| VT-EP-006-003 | EP-006-MONTHLY-PLANNING-AND-DEFENSE | Проверить, что каждая задача имеет 15 человеко-часов | Открыть docs/monthly/monthly-plan.yml. | docs/verification-dashboard.yml |
| VT-EP-006-004 | EP-006-MONTHLY-PLANNING-AND-DEFENSE | Проверить наличие БФТ | Открыть docs/monthly/2026-06/01-bft-reference-data-governance.md. | docs/verification-dashboard.yml |
| VT-EP-006-005 | EP-006-MONTHLY-PLANNING-AND-DEFENSE | Проверить наличие ТЗ | Открыть docs/monthly/2026-06/02-technical-task-reference-data-governance.md. | docs/verification-dashboard.yml |
| VT-EP-006-006 | EP-006-MONTHLY-PLANNING-AND-DEFENSE | Проверить наличие протокола тестирования | Открыть docs/monthly/2026-06/03-test-protocol-reference-data-governance.md. | docs/verification-dashboard.yml |
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

## 8. Как принять EP через единое окно

1. Выполнить команды проверки, указанные для EP.
2. Проверить blockers и risks.
3. Заполнить `user_decision` в `docs/user-review-workbench.yml`.
4. Запустить `make apply-user-review-decisions`.
5. Запустить `make generate-dashboards`.
6. Запустить `make validate-plan`.
7. Запустить `make check`.
8. Убедиться, что принятый EP исчез из `active_review_items`, но сохранился в acceptance report и dashboards.

## 9. Недавно принятые пакеты

| EP | Дата | Кем | Acceptance report |
|---|---|---|---|
| EP-001-INFRA | 2026-06-08 | Дмитрий | docs/acceptance/EP-001-INFRA.acceptance.md |
| EP-002-REFERENCE-GOVERNANCE | 2026-06-08 | Дмитрий | docs/acceptance/EP-002-REFERENCE-GOVERNANCE.acceptance.md |
| EP-003-REFERENCE-VERSIONING | 2026-06-08 | Дмитрий | docs/acceptance/EP-003-REFERENCE-VERSIONING.acceptance.md |
| EP-004-PROJECT-PLANNING-AND-ACCEPTANCE | 2026-06-08 | Дмитрий | docs/acceptance/EP-004-PROJECT-PLANNING-AND-ACCEPTANCE.acceptance.md |
| EP-005-ACCEPTANCE-AND-USER-ACTION-DASHBOARDS | 2026-06-08 | Дмитрий | docs/acceptance/EP-005-ACCEPTANCE-AND-USER-ACTION-DASHBOARDS.acceptance.md |
| EP-007-VERIFICATION-DASHBOARD | 2026-06-08 | Дмитрий | docs/acceptance/EP-007-VERIFICATION-DASHBOARD.acceptance.md |
| EP-008-DISSERTATION-PROMPT-GENERATION | 2026-06-08 | Дмитрий | docs/acceptance/EP-008-DISSERTATION-PROMPT-GENERATION.acceptance.md |
| EP-012-USER-REVIEW-WORKBENCH-AND-ACCEPTANCE-STANDARD | 2026-06-08 | Дмитрий | docs/acceptance/EP-012-USER-REVIEW-WORKBENCH-AND-ACCEPTANCE-STANDARD.acceptance.md |
