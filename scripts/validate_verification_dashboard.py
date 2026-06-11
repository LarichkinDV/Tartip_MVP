#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

from reference_utils import load_data


PROJECT_ROOT = Path(__file__).resolve().parents[1]
YAML_PATH = PROJECT_ROOT / "docs" / "verification-dashboard.yml"
MARKDOWN_PATH = PROJECT_ROOT / "docs" / "verification-dashboard.md"
PROTOCOL_PATH = (
    PROJECT_ROOT
    / "docs"
    / "monthly"
    / "2026-06"
    / "03-test-protocol-reference-data-governance.md"
)

ALLOWED_STATUSES = {
    "pending",
    "in_progress",
    "passed",
    "failed",
    "blocked",
    "requires_user_action",
    "not_applicable",
}
ALLOWED_TYPES = {
    "automated_command",
    "manual_command",
    "manual_document_review",
    "manual_functional_review",
    "manual_normative_review",
    "manual_acceptance_review",
}
MANUAL_TYPES = {
    check_type for check_type in ALLOWED_TYPES if check_type.startswith("manual_")
}
ALLOWED_SCOPE_TYPES = {"monthly_block"}
MONTHLY_SCOPE_ID = "MONTHLY-2026-06"
LEGACY_MONTHLY_PACKET = "EP-006-MONTHLY-PLANNING-AND-DEFENSE"


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


def load_dashboard() -> dict[str, Any]:
    if not YAML_PATH.exists():
        raise ValueError(f"Missing verification dashboard YAML: {rel(YAML_PATH)}")
    data = load_data(YAML_PATH)
    dashboard = data.get("verification_dashboard", {}) if isinstance(data, dict) else {}
    if not isinstance(dashboard, dict):
        raise ValueError(
            "docs/verification-dashboard.yml must contain verification_dashboard mapping"
        )
    return dashboard


def protocol_check_ids() -> set[str]:
    if not PROTOCOL_PATH.exists():
        return set()
    text = PROTOCOL_PATH.read_text(encoding="utf-8")
    return set(re.findall(r"\bVT-[A-Z0-9-]+\b", text))


def validate_summary(
    dashboard: dict[str, Any], checks: list[dict[str, Any]]
) -> list[str]:
    errors: list[str] = []
    summary = (
        dashboard.get("summary") if isinstance(dashboard.get("summary"), dict) else {}
    )
    actual = {status: 0 for status in ALLOWED_STATUSES}
    for check in checks:
        status = str(check.get("status") or "pending")
        actual[status if status in actual else "pending"] += 1
    for status in [
        "pending",
        "in_progress",
        "passed",
        "failed",
        "blocked",
        "requires_user_action",
        "not_applicable",
    ]:
        if summary.get(status) != actual[status]:
            errors.append(
                f"summary.{status}={summary.get(status)} does not match actual {actual[status]}"
            )
    return errors


def artifact_paths(check: dict[str, Any]) -> list[str]:
    paths: list[str] = []
    for artifact in as_list(check.get("artifacts")):
        if isinstance(artifact, dict) and artifact.get("path"):
            paths.append(str(artifact["path"]))
        elif isinstance(artifact, str):
            paths.append(artifact)
    return paths


