from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT_ROOT / "scripts" / "validate_monthly_planning.py"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
SPEC = importlib.util.spec_from_file_location("validate_monthly_planning", SCRIPT)
assert SPEC is not None
assert SPEC.loader is not None
validate_monthly_planning = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = validate_monthly_planning
SPEC.loader.exec_module(validate_monthly_planning)


def write_valid_fixture(root: Path) -> None:
    monthly_dir = root / "docs" / "monthly" / "2026-06"
    roadmap_dir = root / "docs" / "roadmap"
    monthly_dir.mkdir(parents=True)
    roadmap_dir.mkdir(parents=True)
    (root / "docs" / "monthly" / "README.md").write_text(
        "# Месячное планирование\n\n"
        "Месяц содержит три задачи по 15 часов и завершается БФТ, ТЗ и протоколом испытаний.\n",
        encoding="utf-8",
    )
    (roadmap_dir / "2026-customer-facing-mvp-roadmap.md").write_text(
        "# Календарный план разработки и проверки прикладного прототипа ТАРТИП на 2026 год\n\n"
        "ТАРТИП — прикладной программный прототип для автоматизации перехода от данных ЦИМ/BIM "
        "к сметно-календарной подготовке и план-фактному контролю.\n\n"
        "## Июнь 2026 — Инфраструктурный контур разработки и приемки\n",
        encoding="utf-8",
    )
    (monthly_dir / "monthly-plan.yml").write_text(
        "month: 2026-06\n"
        "block_title: \"Инфраструктурный контур разработки и приемки\"\n"
        "customer_facing_title: \"Документы для рассмотрения решения о разработке прикладного прототипа\"\n"
        "status: ready_for_documentation\n"
        "planned_total_hours: 45\n"
        "tasks:\n"
        "  -\n"
        "    task_id: M2026-06-T1\n"
        "    title: \"Инфраструктура репозитория\"\n"
        "    planned_hours: 15\n"
        "    expected_document_section: \"БФТ\"\n"
        "  -\n"
        "    task_id: M2026-06-T2\n"
        "    title: \"Контур управления артефактами\"\n"
        "    planned_hours: 15\n"
        "    expected_document_section: \"ТЗ\"\n"
        "  -\n"
        "    task_id: M2026-06-T3\n"
        "    title: \"Контур верификации\"\n"
        "    planned_hours: 15\n"
        "    expected_document_section: \"Протокол испытаний\"\n"
        "deliverables:\n"
        "  -\n"
        "    path: docs/monthly/2026-06/01-business-functional-requirements.md\n"
        "    title: \"Бизнес-функциональные требования\"\n"
        "    status: planned\n"
        "  -\n"
        "    path: docs/monthly/2026-06/02-technical-specification.md\n"
        "    title: \"Техническое задание\"\n"
        "    status: planned\n"
        "  -\n"
        "    path: docs/monthly/2026-06/03-test-protocol-infrastructure-contour.md\n"
        "    title: \"Протокол испытаний\"\n"
        "    status: planned\n",
        encoding="utf-8",
    )


def errors(root: Path) -> list[str]:
    return validate_monthly_planning.validate_project(root)


def test_valid_monthly_plan_passes(tmp_path: Path) -> None:
    write_valid_fixture(tmp_path)

    assert errors(tmp_path) == []


def test_two_tasks_fail(tmp_path: Path) -> None:
    write_valid_fixture(tmp_path)
    plan = tmp_path / "docs" / "monthly" / "2026-06" / "monthly-plan.yml"
    plan.write_text(
        plan.read_text(encoding="utf-8").replace(
            "  -\n"
            "    task_id: M2026-06-T3\n"
            "    title: \"Контур верификации\"\n"
            "    planned_hours: 15\n"
            "    expected_document_section: \"Протокол испытаний\"\n",
            "",
        ),
        encoding="utf-8",
    )

    assert any("tasks must contain exactly 3 items" in error for error in errors(tmp_path))


def test_task_with_wrong_planned_hours_fails(tmp_path: Path) -> None:
    write_valid_fixture(tmp_path)
    plan = tmp_path / "docs" / "monthly" / "2026-06" / "monthly-plan.yml"
    plan.write_text(
        plan.read_text(encoding="utf-8").replace("planned_hours: 15", "planned_hours: 14", 1),
        encoding="utf-8",
    )

    assert any("planned_hours must be 15" in error for error in errors(tmp_path))


def test_missing_bft_deliverable_fails(tmp_path: Path) -> None:
    write_valid_fixture(tmp_path)
    plan = tmp_path / "docs" / "monthly" / "2026-06" / "monthly-plan.yml"
    plan.write_text(
        plan.read_text(encoding="utf-8")
        .replace("01-business-functional-requirements.md", "01-functional-outline.md")
        .replace("Бизнес-функциональные требования", "Функциональное описание"),
        encoding="utf-8",
    )

    assert any("deliverables must include БФТ" in error for error in errors(tmp_path))


def test_prompt_deliverable_fails(tmp_path: Path) -> None:
    write_valid_fixture(tmp_path)
    plan = tmp_path / "docs" / "monthly" / "2026-06" / "monthly-plan.yml"
    plan.write_text(
        plan.read_text(encoding="utf-8").replace(
            "01-business-functional-requirements.md",
            "prompt-templates/01-business-functional-requirements.prompt.md",
        ),
        encoding="utf-8",
    )

    assert any("must not be a prompt template" in error for error in errors(tmp_path))


def test_forbidden_saas_heading_in_customer_roadmap_fails(tmp_path: Path) -> None:
    write_valid_fixture(tmp_path)
    roadmap = tmp_path / "docs" / "roadmap" / "2026-customer-facing-mvp-roadmap.md"
    roadmap.write_text(roadmap.read_text(encoding="utf-8") + "\n## SaaS roadmap\n", encoding="utf-8")

    assert any("forbidden customer-facing term: SaaS" in error for error in errors(tmp_path))


def test_forbidden_open_core_heading_in_customer_roadmap_fails(tmp_path: Path) -> None:
    write_valid_fixture(tmp_path)
    roadmap = tmp_path / "docs" / "roadmap" / "2026-customer-facing-mvp-roadmap.md"
    roadmap.write_text(roadmap.read_text(encoding="utf-8") + "\n## open-core model\n", encoding="utf-8")

    assert any("forbidden customer-facing term: open-core" in error for error in errors(tmp_path))


def test_planning_override_text_in_customer_roadmap_fails(tmp_path: Path) -> None:
    write_valid_fixture(tmp_path)
    roadmap = tmp_path / "docs" / "roadmap" / "2026-customer-facing-mvp-roadmap.md"
    roadmap.write_text(
        roadmap.read_text(encoding="utf-8")
        + "\nPlanning override: EP-016-REFERENCE-INTAKE-PREPARATION temporarily deferred.\n",
        encoding="utf-8",
    )

    assert any("planning override marker" in error for error in errors(tmp_path))
