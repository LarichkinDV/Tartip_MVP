# Audit Contour

`docs/audit/` хранит локальный контур аудита правил Codex для Tartip. Контур нужен, чтобы выявлять нарушения, фиксировать audit findings и показывать пользователю, какие решения требуют ручной проверки.

## Что проверяется

- доменные запреты BIM-КСИ-ГЭСН, включая запрет `ModelElement -> GESNNorm`;
- reference data discipline и принцип `No source — no rule`;
- запрет для Codex ставить `accepted`, `checked_by`, `answered_by`, `decided_by`;
- protection accepted artifacts;
- актуальность acceptance, user-action и verification dashboards;
- monthly defense layer;
- dissertation sync guardrails;
- языковая политика пользовательских артефактов.

## Команды

```sh
make audit-codex-spec
make audit-language
make validate-audit
make audit
```

`make audit-codex-spec` выполняет верхнеуровневый аудит правил проекта. `make audit-language` выполняет мягкий аудит языка. `make validate-audit` проверяет структуру отчетов и `audit-findings.yml`.

## Где смотреть findings

Основной машинно-читаемый файл:

```text
docs/audit/audit-findings.yml
```

Человекочитаемые отчеты:

```text
docs/audit/codex-spec-audit.md
docs/audit/language-audit-report.md
```

Открытые findings также выводятся в `docs/user-action-dashboard.md` после генерации dashboards.

## Critical finding

Critical finding означает нарушение, которое может сломать доменную модель, acceptance ownership, protection accepted artifacts, verification ownership или dissertation guardrails. Такие findings должны блокировать соответствующую audit-команду.

## Warning

Warning или medium/low finding фиксирует риск, который требует внимания, но не всегда должен останавливать локальную проверку. Medium/low language findings не блокируют `make check` на первом этапе.

## Как закрывать findings

Пользователь или последующий execution packet может изменить статус finding в `docs/audit/audit-findings.yml` на `acknowledged`, `fixed`, `accepted_risk`, `false_positive`, `blocked` или `requires_user_approval`. Codex не должен сбрасывать эти статусы в `open` при новом запуске аудита.

## Почему EP-009 не исправляет все автоматически

`EP-009-CODEX-SPEC-AUDIT` является audit-first / read-mostly packet. Его задача — создать механизм обнаружения нарушений и зафиксировать findings. Массовое переписывание документов, массовая русификация и исправление accepted/protected artifacts требуют отдельного пакета и решения пользователя.

## Accepted/protected artifacts

Accepted/protected artifacts нельзя удалять, переименовывать, переписывать или materially modify без user approval. Если аудит обнаруживает проблему в таком артефакте, он создает finding или `requires_user_approval` action, но не меняет artifact напрямую.
