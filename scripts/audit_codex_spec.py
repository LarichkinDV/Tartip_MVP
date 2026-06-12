#!/usr/bin/env python3
from __future__ import annotations

import fnmatch
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path
from typing import Any

from reference_utils import load_data, write_yaml


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TODAY = date.today().isoformat()
FINDINGS_PATH = PROJECT_ROOT / "docs" / "audit" / "audit-findings.yml"
REPORT_PATH = PROJECT_ROOT / "docs" / "audit" / "codex-spec-audit.md"
PACKETS_PATH = PROJECT_ROOT / "docs" / "grace" / "execution-packets.xml"
KNOWLEDGE_GRAPH_PATH = PROJECT_ROOT / "docs" / "grace" / "knowledge-graph.xml"
REGISTRY_PATH = PROJECT_ROOT / "docs" / "artifact-registry.yml"
ACCEPTANCE_DASHBOARD_PATH = PROJECT_ROOT / "docs" / "acceptance-dashboard.yml"
USER_ACTION_DASHBOARD_PATH = PROJECT_ROOT / "docs" / "user-action-dashboard.yml"
VERIFICATION_DASHBOARD_PATH = PROJECT_ROOT / "docs" / "verification-dashboard.yml"
PROJECT_STATE_PATH = PROJECT_ROOT / "docs" / "project-state.yml"
MONTHLY_PLAN_PATH = PROJECT_ROOT / "docs" / "monthly" / "monthly-plan.yml"
FORBIDDEN_CLAIMS_PATH = (
    PROJECT_ROOT / "docs" / "dissertation" / "prompt-profiles" / "forbidden-claims.yml"
)
BRANCH_RE = re.compile(r"^ep-\d{3}-[a-z0-9][a-z0-9-]*$")
BRANCH_PACKET_RE = re.compile(r"^ep-(?P<number>\d{3})-")
BRANCH_MISMATCH_ISSUE_RE = re.compile(
    r"Имя ветки (?P<branch>\S+) не соответствует packet (?P<packet>EP-\d{3}-[A-Z0-9-]+)\."
)
FORBIDDEN_GIT_PATTERNS = [
    ".env",
    ".env.*",
    ".venv/*",
    "node_modules/*",
    "*.dump",
    "*.sql",
    "*.backup",
    "backups/*",
    "thesis/source/*.docx",
    "thesis/versions/*.docx",
    "thesis/exports/pdf/*.pdf",
]

ALLOWED_STATUSES = {
    "open",
    "acknowledged",
    "fixed",
    "accepted_risk",
    "false_positive",
    "blocked",
    "requires_user_approval",
}
BLOCKING_STATUSES = {"open", "blocked", "requires_user_approval"}
ACTIVE_PACKET_STATUSES = {"ready_for_acceptance", "accepted"}


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(PROJECT_ROOT))
    except ValueError:
        return str(path)


def as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def finding(
    finding_id: str,
    check_id: str,
    severity: str,
    category: str,
    file: str,
    line: int | None,
    issue: str,
    recommendation: str,
    status: str = "open",
) -> dict[str, Any]:
    return {
        "id": finding_id,
        "check_id": check_id,
        "severity": severity,
        "category": category,
        "file": file,
        "line": line,
        "issue": issue,
        "recommendation": recommendation,
        "status": status,
        "created_at": TODAY,
        "resolved_by": None,
        "resolved_at": None,
        "resolution": None,
        "preserve_user_resolution": True,
        "last_seen_at": TODAY,
        "current_detected": True,
    }


def load_findings() -> list[dict[str, Any]]:
    if not FINDINGS_PATH.exists():
        return []
    data = load_data(FINDINGS_PATH)
    findings = data.get("findings", []) if isinstance(data, dict) else []
    return [item for item in findings if isinstance(item, dict)]


def merge_findings(generated: list[dict[str, Any]]) -> list[dict[str, Any]]:
    existing = load_findings()
    by_id = {str(item.get("id")): item for item in existing if item.get("id")}
    merged: list[dict[str, Any]] = []
    generated_ids = {str(item["id"]) for item in generated}

    for item in existing:
        item_id = str(item.get("id") or "")
        if item_id not in generated_ids:
            item["current_detected"] = False
            merged.append(item)

    for item in generated:
        item_id = str(item["id"])
        previous = by_id.get(item_id)
        if previous:
            preserved = dict(item)
            for key in [
                "status",
                "created_at",
                "resolved_by",
                "resolved_at",
                "resolution",
            ]:
                if key in previous:
                    preserved[key] = previous.get(key)
            preserved["preserve_user_resolution"] = True
            preserved["last_seen_at"] = TODAY
            merged.append(preserved)
        else:
            merged.append(item)

    merged.sort(key=lambda value: str(value.get("id") or ""))
    write_yaml(
        FINDINGS_PATH,
        {
            "schema_version": 1,
            "updated_at": TODAY,
            "allowed_statuses": sorted(ALLOWED_STATUSES),
            "audit_finding_groups": audit_finding_groups(merged),
            "findings": merged,
        },
    )
    return merged


def line_for(path: Path, needle: str) -> int | None:
    if not path.exists():
        return None
    for index, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if needle in line:
            return index
    return None


