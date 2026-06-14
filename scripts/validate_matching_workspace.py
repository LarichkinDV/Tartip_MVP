#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

from reference_utils import load_data


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCENARIO = (
    PROJECT_ROOT
    / "examples"
    / "vertical-scenarios"
    / "partition-brick-120-reinf.workspace.yml"
)

REQUIRED_FILES = [
    "docs/matching-workspace/README.md",
    "docs/matching-workspace/evidence-gated-workflow.md",
    "schemas/domain/matching-workspace-session.schema.yml",
    "schemas/domain/matching-workspace-group.schema.yml",
    "schemas/domain/evidence-slot.schema.yml",
    "schemas/domain/calculation-unit-candidate.schema.yml",
    "schemas/domain/work-quantity.schema.yml",
    "schemas/domain/work-package.schema.yml",
    "schemas/domain/actual-record.schema.yml",
    "schemas/domain/plan-fact-comparison.schema.yml",
    "examples/vertical-scenarios/partition-brick-120-reinf.workspace.yml",
    "docs/monthly/2026-09/monthly-plan.yml",
    "docs/monthly/2026-09/01-business-functional-requirements.md",
    "docs/monthly/2026-09/02-technical-specification.md",
    "docs/monthly/2026-09/03-test-protocol-matching-workspace.md",
]

OFFICIAL_TARGET_FIELDS = {
    "ksi_result_code",
    "gesn_norm_code",
    "fsnb_version",
    "normative_unit",
    "work_composition",
    "resource_composition",
}

OFFICIAL_SOURCE_ORIGINS = {
    "official_public_source",
    "official_user_provided_file",
}

CODE_LIKE_RE = re.compile(
    r"(?:ГЭСН|ФЕР|КСИ|ФСНБ|GESN|FER|KSI|FSNB)[\s_-]*\d",
    re.IGNORECASE,
)


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(PROJECT_ROOT))
    except ValueError:
        return str(path)


