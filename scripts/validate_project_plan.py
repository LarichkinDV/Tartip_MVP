#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

from reference_utils import load_data
from validate_verification_dashboard import (
    validate_dashboard as validate_verification_dashboard_data,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = PROJECT_ROOT / "docs" / "artifact-registry.yml"
PACKETS_PATH = PROJECT_ROOT / "docs" / "grace" / "execution-packets.xml"
PROJECT_PLAN_PATH = PROJECT_ROOT / "docs" / "project-plan.md"
ACCEPTANCE_DIR = PROJECT_ROOT / "docs" / "acceptance"
ACCEPTANCE_DASHBOARD_MD = PROJECT_ROOT / "docs" / "acceptance-dashboard.md"
ACCEPTANCE_DASHBOARD_YML = PROJECT_ROOT / "docs" / "acceptance-dashboard.yml"
USER_ACTION_DASHBOARD_MD = PROJECT_ROOT / "docs" / "user-action-dashboard.md"
USER_ACTION_DASHBOARD_YML = PROJECT_ROOT / "docs" / "user-action-dashboard.yml"
VERIFICATION_DASHBOARD_MD = PROJECT_ROOT / "docs" / "verification-dashboard.md"
VERIFICATION_DASHBOARD_YML = PROJECT_ROOT / "docs" / "verification-dashboard.yml"
QUESTION_FILES = [
    PROJECT_ROOT / "data" / "questions" / "data-requirements.yml",
    PROJECT_ROOT / "data" / "questions" / "unresolved-mapping-questions.yml",
    PROJECT_ROOT / "data" / "questions" / "normative-review-questions.yml",
    PROJECT_ROOT / "data" / "questions" / "project-decisions.yml",
    PROJECT_ROOT / "data" / "questions" / "import-issues.yml",
]
NON_EXISTENT_STATUSES = {"planned", "blocked"}


def as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(PROJECT_ROOT))
    except ValueError:
        return str(path)


def load_registry() -> list[dict[str, Any]]:
    if not REGISTRY_PATH.exists():
        raise ValueError(f"Missing artifact registry: {rel(REGISTRY_PATH)}")
    data = load_data(REGISTRY_PATH)
    artifacts = data.get("artifacts", []) if isinstance(data, dict) else []
    if not isinstance(artifacts, list):
        raise ValueError("docs/artifact-registry.yml must contain an artifacts list")
    return [artifact for artifact in artifacts if isinstance(artifact, dict)]


def acceptance_decision(report_path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not report_path.exists():
        return values
    for line in report_path.read_text(encoding="utf-8").splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        if key in {"acceptance_decision", "accepted_by", "accepted_at", "comments"}:
            values[key] = value.strip()
    return values


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
        or protection.get("protection_status") == "protected"
        or protection.get("locked") is True
    )


def load_dashboard(path: Path, root_key: str) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = load_data(path)
    if not isinstance(data, dict):
        return {}
    value = data.get(root_key, {})
    return value if isinstance(value, dict) else {}


def packet_acceptance_report(packet_id: str) -> Path:
    return ACCEPTANCE_DIR / f"{packet_id}.acceptance.md"


