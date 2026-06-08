#!/usr/bin/env python3
from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path
from typing import Any

from reference_utils import load_data, write_yaml


PROJECT_ROOT = Path(__file__).resolve().parents[1]
VERIFICATION_PLAN_PATH = PROJECT_ROOT / "docs" / "grace" / "verification-plan.xml"
PROTOCOL_PATH = (
    PROJECT_ROOT
    / "docs"
    / "monthly"
    / "2026-06"
    / "03-test-protocol-reference-data-governance.md"
)
ACCEPTANCE_DASHBOARD_PATH = PROJECT_ROOT / "docs" / "acceptance-dashboard.yml"
REGISTRY_PATH = PROJECT_ROOT / "docs" / "artifact-registry.yml"
YAML_PATH = PROJECT_ROOT / "docs" / "verification-dashboard.yml"
MARKDOWN_PATH = PROJECT_ROOT / "docs" / "verification-dashboard.md"

ALLOWED_STATUSES = {
    "pending",
    "in_progress",
    "passed",
    "failed",
    "blocked",
    "requires_user_action",
    "not_applicable",
}
MANUAL_TYPES = {
    "manual_command",
    "manual_document_review",
    "manual_functional_review",
    "manual_normative_review",
    "manual_acceptance_review",
}


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(PROJECT_ROOT))
    except ValueError:
        return str(path)


def source_files() -> list[str]:
    return [
        "docs/grace/verification-plan.xml",
        "docs/monthly/2026-06/03-test-protocol-reference-data-governance.md",
        "docs/acceptance-dashboard.yml",
        "docs/artifact-registry.yml",
    ]


def read_existing_results() -> dict[str, dict[str, Any]]:
    if not YAML_PATH.exists():
        return {}
    data = load_data(YAML_PATH)
    dashboard = data.get("verification_dashboard", {}) if isinstance(data, dict) else {}
    checks = dashboard.get("checks", []) if isinstance(dashboard, dict) else []
    existing: dict[str, dict[str, Any]] = {}
    for check in checks if isinstance(checks, list) else []:
        if isinstance(check, dict) and check.get("check_id"):
            existing[str(check["check_id"])] = check
    return existing


def user_result(existing_check: dict[str, Any] | None) -> dict[str, Any]:
    existing = (
        existing_check.get("user_result", {})
        if existing_check and isinstance(existing_check.get("user_result"), dict)
        else {}
    )
    checked_by = existing.get("checked_by") or ""
    if checked_by == "Codex":
        checked_by = ""
    return {
        "checked": bool(existing.get("checked")) if checked_by else False,
        "checked_by": checked_by,
        "checked_at": existing.get("checked_at") or "",
        "result": existing.get("result") or "",
        "comments": existing.get("comments") or "",
    }


def make_steps(steps: list[str]) -> list[dict[str, str]]:
    return [{"step": step} for step in steps]


def make_results(results: list[str]) -> list[dict[str, str]]:
    return [{"result": result} for result in results]


def make_artifacts(paths: list[str]) -> list[dict[str, str]]:
    return [{"path": path} for path in paths]


def make_commands(commands: list[str]) -> list[dict[str, str]]:
    return [{"command": command} for command in commands]


def base_check(
    check_id: str,
    title: str,
    related_packet: str,
    related_requirement: str,
    related_acceptance_criterion: str,
    check_type: str,
    priority: str,
    how_to_check: list[str],
    expected_result: list[str],
    artifacts: list[str],
    commands: list[str] | None = None,
) -> dict[str, Any]:
    status = (
        "requires_user_action" if check_type == "manual_normative_review" else "pending"
    )
    return {
        "check_id": check_id,
        "title": title,
        "source_protocol": rel(PROTOCOL_PATH),
        "related_packet": related_packet,
        "related_requirement": related_requirement,
        "related_acceptance_criterion": related_acceptance_criterion,
        "check_type": check_type,
        "priority": priority,
        "status": status,
        "how_to_check": make_steps(how_to_check),
        "expected_result": make_results(expected_result),
        "artifacts": make_artifacts(artifacts),
        "commands": make_commands(commands or []),
        "user_result": {
            "checked": False,
            "checked_by": "",
            "checked_at": "",
            "result": "",
            "comments": "",
        },
    }


