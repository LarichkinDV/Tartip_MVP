#!/usr/bin/env python3
from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any

from reference_utils import load_data, write_yaml


PROJECT_ROOT = Path(__file__).resolve().parents[1]
QUESTION_FILES = [
    PROJECT_ROOT / "data" / "questions" / "data-requirements.yml",
    PROJECT_ROOT / "data" / "questions" / "unresolved-mapping-questions.yml",
    PROJECT_ROOT / "data" / "questions" / "normative-review-questions.yml",
    PROJECT_ROOT / "data" / "questions" / "project-decisions.yml",
    PROJECT_ROOT / "data" / "questions" / "import-issues.yml",
]
AUDIT_FINDINGS_PATH = PROJECT_ROOT / "docs" / "audit" / "audit-findings.yml"
YAML_PATH = PROJECT_ROOT / "docs" / "user-action-dashboard.yml"
MARKDOWN_PATH = PROJECT_ROOT / "docs" / "user-action-dashboard.md"


def rel(path: Path) -> str:
    return str(path.relative_to(PROJECT_ROOT))


def normalize_type(raw_type: Any, source_file: Path) -> str:
    text = str(raw_type or "").strip()
    if text:
        if text == "normative_review_question":
            return "normative_review"
        return text
    name = source_file.name
    if name == "data-requirements.yml":
        return "data_requirement"
    if name == "unresolved-mapping-questions.yml":
        return "mapping_question"
    if name == "normative-review-questions.yml":
        return "normative_review"
    if name == "project-decisions.yml":
        return "project_decision"
    if name == "import-issues.yml":
        return "import_issue"
    return "question"


def as_blocks(value: Any) -> list[dict[str, str]]:
    if value is None:
        return []
    if isinstance(value, list):
        return [{"item": str(item)} for item in value]
    return [{"item": str(value)}]


def audit_priority(severity: Any) -> str:
    severity_text = str(severity or "").strip()
    if severity_text in {"critical", "high"}:
        return "high"
    if severity_text == "medium":
        return "normal"
    return "low"


def read_actions() -> tuple[list[dict[str, Any]], list[str]]:
    actions: list[dict[str, Any]] = []
    warnings: list[str] = []
    for source_file in QUESTION_FILES:
        if not source_file.exists():
            warnings.append(f"Missing question source: {rel(source_file)}")
            continue
        data = load_data(source_file)
        questions = data.get("questions", []) if isinstance(data, dict) else []
        if not isinstance(questions, list):
            warnings.append(
                f"Question source has no questions list: {rel(source_file)}"
            )
            continue
        for question in questions:
            if not isinstance(question, dict):
                continue
            status = str(question.get("status") or "open")
            action_type = normalize_type(question.get("type"), source_file)
            requires_approval = action_type in {
                "requires_user_approval",
                "change_request",
            }
            actions.append(
                {
                    "id": question.get("id"),
                    "type": action_type,
                    "priority": question.get("priority", "normal"),
                    "status": status,
                    "topic": question.get("topic"),
                    "question": question.get("question"),
                    "expected_action": question.get("needed_for")
                    or question.get("expected_action"),
                    "expected_input": question.get("expected_input"),
                    "target_path": question.get("target_path"),
                    "blocks": as_blocks(question.get("blocks")),
                    "source_file": rel(source_file),
                    "owner": "Дмитрий"
                    if status in {"open", "pending"}
                    else question.get("owner"),
                    "requires_user_approval": requires_approval,
                    "response": {
                        "decision": question.get("resolution") or "",
                        "answered_by": question.get("answered_by") or "",
                        "answered_at": question.get("answered_at") or "",
                        "comment": question.get("comments") or "",
                    },
                }
            )
    if AUDIT_FINDINGS_PATH.exists():
        data = load_data(AUDIT_FINDINGS_PATH)
        findings = data.get("findings", []) if isinstance(data, dict) else []
        if not isinstance(findings, list):
            warnings.append(
                f"Audit findings source has no findings list: {rel(AUDIT_FINDINGS_PATH)}"
            )
        else:
            for item in findings:
                if not isinstance(item, dict):
                    continue
                status = str(item.get("status") or "open")
                action_type = (
                    "requires_user_approval"
                    if status == "requires_user_approval"
                    else "audit_finding"
                )
                actions.append(
                    {
                        "id": item.get("id"),
                        "type": action_type,
                        "priority": audit_priority(item.get("severity")),
                        "status": status,
                        "topic": item.get("category"),
                        "question": item.get("issue"),
                        "expected_action": "Review audit finding and decide next action.",
                        "expected_input": item.get("recommendation"),
                        "target_path": item.get("file"),
                        "blocks": []
                        if item.get("severity") not in {"critical", "high"}
                        else [{"item": item.get("check_id")}],
                        "source_file": rel(AUDIT_FINDINGS_PATH),
                        "owner": "Дмитрий"
                        if status
                        in {"open", "pending", "blocked", "requires_user_approval"}
                        else item.get("resolved_by"),
                        "requires_user_approval": status
                        == "requires_user_approval",
                        "response": {
                            "decision": item.get("resolution") or "",
                            "answered_by": item.get("resolved_by") or "",
                            "answered_at": item.get("resolved_at") or "",
                            "comment": "",
                        },
                    }
                )
    return actions, warnings


