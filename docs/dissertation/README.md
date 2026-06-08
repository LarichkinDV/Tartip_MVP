# Dissertation Synchronization

Этот каталог хранит контролируемый контур синхронизации проекта Tartip с текстом диссертации.

Контур нужен для того, чтобы изменения в Tartip не переписывали диссертацию автоматически. Любое изменение проходит через оценку влияния, prompt, markdown patch, пользовательскую приемку и только затем может попасть в DOCX по отдельному явному запросу.

## Принцип

Рабочая цепочка:

1. Tartip execution packet.
2. Dissertation impact analysis.
3. Запись в `dissertation-impact-log.yml`.
4. Запись в `section-update-queue.yml`.
5. Prompt в `prompt-queue/pending/`.
6. Проверка prompt пользователем.
7. Markdown patch в `patches/pending/`.
8. Пользовательская приемка patch.
9. DOCX update только по явному запросу пользователя.
10. Render/visual check после DOCX update.

## Почему DOCX не редактируется напрямую

DOCX является финальным пользовательским артефактом. Codex не должен редактировать его напрямую, создавать новую DOCX-версию, менять библиографическую нумерацию или переносить инженерные детали Tartip в научный текст без отдельного решения пользователя.

На этом этапе создаются только prompts, markdown patches и контрольные YAML/Markdown файлы.

## Где что хранится

- `prompt-profiles/`: профиль диссертационного редактора, alignment rules и forbidden claims.
- `prompt-templates/`: шаблоны prompt для анализа влияния, обновления разделов, терминологии, библиографии и DOCX update.
- `prompt-queue/pending/`: prompts, ожидающие проверки пользователя.
- `prompt-queue/accepted/`: prompts, принятые пользователем.
- `prompt-queue/rejected/`: отклоненные prompts.
- `patches/pending/`: markdown patches, ожидающие приемки.
- `patches/accepted/`: markdown patches, принятые пользователем.
- `patches/rejected/`: отклоненные markdown patches.
- `acceptance/`: локальные отчеты по диссертационным обновлениям.
- `notes/`: рабочие заметки без статуса научного источника.

## Защита accepted artifacts

Принятые артефакты защищены. Если изменение Tartip требует изменить accepted artifact, Codex должен создать proposed change request или `requires_user_approval` item, а не редактировать артефакт напрямую.

Codex не может ставить `accepted`, `accepted_by: Codex` или закрывать пользовательские решения.
