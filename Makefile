SHELL := /bin/sh

COMPOSE ?= docker compose
PYTHON ?= python3
NPM ?= npm

BACKEND_DIR := backend
FRONTEND_DIR := frontend

.PHONY: up down logs test lint format backup restore check validate-reference compare-reference-fixtures generate-data-questions

up:
	$(COMPOSE) up --build

down:
	$(COMPOSE) down

logs:
	$(COMPOSE) logs --follow

test:
	cd $(BACKEND_DIR) && $(PYTHON) -m pytest

lint:
	cd $(BACKEND_DIR) && $(PYTHON) -m ruff check .
	cd $(FRONTEND_DIR) && $(NPM) run lint

format:
	cd $(BACKEND_DIR) && $(PYTHON) -m ruff format .
	cd $(FRONTEND_DIR) && $(NPM) run format

backup:
	./scripts/backup_db.sh

restore:
	./scripts/restore_db.sh $(BACKUP_FILE)

check:
	./scripts/check_project.sh
	@if command -v docker >/dev/null 2>&1; then \
		$(COMPOSE) config --quiet; \
	else \
		printf 'Docker is not installed; skipped Docker Compose syntax check.\n'; \
	fi

validate-reference:
	$(PYTHON) scripts/validate_reference_sources.py

compare-reference-fixtures:
	$(PYTHON) scripts/compare_reference_releases.py --fixture

generate-data-questions:
	$(PYTHON) scripts/generate_data_questions.py
