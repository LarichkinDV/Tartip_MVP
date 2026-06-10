# Tartip

`Tartip` — локальный каркас проекта для BIM5D cost-schedule matching.
Текущий контур включает инфраструктуру: `Docker Compose`, backend на `FastAPI`,
frontend на `Vite` / `React`, `PostgreSQL`, `Adminer`, скрипты резервного
копирования и проверки CI.

Бизнес-логика сопоставления BIM, KSI, GESN, ВОР, пакетов работ, фактических
записей и план-фактного сравнения намеренно не реализована в `EP-001-INFRA`.

## Локальный запуск

Создать локальный файл окружения из примера:

```sh
cp .env.example .env
```

Запустить локальный стек:

```sh
make up
```

Полезные адреса:

- Backend `/health`: http://localhost:8000/health
- Backend `OpenAPI`: http://localhost:8000/docs
- Frontend: http://localhost:5173
- Adminer: http://localhost:8080

Остановить стек:

```sh
make down
```

Посмотреть логи:

```sh
make logs
```

Первый запуск Docker может загрузить публичные базовые образы и зависимости
пакетов. Выполняйте его только тогда, когда сетевой доступ допустим.

## Команды разработки

Запустить backend-тесты:

```sh
make test
```

Запустить linting:

```sh
make lint
```

Запустить форматирование:

```sh
make format
```

Запустить проектные проверки:

```sh
make check
```

Сгенерировать проектные dashboards:

```sh
make generate-dashboards
```

Запустить audit-проверки Codex:

```sh
make audit
```

Запустить advisory-проверки Git workflow:

```sh
make validate-git-workflow
```

Если Docker не установлен, `make check` все равно выполняет проверки безопасности
репозитория и сообщает, что синтаксическая проверка `Docker Compose` пропущена.
Полная проверка стека требует Docker, но проверки Python, Ruff, pytest, npm и
TypeScript могут выполняться локально из `.venv` и `frontend/node_modules`.

Проверки без Docker:

```sh
source .venv/bin/activate && make format
source .venv/bin/activate && make lint
source .venv/bin/activate && make test
make check
make generate-dashboards
make generate-verification-dashboard
make validate-verification
make validate-reference
make compare-reference-fixtures
make generate-data-questions
make audit
make validate-git-workflow
```

## Резервные копии базы данных

Создать резервную копию `PostgreSQL` в формате custom в смонтированном каталоге
`backups/`:

```sh
make backup
```

Восстановить базу из файла резервной копии:

```sh
CONFIRM_RESTORE=1 BACKUP_FILE=backups/tartip_YYYYMMDD_HHMMSS.dump make restore
```

Не добавляйте в Git файлы `.env` и незашифрованные дампы базы данных.
`scripts/check_project.sh` проверяет эти правила безопасности.

## Процесс работы со справочными данными

Reference governance следует правилу проекта: `No source — no rule`.
Codex не загружает внешние данные KSI/FSNB/GESN и не придумывает коды
классификаторов, коды норм, единицы норм, состав работ, ресурсы, коэффициенты
или нормативные значения.

Файлы источников от пользователя сначала помещаются в слой `inbox`:

- KSI-файлы: `data/reference/inbox/ksi/`
- FSNB/GESN-файлы: `data/reference/inbox/fsnb/`
- Проектные справочники видов работ: `data/reference/inbox/work_types/`

Слои жизненного цикла:

- `data/reference/inbox/`: пользователь поместил исходный локальный файл.
- `data/reference/quarantine/`: файл обнаружен, но не принят как источник.
- `data/reference/raw/`: неизменяемая принятая копия с checksum.
- `data/reference/staging/`: временные записи после разбора.
- `data/reference/normalized/`: нормализованные записи для поиска.
- `data/reference/manifests/`: манифест источников и журнал импорта.
- `data/reference/reports/`: отчеты проверки, импорта и сравнения.

Файлы в `inbox` не являются доверенным evidence. Источник можно использовать
только после приемки в `raw`, получения `checksum_sha256` и регистрации в
`data/reference/manifests/source-manifest.yml` с допустимым authority.

Проверить источники и evidence для правил сопоставления:

```sh
make validate-reference
```

Сгенерировать структурированные вопросы по отсутствующим источникам или evidence:

```sh
make generate-data-questions
```

Запустить fixtures для проверки дельтового версионирования:

```sh
make compare-reference-fixtures
```

Тестовые fixtures нужны только для проверки механики версионирования. Они не
являются classifier или normative evidence.

## Процесс проектного планирования и приемки

План проекта находится в `docs/project-plan.md`. Это человекочитаемая сводка;
источник истины по артефактам — `docs/artifact-registry.yml`.

Execution packets находятся в `docs/grace/execution-packets.xml`. Каждый пакет
должен быть связан с фактическими артефактами, verification scenarios и
acceptance report в `docs/acceptance/`.

Codex может подготовить пакет в статусе `ready_for_acceptance`, но только
пользователь может выставить acceptance decision, например `accepted`,
`rejected` или `needs_revision`. Поле `accepted_by` не должно быть `Codex`.

