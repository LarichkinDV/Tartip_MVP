# Tartip

`Tartip` is a local-first project skeleton for BIM5D cost-schedule matching.
The current scope is infrastructure only: Docker Compose, FastAPI backend,
Vite React frontend, PostgreSQL, Adminer, backup scripts, and CI checks.

Business matching logic for BIM, KSI, GESN, BoQ, work packages, actual records,
and plan-fact comparisons is intentionally not implemented in `EP-001-INFRA`.

## Local Run

Create a local environment file from the example:

```sh
cp .env.example .env
```

Start the local stack:

```sh
make up
```

Useful URLs:

- Backend health endpoint: http://localhost:8000/health
- Backend OpenAPI docs: http://localhost:8000/docs
- Frontend: http://localhost:5173
- Adminer: http://localhost:8080

Stop the stack:

```sh
make down
```

View logs:

```sh
make logs
```

The first Docker run can pull public base images and package dependencies.
Run it only when network access is acceptable.

## Development Commands

Run backend tests:

```sh
make test
```

Run linting:

```sh
make lint
```

Run formatting:

```sh
make format
```

Run project checks:

```sh
make check
```

Generate project dashboards:

```sh
make generate-dashboards
```

Run Codex audit checks:

```sh
make audit
```

Run Git workflow advisory checks:

```sh
make validate-git-workflow
```

When Docker is not installed, `make check` still runs repository safety checks and
prints that the Docker Compose syntax check was skipped. Full stack validation
requires Docker, but Python, Ruff, pytest, npm, and TypeScript checks can run
locally from `.venv` and `frontend/node_modules`.

Dockerless verification checklist:

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

## Database Backups

Create a PostgreSQL custom-format backup in the mounted `backups/` directory:

```sh
make backup
```

Restore from a backup file:

```sh
CONFIRM_RESTORE=1 BACKUP_FILE=backups/tartip_YYYYMMDD_HHMMSS.dump make restore
```

Do not commit `.env` files or unencrypted database dumps. `scripts/check_project.sh`
checks these safety rules.

## Reference Data Workflow

Reference governance follows the project rule: `No source — no rule`.
Codex does not download external KSI/FSNB/GESN data and does not invent classifier
codes, norm codes, norm units, work composition, resources, coefficients, or normative values.

User-provided source files go into the `inbox` layer first:

- KSI files: `data/reference/inbox/ksi/`
- FSNB/GESN files: `data/reference/inbox/fsnb/`
- Project work type dictionaries: `data/reference/inbox/work_types/`

Lifecycle layers:

- `data/reference/inbox/`: user placed an original local file.
- `data/reference/quarantine/`: file detected but not accepted as a source.
- `data/reference/raw/`: immutable accepted copy with checksum.
- `data/reference/staging/`: parsed temporary records.
- `data/reference/normalized/`: normalized lookup-ready records.
- `data/reference/manifests/`: source manifest and import log.
- `data/reference/reports/`: validation, import, and comparison reports.

Files in `inbox` are not trusted evidence. A source can be used only after it is
accepted into `raw`, receives `checksum_sha256`, and is registered in
`data/reference/manifests/source-manifest.yml` with allowed source authority.

Validate reference sources and matching rule evidence:

```sh
make validate-reference
```

Generate structured data questions for missing sources or evidence:

```sh
make generate-data-questions
```

Run fake delta-versioning fixtures:

```sh
make compare-reference-fixtures
```

The fake fixtures are only for testing versioning mechanics. They are not
classifier or normative evidence.

## Project Planning And Acceptance Workflow

The project plan is in `docs/project-plan.md`. It is a human-readable summary;
the actual artifact source of truth is `docs/artifact-registry.yml`.

Execution packets live in `docs/grace/execution-packets.xml`. Each packet should
be traceable to actual artifacts, verification scenarios, and an acceptance
report in `docs/acceptance/`.

Codex may prepare a packet as `ready_for_acceptance`, but only the user may set
an acceptance decision such as `accepted`, `rejected`, or `needs_revision`.
`accepted_by` must not be `Codex`.

Validate the project planning contour:

```sh
make validate-plan
```

## Acceptance And User Action Dashboards

Dashboards are local documentation artifacts only. They do not create web UI,
frontend routes, or backend endpoints.

