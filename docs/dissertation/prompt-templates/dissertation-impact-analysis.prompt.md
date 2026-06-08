---
template_id: dissertation-impact-analysis
prompt_type: impact_analysis
status: template
---

# Dissertation Impact Analysis Prompt

Оцени, влияет ли execution packet Tartip на текст диссертации.

Используй:

- `docs/dissertation/dissertation-artifact-map.yml`;
- `docs/dissertation/prompt-profiles/dissertation-editor-profile.md`;
- `docs/dissertation/prompt-profiles/tartip-dissertation-alignment.md`;
- `docs/dissertation/prompt-profiles/forbidden-claims.yml`.

Верни результат строго в форме:

```yaml
dissertation_impact: yes/no
affected_sections:
impact_type:
reason:
recommended_action:
generated_prompt_needed: yes/no
```

Не предлагай DOCX update. Если влияние отсутствует, зафиксируй `dissertation_impact: no` и краткую причину.
