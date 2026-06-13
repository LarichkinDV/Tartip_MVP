# Модель доверенности источников

## 1. Source origin

`source_origin` фиксирует происхождение источника:

- `official_public_source` — официальный публичный источник;
- `official_user_provided_file` — официальный файл, предоставленный пользователем;
- `project_dictionary` — внутренний проектный словарь;
- `user_decision` — пользовательское проектное решение;
- `llm_generated` — LLM-generated content;
- `forbidden` — запрещенный источник.

## 2. Source authority

`source_authority` фиксирует уровень доверия:

- `official` — может подтверждать официальные нормативно-справочные поля после review;
- `project_authorized` — применим только для project-only entities;
- `user_asserted` — пользовательское утверждение, не официальный нормативный источник;
- `draft` — предварительная запись без доверенного статуса;
- `forbidden` — запрещено использовать как evidence.

## 3. Trust status

Trust status возникает только после проверки происхождения, версии, checksum и пользовательского решения.

`accepted_by` и `accepted_at` являются user-owned fields. Codex не заполняет их.

## 4. Границы подтверждения

Только `official_public_source` и `official_user_provided_file` могут быть кандидатами на подтверждение official KSI/GESN/FSNB fields.

`project_dictionary`, `user_decision`, `llm_generated` и `forbidden` не подтверждают official KSI/GESN/FSNB fields.

## 5. requires_norm_review

`requires_norm_review` применяется, когда источник или запись требуют отдельной нормативной проверки перед дальнейшим использованием.
