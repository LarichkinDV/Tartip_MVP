#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

from reference_utils import load_data


PROJECT_ROOT = Path(__file__).resolve().parents[1]
WORKBENCH_YAML = PROJECT_ROOT / "docs" / "user-review-workbench.yml"
WORKBENCH_MD = PROJECT_ROOT / "docs" / "user-review-workbench.md"
ACCEPTANCE_DASHBOARD = PROJECT_ROOT / "docs" / "acceptance-dashboard.yml"
VERIFICATION_DASHBOARD = PROJECT_ROOT / "docs" / "verification-dashboard.yml"
USER_ACTION_DASHBOARD = PROJECT_ROOT / "docs" / "user-action-dashboard.yml"
AUDIT_FINDINGS = PROJECT_ROOT / "docs" / "audit" / "audit-findings.yml"

ACTIVE_ACCEPTANCE_STATUSES = {
    "ready_for_acceptance",
    "needs_revision",
    "blocked",
}
ACTIVE_CHECK_STATUSES = {"pending", "in_progress", "blocked", "requires_user_action"}
ACTIVE_ACTION_STATUSES = {"open", "pending", "blocked", "requires_user_approval"}
PSEUDO_EMPTY_VALUES = {
    "отсутствуют",
    "нет",
    "блокеров нет",
    "рисков нет",
    "none",
    "no blockers",
    "no risks",
}
TECHNICAL_RE = re.compile(
    r"^([A-Z0-9_-]+|[a-z0-9_./:-]+|EP-\d{3}-[A-Z0-9-]+|VT-[A-Z0-9-]+)$"
)


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


def as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def pseudo_text(value: Any) -> bool:
    text = str(value or "").strip().strip(".:;!-—").lower()
    return text in PSEUDO_EMPTY_VALUES


def active_items(workbench: dict[str, Any]) -> list[dict[str, Any]]:
    items = workbench.get("active_review_items", [])
    return (
        [item for item in items if isinstance(item, dict)]
        if isinstance(items, list)
        else []
    )


def recently_accepted(workbench: dict[str, Any]) -> list[dict[str, Any]]:
    items = workbench.get("recently_accepted", [])
    return (
        [item for item in items if isinstance(item, dict)]
        if isinstance(items, list)
        else []
    )


def active_item_ids(workbench: dict[str, Any]) -> set[str]:
    return {str(item.get("id")) for item in active_items(workbench)}


def validate_required_files() -> list[str]:
    errors: list[str] = []
    for path in [WORKBENCH_YAML, WORKBENCH_MD]:
        if not path.exists():
            errors.append(f"Missing file: {rel(path)}")
    return errors


def expected_acceptance_ids() -> tuple[set[str], set[str]]:
    dashboard = load_root(ACCEPTANCE_DASHBOARD, "acceptance_dashboard")
    items = dashboard.get("items", [])
    active: set[str] = set()
    accepted: set[str] = set()
    for item in items if isinstance(items, list) else []:
        if not isinstance(item, dict):
            continue
        packet_id = str(item.get("packet_id") or "")
        decision = str(item.get("acceptance_decision") or "pending")
        status = str(item.get("status") or "")
        item_id = f"ACCEPTANCE-{packet_id}"
        if decision == "accepted":
            accepted.add(item_id)
        elif status in ACTIVE_ACCEPTANCE_STATUSES or decision in {
            "pending",
            "needs_revision",
        }:
            active.add(item_id)
    return active, accepted


def expected_manual_check_ids() -> set[str]:
    dashboard = load_root(VERIFICATION_DASHBOARD, "verification_dashboard")
    checks = dashboard.get("checks", [])
    expected: set[str] = set()
    for check in checks if isinstance(checks, list) else []:
        if not isinstance(check, dict):
            continue
        if (
            str(check.get("check_type") or "") != "automated_command"
            and str(check.get("status") or "") in ACTIVE_CHECK_STATUSES
        ):
            expected.add(f"VERIFICATION-{check.get('check_id')}")
    return expected


def expected_user_action_ids() -> set[str]:
    dashboard = load_root(USER_ACTION_DASHBOARD, "user_action_dashboard")
    actions = dashboard.get("actions", [])
    expected: set[str] = set()
    for action in actions if isinstance(actions, list) else []:
        if not isinstance(action, dict):
            continue
        if str(action.get("type") or "") == "audit_finding":
            continue
        if str(action.get("status") or "") in ACTIVE_ACTION_STATUSES:
            expected.add(f"USER-ACTION-{action.get('id')}")
    return expected


