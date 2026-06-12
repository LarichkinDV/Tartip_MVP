# Project Plan

`docs/project-plan.md` is a human-readable summary. The machine-readable project state is [project-state.yml](project-state.yml), the artifact source of truth is [artifact-registry.yml](artifact-registry.yml), while packet definitions remain in [execution-packets.xml](grace/execution-packets.xml).

## 1. Project Goal

Create a local-first system for BIM5D cost-schedule matching that keeps BIM elements, KSI classification, calculation units, GESN candidates, work packages, schedule tasks, actual records, plan-fact comparison, and control decisions separated by explicit contracts and review gates.

## 2. Current Version

`0.1.0`

## 3. Project State

Current execution packet: `none`.

```yaml
project_state: accepted_baseline
active_execution_packet: none
last_accepted_execution_packet: EP-021-POST-ACCEPTANCE-SYNC-AUTOMATION
last_completed_execution_packet: EP-021-POST-ACCEPTANCE-SYNC-AUTOMATION
next_recommended_packet: EP-019-CODEX-CONTEXT-COMPACTION
```

## 4. Current Stage

The accepted baseline through EP-014 is closed by user decisions in `docs/acceptance/*.acceptance.md`. EP-014 synchronized the user-review decision CLI safety gap without repeating EP-012 and without changing accepted decisions EP-001 through EP-013.

EP-018 принят пользователем 2026-06-10 и синхронизирован в post-acceptance baseline. `CR-EP-010-README-CHANGELOG-LANGUAGE-NORMALIZATION` approved пользователем до старта EP-010. `EP-010-LANGUAGE-NORMALIZATION` принят пользователем 2026-06-10 после нормализации только пользовательских фрагментов README.md и CHANGELOG.md без изменения технических идентификаторов, команд, enum-статусов, кодовых блоков и предметной методики. `EP-015-VERIFICATION-DASHBOARD-RECONCILIATION` принят пользователем 2026-06-11 и синхронизирован в post-acceptance baseline. `EP-017-AUDIT-FINDINGS-CLEANUP` принят пользователем 2026-06-12 и синхронизирован в post-acceptance baseline; stale audit/workbench noise сокращен без удаления истории findings. `EP-021-POST-ACCEPTANCE-SYNC-AUTOMATION` принят пользователем 2026-06-12 и синхронизирован в post-acceptance baseline; sync automation остается инструментом для уже принятых пользователем пакетов и не принимает пакеты от имени Codex.

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
    - EP-010-LANGUAGE-NORMALIZATION
    - EP-011-GIT-WORKFLOW-DISCIPLINE
    - EP-012-USER-REVIEW-WORKBENCH-AND-ACCEPTANCE-STANDARD
    - EP-013-POST-ACCEPTANCE-STATE-SYNC
    - EP-014-USER-REVIEW-DECISION-CLI-SAFETY
    - EP-015-VERIFICATION-DASHBOARD-RECONCILIATION
    - EP-017-AUDIT-FINDINGS-CLEANUP
    - EP-018-ACCEPTED-ARTIFACT-PROTECTION
    - EP-021-POST-ACCEPTANCE-SYNC-AUTOMATION