def validate_check(check: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    check_id = str(check.get("check_id") or "<missing check_id>")
    for field in ["check_id", "title", "check_type", "priority", "status"]:
        if not check.get(field):
            errors.append(f"{check_id}: missing {field}")
    check_type = str(check.get("check_type") or "")
    status = str(check.get("status") or "")
    if check_type and check_type not in ALLOWED_TYPES:
        errors.append(f"{check_id}: unsupported check_type={check_type}")
    if status and status not in ALLOWED_STATUSES:
        errors.append(f"{check_id}: unsupported status={status}")
    scope_type = str(check.get("scope_type") or "")
    scope_id = str(check.get("scope_id") or "")
    related_packet = str(check.get("related_packet") or "")
    if scope_type and scope_type not in ALLOWED_SCOPE_TYPES:
        errors.append(f"{check_id}: unsupported scope_type={scope_type}")
    if scope_type == "monthly_block":
        if scope_id != MONTHLY_SCOPE_ID:
            errors.append(f"{check_id}: monthly_block requires scope_id={MONTHLY_SCOPE_ID}")
        if related_packet:
            errors.append(f"{check_id}: monthly_block must not use related_packet={related_packet}")
        if check.get("legacy_related_packet") != LEGACY_MONTHLY_PACKET:
            errors.append(f"{check_id}: monthly_block must preserve legacy_related_packet={LEGACY_MONTHLY_PACKET}")
    elif related_packet == LEGACY_MONTHLY_PACKET:
        errors.append(f"{check_id}: legacy monthly packet must be represented as monthly_block scope")
    if not as_list(check.get("how_to_check")):
        errors.append(f"{check_id}: missing how_to_check")
    if not as_list(check.get("expected_result")):
        errors.append(f"{check_id}: missing expected_result")
    user_result = (
        check.get("user_result") if isinstance(check.get("user_result"), dict) else {}
    )
    checked_by = str(user_result.get("checked_by") or "")
    result = str(user_result.get("result") or "")
    checked_at = str(user_result.get("checked_at") or "")
    if checked_by == "Codex":
        errors.append(f"{check_id}: checked_by must not be Codex")
    if check_type in MANUAL_TYPES and checked_by == "Codex":
        errors.append(f"{check_id}: manual check cannot be closed by Codex")
    if user_result.get("checked") is True and not checked_by:
        errors.append(f"{check_id}: checked=true requires checked_by")
    if result in {"passed", "failed"} and not checked_at:
        errors.append(f"{check_id}: result={result} requires checked_at")
    if result and result not in {"passed", "failed"}:
        errors.append(f"{check_id}: unsupported user result={result}")
    if (
        check_type == "automated_command"
        and status == "passed"
        and not as_list(check.get("commands"))
    ):
        errors.append(f"{check_id}: automated passed check requires command evidence")
    if status != "blocked":
        for path in artifact_paths(check):
            if path.startswith("http://") or path.startswith("https://"):
                continue
            if not (PROJECT_ROOT / path).exists():
                errors.append(f"{check_id}: artifact path does not exist: {path}")
    return errors


def validate_dashboard(project_root: Path | None = None) -> list[str]:
    del project_root
    errors: list[str] = []
    if not MARKDOWN_PATH.exists():
        errors.append(f"Missing verification dashboard Markdown: {rel(MARKDOWN_PATH)}")
    try:
        dashboard = load_dashboard()
    except ValueError as exc:
        return [str(exc)]
    checks_value = dashboard.get("checks", [])
    if not isinstance(checks_value, list):
        return ["verification_dashboard.checks must be a list"]
    checks = [check for check in checks_value if isinstance(check, dict)]
    if len(checks) != len(checks_value):
        errors.append("verification_dashboard.checks contains non-mapping entries")
    seen: set[str] = set()
    for check in checks:
        check_id = str(check.get("check_id") or "")
        if check_id in seen:
            errors.append(f"duplicate check_id: {check_id}")
        if check_id:
            seen.add(check_id)
        errors.extend(validate_check(check))
    errors.extend(validate_summary(dashboard, checks))
    protocol_ids = protocol_check_ids()
    if not PROTOCOL_PATH.exists():
        errors.append(f"Missing monthly test protocol: {rel(PROTOCOL_PATH)}")
    else:
        missing = sorted(protocol_ids - seen)
        for check_id in missing:
            errors.append(
                f"protocol check missing from verification dashboard: {check_id}"
            )
    return errors


def main() -> int:
    errors = validate_dashboard(PROJECT_ROOT)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Verification dashboard validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
