# Протокол проверки: Data Contribution Safety Gates

## 1. Цель

Проверить, что EP-024 создает безопасный schema-first контур без включения передачи, telemetry, commercial use или AI training.

## 2. Automated Checks

| Check | Command | Expected |
|---|---|---|
| Python syntax | `PYTHONPYCACHEPREFIX=/private/tmp/tartip-pycache python3 -m py_compile scripts/validate_data_contribution.py` | exit 0 |
| Unit tests | `PYTHONPYCACHEPREFIX=/private/tmp/tartip-pycache .venv/bin/python -m pytest tests/test_validate_data_contribution.py` | exit 0 |
| Project validator | `python3 scripts/validate_data_contribution.py` | exit 0 |
| Full verify | `make verify` | exit 0 |
| Full check | `make check` | exit 0 |

## 3. Manual Checks

| Check | Status | checked_by | checked_at | result |
|---|---|---|---|---|
| Synthetic examples do not identify a real party | pending_user_check |  |  |  |
| User-owned approval fields are not filled by Codex | pending_user_check |  |  |  |
| Monthly documents do not claim runtime data collection | pending_user_check |  |  |  |

## 4. Expected Result

Все проверки подтверждают, что EP-024 остается documentation-first/schema-first и не изменяет BIM-КСИ-ГЭСН методику.
