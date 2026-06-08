# Language Policy

Пользовательские человекочитаемые артефакты Tartip должны быть на русском языке там, где это возможно. Это относится к README-разделам для пользователя, acceptance reports, dashboards, monthly defense documents, dissertation prompts, methodology notes, architecture notes, status reports, decision logs и человекочитаемым полям YAML/XML.

## Что можно оставлять на английском

- имена файлов и директорий;
- YAML/XML/JSON-ключи;
- enum-статусы;
- technical identifiers;
- API endpoints;
- классы, функции, переменные;
- команды терминала;
- названия библиотек, пакетов и стандартов;
- кодовые блоки;
- URL.

## Что не переводится механически

Codex не должен переводить технические идентификаторы, YAML/XML/JSON-ключи и enum-статусы ради русификации. Например, `WorkPackage`, `CalculationUnit`, `requires_review`, `accepted_by`, `docs/audit/audit-findings.yml` и `make audit` остаются без перевода.

## Как фиксируются нарушения

Если найден англоязычный пользовательский текст, `scripts/audit_language_policy.py` создает language audit finding с рекомендацией. EP-009 не выполняет массовую русификацию существующих документов.

Если обнаружена попытка перевести технический идентификатор или сломать YAML/XML/JSON-ключ, это считается critical finding `AUD-LANG-002`.

## Dissertation prompts

Prompts для диссертации должны быть на русском языке, кроме технических идентификаторов, путей, команд и имен файлов. Если перевод невозможен или нежелателен, нужно создать audit finding, а не менять текст автоматически.
