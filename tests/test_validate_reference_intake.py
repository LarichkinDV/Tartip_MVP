from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT_ROOT / "scripts" / "validate_reference_intake.py"
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
SPEC = importlib.util.spec_from_file_location("validate_reference_intake", SCRIPT)
assert SPEC is not None
assert SPEC.loader is not None
validate_reference_intake = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = validate_reference_intake
SPEC.loader.exec_module(validate_reference_intake)


def write_yaml(path: Path, data: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(data, encoding="utf-8")


def write_valid_fixture(root: Path) -> None:
    reference_dir = root / "docs" / "reference-intake"
    reference_dir.mkdir(parents=True)
    for name in [
        "README.md",
        "source-intake-policy.md",
        "source-authority-model.md",
        "intake-workflow.md",
    ]:
        (reference_dir / name).write_text(
            "# Reference intake\n\n"
            + validate_reference_intake.MANDATORY_INTAKE_TEXT
            + "\n",
            encoding="utf-8",
        )

    write_yaml(
        root / "data" / "reference" / "manifests" / "intake-manifest.schema.yml",
        """
schema_version: 1
fields:
  source_id: {}
  source_name: {}
  source_type: {}
  source_origin: {}
  source_authority: {}
  source_status: {}
  version_label: {}
  effective_date: {}
  received_at: {}
  file_path: {}
  checksum_sha256: {}
  checksum_status: {}
  review_status: {}
  review_required: {}
  accepted_by: {}
  accepted_at: {}
  notes: {}
enums:
  source_origin:
    - official_public_source
    - official_user_provided_file
    - project_dictionary
    - user_decision
    - llm_generated
    - forbidden
  source_authority:
    - official
    - project_authorized
    - user_asserted
    - draft
    - forbidden
  source_status:
    - inbox
    - draft
    - under_review
    - accepted
    - rejected
    - forbidden
    - requires_norm_review
  checksum_status:
    - missing
    - calculated
    - verified
    - mismatch
  review_status:
    - not_reviewed
    - pending_user_review
    - accepted_by_user
    - rejected_by_user
    - requires_norm_review
""".lstrip(),
    )
    write_yaml(
        root / "data" / "reference" / "manifests" / "source-authority-catalog.yml",
        """
official_public_source:
  can_confirm_official_normative_data: true
official_user_provided_file:
  can_confirm_official_normative_data: true
project_dictionary:
  can_confirm_official_normative_data: false
user_decision:
  can_confirm_official_normative_data: false
llm_generated:
  can_confirm_official_normative_data: false
forbidden:
  can_confirm_official_normative_data: false
""".lstrip(),
    )
    write_yaml(
        root / "data" / "reference" / "manifests" / "intake-log.yml",
        """
schema_version: 1
sources: []
data_requirements:
  -
    requirement_id: DR-REF-001
    title: "Предоставить источник"
    status: pending_user_input
""".lstrip(),
    )
    for folder in [
        root / "data" / "reference" / "inbox",
        root / "data" / "reference" / "raw",
    ]:
        folder.mkdir(parents=True)
        (folder / ".gitkeep").write_text("", encoding="utf-8")


def write_sources(root: Path, sources_yaml: str) -> None:
    write_yaml(
        root / "data" / "reference" / "manifests" / "intake-log.yml",
        "schema_version: 1\nsources:\n" + sources_yaml,
    )


def errors(root: Path, allow_non_gitkeep_files: bool = False) -> list[str]:
    return validate_reference_intake.validate_project(root, allow_non_gitkeep_files)


def test_valid_empty_intake_log_passes(tmp_path: Path) -> None:
    write_valid_fixture(tmp_path)

    assert errors(tmp_path) == []


def test_duplicate_source_id_fails(tmp_path: Path) -> None:
    write_valid_fixture(tmp_path)
    write_sources(
        tmp_path,
        """
  -
    source_id: SRC-1
    source_origin: official_public_source
    source_authority: official
    source_status: draft
    checksum_status: missing
    review_status: not_reviewed
    review_required: true
  -
    source_id: SRC-1
    source_origin: official_public_source
    source_authority: official
    source_status: draft
    checksum_status: missing
    review_status: not_reviewed
    review_required: true
""",
    )

    assert any("duplicate source_id: SRC-1" in error for error in errors(tmp_path))


def test_accepted_source_without_checksum_fails(tmp_path: Path) -> None:
    write_valid_fixture(tmp_path)
    write_sources(
        tmp_path,
        """
  -
    source_id: SRC-ACCEPTED
    source_origin: official_public_source
    source_authority: official
    source_status: accepted
    checksum_status: missing
    review_status: accepted_by_user
    review_required: false
    accepted_by: "Дмитрий"
    accepted_at: 2026-06-13
""",
    )

    assert any("requires checksum_sha256" in error for error in errors(tmp_path))


def test_accepted_source_without_user_fields_fails(tmp_path: Path) -> None:
    write_valid_fixture(tmp_path)
    write_sources(
        tmp_path,
        """
  -
    source_id: SRC-ACCEPTED
    source_origin: official_public_source
    source_authority: official
    source_status: accepted
    checksum_sha256: abc
    checksum_status: calculated
    review_status: accepted_by_user
    review_required: false
""",
    )

    assert any("requires accepted_by and accepted_at" in error for error in errors(tmp_path))


def test_accepted_by_codex_fails(tmp_path: Path) -> None:
    write_valid_fixture(tmp_path)
    write_sources(
        tmp_path,
        """
  -
    source_id: SRC-CODEX
    source_origin: official_public_source
    source_authority: official
    source_status: accepted
    checksum_sha256: abc
    checksum_status: calculated
    review_status: accepted_by_user
    review_required: false
    accepted_by: Codex
    accepted_at: 2026-06-13
""",
    )

    assert any("accepted_by must not be Codex" in error for error in errors(tmp_path))


def test_llm_generated_with_official_authority_fails(tmp_path: Path) -> None:
    write_valid_fixture(tmp_path)
    write_sources(
        tmp_path,
        """
  -
    source_id: SRC-LLM
    source_origin: llm_generated
    source_authority: official
    source_status: draft
    checksum_status: missing
    review_status: not_reviewed
    review_required: true
""",
    )

    assert any("llm_generated cannot be official" in error for error in errors(tmp_path))


def test_forbidden_accepted_source_fails(tmp_path: Path) -> None:
    write_valid_fixture(tmp_path)
    write_sources(
        tmp_path,
        """
  -
    source_id: SRC-FORBIDDEN
    source_origin: forbidden
    source_authority: forbidden
    source_status: accepted
    checksum_sha256: abc
    checksum_status: calculated
    review_status: accepted_by_user
    review_required: false
    accepted_by: "Дмитрий"
    accepted_at: 2026-06-13
""",
    )

    assert any("forbidden source cannot be accepted" in error for error in errors(tmp_path))


def test_user_decision_confirming_official_data_fails(tmp_path: Path) -> None:
    write_valid_fixture(tmp_path)
    write_sources(
        tmp_path,
        """
  -
    source_id: SRC-USER
    source_origin: user_decision
    source_authority: user_asserted
    source_status: draft
    checksum_status: missing
    review_status: not_reviewed
    review_required: true
    confirms_official_gesn: true
""",
    )

    assert any("user_decision cannot confirm official" in error for error in errors(tmp_path))


def test_non_gitkeep_file_in_inbox_fails_unless_allowed(tmp_path: Path) -> None:
    write_valid_fixture(tmp_path)
    (tmp_path / "data" / "reference" / "inbox" / "candidate.txt").write_text(
        "synthetic placeholder",
        encoding="utf-8",
    )

    assert any("may contain only .gitkeep" in error for error in errors(tmp_path))
    assert errors(tmp_path, allow_non_gitkeep_files=True) == []


def test_customer_specific_field_in_manifest_fails(tmp_path: Path) -> None:
    write_valid_fixture(tmp_path)
    write_sources(
        tmp_path,
        """
  -
    source_id: SRC-CUSTOMER
    source_origin: project_dictionary
    source_authority: draft
    source_status: draft
    checksum_status: missing
    review_status: not_reviewed
    review_required: true
    notes: "Пример ИНН 1234567890"
""",
    )

    assert any("customer-specific data pattern" in error for error in errors(tmp_path))