Generate both dashboards:

```sh
make generate-dashboards
```

Dashboard files:

- `docs/acceptance-dashboard.md`: human-readable acceptance window.
- `docs/acceptance-dashboard.yml`: machine-readable acceptance state.
- `docs/user-action-dashboard.md`: human-readable user question and action window.
- `docs/user-action-dashboard.yml`: machine-readable user action state.

The acceptance dashboard aggregates `docs/grace/execution-packets.xml`,
`docs/artifact-registry.yml`, `docs/acceptance/*.acceptance.md`, and
`docs/status-report.md`.

The user action dashboard aggregates `data/questions/*.yml` and
`docs/audit/audit-findings.yml`. Codex must not fill `answered_by`,
`answered_at`, `accepted_by`, or `decided_by` for the user.

Accepted artifacts are protected. If an artifact is accepted by the user or
locked in `docs/artifact-registry.yml`, Codex must create a change request or
`requires_user_approval` action before any material change.

## Verification Dashboard

The verification dashboard is a local manual testing window. It does not replace
pytest, `make validate-plan`, `make validate-reference`, `make compare-reference-fixtures`,
the monthly test protocol, or the acceptance dashboard.

Generate it:

```sh
make generate-verification-dashboard
```

Validate it:

```sh
make validate-verification
```

Files:

- `docs/verification-dashboard.md`: human-readable manual verification checklist.
- `docs/verification-dashboard.yml`: machine-readable verification task registry.
- `docs/monthly/2026-06/03-test-protocol-reference-data-governance.md`: monthly test protocol source.

Codex must not mark manual checks as passed, must not set `checked_by: Codex`,
and must not treat verification as acceptance. The user fills `user_result` in
`docs/verification-dashboard.yml` after performing checks.

User acceptance flow:

1. Open the relevant `docs/acceptance/<PACKET_ID>.acceptance.md` report.
2. Review listed artifacts and criteria.
3. Run the report's verification commands.
4. Fill `acceptance_decision`, `accepted_by`, `accepted_at`, and `comments`.

## Codex Audit Workflow

`EP-009-CODEX-SPEC-AUDIT` добавляет audit-first/read-mostly контур. Он фиксирует нарушения в `docs/audit/audit-findings.yml`, создает отчеты `docs/audit/codex-spec-audit.md` и `docs/audit/language-audit-report.md`, но не выполняет массовую русификацию и не исправляет accepted/protected artifacts без user approval.

Команды:

```sh
make audit-codex-spec
make audit-language
make validate-audit
make audit
```

Medium/low language findings не блокируют `make check`. Critical findings должны блокировать соответствующую audit-команду.

## Git Workflow

Git workflow описан в `docs/git-workflow.md`. Новый execution packet должен выполняться в ветке формата `ep-<number>-<short-slug>`, если задача не read-only и не является продолжением текущей packet-ветки.

Advisory validation:

```sh
make validate-git-workflow
```

Strict validation перед merge preparation:

```sh
make validate-git-workflow-strict
```

Codex не выполняет `git add`, `git commit`, `git push`, `git merge` или удаление веток в рамках validator. Merge в `main` запрещен без `acceptance_decision = accepted`, заполненного `accepted_by`, успешного `make check`, отсутствия critical/high audit findings и явного user approval.

## Dissertation Synchronization Workflow

Tartip does not edit the dissertation directly. Project changes are first checked for dissertation impact and only then converted into controlled prompts.

Workflow:

1. Tartip execution packet is completed.
2. Dissertation impact is recorded in `docs/dissertation/dissertation-impact-log.yml`.
3. A section update entry is recorded in `docs/dissertation/section-update-queue.yml`.
4. If needed, a prompt is generated in `docs/dissertation/prompt-queue/pending/`.
5. The user reviews the prompt.
6. After prompt acceptance, a markdown patch can be prepared in `docs/dissertation/patches/pending/`.
7. After patch acceptance, DOCX can be updated only by explicit user request.
8. DOCX update requires render/visual check.

Run dissertation sync checks:

```sh
make validate-dissertation-sync
make validate-dissertation-prompts
make generate-dissertation-prompts
```

Accepted artifacts are protected. Codex must not mark dissertation prompts, patches, DOCX updates, or acceptance reports as accepted.