def required_checks() -> list[dict[str, Any]]:
    return [
        base_check(
            "VT-EP-004-001",
            "Проверить наличие docs/project-plan.md",
            "EP-004-PROJECT-PLANNING-AND-ACCEPTANCE",
            "REQ-008",
            "AC-EP-004-001",
            "manual_document_review",
            "high",
            [
                "Открыть docs/project-plan.md.",
                "Проверить, что файл существует и содержит текущий execution packet.",
            ],
            ["docs/project-plan.md существует и доступен для ручной проверки."],
            ["docs/project-plan.md"],
        ),
        base_check(
            "VT-EP-004-002",
            "Проверить наличие docs/artifact-registry.yml",
            "EP-004-PROJECT-PLANNING-AND-ACCEPTANCE",
            "REQ-010",
            "AC-EP-004-002",
            "manual_document_review",
            "high",
            [
                "Открыть docs/artifact-registry.yml.",
                "Проверить, что реестр содержит созданные артефакты.",
            ],
            ["docs/artifact-registry.yml существует и содержит artifact registry."],
            ["docs/artifact-registry.yml"],
        ),
        base_check(
            "VT-EP-004-003",
            "Проверить, что accepted_by не может быть Codex",
            "EP-004-PROJECT-PLANNING-AND-ACCEPTANCE",
            "REQ-008",
            "AC-EP-004-011",
            "manual_document_review",
            "high",
            [
                "Открыть scripts/validate_project_plan.py.",
                "Проверить наличие запрета accepted_by=Codex.",
            ],
            ["Валидация запрещает accepted_by=Codex."],
            ["scripts/validate_project_plan.py"],
        ),
        base_check(
            "VT-EP-004-004",
            "Проверить, что make validate-plan проходит",
            "EP-004-PROJECT-PLANNING-AND-ACCEPTANCE",
            "REQ-010",
            "AC-EP-004-010",
            "automated_command",
            "high",
            ["Запустить make validate-plan."],
            ["Команда завершается с кодом 0."],
            ["scripts/validate_project_plan.py"],
            ["make validate-plan"],
        ),
        base_check(
            "VT-EP-005-001",
            "Проверить генерацию acceptance dashboard",
            "EP-005-ACCEPTANCE-AND-USER-ACTION-DASHBOARDS",
            "REQ-009",
            "AC-EP-005-001",
            "automated_command",
            "high",
            ["Запустить make generate-acceptance-dashboard."],
            [
                "docs/acceptance-dashboard.md и docs/acceptance-dashboard.yml обновлены без accepted от Codex."
            ],
            ["docs/acceptance-dashboard.md", "docs/acceptance-dashboard.yml"],
            ["make generate-acceptance-dashboard"],
        ),
        base_check(
            "VT-EP-005-002",
            "Проверить генерацию user action dashboard",
            "EP-005-ACCEPTANCE-AND-USER-ACTION-DASHBOARDS",
            "REQ-008",
            "AC-EP-005-003",
            "automated_command",
            "high",
            ["Запустить make generate-user-action-dashboard."],
            [
                "docs/user-action-dashboard.md и docs/user-action-dashboard.yml обновлены без закрытия вопросов за пользователя."
            ],
            ["docs/user-action-dashboard.md", "docs/user-action-dashboard.yml"],
            ["make generate-user-action-dashboard"],
        ),
        base_check(
            "VT-EP-005-003",
            "Проверить, что accepted artifacts отображаются как protected",
            "EP-005-ACCEPTANCE-AND-USER-ACTION-DASHBOARDS",
            "REQ-008",
            "AC-EP-005-011",
            "manual_acceptance_review",
            "normal",
            [
                "Открыть docs/acceptance-dashboard.md.",
                "Проверить раздел защищенных принятых артефактов.",
            ],
            [
                "Accepted artifacts отображаются как protected или явно указано, что accepted artifacts отсутствуют."
            ],
            ["docs/acceptance-dashboard.md", "docs/acceptance-dashboard.yml"],
        ),
        base_check(
            "VT-EP-005-004",
            "Проверить, что open questions отображаются в user-action-dashboard",
            "EP-005-ACCEPTANCE-AND-USER-ACTION-DASHBOARDS",
            "REQ-005",
            "AC-EP-005-006",
            "manual_document_review",
            "high",
            [
                "Открыть docs/user-action-dashboard.md.",
                "Сверить open вопросы с data/questions/*.yml.",
            ],
            ["Все open/high priority вопросы видны в user action dashboard."],
            [
                "docs/user-action-dashboard.md",
                "data/questions/data-requirements.yml",
                "data/questions/normative-review-questions.yml",
            ],
        ),
        base_check(
            "VT-EP-006-001",
            "Проверить наличие monthly-plan.yml",
            "EP-006-MONTHLY-PLANNING-AND-DEFENSE",
            "REQ-010",
            "AC-EP-006-001",
            "manual_document_review",
            "normal",
            ["Открыть docs/monthly/monthly-plan.yml."],
            ["monthly-plan.yml существует и описывает блок 2026-06."],
            ["docs/monthly/monthly-plan.yml"],
        ),
        base_check(
            "VT-EP-006-002",
            "Проверить, что месячный блок содержит ровно 3 задачи",
            "EP-006-MONTHLY-PLANNING-AND-DEFENSE",
            "REQ-010",
            "AC-EP-006-002",
            "manual_document_review",
            "normal",
            [
                "Открыть docs/monthly/monthly-plan.yml.",
                "Посчитать задачи в monthly_plan.tasks.",
            ],
            ["В блоке 2026-06 указано ровно 3 задачи."],
            ["docs/monthly/monthly-plan.yml"],
        ),
        base_check(
            "VT-EP-006-003",
            "Проверить, что каждая задача имеет 15 человеко-часов",
            "EP-006-MONTHLY-PLANNING-AND-DEFENSE",
            "REQ-010",
            "AC-EP-006-003",
            "manual_document_review",
            "normal",
            [
                "Открыть docs/monthly/monthly-plan.yml.",
                "Проверить planned_hours у каждой задачи.",
            ],
            ["Каждая из 3 задач имеет planned_hours: 15."],
            ["docs/monthly/monthly-plan.yml"],
        ),
        base_check(
            "VT-EP-006-004",
            "Проверить наличие БФТ",
            "EP-006-MONTHLY-PLANNING-AND-DEFENSE",
            "REQ-010",
            "AC-EP-006-004",
            "manual_document_review",
            "normal",
            ["Открыть docs/monthly/2026-06/01-bft-reference-data-governance.md."],
            [
                "Документ БФТ существует и не содержит нормативных данных, придуманных Codex."
            ],
            ["docs/monthly/2026-06/01-bft-reference-data-governance.md"],
        ),
        base_check(
            "VT-EP-006-005",
            "Проверить наличие ТЗ",
            "EP-006-MONTHLY-PLANNING-AND-DEFENSE",
            "REQ-010",
            "AC-EP-006-005",
            "manual_document_review",
            "normal",
            [
                "Открыть docs/monthly/2026-06/02-technical-task-reference-data-governance.md."
            ],
            [
                "Документ ТЗ существует и фиксирует задачи проверки без изменения доменной методики."
            ],
            ["docs/monthly/2026-06/02-technical-task-reference-data-governance.md"],
        ),
        base_check(
            "VT-EP-006-006",
            "Проверить наличие протокола тестирования",
            "EP-006-MONTHLY-PLANNING-AND-DEFENSE",
            "REQ-010",
            "AC-EP-006-006",
            "manual_document_review",
            "normal",
            [
                "Открыть docs/monthly/2026-06/03-test-protocol-reference-data-governance.md."
            ],
            ["Протокол тестирования существует и связан с verification dashboard."],
            ["docs/monthly/2026-06/03-test-protocol-reference-data-governance.md"],
        ),
        base_check(
            "VT-EP-007-001",
            "Проверить наличие verification-dashboard.md",
            "EP-007-VERIFICATION-DASHBOARD",
            "REQ-010",
            "AC-EP-007-001",
            "manual_document_review",
            "high",
            ["Открыть docs/verification-dashboard.md."],
            ["verification-dashboard.md существует и содержит окно ручной проверки."],
            ["docs/verification-dashboard.md"],
        ),
        base_check(
            "VT-EP-007-002",
            "Проверить наличие verification-dashboard.yml",
            "EP-007-VERIFICATION-DASHBOARD",
            "REQ-010",
            "AC-EP-007-002",
            "manual_document_review",
            "high",
            ["Открыть docs/verification-dashboard.yml."],
            ["verification-dashboard.yml существует и содержит checks."],
            ["docs/verification-dashboard.yml"],
        ),
        base_check(
            "VT-EP-007-003",
            "Проверить, что manual checks не отмечены Codex как passed",
            "EP-007-VERIFICATION-DASHBOARD",
            "REQ-008",
            "AC-EP-007-006",
            "manual_document_review",
            "high",
            [
                "Открыть docs/verification-dashboard.yml.",
                "Проверить manual_* checks и user_result.",
            ],
            ["Manual checks не имеют checked_by: Codex и не закрыты Codex."],
            ["docs/verification-dashboard.yml"],
        ),
        base_check(
            "VT-EP-007-004",
            "Проверить, что checked_by не может быть Codex",
            "EP-007-VERIFICATION-DASHBOARD",
            "REQ-008",
            "AC-EP-007-007",
            "manual_document_review",
            "high",
            [
                "Открыть scripts/validate_verification_dashboard.py.",
                "Проверить запрет checked_by=Codex.",
            ],
            ["Валидатор запрещает checked_by=Codex."],
            ["scripts/validate_verification_dashboard.py"],
        ),
        base_check(
            "VT-EP-007-005",
            "Проверить, что verification dashboard связан с протоколом тестирования",
            "EP-007-VERIFICATION-DASHBOARD",
            "REQ-010",
            "AC-EP-007-010",
            "manual_document_review",
            "high",
            [
                "Открыть docs/monthly/2026-06/03-test-protocol-reference-data-governance.md.",
                "Проверить ссылки на docs/verification-dashboard.md и check_id.",
            ],
            [
                "Протокол тестирования содержит раздел про окно ручной проверки и check_id."
            ],
            [
                "docs/monthly/2026-06/03-test-protocol-reference-data-governance.md",
                "docs/verification-dashboard.md",
            ],
        ),
        base_check(
            "VT-EP-008-001",
            "Проверить наличие docs/dissertation/README.md",
            "EP-008-DISSERTATION-PROMPT-GENERATION",
            "REQ-011",
            "AC-EP-008-001",
            "manual_document_review",
            "high",
            ["Открыть docs/dissertation/README.md."],
            [
                "docs/dissertation/README.md существует и описывает dissertation sync workflow."
            ],
            ["docs/dissertation/README.md"],
        ),
        base_check(
            "VT-EP-008-002",
            "Проверить наличие forbidden-claims.yml",
            "EP-008-DISSERTATION-PROMPT-GENERATION",
            "REQ-011",
            "AC-EP-008-005",
            "manual_document_review",
            "high",
            ["Открыть docs/dissertation/prompt-profiles/forbidden-claims.yml."],
            [
                "forbidden-claims.yml содержит FC-001..FC-007 и запрет автоматического выбора ГЭСН по BIM-элементу."
            ],
            ["docs/dissertation/prompt-profiles/forbidden-claims.yml"],
        ),
        base_check(
            "VT-EP-008-003",
            "Проверить запрет docx_update prompt без accepted patch",
            "EP-008-DISSERTATION-PROMPT-GENERATION",
            "REQ-011",
            "AC-EP-008-009",
            "automated_command",
            "high",
            ["Запустить make validate-dissertation-prompts."],
            ["Валидатор запрещает docx_update prompt без accepted patch."],
            ["scripts/validate_dissertation_prompts.py"],
            ["make validate-dissertation-prompts"],
        ),
        base_check(
            "VT-EP-008-004",
            "Проверить, что prompts не содержат forbidden claims",
            "EP-008-DISSERTATION-PROMPT-GENERATION",
            "REQ-011",
            "AC-EP-008-009",
            "automated_command",
            "high",
            ["Запустить make validate-dissertation-prompts."],
            ["Валидатор запрещает generated prompts с forbidden claims."],
            [
                "scripts/validate_dissertation_prompts.py",
                "docs/dissertation/prompt-profiles/forbidden-claims.yml",
            ],
            ["make validate-dissertation-prompts"],
        ),
        base_check(
            "VT-EP-008-005",
            "Проверить, что Codex не создал DOCX",
            "EP-008-DISSERTATION-PROMPT-GENERATION",
            "REQ-011",
            "AC-EP-008-013",
            "automated_command",
            "high",
            ["Запустить make validate-dissertation-sync."],
            ["Валидатор не находит DOCX/PDF в thesis/."],
            ["scripts/validate_dissertation_sync.py", "thesis/.gitkeep"],
            ["make validate-dissertation-sync"],
        ),
        base_check(
            "VT-EP-008-006",
            "Проверить, что acceptance_decision остается pending",
            "EP-008-DISSERTATION-PROMPT-GENERATION",
            "REQ-008",
            "AC-EP-008-015",
            "manual_acceptance_review",
            "high",
            [
                "Открыть docs/acceptance/EP-008-DISSERTATION-PROMPT-GENERATION.acceptance.md.",
                "Проверить блок Решение пользователя.",
            ],
            ["acceptance_decision остается pending, accepted_by не заполнен Codex."],
            ["docs/acceptance/EP-008-DISSERTATION-PROMPT-GENERATION.acceptance.md"],
        ),
        base_check(
            "VT-EP-008-007",
            "Проверить защиту accepted/protected artifacts",
            "EP-008-DISSERTATION-PROMPT-GENERATION",
            "REQ-008",
            "AC-EP-008-016",
            "manual_acceptance_review",
            "normal",
            [
                "Открыть docs/acceptance-dashboard.md.",
                "Проверить раздел защищенных принятых артефактов.",
            ],
            [
                "Accepted/protected artifacts не изменены без user approval или явно указано, что таких артефактов нет."
            ],
            ["docs/acceptance-dashboard.md", "docs/artifact-registry.yml"],
        ),
        base_check(
            "VT-EP-009-001",
            "Проверить наличие audit contour",
            "EP-009-CODEX-SPEC-AUDIT",
            "REQ-012",
            "AC-EP-009-001",
            "automated_command",
            "high",
            ["Запустить make validate-audit."],
            ["Все обязательные audit-файлы существуют и валидны."],
            [
                "docs/audit/README.md",
                "docs/audit/codex-spec-audit.md",
                "docs/audit/codex-spec-audit.yml",
                "docs/audit/language-policy.md",
                "docs/audit/language-audit-report.md",
                "docs/audit/audit-findings.yml",
            ],
            ["make validate-audit"],
        ),
        base_check(
            "VT-EP-009-002",
            "Проверить Codex spec audit script",
            "EP-009-CODEX-SPEC-AUDIT",
            "REQ-012",
            "AC-EP-009-006",
            "automated_command",
            "high",
            ["Запустить make audit-codex-spec."],
            [
                "Скрипт проверяет domain, acceptance, protection, dashboards, verification, monthly и dissertation guardrails."
            ],
            ["scripts/audit_codex_spec.py", "docs/audit/codex-spec-audit.md"],
            ["make audit-codex-spec"],
        ),
        base_check(
            "VT-EP-009-003",
            "Проверить language audit script",
            "EP-009-CODEX-SPEC-AUDIT",
            "REQ-012",
            "AC-EP-009-007",
            "automated_command",
            "high",
            ["Запустить make audit-language."],
            [
                "Скрипт создает language findings и не падает на medium/low пользовательских англоязычных фрагментах."
            ],
            ["scripts/audit_language_policy.py", "docs/audit/language-audit-report.md"],
            ["make audit-language"],
        ),
        base_check(
            "VT-EP-009-004",
            "Проверить Language policy в AGENTS.md",
            "EP-009-CODEX-SPEC-AUDIT",
            "REQ-012",
            "AC-EP-009-009",
            "manual_document_review",
            "high",
            ["Открыть AGENTS.md и найти раздел Language policy."],
            [
                "AGENTS.md содержит Language policy с исключениями для technical identifiers."
            ],
            ["AGENTS.md"],
        ),
        base_check(
            "VT-EP-009-005",
            "Проверить Audit discipline в AGENTS.md",
            "EP-009-CODEX-SPEC-AUDIT",
            "REQ-012",
            "AC-EP-009-010",
            "manual_document_review",
            "high",
            ["Открыть AGENTS.md и найти раздел Audit discipline."],
            [
                "AGENTS.md содержит audit-first/read-mostly discipline и запрет mass rewrite."
            ],
            ["AGENTS.md"],
        ),
        base_check(
            "VT-EP-009-006",
            "Проверить запрет ModelElement -> GESNNorm в audit",
            "EP-009-CODEX-SPEC-AUDIT",
            "REQ-001",
            "AC-EP-009-011",
            "automated_command",
            "high",
            ["Запустить make audit-codex-spec."],
            [
                "Отсутствие forbidden edge ModelElement -> GESNNorm создает critical finding."
            ],
            ["scripts/audit_codex_spec.py", "docs/grace/knowledge-graph.xml"],
            ["make audit-codex-spec"],
        ),
        base_check(
            "VT-EP-009-007",
            "Проверить запрет Codex в user-owned fields",
            "EP-009-CODEX-SPEC-AUDIT",
            "REQ-008",
            "AC-EP-009-012",
            "automated_command",
            "high",
            ["Запустить make audit-codex-spec."],
            ["accepted_by, decided_by, checked_by и answered_by не могут быть Codex."],
            ["scripts/audit_codex_spec.py"],
            ["make audit-codex-spec"],
        ),
        base_check(
            "VT-EP-009-008",
            "Проверить preservation audit findings",
            "EP-009-CODEX-SPEC-AUDIT",
            "REQ-012",
            "AC-EP-009-017",
            "manual_document_review",
            "high",
            [
                "Открыть scripts/audit_codex_spec.py и scripts/audit_language_policy.py.",
                "Проверить, что merge_findings сохраняет status, resolution, resolved_by и resolved_at.",
            ],
            ["Audit scripts preserve existing user resolutions in audit-findings.yml."],
            [
                "scripts/audit_codex_spec.py",
                "scripts/audit_language_policy.py",
                "docs/audit/audit-findings.yml",
            ],
        ),
        base_check(
            "VT-EP-009-009",
            "Проверить, что language findings не блокируют make check",
            "EP-009-CODEX-SPEC-AUDIT",
            "REQ-012",
            "AC-EP-009-021",
            "automated_command",
            "high",
            ["Запустить make check."],
            [
                "Medium/low AUD-LANG-001 findings фиксируются, но не блокируют make check."
            ],
            ["Makefile", "scripts/audit_language_policy.py"],
            ["make check"],
        ),
        base_check(
            "VT-EP-009-010",
            "Проверить, что EP-009 не mass-rewrite packet",
            "EP-009-CODEX-SPEC-AUDIT",
            "REQ-012",
            "AC-EP-009-019",
            "manual_acceptance_review",
            "normal",
            [
                "Проверить git diff.",
                "Убедиться, что изменения ограничены audit contour, scripts, GRACE registration, dashboards, plans, README и CHANGELOG.",
            ],
            ["EP-009 не выполняет массовую русификацию существующих документов."],
            ["docs/audit/README.md", "docs/audit/language-audit-report.md"],
        ),
        base_check(
            "VT-EP-011-001",
            "Проверить Git workflow validator",
            "EP-011-GIT-WORKFLOW-DISCIPLINE",
            "REQ-013",
            "AC-EP-011-003",
            "automated_command",
            "high",
            ["Запустить make validate-git-workflow."],
            [
                "Advisory validator завершается с кодом 0 или фиксирует documented warning без Git mutations."
            ],
            ["scripts/validate_git_workflow.py", "Makefile"],
            ["make validate-git-workflow"],
        ),
        base_check(
            "VT-EP-011-002",
            "Проверить Git workflow discipline в AGENTS.md",
            "EP-011-GIT-WORKFLOW-DISCIPLINE",
            "REQ-013",
            "AC-EP-011-001",
            "manual_document_review",
            "high",
            ["Открыть AGENTS.md и найти раздел Git workflow discipline."],
            [
                "AGENTS.md описывает branch creation, dirty tree, merge gate и forbidden files."
            ],
            ["AGENTS.md"],
        ),
        base_check(
            "VT-EP-011-003",
            "Проверить branch naming policy",
            "EP-011-GIT-WORKFLOW-DISCIPLINE",
            "REQ-013",
            "AC-EP-011-004",
            "manual_document_review",
            "high",
            ["Открыть docs/git-workflow.md."],
            ["Документ фиксирует формат ep-<number>-<short-slug>."],
            ["docs/git-workflow.md"],
        ),
        base_check(
            "VT-EP-011-004",
            "Проверить merge policy",
            "EP-011-GIT-WORKFLOW-DISCIPLINE",
            "REQ-013",
            "AC-EP-011-005",
            "manual_document_review",
            "high",
            ["Открыть docs/git-workflow.md и AGENTS.md."],
            [
                "Merge в main разрешен только после accepted packet, make check, audit gate и explicit user approval."
            ],
            ["docs/git-workflow.md", "AGENTS.md"],
        ),
        base_check(
            "VT-EP-011-005",
            "Проверить запрет merge без acceptance",
            "EP-011-GIT-WORKFLOW-DISCIPLINE",
            "REQ-013",
            "AC-EP-011-006",
            "automated_command",
            "high",
            ["Запустить make audit-codex-spec."],
            ["Audit фиксирует merge forbidden, пока acceptance_decision не accepted."],
            ["scripts/audit_codex_spec.py", "docs/audit/audit-findings.yml"],
            ["make audit-codex-spec"],
        ),
        base_check(
            "VT-EP-011-006",
            "Проверить запрет accepted_by = Codex",
            "EP-011-GIT-WORKFLOW-DISCIPLINE",
            "REQ-013",
            "AC-EP-011-007",
            "automated_command",
            "high",
            ["Запустить make audit-codex-spec."],
            ["Audit и validator запрещают accepted_by = Codex."],
            ["scripts/audit_codex_spec.py", "scripts/validate_git_workflow.py"],
            ["make audit-codex-spec"],
        ),
        base_check(
            "VT-EP-011-007",
            "Проверить forbidden Git files",
            "EP-011-GIT-WORKFLOW-DISCIPLINE",
            "REQ-013",
            "AC-EP-011-008",
            "automated_command",
            "high",
            ["Запустить make validate-git-workflow."],
            [
                "Validator проверяет .env, .venv, node_modules, SQL/dump/backup files и реальные dissertation DOCX/PDF."
            ],
            ["scripts/validate_git_workflow.py"],
            ["make validate-git-workflow"],
        ),
        base_check(
            "VT-EP-011-008",
            "Проверить, что validator не выполняет Git mutations",
            "EP-011-GIT-WORKFLOW-DISCIPLINE",
            "REQ-013",
            "AC-EP-011-010",
            "manual_document_review",
            "high",
            ["Открыть scripts/validate_git_workflow.py."],
            [
                "Скрипт не вызывает git add, git commit, git merge, git push или удаление веток."
            ],
            ["scripts/validate_git_workflow.py"],
        ),
    ]


