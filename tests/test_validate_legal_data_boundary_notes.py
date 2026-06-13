from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT_ROOT / "scripts" / "validate_legal_data_boundary_notes.py"
SPEC = importlib.util.spec_from_file_location(
    "validate_legal_data_boundary_notes", SCRIPT
)
assert SPEC is not None
assert SPEC.loader is not None
validate_legal_data_boundary_notes = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = validate_legal_data_boundary_notes
SPEC.loader.exec_module(validate_legal_data_boundary_notes)


DISCLAIMER = validate_legal_data_boundary_notes.DISCLAIMER
WARNING = validate_legal_data_boundary_notes.REIDENTIFICATION_WARNING


def write_valid_fixture(root: Path) -> None:
    legal_dir = root / "docs" / "legal"
    legal_dir.mkdir(parents=True)
    (legal_dir / "README.md").write_text(
        "# Legal/Data Boundary Notes\n\n"
        "Внутренние policy notes требуют юридической проверки.\n",
        encoding="utf-8",
    )
    base = (
        DISCLAIMER
        + "\n\n# Note\n\n"
        "Это проектное допущение и предварительная policy note. Документ требует юридической проверки "
        "и не применяется без договорного основания. Документ не является согласием Заказчика.\n"
    )
    for filename in [
        "ip-and-deliverables-policy-note.md",
        "customer-data-boundary-policy-note.md",
        "data-contribution-policy-note.md",
        "anonymization-and-aggregation-policy-note.md",
        "code-license-and-data-use-boundary-note.md",
    ]:
        (legal_dir / filename).write_text(base, encoding="utf-8")

    (legal_dir / "customer-data-boundary-policy-note.md").write_text(
        base
        + "\nПередача данных за пределы локального контура отключена по умолчанию. "
        "Локальная поставка не означает автоматический сбор или передачу данных.\n",
        encoding="utf-8",
    )
    (legal_dir / "data-contribution-policy-note.md").write_text(
        base
        + "\n"
        + validate_legal_data_boundary_notes.MANDATORY_DATA_CONTRIBUTION_TEXT
        + "\n",
        encoding="utf-8",
    )
    (legal_dir / "anonymization-and-aggregation-policy-note.md").write_text(
        base
        + "\nPipeline включает re-identification risk check.\n"
        + WARNING
        + "\n",
        encoding="utf-8",
    )
    (legal_dir / "code-license-and-data-use-boundary-note.md").write_text(
        base
        + "\n```text\n"
        "telemetry_enabled=false\n"
        "dataset_contribution_enabled=false\n"
        "external_upload_enabled=false\n"
        "ai_training_allowed=false\n"
        "commercial_use_allowed=false\n"
        "```\n",
        encoding="utf-8",
    )


def errors(root: Path) -> list[str]:
    return validate_legal_data_boundary_notes.validate_project(root)


def test_valid_policy_notes_pass(tmp_path: Path) -> None:
    write_valid_fixture(tmp_path)

    assert errors(tmp_path) == []


def test_missing_disclaimer_fails(tmp_path: Path) -> None:
    write_valid_fixture(tmp_path)
    note = tmp_path / "docs" / "legal" / "ip-and-deliverables-policy-note.md"
    note.write_text(note.read_text(encoding="utf-8").replace(DISCLAIMER, "", 1), encoding="utf-8")

    assert any("missing required disclaimer" in error for error in errors(tmp_path))


def test_forbidden_user_agrees_phrase_fails(tmp_path: Path) -> None:
    write_valid_fixture(tmp_path)
    note = tmp_path / "docs" / "legal" / "data-contribution-policy-note.md"
    note.write_text(
        note.read_text(encoding="utf-8") + "\nПользователь соглашается на передачу.\n",
        encoding="utf-8",
    )

    assert any("пользователь соглашается" in error for error in errors(tmp_path))


def test_missing_default_off_flags_fails(tmp_path: Path) -> None:
    write_valid_fixture(tmp_path)
    note = tmp_path / "docs" / "legal" / "code-license-and-data-use-boundary-note.md"
    note.write_text(
        note.read_text(encoding="utf-8").replace("ai_training_allowed=false\n", ""),
        encoding="utf-8",
    )

    assert any("missing default-off flag: ai_training_allowed=false" in error for error in errors(tmp_path))


def test_missing_reidentification_warning_fails(tmp_path: Path) -> None:
    write_valid_fixture(tmp_path)
    note = tmp_path / "docs" / "legal" / "anonymization-and-aggregation-policy-note.md"
    note.write_text(note.read_text(encoding="utf-8").replace(WARNING, ""), encoding="utf-8")

    assert any("missing re-identification warning" in error for error in errors(tmp_path))


def test_obvious_inn_pattern_fails(tmp_path: Path) -> None:
    write_valid_fixture(tmp_path)
    note = tmp_path / "docs" / "legal" / "customer-data-boundary-policy-note.md"
    note.write_text(
        note.read_text(encoding="utf-8") + "\nПример запрещенного значения: ИНН 1234567890.\n",
        encoding="utf-8",
    )

    assert any("obvious INN-like value" in error for error in errors(tmp_path))

