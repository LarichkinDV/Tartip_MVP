# Project Plan

`docs/project-plan.md` is a human-readable summary. The artifact source of truth is [artifact-registry.yml](artifact-registry.yml), while packet definitions remain in [execution-packets.xml](grace/execution-packets.xml).

## 1. Project Goal

Create a local-first system for BIM5D cost-schedule matching that keeps BIM elements, KSI classification, calculation units, GESN candidates, work packages, schedule tasks, actual records, plan-fact comparison, and control decisions separated by explicit contracts and review gates.

## 2. Current Version

`0.1.0`

## 3. Project State

Current execution packet: `EP-013-POST-ACCEPTANCE-STATE-SYNC`.

```yaml
project_state: accepted_baseline
active_execution_packet: EP-013-POST-ACCEPTANCE-STATE-SYNC
next_recommended_packet: EP-014-ACCEPTED-ARTIFACT-PROTECTION
previous_active_execution_packet: EP-012-USER-REVIEW-WORKBENCH-AND-ACCEPTANCE-STANDARD
```

## 4. Current Stage

Post-acceptance state synchronization after the first accepted baseline. The previous acceptance cycle is closed by user decisions in `docs/acceptance/*.acceptance.md`; EP-013 reflects those decisions in project registries, dashboards, and status documents.

## 5. Post-Acceptance Baseline

The acceptance reports are the source of truth for user acceptance decisions.

```yaml
post_acceptance_baseline:
  accepted_packets:
    - EP-001-INFRA
    - EP-002-REFERENCE-GOVERNANCE
    - EP-003-REFERENCE-VERSIONING
    - EP-004-PROJECT-PLANNING-AND-ACCEPTANCE
    - EP-005-ACCEPTANCE-AND-USER-ACTION-DASHBOARDS
    - EP-007-VERIFICATION-DASHBOARD
    - EP-008-DISSERTATION-PROMPT-GENERATION
    - EP-009-CODEX-SPEC-AUDIT
    - EP-011-GIT-WORKFLOW-DISCIPLINE
    - EP-012-USER-REVIEW-WORKBENCH-AND-ACCEPTANCE-STANDARD
```

EP-012 was the previous active packet before the acceptance queue was closed. EP-013 does not re-accept earlier packets; it only synchronizes state from user-owned acceptance reports.

## 6. Stage Table

