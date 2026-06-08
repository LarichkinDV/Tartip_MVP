# Decision Log

| ID | Decision | Status | Rationale | Related Requirements |
|---|---|---|---|---|
| DEC-001 | Отказ от прямой связи BIM-элемент -> ГЭСН. | active | BIM-элемент не равен строительной работе; прямое сопоставление запрещено knowledge graph. | REQ-001 |
| DEC-002 | КСИ используется как классификационный слой. | active | КСИ не выбирает ГЭСН напрямую и не является нормативным источником. | REQ-002 |
| DEC-003 | `CalculationUnit` является нормативно-расчетным шаблоном. | active | Не хранит фактические данные и не является универсальным контейнером. | REQ-003 |
| DEC-004 | Фактические данные привязываются к `WorkPackage` / захватке. | active | `ActualRecord` не должен быть привязан только к одиночному `ModelElement`. | REQ-004 |
| DEC-005 | `No source — no rule`. | active | Нормативные и классификационные данные требуют источника и версии. | REQ-005 |
| DEC-006 | GRACE-light используется как дисциплина агентской разработки. | active | Execution packets, module contracts and verification scenarios задают безопасный контур изменений. | REQ-009 |
| DEC-007 | Справочники КСИ/ФСНБ версионируются дельтово. | active | Неизмененные записи не должны дублироваться между релизами. | REQ-007 |
| DEC-008 | Пользователь является единственным acceptance owner. | active | Codex готовит результат к приемке, но не принимает его. | REQ-008 |
| DEC-009 | Codex может ставить только `ready_for_acceptance`, но не `accepted`. | active | `accepted`, `rejected`, `needs_revision` являются пользовательскими решениями. | REQ-008 |
| DEC-010 | Синхронизация с диссертацией идет через impact log, prompt и markdown patch. | active | Tartip не должен редактировать DOCX напрямую или переносить инженерные детали как научный результат без пользовательского решения. | REQ-011 |
| DEC-011 | EP-009 работает как audit-first/read-mostly packet. | active | Аудит должен сначала фиксировать findings, сохранять пользовательские статусы и не выполнять массовую русификацию или исправление accepted/protected artifacts без user approval. | REQ-012 |
| DEC-012 | Git workflow связывает ветку с execution packet и запрещает merge без user acceptance. | active | Codex может валидировать Git state и готовить инструкции, но не выполняет merge в main без accepted packet, passed checks и явного user approval. | REQ-013 |
