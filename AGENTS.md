\# AGENTS.md



\## Project



You are working on the BIM5D Cost-Schedule Matching project.



The project implements a local-first system for mapping BIM model elements to KSI classifier codes, calculation units, work types, GESN norm candidates, work quantities, work packages, schedule tasks, actual records, plan-fact comparisons, and control decisions.



\## Required reading before any domain or infrastructure change



Read these files first:



1\. docs/01-methodology.md

2\. docs/02-domain-model.md

3\. docs/grace/knowledge-graph.xml

4\. docs/grace/module-contracts.xml

5\. docs/grace/verification-plan.xml

6\. docs/grace/execution-packets.xml



\## Non-negotiable domain rules



1\. A BIM element is not equal to a construction work.

2\. KSI is a classification layer and must not directly select GESN.

3\. CalculationUnit is a normative-calculation template, not a universal container.

4\. ActualRecord is primarily linked to WorkPackage / zone, not to an isolated BIM element.

5\. ScheduleTask is created for WorkPackage, not for every GESN norm.

6\. Every classifier, norm, matching rule, and calculation unit must have version and status.

7\. Ambiguous matches must return `requires\_review`.

8\. Do not hard-code normative labor, cost, or GESN values as final truth without source and version fields.



\## Forbidden architecture



Do not introduce:



\- direct ModelElement -> GESNNorm mapping;

\- direct KSIResultCode -> GESNNorm selection;

\- direct GESNNorm -> ScheduleTask creation;

\- CalculationUnit storing actual fact data;

\- ActualRecord linked only to a single ModelElement;

\- hidden auto-confirmed matching when required data is incomplete.



\## Required stack



Backend:

\- Python

\- FastAPI

\- SQLAlchemy

\- Alembic

\- PostgreSQL

\- Pydantic

\- pytest



Frontend:

\- TypeScript

\- React

\- Vite



Infrastructure:

\- Docker Compose

\- Makefile

\- GitHub Actions or GitLab CI



\## Work discipline



Before implementation:

1\. Identify the execution packet.

2\. Identify affected modules.

3\. Check the knowledge graph.

4\. Check module contracts.

5\. Check verification requirements.



After implementation:

1\. Run formatting.

2\. Run linting.

3\. Run tests.

4\. Update documentation.

5\. Update CHANGELOG.md.



\## Forbidden actions



Do not:

\- delete migrations;

\- rewrite Git history;

\- commit secrets;

\- modify `.env` except `.env.example`;

\- remove GRACE artifacts;

\- add external services without documenting them;

\- bypass tests or verification scenarios.

## Reference data discipline

No source — no rule.

Codex may create:

- candidate;
- draft;
- structured question;
- review item;
- data requirement.

Codex must not create an active matching rule from memory, assumptions, or LLM-generated data.

LLM-generated content is forbidden as evidence.

Official normative fields require official evidence:

- GESN code;
- norm unit;
- included works;
- excluded works;
- resource composition;
- coefficients;
- FSNB version;
- technical part references.

Official classifier fields require official classifier evidence:

- KSI code;
- KSI name;
- KSI table;
- KSI version.

User decisions are allowed only for project entities:

- internal work types;
- work packages;
- grouping rules;
- project naming.

A user decision must not confirm normative FSNB fields or official KSI codes.

If required evidence is missing, create a structured record in `data/questions/`.

## Project planning and acceptance discipline

1. After each execution packet, Codex must update:
   - `docs/project-plan.md`;
   - `docs/artifact-registry.yml`;
   - `docs/traceability-matrix.md`;
   - `docs/status-report.md`;
   - `CHANGELOG.md`;
   - `docs/acceptance/<PACKET_ID>.acceptance.md`.

2. Every created artifact must be registered in `docs/artifact-registry.yml`.

3. Every execution packet must have:
   - expected artifacts;
   - actual artifacts;
   - acceptance criteria;
   - verification status;
   - unresolved questions;
   - blockers;
   - risks;
   - next step.

4. Codex must not mark an execution packet as accepted.

5. Codex may set only `ready_for_acceptance` when:
   - expected artifacts are created or explicitly marked as blocked/planned;
   - actual artifacts are registered;
   - verification commands were run or the blocking reason is documented;
   - acceptance report is created;
   - нерешенные риски и блокеры перечисляются только при их фактическом наличии; если блокеров или рисков нет, соответствующие разделы остаются пустыми.

6. The user is the only acceptance owner.

7. A task must not be marked accepted when:
   - acceptance report is missing;
   - acceptance criteria are missing;
   - `accepted_by` is missing;
   - `accepted_by = Codex`;
   - artifacts are not registered;
   - verification is neither executed nor documented.

