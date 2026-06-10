#!/usr/bin/env python3
from __future__ import annotations

import hashlib
from datetime import date
from pathlib import Path
from typing import Any

from reference_utils import load_data, write_yaml


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ACCEPTANCE_DASHBOARD_PATH = PROJECT_ROOT / "docs" / "acceptance-dashboard.yml"
VERIFICATION_DASHBOARD_PATH = PROJECT_ROOT / "docs" / "verification-dashboard.yml"
USER_ACTION_DASHBOARD_PATH = PROJECT_ROOT / "docs" / "user-action-dashboard.yml"
AUDIT_FINDINGS_PATH = PROJECT_ROOT / "docs" / "audit" / "audit-findings.yml"
ARTIFACT_REGISTRY_PATH = PROJECT_ROOT / "docs" / "artifact-registry.yml"
STATUS_REPORT_PATH = PROJECT_ROOT / "docs" / "status-report.md"
PACKETS_PATH = PROJECT_ROOT / "docs" / "grace" / "execution-packets.xml"
YAML_PATH = PROJECT_ROOT / "docs" / "user-review-workbench.yml"
MARKDOWN_PATH = PROJECT_ROOT / "docs" / "user-review-workbench.md"
PROTECTION_PACKET = "EP-018-ACCEPTED-ARTIFACT-PROTECTION"

SOURCE_PATHS = [
    ACCEPTANCE_DASHBOARD_PATH,
    VERIFICATION_DASHBOARD_PATH,
    USER_ACTION_DASHBOARD_PATH,
    AUDIT_FINDINGS_PATH,
    ARTIFACT_REGISTRY_PATH,
    STATUS_REPORT_PATH,
    PACKETS_PATH,
]

ACTIVE_ACCEPTANCE_STATUSES = {
    "ready_for_acceptance",
    "needs_revision",
    "blocked",
}
ACTIVE_ACTION_STATUSES = {"open", "pending", "blocked", "requires_user_approval"}
ACTIVE_CHECK_STATUSES = {"pending", "in_progress", "blocked", "requires_user_action"}
PSEUDO_EMPTY_VALUES = {
    "отсутствуют",
    "нет",
    "блокеров нет",
    "рисков нет",
    "none",
    "no blockers",
    "no risks",
}
PRIORITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(PROJECT_ROOT))
    except ValueError:
        return str(path)


def checksum(path: Path) -> str:
    if not path.exists():
        return ""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_dashboard(path: Path, root_key: str) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = load_data(path)
    if not isinstance(data, dict):
        return {}
    value = data.get(root_key, {})
    return value if isinstance(value, dict) else {}


def as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def md(value: Any) -> str:
    return ("" if value is None else str(value)).replace("|", "\\|") or "-"


def source_file_entry(path: Path) -> dict[str, Any]:
    exists = path.exists()
    return {
        "path": rel(path),
        "checksum_sha256": checksum(path) if exists else "",
        "status": "present" if exists else "missing",
        "warning": "" if exists else f"Source file is missing: {rel(path)}",
    }


def source_file_warning(path: Path) -> dict[str, str]:
    return {
        "id": f"WRK-SOURCE-MISSING-{rel(path).replace('/', '-').upper()}",
        "severity": "high",
        "text": f"Source file is missing: {rel(path)}",
        "source_file": rel(path),
    }


def pseudo_text(value: Any) -> bool:
    text = str(value or "").strip().strip(".:;!-—").lower()
    return text in PSEUDO_EMPTY_VALUES


def pseudo_warnings(
    item_id: str, source_file: str, values: list[dict[str, Any]], section: str
) -> list[dict[str, str]]:
    warnings: list[dict[str, str]] = []
    for value in values:
        text = value.get("text") if isinstance(value, dict) else value
        if pseudo_text(text):
            warnings.append(
                {
                    "id": f"WRK-PSEUDO-{section.upper()}-{item_id}",
                    "severity": "high",
                    "text": f"Pseudo {section} value found: {text}",
                    "source_file": source_file,
                }
            )
    return warnings


def priority(value: Any, default: str = "medium") -> str:
    raw = str(value or default).strip()
    if raw in {"critical", "high", "medium", "low"}:
        return raw
    if raw in {"normal", "средний"}:
        return "medium"
    return default