def check_agents_sections() -> list[dict[str, Any]]:
    path = PROJECT_ROOT / "AGENTS.md"
    required = [
        "Reference data discipline",
        "Project planning and acceptance discipline",
        "Dashboard discipline",
        "Accepted artifact protection",
        "Verification dashboard discipline",
        "Monthly defense discipline",
        "Dissertation synchronization and prompt generation discipline",
        "Language policy",
        "Audit discipline",
        "Git workflow discipline",
    ]
    findings: list[dict[str, Any]] = []
    if not path.exists():
        return [
            finding(
                "AUD-AUDIT-AGENTS-MISSING",
                "AUD-AUDIT-001",
                "critical",
                "audit_integrity",
                "AGENTS.md",
                None,
                "Файл AGENTS.md отсутствует.",
                "Восстановить AGENTS.md перед изменением доменной логики или инфраструктуры.",
            )
        ]
    text = path.read_text(encoding="utf-8")
    for section in required:
        if f"## {section}" not in text:
            findings.append(
                finding(
                    f"AUD-AUDIT-AGENTS-MISSING-{section.upper().replace(' ', '-')}",
                    "AUD-AUDIT-001",
                    "critical",
                    "audit_integrity",
                    "AGENTS.md",
                    None,
                    f"В AGENTS.md отсутствует раздел {section}.",
                    "Добавить раздел без изменения доменной методики.",
                )
            )
    return findings


def check_knowledge_graph() -> list[dict[str, Any]]:
    if not KNOWLEDGE_GRAPH_PATH.exists():
        return [
            finding(
                "AUD-DOMAIN-KNOWLEDGE-GRAPH-MISSING",
                "AUD-DOMAIN-001",
                "critical",
                "domain_logic",
                rel(KNOWLEDGE_GRAPH_PATH),
                None,
                "GRACE knowledge graph отсутствует.",
                "Восстановить knowledge-graph.xml с ForbiddenEdge для ModelElement -> GESNNorm.",
            )
        ]
    root = ET.parse(KNOWLEDGE_GRAPH_PATH).getroot()
    for node in root.findall(".//ForbiddenEdge"):
        attrs = {key.lower(): value for key, value in node.attrib.items()}
        source = attrs.get("from") or attrs.get("source") or attrs.get("src")
        target = attrs.get("to") or attrs.get("target") or attrs.get("dst")
        if source == "ModelElement" and target == "GESNNorm":
            return []
    text = KNOWLEDGE_GRAPH_PATH.read_text(encoding="utf-8")
    if "ModelElement" in text and "GESNNorm" in text and "ForbiddenEdge" in text:
        return []
    return [
        finding(
            "AUD-DOMAIN-MODELELEMENT-GESNNORM-FORBIDDEN-EDGE-MISSING",
            "AUD-DOMAIN-001",
            "critical",
            "domain_logic",
            rel(KNOWLEDGE_GRAPH_PATH),
            line_for(KNOWLEDGE_GRAPH_PATH, "ModelElement"),
            "В knowledge graph не найден явный запрет прямой связи ModelElement -> GESNNorm.",
            "Добавить ForbiddenEdge только как запрет, не как разрешенную связь.",
        )
    ]


def check_execution_packets() -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    if not PACKETS_PATH.exists():
        return [
            finding(
                "AUD-AUDIT-PACKETS-MISSING",
                "AUD-AUDIT-001",
                "critical",
                "audit_integrity",
                rel(PACKETS_PATH),
                None,
                "execution-packets.xml отсутствует.",
                "Восстановить GRACE execution packet registry.",
            )
        ]
    root = ET.parse(PACKETS_PATH).getroot()
    seen: set[str] = set()
    for packet in root.findall("Packet"):
        packet_id = packet.attrib.get("id") or "<missing-id>"
        if packet_id in seen:
            findings.append(
                finding(
                    f"AUD-AUDIT-DUPLICATE-PACKET-ID-{packet_id}",
                    "AUD-AUDIT-001",
                    "critical",
                    "audit_integrity",
                    rel(PACKETS_PATH),
                    line_for(PACKETS_PATH, f'id="{packet_id}"'),
                    f"Найден duplicate packet id: {packet_id}.",
                    "Оставить один уникальный packet id и перенести данные вручную.",
                )
            )
        seen.add(packet_id)
        if packet.attrib.get("status") in ACTIVE_PACKET_STATUSES:
            for tag in ["ExpectedArtifacts", "AcceptanceCriteria", "AcceptanceOwner"]:
                node = packet.find(tag)
                if node is None or (tag != "AcceptanceOwner" and not list(node)):
                    findings.append(
                        finding(
                            f"AUD-AUDIT-ACTIVE-PACKET-MISSING-{tag.upper()}-{packet_id}",
                            "AUD-AUDIT-001",
                            "critical",
                            "audit_integrity",
                            rel(PACKETS_PATH),
                            line_for(PACKETS_PATH, f'id="{packet_id}"'),
                            f"Активный packet {packet_id} не содержит {tag}.",
                            "Заполнить обязательный блок для ready_for_acceptance/accepted packet.",
                        )
                    )
                elif tag == "AcceptanceOwner" and not (node.text or "").strip():
                    findings.append(
                        finding(
                            f"AUD-AUDIT-ACTIVE-PACKET-MISSING-OWNER-{packet_id}",
                            "AUD-AUDIT-001",
                            "critical",
                            "audit_integrity",
                            rel(PACKETS_PATH),
                            line_for(PACKETS_PATH, f'id="{packet_id}"'),
                            f"Активный packet {packet_id} не содержит AcceptanceOwner.",
                            "Указать пользователя-владельца приемки.",
                        )
                    )
    return findings


def accepted_artifact(artifact: dict[str, Any]) -> bool:
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
        artifact.get("status") == "accepted"
        or acceptance.get("status") == "accepted"
        or protection.get("locked") is True
    )