Проверить контур проектного планирования:

```sh
make validate-plan
```

## Сводки приемки и действий пользователя

Сводки являются только локальными документационными артефактами. Они не создают
web UI, frontend routes или backend endpoints.

Сгенерировать обе сводки:

```sh
make generate-dashboards
```

Файлы сводок:

- `docs/acceptance-dashboard.md`: человекочитаемое окно приемки.
- `docs/acceptance-dashboard.yml`: машинно-читаемое состояние приемки.
- `docs/user-action-dashboard.md`: человекочитаемое окно вопросов и действий пользователя.
- `docs/user-action-dashboard.yml`: машинно-читаемое состояние действий пользователя.

Сводка приемки агрегирует `docs/grace/execution-packets.xml`,
`docs/artifact-registry.yml`, `docs/acceptance/*.acceptance.md` и
`docs/status-report.md`.

Сводка действий пользователя агрегирует `data/questions/*.yml` и
`docs/audit/audit-findings.yml`. Codex не должен заполнять `answered_by`,
`answered_at`, `accepted_by` или `decided_by` за пользователя.

Принятые артефакты защищены. Если артефакт принят пользователем или заблокирован
в `docs/artifact-registry.yml`, Codex должен создать `change request` или
`requires_user_approval` до любого существенного изменения.

## Сводка проверок

Сводка проверок — локальное окно ручной проверки. Она не заменяет pytest,
`make validate-plan`, `make validate-reference`, `make compare-reference-fixtures`,
monthly test protocol или сводку приемки.

Сгенерировать dashboard:

```sh
make generate-verification-dashboard
```

Проверить dashboard:

```sh
make validate-verification
```

Файлы:

- `docs/verification-dashboard.md`: человекочитаемый checklist ручной проверки.
- `docs/verification-dashboard.yml`: машинно-читаемый реестр verification tasks.
- `docs/monthly/2026-06/03-test-protocol-reference-data-governance.md`: источник monthly test protocol.

Codex не должен отмечать manual checks как passed, не должен выставлять
`checked_by: Codex` и не должен считать verification приемкой. Пользователь
заполняет `user_result` в `docs/verification-dashboard.yml` после выполнения
проверок.

Процесс пользовательской приемки:

1. Открыть нужный отчет `docs/acceptance/<PACKET_ID>.acceptance.md`.
2. Проверить перечисленные артефакты и критерии.
3. Запустить команды проверки из отчета.
4. Заполнить `acceptance_decision`, `accepted_by`, `accepted_at` и `comments`.

## Процесс Codex audit

`EP-009-CODEX-SPEC-AUDIT` добавляет контур audit-first/read-mostly. Он фиксирует
нарушения в `docs/audit/audit-findings.yml`, создает отчеты
`docs/audit/codex-spec-audit.md` и `docs/audit/language-audit-report.md`, но не
выполняет массовую русификацию и не исправляет accepted/protected artifacts без
user approval.

Команды:

```sh
make audit-codex-spec
make audit-language
make validate-audit
make audit
```

Находки `medium`/`low` из `language audit` не блокируют `make check`.
Находки `critical` должны блокировать соответствующую audit-команду.

## Git workflow

`Git workflow` описан в `docs/git-workflow.md`. Новый `execution packet` должен
выполняться в ветке формата `ep-<number>-<short-slug>`, если задача не
`read-only` и не является продолжением текущей packet-ветки.

Advisory validation:

```sh
make validate-git-workflow
```

Strict validation перед подготовкой merge:

```sh
make validate-git-workflow-strict
```

Codex не выполняет `git add`, `git commit`, `git push`, `git merge` или удаление
веток в рамках validator. Merge в `main` запрещен без `acceptance_decision =
accepted`, заполненного `accepted_by`, успешного `make check`, отсутствия
находок `critical`/`high` и явного user approval.

## Процесс синхронизации диссертации

Tartip не редактирует диссертацию напрямую. Изменения проекта сначала
проверяются на влияние на диссертацию и только затем превращаются в
контролируемые prompts.

Процесс:

1. `Execution packet` Tartip завершен.
2. Влияние на диссертацию записано в `docs/dissertation/dissertation-impact-log.yml`.
3. Запись для обновления раздела внесена в `docs/dissertation/section-update-queue.yml`.
4. При необходимости prompt создается в `docs/dissertation/prompt-queue/pending/`.
5. Пользователь проверяет prompt.
6. После приемки prompt может быть подготовлен markdown patch в `docs/dissertation/patches/pending/`.
7. После приемки patch DOCX можно обновлять только по явной команде пользователя.
8. DOCX update требует render/visual check.

Запустить проверки синхронизации диссертации:

```sh
make validate-dissertation-sync
make validate-dissertation-prompts
make generate-dissertation-prompts
```

Принятые артефакты защищены. Codex не должен отмечать `dissertation prompts`,
`patches`, `DOCX updates` или `acceptance reports` как `accepted`.
