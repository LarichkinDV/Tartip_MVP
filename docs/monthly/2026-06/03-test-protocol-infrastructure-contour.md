# Протокол испытаний инфраструктурного контура прикладного прототипа ТАРТИП

## 1. Общие сведения

Протокол фиксирует порядок проверки созданных инфраструктурных и документационных артефактов. Результаты ручной проверки заполняются пользователем. Codex не заполняет поля checked_by, checked_at, result: passed и не принимает результаты испытаний от имени пользователя.

## 2. Объект испытаний

Объект испытаний — инфраструктурный контур разработки, проверки, приемки и документационного сопровождения прикладного прототипа ТАРТИП за первый месяц.

## 3. Основание испытаний

Основанием являются:

- `docs/monthly/2026-06/monthly-plan.yml`;
- `docs/project-state.yml`;
- `docs/grace/execution-packets.xml`;
- `docs/grace/verification-plan.xml`;
- `docs/artifact-registry.yml`;
- acceptance reports принятых execution packets.

## 4. Состав проверяемых артефактов

- `docs/monthly/2026-06/01-business-functional-requirements.md`;
- `docs/monthly/2026-06/02-technical-specification.md`;
- `docs/monthly/2026-06/03-test-protocol-infrastructure-contour.md`;
- `docs/monthly/2026-06/presentation-outline.md`;
- `docs/acceptance/EP-023-MONTH-01-INFRASTRUCTURE-CUSTOMER-DOCUMENTS.acceptance.md`;
- generated dashboards/workbench после `make check`.

## 5. Условия проведения испытаний

Проверки выполняются в локальном репозитории `/Users/larichkindv/Tartip`.

Перед приемкой должны отсутствовать незадокументированные изменения protected/user-owned artifacts.

## 6. Команды проверки

```sh
wc -l docs/monthly/2026-06/01-business-functional-requirements.md
wc -l docs/monthly/2026-06/02-technical-specification.md
wc -l docs/monthly/2026-06/03-test-protocol-infrastructure-contour.md
FORBIDDEN_PATTERN='Sa''aS\|D''aaS\|free''mium\|bottom-up adop''tion\|open-''core\|commercial data lay''er'
grep -n "$FORBIDDEN_PATTERN" docs/monthly/2026-06/*.md || true
make verify
make check
```

## 7. Таблица испытаний

| ID | Проверка | Тип | Ожидаемый результат | User result |
|---|---|---|---|---|
| TP-EP-023-001 | БФТ создан и содержит границы первого месяца | automated/manual | файл существует, ограничения указаны | pending_user_check |
| TP-EP-023-002 | ТЗ создано и не заявляет промышленную эксплуатацию | automated/manual | файл существует, safe wording присутствует | pending_user_check |
| TP-EP-023-003 | Протокол испытаний создан | automated/manual | файл существует, manual fields user-owned | pending_user_check |
| TP-EP-023-004 | Presentation outline создан | manual | outline содержит 5-7 слайдов | pending_user_check |
| TP-EP-023-005 | Customer-facing документы не используют запрещенную рамку | automated | grep не находит запрещенные термины | pending_user_check |
| TP-EP-023-006 | `make verify` проходит | automated | команда завершается успешно | pending_user_check |
| TP-EP-023-007 | `make check` проходит | automated | команда завершается успешно | pending_user_check |

## 8. Минимальные проверки

- Файлы месячных документов существуют.
- Документы написаны как source artifacts, а не prompt templates.
- Документы описывают прикладной прототип и инфраструктурный контур.
- Документы не заявляют industrial-ready продукт.
- Документы не заявляют импорт реальных нормативных источников.
- Документы не используют реальные данные работодателя или Заказчика.

## 9. Проверка запретов

Должны сохраняться запреты:

- нет прямой связи `ModelElement -> GESNNorm`;
- нет прямого выбора `GESNNorm` через `KSIResultCode`;
- нет active matching rules без evidence;
- нет передачи данных Заказчика за пределы локального контура;
- нет DOCX/PDF без отдельной команды пользователя;
- нет заполнения user-owned fields Codex.

## 10. Итоговое заключение

Итоговое заключение заполняет пользователь после проверки документов и команд.

До пользовательского решения EP-023 остается в статусе `ready_for_acceptance`.

## 11. User-owned поля ручной проверки

```yaml
manual_verification:
  result: pending_user_check
  checked_by:
  checked_at:
  comments:
```
