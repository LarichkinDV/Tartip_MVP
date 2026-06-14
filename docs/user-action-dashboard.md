# Вопросы и действия для пользователя

Дата обновления: 2026-06-14

## 1. Сводка

| Категория | Количество |
|---|---:|
| open | 10 |
| high_priority | 10 |
| blocked | 10 |
| answered | 0 |
| closed | 0 |
| requires_user_approval | 0 |
| audit_finding_groups | 6 |
| historical_audit_finding_groups | 6 |

## 2. Срочные вопросы

| ID | Тип | Приоритет | Вопрос | Что требуется | Блокирует |
|---|---|---|---|---|---|
| DR-REF-KSI-001 | data_requirement | high | Provide a local official or project-authorized ksi source file and source metadata. | Place the source file in the target inbox path and provide source authority, version, acquisition date, and usage note. | active matching rules that require this reference source type |
| DR-REF-FSNB-001 | data_requirement | high | Provide a local official or project-authorized fsnb source file and source metadata. | Place the source file in the target inbox path and provide source authority, version, acquisition date, and usage note. | active matching rules that require this reference source type |
| DR-REF-WORK-TYPES-001 | data_requirement | high | Provide a local official or project-authorized work_types source file and source metadata. | Place the source file in the target inbox path and provide source authority, version, acquisition date, and usage note. | active matching rules that require this reference source type |
| DR-MW-KSI-001 | data_requirement | high | Предоставить official или project-authorized источник classifier result с версией и review metadata для draft workspace. | Source file или source reference с authority, version, checksum, acquisition note и review decision. | activation evidence slot DR-MW-KSI-001 |
| DR-MW-GESN-001 | data_requirement | high | Предоставить official или project-authorized normative source с версией и review metadata для candidate norm placeholder. | Source file или source reference с authority, version, checksum, acquisition note и review decision. | activation evidence slot DR-MW-GESN-001 |
| DR-MW-FSNB-001 | data_requirement | high | Предоставить official или project-authorized source version evidence для candidate normative placeholder. | Source version metadata с authority, checksum, acquisition note и review decision. | activation evidence slot DR-MW-FSNB-001 |
| DR-MW-NORMUNIT-001 | data_requirement | high | Предоставить official или project-authorized normative unit evidence для candidate calculation template. | Source file или source reference с authority, version, checksum, acquisition note и review decision. | activation evidence slot DR-MW-NORMUNIT-001 |
| DR-MW-WORKCOMP-001 | data_requirement | high | Предоставить official или project-authorized work composition evidence для candidate normative placeholder. | Source file или source reference с authority, version, checksum, acquisition note и review decision. | activation evidence slot DR-MW-WORKCOMP-001 |
| DR-MW-RESCOMP-001 | data_requirement | high | Предоставить official или project-authorized resource composition evidence для candidate normative placeholder. | Source file или source reference с authority, version, checksum, acquisition note и review decision. | activation evidence slot DR-MW-RESCOMP-001 |
| NR-RULE-PARTITION-BRICK-120-REINF-001 | normative_review | high | Provide official evidence references for missing matching rule evidence fields. | source_id and normalized_record_id for: excluded_works, gesn_norm, included_works, ksi_process_code, ksi_result_code, norm_unit, resource_composition, technical_part_reference, work_type | rule activation |

## 3. Требуют согласования пользователя

| ID | Вопрос | Причина | Затрагиваемые принятые артефакты | Что требуется |
|---|---|---|---|---|
| - | - | - | - | - |

## 4. Требования к данным