8. If Codex is unsure, it must set `review_required` or `ready_for_acceptance`, not `accepted`.

### Acceptance blockers and risks format

1. Разделы `## 7. Блокеры` и `## 8. Риски` обязательны в каждом acceptance report.

2. Если блокеров нет, раздел `## 7. Блокеры` должен оставаться пустым.

3. Если рисков нет, раздел `## 8. Риски` должен оставаться пустым.

4. Запрещено писать в пустых разделах:
   - `Отсутствуют`;
   - `Нет`;
   - `Блокеров нет`;
   - `Рисков нет`;
   - `None`;
   - `No blockers`;
   - `No risks`.

5. Любая строка списка в разделе `## 7. Блокеры` считается реальным блокером.

6. Любая строка списка в разделе `## 8. Риски` считается реальным риском.

7. Если ограничение не блокирует приемку пакета, его нельзя помещать в раздел `## 7. Блокеры`. Такое ограничение фиксируется либо в разделе `## 8. Риски`, либо в `comments` решения пользователя, либо выносится в отдельный future execution packet.

8. Если пакет принят, но acceptance dashboard показывает псевдоблокер вида `Блокеров нет`, `Отсутствуют`, `None` или аналогичный текст, исходный acceptance report требует нормализации.

9. Codex не должен создавать псевдоблокеры или псевдориски для заполнения пустых разделов.

## Dashboard discipline

1. After each execution packet, Codex must update:
   - `docs/acceptance-dashboard.md`;
   - `docs/acceptance-dashboard.yml`;
   - `docs/user-action-dashboard.md`;
   - `docs/user-action-dashboard.yml`.

2. The acceptance dashboard is a single window for review, but it does not replace detailed acceptance reports in `docs/acceptance/`.

3. The user action dashboard is a single window for user questions, but it does not replace source question files in `data/questions/*.yml`.

4. Codex must not change these fields when they represent a user decision:
   - `acceptance_decision: accepted`;
   - `decided_by`;
   - `accepted_by`;
   - `answered_by`;
   - `answered_at`.

5. Codex may aggregate and highlight these statuses:
   - `ready_for_acceptance`;
   - `pending`;
   - `open`;
   - `blocked`;
   - `needs_revision`.

6. If dashboard data conflicts with source files, Codex must not close the task. It must set `review_required` or `blocked` and describe the discrepancy in the dashboard.

## User review workbench discipline

1. `docs/user-review-workbench.md` и `docs/user-review-workbench.yml` являются единым активным окном пользовательской проверки.

2. User review workbench не заменяет source of truth.

3. Source of truth остаются:
   - `docs/acceptance/<PACKET_ID>.acceptance.md` для решений по приемке EP;
   - `docs/acceptance-dashboard.yml` для сводки приемки;
   - `docs/verification-dashboard.yml` для ручных проверок;
   - `docs/user-action-dashboard.yml` для вопросов и действий пользователя;
   - `docs/audit/audit-findings.yml` для audit findings;
   - `docs/artifact-registry.yml` для артефактов;
   - `docs/grace/execution-packets.xml` для execution packets.

4. User review workbench показывает только активные элементы, требующие реакции пользователя:
   - пакеты `ready_for_acceptance`;
   - пакеты `needs_revision`;
   - pending manual checks;
   - open user actions;
   - requires_user_approval;
   - critical/high audit findings;
   - active blockers.

5. Accepted packets не должны отображаться в `active_review_items`.

6. Accepted packets должны сохраняться в истории:
   - acceptance reports;
   - acceptance dashboard;
   - artifact registry;
   - status report;
   - Git history.

7. Пользователь может заполнить решение в `docs/user-review-workbench.yml`, но это решение становится source-of-truth только после применения через `scripts/apply_user_review_decisions.py`.

8. `scripts/apply_user_review_decisions.py` переносит пользовательские решения из workbench в профильные source files.

9. Codex не имеет права сам заполнять:
   - `acceptance_decision: accepted`;
   - `accepted_by`;
   - `accepted_at`;
   - `checked_by`;
   - `answered_by`;
   - `decided_by`.

10. Codex не имеет права удалять acceptance reports или историю принятых пакетов.

11. Если workbench конфликтует с source files, source files имеют приоритет, а workbench должен показать warning.

12. Если source file изменился после генерации workbench, пользовательское решение из workbench нельзя применять без повторной генерации.

## Accepted artifact protection discipline

1. Accepted source/manual artifacts are protected after user acceptance.

