# Git Workflow Discipline

Этот документ фиксирует правила Git workflow для Tartip. Цель правил — не смешивать разные execution packets, не отправлять в Git запрещенные файлы и не готовить merge до пользовательской приемки.

## 1. Зачем нужны ветки

Ветка отделяет изменения одного execution packet от другого. Это делает review проще: пользователь видит, какие файлы относятся к конкретному пакету, какие проверки выполнены и какой acceptance report нужно открыть.

## 2. Когда создается новая ветка

Новая ветка нужна, если начинается новый execution packet и задача не read-only. Ветка также нужна, если меняются `AGENTS.md`, GRACE-файлы, `Makefile`, `scripts/*.py`, dashboards, `docs/artifact-registry.yml`, acceptance report, больше 3 файлов или потенциально accepted/protected artifacts.

## 3. Когда ветка не создается

Ветка не создается, если задача read-only, выполняются только проверки, текущая ветка уже соответствует execution packet или делается малая доработка в рамках текущей packet-ветки.

## 4. Как именуются ветки

Формат:

```text
ep-<number>-<short-slug>
```

Примеры:

- `ep-010-language-normalization`;
- `ep-011-git-workflow-discipline`;
- `ep-012-partition-rule-candidate`.

## 5. Когда можно готовить merge

Merge можно готовить только после пользовательской приемки:

- `acceptance_decision = accepted`;
- `accepted_by` заполнен;
- `accepted_by != Codex`;
- `make check` passed;
- `make validate-plan` passed;
- `make audit` passed, если audit доступен;
- нет critical/high audit findings;
- нет несогласованных изменений accepted/protected artifacts;
- пользователь явно разрешил merge.

Codex может подготовить инструкции, но не выполняет merge в `main` без явного разрешения пользователя.

## 6. Когда merge запрещен

Merge запрещен, если packet status остается `ready_for_acceptance`, `acceptance_decision = pending`, `acceptance_decision = needs_revision`, `accepted_by` пустой, `accepted_by = Codex`, `make check` fails, есть critical/high audit findings, есть несогласованные изменения accepted/protected artifacts или в staging есть запрещенные файлы.

## 7. Связь Git branches, execution packets и acceptance

Ветка должна соответствовать одному execution packet. Acceptance report фиксирует статус Codex и решение пользователя. `ready_for_acceptance` означает, что Codex подготовил пакет к проверке, но это не разрешение на merge. Только пользователь может поставить `accepted`.

## 8. Dirty working tree

Перед изменением файлов Codex выполняет:

```sh
git branch --show-current
git status --short
```

Если working tree содержит uncommitted changes от другого пакета, Codex не переключает ветку и не создает новую ветку без явного user approval. Вместо угадывания Codex должен зафиксировать warning или user-action item.

## 9. Что нельзя добавлять в Git

Запрещено добавлять:

- `.env`;
- `.venv/`;
- `node_modules/`;
- `*.dump`;
- `*.sql` как дампы;
- `*.backup`;
- `backups/*`;
- secrets;
- real proprietary normative datasets;
- `thesis/source/*.docx`;
- `thesis/versions/*.docx`;
- `thesis/exports/pdf/*.pdf`.

Исключения для реальных DOCX/PDF и proprietary normative datasets требуют явного user approval.

## 10. Mixed changes от разных EP

Если в одном working tree видны изменения разных execution packets, Codex не должен делать commit/merge. Нужно разделить изменения по пакетам вручную или получить явное user approval на совместную ветку.

## 11. Documented exception для текущего baseline

На момент создания `EP-011-GIT-WORKFLOW-DISCIPLINE` текущий working tree уже содержит pre-existing uncommitted changes от предыдущих пакетов на ветке `main`. Поэтому EP-011 не создает и не переключает ветку. Это exception действует только как audit/documentation note и не является разрешением на merge.