| Stage | Scope | Status | Main Artifacts |
|---|---|---|---|
| Foundation | Local infrastructure, backend/frontend skeleton, safety checks | accepted | [README.md](../README.md), [Makefile](../Makefile), [docker-compose.yml](../docker-compose.yml) |
| Reference Governance | Source discipline, manifests, question registries | accepted | [reference data policy](07-reference-data-policy.md), [source manifest](../data/reference/manifests/source-manifest.yml) |
| Reference Versioning | Delta schemas, canonical hashes, fixture comparison | accepted | [reference versioning schema](../db/schemas/reference_versioning.sql), [compare script](../scripts/compare_reference_releases.py) |
| Planning And Acceptance | Project plan, artifact registry, acceptance reports | accepted | [artifact registry](artifact-registry.yml), [status report](status-report.md), [EP-004 acceptance](acceptance/EP-004-PROJECT-PLANNING-AND-ACCEPTANCE.acceptance.md) |
| Acceptance Dashboards | Acceptance dashboard, user action dashboard, accepted artifact protection discipline | accepted | [acceptance dashboard](acceptance-dashboard.md), [user action dashboard](user-action-dashboard.md), [EP-005 acceptance](acceptance/EP-005-ACCEPTANCE-AND-USER-ACTION-DASHBOARDS.acceptance.md) |
| Verification Dashboard | Manual verification window, monthly protocol checks, user-owned check results | accepted | [verification dashboard](verification-dashboard.md), [monthly protocol](monthly/2026-06/03-test-protocol-reference-data-governance.md), [EP-007 acceptance](acceptance/EP-007-VERIFICATION-DASHBOARD.acceptance.md) |
| Dissertation Sync | Impact log, prompt profiles, prompt templates, prompt queues, patch queues, and DOCX guardrails | accepted | [dissertation README](dissertation/README.md), [forbidden claims](dissertation/prompt-profiles/forbidden-claims.yml), [EP-008 acceptance](acceptance/EP-008-DISSERTATION-PROMPT-GENERATION.acceptance.md) |
| Codex Spec Audit | Audit-first/read-mostly checks, language policy, audit findings, and audit reports | accepted | [audit README](audit/README.md), [audit findings](audit/audit-findings.yml), [EP-009 acceptance](acceptance/EP-009-CODEX-SPEC-AUDIT.acceptance.md) |
| Git Workflow | Branch naming, dirty tree handling, merge gates, and forbidden Git files | accepted | [git workflow](git-workflow.md), [git workflow validator](../scripts/validate_git_workflow.py), [EP-011 acceptance](acceptance/EP-011-GIT-WORKFLOW-DISCIPLINE.acceptance.md) |
| User Review Workbench | Active user review queue, safe decision application, and empty blockers/risks standard | accepted | [user review workbench](user-review-workbench.md), [workbench generator](../scripts/generate_user_review_workbench.py), [EP-012 acceptance](acceptance/EP-012-USER-REVIEW-WORKBENCH-AND-ACCEPTANCE-STANDARD.acceptance.md) |
| Post-Acceptance State Sync | Accepted baseline synchronization, follow-up debt visibility, and validation | ready_for_acceptance | [EP-013 acceptance](acceptance/EP-013-POST-ACCEPTANCE-STATE-SYNC.acceptance.md), [post-acceptance validator](../scripts/validate_post_acceptance_state.py) |

## 7. Execution Packets

| Packet | Name | Status | Acceptance Report | Next Step |
|---|---|---|---|---|
| EP-001-INFRA | Prepare local infrastructure | accepted | [EP-001 report](acceptance/EP-001-INFRA.acceptance.md) | Protected artifact classification is deferred to EP-014. |
| EP-002-REFERENCE-GOVERNANCE | Reference data governance | accepted | [EP-002 report](acceptance/EP-002-REFERENCE-GOVERNANCE.acceptance.md) | Reference intake is deferred to EP-016. |
| EP-003-REFERENCE-VERSIONING | Delta-based reference versioning | accepted | [EP-003 report](acceptance/EP-003-REFERENCE-VERSIONING.acceptance.md) | Real source import waits for EP-016 and later parser work. |
| EP-004-PROJECT-PLANNING-AND-ACCEPTANCE | Project planning and acceptance contour | accepted | [EP-004 report](acceptance/EP-004-PROJECT-PLANNING-AND-ACCEPTANCE.acceptance.md) | Post-acceptance state is synchronized in EP-013. |
| EP-005-ACCEPTANCE-AND-USER-ACTION-DASHBOARDS | Acceptance and user action dashboards | accepted | [EP-005 report](acceptance/EP-005-ACCEPTANCE-AND-USER-ACTION-DASHBOARDS.acceptance.md) | Protection flags are deferred to EP-014. |
| EP-007-VERIFICATION-DASHBOARD | Verification dashboard | accepted | [EP-007 report](acceptance/EP-007-VERIFICATION-DASHBOARD.acceptance.md) | Pending verification checks remain post-acceptance debt for EP-015. |
| EP-008-DISSERTATION-PROMPT-GENERATION | Dissertation prompt generation contour | accepted | [EP-008 report](acceptance/EP-008-DISSERTATION-PROMPT-GENERATION.acceptance.md) | DOCX/PDF updates still require explicit user request. |
| EP-009-CODEX-SPEC-AUDIT | Codex specification audit and language policy | accepted | [EP-009 report](acceptance/EP-009-CODEX-SPEC-AUDIT.acceptance.md) | Stale audit finding cleanup is deferred to EP-017. |
| EP-011-GIT-WORKFLOW-DISCIPLINE | Git workflow discipline | accepted | [EP-011 report](acceptance/EP-011-GIT-WORKFLOW-DISCIPLINE.acceptance.md) | Merge still requires explicit user approval after checks. |
| EP-012-USER-REVIEW-WORKBENCH-AND-ACCEPTANCE-STANDARD | User review workbench and acceptance standard | accepted | [EP-012 report](acceptance/EP-012-USER-REVIEW-WORKBENCH-AND-ACCEPTANCE-STANDARD.acceptance.md) | Workbench remains the active review window. |
| EP-013-POST-ACCEPTANCE-STATE-SYNC | Post-acceptance state sync | ready_for_acceptance | [EP-013 report](acceptance/EP-013-POST-ACCEPTANCE-STATE-SYNC.acceptance.md) | User reviews synchronized accepted baseline. |

