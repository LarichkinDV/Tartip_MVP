# Acceptance Report — EP-014-USER-REVIEW-DECISION-CLI-SAFETY

## 0. Правила заполнения

- Если блокеров нет, раздел `## 7. Блокеры` оставить пустым.
- Если рисков нет, раздел `## 8. Риски` оставить пустым.
- Не писать в пустых разделах `Отсутствуют`, `Нет`, `Блокеров нет`, `Рисков нет`, `None`, `No blockers`, `No risks`.
- Любая строка списка в разделе `## 7. Блокеры` считается реальным блокером.
- Любая строка списка в разделе `## 8. Риски` считается реальным риском.
- Codex не должен заполнять пользовательское решение за пользователя.

## 1. Пакет

- Execution packet: EP-014-USER-REVIEW-DECISION-CLI-SAFETY
- Статус Codex: ready_for_acceptance
- Acceptance owner: Дмитрий
- Дата подготовки: 2026-06-09

## 2. Что реализовано

- `scripts/apply_user_review_decisions.py` получил явные CLI-режимы `--dry-run` и `--apply`.
- Без `--apply` скрипт работает как dry-run и не пишет файлы.
- `--dry-run` выводит planned changes, affected files, reasons и unified diff.
- `--apply` применяет только явно заполненные пользовательские решения для items `type: acceptance`.
- Для `manual_verification`, `user_action`, `audit_finding` и `requires_user_approval` выводится warning без применения.
- Добавлены проверки `accepted_by != Codex`, обязательных `accepted_by`, `accepted_at`, `comments`, stale `source_checksum_sha256`, active blockers и запрета перезаписи уже accepted reports.
- Перед записью формируется diff, запись выполняется atomic write.
- `Makefile` получил targets `apply-user-review-decisions-dry-run` и `apply-user-review-decisions`.
- `scripts/validate_user_review_workbench.py` проверяет наличие Makefile targets, поддержку `--dry-run` / `--apply` и неизменность `git status --short` после dry-run.
- `scripts/validate_post_acceptance_state.py` разрешает только явно зарегистрированный текущий packet `EP-014-USER-REVIEW-DECISION-CLI-SAFETY` в статусе `ready_for_acceptance` после accepted baseline.
- Зафиксировано planning decision: текущий EP-014 занимает CLI safety; ранее рекомендованный `EP-014-ACCEPTED-ARTIFACT-PROTECTION` переносится на `EP-018-ACCEPTED-ARTIFACT-PROTECTION`.
- `scripts/generate_user_review_workbench.py` генерирует инструкции, где `make apply-user-review-decisions-dry-run` обязателен до `make apply-user-review-decisions`.
- Generated workbench явно требует проверить dry-run diff, affected files, чужие acceptance reports и user-owned поля до apply.
- `scripts/generate_acceptance_dashboard.py` и `scripts/generate_user_review_workbench.py` используют `EP-018-ACCEPTED-ARTIFACT-PROTECTION` для accepted artifact protection debt.
- GitHub push, merge, archive export и release publication не выполнялись.

## 3. Артефакты для проверки

