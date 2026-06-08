# Monthly Defense Dashboard

Дата обновления: 2026-06-08

## 1. Сводка

| Период | Плановые часы | Задачи | Статус |
|---|---:|---:|---|
| 2026-06 | 45 | 3 | ready_for_manual_review |

## 2. Артефакты месяца

| Артефакт | Назначение | Проверка |
|---|---|---|
| `docs/monthly/monthly-plan.yml` | План месяца | `VT-EP-006-001..003` |
| `docs/monthly/2026-06/01-bft-reference-data-governance.md` | БФТ | `VT-EP-006-004` |
| `docs/monthly/2026-06/02-technical-task-reference-data-governance.md` | ТЗ | `VT-EP-006-005` |
| `docs/monthly/2026-06/03-test-protocol-reference-data-governance.md` | Протокол тестирования | `VT-EP-006-006`, `VT-EP-007-005` |
| `docs/dissertation/README.md` | Контур синхронизации диссертации | `VT-EP-008-001..007` |
| `docs/audit/README.md` | Audit contour Codex-спецификации и language policy | `VT-EP-009-001..010` |
| `docs/git-workflow.md` | Git workflow discipline | `VT-EP-011-001..008` |

## 3. Источник факта выполнения проверок

Факт выполнения ручных и командных проверок фиксируется в:

- `docs/verification-dashboard.md`
- `docs/verification-dashboard.yml`

Monthly defense dashboard не заменяет verification dashboard и не является acceptance decision.

EP-008 dissertation synchronization checks remain manual/command checks in the verification dashboard. DOCX/PDF artifacts are not created by this dashboard.

EP-009 audit checks remain manual/command checks in the verification dashboard. Language findings are not acceptance decisions and must be reviewed by the user.

EP-011 Git workflow checks remain manual/command checks in the verification dashboard. Git operations such as add, commit, push, merge, branch switch, or branch deletion are not performed by this dashboard.