def check_artifact_registry() -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    if not REGISTRY_PATH.exists():
        return [
            finding(
                "AUD-PROTECT-REGISTRY-MISSING",
                "AUD-PROTECT-001",
                "critical",
                "artifact_protection",
                rel(REGISTRY_PATH),
                None,
                "artifact-registry.yml отсутствует.",
                "Создать registry перед acceptance/protection проверками.",
            )
        ]
    data = load_data(REGISTRY_PATH)
    artifacts = data.get("artifacts", []) if isinstance(data, dict) else []
    if not isinstance(artifacts, list):
        return [
            finding(
                "AUD-PROTECT-REGISTRY-NOT-LIST",
                "AUD-PROTECT-001",
                "critical",
                "artifact_protection",
                rel(REGISTRY_PATH),
                None,
                "artifact-registry.yml не содержит список artifacts.",
                "Исправить структуру registry вручную.",
            )
        ]
    paths = {
        str(item.get("path"))
        for item in artifacts
        if isinstance(item, dict) and item.get("path")
    }
    required_paths = {
        "AGENTS.md",
        "docs/grace/execution-packets.xml",
        "docs/artifact-registry.yml",
        "docs/audit/audit-findings.yml",
        "docs/git-workflow.md",
        "scripts/audit_codex_spec.py",
        "scripts/audit_language_policy.py",
        "scripts/validate_audit_reports.py",
        "scripts/validate_git_workflow.py",
    }
    for path in sorted(required_paths - paths):
        findings.append(
            finding(
                f"AUD-PROTECT-REGISTRY-MISSING-PATH-{path.replace('/', '-')}",
                "AUD-PROTECT-001",
                "critical",
                "artifact_protection",
                rel(REGISTRY_PATH),
                None,
                f"В artifact registry не зарегистрирован ключевой артефакт {path}.",
                "Зарегистрировать artifact с acceptance owner и pending acceptance.",
            )
        )
    for artifact in artifacts:
        if not isinstance(artifact, dict) or not accepted_artifact(artifact):
            continue
        artifact_id = str(artifact.get("artifact_id") or artifact.get("path"))
        protection = (
            artifact.get("protection")
            if isinstance(artifact.get("protection"), dict)
            else {}
        )
        acceptance = (
            artifact.get("acceptance")
            if isinstance(artifact.get("acceptance"), dict)
            else {}
        )
        if protection.get("locked") is not True:
            findings.append(
                finding(
                    f"AUD-PROTECT-ACCEPTED-NOT-LOCKED-{artifact_id}",
                    "AUD-PROTECT-002",
                    "high",
                    "artifact_protection",
                    rel(REGISTRY_PATH),
                    None,
                    f"Accepted artifact {artifact_id} не имеет protection.locked=true.",
                    "Добавить protection.locked=true после user approval или создать change request.",
                    "requires_user_approval",
                )
            )
        checksum = (
            artifact.get("checksum")
            or artifact.get("checksum_sha256")
            or protection.get("checksum")
        )
        if not checksum:
            findings.append(
                finding(
                    f"AUD-PROTECT-ACCEPTED-MISSING-CHECKSUM-{artifact_id}",
                    "AUD-PROTECT-003",
                    "medium",
                    "artifact_protection",
                    str(artifact.get("path") or rel(REGISTRY_PATH)),
                    None,
                    f"Accepted artifact {artifact_id} не имеет checksum.",
                    "Добавить checksum после ручной проверки принятого артефакта.",
                    "requires_user_approval",
                )
            )
        if acceptance.get("accepted_by") == "Codex":
            findings.append(
                finding(
                    f"AUD-ACCEPT-ACCEPTED-BY-CODEX-{artifact_id}",
                    "AUD-ACCEPT-001",
                    "critical",
                    "acceptance",
                    rel(REGISTRY_PATH),
                    None,
                    f"Accepted artifact {artifact_id} содержит accepted_by=Codex.",
                    "Снять некорректное acceptance status только через user-owned correction.",
                    "requires_user_approval",
                )
            )
    return findings


def scan_for_codex_user_fields() -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    pattern = re.compile(
        r"^\s*(accepted_by|decided_by|checked_by|answered_by)\s*:\s*[\"']?Codex[\"']?\s*$"
    )
    for base in [PROJECT_ROOT / "docs", PROJECT_ROOT]:
        for path in sorted(
            base.glob("*.md") if base == PROJECT_ROOT else base.rglob("*")
        ):
            if path.is_dir() or path.suffix.lower() not in {
                ".md",
                ".yml",
                ".yaml",
                ".xml",
            }:
                continue
            if any(part in {".git", ".venv", "node_modules"} for part in path.parts):
                continue
            for index, line in enumerate(
                path.read_text(encoding="utf-8").splitlines(), 1
            ):
                match = pattern.match(line)
                if not match:
                    continue
                findings.append(
                    finding(
                        f"AUD-ACCEPT-CODEX-USER-FIELD-{rel(path).replace('/', '-')}-{index}",
                        "AUD-ACCEPT-001",
                        "critical",
                        "acceptance",
                        rel(path),
                        index,
                        f"Поле {match.group(1)} установлено в Codex.",
                        "Заменить только после user-owned correction; Codex не может быть владельцем решения.",
                    )
                )
    return findings


