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

CURRENT_PACKET = "EP-018-ACCEPTED-ARTIFACT-PROTECTION"
PREVIOUS_PACKET = "EP-014-USER-REVIEW-DECISION-CLI-SAFETY"
CURRENT_READY_PACKET = "EP-010-LANGUAGE-NORMALIZATION"
NEXT_RECOMMENDED_PACKET = "BASELINE-TAG-BEFORE-EP-010"
PREVIOUS_ACTIVE_PACKET_AFTER_BASELINE = CURRENT_PACKET
PRE_ACCEPTANCE_CURRENT_STATUSES = {"pending", "ready_for_acceptance"}
BASELINE_ACCEPTED_PACKETS = {
    "EP-001-INFRA",
    "EP-002-REFERENCE-GOVERNANCE",
    "EP-003-REFERENCE-VERSIONING",
    "EP-004-PROJECT-PLANNING-AND-ACCEPTANCE",
    "EP-005-ACCEPTANCE-AND-USER-ACTION-DASHBOARDS",
    "EP-007-VERIFICATION-DASHBOARD",
    "EP-008-DISSERTATION-PROMPT-GENERATION",
    "EP-009-CODEX-SPEC-AUDIT",
    "EP-011-GIT-WORKFLOW-DISCIPLINE",
    "EP-012-USER-REVIEW-WORKBENCH-AND-ACCEPTANCE-STANDARD",
    "EP-013-POST-ACCEPTANCE-STATE-SYNC",
    PREVIOUS_PACKET,
}
POST_ACCEPTANCE_ACCEPTED_PACKETS = BASELINE_ACCEPTED_PACKETS | {CURRENT_PACKET}
ALLOWED_READY_PACKETS_AFTER_BASELINE: set[str] = set()
ALLOWED_PROTECTION_DEFERRALS = {
    "deferred_to_EP-018",
    "classified_by_EP-018",
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


def validate_acceptance_report_ownership(errors: list[str]) -> None:
    for path in ACCEPTANCE_DIR.glob("EP-*.acceptance.md"):
        packet_id = path.name.removesuffix(".acceptance.md")
        decision = parse_acceptance_report(path)
        if (
            decision.get("acceptance_decision") == "accepted"
            and decision.get("accepted_by") == "Codex"
        ):
            errors.append(f"{packet_id}: accepted_by must not be Codex")


def packet_statuses() -> dict[str, str]:
    if not PACKETS_PATH.exists():
        return {}
    root = ET.parse(PACKETS_PATH).getroot()
    return {
        str(packet.attrib.get("id")): str(packet.attrib.get("status") or "")
        for packet in root.findall("Packet")
    }


def ready_for_acceptance_packets(statuses: dict[str, str]) -> set[str]:
    return {
        packet_id
        for packet_id, status in statuses.items()
        if status == "ready_for_acceptance"
    }


def detect_acceptance_mode(
    errors: list[str],
    accepted: set[str],
    statuses: dict[str, str],
) -> str:
    current_status = statuses.get(CURRENT_PACKET, "")
    if CURRENT_PACKET in accepted:
        if current_status != "accepted":
            errors.append(
                f"{CURRENT_PACKET}: accepted report requires execution packet status accepted"
            )
        return "post_acceptance"

    if current_status not in PRE_ACCEPTANCE_CURRENT_STATUSES:
        errors.append(
            f"{CURRENT_PACKET}: pre-acceptance status must be pending or ready_for_acceptance"
        )
    return "pre_acceptance"


def expected_accepted_packets(mode: str) -> set[str]:
    if mode == "post_acceptance":
        accepted = accepted_reports()
        if CURRENT_READY_PACKET in accepted:
            return POST_ACCEPTANCE_ACCEPTED_PACKETS | {CURRENT_READY_PACKET}
        return POST_ACCEPTANCE_ACCEPTED_PACKETS
    return BASELINE_ACCEPTED_PACKETS


def last_accepted_packet(accepted: set[str]) -> str:
    if CURRENT_READY_PACKET in accepted:
        return CURRENT_READY_PACKET
    return CURRENT_PACKET


def previous_active_packet(accepted: set[str], allowed_ready: set[str]) -> str:
    if allowed_ready:
        return PREVIOUS_ACTIVE_PACKET_AFTER_BASELINE
    if CURRENT_PACKET in accepted:
        return CURRENT_PACKET
    if CURRENT_READY_PACKET in accepted:
        return CURRENT_READY_PACKET
    return PREVIOUS_PACKET


def validate_execution_packets(
    errors: list[str],
    accepted: set[str],
    statuses: dict[str, str],
    mode: str,
) -> None:
    for packet_id in sorted(accepted):
        if statuses.get(packet_id) != "accepted":
            errors.append(
                f"{packet_id}: accepted acceptance report is not reflected as accepted in execution-packets.xml"
            )
    if mode == "pre_acceptance":
        if statuses.get(CURRENT_PACKET) not in PRE_ACCEPTANCE_CURRENT_STATUSES:
            errors.append(
                f"{CURRENT_PACKET}: expected pre-acceptance status pending or ready_for_acceptance"
            )
    elif statuses.get(CURRENT_PACKET) != "accepted":
        errors.append(f"{CURRENT_PACKET}: expected post-acceptance status accepted")
    if mode == "post_acceptance":
        ready_packets = ready_for_acceptance_packets(statuses)
        unexpected_ready = ready_packets - ALLOWED_READY_PACKETS_AFTER_BASELINE
        if unexpected_ready:
            errors.append(
                "unexpected ready_for_acceptance packets after accepted baseline: "
                + ", ".join(sorted(unexpected_ready))
            )


def validate_planning_documents(
    errors: list[str],
    accepted: set[str],
    statuses: dict[str, str],
    mode: str,
) -> None:
    expected_packets = expected_accepted_packets(mode)
    ready_packets = ready_for_acceptance_packets(statuses)
    allowed_ready = ready_packets & ALLOWED_READY_PACKETS_AFTER_BASELINE
    for path in [PROJECT_PLAN_PATH, STATUS_REPORT_PATH]:
        if not path.exists():
            errors.append(f"Missing planning document: {rel(path)}")
            continue
        text = path.read_text(encoding="utf-8")
        common_needles = [
            "project_state: accepted_baseline",
            CURRENT_READY_PACKET,
            NEXT_RECOMMENDED_PACKET,
            "EP-015-VERIFICATION-DASHBOARD-RECONCILIATION",
            "EP-016-REFERENCE-INTAKE-PREPARATION",
            "EP-017-AUDIT-FINDINGS-CLEANUP",
            "EP-006-MONTHLY-PLANNING-AND-DEFENSE",
        ]
        if mode == "post_acceptance":
            if allowed_ready:
                mode_needles = [
                    f"active_execution_packet: {CURRENT_READY_PACKET}",
                    f"next_recommended_packet: {NEXT_RECOMMENDED_PACKET}",
                    f"last_accepted_execution_packet: {CURRENT_PACKET}",
                    f"previous_active_execution_packet: {PREVIOUS_ACTIVE_PACKET_AFTER_BASELINE}",
                ]
            else:
                mode_needles = [
                    "active_execution_packet: none",
                    f"last_accepted_execution_packet: {last_accepted_packet(accepted)}",
                    f"previous_active_execution_packet: {previous_active_packet(accepted, allowed_ready)}",
                ]
        else:
            mode_needles = [
                f"active_execution_packet: {CURRENT_PACKET}",
            ]
        for needle in common_needles + mode_needles:
            if needle not in text:
                errors.append(f"{rel(path)} missing post-acceptance marker: {needle}")
        if mode == "post_acceptance" and re.search(
            rf"^active_execution_packet:\s+{re.escape(CURRENT_PACKET)}$",
            text,
            re.MULTILINE,
        ):
            errors.append(
                f"{rel(path)} still lists EP-018 as active packet after acceptance"
            )
        current_section = re.search(
            r"## \d+\. (?:Current Execution Packet|Текущий Execution Packet)\n\n`([^`]+)`",
            text,
        )
        if current_section and current_section.group(1) == PREVIOUS_PACKET:
            errors.append(f"{rel(path)} still lists EP-014 as current active packet")
        if (
            mode == "post_acceptance"
            and current_section
            and current_section.group(1) not in (allowed_ready or {"none"})
        ):
            errors.append(
                f"{rel(path)} current execution packet must be none or explicitly allowed ready packet"
            )
        for packet_id in sorted(expected_packets):
            if packet_id not in text:
                errors.append(
                    f"{rel(path)} baseline missing accepted packet {packet_id}"
                )
        if not accepted >= expected_packets:
            missing = ", ".join(sorted(expected_packets - accepted))
            errors.append(f"acceptance reports missing accepted packets: {missing}")


def validate_acceptance_dashboard(
    errors: list[str],
    accepted: set[str],
    statuses: dict[str, str],
    mode: str,
) -> None:
    expected_packets = expected_accepted_packets(mode)
    ready_packets = ready_for_acceptance_packets(statuses)
    allowed_ready = ready_packets & ALLOWED_READY_PACKETS_AFTER_BASELINE
    dashboard = load_root(ACCEPTANCE_DASHBOARD_PATH, "acceptance_dashboard")
    if not dashboard:
        errors.append("Missing or invalid docs/acceptance-dashboard.yml")
        return
    summary = (
        dashboard.get("summary") if isinstance(dashboard.get("summary"), dict) else {}
    )
    expected_ready = len(allowed_ready) if mode == "post_acceptance" else 1
    if summary.get("ready_for_acceptance") != expected_ready:
        errors.append(
            "acceptance dashboard ready_for_acceptance count does not match explicitly registered current packet"
        )
    if summary.get("accepted") != len(accepted):
        errors.append(
            "acceptance dashboard accepted count does not match accepted reports"
        )
    protected_count = int(summary.get("protected_accepted_artifacts") or 0)
    if protected_count < len(accepted):
        errors.append("accepted artifact protection count is lower than accepted reports")

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
    if not expected_packets <= baseline_packets:
        errors.append(
            "acceptance dashboard post_acceptance_baseline misses expected accepted packets"
        )
    if baseline.get("protection_flags_status") not in ALLOWED_PROTECTION_DEFERRALS:
        errors.append("acceptance dashboard has unexpected protection deferral status")

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
    elif mode == "post_acceptance":
        if ep013.get("status") != "accepted":
            errors.append(f"{CURRENT_PACKET}: dashboard status must be accepted")
        if ep013.get("acceptance_decision") != "accepted":
            errors.append(f"{CURRENT_PACKET}: dashboard decision must be accepted")
    elif ep013.get("status") not in PRE_ACCEPTANCE_CURRENT_STATUSES:
        errors.append(f"{CURRENT_PACKET}: dashboard status must be pending or ready")
    for packet_id in sorted(ready_packets):
        item = item_by_packet.get(packet_id)
        if packet_id not in ALLOWED_READY_PACKETS_AFTER_BASELINE:
            errors.append(f"{packet_id}: not allowed as active ready packet")
            continue
        if not item:
            errors.append(f"{packet_id}: registered ready packet missing from dashboard")
        elif item.get("status") != "ready_for_acceptance":
            errors.append(f"{packet_id}: dashboard status must be ready_for_acceptance")


def validate_workbench(errors: list[str], statuses: dict[str, str], mode: str) -> None:
    expected_packets = expected_accepted_packets(mode)
    ready_packets = ready_for_acceptance_packets(statuses)
    allowed_ready = ready_packets & ALLOWED_READY_PACKETS_AFTER_BASELINE
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
    unexpected = sorted(expected_packets & active_acceptance)
    if unexpected:
        errors.append(
            "accepted packets must not be active acceptance items: "
            + ", ".join(unexpected)
        )
    if mode == "pre_acceptance" and CURRENT_PACKET not in active_acceptance:
        errors.append(
            "EP-018 must be active acceptance item while ready_for_acceptance"
        )
    if mode == "post_acceptance" and active_acceptance - allowed_ready:
        errors.append(
            "active acceptance queue contains non-allowed packets after accepted baseline: "
            + ", ".join(sorted(active_acceptance - allowed_ready))
        )
    missing_ready = allowed_ready - active_acceptance
    if mode == "post_acceptance" and missing_ready:
        errors.append(
            "allowed ready_for_acceptance packets missing from active acceptance queue: "
            + ", ".join(sorted(missing_ready))
        )

    recent = {
        str(item.get("packet_id"))
        for item in workbench.get("recently_accepted", [])
        if isinstance(item, dict)
    }
    if not expected_packets <= recent:
        errors.append("workbench recently_accepted misses expected accepted packets")

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
    if not expected_packets <= baseline_packets:
        errors.append(
            "workbench post_acceptance_baseline misses expected accepted packets"
        )
    if baseline.get("protection_flags_status") not in ALLOWED_PROTECTION_DEFERRALS:
        errors.append("workbench has unexpected protection deferral status")


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
            "audit findings appear to be mass-closed; post-acceptance baseline must leave audit debt open"
        )


def main() -> int:
    errors: list[str] = []
    accepted = accepted_reports()
    statuses = packet_statuses()
    validate_acceptance_report_ownership(errors)
    mode = detect_acceptance_mode(errors, accepted, statuses)
    expected_packets = expected_accepted_packets(mode)
    if BASELINE_ACCEPTED_PACKETS - accepted:
        missing = ", ".join(sorted(BASELINE_ACCEPTED_PACKETS - accepted))
        errors.append(f"expected accepted reports are not accepted: {missing}")
    if expected_packets - accepted:
        missing = ", ".join(sorted(expected_packets - accepted))
        errors.append(f"expected accepted reports are not accepted in {mode}: {missing}")

    validate_execution_packets(errors, accepted, statuses, mode)
    validate_planning_documents(errors, accepted, statuses, mode)
    validate_acceptance_dashboard(errors, accepted, statuses, mode)
    validate_workbench(errors, statuses, mode)
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
