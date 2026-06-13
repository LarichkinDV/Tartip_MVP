# Техническое задание на контур учета источников

## 1. Общие сведения

Настоящий документ определяет требования к контуру учета и проверки нормативно-справочных источников. Документ не является утверждением состава нормативной базы и не подтверждает соответствие конкретных КСИ/ГЭСН/ФСНБ записей.

Контур относится к подготовительному этапу и не реализует parser/import реальных источников.

## 2. Назначение контура

Контур должен фиксировать source file, manifest metadata, checksum, authority, status и review gate до дальнейшего использования источника.

## 3. Состав артефактов

В состав входят:

- `docs/reference-intake/README.md`;
- `docs/reference-intake/source-intake-policy.md`;
- `docs/reference-intake/source-authority-model.md`;
- `docs/reference-intake/intake-workflow.md`;
- `data/reference/manifests/intake-manifest.schema.yml`;
- `data/reference/manifests/intake-log.yml`;
- `data/reference/manifests/source-authority-catalog.yml`;
- `scripts/validate_reference_intake.py`;
- `tests/test_validate_reference_intake.py`.

## 4. Требования к manifest

Manifest должен содержать поля source identity, origin, authority, status, version, checksum, review state и user-owned acceptance fields.

`accepted_by` и `accepted_at` остаются пустыми до пользовательской проверки.

## 5. Требования к authority model

Только `official_public_source` и `official_user_provided_file` могут быть кандидатами на подтверждение official normative data после review.

`project_dictionary`, `user_decision`, `llm_generated` и `forbidden` не подтверждают official KSI/GESN/FSNB fields.

## 6. Требования к validator

Validator должен проверять:

- наличие reference-intake docs;
- наличие schema, intake log и authority catalog;
- уникальность `source_id`;
- checksum перед accepted status;
- запрет `accepted_by: Codex`;
- запрет official authority для `llm_generated`;
- запрет acceptance для forbidden sources;
- запрет official confirmation через `user_decision` или `project_dictionary`;
- отсутствие реальных файлов в inbox/raw до явного предоставления пользователем;
- отсутствие customer-specific patterns в manifests.

## 7. Ограничения

Запрещено создавать active matching, official KSI/GESN/FSNB records, normative units, resource composition или прямые BIM-КСИ-ГЭСН связи.

Запрещено включать dataset contribution или менять default-off data boundary.

## 8. Контроль

Контроль выполняется командами:

```sh
python3 scripts/validate_reference_intake.py
make verify
make check
```

Ручные решения по источникам заполняет пользователь.
