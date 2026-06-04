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
make validate-reference
make compare-reference-fixtures
make generate-data-questions
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