def command_list(values: Any) -> list[dict[str, str]]:
    commands: list[dict[str, str]] = []
    for item in as_list(values):
        if not isinstance(item, dict):
            continue
        command = item.get("command")
        if command:
            commands.append(
                {"command": str(command), "status": str(item.get("status") or "")}
            )
    return commands


def artifact_list(values: Any) -> list[dict[str, str]]:
    artifacts: list[dict[str, str]] = []
    for item in as_list(values):
        if isinstance(item, dict) and item.get("path"):
            artifacts.append({"path": str(item["path"])})
    return artifacts


def block_list(values: Any) -> list[dict[str, str]]:
    result: list[dict[str, str]] = []
    for index, item in enumerate(as_list(values), start=1):
        if isinstance(item, dict):
            text = item.get("text") or item.get("item") or ""
            item_id = item.get("id") or f"BLOCK-{index:03d}"
        else:
            text = str(item)
            item_id = f"BLOCK-{index:03d}"
        if text:
            result.append({"id": str(item_id), "text": russian_block_text(str(text))})
    return result


def russian_block_text(text: str) -> str:
    replacements = {
        "active matching rules that require this reference source type": "активацию правил сопоставления, которым нужен этот тип справочного источника",
        "rule activation": "активацию правила",
    }
    return replacements.get(text, text)


def russian_user_action_title(action: dict[str, Any]) -> str:
    action_id = str(action.get("id") or "")
    titles = {
        "DR-REF-FSNB-001": "Требуется локальный официальный или проектно разрешенный источник ФСНБ",
        "DR-REF-KSI-001": "Требуется локальный официальный или проектно разрешенный источник КСИ",
        "DR-REF-WORK-TYPES-001": "Требуется локальный официальный или проектно разрешенный источник видов работ",
        "NR-RULE-PARTITION-BRICK-120-REINF-001": "Требуются официальные evidence references для правила сопоставления",
    }
    return titles.get(action_id, str(action.get("topic") or action_id))


def russian_required_user_action(action: dict[str, Any]) -> str:
    action_id = str(action.get("id") or "")
    actions = {
        "DR-REF-FSNB-001": "Поместить файл источника в `data/reference/inbox/fsnb/` и указать authority, version, acquisition date и usage note.",
        "DR-REF-KSI-001": "Поместить файл источника в `data/reference/inbox/ksi/` и указать authority, version, acquisition date и usage note.",
        "DR-REF-WORK-TYPES-001": "Поместить файл источника в `data/reference/inbox/work_types/` и указать authority, version, acquisition date и usage note.",
        "NR-RULE-PARTITION-BRICK-120-REINF-001": "Указать `source_id` и `normalized_record_id` для недостающих evidence fields: excluded_works, gesn_norm, included_works, ksi_process_code, ksi_result_code, norm_unit, resource_composition, technical_part_reference, work_type.",
    }
    return actions.get(
        action_id,
        str(
            action.get("expected_input")
            or action.get("expected_action")
            or action.get("question")
            or "Ответить на вопрос пользователя."
        ),
    )


def text_blocks(values: Any, key: str) -> list[dict[str, str]]:
    result: list[dict[str, str]] = []
    for item in as_list(values):
        if isinstance(item, dict) and item.get(key):
            result.append({key: str(item[key])})
    return result


