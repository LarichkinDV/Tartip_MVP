#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from reference_utils import load_data


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_MANIFEST = PROJECT_ROOT / "data" / "reference" / "manifests" / "source-manifest.yml"
RULES_DIR = PROJECT_ROOT / "rules" / "matching"

ACCEPTED_STATUSES = {"accepted", "raw_accepted", "normalized", "active", "trusted", "imported"}
NORMATIVE_FIELDS = {
    "gesn_norm",
    "norm_unit",
    "included_works",
    "excluded_works",
    "resource_composition",
    "technical_part_reference",
}
REQUIRED_EVIDENCE_FIELDS = {
    "ksi_result_code",
    "ksi_process_code",
    "work_type",
    "gesn_norm",
    "norm_unit",
    "included_works",
    "excluded_works",
    "resource_composition",
    "technical_part_reference",
}
PROJECT_ONLY_AUTHORITIES = {"project_authoritative", "project_authoritative_only"}


def is_accepted(source: dict[str, Any]) -> bool:
    status = str(source.get("status") or source.get("import_status") or "").lower()
    return status in ACCEPTED_STATUSES


def is_inbox_path(value: Any) -> bool:
    if not value:
        return False
    return str(value).startswith("data/reference/inbox/")


def evidence_missing(value: Any) -> bool:
    if not isinstance(value, dict):
        return True
    if value.get("evidence_status") in {"missing", "required", None}:
        return True
    return not value.get("source_id") or not value.get("normalized_record_id")


def validate_sources(sources: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    for source in sources:
        source_id = source.get("source_id", "<missing source_id>")
        origin = source.get("source_origin")
        authority = source.get("source_authority")
        checksum = source.get("checksum_sha256")
        if origin == "llm_generated" and authority != "forbidden":
            errors.append(f"{source_id}: llm_generated source_authority must be forbidden")
        if is_accepted(source) and not checksum:
            errors.append(f"{source_id}: accepted sources require checksum_sha256")
        if is_accepted(source) and is_inbox_path(source.get("local_original_path")):
            errors.append(f"{source_id}: inbox files are not trusted until copied to raw with checksum")
        if is_accepted(source) and is_inbox_path(source.get("raw_immutable_path")):
            errors.append(f"{source_id}: raw_immutable_path cannot point to inbox")
    return errors


def validate_rules(source_by_id: dict[str, dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    for rule_path in sorted(list(RULES_DIR.glob("*.yaml")) + list(RULES_DIR.glob("*.yml"))):
        rule = load_data(rule_path)
        if not isinstance(rule, dict):
            errors.append(f"{rule_path}: rule must be a mapping")
            continue
        status = rule.get("status")
        evidence = rule.get("evidence") or {}
        missing_fields = [field for field in REQUIRED_EVIDENCE_FIELDS if evidence_missing(evidence.get(field))]
        if status == "active" and missing_fields:
            errors.append(
                f"{rule_path}: active rule has missing evidence fields: {', '.join(missing_fields)}"
            )
        for field_name, evidence_item in evidence.items():
            if not isinstance(evidence_item, dict):
                continue
            source_id = evidence_item.get("source_id")
            if not source_id:
                continue
            source = source_by_id.get(str(source_id))
            if source is None:
                errors.append(f"{rule_path}: evidence {field_name} references unknown source {source_id}")
                continue
            origin = source.get("source_origin")
            authority = source.get("source_authority")
            if origin == "llm_generated" or authority == "forbidden":
                errors.append(f"{rule_path}: evidence {field_name} uses forbidden source {source_id}")
            if field_name in NORMATIVE_FIELDS and (
                origin == "user_decision" or authority in PROJECT_ONLY_AUTHORITIES
            ):
                errors.append(
                    f"{rule_path}: user/project decision cannot validate normative field {field_name}"
                )
            if is_inbox_path(source.get("local_original_path")) or is_inbox_path(
                source.get("raw_immutable_path")
            ):
                errors.append(f"{rule_path}: evidence {field_name} points to an inbox source")
    return errors


def main() -> int:
    if not SOURCE_MANIFEST.exists():
        print(f"ERROR: source manifest not found: {SOURCE_MANIFEST}", file=sys.stderr)
        return 1

    manifest = load_data(SOURCE_MANIFEST)
    sources = manifest.get("sources", []) if isinstance(manifest, dict) else []
    if not isinstance(sources, list):
        print("ERROR: source-manifest.yml sources must be a list", file=sys.stderr)
        return 1

    source_by_id = {
        str(source.get("source_id")): source
        for source in sources
        if isinstance(source, dict) and source.get("source_id")
    }
    errors = validate_sources([source for source in sources if isinstance(source, dict)])
    errors.extend(validate_rules(source_by_id))

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("Reference source validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