| Артефакт | Назначение | Что проверить |
|---|---|---|
| `scripts/apply_user_review_decisions.py` | Безопасное применение пользовательских acceptance decisions | Есть `--dry-run`, `--apply`, non-writing default, diff и atomic write. |
| `Makefile` | Команды проекта | Есть `apply-user-review-decisions-dry-run` и `apply-user-review-decisions`. |
| `scripts/validate_user_review_workbench.py` | Workbench validator | Проверяет CLI safety и неизменность дерева после dry-run. |
| `scripts/validate_post_acceptance_state.py` | Post-acceptance validator | Разрешает только EP-014 CLI safety как текущий ready packet. |
| `scripts/generate_user_review_workbench.py` | Генератор workbench | Генерирует dry-run-first flow и EP-018 protection deferral. |
| `scripts/generate_acceptance_dashboard.py` | Генератор acceptance dashboard | Генерирует EP-018 protection deferral вместо legacy EP-014 labels. |
| `docs/grace/execution-packets.xml` | Реестр execution packets | EP-014 зарегистрирован как `ready_for_acceptance`, не `accepted`. |
| `docs/grace/module-contracts.xml` | Контракт модуля | Добавлен safety-контракт CLI decisions. |
| `docs/grace/verification-plan.xml` | Verification scenarios | Добавлены сценарии CLI safety и allowed ready packet. |
| `docs/project-plan.md` | План проекта | Зафиксировано planning decision по номеру EP-014 и перенос protection packet на EP-018. |
| `docs/status-report.md` | Статус проекта | Активный packet EP-014, следующий recommended packet EP-018. |
| `docs/artifact-registry.yml` | Реестр артефактов | Артефакты EP-014 зарегистрированы. |

## 4. Команды проверки

```sh
git rev-parse --show-toplevel
git branch --show-current
git status --short
git log --oneline --decorate -8
python3 scripts/apply_user_review_decisions.py --dry-run
make apply-user-review-decisions-dry-run
git status --short
git --no-pager diff --name-status
make validate-user-review-workbench
make generate-dashboards
make validate-plan
make validate-verification
make validate-audit
make validate-post-acceptance-state
make check
```

Результаты выполнения:

- `git rev-parse --show-toplevel`: `/Users/larichkindv/Tartip`.
- `git branch --show-current`: `ep-014-user-review-decision-cli-safety`.
- `make apply-user-review-decisions-dry-run`: passed; no acceptance report changes planned; files were not modified.
- `git status --short` before/after standalone dry-run: unchanged dirty EP-014 baseline.
- `git --no-pager diff --name-status`: showed only current EP-014 modified files and the untracked EP-014 acceptance report.
- `make validate-plan`: passed.
- `make validate-user-review-workbench`: passed; validates dry-run target, CLI flags, dry-run non-writing behavior, and generated dry-run-first flow.
- `make validate-verification`: passed.
- `make validate-audit`: passed.
- `make validate-post-acceptance-state`: passed.
- `make check`: passed.
- `python3 scripts/apply_user_review_decisions.py --dry-run`: passed; no acceptance report changes planned; files were not modified.
- `python -m ruff check scripts/apply_user_review_decisions.py scripts/generate_acceptance_dashboard.py scripts/generate_user_review_workbench.py scripts/validate_post_acceptance_state.py scripts/validate_user_review_workbench.py`: passed.
- `python3 -m py_compile` for changed Python scripts: passed.
- Legacy deferral status scan: exact old status value was not found. Historical old protection packet references remain only in accepted EP-013 report and explicit planning-decision notes that state the move to `EP-018-ACCEPTED-ARTIFACT-PROTECTION`; accepted EP-013 report was not modified.
- Diff check for EP-001..EP-013 acceptance reports: no changes.

## 5. Критерии приемки