def acceptance_item(item: dict[str, Any]) -> dict[str, Any]:
    packet_id = str(item.get("packet_id") or "")
    report = str(item.get("acceptance_report") or "")
    report_path = PROJECT_ROOT / report
    blockers = block_list(item.get("blockers"))
    risks = block_list(item.get("risks"))
    status = str(item.get("status") or "pending")
    item_priority = "high" if status in {"needs_revision", "blocked"} else "medium"
    return {
        "id": f"ACCEPTANCE-{packet_id}",
        "type": "acceptance",
        "priority": item_priority,
        "status": status,
        "packet_id": packet_id,
        "title": item.get("title") or packet_id,
        "source_file": report,
        "source_id": packet_id,
        "source_checksum_sha256": checksum(report_path),
        "acceptance_report": report,
        "related_artifacts": artifact_list(item.get("artifacts")),
        "commands": command_list(item.get("verification_commands")),
        "acceptance_criteria": as_list(item.get("acceptance_criteria")),
        "blockers": blockers,
        "risks": risks,
        "required_user_action": "Проверить acceptance report, выполнить команды и заполнить решение пользователя.",
        "how_to_check": [
            {"step": "Открыть acceptance report."},
            {"step": "Проверить критерии приемки, артефакты, блокеры и риски."},
            {"step": "Выполнить указанные команды проверки."},
        ],
        "expected_result": [
            {
                "result": "Пользователь вручную принимает решение в workbench или непосредственно в acceptance report."
            }
        ],
        "target_decision_file": report,
        "target_fields_to_fill": [
            {"field": "acceptance_decision"},
            {"field": "accepted_by"},
            {"field": "accepted_at"},
            {"field": "comments"},
        ],
        "user_decision": {
            "acceptance_decision": "pending",
            "accepted_by": "",
            "accepted_at": "",
            "comments": "",
        },
        "apply_policy": {
            "can_apply": False,
            "reason": "Заполните user_decision и примените через scripts/apply_user_review_decisions.py.",
        },
    }


def recently_accepted_item(item: dict[str, Any]) -> dict[str, Any]:
    decision = (
        item.get("user_decision") if isinstance(item.get("user_decision"), dict) else {}
    )
    return {
        "packet_id": item.get("packet_id"),
        "accepted_by": decision.get("decided_by") or "",
        "accepted_at": decision.get("decided_at") or "",
        "acceptance_report": item.get("acceptance_report") or "",
        "hidden_from_active_queue": True,
    }


def manual_check_item(check: dict[str, Any]) -> dict[str, Any]:
    check_id = str(check.get("check_id") or "")
    source_file = rel(VERIFICATION_DASHBOARD_PATH)
    return {
        "id": f"VERIFICATION-{check_id}",
        "type": "manual_verification",
        "priority": priority(check.get("priority")),
        "status": str(check.get("status") or "pending"),
        "packet_id": check.get("related_packet") or "",
        "title": check.get("title") or check_id,
        "source_file": source_file,
        "source_id": check_id,
        "source_checksum_sha256": checksum(VERIFICATION_DASHBOARD_PATH),
        "acceptance_report": "",
        "related_artifacts": artifact_list(check.get("artifacts")),
        "commands": command_list(check.get("commands")),
        "acceptance_criteria": [],
        "blockers": [],
        "risks": [],
        "required_user_action": "Выполнить ручную проверку и заполнить user_result в verification dashboard.",
        "how_to_check": text_blocks(check.get("how_to_check"), "step"),
        "expected_result": text_blocks(check.get("expected_result"), "result"),
        "target_decision_file": source_file,
        "target_fields_to_fill": [
            {"field": "user_result.checked"},
            {"field": "user_result.checked_by"},
            {"field": "user_result.checked_at"},
            {"field": "user_result.result"},
            {"field": "user_result.comments"},
        ],
        "user_decision": {
            "acceptance_decision": "pending",
            "accepted_by": "",
            "accepted_at": "",
            "comments": "",
        },
        "apply_policy": {
            "can_apply": False,
            "reason": "Первый apply script применяет только acceptance decisions.",
        },
    }


def user_action_item(action: dict[str, Any]) -> dict[str, Any]:
    action_id = str(action.get("id") or "")
    source_file = str(action.get("source_file") or rel(USER_ACTION_DASHBOARD_PATH))
    source_path = PROJECT_ROOT / source_file
    blocks = block_list(action.get("blocks"))
    item_type = (
        "requires_user_approval"
        if action.get("requires_user_approval")
        else "user_action"
    )
    return {
        "id": f"USER-ACTION-{action_id}",
        "type": item_type,
        "priority": priority(action.get("priority"), "medium"),
        "status": str(action.get("status") or "open"),
        "packet_id": "",
        "title": russian_user_action_title(action),
        "source_file": source_file,
        "source_id": action_id,
        "source_checksum_sha256": checksum(source_path),
        "acceptance_report": "",
        "related_artifacts": [{"path": str(action.get("target_path"))}]
        if action.get("target_path")
        else [],
        "commands": [],
        "acceptance_criteria": [],
        "blockers": blocks,
        "risks": [],
        "required_user_action": russian_required_user_action(action),
        "how_to_check": [{"step": f"Открыть {source_file}."}],
        "expected_result": [
            {"result": "Пользователь заполняет профильные поля ответа в source file."}
        ],
        "target_decision_file": source_file,
        "target_fields_to_fill": [
            {"field": "resolution"},
            {"field": "answered_by"},
            {"field": "answered_at"},
            {"field": "comments"},
        ],
        "user_decision": {
            "acceptance_decision": "pending",
            "accepted_by": "",
            "accepted_at": "",
            "comments": "",
        },
        "apply_policy": {
            "can_apply": False,
            "reason": "Первый apply script не применяет user actions.",
        },
    }