2. A protected accepted artifact must not be modified, normalized, reformatted, regenerated, or overwritten without explicit user approval.

3. Generated dashboards and derived reports are not hard-locked as protected source artifacts, but their generators must not alter source-of-truth user decisions.

4. If a future packet needs to change a protected accepted artifact, it must create a change request with:
   - protected artifact path;
   - reason for change;
   - impact analysis;
   - affected EP;
   - user approval field;
   - verification commands;
   - rollback note.

5. Codex must not silently change:
   - `acceptance_decision`;
   - `accepted_by`;
   - `accepted_at`;
   - `comments`;
   - `checked_by`;
   - `answered_by`;
   - `decided_by`.

6. EP-010-LANGUAGE-NORMALIZATION must not modify protected accepted artifacts unless a separate approved change request exists.

7. Accepted acceptance reports are historical records. They must not be rewritten to improve style, language, formatting, or terminology after acceptance without explicit user approval.

8. Protection applies to source/manual accepted artifacts, not to generated dashboards that are recreated from source-of-truth files.

## Verification dashboard discipline

1. Codex must create and update:
   - `docs/verification-dashboard.md`;
   - `docs/verification-dashboard.yml`;
   after changes to:
   - `docs/grace/verification-plan.xml`;
   - the monthly test protocol;
   - acceptance dashboard;
   - project plan;
   - verification scripts.

2. Codex must not mark manual checks as checked or passed on behalf of the user.

3. Codex may mark automated checks as passed only when it actually ran the corresponding command and recorded the result.

4. For manual checks, `checked_by`, `checked_at`, and `result` must not be filled by Codex.

5. `checked_by` cannot be `Codex`.

6. If a check cannot be performed, its status must be `blocked` with a clear reason.

7. Each verification task must have:
   - `check_id`;
   - `title`;
   - `related_packet`;
   - `related_requirement`;
   - `check_type`;
   - `priority`;
   - `status`;
   - `how_to_check`;
   - `expected_result`;
   - `artifacts`;
   - `user_result`.

8. Verification dashboard does not replace acceptance dashboard.

9. Verification dashboard does not replace the monthly test protocol.

10. Verification dashboard is a practical checklist for executing checks from the test protocol.

## Monthly defense discipline

1. Ежемесячный контур защиты ведется через:
   - `docs/monthly/monthly-plan.yml`;
   - `docs/monthly/monthly-defense-dashboard.md`;
   - monthly protocol artifacts in `docs/monthly/<YYYY-MM>/`.

2. Активный monthly block должен содержать 3 задачи по 15 часов, если пользователь не утвердил иной состав.

3. Codex может готовить материалы для ручной проверки, но не может отмечать monthly defense artifacts как accepted.

4. Manual review results, reviewer names, and final acceptance decisions are user-owned fields.

## Dissertation synchronization and prompt generation discipline

1. После каждого execution packet Codex должен оценивать влияние изменений на диссертацию.

2. Если влияние есть, Codex должен:
   - добавить запись в `docs/dissertation/dissertation-impact-log.yml`;
   - добавить запись в `docs/dissertation/section-update-queue.yml`;
   - сгенерировать prompt в `docs/dissertation/prompt-queue/pending/`;
   - обновить `docs/status-report.md`;
   - обновить dashboards;
   - указать generated prompt в acceptance report.

3. Если влияния нет, Codex должен зафиксировать:
   - `dissertation_impact: none`;
   - `reason: ...`.

4. Codex не имеет права редактировать DOCX напрямую без явной команды пользователя.

5. Codex не имеет права создавать новую DOCX-версию без явной команды пользователя.

6. Codex не имеет права добавлять источники в список литературы без citation request.

7. Codex не имеет права перенумеровывать литературу без явной команды пользователя.

8. Codex не имеет права переносить инженерные детали Tartip в диссертацию как научный результат.

9. Codex не имеет права отмечать dissertation prompt, patch или DOCX update как accepted.

10. Пользователь является acceptance owner для всех dissertation updates.

11. Accepted artifacts are protected.

12. Если диссертационная синхронизация требует изменения accepted artifact, Codex должен создать `requires_user_approval` item, а не изменять артефакт напрямую.

## Language policy

1. Все пользовательские человекочитаемые артефакты должны быть на русском языке там, где это возможно.

2. Это относится к:
   - пояснительным запискам;
   - README-разделам для пользователя;
   - acceptance reports;
   - dashboards;
   - monthly defense documents;
   - dissertation prompts;
   - methodology notes;
   - architecture notes;
   - status reports;
   - decision logs;
   - человекочитаемым `title`, `description`, `notes`, `summary`, `question`, `recommendation`, `comments` в YAML/XML.