def as_mapping(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def iter_items(value: Any, path: str = "") -> list[tuple[str, Any]]:
    items: list[tuple[str, Any]] = [(path, value)]
    if isinstance(value, dict):
        for key, nested in value.items():
            child_path = f"{path}.{key}" if path else str(key)
            items.extend(iter_items(nested, child_path))
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            child_path = f"{path}[{index}]" if path else f"[{index}]"
            items.extend(iter_items(nested, child_path))
    return items


def contains_key(value: Any, target_key: str) -> bool:
    target_lower = target_key.lower()
    if isinstance(value, dict):
        return any(str(key).lower() == target_lower for key in value)
    return False


def values_by_key(value: Any, key_name: str) -> list[Any]:
    key_lower = key_name.lower()
    result: list[Any] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            if str(key).lower() == key_lower:
                result.append(nested)
            result.extend(values_by_key(nested, key_name))
    elif isinstance(value, list):
        for item in value:
            result.extend(values_by_key(item, key_name))
    return result


def mapping_has_official_accepted_source(mapping: dict[str, Any]) -> bool:
    return (
        mapping.get("source_origin") in OFFICIAL_SOURCE_ORIGINS
        and mapping.get("source_authority") in {"official", "project_authorized"}
        and mapping.get("review_status") == "accepted_by_user"
    )


def target_is_official_field(target_field: Any) -> bool:
    text = str(target_field or "")
    return text in OFFICIAL_TARGET_FIELDS or any(
        marker in text
        for marker in [
            "ksi",
            "gesn",
            "fsnb",
            "normative",
            "work_composition",
            "resource_composition",
        ]
    )


def validate_required_files(root: Path = PROJECT_ROOT) -> list[str]:
    errors: list[str] = []
    for relative_path in REQUIRED_FILES:
        if not (root / relative_path).exists():
            errors.append(f"missing required matching workspace artifact: {relative_path}")
    return errors


def validate_forbidden_edges(workspace: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for path, value in iter_items(workspace):
        if not isinstance(value, dict):
            continue
        path_lower = path.lower()
        if "model_element" in path_lower and contains_key(value, "gesn_norm_id"):
            errors.append(f"{path}: model element must not reference gesn_norm_id")
        if "ksi_result_code" in path_lower and contains_key(value, "gesn_norm_id"):
            errors.append(f"{path}: ksi result code must not reference gesn_norm_id")
        if "gesn_norm" in path_lower and contains_key(value, "schedule_task_id"):
            errors.append(f"{path}: candidate norm must not reference schedule_task_id")
        if "calculation_unit" in path_lower and contains_key(value, "actual_record_id"):
            errors.append(
                f"{path}: calculation unit candidate must not reference actual_record_id"
            )
    return errors


def validate_status_gates(workspace: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if workspace.get("status") == "active":
        errors.append("workspace status active is forbidden")
    if workspace.get("normative_status") != "not_active":
        errors.append("normative_status must be not_active")
    if workspace.get("activation_allowed") is not False:
        errors.append("workspace activation_allowed must be false")
    if workspace.get("evidence_status") == "missing_official_sources" and workspace.get(
        "status"
    ) == "active":
        errors.append("active workspace is forbidden when evidence is missing")

    for path, value in iter_items(workspace):
        if path.endswith(".status") and value == "active":
            errors.append(f"{path}: active status is forbidden in draft workspace")
        if path.endswith(".activation_allowed") and value is True:
            errors.append(f"{path}: activation_allowed true is forbidden")
        if path.endswith(".accepted_by") and value == "Codex":
            errors.append(f"{path}: accepted_by must not be Codex")
    return errors


def validate_evidence_slots(workspace: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    slots = as_list(workspace.get("evidence_slots"))
    for slot in slots:
        if not isinstance(slot, dict):
            errors.append("evidence_slots entries must be mappings")
            continue
        slot_id = str(slot.get("slot_id") or "<missing slot_id>")
        origin = slot.get("source_origin")
        authority = slot.get("source_authority")
        target_field = slot.get("target_field")
        if origin == "llm_generated":
            errors.append(f"{slot_id}: source_origin=llm_generated is forbidden")
        if authority == "forbidden":
            errors.append(f"{slot_id}: source_authority=forbidden is forbidden")
        if origin == "user_decision" and target_is_official_field(target_field):
            errors.append(
                f"{slot_id}: user_decision cannot confirm official classifier or normative field"
            )
        if slot.get("requires_official_source") is True and slot.get("value") is not None:
            if not mapping_has_official_accepted_source(slot):
                errors.append(
                    f"{slot_id}: official field value requires accepted official source review"
                )
        if slot.get("activation_allowed") is not False:
            errors.append(f"{slot_id}: activation_allowed must be false")
    return errors


def validate_code_like_values(workspace: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for path, value in iter_items(workspace):
        if not isinstance(value, dict):
            continue
        for key, nested in value.items():
            key_text = str(key).lower()
            if key_text == "question_id" or key_text.endswith("_id"):
                continue
            if not isinstance(nested, str) or not CODE_LIKE_RE.search(nested):
                continue
            if not mapping_has_official_accepted_source(value):
                errors.append(
                    f"{path}.{key}: code-like value requires accepted official source review"
                )
    return errors


def validate_work_package_chain(workspace: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    packages = {
        str(item.get("work_package_id")): item
        for item in as_list(workspace.get("work_packages"))
        if isinstance(item, dict) and item.get("work_package_id")
    }
    package_ids = set(packages)
    if not package_ids:
        errors.append("workspace requires at least one WorkPackage")

    for quantity in as_list(workspace.get("work_quantities")):
        if not isinstance(quantity, dict):
            continue
        quantity_id = str(quantity.get("work_quantity_id") or "<missing work_quantity_id>")
        if quantity.get("work_package_id") not in package_ids:
            errors.append(f"{quantity_id}: WorkQuantity must target a WorkPackage")

    for task in as_list(workspace.get("schedule_tasks")):
        if not isinstance(task, dict):
            continue
        task_id = str(task.get("schedule_task_id") or "<missing schedule_task_id>")
        if task.get("work_package_id") not in package_ids:
            errors.append(f"{task_id}: ScheduleTask must be linked through WorkPackage")
        if "gesn_norm_id" in task:
            errors.append(f"{task_id}: ScheduleTask must not reference candidate norm")

    for record in as_list(workspace.get("actual_records")):
        if not isinstance(record, dict):
            continue
        record_id = str(record.get("actual_record_id") or "<missing actual_record_id>")
        has_work_package = bool(record.get("work_package_id"))
        has_zone = bool(record.get("zone_id") or record.get("capture_zone_id"))
        has_model_only = bool(record.get("model_element_id")) and not (
            has_work_package or has_zone
        )
        if record.get("work_package_id") not in package_ids:
            errors.append(f"{record_id}: ActualRecord must target a WorkPackage")
        if has_model_only:
            errors.append(
                f"{record_id}: ActualRecord must not use only model_element_id as production context"
            )

    for comparison in as_list(workspace.get("plan_fact_comparisons")):
        if not isinstance(comparison, dict):
            continue
        comparison_id = str(comparison.get("comparison_id") or "<missing comparison_id>")
        if comparison.get("work_package_id") not in package_ids:
            errors.append(f"{comparison_id}: PlanFactComparison must keep WorkPackage context")
    return errors


def validate_matching_rules(workspace: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for rule in as_list(workspace.get("matching_rules")):
        if not isinstance(rule, dict):
            continue
        rule_id = str(rule.get("rule_id") or "<missing rule_id>")
        if rule.get("status") == "active":
            errors.append(f"{rule_id}: active matching rules are forbidden in EP-025")
    return errors


def validate_workspace(workspace: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    errors.extend(validate_forbidden_edges(workspace))
    errors.extend(validate_status_gates(workspace))
    errors.extend(validate_evidence_slots(workspace))
    errors.extend(validate_code_like_values(workspace))
    errors.extend(validate_work_package_chain(workspace))
    errors.extend(validate_matching_rules(workspace))
    return errors


def validate_workspace_file(path: Path) -> list[str]:
    data = load_data(path)
    if not isinstance(data, dict):
        return [f"{rel(path)}: workspace file must contain a mapping"]
    return validate_workspace(data)


def validate_project(root: Path = PROJECT_ROOT) -> list[str]:
    errors = validate_required_files(root)
    scenario = root / "examples/vertical-scenarios/partition-brick-120-reinf.workspace.yml"
    if scenario.exists():
        errors.extend(validate_workspace_file(scenario))
    return errors


def main(argv: list[str]) -> int:
    target = Path(argv[1]) if len(argv) > 1 else DEFAULT_SCENARIO
    if not target.is_absolute():
        target = PROJECT_ROOT / target
    errors = validate_project(PROJECT_ROOT)
    if target != DEFAULT_SCENARIO and target.exists():
        errors.extend(validate_workspace_file(target))
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Matching workspace validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
