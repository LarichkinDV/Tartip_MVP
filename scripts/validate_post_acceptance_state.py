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
PROJECT_STATE_PATH = PROJECT_ROOT / "docs" / "project-state.yml"
PACKETS_PATH = PROJECT_ROOT / "docs" / "grace" / "execution-packets.xml"
PROJECT_PLAN_PATH = PROJECT_ROOT / "docs" / "project-plan.md"
STATUS_REPORT_PATH = PROJECT_ROOT / "docs" / "status-report.md"
ACCEPTANCE_DASHBOARD_PATH = PROJECT_ROOT / "docs" / "acceptance-dashboard.yml"
WORKBENCH_PATH = PROJECT_ROOT / "docs" / "user-review-workbench.yml"
VERIFICATION_DASHBOARD_PATH = PROJECT_ROOT / "docs" / "verification-dashboard.yml"
USER_ACTION_DASHBOARD_PATH = PROJECT_ROOT / "docs" / "user-action-dashboard.yml"
AUDIT_FINDINGS_PATH = PROJECT_ROOT / "docs" / "audit" / "audit-findings.yml"

ALLOWED_STATE_MODES = {
    "accepted_baseline",
    "in_progress",
    "ready_for_acceptance",
    "blocked",
}
REQUIRED_PROJECT_STATE_KEYS = {
    "schema_version",
    "state_mode",
    "active_execution_packet",
    "last_accepted_execution_packet",
    "last_completed_execution_packet",
    "next_recommended_packet",
    "deferred_follow_up_packets",
    "accepted_packets",
    "monthly_scopes",
}
ACTIVE_STATE_MODES = {"in_progress", "ready_for_acceptance", "blocked"}
ALLOWED_ACTIVE_PACKET_STATUSES = {
    "planned",
    "in_progress",
    "ready_for_acceptance",
    "blocked",
    "needs_revision",
}
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
USER_OWNED_FIELD_RE = re.compile(
    r"^\s*(accepted_by|decided_by|checked_by|answered_by)\s*:\s*[\"']?Codex[\"']?\s*$"
)


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


def normalize_packet(value: Any) -> str:
    text = str(value or "").strip()
    return "" if text in {"", "none", "null", "None", "~"} else text


def load_root(path: Path, root_key: str) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = load_data(path)
    if not isinstance(data, dict):
        return {}
    root = data.get(root_key, {})
    return root if isinstance(root, dict) else {}


def load_project_state(errors: list[str]) -> dict[str, Any]:
    if not PROJECT_STATE_PATH.exists():
        errors.append("Missing docs/project-state.yml")
        return {}
    data = load_data(PROJECT_STATE_PATH)
    state = data.get("project_state", {}) if isinstance(data, dict) else {}
    if not isinstance(state, dict):
        errors.append("docs/project-state.yml must contain project_state mapping")
        return {}
    missing = sorted(REQUIRED_PROJECT_STATE_KEYS - set(state))
    if missing:
        errors.append("docs/project-state.yml missing required keys: " + ", ".join(missing))
    if state.get("schema_version") != 1:
        errors.append("docs/project-state.yml schema_version must be 1")
    mode = str(state.get("state_mode") or "")
    if mode not in ALLOWED_STATE_MODES:
        errors.append(f"docs/project-state.yml has invalid state_mode: {mode}")
    accepted_packets = state.get("accepted_packets")
    if not isinstance(accepted_packets, list):
        errors.append("docs/project-state.yml accepted_packets must be a list")
    monthly_scopes = state.get("monthly_scopes")
    if not isinstance(monthly_scopes, list):
        errors.append("docs/project-state.yml monthly_scopes must be a list")
    next_packet = normalize_packet(state.get("next_recommended_packet"))
    active_packet = normalize_packet(state.get("active_execution_packet"))
    if active_packet and next_packet == active_packet:
        errors.append("next_recommended_packet must not equal active_execution_packet")
    if mode in ACTIVE_STATE_MODES and not active_packet:
        errors.append(f"state_mode={mode} requires active_execution_packet")
    if mode == "accepted_baseline" and active_packet:
        errors.append("state_mode=accepted_baseline requires active_execution_packet to be empty or none")
    return state


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