| ID | Критерий | Статус Codex | Статус пользователя |
|---|---|---|---|
| AC-EP-014-001 | `scripts/apply_user_review_decisions.py` поддерживает `--dry-run`. | ready_for_acceptance | pending |
| AC-EP-014-002 | `scripts/apply_user_review_decisions.py` поддерживает `--apply`. | ready_for_acceptance | pending |
| AC-EP-014-003 | Без `--apply` скрипт не изменяет файлы. | ready_for_acceptance | pending |
| AC-EP-014-004 | `--dry-run` показывает planned changes, affected files, reasons и diff. | ready_for_acceptance | pending |
| AC-EP-014-005 | `--apply` применяет только явно заполненные пользовательские решения. | ready_for_acceptance | pending |
| AC-EP-014-006 | `accepted_by = Codex` запрещен. | ready_for_acceptance | pending |
| AC-EP-014-007 | `accepted_by`, `accepted_at` и `comments` обязательны. | ready_for_acceptance | pending |
| AC-EP-014-008 | Stale `source_checksum_sha256` запрещает apply. | ready_for_acceptance | pending |
| AC-EP-014-009 | Already accepted report не перезаписывается без explicit user approval. | ready_for_acceptance | pending |
| AC-EP-014-010 | Items с active blockers не применяются. | ready_for_acceptance | pending |
| AC-EP-014-011 | Применяются только items `type: acceptance`. | ready_for_acceptance | pending |
| AC-EP-014-012 | Manual verification, user action, audit finding и requires_user_approval остаются warning-only. | ready_for_acceptance | pending |
| AC-EP-014-013 | Запись выполняется atomic write. | ready_for_acceptance | pending |
| AC-EP-014-014 | Acceptance criteria, blockers, risks, artifacts и unrelated sections не меняются apply-скриптом. | ready_for_acceptance | pending |
| AC-EP-014-015 | Acceptance decisions EP-001..EP-013 не изменены. | ready_for_acceptance | pending |
| AC-EP-014-016 | EP-010 не выполнялся. | ready_for_acceptance | pending |
| AC-EP-014-017 | Generated workbench требует dry-run перед apply. | ready_for_acceptance | pending |
| AC-EP-014-018 | `Makefile` содержит `apply-user-review-decisions-dry-run`. | ready_for_acceptance | pending |
| AC-EP-014-019 | Apply script в dry-run режиме не пишет файлы. | ready_for_acceptance | pending |
| AC-EP-014-020 | Legacy EP-014 protection labels заменены на EP-018 в generated artifacts. | ready_for_acceptance | pending |
| AC-EP-014-021 | GitHub/archive export, merge и push не выполнялись. | ready_for_acceptance | pending |

## 6. Что нужно проверить пользователю

- Проверить, что `python3 scripts/apply_user_review_decisions.py --dry-run` не меняет рабочее дерево.
- Проверить, что `make apply-user-review-decisions-dry-run` вызывает dry-run, а не apply.
- Проверить, что `--apply` требует заполненные пользовательские поля и не принимает `accepted_by = Codex`.
- Проверить, что stale checksum, active blockers и already accepted report блокируют apply.
- Проверить, что accepted decisions EP-001..EP-013 не изменялись.
- Проверить planning decision: `EP-014-USER-REVIEW-DECISION-CLI-SAFETY` текущий, accepted artifact protection перенесен на `EP-018-ACCEPTED-ARTIFACT-PROTECTION`.
- Проверить generated workbench flow: сначала dry-run, затем проверка affected files, чужих acceptance reports и user-owned полей, только потом apply.
- Проверить, что generated acceptance/workbench artifacts используют `EP-018-ACCEPTED-ARTIFACT-PROTECTION` для protection debt.

## 7. Блокеры

## 8. Риски

## 9. Спорные решения

- Номер EP-014 использован для CLI safety, потому что этот safety gap блокирует безопасное применение пользовательских решений из workbench. Ранее рекомендованный protection packet перенесен на следующий свободный номер `EP-018`.

## 10. Решение пользователя

acceptance_decision: accepted
accepted_by: Дмитрий
accepted_at: 2026-06-10
comments: Принято. Проверено: make apply-user-review-decisions-dry-run и python3 scripts/apply_user_review_decisions.py --dry-run выполняются в non-writing режиме; сравнение git status до и после dry-run не выявило изменений. Режим --apply отделен от dry-run и защищен проверками обязательных user-owned полей, stale checksum, active blockers, запрета accepted_by = Codex и запрета перезаписи уже accepted reports. Manual verification и user_action решения в текущей версии не применяются автоматически. Accepted decisions EP-001–EP-013 не изменены. Planning decision DEC-EP-014-001 зафиксирован; перенос EP-014-ACCEPTED-ARTIFACT-PROTECTION на EP-018 подтвержден.
