#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

from reference_utils import load_data


PROJECT_ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "docs/data-contribution/README.md",
    "docs/data-contribution/data-contribution-workflow.md",
    "docs/data-contribution/anonymization-pipeline.md",
    "docs/data-contribution/reidentification-risk-policy.md",
    "docs/data-contribution/commercial-aggregate-policy.md",
    "schemas/data-contribution/data-contribution-consent.schema.yml",
    "schemas/data-contribution/raw-purchase-event.schema.yml",
    "schemas/data-contribution/anonymized-purchase-signal.schema.yml",
    "schemas/data-contribution/commercial-price-aggregate.schema.yml",
    "examples/data-contribution/rebar-d12-synthetic.raw.example.yml",
    "examples/data-contribution/rebar-d12-synthetic-aggregate.example.yml",
    "docs/monthly/2026-08/monthly-plan.yml",
    "docs/monthly/2026-08/01-business-functional-requirements.md",
    "docs/monthly/2026-08/02-technical-specification.md",
    "docs/monthly/2026-08/03-test-protocol-data-contribution.md",
]

DEFAULT_FALSE_FLAGS = {
    "telemetry_enabled",
    "dataset_contribution_enabled",
    "external_upload_enabled",
    "ai_training_allowed",
    "commercial_use_allowed",
}

DIRECT_IDENTIFIER_FIELDS = {
    "customer_ref",
    "supplier_ref",
    "customer_name",
    "supplier_name",
    "inn",
    "kpp",
    "ogrn",
    "contract_id",
    "invoice_id",
    "address",
    "phone",
    "email",
}

EXACT_AGGREGATE_FIELDS = {
    "event_date",
    "transaction_date",
    "exact_date",
    "city",
    "exact_city",
    "address",
}

REAL_DATA_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in [
        r"\b(?:inn|kpp|ogrn)\b\s*[:=]",
        r"\b(?:contract|invoice)[_-]?id\b\s*[:=]",
        r"@[a-z0-9.-]+\.[a-z]{2,}",
        r"\+7[\s()0-9-]{7,}",
        r"\b\d{10,13}\b",
    ]
]

MONTHLY_REQUIRED_PHRASES = [
    "schema-first",
    "documentation-first",
    "default-off",
    "EP-024",
]


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(PROJECT_ROOT))
    except ValueError:
        return str(path)


