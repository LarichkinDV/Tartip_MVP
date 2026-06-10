# Decision Log

| ID | Decision | Status | Rationale | Related Requirements |
|---|---|---|---|---|
| DEC-001 | Отказ от прямой связи BIM-элемент -> ГЭСН. | active | BIM-элемент не равен строительной работе; прямое сопоставление запрещено knowledge graph. | REQ-001 |
| DEC-002 | КСИ используется как классификационный слой. | active | КСИ не выбирает ГЭСН напрямую и не является нормативным источником. | REQ-002 |
| DEC-003 | `CalculationUnit` является нормативно-расчетным шаблоном. | active | Не хранит фактические данные и не является универсальным контейнером. | REQ-003 |
| DEC-004 | Фактические данные привязываются к `WorkPackage` / захватке. | active | `ActualRecord` не должен быть привязан только к одиночному `ModelElement`. | REQ-004 |
| DEC-005 | `No source — no rule`. | active | Нормативные и классификационные данные требуют источника и версии. | REQ-005 |
| DEC-006 | GRACE-light используется как дисциплина агентской разработки. | active | Execution packets, module contracts and verification scenarios задают безопасный контур изменений. | REQ-009 |
| DEC-007 | Справочники КСИ/ФСНБ версионируются дельтово. | active | Неизмененные записи не должны дублироваться между релизами. | REQ-007 |
| DEC-008 | Пользователь является единственным acceptance owner. | active | Codex готовит результат к приемке, но не принимает его. | REQ-008 |
| DEC-009 | Codex может ставить только `ready_for_acceptance`, но не `accepted`. | active | `accepted`, `rejected`, `needs_revision` являются пользовательскими решениями. | REQ-008 |
| DEC-010 | Синхронизация с диссертацией идет через impact log, prompt и markdown patch. | active | Tartip не должен редактировать DOCX напрямую или переносить инженерные детали как научный результат без пользовательского решения. | REQ-011 |
| DEC-011 | EP-009 работает как audit-first/read-mostly packet. | active | Аудит должен сначала фиксировать findings, сохранять пользовательские статусы и не выполнять массовую русификацию или исправление accepted/protected artifacts без user approval. | REQ-012 |
| DEC-012 | Git workflow связывает ветку с execution packet и запрещает merge без user acceptance. | active | Codex может валидировать Git state и готовить инструкции, но не выполняет merge в main без accepted packet, passed checks и явного user approval. | REQ-013 |

## DEC-EP-014-001 — Planning / Execution Packet Ordering

- Decision ID: DEC-EP-014-001
- Дата: 2026-06-10
- Тип решения: planning / execution packet ordering
- Решение: текущий EP-014 используется для `EP-014-USER-REVIEW-DECISION-CLI-SAFETY`.
- Перенос: ранее планировавшийся `EP-014-ACCEPTED-ARTIFACT-PROTECTION` переносится на `EP-018-ACCEPTED-ARTIFACT-PROTECTION`.
- Причина: перед дальнейшей автоматизацией пользовательских решений необходимо закрыть safety gap в `scripts/apply_user_review_decisions.py`: явный `--dry-run`, защищенный `--apply`, запрет неявной записи и защита user-owned полей.
- Impact: `EP-015`, `EP-016` и `EP-017` сохраняют свои назначения; пакет защиты accepted artifacts переносится на `EP-018`.
- Affected artifacts:
  - `docs/project-plan.md`
  - `docs/status-report.md`
  - `docs/grace/execution-packets.xml`
  - `docs/artifact-registry.yml`
  - `docs/traceability-matrix.md`
  - `docs/acceptance/EP-014-USER-REVIEW-DECISION-CLI-SAFETY.acceptance.md`
- Acceptance impact: EP-014 остается `ready_for_acceptance`; пользовательское решение остается `pending`.
- User approval: пользователь должен проверить и принять это решение при приемке EP-014.

## DEC-EP-018-001 — Accepted Artifact Protection Classification

- Decision ID: DEC-EP-018-001
- Дата: 2026-06-10
- Тип решения: governance / accepted artifact protection
- Решение: accepted source/manual artifacts классифицируются как protected в `docs/artifact-registry.yml`.
- Разделение: generated dashboards, generated workbench и generated audit reports не hard-lock; они классифицируются как derived/generated artifacts с `generator`, `derived_from` и `regeneration_command`.
- Change request: будущие изменения protected accepted artifacts требуют записи в `docs/protected-artifact-change-requests.yml` и explicit user approval.
- EP-010 guard: `EP-010-LANGUAGE-NORMALIZATION` не может менять protected accepted artifacts без approved change request.
- Affected artifacts:
  - `AGENTS.md`
  - `docs/artifact-registry.yml`
  - `docs/protected-artifact-change-requests.yml`
  - `docs/grace/execution-packets.xml`
  - `docs/grace/module-contracts.xml`
  - `docs/grace/verification-plan.xml`
  - `scripts/validate_accepted_artifact_protection.py`
  - `Makefile`
  - `docs/acceptance/EP-018-ACCEPTED-ARTIFACT-PROTECTION.acceptance.md`
- Acceptance impact: EP-018 получает статус `ready_for_acceptance`; пользовательское решение остается `pending`.
- User approval: пользователь должен проверить classification/protection metadata и принять или отклонить EP-018.