def expected_audit_ids() -> set[str]:
    if not AUDIT_FINDINGS.exists():
        return set()
    data = load_data(AUDIT_FINDINGS)
    findings = data.get("findings", []) if isinstance(data, dict) else []
    expected: set[str] = set()
    for finding in findings if isinstance(findings, list) else []:
        if not isinstance(finding, dict):
            continue
        status = str(finding.get("status") or "")
        severity = str(finding.get("severity") or "")
        if status in ACTIVE_ACTION_STATUSES and (
            severity in {"critical", "high"} or status == "requires_user_approval"
        ):
            expected.add(f"AUDIT-{finding.get('id')}")
    return expected


def validate_expected_items(workbench: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    item_ids = active_item_ids(workbench)
    expected_acceptance, accepted_acceptance = expected_acceptance_ids()
    for item_id in sorted(expected_acceptance):
        if item_id not in item_ids:
            errors.append(f"Active acceptance item missing: {item_id}")
    for item_id in sorted(accepted_acceptance):
        if item_id in item_ids:
            errors.append(
                f"Accepted packet is present in active_review_items: {item_id}"
            )
    accepted_history = {
        f"ACCEPTANCE-{item.get('packet_id')}" for item in recently_accepted(workbench)
    }
    for item_id in sorted(accepted_acceptance):
        if item_id not in accepted_history:
            errors.append(f"Accepted packet missing from recently_accepted: {item_id}")

    for item_id in sorted(expected_manual_check_ids()):
        if item_id not in item_ids:
            errors.append(f"Pending manual check missing: {item_id}")
    for item_id in sorted(expected_user_action_ids()):
        if item_id not in item_ids:
            errors.append(f"Open user action missing: {item_id}")
    for item_id in sorted(expected_audit_ids()):
        if item_id not in item_ids:
            errors.append(f"Critical/high audit finding missing: {item_id}")
    return errors


def validate_active_item_shape(workbench: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for item in active_items(workbench):
        item_id = item.get("id", "<missing id>")
        if not item.get("source_file"):
            errors.append(f"{item_id}: missing source_file")
        if not item.get("source_checksum_sha256"):
            errors.append(f"{item_id}: missing source_checksum_sha256")
        if item.get("type") == "acceptance":
            if not item.get("target_decision_file"):
                errors.append(
                    f"{item_id}: acceptance item missing target_decision_file"
                )
            fields = item.get("target_fields_to_fill")
            if not isinstance(fields, list) or not fields:
                errors.append(
                    f"{item_id}: acceptance item missing target_fields_to_fill"
                )
        for section in ["blockers", "risks"]:
            for value in as_list(item.get(section)):
                text = value.get("text") if isinstance(value, dict) else value
                if pseudo_text(text):
                    errors.append(f"{item_id}: pseudo value in {section}: {text}")
    return errors


def validate_user_owned_fields(value: Any, path: str = "workbench") -> list[str]:
    errors: list[str] = []
    if isinstance(value, dict):
        for key, item in value.items():
            if (
                key in {"accepted_by", "checked_by", "answered_by", "decided_by"}
                and item == "Codex"
            ):
                errors.append(f"{path}.{key} must not be Codex")
            errors.extend(validate_user_owned_fields(item, f"{path}.{key}"))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            errors.extend(validate_user_owned_fields(item, f"{path}[{index}]"))
    return errors


def validate_language(workbench: dict[str, Any]) -> list[str]:
    warnings: list[str] = []
    for item in active_items(workbench):
        for key in ["required_user_action"]:
            text = str(item.get(key) or "")
            if not text or any("а" <= char.lower() <= "я" for char in text):
                continue
            if TECHNICAL_RE.match(text):
                continue
            warnings.append(
                f"{item.get('id')}: user-facing text may need Russian: {key}"
            )
    return warnings


def main() -> int:
    errors = validate_required_files()
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    try:
        data = load_data(WORKBENCH_YAML)
    except Exception as exc:
        print(f"ERROR: cannot read {rel(WORKBENCH_YAML)}: {exc}", file=sys.stderr)
        return 1
    workbench = data.get("user_review_workbench", {}) if isinstance(data, dict) else {}
    if not isinstance(workbench, dict):
        print("ERROR: user_review_workbench root must be a mapping", file=sys.stderr)
        return 1

    errors.extend(validate_expected_items(workbench))
    errors.extend(validate_active_item_shape(workbench))
    errors.extend(validate_user_owned_fields(workbench))

    warnings = validate_language(workbench)
    for warning in warnings:
        print(f"WARNING: {warning}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("User review workbench validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
