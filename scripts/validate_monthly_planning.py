#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

from reference_utils import load_data


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MONTHLY_README = Path("docs/monthly/README.md")
ROADMAP = Path("docs/roadmap/2026-customer-facing-mvp-roadmap.md")
MONTHLY_PLAN = Path("docs/monthly/2026-06/monthly-plan.yml")
FORBIDDEN_ROADMAP_TERMS = [
    "SaaS",
    "open-core",
    "DaaS",
    "freemium",
    "bottom-up adoption",
    "commercial data layer",
    "отраслевой стандарт",
]
PLANNING_OVERRIDE_MARKERS = [
    "planning override",
    "EP-016-REFERENCE-INTAKE-PREPARATION",
    "REFERENCE-INTAKE",
    "temporarily deferred",
    "отложить EP-016",
    "EP-016 отлож",
]


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def rel(root: Path, path: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def roadmap_without_code_blocks(text: str) -> str:
    return re.sub(r"```.*?```", "", text, flags=re.DOTALL)


def has_deliverable(deliverables: list[Any], patterns: list[str]) -> bool:
    for deliverable in deliverables:
        if not isinstance(deliverable, dict):
            continue
        text = " ".join(
            str(deliverable.get(key) or "")
            for key in ["path", "title", "status"]
        ).lower()
        if any(pattern.lower() in text for pattern in patterns):
            return True
    return False


def validate_project(root: Path) -> list[str]:
    errors: list[str] = []
    monthly_readme_path = root / MONTHLY_README
    roadmap_path = root / ROADMAP
    monthly_plan_path = root / MONTHLY_PLAN

    for path in [monthly_readme_path, roadmap_path, monthly_plan_path]:
        if not path.exists():
            errors.append(f"missing required file: {rel(root, path)}")

    if monthly_plan_path.exists():
        data = load_data(monthly_plan_path)
        if not isinstance(data, dict):
            errors.append(f"{MONTHLY_PLAN}: monthly plan must be a mapping")
        else:
            tasks = as_list(data.get("tasks"))
            deliverables = as_list(data.get("deliverables"))
            if data.get("planned_total_hours") != 45:
                errors.append(f"{MONTHLY_PLAN}: planned_total_hours must be 45")
            if len(tasks) != 3:
                errors.append(f"{MONTHLY_PLAN}: tasks must contain exactly 3 items")
            for task in tasks:
                if not isinstance(task, dict):
                    errors.append(f"{MONTHLY_PLAN}: task entry must be a mapping")
                    continue
                task_id = str(task.get("task_id") or "<missing task_id>")
                if task.get("planned_hours") != 15:
                    errors.append(f"{MONTHLY_PLAN}: {task_id} planned_hours must be 15")
            if len(deliverables) != 3:
                errors.append(f"{MONTHLY_PLAN}: deliverables must contain exactly 3 items")
            if not has_deliverable(deliverables, ["БФТ", "business-functional"]):
                errors.append(f"{MONTHLY_PLAN}: deliverables must include БФТ")
            if not has_deliverable(deliverables, ["ТЗ", "technical-specification"]):
                errors.append(f"{MONTHLY_PLAN}: deliverables must include ТЗ")
            if not has_deliverable(deliverables, ["протокол испытаний", "test-protocol"]):
                errors.append(
                    f"{MONTHLY_PLAN}: deliverables must include протокол испытаний"
                )
            for deliverable in deliverables:
                if not isinstance(deliverable, dict):
                    errors.append(f"{MONTHLY_PLAN}: deliverable entry must be a mapping")
                    continue
                path_value = str(deliverable.get("path") or "")
                if re.search(r"(prompt|template)", path_value, flags=re.IGNORECASE):
                    errors.append(
                        f"{MONTHLY_PLAN}: deliverable path must not be a prompt template: {path_value}"
                    )

    if roadmap_path.exists():
        roadmap_text = roadmap_without_code_blocks(
            roadmap_path.read_text(encoding="utf-8")
        )
        for term in FORBIDDEN_ROADMAP_TERMS:
            if re.search(re.escape(term), roadmap_text, flags=re.IGNORECASE):
                errors.append(f"{ROADMAP}: forbidden customer-facing term: {term}")
        for marker in PLANNING_OVERRIDE_MARKERS:
            if re.search(re.escape(marker), roadmap_text, flags=re.IGNORECASE):
                errors.append(f"{ROADMAP}: planning override marker must not be present")
                break

    return errors


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate monthly planning and customer-facing roadmap artifacts."
    )
    parser.add_argument(
        "--project-root",
        default=str(PROJECT_ROOT),
        help=argparse.SUPPRESS,
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])
    root = Path(args.project_root).resolve()
    errors = validate_project(root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Monthly planning validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
