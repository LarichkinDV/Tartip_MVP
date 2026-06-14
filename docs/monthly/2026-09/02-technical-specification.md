# ТЗ: Evidence-Gated Matching Workspace

## 1. Scope

EP-025 создает YAML-схемы, draft scenario, validator и regression tests. Это schema-first / documentation-first контур.

## 2. Source Artifacts

- `docs/matching-workspace/README.md`;
- `docs/matching-workspace/evidence-gated-workflow.md`;
- `schemas/domain/*.schema.yml`;
- `examples/vertical-scenarios/partition-brick-120-reinf.workspace.yml`;
- `scripts/validate_matching_workspace.py`;
- `tests/test_validate_matching_workspace.py`.

## 3. Validation Rules

Validator должен блокировать:

- activation при missing evidence;
- active workspace status;
- official-looking codes without accepted source review;
- `source_origin: llm_generated` as evidence;
- `source_authority: forbidden` as evidence;
- user decision as confirmation for official fields;
- fact record without WorkPackage context;
- schedule task without WorkPackage context;
- calculation unit candidate storing fact context.

## 4. Allowed Result

Единственный допустимый результат EP-025 — `draft_requires_data` workspace with `activation_allowed: false`.

## 5. Exclusions

Не создаются API, backend services, UI, migrations, real reference import, active rules or production configuration.
