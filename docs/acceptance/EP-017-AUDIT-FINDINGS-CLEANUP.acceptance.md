# Acceptance Report — EP-017-AUDIT-FINDINGS-CLEANUP

## 1. Сводка

- Execution packet: EP-017-AUDIT-FINDINGS-CLEANUP
- Статус Codex: ready_for_acceptance
- Владелец приемки: Дмитрий
- Дата подготовки: 2026-06-11

EP-017 сокращает шум в audit findings, user-action-dashboard и user-review-workbench. Пакет сохраняет историю audit findings, не закрывает findings как `fixed`, не меняет пользовательские решения и не затрагивает BIM-КСИ-ГЭСН методику.

## 2. Область изменений

- `current_detected: false` findings исключены из active review/action windows.
- Historical/stale findings сохранены в `docs/audit/audit-findings.yml`.
- Добавлен deterministic grouped layer `audit_finding_groups`.
- `docs/user-review-workbench.md` показывает компактный top-N список active critical/high findings и grouped historical summary.
- `docs/user-action-dashboard.*` не показывает stale historical findings как urgent/current user actions.
- `docs/audit/codex-spec-audit.md` разделяет active findings и historical/stale finding groups.
- EP-017 зарегистрирован в `docs/grace/execution-packets.xml`.

## 3. Артефакты

| Артефакт | Тип | Статус |
|---|---|---|
| `scripts/audit_codex_spec.py` | audit generator | updated |
| `scripts/generate_user_action_dashboard.py` | dashboard generator | updated |
| `scripts/generate_user_review_workbench.py` | workbench generator | updated |
| `scripts/validate_user_review_workbench.py` | validator | updated |
| `docs/audit/audit-findings.yml` | generated audit registry | generated |
| `docs/audit/codex-spec-audit.md` | generated audit report | generated |
| `docs/user-action-dashboard.md` | generated dashboard | generated |
| `docs/user-action-dashboard.yml` | generated dashboard | generated |
| `docs/user-review-workbench.md` | generated workbench | generated |
| `docs/user-review-workbench.yml` | generated workbench | generated |
| `docs/grace/execution-packets.xml` | GRACE packet registry | updated |
| `docs/grace/verification-plan.xml` | GRACE verification plan | updated |
| `docs/artifact-registry.yml` | artifact registry | updated |
| `docs/project-state.yml` | project state | updated |
| `docs/project-plan.md` | planning document | updated |
| `docs/status-report.md` | status report | updated |
| `docs/traceability-matrix.md` | traceability matrix | updated |

## 4. Проверки

```sh
make regenerate
python3 -m py_compile scripts/audit_codex_spec.py scripts/generate_user_action_dashboard.py scripts/generate_user_review_workbench.py scripts/validate_user_review_workbench.py
make validate-user-review-workbench
make validate-post-acceptance-state
make validate-accepted-artifact-protection
make verify
make check
```

## 5. Критерии приемки

| ID | Критерий | Статус Codex | Решение пользователя |
|---|---|---|---|
| AC-EP-017-001 | EP-015 был принят и синхронизирован до старта EP-017. | ready_for_acceptance | pending |
| AC-EP-017-002 | `docs/project-state.yml` указывает EP-017 как active packet и после проверок имеет `state_mode: ready_for_acceptance`. | ready_for_acceptance | pending |
| AC-EP-017-003 | EP-017 зарегистрирован как `ready_for_acceptance` и не `accepted`. | ready_for_acceptance | pending |
| AC-EP-017-004 | `current_detected: false` findings не попадают в `active_review_items`. | ready_for_acceptance | pending |
| AC-EP-017-005 | `current_detected: false` findings не считаются active blockers. | ready_for_acceptance | pending |
| AC-EP-017-006 | Historical audit findings сохранены. | ready_for_acceptance | pending |
| AC-EP-017-007 | Однотипные stale findings сгруппированы детерминированно. | ready_for_acceptance | pending |
| AC-EP-017-008 | Workbench Markdown стал top-N/grouped и не выводит сотни однотипных строк. | ready_for_acceptance | pending |
| AC-EP-017-009 | User-action dashboard не показывает stale findings как urgent user actions. | ready_for_acceptance | pending |
| AC-EP-017-010 | Audit report разделяет active и historical findings. | ready_for_acceptance | pending |
| AC-EP-017-011 | Codex не заполнял `resolved_by` и user-owned fields. | ready_for_acceptance | pending |
| AC-EP-017-012 | Accepted reports других EP не изменялись. | ready_for_acceptance | pending |
| AC-EP-017-013 | `README.md`, `CHANGELOG.md`, `AGENTS.md` не изменялись. | ready_for_acceptance | pending |
| AC-EP-017-014 | BIM-КСИ-ГЭСН методика и нормативные данные не изменялись. | ready_for_acceptance | pending |
| AC-EP-017-015 | `make verify` остается read-only. | ready_for_acceptance | pending |

## 6. Нерешенные вопросы

## 7. Блокеры

## 8. Риски

## 9. User-owned решение

```yaml
acceptance_decision: accepted
accepted_by: Дмитрий
accepted_at: 2026-06-12
comments: Принято. Проверено: stale audit findings с current_detected=false не попадают в active review/action windows; audit history сохранена; findings не удалялись; status/resolution fields не менялись; resolved_by: Codex не выставлялся; workbench и user-action dashboard больше не показывают stale findings как active blockers; make verify и make check проходят; README.md, CHANGELOG.md, AGENTS.md и accepted reports других EP не изменены; BIM-КСИ-ГЭСН методика и нормативные данные не изменялись.
```

## 10. Следующий шаг

Пользователь проверяет grouped historical findings, active review/action windows, результаты проверок и вручную принимает или возвращает EP-017 на доработку.