def ready_for_acceptance_packets(statuses: dict[str, str]) -> set[str]:
    return {
        packet_id
        for packet_id, status in statuses.items()
        if status == "ready_for_acceptance"
    }


def scan_codex_user_fields(errors: list[str]) -> None:
    roots = [
        ACCEPTANCE_DIR,
        PROJECT_ROOT / "docs",
    ]
    for root in roots:
        if not root.exists():
            continue
        paths = root.glob("*.md") if root == ACCEPTANCE_DIR else root.rglob("*")
        for path in sorted(paths):
            if path.is_dir() or path.suffix.lower() not in {".md", ".yml", ".yaml"}:
                continue
            for index, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                match = USER_OWNED_FIELD_RE.match(line)
                if match:
                    errors.append(f"{rel(path)}:{index}: {match.group(1)} must not be Codex")


def validate_project_state_against_sources(
    errors: list[str],
    state: dict[str, Any],
    accepted: set[str],
    statuses: dict[str, str],
) -> None:
    accepted_packets = {str(packet) for packet in as_list(state.get("accepted_packets"))}
    active_packet = normalize_packet(state.get("active_execution_packet"))
    last_accepted = normalize_packet(state.get("last_accepted_execution_packet"))
    last_completed = normalize_packet(state.get("last_completed_execution_packet"))

    if accepted_packets != accepted:
        missing = sorted(accepted - accepted_packets)
        extra = sorted(accepted_packets - accepted)
        if missing:
            errors.append("docs/project-state.yml accepted_packets misses accepted reports: " + ", ".join(missing))
        if extra:
            errors.append("docs/project-state.yml accepted_packets contains non-accepted reports: " + ", ".join(extra))
    for packet_id in sorted(accepted_packets):
        if statuses.get(packet_id) != "accepted":
            errors.append(f"{packet_id}: project-state accepted packet is not accepted in execution-packets.xml")
        report = ACCEPTANCE_DIR / f"{packet_id}.acceptance.md"
        decision = parse_acceptance_report(report)
        if decision.get("acceptance_decision") != "accepted":
            errors.append(f"{packet_id}: project-state accepted packet lacks accepted acceptance_decision")
        accepted_by = decision.get("accepted_by")
        if not accepted_by:
            errors.append(f"{packet_id}: project-state accepted packet lacks accepted_by")
        if accepted_by == "Codex":
            errors.append(f"{packet_id}: accepted_by must not be Codex")
    if active_packet:
        if active_packet in accepted_packets:
            errors.append(f"active_execution_packet must not be in accepted_packets: {active_packet}")
        status = statuses.get(active_packet)
        if status not in ALLOWED_ACTIVE_PACKET_STATUSES:
            errors.append(f"{active_packet}: active packet has invalid status for current state: {status or '-'}")
        if state.get("state_mode") == "ready_for_acceptance" and status != "ready_for_acceptance":
            errors.append(f"{active_packet}: state_mode=ready_for_acceptance requires packet status ready_for_acceptance")
    if last_accepted and last_accepted not in accepted_packets:
        errors.append(f"last_accepted_execution_packet is not in accepted_packets: {last_accepted}")
    if last_completed and last_completed not in accepted_packets and last_completed != active_packet:
        errors.append(f"last_completed_execution_packet is neither accepted nor active: {last_completed}")

    ready_packets = ready_for_acceptance_packets(statuses)
    allowed_ready = {active_packet} if state.get("state_mode") == "ready_for_acceptance" and active_packet else set()
    unexpected_ready = ready_packets - allowed_ready
    if unexpected_ready:
        errors.append("unexpected ready_for_acceptance packets outside project-state active packet: " + ", ".join(sorted(unexpected_ready)))