def build_dashboard() -> dict[str, Any]:
    actions, warnings = read_actions()
    summary = {
        "open": sum(action["status"] == "open" for action in actions),
        "high_priority": sum(action.get("priority") == "high" for action in actions),
        "blocked": sum(
            action["status"] == "blocked" or bool(action.get("blocks"))
            for action in actions
        ),
        "answered": sum(
            bool(action.get("response", {}).get("answered_by")) for action in actions
        ),
        "closed": sum(action["status"] in {"closed", "resolved"} for action in actions),
        "requires_user_approval": sum(
            action.get("requires_user_approval") for action in actions
        ),
    }
    return {
        "user_action_dashboard": {
            "updated_at": date.today().isoformat(),
            "source_files": [rel(path) for path in QUESTION_FILES]
            + ([rel(AUDIT_FINDINGS_PATH)] if AUDIT_FINDINGS_PATH.exists() else []),
            "summary": summary,
            "warnings": warnings,
            "actions": actions,
        }
    }


def md(value: Any) -> str:
    return ("" if value is None else str(value)).replace("|", "\\|") or "-"


def block_text(action: dict[str, Any]) -> str:
    blocks = action.get("blocks") or []
    return (
        "; ".join(block.get("item", "") for block in blocks if block.get("item")) or "-"
    )


def rows_or_empty(rows: list[str], columns: int) -> list[str]:
    return rows or ["| " + " | ".join(["-"] * columns) + " |"]


