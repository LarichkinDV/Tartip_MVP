---
template_id: dissertation-bibliography-check
prompt_type: bibliography_check
status: template
---

# Dissertation Bibliography Check Prompt

Проверь, требуется ли новый источник для предлагаемого изменения.

Если источник нужен, создай proposal для `citation request`. Не меняй список литературы и не меняй сквозную нумерацию.

Результат:

```yaml
citation_request_needed: yes/no
reason:
candidate_source_description:
target_section:
bibliography_update_allowed: no
```