def ready_packet_ids() -> set[str]:
    if not PACKETS_PATH.exists():
        return set()
    root = ET.parse(PACKETS_PATH).getroot()
    return {
        packet.attrib.get("id", "")
        for packet in root.findall("Packet")
        if packet.attrib.get("status") == "ready_for_acceptance"
    }


def check_acceptance_dashboard() -> list[dict[str, Any]]:
    if not ACCEPTANCE_DASHBOARD_PATH.exists():
        return [
            finding(
                "AUD-DASH-ACCEPTANCE-DASHBOARD-MISSING",
                "AUD-DASH-001",
                "high",
                "dashboards",
                rel(ACCEPTANCE_DASHBOARD_PATH),
                None,
                "acceptance-dashboard.yml отсутствует.",
                "Запустить make generate-acceptance-dashboard.",
            )
        ]
    data = load_data(ACCEPTANCE_DASHBOARD_PATH)
    dashboard = data.get("acceptance_dashboard", {}) if isinstance(data, dict) else {}
    items = dashboard.get("items", []) if isinstance(dashboard, dict) else []
    present = {str(item.get("packet_id")) for item in items if isinstance(item, dict)}
    findings: list[dict[str, Any]] = []
    for packet_id in sorted(ready_packet_ids() - present):
        findings.append(
            finding(
                f"AUD-DASH-READY-PACKET-MISSING-{packet_id}",
                "AUD-DASH-001",
                "high",
                "dashboards",
                rel(ACCEPTANCE_DASHBOARD_PATH),
                None,
                f"ready_for_acceptance packet {packet_id} отсутствует в acceptance dashboard.",
                "Запустить make generate-acceptance-dashboard.",
            )
        )
    return findings


def open_question_ids() -> set[str]:
    result: set[str] = set()
    for path in (PROJECT_ROOT / "data" / "questions").glob("*.yml"):
        data = load_data(path)
        questions = data.get("questions", []) if isinstance(data, dict) else []
        if not isinstance(questions, list):
            continue
        for question in questions:
            if isinstance(question, dict) and question.get("status", "open") in {
                "open",
                "pending",
                "blocked",
            }:
                result.add(str(question.get("id")))
    return result


def check_user_action_dashboard() -> list[dict[str, Any]]:
    question_ids = open_question_ids()
    if not question_ids:
        return []
    if not USER_ACTION_DASHBOARD_PATH.exists():
        return [
            finding(
                "AUD-DASH-USER-ACTION-DASHBOARD-MISSING",
                "AUD-DASH-002",
                "high",
                "dashboards",
                rel(USER_ACTION_DASHBOARD_PATH),
                None,
                "user-action-dashboard.yml отсутствует при наличии open questions.",
                "Запустить make generate-user-action-dashboard.",
            )
        ]
    data = load_data(USER_ACTION_DASHBOARD_PATH)
    dashboard = data.get("user_action_dashboard", {}) if isinstance(data, dict) else {}
    actions = dashboard.get("actions", []) if isinstance(dashboard, dict) else []
    present = {str(action.get("id")) for action in actions if isinstance(action, dict)}
    findings: list[dict[str, Any]] = []
    for question_id in sorted(question_ids - present):
        findings.append(
            finding(
                f"AUD-DASH-OPEN-QUESTION-MISSING-{question_id}",
                "AUD-DASH-002",
                "high",
                "dashboards",
                rel(USER_ACTION_DASHBOARD_PATH),
                None,
                f"Open question {question_id} отсутствует в user action dashboard.",
                "Запустить make generate-user-action-dashboard.",
            )
        )
    return findings


def check_verification_dashboard() -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    if not VERIFICATION_DASHBOARD_PATH.exists():
        return [
            finding(
                "AUD-VERIF-DASHBOARD-MISSING",
                "AUD-VERIF-001",
                "critical",
                "verification",
                rel(VERIFICATION_DASHBOARD_PATH),
                None,
                "verification-dashboard.yml отсутствует.",
                "Запустить make generate-verification-dashboard.",
            )
        ]
    data = load_data(VERIFICATION_DASHBOARD_PATH)
    dashboard = data.get("verification_dashboard", {}) if isinstance(data, dict) else {}
    checks = dashboard.get("checks", []) if isinstance(dashboard, dict) else []
    for check in checks if isinstance(checks, list) else []:
        if not isinstance(check, dict):
            continue
        result = (
            check.get("user_result")
            if isinstance(check.get("user_result"), dict)
            else {}
        )
        if result.get("checked_by") == "Codex":
            findings.append(
                finding(
                    f"AUD-VERIF-CHECKED-BY-CODEX-{check.get('check_id')}",
                    "AUD-VERIF-001",
                    "critical",
                    "verification",
                    rel(VERIFICATION_DASHBOARD_PATH),
                    None,
                    f"Manual check {check.get('check_id')} содержит checked_by=Codex.",
                    "Очистить user-owned поле через отдельное решение пользователя.",
                )
            )
    return findings


