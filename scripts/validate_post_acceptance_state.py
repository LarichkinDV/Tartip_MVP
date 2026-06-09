#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

from reference_utils import load_data


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ACCEPTANCE_DIR = PROJECT_ROOT / "docs" / "acceptance"
PACKETS_PATH = PROJECT_ROOT / "docs" / "grace" / "execution-packets.xml"
PROJECT_PLAN_PATH = PROJECT_ROOT / "docs" / "project-plan.md"
STATUS_REPORT_PATH = PROJECT_ROOT / "docs" / "status-report.md"
ACCEPTANCE_DASHBOARD_PATH = PROJECT_ROOT / "docs" / "acceptance-dashboard.yml"
WORKBENCH_PATH = PROJECT_ROOT / "docs" / "user-review-workbench.yml"
VERIFICATION_DASHBOARD_PATH = PROJECT_ROOT / "docs" / "verification-dashboard.yml"
USER_ACTION_DASHBOARD_PATH = PROJECT_ROOT / "docs" / "user-action-dashboard.yml"
AUDIT_FINDINGS_PATH = PROJECT_ROOT / "docs" / "audit" / "audit-findings.yml"

CURRENT_PACKET = "EP-013-POST-ACCEPTANCE-STATE-SYNC"
PREVIOUS_PACKET = "EP-012-USER-REVIEW-WORKBENCH-AND-ACCEPTANCE-STANDARD"
EXPECTED_ACCEPTED_PACKETS = {
    "EP-001-INFRA",
    "EP-002-REFERENCE-GOVERNANCE",
    "EP-003-REFERENCE-VERSIONING",
    "EP-004-PROJECT-PLANNING-AND-ACCEPTANCE",
    "EP-005-ACCEPTANCE-AND-USER-ACTION-DASHBOARDS",
    "EP-007-VERIFICATION-DASHBOARD",
    "EP-008-DISSERTATION-PROMPT-GENERATION",
    "EP-009-CODEX-SPEC-AUDIT",
    "EP-011-GIT-WORKFLOW-DISCIPLINE",
    PREVIOUS_PACKET,
}
HIGH_PRIORITY_ACTIONS = {
    "DR-REF-KSI-001",
    "DR-REF-FSNB-001",
    "DR-REF-WORK-TYPES-001",
    "NR-RULE-PARTITION-BRICK-120-REINF-001",
}
ALLOWED_AUDIT_STATUSES = {
    "open",
    "acknowledged",
    "fixed",
    "accepted_risk",
    "false_positive",
    "blocked",
    "requires_user_approval",
}


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(PROJECT_ROOT))
    except ValueError:
        return str(path)


def load_root(path: Path, root_key: str) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = load_data(path)
    if not isinstance(data, dict):
        return {}
    root = data.get(root_key, {})
    return root if isinstance(root, dict) else {}


def parse_acceptance_report(path: Path) -> dict[str, str]:
    values = {
        "acceptance_decision": "pending",
        "accepted_by": "",
        "accepted_at": "",
        "comments": "",
    }
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


def accepted_reports() -> set[str]:
    accepted: set[str] = set()
    for path in ACCEPTANCE_DIR.glob("EP-*.acceptance.md"):
        packet_id = path.name.removesuffix(".acceptance.md")
        decision = parse_acceptance_report(path)
        if (
            decision.get("acceptance_decision") == "accepted"
            and decision.get("accepted_by")
            and decision.get("accepted_by") != "Codex"
        ):
            accepted.add(packet_id)
    return accepted


def packet_statuses() -> dict[str, str]:
    if not PACKETS_PATH.exists():
        return {}
    root = ET.parse(PACKETS_PATH).getroot()
    return {
        str(packet.attrib.get("id")): str(packet.attrib.get("status") or "")
        for packet in root.findall("Packet")
    }


def validate_execution_packets(errors: list[str], accepted: set[str]) -> None:
    statuses = packet_statuses()
    for packet_id in sorted(accepted):
        if statuses.get(packet_id) != "accepted":
            errors.append(
                f"{packet_id}: accepted acceptance report is not reflected as accepted in execution-packets.xml"
            )
    if statuses.get(CURRENT_PACKET) != "ready_for_acceptance":
        errors.append(f"{CURRENT_PACKET}: expected status ready_for_acceptance")


