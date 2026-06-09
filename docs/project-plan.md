# Project Plan

`docs/project-plan.md` is a human-readable summary. The artifact source of truth is [artifact-registry.yml](artifact-registry.yml), while packet definitions remain in [execution-packets.xml](grace/execution-packets.xml).

## 1. Project Goal

Create a local-first system for BIM5D cost-schedule matching that keeps BIM elements, KSI classification, calculation units, GESN candidates, work packages, schedule tasks, actual records, plan-fact comparison, and control decisions separated by explicit contracts and review gates.

## 2. Current Version

`0.1.0`

## 3. Current Stage

Project foundation, governance contour, dashboard-based acceptance coordination, manual verification tracking, dissertation synchronization prompt generation, Codex specification audit contour, Git workflow discipline, and user review workbench.

## 4. Current Execution Packet

`EP-012-USER-REVIEW-WORKBENCH-AND-ACCEPTANCE-STANDARD`

## 5. Stage Table

| Stage | Scope | Status | Main Artifacts |
|---|---|---|---|
| Foundation | Local infrastructure, backend/frontend skeleton, safety checks | ready_for_acceptance | [README.md](../README.md), [Makefile](../Makefile), [docker-compose.yml](../docker-compose.yml) |
| Reference Governance | Source discipline, manifests, question registries | ready_for_acceptance | [reference data policy](07-reference-data-policy.md), [source manifest](../data/reference/manifests/source-manifest.yml) |
| Reference Versioning | Delta schemas, canonical hashes, fixture comparison | ready_for_acceptance | [reference versioning schema](../db/schemas/reference_versioning.sql), [compare script](../scripts/compare_reference_releases.py) |
| Planning And Acceptance | Project plan, artifact registry, acceptance reports | ready_for_acceptance | [artifact registry](artifact-registry.yml), [status report](status-report.md), [EP-004 acceptance](acceptance/EP-004-PROJECT-PLANNING-AND-ACCEPTANCE.acceptance.md) |
| Acceptance Dashboards | Acceptance dashboard, user action dashboard, accepted artifact protection | ready_for_acceptance | [acceptance dashboard](acceptance-dashboard.md), [user action dashboard](user-action-dashboard.md), [EP-005 acceptance](acceptance/EP-005-ACCEPTANCE-AND-USER-ACTION-DASHBOARDS.acceptance.md) |
| Verification Dashboard | Manual verification window, monthly protocol checks, user-owned check results | ready_for_acceptance | [verification dashboard](verification-dashboard.md), [monthly protocol](monthly/2026-06/03-test-protocol-reference-data-governance.md), [EP-007 acceptance](acceptance/EP-007-VERIFICATION-DASHBOARD.acceptance.md) |
| Dissertation Sync | Impact log, prompt profiles, prompt templates, prompt queues, patch queues, and DOCX guardrails | ready_for_acceptance | [dissertation README](dissertation/README.md), [forbidden claims](dissertation/prompt-profiles/forbidden-claims.yml), [EP-008 acceptance](acceptance/EP-008-DISSERTATION-PROMPT-GENERATION.acceptance.md) |
| Codex Spec Audit | Audit-first/read-mostly checks, language policy, audit findings, and audit reports | ready_for_acceptance | [audit README](audit/README.md), [audit findings](audit/audit-findings.yml), [EP-009 acceptance](acceptance/EP-009-CODEX-SPEC-AUDIT.acceptance.md) |
| Git Workflow | Branch naming, dirty tree handling, merge gates, and forbidden Git files | ready_for_acceptance | [git workflow](git-workflow.md), [git workflow validator](../scripts/validate_git_workflow.py), [EP-011 acceptance](acceptance/EP-011-GIT-WORKFLOW-DISCIPLINE.acceptance.md) |
| User Review Workbench | Active user review queue, safe decision application, and empty blockers/risks standard | ready_for_acceptance | [user review workbench](user-review-workbench.md), [workbench generator](../scripts/generate_user_review_workbench.py), [EP-012 acceptance](acceptance/EP-012-USER-REVIEW-WORKBENCH-AND-ACCEPTANCE-STANDARD.acceptance.md) |

## 6. Execution Packets

