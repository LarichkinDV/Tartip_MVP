# Acceptance Report — EP-012-USER-REVIEW-WORKBENCH-AND-ACCEPTANCE-STANDARD

## 0. Правила заполнения

- Если блокеров нет, раздел `## 7. Блокеры` оставить пустым.
- Если рисков нет, раздел `## 8. Риски` оставить пустым.
- Не писать в пустых разделах `Отсутствуют`, `Нет`, `Блокеров нет`, `Рисков нет`, `None`, `No blockers`, `No risks`.
- Любая строка списка в разделе `## 7. Блокеры` считается реальным блокером.
- Любая строка списка в разделе `## 8. Риски` считается реальным риском.
- Ограничения, которые не блокируют приемку, фиксируются в разделе `## 8. Риски`, в `comments` решения пользователя или выносятся в отдельный future execution packet.
- Codex не должен заполнять пользовательское решение за пользователя.

## 1. Пакет

- Execution packet: EP-012-USER-REVIEW-WORKBENCH-AND-ACCEPTANCE-STANDARD
- Статус Codex: ready_for_acceptance
- Acceptance owner: Дмитрий
- Дата подготовки: 2026-06-08

## 2. Что реализовано

- Добавлен стандарт пустых разделов `Блокеры` и `Риски` в `AGENTS.md`.
- Обновлен `docs/acceptance/ACCEPTANCE_TEMPLATE.md`.
- Создан `docs/user-review-workbench.yml`.
- Создан `docs/user-review-workbench.md`.
- Создан `scripts/generate_user_review_workbench.py`.
- Создан `scripts/validate_user_review_workbench.py`.
- Создан `scripts/apply_user_review_decisions.py`.
- Добавлены Makefile targets `generate-user-review-workbench`, `validate-user-review-workbench`, `apply-user-review-decisions`.
- EP-012 зарегистрирован в GRACE execution packets, verification plan, module contracts, artifact registry, project plan, status report и traceability matrix.

## 3. Артефакты для проверки

| Артефакт | Назначение | Что проверить |
|---|---|---|
| `AGENTS.md` | Регламент агента | Есть standard для пустых blockers/risks и user review workbench discipline. |
| `docs/acceptance/ACCEPTANCE_TEMPLATE.md` | Шаблон acceptance report | Раздел `## 0. Правила заполнения` добавлен, `## 7. Блокеры` и `## 8. Риски` остаются пустыми. |
| `docs/user-review-workbench.yml` | Машинно-читаемое активное окно проверки | Accepted packets скрыты из `active_review_items`, source file/checksum поля заполнены. |
| `docs/user-review-workbench.md` | Человекочитаемое активное окно проверки | Пользователь видит активные решения, проверки, вопросы, блокеры, риски и историю accepted EP. |
| `scripts/generate_user_review_workbench.py` | Генератор workbench | Читает source files и не меняет их. |
| `scripts/validate_user_review_workbench.py` | Валидатор workbench | Проверяет полноту active queue, source checksums, user-owned fields и псевдоблокеры. |
| `scripts/apply_user_review_decisions.py` | Применение решений | Переносит только явные acceptance decisions в acceptance reports после checksum и ownership checks. |

## 4. Команды проверки

```sh
git branch --show-current
git status --short
source .venv/bin/activate && make generate-user-review-workbench
source .venv/bin/activate && make validate-user-review-workbench
source .venv/bin/activate && make generate-dashboards
source .venv/bin/activate && make validate-plan
source .venv/bin/activate && make validate-verification
source .venv/bin/activate && make validate-reference
source .venv/bin/activate && make compare-reference-fixtures
source .venv/bin/activate && make lint
source .venv/bin/activate && make test
source .venv/bin/activate && make check
source .venv/bin/activate && make audit
env PYTHONPYCACHEPREFIX=/tmp/tartip_pycache .venv/bin/python -m py_compile scripts/generate_user_review_workbench.py scripts/validate_user_review_workbench.py scripts/apply_user_review_decisions.py
python3 -c "from pathlib import Path; import yaml; root=yaml.safe_load(Path('docs/user-review-workbench.yml').read_text(encoding='utf-8'))['user_review_workbench']; active={i.get('packet_id') for i in root.get('active_review_items', []) if i.get('type')=='acceptance'}; accepted={i.get('packet_id') for i in root.get('recently_accepted', [])}; hidden={'EP-001'+'-INFRA','EP-002'+'-REFERENCE-GOVERNANCE'}; expected={'EP-003'+'-REFERENCE-VERSIONING','EP-004'+'-PROJECT-PLANNING-AND-ACCEPTANCE','EP-005'+'-ACCEPTANCE-AND-USER-ACTION-DASHBOARDS','EP-007'+'-VERIFICATION-DASHBOARD','EP-008'+'-DISSERTATION-PROMPT-GENERATION','EP-009'+'-CODEX-SPEC-AUDIT','EP-011'+'-GIT-WORKFLOW-DISCIPLINE','EP-012'+'-USER-REVIEW-WORKBENCH-AND-ACCEPTANCE-STANDARD'}; assert not hidden & active; assert hidden <= accepted; assert expected <= active; print('workbench packet visibility passed')"
python3 -c "from pathlib import Path; bad=[('text: '+chr(34)+'Блокеров'+' нет'),('text: '+chr(34)+'Рисков'+' нет'),('text: '+chr(34)+'Отсутствуют.'),('No '+'blockers'),('No '+'risks')]; files=[Path('docs/user-review-workbench.yml'),Path('docs/acceptance-dashboard.yml')]; hits=[f'{p}:{i}:{b}' for p in files for i,line in enumerate(p.read_text(encoding='utf-8').splitlines(),1) for b in bad if b in line]; print('\n'.join(hits)); raise SystemExit(1 if hits else 0)"
rg -n "^acceptance_decision: pending$" docs/acceptance/EP-003-REFERENCE-VERSIONING.acceptance.md docs/acceptance/EP-004-PROJECT-PLANNING-AND-ACCEPTANCE.acceptance.md docs/acceptance/EP-005-ACCEPTANCE-AND-USER-ACTION-DASHBOARDS.acceptance.md docs/acceptance/EP-007-VERIFICATION-DASHBOARD.acceptance.md docs/acceptance/EP-008-DISSERTATION-PROMPT-GENERATION.acceptance.md docs/acceptance/EP-009-CODEX-SPEC-AUDIT.acceptance.md docs/acceptance/EP-011-GIT-WORKFLOW-DISCIPLINE.acceptance.md
```

