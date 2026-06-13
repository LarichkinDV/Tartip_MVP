# Workflow учета источников

## 1. Последовательность

```text
source file -> inbox -> manifest -> checksum -> authority/status -> review -> accepted reference source
```

## 2. Поступление

Поступивший файл размещается в `data/reference/inbox/` только как входной материал. Наличие файла в inbox не делает его trusted evidence.

## 3. Manifest

Запись в `data/reference/manifests/intake-log.yml` фиксирует:

- `source_id`;
- `source_name`;
- `source_type`;
- `source_origin`;
- `source_authority`;
- `source_status`;
- `version_label`;
- `effective_date`;
- `received_at`;
- `file_path`;
- `checksum_sha256`;
- `checksum_status`;
- `review_status`;
- `review_required`;
- `accepted_by`;
- `accepted_at`;
- `notes`.

## 4. Review gate

Пользователь проверяет происхождение, версию, checksum, применимость и ограничения. Codex может подготовить structured question или data requirement, но не принимает источник.

## 5. Связь с будущими EP

Будущие пакеты могут добавить parser, import review, versioning или comparison workflow. EP-016 создает только подготовительный контур учета и проверки источников.

## 6. Запрет обхода

Если источник отсутствует или не прошел review, дальнейшее действие ограничивается data requirement, structured question или review item. Active matching не выполняется.
