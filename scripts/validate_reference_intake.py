#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

from reference_utils import load_data


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REFERENCE_DOCS = [
    Path("docs/reference-intake/README.md"),
    Path("docs/reference-intake/source-intake-policy.md"),
    Path("docs/reference-intake/source-authority-model.md"),
    Path("docs/reference-intake/intake-workflow.md"),
]
SCHEMA_PATH = Path("data/reference/manifests/intake-manifest.schema.yml")
INTAKE_LOG_PATH = Path("data/reference/manifests/intake-log.yml")
AUTHORITY_CATALOG_PATH = Path("data/reference/manifests/source-authority-catalog.yml")
INBOX_DIR = Path("data/reference/inbox")
RAW_DIR = Path("data/reference/raw")
MANDATORY_INTAKE_TEXT = (
    "Контур учета источников не создает нормативные правила и не подтверждает "
    "соответствие КСИ/ГЭСН/ФСНБ. Он только фиксирует поступление источника, "
    "его происхождение, версию, checksum, статус доверия и необходимость проверки."
)

REQUIRED_SCHEMA_FIELDS = {
    "source_id",
    "source_name",
    "source_type",
    "source_origin",
    "source_authority",
    "source_status",
    "version_label",
    "effective_date",
    "received_at",
    "file_path",
    "checksum_sha256",
    "checksum_status",
    "review_status",
    "review_required",
    "accepted_by",
    "accepted_at",
    "notes",
}
ENUMS = {
    "source_origin": {
        "official_public_source",
        "official_user_provided_file",
        "project_dictionary",
        "user_decision",
        "llm_generated",
        "forbidden",
    },
    "source_authority": {
        "official",
        "project_authorized",
        "user_asserted",
        "draft",
        "forbidden",
    },
    "source_status": {
        "inbox",
        "draft",
        "under_review",
        "accepted",
        "rejected",
        "forbidden",
        "requires_norm_review",
    },
    "checksum_status": {"missing", "calculated", "verified", "mismatch"},
    "review_status": {
        "not_reviewed",
        "pending_user_review",
        "accepted_by_user",
        "rejected_by_user",
        "requires_norm_review",
    },
}
OFFICIAL_CONFIRMATION_FIELDS = {
    "can_confirm_official_normative_data",
    "confirms_official_ksi",
    "confirms_official_gesn",
    "confirms_official_fsnb",
    "confirms_official_normative_data",
}
PROJECT_ONLY_ORIGINS = {"user_decision", "project_dictionary"}
ACCEPTED_SOURCE_STATUSES = {"accepted"}
ACCEPTED_REVIEW_STATUSES = {"accepted_by_user"}
CUSTOMER_SPECIFIC_PATTERNS = [
    re.compile(r"\bИНН\s*[0-9]{10}(?:[0-9]{2})?\b", re.IGNORECASE),
    re.compile(r"\bКПП\s*[0-9]{9}\b", re.IGNORECASE),
    re.compile(r"\bОГРН\s*[0-9]{13,15}\b", re.IGNORECASE),
    re.compile(r"\b(?:договор|счет|упд|накладн|акт|кс-2|кс-3)\s*(?:№|N|No\.?)?\s*[0-9]+", re.IGNORECASE),
    re.compile(r"\+7\s*\(?[0-9]{3}\)?\s*[0-9]", re.IGNORECASE),
    re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.IGNORECASE),
]


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def rel(root: Path, path: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def load_mapping(root: Path, path: Path, errors: list[str]) -> dict[str, Any]:
    full_path = root / path
    if not full_path.exists():
        errors.append(f"missing required file: {path}")
        return {}
    data = load_data(full_path)
    if not isinstance(data, dict):
        errors.append(f"{path}: file must contain a mapping")
        return {}
    return data


def source_is_accepted(source: dict[str, Any]) -> bool:
    return (
        source.get("source_status") in ACCEPTED_SOURCE_STATUSES
        or source.get("review_status") in ACCEPTED_REVIEW_STATUSES
    )


def truthy(value: Any) -> bool:
    return value is True or str(value).lower() in {"true", "yes", "1"}


def validate_docs(root: Path) -> list[str]:
    errors: list[str] = []
    mandatory_text_found = False
    for path in REFERENCE_DOCS:
        full_path = root / path
        if not full_path.exists():
            errors.append(f"missing reference-intake document: {path}")
            continue
        text = full_path.read_text(encoding="utf-8")
        if MANDATORY_INTAKE_TEXT in text:
            mandatory_text_found = True
    if not mandatory_text_found:
        errors.append("reference-intake docs must contain mandatory scope wording")
    return errors


def validate_schema(root: Path, errors: list[str]) -> None:
    schema = load_mapping(root, SCHEMA_PATH, errors)
    fields = schema.get("fields") if isinstance(schema.get("fields"), dict) else {}
    missing_fields = sorted(REQUIRED_SCHEMA_FIELDS - set(fields))
    if missing_fields:
        errors.append(f"{SCHEMA_PATH}: missing fields: {', '.join(missing_fields)}")
    enums = schema.get("enums") if isinstance(schema.get("enums"), dict) else {}
    for enum_name, expected_values in ENUMS.items():
        values = set(str(item) for item in as_list(enums.get(enum_name)))
        missing_values = sorted(expected_values - values)
        if missing_values:
            errors.append(
                f"{SCHEMA_PATH}: enum {enum_name} missing values: {', '.join(missing_values)}"
            )


def validate_authority_catalog(root: Path, errors: list[str]) -> None:
    catalog = load_mapping(root, AUTHORITY_CATALOG_PATH, errors)
    for origin in ENUMS["source_origin"]:
        if origin not in catalog:
            errors.append(f"{AUTHORITY_CATALOG_PATH}: missing authority category {origin}")
            continue
        entry = catalog.get(origin)
        if not isinstance(entry, dict):
            errors.append(f"{AUTHORITY_CATALOG_PATH}: {origin} must be a mapping")
            continue
        can_confirm = entry.get("can_confirm_official_normative_data")
        if origin in {"official_public_source", "official_user_provided_file"}:
            if can_confirm is not True:
                errors.append(f"{AUTHORITY_CATALOG_PATH}: {origin} must allow official confirmation")
        elif can_confirm is not False:
            errors.append(f"{AUTHORITY_CATALOG_PATH}: {origin} must not allow official confirmation")


def validate_reference_files(root: Path, allow_non_gitkeep_files: bool) -> list[str]:
    errors: list[str] = []
    for folder in [root / INBOX_DIR, root / RAW_DIR]:
        if not folder.exists():
            errors.append(f"missing reference folder: {rel(root, folder)}")
            continue
        for path in sorted(folder.rglob("*")):
            if path.is_dir():
                continue
            if path.name == ".gitkeep":
                continue
            if allow_non_gitkeep_files:
                continue
            errors.append(
                f"{rel(root, path)}: reference inbox/raw may contain only .gitkeep placeholders before explicit user-provided files"
            )
    return errors


def contains_customer_specific_data(path: Path) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8")
    return any(pattern.search(text) for pattern in CUSTOMER_SPECIFIC_PATTERNS)


def validate_source(source: dict[str, Any], errors: list[str]) -> None:
    source_id = str(source.get("source_id") or "<missing source_id>")
    origin = source.get("source_origin")
    authority = source.get("source_authority")
    status = source.get("source_status")
    review_status = source.get("review_status")
    checksum = source.get("checksum_sha256")
    checksum_status = source.get("checksum_status")

    for field_name, allowed_values in ENUMS.items():
        value = source.get(field_name)
        if value and str(value) not in allowed_values:
            errors.append(f"{source_id}: invalid {field_name}: {value}")

    if source_is_accepted(source):
        if not checksum:
            errors.append(f"{source_id}: accepted source requires checksum_sha256")
        if checksum_status not in {"calculated", "verified"}:
            errors.append(f"{source_id}: accepted source requires calculated or verified checksum_status")
        if not source.get("accepted_by") or not source.get("accepted_at"):
            errors.append(f"{source_id}: accepted source requires accepted_by and accepted_at")
    if source.get("accepted_by") == "Codex":
        errors.append(f"{source_id}: accepted_by must not be Codex")
    if origin == "llm_generated" and authority in {"official", "project_authorized"}:
        errors.append(f"{source_id}: llm_generated cannot be official or project_authorized")
    if (origin == "forbidden" or authority == "forbidden" or status == "forbidden") and source_is_accepted(source):
        errors.append(f"{source_id}: forbidden source cannot be accepted")
    if origin in PROJECT_ONLY_ORIGINS:
        for field_name in OFFICIAL_CONFIRMATION_FIELDS:
            if truthy(source.get(field_name)):
                errors.append(f"{source_id}: {origin} cannot confirm official KSI/GESN/FSNB data")
    if source.get("matching_rule_status") == "active" or truthy(source.get("active_matching_rule")):
        errors.append(f"{source_id}: reference-intake manifest must not create active matching rules")
    if source.get("review_required") is False and review_status in {"not_reviewed", "pending_user_review"}:
        errors.append(f"{source_id}: unreviewed source must keep review_required=true")


def validate_intake_log(root: Path, errors: list[str]) -> None:
    intake_log = load_mapping(root, INTAKE_LOG_PATH, errors)
    sources = as_list(intake_log.get("sources"))
    seen: set[str] = set()
    for item in sources:
        if not isinstance(item, dict):
            errors.append(f"{INTAKE_LOG_PATH}: each source must be a mapping")
            continue
        source_id = str(item.get("source_id") or "")
        if not source_id:
            errors.append(f"{INTAKE_LOG_PATH}: source_id is required")
        elif source_id in seen:
            errors.append(f"{INTAKE_LOG_PATH}: duplicate source_id: {source_id}")
        seen.add(source_id)
        validate_source(item, errors)
    for requirement in as_list(intake_log.get("data_requirements")):
        if not isinstance(requirement, dict):
            errors.append(f"{INTAKE_LOG_PATH}: data_requirements entries must be mappings")
            continue
        if not requirement.get("requirement_id"):
            errors.append(f"{INTAKE_LOG_PATH}: data requirement missing requirement_id")
        if requirement.get("status") != "pending_user_input":
            errors.append(
                f"{INTAKE_LOG_PATH}: data requirement status must remain pending_user_input until user input"
            )


def validate_project(root: Path, allow_non_gitkeep_files: bool = False) -> list[str]:
    errors: list[str] = []
    errors.extend(validate_docs(root))
    validate_schema(root, errors)
    validate_authority_catalog(root, errors)
    validate_intake_log(root, errors)
    errors.extend(validate_reference_files(root, allow_non_gitkeep_files))
    for path in [SCHEMA_PATH, INTAKE_LOG_PATH, AUTHORITY_CATALOG_PATH]:
        if contains_customer_specific_data(root / path):
            errors.append(f"{path}: manifest contains customer-specific data pattern")
    return errors


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate reference intake governance artifacts.")
    parser.add_argument("--project-root", default=str(PROJECT_ROOT), help=argparse.SUPPRESS)
    parser.add_argument(
        "--allow-non-gitkeep-reference-files",
        action="store_true",
        help=argparse.SUPPRESS,
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])
    root = Path(args.project_root).resolve()
    errors = validate_project(root, args.allow_non_gitkeep_reference_files)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Reference intake validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
