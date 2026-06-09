# Changelog

## 0.1.0 - 2026-06-04

- Added `EP-001-INFRA` local infrastructure skeleton.
- Added Dockerless verification checklist for local checks when Docker is unavailable.
- Added GRACE-light artifacts for execution packets, module contracts, verification scenarios, and the knowledge graph.
- Added backend and frontend skeletons with FastAPI, pytest, Vite, React, and TypeScript.
- Added reference governance scaffolding for source manifests, import logs, question registries, and `No source — no rule` policy.
- Added reference versioning scaffolding with documented delta schemas, canonical hashing, comparison utility, and fake fixtures.
- Added safety checks and backup scripts for local project hygiene and database backup/restore workflows.
- Added project planning contour, artifact registry, traceability matrix, decision log, status report, and acceptance reports.
- Added acceptance owner discipline and `scripts/validate_project_plan.py` with `make validate-plan`.
- Added `EP-005-ACCEPTANCE-AND-USER-ACTION-DASHBOARDS` for local acceptance and user action dashboards.
- Added accepted artifact protection discipline, dashboard generators, `make generate-dashboards`, and dashboard validation checks.
- Added `EP-007-VERIFICATION-DASHBOARD` for local manual verification tracking without web UI.
- Added monthly test protocol scaffolding, verification dashboard generator/validator, and `make validate-verification`.
- Added `EP-008-DISSERTATION-PROMPT-GENERATION` for dissertation impact logging, prompt generation, forbidden claim checks, and DOCX update guardrails.
- Added dissertation prompt profiles, prompt templates, prompt/patch queues, and validation commands without creating DOCX/PDF dissertation files.
- Added `EP-009-CODEX-SPEC-AUDIT` for audit-first Codex specification checks, language policy, audit findings, and audit report validation.
- Added audit Makefile targets and user-action dashboard integration for audit findings without mass-russifying existing documents.
- Added `EP-011-GIT-WORKFLOW-DISCIPLINE` for branch naming, dirty working tree handling, merge gates, forbidden Git files, and advisory/strict Git workflow validation.
- Prepared `EP-013-POST-ACCEPTANCE-STATE-SYNC` to synchronize the accepted baseline after the accepted acceptance cycle.
- Reflected accepted EP-001, EP-002, EP-003, EP-004, EP-005, EP-007, EP-008, EP-009, EP-011, and EP-012 as the post-acceptance baseline.
- Added post-acceptance validation scaffolding and follow-up roadmap for artifact protection, verification reconciliation, reference intake, and audit cleanup.
