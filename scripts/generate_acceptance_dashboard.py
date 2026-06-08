#!/usr/bin/env python3
from __future__ import annotations

import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path
from typing import Any

from reference_utils import load_data, write_yaml


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PACKETS_PATH = PROJECT_ROOT / "docs" / "grace" / "execution-packets.xml"
REGISTRY_PATH = PROJECT_ROOT / "docs" / "artifact-registry.yml"
ACCEPTANCE_DIR = PROJECT_ROOT / "docs" / "acceptance"
YAML_PATH = PROJECT_ROOT / "docs" / "acceptance-dashboard.yml"
MARKDOWN_PATH = PROJECT_ROOT / "docs" / "acceptance-dashboard.md"


def rel(path: Path) -> str:
    return str(path.relative_to(PROJECT_ROOT))


def read_registry() -> list[dict[str, Any]]:
    if not REGISTRY_PATH.exists():
        return []
    data = load_data(REGISTRY_PATH)
    artifacts = data.get("artifacts", []) if isinstance(data, dict) else []
    return [artifact for artifact in artifacts if isinstance(artifact, dict)]


def read_packets() -> list[dict[str, Any]]:
    if not PACKETS_PATH.exists():
        return []
    root = ET.parse(PACKETS_PATH).getroot()
    packets: list[dict[str, Any]] = []
    for packet in root.findall("Packet"):
        criteria = []
        criteria_node = packet.find("AcceptanceCriteria")
        if criteria_node is not None:
            for criterion in criteria_node.findall("Criterion"):
                criteria.append(
                    {
                        "id": criterion.attrib.get("id", ""),
                        "text": (criterion.text or "").strip(),
                    }
                )
        packets.append(
            {
                "packet_id": packet.attrib.get("id", ""),
                "status": packet.attrib.get("status", "planned"),
                "title": (packet.findtext("Name") or "").strip(),
                "acceptance_owner": (
                    packet.findtext("AcceptanceOwner") or "Дмитрий"
                ).strip(),
                "acceptance_criteria": criteria,
            }
        )
    return packets


def parse_acceptance_report(path: Path) -> dict[str, Any]:
    result: dict[str, Any] = {
        "acceptance_decision": "pending",
        "accepted_by": "",
        "accepted_at": "",
        "comments": "",
        "codex_status": "",
        "commands": [],
        "blockers": [],
        "risks": [],
    }
    if not path.exists():
        result["warning"] = "acceptance report missing"
        return result
    text = path.read_text(encoding="utf-8")
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("- Статус Codex:"):
            result["codex_status"] = stripped.split(":", 1)[1].strip()
        elif stripped.startswith("acceptance_decision:"):
            value = stripped.split(":", 1)[1].strip()
            result["acceptance_decision"] = value or "pending"
        elif stripped.startswith("accepted_by:"):
            result["accepted_by"] = stripped.split(":", 1)[1].strip()
        elif stripped.startswith("accepted_at:"):
            result["accepted_at"] = stripped.split(":", 1)[1].strip()
        elif stripped.startswith("comments:"):
            result["comments"] = stripped.split(":", 1)[1].strip()
    result["commands"] = extract_code_block_commands(text, "## 4.")
    result["blockers"] = extract_bullets(text, "## 7.")
    result["risks"] = extract_bullets(text, "## 8.")
    return result


def extract_code_block_commands(text: str, section_prefix: str) -> list[str]:
    lines = text.splitlines()
    in_section = False
    in_code = False
    commands: list[str] = []
    for line in lines:
        if line.startswith("## "):
            in_section = line.startswith(section_prefix)
            in_code = False
            continue
        if not in_section:
            continue
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code and line.strip():
            commands.append(line.strip())
    return commands


def extract_bullets(text: str, section_prefix: str) -> list[str]:
    lines = text.splitlines()
    in_section = False
    bullets: list[str] = []
    for line in lines:
        if line.startswith("## "):
            if in_section:
                break
            in_section = line.startswith(section_prefix)
            continue
        if in_section and line.strip().startswith("-"):
            bullets.append(line.strip().lstrip("-").strip())
    return bullets


def is_accepted_artifact(artifact: dict[str, Any]) -> bool:
    acceptance = (
        artifact.get("acceptance")
        if isinstance(artifact.get("acceptance"), dict)
        else {}
    )
    protection = (
        artifact.get("protection")
        if isinstance(artifact.get("protection"), dict)
        else {}
    )
    return bool(
        acceptance.get("status") == "accepted"
        or artifact.get("status") == "accepted"
        or (artifact.get("status") == "verified" and acceptance.get("accepted_by"))
        or protection.get("locked") is True
    )


def artifact_summary(artifact: dict[str, Any]) -> dict[str, Any]:
    acceptance = (
        artifact.get("acceptance")
        if isinstance(artifact.get("acceptance"), dict)
        else {}
    )
    protection = (
        artifact.get("protection")
        if isinstance(artifact.get("protection"), dict)
        else {}
    )
    protected = is_accepted_artifact(artifact)
    return {
        "path": artifact.get("path"),
        "status": artifact.get("status"),
        "type": artifact.get("type"),
        "acceptance_status": acceptance.get("status", "pending"),
        "protection_locked": bool(protected or protection.get("locked") is True),
    }


