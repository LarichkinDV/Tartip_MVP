#!/usr/bin/env python3
from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any

from reference_utils import load_data, write_yaml
from validate_reference_sources import (
    REQUIRED_EVIDENCE_FIELDS,
    SOURCE_MANIFEST,
    evidence_missing,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
QUESTIONS_DIR = PROJECT_ROOT / "data" / "questions"
RULES_DIR = PROJECT_ROOT / "rules" / "matching"
QUESTION_FIELDS = [
    "id",
    "type",
    "status",
    "priority",
    "module",
    "topic",
    "question",
    "needed_for",
    "expected_input",
    "target_path",
    "blocks",
    "created_at",
    "resolved_at",
    "resolution",
]


def empty_registry(name: str, description: str) -> dict[str, Any]:
    return {
        "registry": name,
        "description": description,
        "question_fields": QUESTION_FIELDS,
        "questions": [],
    }


def load_registry(path: Path, name: str, description: str) -> dict[str, Any]:
    if path.exists():
        data = load_data(path)
        if isinstance(data, dict):
            data.setdefault("registry", name)
            data.setdefault("description", description)
            data.setdefault("question_fields", QUESTION_FIELDS)
            data.setdefault("questions", [])
            return data
    return empty_registry(name, description)


def add_question(registry: dict[str, Any], question: dict[str, Any]) -> bool:
    questions = registry.setdefault("questions", [])
    existing_ids = {item.get("id") for item in questions if isinstance(item, dict)}
    if question["id"] in existing_ids:
        return False
    questions.append(question)
    return True


def accepted_source_types() -> set[str]:
    if not SOURCE_MANIFEST.exists():
        return set()
    manifest = load_data(SOURCE_MANIFEST)
    sources = manifest.get("sources", []) if isinstance(manifest, dict) else []
    accepted_statuses = {
        "accepted",
        "raw_accepted",
        "normalized",
        "active",
        "trusted",
        "imported",
    }
    result: set[str] = set()
    for source in sources:
        if not isinstance(source, dict):
            continue
        status = str(source.get("status") or source.get("import_status") or "").lower()
        if status in accepted_statuses:
            source_type = source.get("source_type")
            if source_type:
                result.add(str(source_type))
    return result


def data_requirement(
    question_id: str, source_type: str, target_path: str
) -> dict[str, Any]:
    today = date.today().isoformat()
    return {
        "id": question_id,
        "type": "data_requirement",
        "status": "open",
        "priority": "high",
        "module": "M-REFERENCE-GOVERNANCE",
        "topic": f"Missing {source_type} reference source",
        "question": f"Provide a local official or project-authorized {source_type} source file and source metadata.",
        "needed_for": "Reference evidence validation and matching rule activation gates.",
        "expected_input": "Place the source file in the target inbox path and provide source authority, version, acquisition date, and usage note.",
        "target_path": target_path,
        "blocks": "active matching rules that require this reference source type",
        "created_at": today,
        "resolved_at": None,
        "resolution": None,
    }


def normative_review_question(
    rule_path: Path, missing_fields: list[str]
) -> dict[str, Any]:
    today = date.today().isoformat()
    rule_id = rule_path.stem.upper().replace("_", "-")
    return {
        "id": f"NR-RULE-{rule_id}-001",
        "type": "normative_review_question",
        "status": "open",
        "priority": "high",
        "module": "M-MATCHING",
        "topic": "Missing normative or classifier evidence",
        "question": "Provide official evidence references for missing matching rule evidence fields.",
        "needed_for": str(rule_path.relative_to(PROJECT_ROOT)),
        "expected_input": f"source_id and normalized_record_id for: {', '.join(missing_fields)}",
        "target_path": str(rule_path.relative_to(PROJECT_ROOT)),
        "blocks": "rule activation",
        "created_at": today,
        "resolved_at": None,
        "resolution": None,
    }


def main() -> int:
    QUESTIONS_DIR.mkdir(parents=True, exist_ok=True)
    data_requirements_path = QUESTIONS_DIR / "data-requirements.yml"
    normative_questions_path = QUESTIONS_DIR / "normative-review-questions.yml"

    data_requirements = load_registry(
        data_requirements_path,
        "data-requirements",
        "Missing source files, official sources, or exports required for reference governance.",
    )
    normative_questions = load_registry(
        normative_questions_path,
        "normative-review-questions",
        "Questions requiring review of normative applicability, technical parts, or official norm evidence.",
    )

    present_types = accepted_source_types()
    source_requirements = [
        ("DR-REF-KSI-001", "ksi", "data/reference/inbox/ksi/"),
        ("DR-REF-FSNB-001", "fsnb", "data/reference/inbox/fsnb/"),
        ("DR-REF-WORK-TYPES-001", "work_types", "data/reference/inbox/work_types/"),
    ]
    added = 0
    for question_id, source_type, target_path in source_requirements:
        if source_type not in present_types:
            added += int(
                add_question(
                    data_requirements,
                    data_requirement(question_id, source_type, target_path),
                )
            )

    for rule_path in sorted(
        list(RULES_DIR.glob("*.yaml")) + list(RULES_DIR.glob("*.yml"))
    ):
        rule = load_data(rule_path)
        evidence = rule.get("evidence", {}) if isinstance(rule, dict) else {}
        missing_fields = [
            field
            for field in sorted(REQUIRED_EVIDENCE_FIELDS)
            if evidence_missing(evidence.get(field))
        ]
        if missing_fields:
            added += int(
                add_question(
                    normative_questions,
                    normative_review_question(rule_path, missing_fields),
                )
            )

    write_yaml(data_requirements_path, data_requirements)
    write_yaml(normative_questions_path, normative_questions)
    print(f"Data question generation completed. Added {added} question(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