## 8. Status Values

Allowed packet statuses: `planned`, `in_progress`, `ready_for_acceptance`, `accepted`, `needs_revision`, `rejected`, `blocked`, `deprecated`.

Codex may prepare `ready_for_acceptance`; `accepted` in EP-013 is a synchronization of existing user decisions from acceptance reports, not a new Codex acceptance action.

## 9. Main Artifacts

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

## 10. Acceptance Reports

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
- [EP-013-POST-ACCEPTANCE-STATE-SYNC.acceptance.md](acceptance/EP-013-POST-ACCEPTANCE-STATE-SYNC.acceptance.md)

## 11. Follow-Up Roadmap

- `EP-014-ACCEPTED-ARTIFACT-PROTECTION`: classify accepted artifacts and introduce protection flags for source/manual artifacts without locking generated dashboards.
- `EP-015-VERIFICATION-DASHBOARD-RECONCILIATION`: reconcile pending verification checks and the `EP-006-MONTHLY-PLANNING-AND-DEFENSE` orphan monthly scope.
- `EP-016-REFERENCE-INTAKE-PREPARATION`: prepare intake of official or project-authorized KSI, FSNB/GESN, and work type sources.
- `EP-017-AUDIT-FINDINGS-CLEANUP`: clean stale audit findings without mass-russification and without changing accepted/protected artifacts.

## 12. Open Follow-Up Debt

- `protected_accepted_artifacts: 0` remains visible and is deferred to `EP-014-ACCEPTED-ARTIFACT-PROTECTION`.
- Pending verification checks are post-acceptance verification debt and do not reopen already accepted acceptance reports.
- `EP-006-MONTHLY-PLANNING-AND-DEFENSE` appears in the verification dashboard but has no corresponding accepted execution packet and no acceptance report; EP-015 must reclassify these checks as monthly-scope checks such as `MONTHLY-2026-06`, or create a future correctly registered package.
- High-priority reference and normative user actions remain open until official or project-authorized local sources are provided.
- Audit findings remain open for EP-017; critical/high findings stay blocking gates and medium/low findings remain advisory.

## 13. Blockers

## 14. Risks

- EP-013 intentionally does not enable protection flags, close verification checks, close user actions, or change audit finding statuses.
- Real KSI/FSNB/GESN sources are still absent, so active normative matching rules remain prohibited by the `No source — no rule` policy.

## 15. Next Step

User reviews [EP-013 acceptance report](acceptance/EP-013-POST-ACCEPTANCE-STATE-SYNC.acceptance.md), [acceptance dashboard](acceptance-dashboard.md), and [user review workbench](user-review-workbench.md). After EP-013 acceptance, the project should move to `active_execution_packet: none`, keep `project_state: accepted_baseline`, and start `EP-014-ACCEPTED-ARTIFACT-PROTECTION` as the next recommended package.