def validate_planning_documents(errors: list[str], state: dict[str, Any]) -> None:
    accepted_packets = {str(packet) for packet in as_list(state.get("accepted_packets"))}
    active_packet = normalize_packet(state.get("active_execution_packet"))
    current_text = active_packet or "none"
    required_markers = [
        f"project_state: {state.get('state_mode')}",
        f"active_execution_packet: {active_packet or 'none'}",
        f"last_accepted_execution_packet: {state.get('last_accepted_execution_packet')}",
        f"last_completed_execution_packet: {state.get('last_completed_execution_packet')}",
        f"next_recommended_packet: {state.get('next_recommended_packet')}",
    ]
    for path in [PROJECT_PLAN_PATH, STATUS_REPORT_PATH]:
        if not path.exists():
            errors.append(f"Missing planning document: {rel(path)}")
            continue
        text = path.read_text(encoding="utf-8")
        for marker in required_markers:
            if marker not in text:
                errors.append(f"{rel(path)} missing project-state marker: {marker}")
        current_section = re.search(
            r"## \d+\. (?:Current Execution Packet|Текущий Execution Packet)\n\n`([^`]+)`",
            text,
        )
        if current_section and current_section.group(1) != current_text:
            errors.append(f"{rel(path)} current execution packet must be {current_text}")
        for packet_id in sorted(accepted_packets):
            if packet_id not in text:
                errors.append(f"{rel(path)} baseline missing accepted packet {packet_id}")


def validate_acceptance_dashboard(
    errors: list[str],
    state: dict[str, Any],
    accepted: set[str],
) -> None:
    dashboard = load_root(ACCEPTANCE_DASHBOARD_PATH, "acceptance_dashboard")
    if not dashboard:
        errors.append("Missing or invalid docs/acceptance-dashboard.yml")
        return
    active_packet = normalize_packet(state.get("active_execution_packet"))
    expected_ready = 1 if state.get("state_mode") == "ready_for_acceptance" and active_packet else 0
    summary = dashboard.get("summary") if isinstance(dashboard.get("summary"), dict) else {}
    if summary.get("ready_for_acceptance") != expected_ready:
        errors.append("acceptance dashboard ready_for_acceptance count does not match project-state")
    if summary.get("accepted") != len(accepted):
        errors.append("acceptance dashboard accepted count does not match accepted reports")
    protected_count = int(summary.get("protected_accepted_artifacts") or 0)
    if protected_count < len(accepted):
        errors.append("accepted artifact protection count is lower than accepted reports")
    baseline = dashboard.get("post_acceptance_baseline") if isinstance(dashboard.get("post_acceptance_baseline"), dict) else {}
    baseline_packets = {
        str(item.get("packet_id"))
        for item in baseline.get("accepted_packets", [])
        if isinstance(item, dict)
    }
    if not accepted <= baseline_packets:
        errors.append("acceptance dashboard post_acceptance_baseline misses accepted packets")
    if baseline.get("protection_flags_status") not in ALLOWED_PROTECTION_DEFERRALS:
        errors.append("acceptance dashboard has unexpected protection deferral status")
    items = dashboard.get("items", [])
    item_by_packet = {
        str(item.get("packet_id")): item for item in items if isinstance(item, dict)
    }
    for packet_id in sorted(accepted):
        item = item_by_packet.get(packet_id)
        if not item:
            errors.append(f"accepted packet missing from acceptance dashboard: {packet_id}")
            continue
        if item.get("status") != "accepted":
            errors.append(f"{packet_id}: dashboard status must be accepted")
        if item.get("acceptance_decision") != "accepted":
            errors.append(f"{packet_id}: dashboard decision must be accepted")
    if active_packet and state.get("state_mode") == "ready_for_acceptance":
        item = item_by_packet.get(active_packet)
        if not item:
            errors.append(f"{active_packet}: active packet missing from acceptance dashboard")
        elif item.get("status") != "ready_for_acceptance":
            errors.append(f"{active_packet}: dashboard status must be ready_for_acceptance")


def validate_workbench(
    errors: list[str],
    state: dict[str, Any],
    accepted: set[str],
) -> None:
    workbench = load_root(WORKBENCH_PATH, "user_review_workbench")
    if not workbench:
        errors.append("Missing or invalid docs/user-review-workbench.yml")
        return
    active_packet = normalize_packet(state.get("active_execution_packet"))
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
    unexpected = sorted(accepted & active_acceptance)
    if unexpected:
        errors.append("accepted packets must not be active acceptance items: " + ", ".join(unexpected))
    allowed_active = {active_packet} if state.get("state_mode") == "ready_for_acceptance" and active_packet else set()
    if active_acceptance - allowed_active:
        errors.append("active acceptance queue contains non-project-state packets: " + ", ".join(sorted(active_acceptance - allowed_active)))
    if allowed_active - active_acceptance:
        errors.append("project-state active ready packet missing from active acceptance queue: " + ", ".join(sorted(allowed_active - active_acceptance)))
    recent = {
        str(item.get("packet_id"))
        for item in workbench.get("recently_accepted", [])
        if isinstance(item, dict)
    }
    if not accepted <= recent:
        errors.append("workbench recently_accepted misses accepted packets")
    baseline = workbench.get("post_acceptance_baseline") if isinstance(workbench.get("post_acceptance_baseline"), dict) else {}
    baseline_packets = {
        str(item.get("packet_id"))
        for item in baseline.get("accepted_packets", [])
        if isinstance(item, dict)
    }
    if not accepted <= baseline_packets:
        errors.append("workbench post_acceptance_baseline misses accepted packets")
    if baseline.get("protection_flags_status") not in ALLOWED_PROTECTION_DEFERRALS:
        errors.append("workbench has unexpected protection deferral status")


