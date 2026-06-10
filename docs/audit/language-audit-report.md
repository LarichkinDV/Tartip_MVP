# Language Audit Report

Дата обновления: 2026-06-10

## 1. Что проверяется

- Markdown-файлы в `docs/`, `README.md` и `CHANGELOG.md`.
- Человекочитаемые поля YAML/XML: `title`, `description`, `notes`, `summary`, `question`, `recommendation`, `comments`, а также основные XML-теги GRACE.

## 2. Что не проверяется

- Кодовые блоки.
- Inline code.
- URL, пути файлов, команды, enum-статусы и технические идентификаторы.

## 3. Допустимые англоязычные исключения

- Имена файлов, директорий, классов, функций, переменных, API endpoints и библиотек.
- `YAML`, `XML`, `JSON` keys и enum values.
- Термины вроде `FastAPI`, `React`, `Vite`, `pytest`, `Docker`, `Codex`, `GRACE`.

## 4. Найденные англоязычные пользовательские фрагменты

| ID | Severity | File | Line | Issue |
|---|---|---|---:|---|
| AUD-LANG-001-0403b9742d | medium | docs/07-reference-data-policy.md | 29 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-0584b2a838 | medium | docs/07-reference-data-policy.md | 19 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-08e52774da | medium | docs/07-reference-data-policy.md | 21 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-0b144b99ab | medium | docs/acceptance/EP-003-REFERENCE-VERSIONING.acceptance.md | 23 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-0b2052d5df | medium | docs/acceptance/EP-002-REFERENCE-GOVERNANCE.acceptance.md | 16 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-0b243217e0 | medium | docs/07-reference-data-policy.md | 5 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-0ba615d854 | medium | docs/acceptance/EP-002-REFERENCE-GOVERNANCE.acceptance.md | 12 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-0ee5c2d891 | medium | docs/acceptance/EP-003-REFERENCE-VERSIONING.acceptance.md | 43 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-140fc5b5da | medium | docs/acceptance/EP-003-REFERENCE-VERSIONING.acceptance.md | 49 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-160edcdf15 | medium | docs/acceptance/EP-003-REFERENCE-VERSIONING.acceptance.md | 15 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-17931122a9 | medium | docs/acceptance/EP-001-INFRA.acceptance.md | 25 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-1993d93ded | medium | docs/acceptance/EP-003-REFERENCE-VERSIONING.acceptance.md | 61 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-1c2a65340e | medium | docs/acceptance/EP-003-REFERENCE-VERSIONING.acceptance.md | 22 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-1c6c2352c8 | medium | docs/acceptance/EP-002-REFERENCE-GOVERNANCE.acceptance.md | 45 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-1c9d128591 | medium | docs/acceptance/EP-001-INFRA.acceptance.md | 22 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-1ca0c9ad14 | medium | docs/acceptance/EP-001-INFRA.acceptance.md | 64 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-203660d971 | medium | docs/acceptance/EP-001-INFRA.acceptance.md | 46 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-237e9a0b6d | medium | docs/07-reference-data-policy.md | 28 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-2752cb38a8 | medium | docs/07-reference-data-policy.md | 86 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-284b1971ac | medium | docs/07-reference-data-policy.md | 87 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-2863e088cc | medium | docs/acceptance/EP-002-REFERENCE-GOVERNANCE.acceptance.md | 22 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-2b927a8c93 | medium | docs/acceptance/EP-001-INFRA.acceptance.md | 23 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-322d7641c0 | medium | docs/07-reference-data-policy.md | 66 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-391503f660 | medium | docs/07-reference-data-policy.md | 42 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-4066fb8d18 | medium | docs/07-reference-data-policy.md | 62 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-408cae52d8 | medium | docs/07-reference-data-policy.md | 74 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-4a895008f0 | medium | docs/acceptance/EP-002-REFERENCE-GOVERNANCE.acceptance.md | 38 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-4dc57e4b82 | medium | docs/07-reference-data-policy.md | 9 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-4e190036af | medium | docs/acceptance/EP-001-INFRA.acceptance.md | 47 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-539f295b1d | medium | docs/acceptance/EP-003-REFERENCE-VERSIONING.acceptance.md | 21 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-55388c287d | medium | docs/acceptance/EP-002-REFERENCE-GOVERNANCE.acceptance.md | 65 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-590d7770a6 | low | docs/acceptance/EP-004-PROJECT-PLANNING-AND-ACCEPTANCE.acceptance.md | 53 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-6529bcdc65 | medium | docs/acceptance/EP-003-REFERENCE-VERSIONING.acceptance.md | 54 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-65902480da | medium | docs/07-reference-data-policy.md | 7 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-662bc1efaa | medium | docs/acceptance/EP-004-PROJECT-PLANNING-AND-ACCEPTANCE.acceptance.md | 26 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-664f61b6bc | medium | docs/acceptance/EP-004-PROJECT-PLANNING-AND-ACCEPTANCE.acceptance.md | 29 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-696f7f1dec | medium | docs/acceptance/EP-003-REFERENCE-VERSIONING.acceptance.md | 37 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-72ded86315 | medium | docs/07-reference-data-policy.md | 44 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-76253fff5b | medium | docs/acceptance/EP-004-PROJECT-PLANNING-AND-ACCEPTANCE.acceptance.md | 62 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-84bd776410 | medium | docs/07-reference-data-policy.md | 17 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-85bb19af87 | medium | docs/acceptance/EP-002-REFERENCE-GOVERNANCE.acceptance.md | 41 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-85c871c337 | medium | docs/07-reference-data-policy.md | 82 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-88016cdc2a | medium | docs/acceptance/EP-003-REFERENCE-VERSIONING.acceptance.md | 38 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-891fe56c1e | medium | docs/acceptance/EP-003-REFERENCE-VERSIONING.acceptance.md | 39 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-9404737958 | medium | docs/07-reference-data-policy.md | 78 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-968c5d281c | medium | docs/acceptance/EP-003-REFERENCE-VERSIONING.acceptance.md | 12 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-96f06d57c4 | medium | docs/07-reference-data-policy.md | 90 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-9b0d0c9ced | medium | docs/07-reference-data-policy.md | 27 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-9f5e6b3e61 | medium | docs/acceptance/EP-001-INFRA.acceptance.md | 40 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-a000dddb0f | medium | docs/acceptance/EP-004-PROJECT-PLANNING-AND-ACCEPTANCE.acceptance.md | 17 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-a149677283 | medium | docs/07-reference-data-policy.md | 46 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-a58cccb460 | medium | docs/acceptance/EP-003-REFERENCE-VERSIONING.acceptance.md | 13 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-a61b931b31 | medium | docs/07-reference-data-policy.md | 11 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-a751af8091 | medium | docs/07-reference-data-policy.md | 38 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-a8fe4c398a | medium | docs/acceptance/EP-002-REFERENCE-GOVERNANCE.acceptance.md | 46 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-aad7f3cfe0 | medium | docs/acceptance/EP-004-PROJECT-PLANNING-AND-ACCEPTANCE.acceptance.md | 28 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-ad4f53f83b | medium | docs/07-reference-data-policy.md | 13 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-af6cd13752 | medium | docs/acceptance/EP-003-REFERENCE-VERSIONING.acceptance.md | 50 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-b25d5b3569 | medium | docs/07-reference-data-policy.md | 83 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-b43f7cd30a | medium | docs/07-reference-data-policy.md | 72 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-b54388e917 | medium | docs/acceptance/EP-004-PROJECT-PLANNING-AND-ACCEPTANCE.acceptance.md | 25 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-b5e844dc84 | medium | docs/07-reference-data-policy.md | 25 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-b80b176d2d | medium | docs/acceptance/EP-001-INFRA.acceptance.md | 15 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-b856004edd | medium | docs/07-reference-data-policy.md | 34 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-c2fc52453a | medium | docs/07-reference-data-policy.md | 58 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-c7e4c6a4d2 | medium | docs/acceptance/EP-002-REFERENCE-GOVERNANCE.acceptance.md | 23 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-c882327c71 | medium | docs/07-reference-data-policy.md | 40 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-cc0512c192 | medium | docs/07-reference-data-policy.md | 76 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-d3f78ad666 | medium | docs/07-reference-data-policy.md | 15 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-d4c4421471 | medium | docs/07-reference-data-policy.md | 64 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-d4dd8fec13 | medium | docs/07-reference-data-policy.md | 32 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-dcd6a88329 | medium | docs/07-reference-data-policy.md | 89 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-df602b0d72 | medium | docs/07-reference-data-policy.md | 70 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-e366604e83 | medium | docs/acceptance/EP-004-PROJECT-PLANNING-AND-ACCEPTANCE.acceptance.md | 27 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-f1060c8fb3 | medium | docs/acceptance/EP-002-REFERENCE-GOVERNANCE.acceptance.md | 13 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-f19dc9a207 | medium | docs/acceptance/EP-004-PROJECT-PLANNING-AND-ACCEPTANCE.acceptance.md | 24 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-f5f0484374 | medium | docs/acceptance/EP-003-REFERENCE-VERSIONING.acceptance.md | 24 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-f5f7163b46 | medium | docs/acceptance/EP-002-REFERENCE-GOVERNANCE.acceptance.md | 24 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-f7f501c85b | medium | docs/07-reference-data-policy.md | 88 | Найден вероятный англоязычный пользовательский фрагмент. |
| AUD-LANG-001-fde0672e17 | medium | docs/acceptance/EP-001-INFRA.acceptance.md | 42 | Найден вероятный англоязычный пользовательский фрагмент. |

## 5. Рекомендации

- Переводить пользовательский текст отдельными follow-up пакетами.
- Не переводить технические идентификаторы и ключи структурированных файлов.
- Сохранять пользовательские статусы findings.

## 6. Открытые language findings

- critical: 0
- high: 0
- medium: 79
- low: 1

## 7. Что не переводилось автоматически

- Existing README, CHANGELOG, dashboards, GRACE и dissertation документы не русифицировались массово.
- Скрипт только создает findings и рекомендации.

## 8. Почему технические идентификаторы не переводятся

Технические идентификаторы являются частью контрактов, путей, API, схем, enum-статусов и кода. Их механический перевод ломает совместимость и проверяемость проекта.