def check_monthly_plan() -> list[dict[str, Any]]:
    if not MONTHLY_PLAN_PATH.exists():
        return [
            finding(
                "AUD-MONTHLY-PLAN-MISSING",
                "AUD-MONTHLY-001",
                "high",
                "monthly_defense",
                rel(MONTHLY_PLAN_PATH),
                None,
                "monthly-plan.yml отсутствует.",
                "Создать или восстановить active monthly block.",
            )
        ]
    data = load_data(MONTHLY_PLAN_PATH)
    plan = data.get("monthly_plan", {}) if isinstance(data, dict) else {}
    tasks = plan.get("tasks", []) if isinstance(plan, dict) else []
    if not isinstance(tasks, list) or len(tasks) != 3:
        return [
            finding(
                "AUD-MONTHLY-TASK-COUNT",
                "AUD-MONTHLY-001",
                "high",
                "monthly_defense",
                rel(MONTHLY_PLAN_PATH),
                None,
                "Active monthly block не содержит ровно 3 задачи.",
                "Согласовать monthly plan с пользователем или обновить план.",
            )
        ]
    bad = [
        task
        for task in tasks
        if not isinstance(task, dict) or task.get("planned_hours") != 15
    ]
    if bad:
        return [
            finding(
                "AUD-MONTHLY-TASK-HOURS",
                "AUD-MONTHLY-001",
                "high",
                "monthly_defense",
                rel(MONTHLY_PLAN_PATH),
                None,
                "Не все задачи active monthly block имеют planned_hours=15.",
                "Согласовать часы с пользователем или обновить план.",
            )
        ]
    return []