def validate_verification_debt(errors: list[str], state: dict[str, Any]) -> None:
    dashboard = load_root(VERIFICATION_DASHBOARD_PATH, "verification_dashboard")
    if not dashboard:
        errors.append("Missing or invalid docs/verification-dashboard.yml")
        return
    summary = dashboard.get("summary") if isinstance(dashboard.get("summary"), dict) else {}
    if int(summary.get("pending") or 0) < 44:
        errors.append("verification pending checks should remain open as post-acceptance debt")
    checks = dashboard.get("checks", [])
    for check in checks if isinstance(checks, list) else []:
        if not isinstance(check, dict):
            continue
        user_result = check.get("user_result") if isinstance(check.get("user_result"), dict) else {}
        if user_result.get("checked_by") == "Codex":
            errors.append(f"{check.get('check_id')}: checked_by must not be Codex")
        if str(check.get("check_type") or "").startswith("manual") and str(check.get("status") or "") == "passed":
            errors.append(f"{check.get('check_id')}: manual check must not be passed by Codex")
    for scope in as_list(state.get("monthly_scopes")):
        if not isinstance(scope, dict):
            errors.append("monthly_scopes entries must be mappings")
            continue
        scope_id = str(scope.get("scope_id") or "")
        legacy_packet = str(scope.get("replaces_orphan_packet_id") or "")
        if not scope_id:
            errors.append("monthly scope missing scope_id")
            continue
        scope_checks = [
            check
            for check in checks
            if isinstance(check, dict)
            and check.get("scope_type") == "monthly_block"
            and check.get("scope_id") == scope_id
        ]
        if not scope_checks:
            errors.append(f"monthly scope {scope_id} has no verification checks")
        legacy_related = [
            str(check.get("check_id"))
            for check in checks
            if isinstance(check, dict) and check.get("related_packet") == legacy_packet
        ]
        if legacy_related:
            errors.append(
                f"{legacy_packet} still appears as related_packet for monthly checks: "
                + ", ".join(legacy_related)
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
    for item in findings:
        if not isinstance(item, dict):
            continue
        status = str(item.get("status") or "")
        if status not in ALLOWED_AUDIT_STATUSES:
            errors.append(f"{item.get('id')}: unexpected audit status {status}")
        if status == "obsolete":
            errors.append(f"{item.get('id')}: obsolete status is forbidden without schema change")
        if item.get("resolved_by") == "Codex":
            errors.append(f"{item.get('id')}: resolved_by must not be Codex")
        if item.get("resolved_by") == "EP-010-LANGUAGE-NORMALIZATION":
            allowed_ep010_resolution = (
                item.get("check_id") == "AUD-LANG-001"
                and item.get("file") in {"README.md", "CHANGELOG.md"}
                and status in {"fixed", "false_positive"}
            )
            if not allowed_ep010_resolution:
                errors.append(f"{item.get('id')}: EP-010 may resolve only AUD-LANG-001 findings for README.md and CHANGELOG.md")


def main() -> int:
    errors: list[str] = []
    state = load_project_state(errors)
    accepted = accepted_reports()
    statuses = packet_statuses()
    scan_codex_user_fields(errors)
    if state:
        validate_project_state_against_sources(errors, state, accepted, statuses)
        validate_planning_documents(errors, state)
        validate_acceptance_dashboard(errors, state, accepted)
        validate_workbench(errors, state, accepted)
        validate_verification_debt(errors, state)
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