def validate_planning_documents(errors: list[str], accepted: set[str]) -> None:
    for path in [PROJECT_PLAN_PATH, STATUS_REPORT_PATH]:
        if not path.exists():
            errors.append(f"Missing planning document: {rel(path)}")
            continue
        text = path.read_text(encoding="utf-8")
        for needle in [
            "project_state: accepted_baseline",
            f"active_execution_packet: {CURRENT_PACKET}",
            "next_recommended_packet: EP-014-ACCEPTED-ARTIFACT-PROTECTION",
            f"previous_active_execution_packet: {PREVIOUS_PACKET}",
            "EP-014-ACCEPTED-ARTIFACT-PROTECTION",
            "EP-015-VERIFICATION-DASHBOARD-RECONCILIATION",
            "EP-016-REFERENCE-INTAKE-PREPARATION",
            "EP-017-AUDIT-FINDINGS-CLEANUP",
            "EP-006-MONTHLY-PLANNING-AND-DEFENSE",
        ]:
            if needle not in text:
                errors.append(f"{rel(path)} missing post-acceptance marker: {needle}")
        current_section = re.search(
            r"## \d+\. (?:Current Execution Packet|Текущий Execution Packet)\n\n`([^`]+)`",
            text,
        )
        if current_section and current_section.group(1) == PREVIOUS_PACKET:
            errors.append(f"{rel(path)} still lists EP-012 as current active packet")
        for packet_id in sorted(EXPECTED_ACCEPTED_PACKETS):
            if packet_id not in text:
                errors.append(
                    f"{rel(path)} baseline missing accepted packet {packet_id}"
                )
        if not accepted >= EXPECTED_ACCEPTED_PACKETS:
            missing = ", ".join(sorted(EXPECTED_ACCEPTED_PACKETS - accepted))
            errors.append(f"acceptance reports missing accepted packets: {missing}")


def validate_acceptance_dashboard(errors: list[str], accepted: set[str]) -> None:
    dashboard = load_root(ACCEPTANCE_DASHBOARD_PATH, "acceptance_dashboard")
    if not dashboard:
        errors.append("Missing or invalid docs/acceptance-dashboard.yml")
        return
    summary = (
        dashboard.get("summary") if isinstance(dashboard.get("summary"), dict) else {}
    )
    if summary.get("ready_for_acceptance") != 1:
        errors.append(
            "acceptance dashboard must show exactly one ready_for_acceptance item: EP-013"
        )
    if summary.get("accepted") != len(accepted):
        errors.append(
            "acceptance dashboard accepted count does not match accepted reports"
        )
    if summary.get("protected_accepted_artifacts") != 0:
        errors.append("EP-013 must not mask protected_accepted_artifacts=0")

    baseline = (
        dashboard.get("post_acceptance_baseline")
        if isinstance(dashboard.get("post_acceptance_baseline"), dict)
        else {}
    )
    baseline_packets = {
        str(item.get("packet_id"))
        for item in baseline.get("accepted_packets", [])
        if isinstance(item, dict)
    }
    if not EXPECTED_ACCEPTED_PACKETS <= baseline_packets:
        errors.append(
            "acceptance dashboard post_acceptance_baseline misses accepted EP-001..EP-012"
        )
    if baseline.get("protection_flags_status") != "deferred_to_EP-014":
        errors.append("acceptance dashboard must defer protection flags to EP-014")

    items = dashboard.get("items", [])
    item_by_packet = {
        str(item.get("packet_id")): item for item in items if isinstance(item, dict)
    }
    for packet_id in sorted(accepted):
        item = item_by_packet.get(packet_id)
        if not item:
            errors.append(
                f"accepted packet missing from acceptance dashboard: {packet_id}"
            )
            continue
        if item.get("status") != "accepted":
            errors.append(f"{packet_id}: dashboard status must be accepted")
        if item.get("acceptance_decision") != "accepted":
            errors.append(f"{packet_id}: dashboard decision must be accepted")
    ep013 = item_by_packet.get(CURRENT_PACKET)
    if not ep013:
        errors.append(f"{CURRENT_PACKET} missing from acceptance dashboard")
    elif ep013.get("status") != "ready_for_acceptance":
        errors.append(
            f"{CURRENT_PACKET}: dashboard status must be ready_for_acceptance"
        )


def validate_workbench(errors: list[str]) -> None:
    workbench = load_root(WORKBENCH_PATH, "user_review_workbench")
    if not workbench:
        errors.append("Missing or invalid docs/user-review-workbench.yml")
        return
    active = [
        item
        for item in workbench.get("active_review_items", [])
        if isinstance(item, dict)
    ]
    active_acceptance = {
        str(item.get("packet_id"))
        for item in active
        if item.get("type") == "acceptance"
    }
    unexpected = sorted(EXPECTED_ACCEPTED_PACKETS & active_acceptance)
    if unexpected:
        errors.append(
            "accepted packets must not be active acceptance items: "
            + ", ".join(unexpected)
        )
    if CURRENT_PACKET not in active_acceptance:
        errors.append(
            "EP-013 must be active acceptance item while ready_for_acceptance"
        )

    recent = {
        str(item.get("packet_id"))
        for item in workbench.get("recently_accepted", [])
        if isinstance(item, dict)
    }
    if not EXPECTED_ACCEPTED_PACKETS <= recent:
        errors.append("workbench recently_accepted misses accepted EP-001..EP-012")

    baseline = (
        workbench.get("post_acceptance_baseline")
        if isinstance(workbench.get("post_acceptance_baseline"), dict)
        else {}
    )
    baseline_packets = {
        str(item.get("packet_id"))
        for item in baseline.get("accepted_packets", [])
        if isinstance(item, dict)
    }
    if not EXPECTED_ACCEPTED_PACKETS <= baseline_packets:
        errors.append(
            "workbench post_acceptance_baseline misses accepted EP-001..EP-012"
        )
    if baseline.get("protection_flags_status") != "deferred_to_EP-014":
        errors.append("workbench must defer protection flags to EP-014")