def build_dashboard() -> dict[str, Any]:
    artifacts = read_registry()
    packets = read_packets()
    artifacts_by_packet: dict[str, list[dict[str, Any]]] = {}
    for artifact in artifacts:
        for packet_id in artifact.get("related_packets", []) or []:
            artifacts_by_packet.setdefault(str(packet_id), []).append(artifact)

    items: list[dict[str, Any]] = []
    warnings: list[str] = []
    report_paths = {
        path.stem.replace(".acceptance", ""): path
        for path in ACCEPTANCE_DIR.glob("*.acceptance.md")
    }
    packet_ids = {packet["packet_id"] for packet in packets}
    for packet_id in sorted(set(packet_ids) | set(report_paths)):
        packet = next(
            (item for item in packets if item["packet_id"] == packet_id), None
        )
        report_path = report_paths.get(
            packet_id, ACCEPTANCE_DIR / f"{packet_id}.acceptance.md"
        )
        report = parse_acceptance_report(report_path)
        status = report.get("codex_status") or (packet or {}).get(
            "status", "review_required"
        )
        if report.get("warning"):
            warnings.append(f"{packet_id}: {report['warning']}")
            status = "review_required"
        decision = report.get("acceptance_decision", "pending") or "pending"
        owner = (packet or {}).get("acceptance_owner", "Дмитрий")
        packet_artifacts = [
            artifact_summary(item) for item in artifacts_by_packet.get(packet_id, [])
        ]
        criteria = [
            {
                "id": item.get("id"),
                "text": item.get("text"),
                "codex_status": "ready_for_acceptance"
                if status == "ready_for_acceptance"
                else status,
                "user_status": decision,
            }
            for item in (packet or {}).get("acceptance_criteria", [])
        ]
        items.append(
            {
                "packet_id": packet_id,
                "title": (packet or {}).get("title", packet_id),
                "status": status,
                "acceptance_owner": owner,
                "acceptance_decision": decision,
                "acceptance_report": rel(report_path)
                if report_path.exists()
                else str(report_path),
                "artifacts": packet_artifacts,
                "verification_commands": [
                    {"command": command, "status": "documented"}
                    for command in report.get("commands", [])
                ],
                "acceptance_criteria": criteria,
                "user_checklist": [
                    {"item": "Open the detailed acceptance report."},
                    {"item": "Review artifacts and criteria."},
                    {"item": "Run verification commands."},
                    {"item": "Fill user decision fields manually."},
                ],
                "blockers": [
                    {"id": f"{packet_id}-BLOCKER-{index + 1:03d}", "text": text}
                    for index, text in enumerate(report.get("blockers", []))
                ],
                "risks": [
                    {"id": f"{packet_id}-RISK-{index + 1:03d}", "text": text}
                    for index, text in enumerate(report.get("risks", []))
                ],
                "user_decision": {
                    "decision": decision,
                    "decided_by": report.get("accepted_by", ""),
                    "decided_at": report.get("accepted_at", ""),
                    "comments": report.get("comments", ""),
                },
            }
        )

    summary = {
        "ready_for_acceptance": sum(
            item["status"] == "ready_for_acceptance" for item in items
        ),
        "accepted": sum(
            item["acceptance_decision"] == "accepted" or item["status"] == "accepted"
            for item in items
        ),
        "needs_revision": sum(
            item["acceptance_decision"] == "needs_revision"
            or item["status"] == "needs_revision"
            for item in items
        ),
        "rejected": sum(
            item["acceptance_decision"] == "rejected" or item["status"] == "rejected"
            for item in items
        ),
        "blocked": sum(item["status"] == "blocked" for item in items),
        "pending": sum(
            item["acceptance_decision"] in {"", "pending"} for item in items
        ),
        "protected_accepted_artifacts": sum(
            is_accepted_artifact(artifact) for artifact in artifacts
        ),
    }
    return {
        "acceptance_dashboard": {
            "updated_at": date.today().isoformat(),
            "source_files": [
                "docs/grace/execution-packets.xml",
                "docs/artifact-registry.yml",
                "docs/acceptance/",
                "docs/status-report.md",
            ],
            "summary": summary,
            "warnings": warnings,
            "items": items,
        }
    }


def md_escape(value: Any) -> str:
    text = "" if value is None else str(value)
    return text.replace("|", "\\|") or "-"


def join_artifacts(artifacts: list[dict[str, Any]]) -> str:
    paths = [artifact.get("path") for artifact in artifacts if artifact.get("path")]
    return ", ".join(paths[:4]) + (", ..." if len(paths) > 4 else "") if paths else "-"