def protocol_check_ids() -> set[str]:
    if not PROTOCOL_PATH.exists():
        return set()
    return set(
        re.findall(r"\bVT-[A-Z0-9-]+\b", PROTOCOL_PATH.read_text(encoding="utf-8"))
    )


def read_verification_scenarios() -> dict[str, dict[str, str]]:
    if not VERIFICATION_PLAN_PATH.exists():
        return {}
    root = ET.parse(VERIFICATION_PLAN_PATH).getroot()
    scenarios: dict[str, dict[str, str]] = {}
    for scenario in root.findall("Scenario"):
        scenario_id = scenario.attrib.get("id", "")
        if not scenario_id:
            continue
        scenarios[scenario_id] = {
            "name": (scenario.findtext("Name") or "").strip(),
            "expected": (scenario.findtext("Expected") or "").strip(),
        }
    return scenarios


def apply_existing_results(checks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    existing = read_existing_results()
    result: list[dict[str, Any]] = []
    for check in checks:
        current = dict(check)
        existing_check = existing.get(str(check["check_id"]))
        current["user_result"] = user_result(existing_check)
        if existing_check and current["user_result"].get("checked"):
            existing_status = str(existing_check.get("status") or "")
            if existing_status in ALLOWED_STATUSES:
                current["status"] = existing_status
        result.append(current)
    return result


def missing_source_warnings() -> list[str]:
    warnings: list[str] = []
    for source in [
        VERIFICATION_PLAN_PATH,
        PROTOCOL_PATH,
        ACCEPTANCE_DASHBOARD_PATH,
        REGISTRY_PATH,
    ]:
        if not source.exists():
            warnings.append(f"Missing source: {rel(source)}")
    return warnings


def build_dashboard() -> dict[str, Any]:
    checks = apply_existing_results(required_checks())
    existing_ids = {check["check_id"] for check in checks}
    for check_id in sorted(protocol_check_ids() - existing_ids):
        checks.append(
            base_check(
                check_id,
                f"Проверка из monthly protocol: {check_id}",
                "EP-007-VERIFICATION-DASHBOARD",
                "REQ-010",
                "",
                "manual_document_review",
                "normal",
                [
                    "Найти check_id в monthly test protocol.",
                    "Выполнить описанные в протоколе шаги.",
                ],
                ["Проверка из протокола выполнена или зафиксирована пользователем."],
                [rel(PROTOCOL_PATH)],
            )
        )
    scenarios = read_verification_scenarios()
    summary = {status: 0 for status in ALLOWED_STATUSES}
    for check in checks:
        status = str(check.get("status") or "pending")
        summary[status if status in summary else "pending"] += 1
    ordered_summary = {
        "pending": summary["pending"],
        "in_progress": summary["in_progress"],
        "passed": summary["passed"],
        "failed": summary["failed"],
        "blocked": summary["blocked"],
        "requires_user_action": summary["requires_user_action"],
        "not_applicable": summary["not_applicable"],
    }
    return {
        "verification_dashboard": {
            "updated_at": date.today().isoformat(),
            "source_files": source_files(),
            "summary": ordered_summary,
            "warnings": missing_source_warnings(),
            "verification_scenarios_count": len(scenarios),
            "checks": checks,
        }
    }


def md(value: Any) -> str:
    return ("" if value is None else str(value)).replace("|", "\\|") or "-"


def first_text(items: list[dict[str, str]], key: str) -> str:
    values = [item.get(key, "") for item in items if item.get(key)]
    return "; ".join(values) if values else "-"


def artifacts_text(check: dict[str, Any]) -> str:
    artifacts = check.get("artifacts") or []
    paths = [artifact.get("path", "") for artifact in artifacts if artifact.get("path")]
    return ", ".join(paths) if paths else "-"


def commands_text(check: dict[str, Any]) -> str:
    commands = check.get("commands") or []
    values = [
        command.get("command", "") for command in commands if command.get("command")
    ]
    return ", ".join(values) if values else "-"


def checkbox(check: dict[str, Any]) -> str:
    user = (
        check.get("user_result") if isinstance(check.get("user_result"), dict) else {}
    )
    if user.get("result") == "passed":
        return "- [x] выполнено"
    if user.get("result") == "failed":
        return "- [!] не прошло"
    return "- [ ] не проверено"


def rows_or_empty(rows: list[str], columns: int) -> list[str]:
    return rows or ["| " + " | ".join(["-"] * columns) + " |"]


def write_markdown(dashboard: dict[str, Any]) -> None:
    data = dashboard["verification_dashboard"]
    checks = data["checks"]
    summary = data["summary"]
    lines = [
        "# Окно проверки работоспособности проекта Tartip",
        "",
        f"Дата обновления: {data['updated_at']}",
        "",
        "## 1. Сводка",
        "",
        "| Статус | Количество |",
        "|---|---:|",
    ]
    for key in [
        "pending",
        "in_progress",
        "passed",
        "failed",
        "blocked",
        "requires_user_action",
        "not_applicable",
    ]:
        lines.append(f"| {key} | {summary[key]} |")
    lines.extend(
        [
            "",
            "## 2. Проверки, ожидающие выполнения",
            "",
            "| Галочка | ID | Проверка | Как проверить | Ожидаемый результат | Артефакты | Статус |",
            "|---|---|---|---|---|---|---|",
        ]
    )
    pending_rows = []
    for check in checks:
        if check.get("status") in {"pending", "in_progress", "requires_user_action"}:
            pending_rows.append(
                f"| {checkbox(check)} | {md(check['check_id'])} | {md(check['title'])} | {md(first_text(check.get('how_to_check', []), 'step'))} | {md(first_text(check.get('expected_result', []), 'result'))} | {md(artifacts_text(check))} | {md(check.get('status'))} |"
            )
    lines.extend(rows_or_empty(pending_rows, 7))
    lines.extend(
        [
            "",
            "## 3. Автоматические проверки",
            "",
            "| ID | Проверка | Команда | Ожидаемый результат | Статус |",
            "|---|---|---|---|---|",
        ]
    )
    automated_rows = [
        f"| {md(check['check_id'])} | {md(check['title'])} | {md(commands_text(check))} | {md(first_text(check.get('expected_result', []), 'result'))} | {md(check.get('status'))} |"
        for check in checks
        if check.get("check_type") == "automated_command"
    ]
    lines.extend(rows_or_empty(automated_rows, 5))
    lines.extend(
        [
            "",
            "## 4. Ручные проверки документов",
            "",
            "| ID | Проверка | Документ | Что проверить | Статус |",
            "|---|---|---|---|---|",
        ]
    )
    document_rows = [
        f"| {md(check['check_id'])} | {md(check['title'])} | {md(artifacts_text(check))} | {md(first_text(check.get('how_to_check', []), 'step'))} | {md(check.get('status'))} |"
        for check in checks
        if check.get("check_type") == "manual_document_review"
    ]
    lines.extend(rows_or_empty(document_rows, 5))
    lines.extend(
        [
            "",
            "## 5. Ручные функциональные проверки",
            "",
            "| ID | Проверка | Как проверить | Ожидаемый результат | Статус |",
            "|---|---|---|---|---|",
        ]
    )
    functional_rows = [
        f"| {md(check['check_id'])} | {md(check['title'])} | {md(first_text(check.get('how_to_check', []), 'step'))} | {md(first_text(check.get('expected_result', []), 'result'))} | {md(check.get('status'))} |"
        for check in checks
        if check.get("check_type")
        in {"manual_functional_review", "manual_command", "manual_acceptance_review"}
    ]
    lines.extend(rows_or_empty(functional_rows, 5))
    lines.extend(
        [
            "",
            "## 6. Нормативные проверки",
            "",
            "| ID | Проверка | Что проверить | Требуемый источник | Статус |",
            "|---|---|---|---|---|",
        ]
    )
    normative_rows = [
        f"| {md(check['check_id'])} | {md(check['title'])} | {md(first_text(check.get('how_to_check', []), 'step'))} | {md(artifacts_text(check))} | {md(check.get('status'))} |"
        for check in checks
        if check.get("check_type") == "manual_normative_review"
    ]
    lines.extend(rows_or_empty(normative_rows, 5))
    lines.extend(
        [
            "",
            "## 7. Выполненные проверки",
            "",
            "| ID | Проверка | Проверил | Дата | Результат | Комментарий |",
            "|---|---|---|---|---|---|",
        ]
    )
    completed_rows = []
    for check in checks:
        user = (
            check.get("user_result")
            if isinstance(check.get("user_result"), dict)
            else {}
        )
        if user.get("checked"):
            completed_rows.append(
                f"| {md(check['check_id'])} | {md(check['title'])} | {md(user.get('checked_by'))} | {md(user.get('checked_at'))} | {md(user.get('result'))} | {md(user.get('comments'))} |"
            )
    lines.extend(rows_or_empty(completed_rows, 6))
    lines.extend(
        [
            "",
            "## 8. Не пройдено",
            "",
            "| ID | Проверка | Ошибка | Что требуется |",
            "|---|---|---|---|",
        ]
    )
    failed_rows = []
    for check in checks:
        user = (
            check.get("user_result")
            if isinstance(check.get("user_result"), dict)
            else {}
        )
        if check.get("status") == "failed" or user.get("result") == "failed":
            failed_rows.append(
                f"| {md(check['check_id'])} | {md(check['title'])} | {md(user.get('comments'))} | Re-run or fix source artifact |"
            )
    lines.extend(rows_or_empty(failed_rows, 4))
    lines.extend(
        [
            "",
            "## 9. Заблокировано",
            "",
            "| ID | Проверка | Причина блокировки | Что требуется |",
            "|---|---|---|---|",
        ]
    )
    blocked_rows = [
        f"| {md(check['check_id'])} | {md(check['title'])} | blocked | Provide missing source or unblock prerequisite |"
        for check in checks
        if check.get("status") == "blocked"
    ]
    lines.extend(rows_or_empty(blocked_rows, 4))
    lines.extend(
        [
            "",
            "## 10. Как отмечать проверку выполненной",
            "",
            "1. Найти проверку в `docs/verification-dashboard.yml`.",
            "2. Заполнить:",
            "   - `checked: true`;",
            "   - `checked_by: Дмитрий`;",
            "   - `checked_at: YYYY-MM-DD`;",
            "   - `result: passed` или `failed`;",
            "   - `comments`.",
            "3. Не указывать `Codex` в `checked_by`.",
            "4. После изменения запустить `make validate-verification`.",
            "",
            "Проверка работоспособности не равна приемке результата. Приемка остается в acceptance dashboard и acceptance reports.",
            "",
        ]
    )
    MARKDOWN_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    dashboard = build_dashboard()
    write_yaml(YAML_PATH, dashboard)
    write_markdown(dashboard)
    print("Verification dashboard generated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