Результаты выполнения:

- Ветка: `ep-012-user-review-workbench-and-acceptance-standard`.
- До начала EP-012 рабочее дерево было чистым.
- `make lint`: passed.
- `make test`: passed, `3 passed`, `1 warning` от `StarletteDeprecationWarning`.
- `make validate-reference`: passed.
- `make compare-reference-fixtures`: passed.
- `make validate-verification`: passed.
- `make validate-user-review-workbench`: passed.
- `make check`: passed.
- `make audit`: passed, audit reports regenerated with `147` Codex spec findings and `80` language findings.
- `py_compile` для EP-012 scripts: passed.
- Workbench visibility check: passed.
- Pseudo blocker/risk placeholder check: passed.
- EP-003, EP-004, EP-005, EP-007, EP-008, EP-009 и EP-011 остались `acceptance_decision: pending`.

## 5. Критерии приемки

| ID | Критерий | Статус Codex | Статус пользователя |
|---|---|---|---|
| AC-EP-012-001 | AGENTS.md содержит стандарт пустых разделов `Блокеры` и `Риски`. | ready_for_acceptance | pending |
| AC-EP-012-002 | ACCEPTANCE_TEMPLATE.md содержит правила заполнения блокеров и рисков. | ready_for_acceptance | pending |
| AC-EP-012-003 | Создан `docs/user-review-workbench.yml`. | ready_for_acceptance | pending |
| AC-EP-012-004 | Создан `docs/user-review-workbench.md`. | ready_for_acceptance | pending |
| AC-EP-012-005 | Создан `generate_user_review_workbench.py`. | ready_for_acceptance | pending |
| AC-EP-012-006 | Создан `validate_user_review_workbench.py`. | ready_for_acceptance | pending |
| AC-EP-012-007 | Создан `apply_user_review_decisions.py`. | ready_for_acceptance | pending |
| AC-EP-012-008 | Accepted packets не отображаются в `active_review_items`. | ready_for_acceptance | pending |
| AC-EP-012-009 | Pending/ready_for_acceptance packets отображаются в `active_review_items`. | ready_for_acceptance | pending |
| AC-EP-012-010 | Решения пользователя из workbench применяются только через `apply_user_review_decisions.py`. | ready_for_acceptance | pending |
| AC-EP-012-011 | Codex не может сам ставить `accepted` / `accepted_by` / `accepted_at`. | ready_for_acceptance | pending |
| AC-EP-012-012 | Acceptance reports остаются source of truth. | ready_for_acceptance | pending |
| AC-EP-012-013 | Псевдоблокеры `Отсутствуют` / `Блокеров нет` / `None` запрещены. | ready_for_acceptance | pending |
| AC-EP-012-014 | EP-010 не выполнялся. | ready_for_acceptance | pending |
| AC-EP-012-015 | `README.md` и `CHANGELOG.md` не нормализовались. | ready_for_acceptance | pending |
| AC-EP-012-016 | EP-003–EP-011 не были автоматически приняты. | ready_for_acceptance | pending |

## 6. Что нужно проверить пользователю

- Проверить `docs/user-review-workbench.md`.
- Проверить `docs/user-review-workbench.yml`.
- Проверить, что EP-001 и EP-002 скрыты из `active_review_items` и сохранены в `recently_accepted`.
- Проверить, что EP-003, EP-004, EP-005, EP-007, EP-008, EP-009, EP-011 и EP-012 видны в активной очереди, пока они pending/ready_for_acceptance.
- Проверить, что `scripts/apply_user_review_decisions.py` не применяет решения с `accepted_by = Codex`, stale checksum, пустыми user fields или активными блокерами.
- Проверить, что user review workbench не заменяет acceptance reports как source of truth.

## 7. Блокеры

## 8. Риски

- `scripts/apply_user_review_decisions.py` в первой версии применяет только acceptance decisions; manual verification, user actions и audit findings остаются для ручного обновления в профильных source files.
- `make check` может штатно регенерировать dashboard или audit артефакты; такие изменения нужно просматривать перед commit.

## 9. Спорные решения

- User review workbench хранит временное пользовательское решение до применения, но source of truth становится только acceptance report после запуска `make apply-user-review-decisions`.

## 10. Решение пользователя

acceptance_decision: accepted
accepted_by: Дмитрий
accepted_at: 2026-06-08
comments: Принято. Единое активное окно проверки пользователем, стандарт пустых разделов блокеров/рисков и apply-скрипт для acceptance decisions проверены. EP-012 принят с учетом зафиксированных рисков первой версии.