def write_markdown(dashboard: dict[str, Any]) -> None:
    data = dashboard["user_action_dashboard"]
    actions = data["actions"]
    summary = data["summary"]
    lines = [
        "# Вопросы и действия для пользователя",
        "",
        f"Дата обновления: {data['updated_at']}",
        "",
        "## 1. Сводка",
        "",
        "| Категория | Количество |",
        "|---|---:|",
    ]
    for key in [
        "open",
        "high_priority",
        "blocked",
        "answered",
        "closed",
        "requires_user_approval",
    ]:
        lines.append(f"| {key} | {summary[key]} |")
    lines.extend(
        [
            "",
            "## 2. Срочные вопросы",
            "",
            "| ID | Тип | Приоритет | Вопрос | Что требуется | Блокирует |",
            "|---|---|---|---|---|---|",
        ]
    )
    urgent = [
        action
        for action in actions
        if action.get("priority") == "high"
        and action.get("status") in {"open", "pending", "blocked"}
    ]
    lines.extend(
        rows_or_empty(
            [
                f"| {md(action['id'])} | {md(action['type'])} | {md(action['priority'])} | {md(action['question'])} | {md(action['expected_input'])} | {md(block_text(action))} |"
                for action in urgent
            ],
            6,
        )
    )
    lines.extend(
        [
            "",
            "## 3. Требуют согласования пользователя",
            "",
            "| ID | Вопрос | Причина | Затрагиваемые принятые артефакты | Что требуется |",
            "|---|---|---|---|---|",
        ]
    )
    approval = [action for action in actions if action.get("requires_user_approval")]
    lines.extend(
        rows_or_empty(
            [
                f"| {md(action['id'])} | {md(action['question'])} | {md(action['topic'])} | {md(action['target_path'])} | User approval |"
                for action in approval
            ],
            5,
        )
    )
    sections = [
        (
            "## 4. Требования к данным",
            "data_requirement",
            "| ID | Вопрос | Ожидаемый файл / действие | Куда положить | Блокирует |",
            5,
        ),
        (
            "## 5. Вопросы сопоставления",
            "mapping_question",
            "| ID | Вопрос | Что нужно решить | Блокирует |",
            4,
        ),
        (
            "## 6. Нормативные проверки",
            "normative_review",
            "| ID | Вопрос | Что проверить | Источник / файл | Блокирует |",
            5,
        ),
        (
            "## 7. Проектные решения",
            "project_decision",
            "| ID | Вопрос | Варианты решения | Рекомендуемое действие |",
            4,
        ),
        (
            "## 8. Ошибки импорта",
            "import_issue",
            "| ID | Проблема | Что нужно сделать | Файл |",
            4,
        ),
        (
            "## 9. Audit findings",
            "audit_finding",
            "| ID | Finding | Recommendation | File |",
            4,
        ),
        (
            "## 10. Audit findings требуют согласования",
            "requires_user_approval",
            "| ID | Finding | Recommendation | File |",
            4,
        ),
    ]
    for title, action_type, header, columns in sections:
        lines.extend(["", title, "", header, "|" + "---|" * columns])
        typed = [action for action in actions if action.get("type") == action_type]
        if action_type == "data_requirement":
            rows = [
                f"| {md(a['id'])} | {md(a['question'])} | {md(a['expected_input'])} | {md(a['target_path'])} | {md(block_text(a))} |"
                for a in typed
            ]
        elif action_type == "normative_review":
            rows = [
                f"| {md(a['id'])} | {md(a['question'])} | {md(a['expected_input'])} | {md(a['target_path'])} | {md(block_text(a))} |"
                for a in typed
            ]
        elif action_type == "import_issue":
            rows = [
                f"| {md(a['id'])} | {md(a['question'])} | {md(a['expected_input'])} | {md(a['target_path'])} |"
                for a in typed
            ]
        elif action_type in {"audit_finding", "requires_user_approval"}:
            rows = [
                f"| {md(a['id'])} | {md(a['question'])} | {md(a['expected_input'])} | {md(a['target_path'])} |"
                for a in typed
            ]
        else:
            rows = [
                f"| {md(a['id'])} | {md(a['question'])} | {md(a['expected_input'])} | {md(a['expected_action'])} |"
                for a in typed
            ]
        lines.extend(rows_or_empty(rows, columns))
    closed = [
        action for action in actions if action.get("status") in {"closed", "resolved"}
    ]
    lines.extend(
        [
            "",
            "## 11. Закрытые вопросы",
            "",
            "| ID | Решение | Дата | Кем принято |",
            "|---|---|---|---|",
        ]
    )
    lines.extend(
        rows_or_empty(
            [
                f"| {md(a['id'])} | {md(a['response'].get('decision'))} | {md(a['response'].get('answered_at'))} | {md(a['response'].get('answered_by'))} |"
                for a in closed
            ],
            4,
        )
    )
    lines.append("")
    MARKDOWN_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    dashboard = build_dashboard()
    write_yaml(YAML_PATH, dashboard)
    write_markdown(dashboard)
    print("User action dashboard generated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
