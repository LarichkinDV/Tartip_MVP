from __future__ import annotations

import copy
import importlib.util
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT_ROOT / "scripts" / "validate_matching_workspace.py"
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
SPEC = importlib.util.spec_from_file_location("validate_matching_workspace", SCRIPT)
assert SPEC is not None
assert SPEC.loader is not None
validate_matching_workspace = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = validate_matching_workspace
SPEC.loader.exec_module(validate_matching_workspace)


def valid_workspace() -> dict:
    return {
        "workspace_id": "W",
        "status": "draft_requires_data",
        "normative_status": "not_active",
        "evidence_status": "missing_official_sources",
        "activation_allowed": False,
        "model_group": {
            "model_elements": [{"model_element_id": "ME-1"}],
        },
        "ksi_result_code": {
            "value": None,
            "requires_official_source": True,
            "review_status": "pending_user_input",
            "activation_allowed": False,
        },
        "calculation_unit_candidate": {
            "candidate_id": "CU-1",
            "status": "draft_requires_data",
        },
        "evidence_slots": [
            {
                "slot_id": "ES-1",
                "target_field": "gesn_norm_code",
                "requires_official_source": True,
                "value": None,
                "source_origin": "missing",
                "source_authority": "missing",
                "review_status": "pending_user_input",
                "activation_allowed": False,
            }
        ],
        "work_quantities": [
            {"work_quantity_id": "WQ-1", "work_package_id": "WP-1"}
        ],
        "work_packages": [
            {
                "work_package_id": "WP-1",
                "work_quantity_ids": ["WQ-1"],
                "schedule_task_ids": ["ST-1"],
                "actual_record_ids": ["AR-1"],
            }
        ],
        "schedule_tasks": [
            {"schedule_task_id": "ST-1", "work_package_id": "WP-1"}
        ],
        "actual_records": [
            {"actual_record_id": "AR-1", "work_package_id": "WP-1", "zone_id": "Z"}
        ],
        "plan_fact_comparisons": [
            {
                "comparison_id": "PFC-1",
                "schedule_task_id": "ST-1",
                "actual_record_id": "AR-1",
                "work_package_id": "WP-1",
            }
        ],
        "matching_rules": [],
    }


def errors(workspace: dict) -> list[str]:
    return validate_matching_workspace.validate_workspace(workspace)


def test_project_scenario_validates() -> None:
    assert validate_matching_workspace.validate_project(PROJECT_ROOT) == []


def test_valid_fixture_passes() -> None:
    assert errors(valid_workspace()) == []


def test_model_element_direct_candidate_norm_reference_fails() -> None:
    workspace = valid_workspace()
    workspace["model_group"]["model_elements"][0]["gesn_norm_id"] = "N"

    assert any("model element" in error for error in errors(workspace))


def test_ksi_result_direct_candidate_norm_reference_fails() -> None:
    workspace = valid_workspace()
    workspace["ksi_result_code"]["gesn_norm_id"] = "N"

    assert any("ksi result code" in error for error in errors(workspace))


def test_candidate_norm_direct_schedule_task_reference_fails() -> None:
    workspace = valid_workspace()
    workspace["calculation_unit_candidate"]["gesn_norm"] = {"schedule_task_id": "ST-1"}

    assert any("schedule_task_id" in error for error in errors(workspace))


def test_calculation_unit_fact_reference_fails() -> None:
    workspace = valid_workspace()
    workspace["calculation_unit_candidate"]["actual_record_id"] = "AR-1"

    assert any("actual_record_id" in error for error in errors(workspace))


def test_active_status_and_activation_are_rejected() -> None:
    workspace = valid_workspace()
    workspace["status"] = "active"
    workspace["activation_allowed"] = True
    workspace["normative_status"] = "active"

    current_errors = errors(workspace)

    assert any("status active" in error for error in current_errors)
    assert any("normative_status" in error for error in current_errors)
    assert any("activation_allowed" in error for error in current_errors)


def test_llm_generated_evidence_fails() -> None:
    workspace = valid_workspace()
    workspace["evidence_slots"][0]["source_origin"] = "llm_generated"

    assert any("llm_generated" in error for error in errors(workspace))


def test_forbidden_authority_fails() -> None:
    workspace = valid_workspace()
    workspace["evidence_slots"][0]["source_authority"] = "forbidden"

    assert any("source_authority=forbidden" in error for error in errors(workspace))


def test_user_decision_cannot_confirm_official_field() -> None:
    workspace = valid_workspace()
    workspace["evidence_slots"][0]["source_origin"] = "user_decision"

    assert any("user_decision cannot confirm" in error for error in errors(workspace))


def test_code_like_value_requires_accepted_official_source() -> None:
    workspace = valid_workspace()
    workspace["evidence_slots"][0]["value"] = "GESN 01"

    assert any("requires accepted official source" in error for error in errors(workspace))


def test_code_like_value_with_accepted_official_source_passes_gate() -> None:
    workspace = valid_workspace()
    workspace["evidence_slots"][0].update(
        {
            "value": "GESN 01",
            "source_origin": "official_public_source",
            "source_authority": "official",
            "review_status": "accepted_by_user",
        }
    )

    assert errors(workspace) == []


def test_actual_record_only_model_element_context_fails() -> None:
    workspace = valid_workspace()
    workspace["actual_records"] = [
        {"actual_record_id": "AR-1", "model_element_id": "ME-1"}
    ]

    current_errors = errors(workspace)

    assert any("ActualRecord must target a WorkPackage" in error for error in current_errors)
    assert any("model_element_id" in error for error in current_errors)


def test_schedule_task_requires_work_package_context() -> None:
    workspace = valid_workspace()
    workspace["schedule_tasks"] = [{"schedule_task_id": "ST-1"}]

    assert any("ScheduleTask must be linked through WorkPackage" in error for error in errors(workspace))


def test_active_matching_rule_fails() -> None:
    workspace = valid_workspace()
    workspace["matching_rules"] = [{"rule_id": "RULE-1", "status": "active"}]

    assert any("active matching rules are forbidden" in error for error in errors(workspace))


def test_accepted_by_codex_fails() -> None:
    workspace = valid_workspace()
    workspace["review"] = {"accepted_by": "Codex"}

    assert any("accepted_by must not be Codex" in error for error in errors(workspace))