def write_markdown(dashboard: dict[str, Any]) -> None:
    data = dashboard["acceptance_dashboard"]
    items = data["items"]
    summary = data["summary"]
    lines = [
        "# Единое окно приемки проекта Tartip",
        "",
        f"Дата обновления: {data['updated_at']}",
        "",
        "## 1. Сводка",
        "",
        "| Статус | Количество |",
        "|---|---:|",
    ]
    for key in [
        "ready_for_acceptance",
        "accepted",
        "needs_revision",
        "rejected",
        "blocked",
        "pending",
        "protected_accepted_artifacts",
    ]:
        lines.append(f"| {key} | {summary[key]} |")
    lines.extend(
        [
            "",
            "## 2. Требуют приемки",
            "",
            "| Галочка | Пакет | Наименование | Что проверить | Артефакты | Команды | Детальный отчет |",
            "|---|---|---|---|---|---|---|",
        ]
    )
    ready_items = [
        item
        for item in items
        if item["status"] == "ready_for_acceptance"
        and item["acceptance_decision"] != "accepted"
    ]
    if ready_items:
        for item in ready_items:
            commands = (
                ", ".join(
                    command["command"] for command in item["verification_commands"]
                )
                or "-"
            )
            report = item["acceptance_report"]
            lines.append(
                f"| - [ ] требует проверки | {md_escape(item['packet_id'])} | {md_escape(item['title'])} | Acceptance criteria and artifacts | {md_escape(join_artifacts(item['artifacts']))} | {md_escape(commands)} | [{md_escape(report)}]({report}) |"
            )
    else:
        lines.append("| - | - | - | - | - | - | - |")
    lines.extend(
        [
            "",
            "## 3. Принятые задачи",
            "",
            "| Пакет | Наименование | Принял | Дата | Комментарий | Защита |",
            "|---|---|---|---|---|---|",
        ]
    )
    accepted_items = [
        item for item in items if item["acceptance_decision"] == "accepted"
    ]
    if accepted_items:
        for item in accepted_items:
            decision = item["user_decision"]
            lines.append(
                f"| {md_escape(item['packet_id'])} | {md_escape(item['title'])} | {md_escape(decision.get('decided_by'))} | {md_escape(decision.get('decided_at'))} | {md_escape(decision.get('comments'))} | protected |"
            )
    else:
        lines.append("| - | - | - | - | - | - |")
    lines.extend(
        [
            "",
            "## 4. Защищенные принятые артефакты",
            "",
            "| Артефакт | Пакет | Принял | Дата | Политика изменения |",
            "|---|---|---|---|---|",
        ]
    )
    protected_rows = []
    for item in items:
        for artifact in item["artifacts"]:
            if artifact.get("protection_locked"):
                protected_rows.append((item, artifact))
    if protected_rows:
        for item, artifact in protected_rows:
            decision = item["user_decision"]
            lines.append(
                f"| {md_escape(artifact.get('path'))} | {md_escape(item['packet_id'])} | {md_escape(decision.get('decided_by'))} | {md_escape(decision.get('decided_at'))} | Изменение требует user approval и новой ревизии |"
            )
    else:
        lines.append("| - | - | - | - | Нет accepted artifacts |")
    lines.extend(
        [
            "",
            "## 5. Требуют доработки",
            "",
            "| Пакет | Причина | Что доработать | Детальный отчет |",
            "|---|---|---|---|",
        ]
    )
    revision_items = [
        item
        for item in items
        if item["acceptance_decision"] == "needs_revision"
        or item["status"] == "needs_revision"
    ]
    if revision_items:
        for item in revision_items:
            report = item["acceptance_report"]
            lines.append(
                f"| {item['packet_id']} | needs_revision | See report | [{report}]({report}) |"
            )
    else:
        lines.append("| - | - | - | - |")
    lines.extend(
        [
            "",
            "## 6. Заблокированные задачи",
            "",
            "| Пакет | Причина блокировки | Что требуется | Детальный отчет |",
            "|---|---|---|---|",
        ]
    )
    blocked_items = [item for item in items if item["status"] == "blocked"]
    if blocked_items:
        for item in blocked_items:
            reason = (
                "; ".join(blocker["text"] for blocker in item["blockers"]) or "blocked"
            )
            report = item["acceptance_report"]
            lines.append(
                f"| {item['packet_id']} | {md_escape(reason)} | Resolve blocker | [{report}]({report}) |"
            )
    else:
        lines.append("| - | - | - | - |")
    lines.extend(
        [
            "",
            "## 7. Как принять задачу",
            "",
            "1. Открыть детальный acceptance report.",
            "2. Проверить артефакты.",
            "3. Запустить команды проверки.",
            "4. Заполнить решение пользователя.",
            "5. Не указывать Codex в качестве accepted_by / decided_by.",
            "",
            "## 8. Как изменить принятый артефакт",
            "",
            "1. Не изменять accepted artifact напрямую.",
            "2. Создать change request.",
            "3. Указать причину изменения.",
            "4. Указать impact analysis.",
            "5. Получить согласование пользователя.",
            "6. Создать новую ревизию или отдельный пакет изменения.",
            "7. Провести повторную приемку.",
            "",
            "Состояние хранится в YAML dashboard и acceptance reports, а не только в Markdown-чекбоксах.",
            "",
        ]
    )
    MARKDOWN_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    dashboard = build_dashboard()
    write_yaml(YAML_PATH, dashboard)
    write_markdown(dashboard)
    print("Acceptance dashboard generated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
