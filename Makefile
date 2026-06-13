SHELL := /bin/sh

COMPOSE ?= docker compose
PYTHON ?= python3
NPM ?= npm

BACKEND_DIR := backend
FRONTEND_DIR := frontend

.PHONY: up down logs test lint format backup restore check regenerate verify validate-plan validate-reference validate-reference-intake validate-data-contribution validate-verification validate-dissertation-prompts validate-dissertation-sync validate-monthly-planning validate-legal-data-boundary-notes validate-git-workflow validate-git-workflow-strict validate-user-review-workbench validate-post-acceptance-state validate-accepted-artifact-protection audit-codex-spec audit-language validate-audit audit compare-reference-fixtures generate-data-questions generate-dissertation-prompts generate-acceptance-dashboard generate-user-action-dashboard generate-verification-dashboard generate-user-review-workbench generate-dashboards apply-user-review-decisions-dry-run apply-user-review-decisions sync-accepted-packet-dry-run sync-accepted-packet

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
	$(MAKE) validate-reference-intake
	$(MAKE) validate-data-contribution
	$(MAKE) validate-dissertation-sync
	$(MAKE) validate-dissertation-prompts
	$(MAKE) validate-monthly-planning
	$(MAKE) validate-legal-data-boundary-notes
	$(MAKE) generate-acceptance-dashboard
	$(MAKE) generate-verification-dashboard
	$(MAKE) audit
	$(MAKE) generate-user-action-dashboard
	$(MAKE) generate-user-review-workbench
	$(MAKE) validate-plan
	$(MAKE) validate-verification
	$(MAKE) validate-user-review-workbench
	$(MAKE) validate-post-acceptance-state
	$(MAKE) validate-accepted-artifact-protection
	@if command -v docker >/dev/null 2>&1; then \
		$(COMPOSE) config --quiet; \
	else \
		printf 'Docker is not installed; skipped Docker Compose syntax check.\n'; \
	fi

regenerate:
	$(MAKE) generate-dashboards
	$(MAKE) audit

verify:
	./scripts/check_project.sh
	$(MAKE) validate-reference-intake
	$(MAKE) validate-data-contribution
	$(MAKE) validate-dissertation-sync
	$(MAKE) validate-dissertation-prompts
	$(MAKE) validate-monthly-planning
	$(MAKE) validate-legal-data-boundary-notes
	$(MAKE) validate-plan
	$(MAKE) validate-verification
	$(MAKE) validate-user-review-workbench
	$(MAKE) validate-post-acceptance-state
	$(MAKE) validate-accepted-artifact-protection
	$(MAKE) validate-audit

validate-plan:
	$(PYTHON) scripts/validate_project_plan.py

validate-reference:
	$(PYTHON) scripts/validate_reference_sources.py

validate-reference-intake:
	$(PYTHON) scripts/validate_reference_intake.py

validate-data-contribution:
	$(PYTHON) scripts/validate_data_contribution.py

validate-verification:
	$(PYTHON) scripts/validate_verification_dashboard.py

validate-dissertation-prompts:
	$(PYTHON) scripts/validate_dissertation_prompts.py

validate-dissertation-sync:
	$(PYTHON) scripts/validate_dissertation_sync.py

validate-monthly-planning:
	$(PYTHON) scripts/validate_monthly_planning.py

validate-legal-data-boundary-notes:
	$(PYTHON) scripts/validate_legal_data_boundary_notes.py

validate-git-workflow:
	$(PYTHON) scripts/validate_git_workflow.py --advisory

validate-git-workflow-strict:
	$(PYTHON) scripts/validate_git_workflow.py --strict

validate-user-review-workbench:
	$(PYTHON) scripts/validate_user_review_workbench.py

validate-post-acceptance-state:
	$(PYTHON) scripts/validate_post_acceptance_state.py

validate-accepted-artifact-protection:
	$(PYTHON) scripts/validate_accepted_artifact_protection.py

audit-codex-spec:
	$(PYTHON) scripts/audit_codex_spec.py

audit-language:
	$(PYTHON) scripts/audit_language_policy.py

validate-audit:
	$(PYTHON) scripts/validate_audit_reports.py

audit: audit-codex-spec audit-language validate-audit

compare-reference-fixtures:
	$(PYTHON) scripts/compare_reference_releases.py --fixture

generate-data-questions:
	$(PYTHON) scripts/generate_data_questions.py

generate-dissertation-prompts:
	$(PYTHON) scripts/generate_dissertation_prompts.py

generate-acceptance-dashboard:
	$(PYTHON) scripts/generate_acceptance_dashboard.py

generate-user-action-dashboard:
	$(PYTHON) scripts/generate_user_action_dashboard.py

generate-verification-dashboard:
	$(PYTHON) scripts/generate_verification_dashboard.py

generate-user-review-workbench:
	$(PYTHON) scripts/generate_user_review_workbench.py

generate-dashboards: generate-acceptance-dashboard generate-user-action-dashboard generate-verification-dashboard generate-user-review-workbench

apply-user-review-decisions-dry-run:
	$(PYTHON) scripts/apply_user_review_decisions.py --dry-run

apply-user-review-decisions:
	$(PYTHON) scripts/apply_user_review_decisions.py --apply

sync-accepted-packet-dry-run:
	@if [ -z "$(PACKET)" ]; then \
		printf 'PACKET is required. Example: make sync-accepted-packet-dry-run PACKET=EP-017-AUDIT-FINDINGS-CLEANUP\n' >&2; \
		exit 2; \
	fi
	$(PYTHON) scripts/sync_accepted_packet.py $(PACKET) --dry-run

sync-accepted-packet:
	@if [ -z "$(PACKET)" ]; then \
		printf 'PACKET is required. Example: make sync-accepted-packet PACKET=EP-017-AUDIT-FINDINGS-CLEANUP\n' >&2; \
		exit 2; \
	fi
	$(PYTHON) scripts/sync_accepted_packet.py $(PACKET) --apply
	$(MAKE) generate-dashboards
	$(MAKE) verify
