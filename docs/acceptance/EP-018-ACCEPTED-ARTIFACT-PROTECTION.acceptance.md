# Acceptance Report — EP-018-ACCEPTED-ARTIFACT-PROTECTION

## 0. Правила заполнения

- Если блокеров нет, раздел `## 7. Блокеры` оставить пустым.
- Если рисков нет, раздел `## 8. Риски` оставить пустым.
- Не писать в пустых разделах `Отсутствуют`, `Нет`, `Блокеров нет`, `Рисков нет`, `None`, `No blockers`, `No risks`.
- Любая строка списка в разделе `## 7. Блокеры` считается реальным блокером.
- Любая строка списка в разделе `## 8. Риски` считается реальным риском.
- Codex не должен заполнять пользовательское решение за пользователя.

## 1. Пакет

- Execution packet: EP-018-ACCEPTED-ARTIFACT-PROTECTION
- Статус Codex: ready_for_acceptance
- Acceptance owner: Дмитрий
- Дата подготовки: 2026-06-10

## 2. Что реализовано

- В `AGENTS.md` уточнена дисциплина accepted artifact protection: защищаются source/manual accepted artifacts, а generated dashboards остаются производными и пересоздаваемыми.
- В `docs/artifact-registry.yml` добавлен блок `protection` для зарегистрированных артефактов.
- Принятые acceptance reports EP-001–EP-014 классифицированы как `protection_status: protected` и `source_category: source_acceptance`.
- Source/manual governance artifacts классифицированы как protected, включая `AGENTS.md`, GRACE XML, `docs/artifact-registry.yml`, `docs/project-plan.md`, `docs/status-report.md`, `docs/traceability-matrix.md` и `docs/decision-log.md`.
- Generated dashboards, generated workbench и generated audit reports классифицированы как `not_protected_generated` с заполненными `generator`, `derived_from` и `regeneration_command`.
- Создан `docs/protected-artifact-change-requests.yml` для будущих approved change requests на изменение protected artifacts.
- Добавлен `scripts/validate_accepted_artifact_protection.py`.
- `Makefile` получил target `validate-accepted-artifact-protection`, target подключен в `make check`.
- `scripts/generate_acceptance_dashboard.py` и `scripts/generate_user_review_workbench.py` отражают protection status как `classified_by_EP-018`.
- `scripts/validate_post_acceptance_state.py` обновлен на baseline EP-014 accepted и current ready packet EP-018.

## 3. Артефакты для проверки

| Артефакт | Назначение | Что проверить |
|---|---|---|
| `AGENTS.md` | Правила работы Codex | Есть `Accepted artifact protection discipline`, generated artifacts не hard-lock. |
| `docs/artifact-registry.yml` | Реестр артефактов | Есть `protection` metadata и классификация protected/generated/code/pending. |
| `docs/protected-artifact-change-requests.yml` | Реестр change requests | Есть схема и пустой список requests. |
| `scripts/validate_accepted_artifact_protection.py` | Validator protection discipline | Проверяет accepted reports, generated artifacts, change requests и EP-010 guard. |
| `Makefile` | Команды проекта | Есть `validate-accepted-artifact-protection`, он входит в `make check`. |
| `docs/grace/execution-packets.xml` | Реестр execution packets | EP-018 зарегистрирован как `ready_for_acceptance`. |
| `docs/grace/module-contracts.xml` | Module contracts | Добавлен `M-ACCEPTED-ARTIFACT-PROTECTION`. |
| `docs/grace/verification-plan.xml` | Verification scenarios | Добавлены `V-ACCEPTED-PROTECTION-*`. |
| `docs/project-plan.md` | План проекта | EP-018 указан как активный ready packet. |
| `docs/status-report.md` | Статус проекта | EP-018 указан как текущий packet. |
| `docs/traceability-matrix.md` | Traceability | Добавлена связь REQ-016 / EP-018 / validator / registry. |
| `docs/decision-log.md` | Решения проекта | Добавлено decision по protection classification и change request mechanism. |

## 4. Команды проверки

