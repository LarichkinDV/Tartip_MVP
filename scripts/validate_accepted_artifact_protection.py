#!/usr/bin/env python3
from __future__ import annotations

import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

from reference_utils import load_data


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = PROJECT_ROOT / "docs" / "artifact-registry.yml"
ACCEPTANCE_DIR = PROJECT_ROOT / "docs" / "acceptance"
PACKETS_PATH = PROJECT_ROOT / "docs" / "grace" / "execution-packets.xml"
CHANGE_REQUESTS_PATH = PROJECT_ROOT / "docs" / "protected-artifact-change-requests.yml"

ALLOWED_SOURCE_CATEGORIES = {
    "source_manual",
    "source_policy",
    "source_grace",
    "source_acceptance",
    "source_registry",
    "generated_dashboard",
    "generated_audit",
    "generated_workbench",
    "generated_report",
    "code",
    "test",
    "script",
    "reference_data",
    "unknown",
}
ALLOWED_PROTECTION_STATUSES = {
    "protected",
    "not_protected_generated",
    "not_protected_code",
    "not_protected_pending",
    "requires_classification",
}
ALLOWED_CHANGE_REQUEST_STATUSES = {
    "draft",
    "requires_user_approval",
    "approved",
    "rejected",
    "applied",
}
USER_OWNED_FIELDS = {
    "acceptance_decision",
    "accepted_by",
    "accepted_at",
    "comments",
}
GENERATED_ARTIFACTS = {
    "docs/acceptance-dashboard.md",
    "docs/acceptance-dashboard.yml",
    "docs/user-action-dashboard.md",
    "docs/user-action-dashboard.yml",
    "docs/user-review-workbench.md",
    "docs/user-review-workbench.yml",
    "docs/verification-dashboard.md",
    "docs/verification-dashboard.yml",
}


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


def load_registry() -> list[dict[str, Any]]:
    if not REGISTRY_PATH.exists():
        raise ValueError(f"missing {rel(REGISTRY_PATH)}")
    data = load_data(REGISTRY_PATH)
    artifacts = data.get("artifacts", []) if isinstance(data, dict) else []
    if not isinstance(artifacts, list):
        raise ValueError("docs/artifact-registry.yml must contain artifacts list")
    return [item for item in artifacts if isinstance(item, dict)]


def acceptance_fields(path: Path) -> dict[str, str]:
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


def accepted_acceptance_reports() -> dict[str, dict[str, str]]:
    reports: dict[str, dict[str, str]] = {}
    for path in sorted(ACCEPTANCE_DIR.glob("EP-*.acceptance.md")):
        fields = acceptance_fields(path)
        if (
            fields.get("acceptance_decision") == "accepted"
            and fields.get("accepted_by")
            and fields.get("accepted_by") != "Codex"
        ):
            reports[rel(path)] = fields
    return reports


def protection_block(artifact: dict[str, Any]) -> dict[str, Any]:
    protection = artifact.get("protection")
    return protection if isinstance(protection, dict) else {}


def validate_change_requests(errors: list[str]) -> set[str]:
    approved: set[str] = set()
    if not CHANGE_REQUESTS_PATH.exists():
        errors.append(f"missing change request registry: {rel(CHANGE_REQUESTS_PATH)}")
        return approved
    data = load_data(CHANGE_REQUESTS_PATH)
    root = (
        data.get("protected_artifact_change_requests", {})
        if isinstance(data, dict)
        else {}
    )
    if not isinstance(root, dict):
        errors.append("protected_artifact_change_requests root must be a mapping")
        return approved
    if root.get("schema_version") != 1:
        errors.append("protected artifact change request schema_version must be 1")
    requests = root.get("requests", [])
    if not isinstance(requests, list):
        errors.append("protected artifact change requests must contain requests list")
        return approved
    for request in requests:
        if not isinstance(request, dict):
            errors.append("change request entry must be a mapping")
            continue
        request_id = str(request.get("id") or "<missing id>")
        status = str(request.get("status") or "")
        if status not in ALLOWED_CHANGE_REQUEST_STATUSES:
            errors.append(f"{request_id}: invalid change request status {status}")
        artifact_path = str(request.get("protected_artifact") or "")
        if not artifact_path:
            errors.append(f"{request_id}: missing protected_artifact")
        approval = (
            request.get("user_approval")
            if isinstance(request.get("user_approval"), dict)
            else {}
        )
        if approval.get("approved_by") == "Codex":
            errors.append(f"{request_id}: approved_by must not be Codex")
        commands = request.get("verification_commands")
        if not isinstance(commands, list):
            errors.append(f"{request_id}: verification_commands must be a list")
        if status in {"approved", "applied"} and artifact_path:
            approved.add(artifact_path)
    return approved


