from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT_ROOT / "scripts" / "validate_data_contribution.py"
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
SPEC = importlib.util.spec_from_file_location("validate_data_contribution", SCRIPT)
assert SPEC is not None
assert SPEC.loader is not None
validate_data_contribution = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = validate_data_contribution
SPEC.loader.exec_module(validate_data_contribution)


def test_valid_raw_event_passes() -> None:
    record = {
        "customer_ref": "EXAMPLE_CUSTOMER",
        "supplier_ref": "EXAMPLE_SUPPLIER",
        "data_classification": "synthetic_example_only",
        "source_status": "synthetic",
        "example_only": True,
        "derived_from_real_customer_data": False,
        "telemetry_enabled": False,
        "dataset_contribution_enabled": False,
        "external_upload_enabled": False,
        "ai_training_allowed": False,
        "commercial_use_allowed": False,
    }

    assert validate_data_contribution.validate_raw_event(record) == []


def test_raw_event_with_customer_ref_cannot_be_commercial() -> None:
    record = {
        "customer_ref": "EXAMPLE_CUSTOMER",
        "source_status": "synthetic",
        "data_classification": "synthetic_example_only",
        "example_only": True,
        "derived_from_real_customer_data": False,
        "telemetry_enabled": False,
        "dataset_contribution_enabled": False,
        "external_upload_enabled": False,
        "ai_training_allowed": False,
        "commercial_use_allowed": True,
    }

    errors = validate_data_contribution.validate_raw_event(record)

    assert any("cannot be commercial_use_allowed" in error for error in errors)


def test_raw_event_with_supplier_ref_cannot_be_ai_training() -> None:
    record = {
        "supplier_ref": "EXAMPLE_SUPPLIER",
        "source_status": "synthetic",
        "data_classification": "synthetic_example_only",
        "example_only": True,
        "derived_from_real_customer_data": False,
        "telemetry_enabled": False,
        "dataset_contribution_enabled": False,
        "external_upload_enabled": False,
        "ai_training_allowed": True,
        "commercial_use_allowed": False,
    }

    errors = validate_data_contribution.validate_raw_event(record)

    assert any("cannot be ai_training_allowed" in error for error in errors)


def test_raw_event_external_upload_is_rejected() -> None:
    record = {
        "customer_ref": "EXAMPLE_CUSTOMER",
        "source_status": "synthetic",
        "data_classification": "synthetic_example_only",
        "example_only": True,
        "derived_from_real_customer_data": False,
        "telemetry_enabled": False,
        "dataset_contribution_enabled": False,
        "external_upload_enabled": True,
        "ai_training_allowed": False,
        "commercial_use_allowed": False,
    }

    errors = validate_data_contribution.validate_raw_event(record)

    assert any("external_upload_enabled must be false" in error for error in errors)


def test_anonymized_signal_rejects_direct_identifiers() -> None:
    record = {
        "signal_id": "SIGNAL-1",
        "customer_ref": "EXAMPLE_CUSTOMER",
        "email": "synthetic@example.test",
    }

    errors = validate_data_contribution.validate_anonymized_signal(record)

    assert any("forbidden direct identifier fields" in error for error in errors)


def test_commercial_aggregate_thresholds_are_enforced() -> None:
    record = {
        "observations_count": 9,
        "independent_customers_count": 4,
        "independent_suppliers_count": 4,
        "reidentification_risk": "low",
        "source_status": "synthetic",
        "derived_from_real_customer_data": False,
        "period_bucket": "2026-Q2",
        "commercial_use_allowed": True,
        "data_classification": "synthetic_aggregate_example",
        "aggregate_approved": True,
    }

    errors = validate_data_contribution.validate_commercial_aggregate(record)

    assert any("observations_count" in error for error in errors)
    assert any("independent_customers_count" in error for error in errors)
    assert any("independent_suppliers_count" in error for error in errors)


def test_commercial_aggregate_requires_low_risk() -> None:
    record = {
        "observations_count": 10,
        "independent_customers_count": 5,
        "independent_suppliers_count": 5,
        "reidentification_risk": "medium",
        "source_status": "synthetic",
        "derived_from_real_customer_data": False,
        "period_bucket": "2026-Q2",
        "commercial_use_allowed": True,
        "data_classification": "synthetic_aggregate_example",
        "aggregate_approved": True,
    }

    errors = validate_data_contribution.validate_commercial_aggregate(record)

    assert any("reidentification_risk must be low" in error for error in errors)


def test_commercial_use_requires_classification_and_approval() -> None:
    record = {
        "observations_count": 10,
        "independent_customers_count": 5,
        "independent_suppliers_count": 5,
        "reidentification_risk": "low",
        "source_status": "synthetic",
        "derived_from_real_customer_data": False,
        "period_bucket": "2026-Q2",
        "commercial_use_allowed": True,
        "data_classification": "raw",
        "aggregate_approved": False,
    }

    errors = validate_data_contribution.validate_commercial_aggregate(record)

    assert any("commercial_use_allowed requires" in error for error in errors)


def test_commercial_aggregate_rejects_real_customer_derivation() -> None:
    record = {
        "observations_count": 10,
        "independent_customers_count": 5,
        "independent_suppliers_count": 5,
        "reidentification_risk": "low",
        "source_status": "synthetic",
        "derived_from_real_customer_data": True,
        "period_bucket": "2026-Q2",
    }

    errors = validate_data_contribution.validate_commercial_aggregate(record)

    assert any("derived_from_real_customer_data must be false" in error for error in errors)


def test_commercial_aggregate_rejects_exact_fields_and_exact_period() -> None:
    record = {
        "observations_count": 10,
        "independent_customers_count": 5,
        "independent_suppliers_count": 5,
        "reidentification_risk": "low",
        "source_status": "synthetic",
        "derived_from_real_customer_data": False,
        "period_bucket": "2026-06-13",
        "city": "synthetic_city",
        "event_date": "2026-06-13",
    }

    errors = validate_data_contribution.validate_commercial_aggregate(record)

    assert any("period_bucket must be bucketed" in error for error in errors)
    assert any("exact fields are forbidden" in error for error in errors)


def test_default_flags_must_be_false() -> None:
    record = {
        "telemetry_enabled": False,
        "dataset_contribution_enabled": True,
        "external_upload_enabled": False,
        "ai_training_allowed": False,
        "commercial_use_allowed": False,
    }

    errors = validate_data_contribution.validate_default_flags(record, "defaults")

    assert any("dataset_contribution_enabled must default to false" in error for error in errors)


def test_project_files_validate() -> None:
    assert validate_data_contribution.validate_project(PROJECT_ROOT) == []