def as_mapping(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def find_key_case_insensitive(mapping: dict[str, Any], key: str) -> Any:
    key_lower = key.lower()
    for current_key, value in mapping.items():
        if str(current_key).lower() == key_lower:
            return value
    return None


def iter_mapping_keys(value: Any) -> list[str]:
    keys: list[str] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            keys.append(str(key))
            keys.extend(iter_mapping_keys(nested))
    elif isinstance(value, list):
        for item in value:
            keys.extend(iter_mapping_keys(item))
    return keys


def load_yaml_mapping(root: Path, relative_path: str) -> dict[str, Any]:
    path = root / relative_path
    data = load_data(path)
    return as_mapping(data)


def validate_required_files(root: Path) -> list[str]:
    errors: list[str] = []
    for relative_path in REQUIRED_FILES:
        if not (root / relative_path).exists():
            errors.append(f"missing required data contribution artifact: {relative_path}")
    return errors


def validate_default_flags(
    record: dict[str, Any], label: str, required: set[str] | None = None
) -> list[str]:
    errors: list[str] = []
    required_flags = required or DEFAULT_FALSE_FLAGS
    for flag in sorted(required_flags):
        value = find_key_case_insensitive(record, flag)
        if value is not False:
            errors.append(f"{label}: {flag} must default to false")
    return errors


def validate_consent_schema(schema: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    defaults = as_mapping(schema.get("default_flags"))
    errors.extend(validate_default_flags(defaults, "consent default_flags"))
    notes = schema.get("notes")
    if not isinstance(notes, list) or not any(
        "Product use is not consent" in str(note) for note in notes
    ):
        errors.append("consent schema must state that product use is not consent")
    return errors


def validate_raw_event(record: dict[str, Any], label: str = "raw event") -> list[str]:
    errors: list[str] = []
    if not record:
        return [f"{label}: record is empty"]

    errors.extend(validate_default_flags(record, label))
    if record.get("source_status") != "synthetic":
        errors.append(f"{label}: source_status must be synthetic in EP-024")
    if record.get("data_classification") != "synthetic_example_only":
        errors.append(f"{label}: data_classification must be synthetic_example_only")
    if record.get("example_only") is not True:
        errors.append(f"{label}: example_only must be true")
    if record.get("derived_from_real_customer_data") is not False:
        errors.append(f"{label}: derived_from_real_customer_data must be false")
    if (record.get("customer_ref") or record.get("customer_name")) and record.get(
        "commercial_use_allowed"
    ) is True:
        errors.append(
            f"{label}: customer-specific raw event cannot be commercial_use_allowed"
        )
    if (record.get("supplier_ref") or record.get("supplier_name")) and record.get(
        "ai_training_allowed"
    ) is True:
        errors.append(
            f"{label}: supplier-specific raw event cannot be ai_training_allowed"
        )
    if record.get("external_upload_enabled") is not False:
        errors.append(f"{label}: external_upload_enabled must be false")
    return errors


def validate_anonymized_signal(
    record: dict[str, Any], label: str = "anonymized signal"
) -> list[str]:
    errors: list[str] = []
    keys = {key.lower() for key in iter_mapping_keys(record)}
    forbidden = sorted(keys & DIRECT_IDENTIFIER_FIELDS)
    if forbidden:
        errors.append(
            f"{label}: forbidden direct identifier fields present: {', '.join(forbidden)}"
        )
    if record.get("external_upload_enabled") is True:
        errors.append(f"{label}: external_upload_enabled must not be true")
    if record.get("dataset_contribution_enabled") is True and record.get(
        "reidentification_risk"
    ) != "low":
        errors.append(f"{label}: dataset contribution requires low risk")
    return errors


def is_bucketed_period(value: Any) -> bool:
    text = str(value or "")
    return bool(re.fullmatch(r"\d{4}-Q[1-4]|\d{4}-\d{2}", text))


def validate_commercial_aggregate(
    record: dict[str, Any], label: str = "commercial aggregate"
) -> list[str]:
    errors: list[str] = []
    if not record:
        return [f"{label}: record is empty"]

    if int(record.get("observations_count") or 0) < 10:
        errors.append(f"{label}: observations_count must be at least 10")
    if int(record.get("independent_customers_count") or 0) < 5:
        errors.append(f"{label}: independent_customers_count must be at least 5")
    if int(record.get("independent_suppliers_count") or 0) < 5:
        errors.append(f"{label}: independent_suppliers_count must be at least 5")
    if record.get("reidentification_risk") != "low":
        errors.append(f"{label}: reidentification_risk must be low")
    if record.get("source_status") not in {"synthetic", "approved_aggregate"}:
        errors.append(f"{label}: source_status must be synthetic or approved_aggregate")
    if record.get("derived_from_real_customer_data") is not False:
        errors.append(f"{label}: derived_from_real_customer_data must be false")
    if not is_bucketed_period(record.get("period_bucket")):
        errors.append(f"{label}: period_bucket must be bucketed, not exact date")

    keys = {key.lower() for key in iter_mapping_keys(record)}
    exact_fields = sorted(keys & EXACT_AGGREGATE_FIELDS)
    if exact_fields:
        errors.append(
            f"{label}: exact fields are forbidden in aggregate: {', '.join(exact_fields)}"
        )
    if record.get("commercial_use_allowed") is True and (
        record.get("data_classification") != "synthetic_aggregate_example"
        or record.get("aggregate_approved") is not True
    ):
        errors.append(
            f"{label}: commercial_use_allowed requires synthetic_aggregate_example and aggregate_approved=true"
        )
    return errors


def validate_no_real_data_patterns(root: Path) -> list[str]:
    errors: list[str] = []
    for relative_path in [
        "examples/data-contribution/rebar-d12-synthetic.raw.example.yml",
        "examples/data-contribution/rebar-d12-synthetic-aggregate.example.yml",
    ]:
        text = (root / relative_path).read_text(encoding="utf-8")
        for pattern in REAL_DATA_PATTERNS:
            if pattern.search(text):
                errors.append(f"{relative_path}: possible real/customer-specific value")
    return errors


def validate_monthly_docs(root: Path) -> list[str]:
    errors: list[str] = []
    monthly_dir = root / "docs" / "monthly" / "2026-08"
    combined = "\n".join(
        path.read_text(encoding="utf-8") for path in sorted(monthly_dir.glob("*"))
    )
    for phrase in MONTHLY_REQUIRED_PHRASES:
        if phrase not in combined:
            errors.append(f"docs/monthly/2026-08: missing phrase {phrase}")
    plan = load_yaml_mapping(root, "docs/monthly/2026-08/monthly-plan.yml").get(
        "monthly_plan", {}
    )
    plan = as_mapping(plan)
    tasks = plan.get("tasks")
    if not isinstance(tasks, list) or len(tasks) != 3:
        errors.append("docs/monthly/2026-08/monthly-plan.yml: requires exactly 3 tasks")
    elif any(as_mapping(task).get("planned_hours") != 15 for task in tasks):
        errors.append("docs/monthly/2026-08/monthly-plan.yml: each task must be 15 hours")
    defaults = as_mapping(plan.get("default_flags"))
    errors.extend(validate_default_flags(defaults, "monthly default_flags"))
    return errors


def validate_project(root: Path = PROJECT_ROOT) -> list[str]:
    errors: list[str] = []
    errors.extend(validate_required_files(root))
    if errors:
        return errors

    consent_schema = load_yaml_mapping(
        root, "schemas/data-contribution/data-contribution-consent.schema.yml"
    )
    raw_example = load_yaml_mapping(
        root, "examples/data-contribution/rebar-d12-synthetic.raw.example.yml"
    )
    anonymized_schema = load_yaml_mapping(
        root, "schemas/data-contribution/anonymized-purchase-signal.schema.yml"
    )
    aggregate_example = load_yaml_mapping(
        root, "examples/data-contribution/rebar-d12-synthetic-aggregate.example.yml"
    )

    errors.extend(validate_consent_schema(consent_schema))
    errors.extend(validate_raw_event(raw_example, "synthetic raw example"))
    errors.extend(validate_anonymized_signal(anonymized_schema, "anonymized schema"))
    errors.extend(validate_commercial_aggregate(aggregate_example, "synthetic aggregate"))
    errors.extend(validate_no_real_data_patterns(root))
    errors.extend(validate_monthly_docs(root))
    return errors


def main() -> int:
    errors = validate_project(PROJECT_ROOT)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Data contribution validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