def ep010_expected_artifacts() -> set[str]:
    if not PACKETS_PATH.exists():
        return set()
    root = ET.parse(PACKETS_PATH).getroot()
    result: set[str] = set()
    for packet in root.findall("Packet"):
        packet_id = str(packet.attrib.get("id") or "")
        if not packet_id.startswith("EP-010-"):
            continue
        expected = packet.find("ExpectedArtifacts")
        if expected is None:
            continue
        for artifact in expected.findall("Artifact"):
            path = (artifact.text or "").strip()
            if path:
                result.add(path)
    return result


def validate_user_owned_acceptance_fields(errors: list[str]) -> None:
    for path in ACCEPTANCE_DIR.glob("EP-*.acceptance.md"):
        fields = acceptance_fields(path)
        for field in USER_OWNED_FIELDS:
            if fields.get(field) == "Codex":
                errors.append(f"{rel(path)}: {field} must not be Codex")


def validate_artifacts(
    errors: list[str],
    warnings: list[str],
    artifacts: list[dict[str, Any]],
    accepted_reports: dict[str, dict[str, str]],
    approved_change_requests: set[str],
) -> None:
    by_path = {str(item.get("path")): item for item in artifacts if item.get("path")}

    for report_path in sorted(accepted_reports):
        artifact = by_path.get(report_path)
        if not artifact:
            errors.append(
                f"accepted acceptance report is not registered: {report_path}"
            )
            continue
        protection = protection_block(artifact)
        if protection.get("protection_status") != "protected":
            errors.append(f"{report_path}: accepted report must be protected")
        if protection.get("source_category") != "source_acceptance":
            errors.append(f"{report_path}: accepted report must be source_acceptance")
        if protection.get("change_requires_user_approval") is not True:
            errors.append(
                f"{report_path}: accepted report requires user approval for changes"
            )

    for artifact in artifacts:
        artifact_id = str(artifact.get("artifact_id") or "<missing artifact_id>")
        path = str(artifact.get("path") or "")
        protection = protection_block(artifact)
        status = str(protection.get("protection_status") or "")
        category = str(protection.get("source_category") or "")
        if not protection:
            errors.append(f"{artifact_id}: missing protection block")
            continue
        if status not in ALLOWED_PROTECTION_STATUSES:
            errors.append(f"{artifact_id}: invalid protection_status {status}")
        if category not in ALLOWED_SOURCE_CATEGORIES:
            errors.append(f"{artifact_id}: invalid source_category {category}")
        if status == "protected":
            if protection.get("change_requires_user_approval") is not True:
                errors.append(
                    f"{artifact_id}: protected artifact requires user approval"
                )
            if category == "generated_dashboard":
                errors.append(
                    f"{artifact_id}: protected artifact must not be generated_dashboard"
                )
        if status == "requires_classification":
            if str(artifact.get("status") or "") in {"planned", "blocked"}:
                warnings.append(f"{artifact_id}: future artifact requires classification")
            else:
                errors.append(f"{artifact_id}: active artifact requires classification")
        if path in GENERATED_ARTIFACTS or category in {
            "generated_dashboard",
            "generated_audit",
            "generated_workbench",
            "generated_report",
        }:
            if status == "protected":
                errors.append(f"{artifact_id}: generated artifact must not be protected")
            for field in ["generator", "derived_from", "regeneration_command"]:
                if not protection.get(field):
                    errors.append(f"{artifact_id}: generated artifact missing {field}")

    protected_paths = {
        str(artifact.get("path"))
        for artifact in artifacts
        if protection_block(artifact).get("protection_status") == "protected"
    }
    for path in sorted(ep010_expected_artifacts() & protected_paths):
        if path not in approved_change_requests:
            errors.append(
                "EP-010 cannot change protected accepted artifact without approved "
                f"change request: {path}"
            )


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    try:
        artifacts = load_registry()
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    accepted_reports = accepted_acceptance_reports()
    approved_change_requests = validate_change_requests(errors)
    validate_user_owned_acceptance_fields(errors)
    validate_artifacts(
        errors,
        warnings,
        artifacts,
        accepted_reports,
        approved_change_requests,
    )

    for warning in warnings:
        print(f"WARNING: {warning}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Accepted artifact protection validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