def audit_finding_item(finding: dict[str, Any]) -> dict[str, Any]:
    finding_id = str(finding.get("id") or "")
    source_file = rel(AUDIT_FINDINGS_PATH)
    return {
        "id": f"AUDIT-{finding_id}",
        "type": "requires_user_approval"
        if finding.get("status") == "requires_user_approval"
        else "audit_finding",
        "priority": priority(finding.get("severity")),
        "status": str(finding.get("status") or "open"),
        "packet_id": "",
        "title": finding.get("issue") or finding_id,
        "source_file": source_file,
        "source_id": finding_id,
        "source_checksum_sha256": checksum(AUDIT_FINDINGS_PATH),
        "acceptance_report": "",
        "related_artifacts": [{"path": str(finding.get("file"))}]
        if finding.get("file")
        else [],
        "commands": [],
        "acceptance_criteria": [],
        "blockers": [
            {
                "id": str(finding.get("check_id") or finding_id),
                "text": str(finding.get("issue") or ""),
            }
        ],
        "risks": [],
        "required_user_action": finding.get("recommendation")
        or "Проверить audit finding и выбрать действие.",
        "how_to_check": [{"step": "Открыть docs/audit/audit-findings.yml."}],
        "expected_result": [
            {
                "result": "Пользователь фиксирует решение по finding в audit-findings.yml."
            }
        ],
        "target_decision_file": source_file,
        "target_fields_to_fill": [
            {"field": "status"},
            {"field": "resolved_by"},
            {"field": "resolved_at"},
            {"field": "resolution"},
        ],
        "user_decision": {
            "acceptance_decision": "pending",
            "accepted_by": "",
            "accepted_at": "",
            "comments": "",
        },
        "apply_policy": {
            "can_apply": False,
            "reason": "Первый apply script не применяет audit findings.",
        },
    }


def read_acceptance_items() -> tuple[
    list[dict[str, Any]], list[dict[str, Any]], list[dict[str, str]]
]:
    dashboard = load_dashboard(ACCEPTANCE_DASHBOARD_PATH, "acceptance_dashboard")
    items = dashboard.get("items", []) if isinstance(dashboard, dict) else []
    active: list[dict[str, Any]] = []
    accepted: list[dict[str, Any]] = []
    warnings: list[dict[str, str]] = []
    for item in items if isinstance(items, list) else []:
        if not isinstance(item, dict):
            continue
        packet_id = str(item.get("packet_id") or "")
        decision = str(item.get("acceptance_decision") or "pending")
        status = str(item.get("status") or "")
        report = str(item.get("acceptance_report") or "")
        if decision == "accepted":
            accepted.append(recently_accepted_item(item))
            continue
        if status in ACTIVE_ACCEPTANCE_STATUSES or decision in {
            "pending",
            "needs_revision",
        }:
            active_item = acceptance_item(item)
            active.append(active_item)
            warnings.extend(
                pseudo_warnings(
                    packet_id,
                    report,
                    active_item.get("blockers", []),
                    "blocker",
                )
            )
            warnings.extend(
                pseudo_warnings(packet_id, report, active_item.get("risks", []), "risk")
            )
    return active, accepted, warnings


def read_manual_checks() -> list[dict[str, Any]]:
    dashboard = load_dashboard(VERIFICATION_DASHBOARD_PATH, "verification_dashboard")
    checks = dashboard.get("checks", []) if isinstance(dashboard, dict) else []
    active: list[dict[str, Any]] = []
    for check in checks if isinstance(checks, list) else []:
        if not isinstance(check, dict):
            continue
        check_type = str(check.get("check_type") or "")
        status = str(check.get("status") or "")
        if check_type != "automated_command" and status in ACTIVE_CHECK_STATUSES:
            active.append(manual_check_item(check))
    return active