```

EP-012 was the previous active packet before the acceptance queue was closed. EP-013 does not re-accept earlier packets; it only synchronizes state from user-owned acceptance reports.

## 5.1. Planning Decision

`EP-014-USER-REVIEW-DECISION-CLI-SAFETY` uses the next execution packet number because it is the current safety correction required before further user decision automation. The previously recommended `EP-014-ACCEPTED-ARTIFACT-PROTECTION` is moved to `EP-018-ACCEPTED-ARTIFACT-PROTECTION`, preserving the already planned follow-up order for `EP-015`, `EP-016`, and `EP-017`.

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
| Post-Acceptance State Sync | Accepted baseline synchronization, follow-up debt visibility, and validation | accepted | [EP-013 acceptance](acceptance/EP-013-POST-ACCEPTANCE-STATE-SYNC.acceptance.md), [post-acceptance validator](../scripts/validate_post_acceptance_state.py) |
| User Review Decision CLI Safety | Explicit dry-run/apply decision CLI, non-writing dry-run, atomic apply guardrails | accepted | [EP-014 acceptance](acceptance/EP-014-USER-REVIEW-DECISION-CLI-SAFETY.acceptance.md), [decision apply script](../scripts/apply_user_review_decisions.py) |
| Accepted Artifact Protection | Protected source/manual artifact classification, generated artifact metadata, and change request guardrails | accepted | [EP-018 acceptance](acceptance/EP-018-ACCEPTED-ARTIFACT-PROTECTION.acceptance.md), [protection validator](../scripts/validate_accepted_artifact_protection.py), [change requests](protected-artifact-change-requests.yml) |
| Language Normalization | Нормализация пользовательских фрагментов README.md и CHANGELOG.md по approved CR | accepted | [EP-010 acceptance](acceptance/EP-010-LANGUAGE-NORMALIZATION.acceptance.md), [README.md](../README.md), [CHANGELOG.md](../CHANGELOG.md) |
| Verification Dashboard Reconciliation | Machine-readable project state, monthly scope model, and read-only verification entrypoint | accepted | [project-state.yml](project-state.yml), [verification dashboard](verification-dashboard.md), [EP-015 acceptance](acceptance/EP-015-VERIFICATION-DASHBOARD-RECONCILIATION.acceptance.md) |
| Audit Findings Cleanup | Active/historical audit finding filtering, grouped stale findings, compact workbench/action windows | accepted | [audit findings](audit/audit-findings.yml), [user review workbench](user-review-workbench.md), [EP-017 acceptance](acceptance/EP-017-AUDIT-FINDINGS-CLEANUP.acceptance.md) |
| Post-Acceptance Sync Automation | Safe CLI automation for synchronizing already accepted packets without changing user-owned fields | accepted | [sync script](../scripts/sync_accepted_packet.py), [sync tests](../tests/test_sync_accepted_packet.py), [EP-021 acceptance](acceptance/EP-021-POST-ACCEPTANCE-SYNC-AUTOMATION.acceptance.md) |

## 7. Execution Packets

| Packet | Name | Status | Acceptance Report | Next Step |
|---|---|---|---|---|
| EP-001-INFRA | Prepare local infrastructure | accepted | [EP-001 report](acceptance/EP-001-INFRA.acceptance.md) | Protected artifact classification is deferred to EP-018. |
| EP-002-REFERENCE-GOVERNANCE | Reference data governance | accepted | [EP-002 report](acceptance/EP-002-REFERENCE-GOVERNANCE.acceptance.md) | Reference intake is deferred to EP-016. |
| EP-003-REFERENCE-VERSIONING | Delta-based reference versioning | accepted | [EP-003 report](acceptance/EP-003-REFERENCE-VERSIONING.acceptance.md) | Real source import waits for EP-016 and later parser work. |
| EP-004-PROJECT-PLANNING-AND-ACCEPTANCE | Project planning and acceptance contour | accepted | [EP-004 report](acceptance/EP-004-PROJECT-PLANNING-AND-ACCEPTANCE.acceptance.md) | Post-acceptance state is synchronized in EP-013. |
| EP-005-ACCEPTANCE-AND-USER-ACTION-DASHBOARDS | Acceptance and user action dashboards | accepted | [EP-005 report](acceptance/EP-005-ACCEPTANCE-AND-USER-ACTION-DASHBOARDS.acceptance.md) | Protection flags are deferred to EP-018. |
| EP-007-VERIFICATION-DASHBOARD | Verification dashboard | accepted | [EP-007 report](acceptance/EP-007-VERIFICATION-DASHBOARD.acceptance.md) | Pending verification checks remain post-acceptance verification debt. |
| EP-008-DISSERTATION-PROMPT-GENERATION | Dissertation prompt generation contour | accepted | [EP-008 report](acceptance/EP-008-DISSERTATION-PROMPT-GENERATION.acceptance.md) | DOCX/PDF updates still require explicit user request. |
| EP-009-CODEX-SPEC-AUDIT | Codex specification audit and language policy | accepted | [EP-009 report](acceptance/EP-009-CODEX-SPEC-AUDIT.acceptance.md) | Stale audit finding cleanup is deferred to EP-017. |
| EP-010-LANGUAGE-NORMALIZATION | Language normalization | accepted | [EP-010 report](acceptance/EP-010-LANGUAGE-NORMALIZATION.acceptance.md) | Completed; verification dashboard reconciliation is accepted in EP-015. |
| EP-011-GIT-WORKFLOW-DISCIPLINE | Git workflow discipline | accepted | [EP-011 report](acceptance/EP-011-GIT-WORKFLOW-DISCIPLINE.acceptance.md) | Merge still requires explicit user approval after checks. |
| EP-012-USER-REVIEW-WORKBENCH-AND-ACCEPTANCE-STANDARD | User review workbench and acceptance standard | accepted | [EP-012 report](acceptance/EP-012-USER-REVIEW-WORKBENCH-AND-ACCEPTANCE-STANDARD.acceptance.md) | Workbench remains the active review window. |
| EP-013-POST-ACCEPTANCE-STATE-SYNC | Post-acceptance state sync | accepted | [EP-013 report](acceptance/EP-013-POST-ACCEPTANCE-STATE-SYNC.acceptance.md) | Completed; EP-014 accepted after CLI safety review. |
| EP-014-USER-REVIEW-DECISION-CLI-SAFETY | User review decision CLI safety | accepted | [EP-014 report](acceptance/EP-014-USER-REVIEW-DECISION-CLI-SAFETY.acceptance.md) | Completed; next recommended packet is EP-018 accepted artifact protection. |
| EP-015-VERIFICATION-DASHBOARD-RECONCILIATION | Verification dashboard reconciliation | accepted | [EP-015 report](acceptance/EP-015-VERIFICATION-DASHBOARD-RECONCILIATION.acceptance.md) | Completed; next recommended packet is EP-017 audit findings cleanup. |
| EP-017-AUDIT-FINDINGS-CLEANUP | Audit findings cleanup | accepted | [EP-017 report](acceptance/EP-017-AUDIT-FINDINGS-CLEANUP.acceptance.md) | Completed; next recommended packet is EP-021 post-acceptance sync automation. |
| EP-018-ACCEPTED-ARTIFACT-PROTECTION | Accepted artifact protection | accepted | [EP-018 report](acceptance/EP-018-ACCEPTED-ARTIFACT-PROTECTION.acceptance.md) | Completed; EP-010 used the approved change request for README.md and CHANGELOG.md. |
| EP-021-POST-ACCEPTANCE-SYNC-AUTOMATION | Post-acceptance sync automation | accepted | [EP-021 report](acceptance/EP-021-POST-ACCEPTANCE-SYNC-AUTOMATION.acceptance.md) | Completed; next recommended packet is EP-019 context compaction. |

## 8. Status Values

Allowed packet statuses: `planned`, `in_progress`, `ready_for_acceptance`, `accepted`, `needs_revision`, `rejected`, `blocked`, `deprecated`.

Codex may prepare `ready_for_acceptance`; `accepted` statuses for EP-013, EP-014, EP-015, EP-017 and EP-021 are synchronization of existing user decisions from acceptance reports, not new Codex acceptance actions.

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
- [EP-010-LANGUAGE-NORMALIZATION.acceptance.md](acceptance/EP-010-LANGUAGE-NORMALIZATION.acceptance.md)
- [EP-011-GIT-WORKFLOW-DISCIPLINE.acceptance.md](acceptance/EP-011-GIT-WORKFLOW-DISCIPLINE.acceptance.md)
- [EP-012-USER-REVIEW-WORKBENCH-AND-ACCEPTANCE-STANDARD.acceptance.md](acceptance/EP-012-USER-REVIEW-WORKBENCH-AND-ACCEPTANCE-STANDARD.acceptance.md)
- [EP-013-POST-ACCEPTANCE-STATE-SYNC.acceptance.md](acceptance/EP-013-POST-ACCEPTANCE-STATE-SYNC.acceptance.md)
- [EP-014-USER-REVIEW-DECISION-CLI-SAFETY.acceptance.md](acceptance/EP-014-USER-REVIEW-DECISION-CLI-SAFETY.acceptance.md)
- [EP-015-VERIFICATION-DASHBOARD-RECONCILIATION.acceptance.md](acceptance/EP-015-VERIFICATION-DASHBOARD-RECONCILIATION.acceptance.md)
- [EP-017-AUDIT-FINDINGS-CLEANUP.acceptance.md](acceptance/EP-017-AUDIT-FINDINGS-CLEANUP.acceptance.md)
- [EP-018-ACCEPTED-ARTIFACT-PROTECTION.acceptance.md](acceptance/EP-018-ACCEPTED-ARTIFACT-PROTECTION.acceptance.md)
- [EP-021-POST-ACCEPTANCE-SYNC-AUTOMATION.acceptance.md](acceptance/EP-021-POST-ACCEPTANCE-SYNC-AUTOMATION.acceptance.md)

## 11. Follow-Up Roadmap

- `EP-016-REFERENCE-INTAKE-PREPARATION`: deferred until audit/workbench noise and Codex context costs are reduced.
- `EP-021-POST-ACCEPTANCE-SYNC-AUTOMATION`: accepted; post-acceptance sync automation is available for already accepted packets.
- `EP-019-CODEX-CONTEXT-COMPACTION`: next recommended packet.
- `EP-018-ACCEPTED-ARTIFACT-PROTECTION`: accepted; protected source/manual artifacts are classified, generated dashboards remain derived artifacts.

## 12. Open Follow-Up Debt

- `CR-EP-010-README-CHANGELOG-LANGUAGE-NORMALIZATION` approved пользователем 2026-06-10 и использован только для языковой нормализации README.md и CHANGELOG.md.
- Pending verification checks are post-acceptance verification debt and do not reopen already accepted acceptance reports.
- `EP-006-MONTHLY-PLANNING-AND-DEFENSE` is represented as monthly scope `MONTHLY-2026-06`, not as an accepted/current execution packet.
- High-priority reference and normative user actions remain open until official or project-authorized local sources are provided.
- Audit history remains open; EP-017 filters stale findings from active windows without closing findings as fixed.
- EP-019 is the next recommended packet after EP-021 post-acceptance sync automation acceptance.

## 13. Blockers

## 14. Risks

- EP-013 intentionally does not enable protection flags, close verification checks, close user actions, or change audit finding statuses.
- Real KSI/FSNB/GESN sources are still absent, so active normative matching rules remain prohibited by the `No source — no rule` policy.

## 15. Next Step

EP-021 синхронизирован как принятое post-acceptance состояние. Следующий рекомендуемый пакет: `EP-019-CODEX-CONTEXT-COMPACTION`.
