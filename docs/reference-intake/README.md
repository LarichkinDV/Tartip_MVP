# Контур учета нормативно-справочных источников

## 1. Назначение

Контур reference intake фиксирует безопасный порядок поступления, учета и предварительной проверки нормативно-справочных источников для будущих этапов ТАРТИП.

Контур учета источников не создает нормативные правила и не подтверждает соответствие КСИ/ГЭСН/ФСНБ. Он только фиксирует поступление источника, его происхождение, версию, checksum, статус доверия и необходимость проверки.

## 2. Границы

Контур не импортирует реальные нормативные данные, не создает официальные записи КСИ/ГЭСН/ФСНБ и не активирует правила сопоставления.

Если официальный источник отсутствует, создается data requirement, structured question или review item. Нормативное правило не создается.

## 3. Основной workflow

```text
source file -> inbox -> manifest -> checksum -> authority/status -> review -> accepted reference source
```

Файл в `data/reference/inbox/` является только входным материалом. Он не считается evidence до регистрации в manifest, фиксации checksum, проверки authority/status и пользовательского решения.

## 4. Source-of-truth файлы

- `docs/reference-intake/source-intake-policy.md`;
- `docs/reference-intake/source-authority-model.md`;
- `docs/reference-intake/intake-workflow.md`;
- `data/reference/manifests/intake-manifest.schema.yml`;
- `data/reference/manifests/intake-log.yml`;
- `data/reference/manifests/source-authority-catalog.yml`.

## 5. Роль пользователя

Пользователь вручную принимает источник после проверки происхождения, версии, checksum и применимости. Codex не принимает источник от имени пользователя и не заполняет `accepted_by` или `accepted_at`.