| ID | Вопрос | Ожидаемый файл / действие | Куда положить | Блокирует |
|---|---|---|---|---|
| DR-REF-KSI-001 | Provide a local official or project-authorized ksi source file and source metadata. | Place the source file in the target inbox path and provide source authority, version, acquisition date, and usage note. | data/reference/inbox/ksi/ | active matching rules that require this reference source type |
| DR-REF-FSNB-001 | Provide a local official or project-authorized fsnb source file and source metadata. | Place the source file in the target inbox path and provide source authority, version, acquisition date, and usage note. | data/reference/inbox/fsnb/ | active matching rules that require this reference source type |
| DR-REF-WORK-TYPES-001 | Provide a local official or project-authorized work_types source file and source metadata. | Place the source file in the target inbox path and provide source authority, version, acquisition date, and usage note. | data/reference/inbox/work_types/ | active matching rules that require this reference source type |
| DR-MW-KSI-001 | Предоставить official или project-authorized источник classifier result с версией и review metadata для draft workspace. | Source file или source reference с authority, version, checksum, acquisition note и review decision. | data/reference/inbox/ksi/ | activation evidence slot DR-MW-KSI-001 |
| DR-MW-GESN-001 | Предоставить official или project-authorized normative source с версией и review metadata для candidate norm placeholder. | Source file или source reference с authority, version, checksum, acquisition note и review decision. | data/reference/inbox/fsnb/ | activation evidence slot DR-MW-GESN-001 |
| DR-MW-FSNB-001 | Предоставить official или project-authorized source version evidence для candidate normative placeholder. | Source version metadata с authority, checksum, acquisition note и review decision. | data/reference/inbox/fsnb/ | activation evidence slot DR-MW-FSNB-001 |
| DR-MW-NORMUNIT-001 | Предоставить official или project-authorized normative unit evidence для candidate calculation template. | Source file или source reference с authority, version, checksum, acquisition note и review decision. | data/reference/inbox/fsnb/ | activation evidence slot DR-MW-NORMUNIT-001 |
| DR-MW-WORKCOMP-001 | Предоставить official или project-authorized work composition evidence для candidate normative placeholder. | Source file или source reference с authority, version, checksum, acquisition note и review decision. | data/reference/inbox/fsnb/ | activation evidence slot DR-MW-WORKCOMP-001 |
| DR-MW-RESCOMP-001 | Предоставить official или project-authorized resource composition evidence для candidate normative placeholder. | Source file или source reference с authority, version, checksum, acquisition note и review decision. | data/reference/inbox/fsnb/ | activation evidence slot DR-MW-RESCOMP-001 |

## 5. Вопросы сопоставления

| ID | Вопрос | Что нужно решить | Блокирует |
|---|---|---|---|
| - | - | - | - |

## 6. Нормативные проверки

| ID | Вопрос | Что проверить | Источник / файл | Блокирует |
|---|---|---|---|---|
| NR-RULE-PARTITION-BRICK-120-REINF-001 | Provide official evidence references for missing matching rule evidence fields. | source_id and normalized_record_id for: excluded_works, gesn_norm, included_works, ksi_process_code, ksi_result_code, norm_unit, resource_composition, technical_part_reference, work_type | rules/matching/partition_brick_120_reinf.yaml | rule activation |

## 7. Проектные решения

| ID | Вопрос | Варианты решения | Рекомендуемое действие |
|---|---|---|---|
| - | - | - | - |

## 8. Ошибки импорта

| ID | Проблема | Что нужно сделать | Файл |
|---|---|---|---|
| - | - | - | - |

## 9. Audit findings

| ID | Finding | Recommendation | File |
|---|---|---|---|
| - | - | - | - |

## 10. Audit findings требуют согласования

| ID | Finding | Recommendation | File |
|---|---|---|---|
| - | - | - | - |

## 11. Historical audit finding groups

| Group | Severity | Total | Current | Historical | Active blocking | Recommendation |
|---|---|---:|---:|---:|---|---|
| AUD-ACCEPT-CODEX-USER-FIELD | critical | 171 | 0 | 171 | False | Historical findings are preserved but hidden from active action windows while current_detected=false. |
| AUD-GIT-001 | medium | 2 | 0 | 2 | False | Historical findings are preserved but hidden from active action windows while current_detected=false. |
| AUD-GIT-002 | medium | 9 | 0 | 9 | False | Historical findings are preserved but hidden from active action windows while current_detected=false. |
| AUD-GIT-005 | medium | 1 | 0 | 1 | False | Historical findings are preserved but hidden from active action windows while current_detected=false. |
| AUD-GIT-006 | medium | 16 | 0 | 16 | False | Historical findings are preserved but hidden from active action windows while current_detected=false. |
| AUD-LANG-001 | medium | 251 | 80 | 171 | False | Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов. |

## 12. Закрытые вопросы

| ID | Решение | Дата | Кем принято |
|---|---|---|---|
| - | - | - | - |