def read_user_actions() -> list[dict[str, Any]]:
    dashboard = load_dashboard(USER_ACTION_DASHBOARD_PATH, "user_action_dashboard")
    actions = dashboard.get("actions", []) if isinstance(dashboard, dict) else []
    active: list[dict[str, Any]] = []
    for action in actions if isinstance(actions, list) else []:
        if not isinstance(action, dict):
            continue
        if str(action.get("type") or "") == "audit_finding":
            continue
        if str(action.get("status") or "") in ACTIVE_ACTION_STATUSES:
            active.append(user_action_item(action))
    return active


def read_audit_findings() -> list[dict[str, Any]]:
    if not AUDIT_FINDINGS_PATH.exists():
        return []
    data = load_data(AUDIT_FINDINGS_PATH)
    findings = data.get("findings", []) if isinstance(data, dict) else []
    active: list[dict[str, Any]] = []
    for finding in findings if isinstance(findings, list) else []:
        if not isinstance(finding, dict):
            continue
        status = str(finding.get("status") or "")
        severity = str(finding.get("severity") or "")
        if status not in ACTIVE_ACTION_STATUSES:
            continue
        if severity in {"critical", "high"} or status == "requires_user_approval":
            active.append(audit_finding_item(finding))
    return active


def sort_items(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        items,
        key=lambda item: (
            PRIORITY_ORDER.get(str(item.get("priority") or "medium"), 2),
            str(item.get("type") or ""),
            str(item.get("id") or ""),
        ),
    )


def build_workbench() -> dict[str, Any]:
    source_entries = [source_file_entry(path) for path in SOURCE_PATHS]
    warnings = [source_file_warning(path) for path in SOURCE_PATHS if not path.exists()]

    acceptance_items, accepted_items, pseudo = read_acceptance_items()
    warnings.extend(pseudo)
    manual_items = read_manual_checks()
    user_action_items = read_user_actions()
    audit_items = read_audit_findings()
    active_items = sort_items(
        acceptance_items + manual_items + user_action_items + audit_items
    )

    summary = {
        "active_review_items": len(active_items),
        "ready_for_acceptance": sum(
            item["type"] == "acceptance"
            and item.get("status") == "ready_for_acceptance"
            for item in active_items
        ),
        "needs_revision": sum(
            item.get("status") == "needs_revision" for item in active_items
        ),
        "pending_manual_checks": len(manual_items),
        "open_user_actions": len(user_action_items),
        "requires_user_approval": sum(
            item.get("type") == "requires_user_approval" for item in active_items
        ),
        "critical_audit_findings": sum(
            item.get("type") == "audit_finding" and item.get("priority") == "critical"
            for item in active_items
        ),
        "high_audit_findings": sum(
            item.get("type") == "audit_finding" and item.get("priority") == "high"
            for item in active_items
        ),
        "active_blockers": sum(
            len(item.get("blockers") or []) for item in active_items
        ),
        "accepted_hidden_from_active_queue": len(accepted_items),
    }
    return {
        "user_review_workbench": {
            "schema_version": 1,
            "generated_at": date.today().isoformat(),
            "generated_by": "Codex",
            "mode": "active_user_review_queue",
            "source_files": source_entries,
            "summary": summary,
            "post_acceptance_baseline": {
                "project_state": "accepted_baseline",
                "accepted_packets": accepted_items,
                "protection_flags_status": "classified_by_EP-018",
                "protection_packet": PROTECTION_PACKET,
                "verification_debt_status": "deferred_to_EP-015",
                "reference_intake_status": "deferred_to_EP-016",
                "audit_cleanup_status": "deferred_to_EP-017",
            },
            "decision_application_flow": [
                {
                    "step": 1,
                    "command": "make apply-user-review-decisions-dry-run",
                    "required": True,
                    "purpose": "Сначала выполнить dry-run и получить planned changes, affected files, reasons и diff.",
                },
                {
                    "step": 2,
                    "command": "",
                    "required": True,
                    "purpose": "Проверить affected files и убедиться, что не меняются чужие acceptance reports.",
                },
                {
                    "step": 3,
                    "command": "",
                    "required": True,
                    "purpose": "Проверить, что Codex не заполняет user-owned поля: accepted_by, accepted_at, checked_by, answered_by, decided_by.",
                },
                {
                    "step": 4,
                    "command": "make apply-user-review-decisions",
                    "required": True,
                    "purpose": "Выполнять apply только после просмотра dry-run diff и подтверждения безопасного scope.",
                },
            ],
            "active_review_items": active_items,
            "recently_accepted": accepted_items,
            "warnings": warnings,
        }
    }


