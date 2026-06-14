# Протокол проверки: Evidence-Gated Matching Workspace

## 1. Цель

Проверить, что EP-025 создает только draft workspace и validator, не активируя нормативное сопоставление.

## 2. Automated Checks

| Check | Command | Expected |
|---|---|---|
| Python syntax | `PYTHONPYCACHEPREFIX=/private/tmp/tartip-pycache python3 -m py_compile scripts/validate_matching_workspace.py` | exit 0 |
| Unit tests | `PYTHONPYCACHEPREFIX=/private/tmp/tartip-pycache .venv/bin/python -m pytest tests/test_validate_matching_workspace.py` | exit 0 |
| Scenario validator | `python3 scripts/validate_matching_workspace.py examples/vertical-scenarios/partition-brick-120-reinf.workspace.yml` | exit 0 |
| Full verify | `make verify` | exit 0 |
| Full check | `make check` | exit 0 |

## 3. Manual Checks

| Check | Status | checked_by | checked_at | result |
|---|---|---|---|---|
| Draft scenario contains no official classifier/normative values | pending_user_check |  |  | pending_user_check |
| WorkPackage sits between quantities, planning, and facts | pending_user_check |  |  | pending_user_check |
| User-owned fields are not filled by Codex | pending_user_check |  |  | pending_user_check |

## 4. Expected Result

Workspace remains `draft_requires_data`, `normative_status: not_active`, `activation_allowed: false`.