def validate_registry(artifacts: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    seen_paths: set[str] = set()
    for artifact in artifacts:
        artifact_id = artifact.get("artifact_id", "<missing artifact_id>")
        path_value = artifact.get("path")
        status = str(artifact.get("status") or "")
        if not path_value:
            errors.append(f"{artifact_id}: missing path")
            continue
        seen_paths.add(str(path_value))
        artifact_path = PROJECT_ROOT / str(path_value)
        if status not in NON_EXISTENT_STATUSES and not artifact_path.exists():
            errors.append(f"{artifact_id}: path does not exist: {path_value}")

        acceptance = artifact.get("acceptance") or {}
        if not isinstance(acceptance, dict):
            errors.append(f"{artifact_id}: acceptance block must be a mapping")
            continue
        if acceptance.get("accepted_by") == "Codex":
            errors.append(f"{artifact_id}: accepted_by must not be Codex")
        if acceptance.get("status") == "accepted" and not acceptance.get("accepted_by"):
            errors.append(f"{artifact_id}: accepted artifact must have accepted_by")
        protection = (
            artifact.get("protection")
            if isinstance(artifact.get("protection"), dict)
            else {}
        )
        if is_accepted_artifact(artifact):
            if not artifact_path.exists():
                errors.append(
                    f"{artifact_id}: accepted artifact has missing path: {path_value}"
                )
            if not (
                protection.get("locked") is True
                or protection.get("protection_status") == "protected"
            ):
                errors.append(
                    f"{artifact_id}: accepted artifact requires protection_status=protected"
                )
            if (
                protection.get("protection_status") == "protected"
                and protection.get("change_requires_user_approval") is not True
            ):
                errors.append(
                    f"{artifact_id}: protected artifact requires change_requires_user_approval=true"
                )
            if acceptance.get("accepted_by") == "Codex":
                errors.append(
                    f"{artifact_id}: accepted artifact must not have accepted_by=Codex"
                )
        if acceptance.get("required") is True:
            report_value = acceptance.get("acceptance_report")
            if not report_value:
                errors.append(
                    f"{artifact_id}: acceptance.required=true requires acceptance_report"
                )
            elif not (PROJECT_ROOT / str(report_value)).exists():
                errors.append(
                    f"{artifact_id}: acceptance_report does not exist: {report_value}"
                )
    return errors


def validate_packets(registered_paths: set[str]) -> list[str]:
    errors: list[str] = []
    if not PACKETS_PATH.exists():
        return [f"Missing execution packets file: {rel(PACKETS_PATH)}"]
    root = ET.parse(PACKETS_PATH).getroot()
    for packet in root.findall("Packet"):
        packet_id = packet.attrib.get("id", "<missing id>")
        status = packet.attrib.get("status", "")
        report = packet_acceptance_report(packet_id)
        criteria = packet.find("AcceptanceCriteria")
        expected = packet.find("ExpectedArtifacts")
        if status == "accepted":
            if not report.exists():
                errors.append(
                    f"{packet_id}: accepted packet requires acceptance report"
                )
            decision = acceptance_decision(report)
            if decision.get("acceptance_decision") != "accepted":
                errors.append(
                    f"{packet_id}: accepted packet requires acceptance_decision=accepted"
                )
        if status == "ready_for_acceptance" and (
            criteria is None or not list(criteria)
        ):
            errors.append(
                f"{packet_id}: ready_for_acceptance packet requires AcceptanceCriteria"
            )
        if expected is not None:
            for artifact_node in expected.findall("Artifact"):
                path = (artifact_node.text or "").strip()
                if path and path not in registered_paths:
                    errors.append(
                        f"{packet_id}: expected artifact is not registered in artifact-registry.yml: {path}"
                    )
    return errors


def validate_project_plan_links() -> list[str]:
    errors: list[str] = []
    if not PROJECT_PLAN_PATH.exists():
        return [f"Missing project plan: {rel(PROJECT_PLAN_PATH)}"]
    text = PROJECT_PLAN_PATH.read_text(encoding="utf-8")
    for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
        if re.match(r"^[a-z]+://", target) or target.startswith("#"):
            continue
        clean_target = target.split("#", 1)[0].strip()
        if not clean_target:
            continue
        if clean_target.startswith("../"):
            target_path = (PROJECT_PLAN_PATH.parent / clean_target).resolve()
        elif clean_target.startswith("docs/"):
            target_path = PROJECT_ROOT / clean_target
        else:
            target_path = PROJECT_PLAN_PATH.parent / clean_target
        if not target_path.exists():
            errors.append(f"docs/project-plan.md link target does not exist: {target}")
    return errors


def local_markdown_links(path: Path) -> list[Path]:
    if not path.exists():
        return []
    targets: list[Path] = []
    for target in re.findall(
        r"\[[^\]]+\]\(([^)]+)\)", path.read_text(encoding="utf-8")
    ):
        if re.match(r"^[a-z]+://", target) or target.startswith("#"):
            continue
        clean_target = target.split("#", 1)[0].strip()
        if not clean_target:
            continue
        if clean_target.startswith("../"):
            targets.append((path.parent / clean_target).resolve())
        elif clean_target.startswith("docs/"):
            targets.append(PROJECT_ROOT / clean_target)
        else:
            targets.append(path.parent / clean_target)
    return targets


def validate_dashboard_links() -> list[str]:
    errors: list[str] = []
    for markdown_path in [
        ACCEPTANCE_DASHBOARD_MD,
        USER_ACTION_DASHBOARD_MD,
        VERIFICATION_DASHBOARD_MD,
    ]:
        for target_path in local_markdown_links(markdown_path):
            if not target_path.exists():
                errors.append(
                    f"{rel(markdown_path)} link target does not exist: {rel(target_path)}"
                )
    return errors


def ready_for_acceptance_packets() -> set[str]:
    if not PACKETS_PATH.exists():
        return set()
    root = ET.parse(PACKETS_PATH).getroot()
    return {
        packet.attrib.get("id", "")
        for packet in root.findall("Packet")
        if packet.attrib.get("status") == "ready_for_acceptance"
    }


def validate_acceptance_dashboard() -> list[str]:
    errors: list[str] = []
    for path in [ACCEPTANCE_DASHBOARD_MD, ACCEPTANCE_DASHBOARD_YML]:
        if not path.exists():
            errors.append(f"Missing acceptance dashboard file: {rel(path)}")
    dashboard = load_dashboard(ACCEPTANCE_DASHBOARD_YML, "acceptance_dashboard")
    if not dashboard:
        return errors
    items = dashboard.get("items", [])
    if not isinstance(items, list):
        errors.append(
            "docs/acceptance-dashboard.yml must contain acceptance_dashboard.items list"
        )
        return errors
    item_packet_ids = {
        str(item.get("packet_id")) for item in items if isinstance(item, dict)
    }
    for packet_id in ready_for_acceptance_packets():
        if packet_id and packet_id not in item_packet_ids:
            errors.append(
                f"ready_for_acceptance packet missing from acceptance dashboard: {packet_id}"
            )
    dashboard_reports = {
        str(item.get("acceptance_report")) for item in items if isinstance(item, dict)
    }
    for report in ACCEPTANCE_DIR.glob("*.acceptance.md"):
        if rel(report) not in dashboard_reports:
            errors.append(
                f"acceptance report missing from acceptance dashboard: {rel(report)}"
            )
    for item in items:
        if not isinstance(item, dict):
            continue
        decision = item.get("acceptance_decision")
        user_decision = (
            item.get("user_decision")
            if isinstance(item.get("user_decision"), dict)
            else {}
        )
        decided_by = (
            user_decision.get("decided_by")
            or item.get("accepted_by")
            or item.get("decided_by")
        )
        if decided_by == "Codex":
            errors.append(
                f"{item.get('packet_id')}: decided_by/accepted_by must not be Codex"
            )
        if decision == "accepted" and not decided_by:
            errors.append(
                f"{item.get('packet_id')}: accepted decision requires decided_by or accepted_by"
            )
    return errors


def collect_open_questions() -> tuple[set[str], set[str]]:
    open_ids: set[str] = set()
    high_priority_ids: set[str] = set()
    for path in QUESTION_FILES:
        if not path.exists():
            continue
        data = load_data(path)
        questions = data.get("questions", []) if isinstance(data, dict) else []
        if not isinstance(questions, list):
            continue
        for question in questions:
            if not isinstance(question, dict) or not question.get("id"):
                continue
            status = str(question.get("status") or "open")
            question_id = str(question["id"])
            if status in {"open", "pending", "blocked"}:
                open_ids.add(question_id)
            if question.get("priority") == "high":
                high_priority_ids.add(question_id)
            for field_name in ["accepted_by", "decided_by", "answered_by"]:
                if question.get(field_name) == "Codex":
                    open_ids.add(question_id)
    return open_ids, high_priority_ids


def validate_user_action_dashboard(artifacts: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    for path in [USER_ACTION_DASHBOARD_MD, USER_ACTION_DASHBOARD_YML]:
        if not path.exists():
            errors.append(f"Missing user action dashboard file: {rel(path)}")
    dashboard = load_dashboard(USER_ACTION_DASHBOARD_YML, "user_action_dashboard")
    if not dashboard:
        return errors
    actions = dashboard.get("actions", [])
    if not isinstance(actions, list):
        errors.append(
            "docs/user-action-dashboard.yml must contain user_action_dashboard.actions list"
        )
        return errors
    action_ids = {
        str(action.get("id")) for action in actions if isinstance(action, dict)
    }
    open_ids, high_priority_ids = collect_open_questions()
    for question_id in open_ids:
        if question_id not in action_ids:
            errors.append(
                f"open question missing from user action dashboard: {question_id}"
            )
    markdown_text = (
        USER_ACTION_DASHBOARD_MD.read_text(encoding="utf-8")
        if USER_ACTION_DASHBOARD_MD.exists()
        else ""
    )
    for question_id in high_priority_ids:
        if question_id not in markdown_text:
            errors.append(
                f"high priority question missing from user-action-dashboard.md: {question_id}"
            )
    for action in actions:
        if not isinstance(action, dict):
            continue
        response = (
            action.get("response") if isinstance(action.get("response"), dict) else {}
        )
        if (
            response.get("answered_by") == "Codex"
            or action.get("decided_by") == "Codex"
        ):
            errors.append(
                f"{action.get('id')}: answered_by/decided_by must not be Codex"
            )
    action_types = {
        str(action.get("type")) for action in actions if isinstance(action, dict)
    }
    for artifact in artifacts:
        protection = (
            artifact.get("protection")
            if isinstance(artifact.get("protection"), dict)
            else {}
        )
        if is_accepted_artifact(artifact) and (
            protection.get("requires_change") is True
            or protection.get("change_requested") is True
        ):
            if not {"requires_user_approval", "change_request"} & action_types:
                errors.append(
                    f"{artifact.get('artifact_id')}: protected artifact change requires requires_user_approval action or change_request"
                )
    return errors


def validate_verification_dashboard() -> list[str]:
    errors: list[str] = []
    for path in [VERIFICATION_DASHBOARD_MD, VERIFICATION_DASHBOARD_YML]:
        if not path.exists():
            errors.append(f"Missing verification dashboard file: {rel(path)}")
    if errors:
        return errors
    errors.extend(validate_verification_dashboard_data(PROJECT_ROOT))
    return errors


def main() -> int:
    errors: list[str] = []
    try:
        artifacts = load_registry()
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    registered_paths = {
        str(artifact.get("path")) for artifact in artifacts if artifact.get("path")
    }
    errors.extend(validate_registry(artifacts))
    errors.extend(validate_packets(registered_paths))
    errors.extend(validate_project_plan_links())
    errors.extend(validate_acceptance_dashboard())
    errors.extend(validate_user_action_dashboard(artifacts))
    errors.extend(validate_verification_dashboard())
    errors.extend(validate_dashboard_links())

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Project plan validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
