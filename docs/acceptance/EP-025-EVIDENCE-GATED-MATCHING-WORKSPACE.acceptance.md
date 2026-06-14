# EP-025-EVIDENCE-GATED-MATCHING-WORKSPACE Acceptance Report

## 1. Статус Codex

ready_for_acceptance

## 2. Пользовательское решение

```yaml
acceptance_decision: accepted
accepted_by: Дмитрий
accepted_at: 2026-06-14
comments: Принято. Проверено: создан draft-only Evidence-Gated Matching Workspace для вертикального сценария перегородки 120 мм; реальные КСИ/ГЭСН/ФСНБ данные не добавлены; active matching rules не создавались; нормативные значения оставлены как placeholders/null и требуют официальных источников; project-authorized источники не трактуются как подтверждение official normative status; запрещенные прямые связи BIM/КСИ/ГЭСН/календарь/факт не созданы; ActualRecord связан через WorkPackage/зону/захватку, а не напрямую с одиночным ModelElement; BIM-КСИ-ГЭСН методика не изменена; protected/manual artifacts и accepted reports других EP не изменены; user-owned поля Codex не заполнял; make verify и make check прошли.
```

## 3. Результат strict baseline

Перед стартом EP-025 проверено состояние после принятого `EP-024-DATA-CONTRIBUTION-AND-ANONYMIZATION-LAYER`:

```yaml
state_mode: accepted_baseline
active_execution_packet: none
last_accepted_execution_packet: EP-024-DATA-CONTRIBUTION-AND-ANONYMIZATION-LAYER
last_completed_execution_packet: EP-024-DATA-CONTRIBUTION-AND-ANONYMIZATION-LAYER
next_recommended_packet: EP-025-EVIDENCE-GATED-MATCHING-WORKSPACE
deferred_follow_up_packets: []
```

Working tree перед созданием ветки был clean. Ветка `ep-025-evidence-gated-matching-workspace` создана для текущего execution packet.

## 4. Созданные артефакты

Созданы matching workspace documents:

- `docs/matching-workspace/README.md`;
- `docs/matching-workspace/evidence-gated-workflow.md`.

Созданы domain schemas:

- `schemas/domain/matching-workspace-session.schema.yml`;
- `schemas/domain/matching-workspace-group.schema.yml`;
- `schemas/domain/evidence-slot.schema.yml`;
- `schemas/domain/calculation-unit-candidate.schema.yml`;
- `schemas/domain/work-quantity.schema.yml`;
- `schemas/domain/work-package.schema.yml`;
- `schemas/domain/actual-record.schema.yml`;
- `schemas/domain/plan-fact-comparison.schema.yml`.

Создан vertical scenario:

- `examples/vertical-scenarios/partition-brick-120-reinf.workspace.yml`.

Обновлены data requirements:

- `data/questions/data-requirements.yml`.

Созданы validator and tests:

- `scripts/validate_matching_workspace.py`;
- `tests/test_validate_matching_workspace.py`.

Созданы September monthly documents:

- `docs/monthly/2026-09/monthly-plan.yml`;
- `docs/monthly/2026-09/01-business-functional-requirements.md`;
- `docs/monthly/2026-09/02-technical-specification.md`;
- `docs/monthly/2026-09/03-test-protocol-matching-workspace.md`.

## 5. Safety statements

- Реальные classifier/normative/customer data не добавлялись.
- Active matching rules не создавались.
- Official classifier/normative fields оставлены `null` и требуют official source.
- `source_origin: llm_generated` запрещен как evidence.
- `user_decision` не подтверждает official classifier/normative fields.
- Actual records связаны через `WorkPackage` / zone context.
- Schedule tasks связаны через `WorkPackage`.
- Calculation unit candidate не хранит fact context.
- Backend runtime, web UI, database tables и migrations не создавались.
- `README.md`, `CHANGELOG.md`, `AGENTS.md`, `docs/01-methodology.md` и `docs/02-domain-model.md` не изменялись.
- Accepted reports других EP не изменялись.
- CHANGELOG.md не изменялся из-за scope/protected-artifact ограничения текущего execution packet.

## 6. Acceptance criteria

- Создан schema-first/documentation-first Evidence-Gated Matching Workspace.
- Создан draft-only vertical scenario для кирпичной армированной перегородки 120 мм.
- Scenario имеет `status: draft_requires_data`, `normative_status: not_active`, `evidence_status: missing_official_sources`, `activation_allowed: false`.
- Potential official fields имеют `value: null`, `requires_official_source: true`, `question_id`, `review_status: pending_user_input`.
- Validator проверяет forbidden domain edges, evidence gates, inactive status и WorkPackage mediation.
- Makefile содержит `validate-matching-workspace`, подключенный к `make verify` и `make check`.
- Создан monthly block 2026-09 с тремя задачами по 15 часов.
- EP-025 остается `ready_for_acceptance` и не добавлен в `accepted_packets`.
- User-owned fields не заполнены Codex.

## 7. Блокеры

## 8. Риски

## 9. Результаты проверки

- `PYTHONPYCACHEPREFIX=/private/tmp/tartip-pycache python3 -m py_compile scripts/validate_matching_workspace.py` — passed.
- `PYTHONPYCACHEPREFIX=/private/tmp/tartip-pycache python3 -m pytest tests/test_validate_matching_workspace.py` — blocked by environment: system `python3` has no `pytest` module.
- `PYTHONPYCACHEPREFIX=/private/tmp/tartip-pycache .venv/bin/python -m pytest tests/test_validate_matching_workspace.py` — passed, 16 tests.
- `python3 scripts/validate_matching_workspace.py examples/vertical-scenarios/partition-brick-120-reinf.workspace.yml` — passed.
- Поиск активных нормативных маркеров, числовых official-code placeholders и `activation_allowed: true` в артефактах EP-025 — passed, no matches.
- Поиск запрещенных прямых domain edges в артефактах EP-025 — passed, no matches.
- Поиск user-owned acceptance/check fields, заполненных Codex или заранее отмеченных как accepted/passed, в артефактах EP-025 — passed, no matches.
- `make generate-dashboards` — passed.
- `make validate-plan` — passed.
- `make validate-user-review-workbench` — passed.
- `make validate-post-acceptance-state` — passed.
- `make validate-verification` — passed.
- `make validate-accepted-artifact-protection` — passed.
- `make validate-audit` — passed.
- `make validate-matching-workspace` — passed.
- `make verify` — passed.
- `make check` — passed.

## 10. Project-state notes

На стадии `ready_for_acceptance`:

```yaml
state_mode: ready_for_acceptance
active_execution_packet: EP-025-EVIDENCE-GATED-MATCHING-WORKSPACE
last_accepted_execution_packet: EP-024-DATA-CONTRIBUTION-AND-ANONYMIZATION-LAYER
last_completed_execution_packet: EP-024-DATA-CONTRIBUTION-AND-ANONYMIZATION-LAYER
next_recommended_packet: none
deferred_follow_up_packets: []
```

EP-025 не добавлен в `accepted_packets`.

## 11. Dissertation impact

```yaml
dissertation_impact: none
reason: EP-025 создает engineering governance и schema-first draft workspace для проекта Tartip, но не меняет научное содержание, методику исследования, источники или DOCX/PDF артефакты диссертации.
generated_prompts: []
```

## 12. User acceptance checklist

Пользователю нужно проверить:

- scenario не содержит official classifier/normative values;
- evidence slots корректно требуют official source и user review;
- WorkPackage действительно является production context между quantities, planning и facts;
- validator покрывает hard domain prohibitions;
- September monthly documents не заявляют activation или production deployment.