def commands_text(item: dict[str, Any]) -> str:
    commands = [command.get("command", "") for command in item.get("commands", [])]
    return ", ".join(command for command in commands if command) or "-"


def blockers_text(item: dict[str, Any]) -> str:
    blockers = [block.get("text", "") for block in item.get("blockers", [])]
    return "; ".join(text for text in blockers if text) or "-"


def risks_text(item: dict[str, Any]) -> str:
    risks = [risk.get("text", "") for risk in item.get("risks", [])]
    return "; ".join(text for text in risks if text) or "-"


def first_step(item: dict[str, Any]) -> str:
    steps = item.get("how_to_check") or []
    if steps and isinstance(steps[0], dict):
        return str(steps[0].get("step") or "-")
    return "-"


def write_markdown(workbench: dict[str, Any]) -> None:
    data = workbench["user_review_workbench"]
    items = data["active_review_items"]
    summary = data["summary"]
    lines = [
        "# Единое активное окно проверки пользователем",
        "",
        f"Дата обновления: {data['generated_at']}",
        "",
        "## 1. Сводка",
        "",
        "| Раздел | Количество |",
        "|---|---:|",
        f"| Активные элементы проверки | {summary['active_review_items']} |",
        f"| Пакеты готовы к приемке | {summary['ready_for_acceptance']} |",
        f"| Ручные проверки ожидают выполнения | {summary['pending_manual_checks']} |",
        f"| Вопросы требуют ответа | {summary['open_user_actions']} |",
        f"| Требуют user approval | {summary['requires_user_approval']} |",
        f"| Critical audit findings | {summary['critical_audit_findings']} |",
        f"| High audit findings | {summary['high_audit_findings']} |",
        f"| Активные блокеры | {summary['active_blockers']} |",
        f"| Принятые пакеты скрыты из активной очереди | {summary['accepted_hidden_from_active_queue']} |",
        "",
        "## 2. Что требует моего решения сейчас",
        "",
        "| Приоритет | Тип | ID | EP | Что проверить | Где источник | Действие |",
        "|---|---|---|---|---|---|---|",
    ]
    if items:
        for item in items:
            lines.append(
                f"| {md(item.get('priority'))} | {md(item.get('type'))} | {md(item.get('id'))} | {md(item.get('packet_id'))} | {md(item.get('title'))} | {md(item.get('source_file'))} | {md(item.get('required_user_action'))} |"
            )
    else:
        lines.append("| - | - | - | - | - | - | - |")

    acceptance_items = [item for item in items if item.get("type") == "acceptance"]
    lines.extend(
        [
            "",
            "## 3. Пакеты ready_for_acceptance",
            "",
            "| EP | Название | Команды | Блокеры | Риски | Где заполнить решение |",
            "|---|---|---|---|---|---|",
        ]
    )
    if acceptance_items:
        for item in acceptance_items:
            lines.append(
                f"| {md(item.get('packet_id'))} | {md(item.get('title'))} | {md(commands_text(item))} | {md(blockers_text(item))} | {md(risks_text(item))} | {md(item.get('target_decision_file'))} |"
            )
    else:
        lines.append("| - | - | - | - | - | - |")

    manual_items = [item for item in items if item.get("type") == "manual_verification"]
    lines.extend(
        [
            "",
            "## 4. Ручные проверки",
            "",
            "| ID | EP | Проверка | Как проверить | Где отметить |",
            "|---|---|---|---|---|",
        ]
    )
    if manual_items:
        for item in manual_items:
            lines.append(
                f"| {md(item.get('source_id'))} | {md(item.get('packet_id'))} | {md(item.get('title'))} | {md(first_step(item))} | {md(item.get('target_decision_file'))} |"
            )
    else:
        lines.append("| - | - | - | - | - |")

    action_items = [item for item in items if item.get("type") == "user_action"]
    lines.extend(
        [
            "",
            "## 5. Вопросы и user actions",
            "",
            "| ID | Вопрос | Что требуется | Блокирует | Где ответить |",
            "|---|---|---|---|---|",
        ]
    )
    if action_items:
        for item in action_items:
            lines.append(
                f"| {md(item.get('source_id'))} | {md(item.get('title'))} | {md(item.get('required_user_action'))} | {md(blockers_text(item))} | {md(item.get('target_decision_file'))} |"
            )
    else:
        lines.append("| - | - | - | - | - |")

    approval_items = [
        item for item in items if item.get("type") == "requires_user_approval"
    ]
    lines.extend(
        [
            "",
            "## 6. Requires user approval",
            "",
            "| ID | Объект | Причина | Что требуется |",
            "|---|---|---|---|",
        ]
    )
    if approval_items:
        for item in approval_items:
            lines.append(
                f"| {md(item.get('source_id'))} | {md(item.get('source_file'))} | {md(item.get('title'))} | {md(item.get('required_user_action'))} |"
            )
    else:
        lines.append("| - | - | - | - |")

    audit_items = [item for item in items if item.get("type") == "audit_finding"]
    lines.extend(
        [
            "",
            "## 7. Audit findings critical/high",
            "",
            "| ID | Severity | Файл | Проблема | Рекомендация |",
            "|---|---|---|---|---|",
        ]
    )
    if audit_items:
        for item in audit_items:
            artifact = item.get("related_artifacts") or [{}]
            lines.append(
                f"| {md(item.get('source_id'))} | {md(item.get('priority'))} | {md(artifact[0].get('path'))} | {md(item.get('title'))} | {md(item.get('required_user_action'))} |"
            )
    else:
        lines.append("| - | - | - | - | - |")

    lines.extend(
        [
            "",
            "## 8. Как принять EP через единое окно",
            "",
            "1. Выполнить команды проверки, указанные для EP.",
            "2. Проверить blockers и risks.",
            "3. Заполнить `user_decision` в `docs/user-review-workbench.yml`.",
            "4. Запустить `make apply-user-review-decisions-dry-run`.",
            "5. Проверить dry-run diff, список affected files и reasons.",
            "6. Убедиться, что dry-run не меняет чужие acceptance reports и Codex не заполняет user-owned поля.",
            "7. Только после просмотра dry-run diff запустить `make apply-user-review-decisions`.",
            "8. Запустить `make generate-dashboards`.",
            "9. Запустить `make validate-plan`.",
            "10. Запустить `make check`.",
            "11. Убедиться, что принятый EP исчез из `active_review_items`, но сохранился в acceptance report и dashboards.",
            "",
            "## 9. Post-acceptance baseline",
            "",
            "Accepted packets are hidden from `active_review_items`; acceptance reports remain the source of truth.",
            "",
            f"Accepted artifact protection is deferred to `{PROTECTION_PACKET}`.",
            "",
            "## 10. Недавно принятые пакеты",
            "",
            "| EP | Дата | Кем | Acceptance report |",
            "|---|---|---|---|",
        ]
    )
    accepted = data.get("recently_accepted") or []
    if accepted:
        for item in accepted:
            lines.append(
                f"| {md(item.get('packet_id'))} | {md(item.get('accepted_at'))} | {md(item.get('accepted_by'))} | {md(item.get('acceptance_report'))} |"
            )
    else:
        lines.append("| - | - | - | - |")

    warnings = data.get("warnings") or []
    if warnings:
        lines.extend(
            [
                "",
                "## 11. Warnings",
                "",
                "| ID | Severity | Text | Source |",
                "|---|---|---|---|",
            ]
        )
        for warning in warnings:
            lines.append(
                f"| {md(warning.get('id'))} | {md(warning.get('severity'))} | {md(warning.get('text'))} | {md(warning.get('source_file'))} |"
            )

    MARKDOWN_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    workbench = build_workbench()
    write_yaml(YAML_PATH, workbench)
    write_markdown(workbench)
    print("User review workbench generated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