```sh
make validate-accepted-artifact-protection
make generate-dashboards
make validate-plan
make validate-post-acceptance-state
make check
git diff -- docs/acceptance/EP-001-*.acceptance.md docs/acceptance/EP-002-*.acceptance.md docs/acceptance/EP-003-*.acceptance.md docs/acceptance/EP-004-*.acceptance.md docs/acceptance/EP-005-*.acceptance.md docs/acceptance/EP-007-*.acceptance.md docs/acceptance/EP-008-*.acceptance.md docs/acceptance/EP-009-*.acceptance.md docs/acceptance/EP-011-*.acceptance.md docs/acceptance/EP-012-*.acceptance.md docs/acceptance/EP-013-*.acceptance.md docs/acceptance/EP-014-*.acceptance.md
git diff -- README.md CHANGELOG.md
git status --short | grep -E "\.env|\.venv|node_modules|\.sql|\.dump|\.backup|thesis/source/.*\.docx|thesis/versions/.*\.docx|thesis/exports/pdf/.*\.pdf"
```

Результаты выполнения:

- `make validate-accepted-artifact-protection`: passed.
- `make generate-dashboards`: passed.
- `make validate-plan`: passed.
- `make validate-post-acceptance-state`: passed.
- `make check`: passed.
- Diff check для accepted reports EP-001–EP-014: passed, output empty.
- Diff check для `README.md` / `CHANGELOG.md`: passed, output empty.
- Forbidden files check: passed, output empty.

## 5. Критерии приемки

| ID | Критерий | Статус Codex | Статус пользователя |
|---|---|---|---|
| AC-EP-018-001 | Accepted acceptance reports classified as protected in artifact registry. | ready_for_acceptance | pending |
| AC-EP-018-002 | Generated dashboards classified as not_protected_generated. | ready_for_acceptance | pending |
| AC-EP-018-003 | Protected artifacts require explicit user approval for future changes. | ready_for_acceptance | pending |
| AC-EP-018-004 | Change request mechanism exists. | ready_for_acceptance | pending |
| AC-EP-018-005 | Validator checks protection discipline. | ready_for_acceptance | pending |
| AC-EP-018-006 | `make check` includes protection validation. | ready_for_acceptance | pending |
| AC-EP-018-007 | EP-010 cannot change protected accepted artifacts without approved change request. | ready_for_acceptance | pending |
| AC-EP-018-008 | Accepted reports EP-001–EP-014 were not modified. | ready_for_acceptance | pending |
| AC-EP-018-009 | Generated dashboards remain regenerable and are not hard-locked. | ready_for_acceptance | pending |
| AC-EP-018-010 | User-owned fields are not modified by Codex. | ready_for_acceptance | pending |

## 6. Что нужно проверить пользователю

- Проверить, что protected source/manual artifacts действительно требуют explicit user approval.
- Проверить, что generated dashboards/workbench/audit reports не hard-lock и могут пересоздаваться из source-of-truth.
- Проверить, что `docs/protected-artifact-change-requests.yml` достаточен для будущих запросов на изменение protected artifacts.
- Проверить, что EP-010 не сможет менять protected accepted artifacts без approved change request.
- Проверить, что accepted reports EP-001–EP-014 не изменялись.
- Проверить, что user-owned поля не изменялись Codex.

## 7. Блокеры

## 8. Риски

- `README.md` и `CHANGELOG.md` классифицированы как protected; EP-010 потребует отдельного approval по `CR-EP-010-README-CHANGELOG-LANGUAGE-NORMALIZATION`.

## 9. Спорные решения

- `Makefile` изменен в рамках EP-018, хотя strict scope не перечислял его явно. Это необходимо, потому что сам пакет требует target `validate-accepted-artifact-protection` и включение этой проверки в `make check`.
- `README.md` и `CHANGELOG.md` классифицированы в registry как protected source/manual artifacts, но их содержимое не изменялось.

## 10. Решение пользователя

acceptance_decision: accepted
accepted_by: Дмитрий
accepted_at: 2026-06-10
comments: Принято. Проверено: accepted artifacts классифицированы; accepted reports EP-001–EP-014 не изменены; generated dashboards не hard-lock; protection validator проходит; change request для будущей русификации README.md и CHANGELOG.md создан как CR-EP-010-README-CHANGELOG-LANGUAGE-NORMALIZATION со статусом requires_user_approval; EP-010 не выполнялся.