| Packet | Name | Codex Status | Acceptance Report | Next Step |
|---|---|---|---|---|
| EP-001-INFRA | Prepare local infrastructure | ready_for_acceptance | [EP-001 report](acceptance/EP-001-INFRA.acceptance.md) | User checks Docker-dependent behavior when Docker is available. |
| EP-002-REFERENCE-GOVERNANCE | Reference data governance | ready_for_acceptance | [EP-002 report](acceptance/EP-002-REFERENCE-GOVERNANCE.acceptance.md) | User provides official local reference sources when available. |
| EP-003-REFERENCE-VERSIONING | Delta-based reference versioning | ready_for_acceptance | [EP-003 report](acceptance/EP-003-REFERENCE-VERSIONING.acceptance.md) | User reviews fake fixture behavior and schema direction. |
| EP-004-PROJECT-PLANNING-AND-ACCEPTANCE | Project planning and acceptance contour | ready_for_acceptance | [EP-004 report](acceptance/EP-004-PROJECT-PLANNING-AND-ACCEPTANCE.acceptance.md) | User performs acceptance decision. |
| EP-005-ACCEPTANCE-AND-USER-ACTION-DASHBOARDS | Acceptance and user action dashboards | ready_for_acceptance | [EP-005 report](acceptance/EP-005-ACCEPTANCE-AND-USER-ACTION-DASHBOARDS.acceptance.md) | User reviews dashboards and accepted artifact protection rules. |
| EP-007-VERIFICATION-DASHBOARD | Verification dashboard | ready_for_acceptance | [EP-007 report](acceptance/EP-007-VERIFICATION-DASHBOARD.acceptance.md) | User performs manual verification checks and fills user_result fields. |
| EP-008-DISSERTATION-PROMPT-GENERATION | Dissertation prompt generation contour | ready_for_acceptance | [EP-008 report](acceptance/EP-008-DISSERTATION-PROMPT-GENERATION.acceptance.md) | User reviews dissertation sync guardrails, prompt profiles, templates, and DOCX restrictions. |
| EP-009-CODEX-SPEC-AUDIT | Codex specification audit and language policy | ready_for_acceptance | [EP-009 report](acceptance/EP-009-CODEX-SPEC-AUDIT.acceptance.md) | User reviews audit findings, language policy, and audit scripts. |
| EP-011-GIT-WORKFLOW-DISCIPLINE | Git workflow discipline | ready_for_acceptance | [EP-011 report](acceptance/EP-011-GIT-WORKFLOW-DISCIPLINE.acceptance.md) | User reviews branch/merge policy and advisory/strict validator behavior. |
| EP-012-USER-REVIEW-WORKBENCH-AND-ACCEPTANCE-STANDARD | User review workbench and acceptance standard | ready_for_acceptance | [EP-012 report](acceptance/EP-012-USER-REVIEW-WORKBENCH-AND-ACCEPTANCE-STANDARD.acceptance.md) | User reviews the active review queue and safe decision application workflow. |

## 7. Status Values

Allowed packet statuses: `planned`, `in_progress`, `ready_for_acceptance`, `accepted`, `needs_revision`, `rejected`, `blocked`, `deprecated`.

Codex may set `ready_for_acceptance`; only the user may set `accepted`, `needs_revision`, or `rejected`.

## 8. Main Artifacts

- [Artifact registry](artifact-registry.yml)
- [Traceability matrix](traceability-matrix.md)
- [Decision log](decision-log.md)
- [Status report](status-report.md)
- [Acceptance dashboard](acceptance-dashboard.md)
- [User action dashboard](user-action-dashboard.md)
- [Verification dashboard](verification-dashboard.md)
- [Dissertation synchronization](dissertation/README.md)
- [Codex audit contour](audit/README.md)
- [Audit findings](audit/audit-findings.yml)
- [Git workflow discipline](git-workflow.md)
- [User review workbench](user-review-workbench.md)
- [Monthly test protocol](monthly/2026-06/03-test-protocol-reference-data-governance.md)
- [GRACE execution packets](grace/execution-packets.xml)
- [GRACE verification plan](grace/verification-plan.xml)
- [Acceptance reports](acceptance/README.md)

## 9. Acceptance Reports

- [EP-001-INFRA.acceptance.md](acceptance/EP-001-INFRA.acceptance.md)
- [EP-002-REFERENCE-GOVERNANCE.acceptance.md](acceptance/EP-002-REFERENCE-GOVERNANCE.acceptance.md)
- [EP-003-REFERENCE-VERSIONING.acceptance.md](acceptance/EP-003-REFERENCE-VERSIONING.acceptance.md)
- [EP-004-PROJECT-PLANNING-AND-ACCEPTANCE.acceptance.md](acceptance/EP-004-PROJECT-PLANNING-AND-ACCEPTANCE.acceptance.md)
- [EP-005-ACCEPTANCE-AND-USER-ACTION-DASHBOARDS.acceptance.md](acceptance/EP-005-ACCEPTANCE-AND-USER-ACTION-DASHBOARDS.acceptance.md)
- [EP-007-VERIFICATION-DASHBOARD.acceptance.md](acceptance/EP-007-VERIFICATION-DASHBOARD.acceptance.md)
- [EP-008-DISSERTATION-PROMPT-GENERATION.acceptance.md](acceptance/EP-008-DISSERTATION-PROMPT-GENERATION.acceptance.md)
- [EP-009-CODEX-SPEC-AUDIT.acceptance.md](acceptance/EP-009-CODEX-SPEC-AUDIT.acceptance.md)
- [EP-011-GIT-WORKFLOW-DISCIPLINE.acceptance.md](acceptance/EP-011-GIT-WORKFLOW-DISCIPLINE.acceptance.md)
- [EP-012-USER-REVIEW-WORKBENCH-AND-ACCEPTANCE-STANDARD.acceptance.md](acceptance/EP-012-USER-REVIEW-WORKBENCH-AND-ACCEPTANCE-STANDARD.acceptance.md)

## 10. Blockers

- Docker is not installed locally, so Docker Compose syntax and service runtime checks are skipped by `make check` with an explicit message.
- Real KSI/FSNB/GESN source files are absent; matching rules remain drafts or candidates requiring evidence.
- User acceptance decisions remain pending until Дмитрий reviews the relevant acceptance reports and dashboards.
- Manual verification results remain pending until Дмитрий fills `user_result` in `docs/verification-dashboard.yml`.
- DOCX update is blocked until an accepted markdown patch and explicit user request exist.
- Existing language findings remain open until the user selects a follow-up correction strategy.
- EP-012 must not apply user decisions until source checksums match and `accepted_by` is not Codex.

## 11. Next Step

User reviews [EP-012 acceptance report](acceptance/EP-012-USER-REVIEW-WORKBENCH-AND-ACCEPTANCE-STANDARD.acceptance.md), checks [user review workbench](user-review-workbench.md), and decides whether the workbench can be used to prepare future acceptance decisions.