3. Допустимо оставлять на английском:
   - имена файлов;
   - директории;
   - YAML/XML/JSON-ключи;
   - enum-статусы;
   - technical identifiers;
   - API;
   - классы;
   - функции;
   - переменные;
   - команды;
   - названия библиотек;
   - стандартные технические термины;
   - кодовые блоки;
   - URL.

4. Codex не должен механически переводить технические идентификаторы.

5. Codex не должен переводить YAML/XML/JSON-ключи.

6. Codex не должен менять enum-статусы ради русификации.

7. Если Codex обнаруживает англоязычный пользовательский текст, он должен создать language audit finding, предложить рекомендацию и не выполнять массовую русификацию в рамках `EP-009-CODEX-SPEC-AUDIT`.

## Audit discipline

1. `EP-009-CODEX-SPEC-AUDIT` является audit-first / read-mostly packet.

2. Codex audits first, fixes only safe non-protected issues.

3. Не выполнять массовое переписывание существующих документов.

4. Не выполнять массовую русификацию существующих документов.

5. Critical findings должны быть отражены в audit reports.

6. Medium/low language findings не должны блокировать `make check` на первом этапе.

7. Accepted/protected artifacts не изменять без user approval.

8. Audit findings не закрывать как `fixed`, если исправление реально не выполнено и не прошло проверку.

9. Существующие пользовательские решения и статусы в `audit-findings.yml` необходимо сохранять.

10. Если audit finding уже имеет статус `acknowledged`, `fixed`, `accepted_risk`, `false_positive` или `blocked`, новый запуск аудита не должен сбрасывать его в `open` без причины.

11. Если найдено нарушение в accepted/protected artifact, создать finding и requires_user_approval action, но не менять файл напрямую.

12. Пользовательские audit reports должны быть на русском языке.

## Git workflow discipline

1. Каждый новый execution packet должен выполняться в отдельной ветке, если задача не является read-only и не является продолжением текущей packet-ветки.

2. Формат имени ветки:

   ```text
   ep-<number>-<short-slug>
   ```

   Примеры:
   - `ep-010-language-normalization`;
   - `ep-011-reference-import`;
   - `ep-012-partition-rule-candidate`.

3. Перед изменением файлов Codex обязан проверить Git state:

   ```sh
   git branch --show-current
   git status --short
   ```

4. Codex должен создать новую ветку, если:
   - начинается новый execution packet;
   - меняется `AGENTS.md`;
   - меняются GRACE-файлы;
   - меняется `Makefile`;
   - меняются `scripts/*.py`;
   - меняются dashboards;
   - меняется `docs/artifact-registry.yml`;
   - создается acceptance report;
   - предполагается изменение более 3 файлов;
   - могут быть затронуты accepted/protected artifacts.

5. Codex не должен создавать новую ветку, если:
   - задача read-only;
   - только запускаются проверки;
   - текущая ветка уже соответствует execution packet;
   - выполняется малая доработка в рамках текущей packet-ветки.

6. Codex не должен переключать ветки, если working tree содержит uncommitted changes от другого пакета.

7. Codex не должен смешивать изменения разных execution packets в одной ветке без явного user approval.

8. Codex может подготовить commit/merge instructions, но не должен merge в `main`, если нет:
   - `acceptance_decision = accepted`;
   - `accepted_by` заполнен;
   - `accepted_by != Codex`;
   - `make check` passed;
   - нет critical/high audit findings;
   - нет несогласованных изменений accepted/protected artifacts;
   - пользователь явно разрешил merge.

9. Merge в `main` запрещен, если:
   - packet status = `ready_for_acceptance`;
   - `acceptance_decision = pending`;
   - `acceptance_decision = needs_revision`;
   - `accepted_by` пустой;
   - `accepted_by = Codex`;
   - `make check` fails;
   - есть critical/high audit findings;
   - есть несогласованные изменения accepted/protected artifacts;
   - в staging есть запрещенные файлы.

10. Перед предложением merge Codex должен выполнить:
    - `make check`;
    - `make validate-plan`;
    - `make audit`, если доступно.

11. Codex не должен добавлять в Git:
    - `.env`;
    - `.venv/`;
    - `node_modules/`;
    - database dumps;
    - backup dumps;
    - secrets;
    - real proprietary normative datasets;
    - real DOCX/PDF dissertation files unless explicitly approved.

12. Если Git state неоднозначен, Codex должен остановиться и создать user-action item, а не угадывать.