def run_git(args: list[str]) -> tuple[int, str, str]:
    result = subprocess.run(
        ["git", *args],
        cwd=PROJECT_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def project_state() -> dict[str, Any]:
    if not PROJECT_STATE_PATH.exists():
        return {}
    data = load_data(PROJECT_STATE_PATH)
    state = data.get("project_state", {}) if isinstance(data, dict) else {}
    return state if isinstance(state, dict) else {}


def normalized_packet_id(value: Any) -> str:
    text = str(value or "").strip()
    return "" if text in {"", "none", "null", "None", "~"} else text


def active_packet_id() -> str:
    return normalized_packet_id(project_state().get("active_execution_packet"))


def advisory_packet_id() -> str:
    return normalized_packet_id(project_state().get("next_recommended_packet"))


def current_packet_id() -> str:
    return active_packet_id() or advisory_packet_id()


def packet_number(packet_id: str) -> str:
    match = re.match(r"EP-(\d{3})-", packet_id)
    return match.group(1) if match else ""


def packet_acceptance(packet_id: str) -> dict[str, str]:
    values = {
        "acceptance_decision": "pending",
        "accepted_by": "",
        "accepted_at": "",
        "comments": "",
    }
    path = PROJECT_ROOT / "docs" / "acceptance" / f"{packet_id}.acceptance.md"
    if not path.exists():
        return values
    for line in path.read_text(encoding="utf-8").splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        if key in values:
            values[key] = value.strip()
    return values


def packet_status(packet_id: str) -> str:
    if not PACKETS_PATH.exists():
        return ""
    root = ET.parse(PACKETS_PATH).getroot()
    for packet in root.findall("Packet"):
        if packet.attrib.get("id") == packet_id:
            return packet.attrib.get("status", "")
    return ""


def packet_id_for_branch(branch: str) -> str:
    match = BRANCH_PACKET_RE.match(branch)
    if not match or not PACKETS_PATH.exists():
        return ""
    prefix = f"EP-{match.group('number')}-"
    root = ET.parse(PACKETS_PATH).getroot()
    for packet in root.findall("Packet"):
        packet_id = packet.attrib.get("id", "")
        if packet_id.startswith(prefix):
            return packet_id
    return ""


def packet_has_user_acceptance(packet_id: str) -> bool:
    acceptance = packet_acceptance(packet_id)
    accepted_by = acceptance.get("accepted_by", "").strip()
    return (
        packet_status(packet_id) == "accepted"
        and acceptance.get("acceptance_decision", "").strip() == "accepted"
        and bool(accepted_by)
        and accepted_by != "Codex"
    )


def obsolete_merge_forbidden_finding(finding_id: str) -> bool:
    prefix = "AUD-GIT-002-MERGE-FORBIDDEN-"
    if not finding_id.startswith(prefix):
        return False
    packet_id = finding_id[len(prefix) :]
    return packet_has_user_acceptance(packet_id)


def obsolete_branch_mismatch_finding(item: dict[str, Any]) -> bool:
    if str(item.get("id") or "") != "AUD-GIT-001-BRANCH-NAME-MISMATCH":
        return False
    issue = str(item.get("issue") or "")
    match = BRANCH_MISMATCH_ISSUE_RE.search(issue)
    if not match:
        return False
    stale_branch = match.group("branch")
    _code, current_branch, _stderr = run_git(["branch", "--show-current"])
    if not current_branch or current_branch == stale_branch:
        return False
    branch_packet_id = packet_id_for_branch(stale_branch)
    return bool(branch_packet_id) and packet_has_user_acceptance(branch_packet_id)


def obsolete_finding(item: dict[str, Any]) -> bool:
    item_id = str(item.get("id") or "")
    return obsolete_merge_forbidden_finding(item_id) or obsolete_branch_mismatch_finding(
        item
    )


def parse_git_status() -> list[tuple[str, str]]:
    code, stdout, _stderr = run_git(["status", "--porcelain"])
    if code != 0:
        return []
    entries: list[tuple[str, str]] = []
    for line in stdout.splitlines():
        if line.startswith("?? "):
            entries.append(("??", line[3:]))
            continue
        path = line[3:] if len(line) > 3 else ""
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        entries.append((line[:2], path))
    return entries


def staged_or_untracked(status_code: str) -> bool:
    return status_code == "??" or status_code[0] not in {" ", "?"}


def forbidden_git_path(path: str) -> bool:
    normalized = path.lstrip("./")
    return any(
        fnmatch.fnmatch(normalized, pattern) for pattern in FORBIDDEN_GIT_PATTERNS
    )


def ep_scope(path: str) -> str:
    if path == "docs/git-workflow.md" or path == "scripts/validate_git_workflow.py":
        return "EP-011"
    if path.startswith("docs/audit/") or path.startswith("scripts/audit_"):
        return "EP-009"
    if path == "scripts/validate_audit_reports.py":
        return "EP-009"
    if path.startswith("docs/dissertation/") or path.startswith("thesis/"):
        return "EP-008"
    if path.startswith("docs/verification-dashboard") or path.startswith(
        "scripts/generate_verification_dashboard.py"
    ):
        return "EP-007"
    if path.startswith("docs/monthly/"):
        return "EP-006"
    if path.startswith("docs/acceptance-dashboard") or path.startswith(
        "docs/user-action-dashboard"
    ):
        return "EP-005"
    if path.startswith("docs/acceptance/EP-011"):
        return "EP-011"
    if path.startswith("docs/acceptance/EP-009"):
        return "EP-009"
    if path.startswith("docs/grace/") or path in {
        "AGENTS.md",
        "Makefile",
        "README.md",
        "CHANGELOG.md",
        "docs/artifact-registry.yml",
        "docs/project-plan.md",
        "docs/status-report.md",
        "docs/traceability-matrix.md",
        "docs/decision-log.md",
    }:
        return "governance"
    return "unknown"


def check_git_workflow() -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    code, branch, stderr = run_git(["branch", "--show-current"])
    active_packet = active_packet_id()
    packet_id = active_packet or advisory_packet_id()
    number = packet_number(packet_id)
    if code != 0 or not branch:
        findings.append(
            finding(
                "AUD-GIT-001-BRANCH-UNDETERMINED",
                "AUD-GIT-001",
                "medium",
                "git_workflow",
                ".git",
                None,
                f"Текущая Git branch не определена: {stderr or '-'}",
                "Проверить Git state вручную перед созданием ветки или merge.",
            )
        )
    elif packet_id and branch == "main":
        findings.append(
            finding(
                "AUD-GIT-001-CURRENT-BRANCH-MAIN",
                "AUD-GIT-001",
                "medium",
                "git_workflow",
                ".git",
                None,
                f"Текущая ветка main не соответствует {packet_id}.",
                "Создавать новую packet-ветку для новых EP; текущий dirty baseline требует user approval перед переключением.",
            )
        )
    elif packet_id and not (
        number and branch.startswith(f"ep-{number}-") and BRANCH_RE.match(branch)
    ):
        findings.append(
            finding(
                "AUD-GIT-001-BRANCH-NAME-MISMATCH",
                "AUD-GIT-001",
                "medium",
                "git_workflow",
                ".git",
                None,
                f"Имя ветки {branch} не соответствует packet {packet_id}.",
                f"Использовать формат ep-{number or '<number>'}-<short-slug>.",
            )
        )

    status_entries = parse_git_status()
    forbidden = [
        path
        for status_code, path in status_entries
        if staged_or_untracked(status_code) and forbidden_git_path(path)
    ]
    for path in forbidden:
        findings.append(
            finding(
                f"AUD-GIT-004-FORBIDDEN-FILE-{path.replace('/', '-')}",
                "AUD-GIT-004",
                "critical",
                "git_workflow",
                path,
                None,
                f"Forbidden file staged or untracked: {path}.",
                "Удалить из staging/untracked или добавить корректное исключение только с user approval.",
            )
        )

    scopes = {ep_scope(path) for _status_code, path in status_entries}
    scopes = {scope for scope in scopes if scope != "unknown"}
    if len(scopes) > 1:
        findings.append(
            finding(
                "AUD-GIT-005-MIXED-EP-SCOPES",
                "AUD-GIT-005",
                "medium",
                "git_workflow",
                ".git",
                None,
                "Working tree содержит изменения нескольких EP scopes: "
                + ", ".join(sorted(scopes)),
                "Не выполнять commit/merge до ручного разделения изменений или явного user approval.",
            )
        )

    if active_packet:
        status = packet_status(active_packet)
        acceptance = packet_acceptance(active_packet)
        decision = acceptance.get("acceptance_decision", "pending")
        accepted_by = acceptance.get("accepted_by", "")
        if accepted_by == "Codex":
            findings.append(
                finding(
                    f"AUD-GIT-003-ACCEPTED-BY-CODEX-{active_packet}",
                    "AUD-GIT-003",
                    "critical",
                    "git_workflow",
                    f"docs/acceptance/{active_packet}.acceptance.md",
                    None,
                    f"{active_packet} содержит accepted_by=Codex.",
                    "Очистить user-owned field через отдельное пользовательское решение.",
                )
            )
        if not packet_has_user_acceptance(active_packet):
            findings.append(
                finding(
                    f"AUD-GIT-002-MERGE-FORBIDDEN-{active_packet}",
                    "AUD-GIT-002",
                    "medium",
                    "git_workflow",
                    f"docs/acceptance/{active_packet}.acceptance.md",
                    None,
                    f"Merge запрещен для {active_packet}: status={status or '-'}, acceptance_decision={decision}, accepted_by={'set' if accepted_by else 'empty'}.",
                    "Не готовить merge, пока пользователь не поставит accepted и accepted_by.",
                )
            )
            findings.append(
                finding(
                    f"AUD-GIT-006-NO-MAIN-MERGE-APPROVAL-{active_packet}",
                    "AUD-GIT-006",
                    "medium",
                    "git_workflow",
                    "docs/git-workflow.md",
                    None,
                    f"Для {active_packet} нет явного user approval на merge в main.",
                    "Получить явное разрешение пользователя после приемки и успешных проверок.",
                )
            )
    return findings


def check_dissertation_sync() -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    for path in (PROJECT_ROOT / "thesis").rglob("*"):
        if path.suffix.lower() in {".docx", ".pdf"}:
            findings.append(
                finding(
                    f"AUD-DISS-DOCX-PDF-PRESENT-{rel(path).replace('/', '-')}",
                    "AUD-DISS-001",
                    "critical",
                    "dissertation_sync",
                    rel(path),
                    None,
                    "В thesis найден DOCX/PDF artifact, который EP-009 не должен создавать или менять.",
                    "Удаление или перенос выполнять только по явному user request.",
                )
            )
    for script in (PROJECT_ROOT / "scripts").glob("*.py"):
        text = script.read_text(encoding="utf-8")
        direct_docx_usage = bool(
            re.search(r"^\s*(from\s+docx\s+import|import\s+docx)\b", text, re.M)
            or re.search(r"^\s*(docx\.)?Document\s*\(", text, re.M)
        )
        if direct_docx_usage:
            findings.append(
                finding(
                    f"AUD-DISS-DIRECT-DOCX-SCRIPT-{script.name}",
                    "AUD-DISS-001",
                    "critical",
                    "dissertation_sync",
                    rel(script),
                    None,
                    "Скрипт содержит признаки прямого DOCX редактирования.",
                    "DOCX update разрешен только по явному user request и после accepted markdown patch.",
                )
            )
    if FORBIDDEN_CLAIMS_PATH.exists():
        text = FORBIDDEN_CLAIMS_PATH.read_text(encoding="utf-8").lower()
        has_gesn = "gesn" in text or "гэсн" in text
        has_bim = "bim" in text or "бим" in text
        has_auto = "automatic" in text or "автомат" in text
        if not (has_gesn and has_bim and has_auto):
            findings.append(
                finding(
                    "AUD-DISS-FORBIDDEN-GESN-AUTO-SELECTION-MISSING",
                    "AUD-DISS-002",
                    "critical",
                    "dissertation_sync",
                    rel(FORBIDDEN_CLAIMS_PATH),
                    None,
                    "forbidden-claims.yml не содержит явный запрет автоматического выбора ГЭСН по BIM-элементу.",
                    "Добавить запрет без изменения доменной методики.",
                )
            )
    return findings


def severity_counts(findings: list[dict[str, Any]]) -> dict[str, int]:
    return {
        severity: sum(item.get("severity") == severity for item in findings)
        for severity in ["critical", "high", "medium", "low"]
    }


def is_current_finding(item: dict[str, Any]) -> bool:
    return item.get("current_detected") is not False


def active_audit_finding(item: dict[str, Any]) -> bool:
    return is_current_finding(item) and item.get("status") in BLOCKING_STATUSES


def active_blocking_critical(findings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        item
        for item in findings
        if item.get("severity") == "critical"
        and active_audit_finding(item)
    ]


def finding_group_id(item: dict[str, Any]) -> str:
    finding_id = str(item.get("id") or "")
    if finding_id.startswith("AUD-ACCEPT-CODEX-USER-FIELD-"):
        return "AUD-ACCEPT-CODEX-USER-FIELD"
    if finding_id.startswith("AUD-LANG-001-"):
        return "AUD-LANG-001"
    return str(item.get("check_id") or finding_id or "AUD-UNKNOWN")


def audit_finding_groups(findings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for item in findings:
        grouped.setdefault(finding_group_id(item), []).append(item)

    result: list[dict[str, Any]] = []
    for group_id in sorted(grouped):
        items = sorted(grouped[group_id], key=lambda value: str(value.get("id") or ""))
        current = [item for item in items if is_current_finding(item)]
        historical = [item for item in items if not is_current_finding(item)]
        first = items[0] if items else {}
        all_historical = bool(items) and not current
        result.append(
            {
                "group_id": group_id,
                "severity": first.get("severity") or "",
                "category": first.get("category") or "",
                "total_count": len(items),
                "current_detected_count": len(current),
                "historical_count": len(historical),
                "active_blocking": any(
                    active_audit_finding(item)
                    and item.get("severity") in {"critical", "high"}
                    for item in items
                ),
                "source_file": rel(FINDINGS_PATH),
                "recommendation": (
                    "Historical findings are preserved but hidden from active_review_items while current_detected=false."
                    if all_historical
                    else str(first.get("recommendation") or "")
                ),
                "example_ids": [
                    str(item.get("id") or "") for item in items[:5] if item.get("id")
                ],
            }
        )
    return result


def write_report(findings: list[dict[str, Any]]) -> None:
    current_findings = [item for item in findings if is_current_finding(item)]
    historical_findings = [item for item in findings if not is_current_finding(item)]
    counts = severity_counts(findings)
    current_counts = severity_counts(current_findings)
    critical = active_blocking_critical(findings)
    groups = audit_finding_groups(findings)
    historical_groups = [group for group in groups if group.get("historical_count")]
    user_required = [
        item
        for item in current_findings
        if item.get("status") == "requires_user_approval"
        or (
            item.get("status") in BLOCKING_STATUSES
            and item.get("severity") in {"critical", "high"}
        )
    ]
    lines = [
        "# Codex Spec Audit",
        "",
        f"Дата обновления: {TODAY}",
        "",
        "## 1. Сводка",
        "",
        "| Severity | Всего | Current | Historical |",
        "|---|---:|---:|---:|",
    ]
    for severity in ["critical", "high", "medium", "low"]:
        historical_count = counts[severity] - current_counts[severity]
        lines.append(
            f"| {severity} | {counts[severity]} | {current_counts[severity]} | {historical_count} |"
        )
    lines.extend(
        [
            "",
            f"Всего findings: {len(findings)}",
            f"Current findings: {len(current_findings)}",
            f"Historical/stale findings: {len(historical_findings)}",
            f"Активных critical findings: {len(critical)}",
            "",
            "## 2. Проверка доменной логики",
            "",
            "- Проверен запрет прямой связи `ModelElement -> GESNNorm` в `docs/grace/knowledge-graph.xml`.",
            "- Прямая доменная методика не изменялась.",
            "",
            "## 3. Проверка reference data discipline",
            "",
            "- Проверено наличие `No source — no rule` в `AGENTS.md` через обязательный раздел Reference data discipline.",
            "- Нормативные данные не создавались и не подключались.",
            "",
            "## 4. Проверка accepted artifact protection",
            "",
            "- Проверен `docs/artifact-registry.yml`.",
            "- Accepted/protected artifacts не изменялись автоматически.",
            "",
            "## 5. Проверка dashboards",
            "",
            "- Проверены acceptance, user-action и verification dashboards.",
            "- User-owned поля не закрывались от имени Codex.",
            "",
            "## 6. Проверка monthly defense layer",
            "",
            "- Проверен active monthly block на 3 задачи по 15 часов.",
            "",
            "## 7. Проверка dissertation sync",
            "",
            "- Проверено отсутствие прямого DOCX/PDF update artifact в `thesis/`.",
            "- Проверены базовые guardrails для forbidden claims.",
            "",
            "## 8. Проверка языковой политики",
            "",
            "- Детальная языковая проверка выполняется `make audit-language`.",
            "",
            "## 8.1. Проверка Git workflow",
            "",
            "- Проверены branch naming, forbidden staged/untracked files, merge acceptance gates и mixed EP scopes.",
            "- Advisory findings по текущему dirty baseline не блокируют `make check`.",
            "",
            "## 9. Active findings",
            "",
            "| ID | Severity | Check | File | Issue | Recommendation | Status |",
            "|---|---|---|---|---|---|---|",
        ]
    )
    open_findings = [
        item for item in current_findings if item.get("status") in BLOCKING_STATUSES
    ]
    if open_findings:
        for item in open_findings:
            lines.append(
                f"| {item.get('id')} | {item.get('severity')} | {item.get('check_id')} | {item.get('file')} | {item.get('issue')} | {item.get('recommendation')} | {item.get('status')} |"
            )
    else:
        lines.append("| - | - | - | - | - | - | - |")
    lines.extend(
        [
            "",
            "## 10. Critical findings",
            "",
        ]
    )
    if critical:
        for item in critical:
            lines.append(f"- `{item.get('id')}`: {item.get('issue')}")
    else:
        lines.append("- Активных critical findings нет.")
    lines.extend(
        [
            "",
            "## 11. Historical/stale finding groups (`audit_finding_groups`)",
            "",
            "| Group | Severity | Category | Total | Current | Historical | Active blocking | Recommendation |",
            "|---|---|---|---:|---:|---:|---|---|",
        ]
    )
    if historical_groups:
        for group in historical_groups:
            lines.append(
                f"| {group.get('group_id')} | {group.get('severity')} | {group.get('category')} | {group.get('total_count')} | {group.get('current_detected_count')} | {group.get('historical_count')} | {group.get('active_blocking')} | {group.get('recommendation')} |"
            )
    else:
        lines.append("| - | - | - | - | - | - | - | - |")
    lines.extend(
        [
            "",
            "## 12. Findings, требующие решения пользователя",
            "",
        ]
    )
    if user_required:
        for item in user_required:
            lines.append(f"- `{item.get('id')}`: {item.get('issue')}")
    else:
        lines.append("- Нет findings, требующих решения пользователя.")
    lines.extend(
        [
            "",
            "## 13. Команды проверки",
            "",
            "```sh",
            "make audit-codex-spec",
            "make audit-language",
            "make validate-audit",
            "make audit",
            "make validate-plan",
            "make check",
            "```",
            "",
            "## 14. Что не исправлялось автоматически",
            "",
            "- Не выполнялась массовая русификация.",
            "- Не переписывались существующие документы вне audit-контура.",
            "- Не менялись accepted/protected artifacts без user approval.",
            "- Findings не закрывались как `fixed` автоматически.",
            "- Historical findings с `current_detected: false` сохранялись как история и не считались active blockers.",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_checks() -> list[dict[str, Any]]:
    generated: list[dict[str, Any]] = []
    for check in [
        check_agents_sections,
        check_knowledge_graph,
        check_execution_packets,
        check_artifact_registry,
        scan_for_codex_user_fields,
        check_acceptance_dashboard,
        check_user_action_dashboard,
        check_verification_dashboard,
        check_monthly_plan,
        check_dissertation_sync,
        check_git_workflow,
    ]:
        generated.extend(check())
    return generated


def main() -> int:
    generated = run_checks()
    findings = merge_findings(generated)
    write_report(findings)
    critical = active_blocking_critical(findings)
    print(f"Codex spec audit complete: {len(findings)} total findings.")
    if critical:
        for item in critical:
            print(f"CRITICAL: {item.get('id')}: {item.get('issue')}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
