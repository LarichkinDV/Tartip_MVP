# Changelog

## 0.1.0 - 2026-06-04

- Добавлен локальный инфраструктурный каркас `EP-001-INFRA`.
- Добавлен checklist проверок без Docker для локального окружения, где Docker недоступен.
- Добавлены артефакты `GRACE-light` для `execution packets`, `module contracts`, `verification scenarios` и `knowledge graph`.
- Добавлены backend и frontend skeletons с `FastAPI`, pytest, `Vite`, `React` и `TypeScript`.
- Добавлен каркас `reference governance` для `source manifests`, `import logs`, `question registries` и политики `No source — no rule`.
- Добавлен каркас `reference versioning` с описанными `delta schemas`, `canonical hashing`, `comparison utility` и `fake fixtures`.
- Добавлены `safety checks` и `backup scripts` для локальной гигиены проекта и сценариев `backup/restore` базы данных.
- Добавлен контур проектного планирования: `artifact registry`, `traceability matrix`, `decision log`, `status report` и `acceptance reports`.
- Добавлена дисциплина acceptance owner и `scripts/validate_project_plan.py` с `make validate-plan`.
- Добавлен `EP-005-ACCEPTANCE-AND-USER-ACTION-DASHBOARDS` для локальных `acceptance` и `user action dashboards`.
- Добавлены правила `accepted artifact protection`, генераторы dashboards, `make generate-dashboards` и проверки dashboards.
- Добавлен `EP-007-VERIFICATION-DASHBOARD` для локального отслеживания manual verification без web UI.
- Добавлены каркас `monthly test protocol`, `generator/validator` для `verification dashboard` и `make validate-verification`.
- Добавлен `EP-008-DISSERTATION-PROMPT-GENERATION` для учета влияния на диссертацию, `prompt generation`, `forbidden claim checks` и `DOCX update guardrails`.
- Добавлены `dissertation prompt profiles`, `prompt templates`, `prompt/patch queues` и `validation commands` без создания DOCX/PDF файлов диссертации.
- Добавлен `EP-009-CODEX-SPEC-AUDIT` для `audit-first` проверок спецификации Codex, `language policy`, `audit findings` и `audit report validation`.
- Добавлены `audit Makefile targets` и интеграция `user-action dashboard` для `audit findings` без массовой русификации существующих документов.
- Добавлен `EP-011-GIT-WORKFLOW-DISCIPLINE` для `branch naming`, контроля `dirty working tree`, `merge gates`, `forbidden Git files` и `advisory/strict Git workflow validation`.
- Подготовлен `EP-013-POST-ACCEPTANCE-STATE-SYNC` для синхронизации accepted baseline после цикла приемки.
- EP-001, EP-002, EP-003, EP-004, EP-005, EP-007, EP-008, EP-009, EP-011 и EP-012 отражены как post-acceptance baseline.
- Добавлены каркас `post-acceptance validation` и `follow-up roadmap` для `artifact protection`, `verification reconciliation`, `reference intake` и `audit cleanup`.