def validate_verification_debt(errors: list[str]) -> None:
    dashboard = load_root(VERIFICATION_DASHBOARD_PATH, "verification_dashboard")
    if not dashboard:
        errors.append("Missing or invalid docs/verification-dashboard.yml")
        return
    summary = (
        dashboard.get("summary") if isinstance(dashboard.get("summary"), dict) else {}
    )
    if int(summary.get("pending") or 0) < 44:
        errors.append(
            "verification pending checks should remain open as post-acceptance debt"
        )
    checks = dashboard.get("checks", [])
    for check in checks if isinstance(checks, list) else []:
        if not isinstance(check, dict):
            continue
        user_result = (
            check.get("user_result")
            if isinstance(check.get("user_result"), dict)
            else {}
        )
        if user_result.get("checked_by") == "Codex":
            errors.append(f"{check.get('check_id')}: checked_by must not be Codex")
        if (
            str(check.get("check_type") or "").startswith("manual")
            and str(check.get("status") or "") == "passed"
        ):
            errors.append(
                f"{check.get('check_id')}: manual check must not be passed by Codex"
            )
    ep006_checks = [
        check
        for check in checks
        if isinstance(check, dict)
        and check.get("related_packet") == "EP-006-MONTHLY-PLANNING-AND-DEFENSE"
    ]
    if not ep006_checks:
        errors.append(
            "EP-006 orphan/monthly checks are not visible for EP-015 follow-up"
        )


def validate_user_actions(errors: list[str]) -> None:
    dashboard = load_root(USER_ACTION_DASHBOARD_PATH, "user_action_dashboard")
    if not dashboard:
        errors.append("Missing or invalid docs/user-action-dashboard.yml")
        return
    actions = dashboard.get("actions", [])
    by_id = {
        str(action.get("id")): action for action in actions if isinstance(action, dict)
    }
    for action_id in sorted(HIGH_PRIORITY_ACTIONS):
        action = by_id.get(action_id)
        if not action:
            errors.append(f"high-priority user action missing: {action_id}")
            continue
        if action.get("status") != "open":
            errors.append(f"{action_id}: high-priority user action must remain open")


def validate_audit_statuses(errors: list[str]) -> None:
    if not AUDIT_FINDINGS_PATH.exists():
        errors.append("Missing docs/audit/audit-findings.yml")
        return
    data = load_data(AUDIT_FINDINGS_PATH)
    findings = data.get("findings", []) if isinstance(data, dict) else []
    if not isinstance(findings, list):
        errors.append("audit-findings.yml must contain findings list")
        return
    open_count = 0
    for item in findings:
        if not isinstance(item, dict):
            continue
        status = str(item.get("status") or "")
        if status not in ALLOWED_AUDIT_STATUSES:
            errors.append(f"{item.get('id')}: unexpected audit status {status}")
        if status == "obsolete":
            errors.append(
                f"{item.get('id')}: obsolete status is forbidden without schema change"
            )
        if status == "open":
            open_count += 1
        if item.get("resolved_by") == "Codex":
            errors.append(f"{item.get('id')}: resolved_by must not be Codex")
    if open_count < 100:
        errors.append(
            "audit findings appear to be mass-closed; EP-013 must leave audit debt open"
        )


def main() -> int:
    errors: list[str] = []
    accepted = accepted_reports()
    if EXPECTED_ACCEPTED_PACKETS - accepted:
        missing = ", ".join(sorted(EXPECTED_ACCEPTED_PACKETS - accepted))
        errors.append(f"expected accepted reports are not accepted: {missing}")
    if CURRENT_PACKET in accepted:
        errors.append("EP-013 must remain pending until user acceptance")

    validate_execution_packets(errors, accepted)
    validate_planning_documents(errors, accepted)
    validate_acceptance_dashboard(errors, accepted)
    validate_workbench(errors)
    validate_verification_debt(errors)
    validate_user_actions(errors)
    validate_audit_statuses(errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Post-acceptance state validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
