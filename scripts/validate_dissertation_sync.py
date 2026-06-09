#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from reference_utils import load_data
from validate_dissertation_prompts import validate_prompts


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DISSERTATION_DIR = PROJECT_ROOT / "docs" / "dissertation"
THESIS_DIR = PROJECT_ROOT / "thesis"
AGENTS_PATH = PROJECT_ROOT / "AGENTS.md"
GITIGNORE_PATH = PROJECT_ROOT / ".gitignore"
ACCEPTANCE_REPORT_PATH = (
    PROJECT_ROOT
    / "docs"
    / "acceptance"
    / "EP-008-DISSERTATION-PROMPT-GENERATION.acceptance.md"
)

REQUIRED_DIRS = [
    DISSERTATION_DIR,
    DISSERTATION_DIR / "prompt-profiles",
    DISSERTATION_DIR / "prompt-templates",
    DISSERTATION_DIR / "prompt-queue",
    DISSERTATION_DIR / "prompt-queue" / "pending",
    DISSERTATION_DIR / "prompt-queue" / "accepted",
    DISSERTATION_DIR / "prompt-queue" / "rejected",
    DISSERTATION_DIR / "patches",
    DISSERTATION_DIR / "patches" / "pending",
    DISSERTATION_DIR / "patches" / "accepted",
    DISSERTATION_DIR / "patches" / "rejected",
    DISSERTATION_DIR / "acceptance",
    DISSERTATION_DIR / "notes",
    THESIS_DIR,
    THESIS_DIR / "source",
    THESIS_DIR / "versions",
    THESIS_DIR / "exports",
    THESIS_DIR / "exports" / "pdf",
    THESIS_DIR / "exports" / "rendered-review",
]

REQUIRED_FILES = [
    DISSERTATION_DIR / "README.md",
    DISSERTATION_DIR / "dissertation-sync-plan.md",
    DISSERTATION_DIR / "dissertation-impact-log.yml",
    DISSERTATION_DIR / "dissertation-artifact-map.yml",
    DISSERTATION_DIR / "section-update-queue.yml",
    DISSERTATION_DIR / "dissertation-change-log.md",
    DISSERTATION_DIR / "bibliography-registry.yml",
    DISSERTATION_DIR / "citation-requests.yml",
    DISSERTATION_DIR / "terminology-control.yml",
    DISSERTATION_DIR / "prompt-profiles" / "dissertation-editor-profile.md",
    DISSERTATION_DIR / "prompt-profiles" / "dissertation-editor-profile.yml",
    DISSERTATION_DIR / "prompt-profiles" / "tartip-dissertation-alignment.md",
    DISSERTATION_DIR / "prompt-profiles" / "forbidden-claims.yml",
    DISSERTATION_DIR / "prompt-templates" / "dissertation-impact-analysis.prompt.md",
    DISSERTATION_DIR / "prompt-templates" / "dissertation-section-update.prompt.md",
    DISSERTATION_DIR / "prompt-templates" / "dissertation-terminology-check.prompt.md",
    DISSERTATION_DIR / "prompt-templates" / "dissertation-bibliography-check.prompt.md",
    DISSERTATION_DIR / "prompt-templates" / "dissertation-docx-update.prompt.md",
]

REQUIRED_SECTION_IDS = {
    "DISS-INTRO",
    "DISS-CH1-PROBLEM",
    "DISS-CH2-METHODOLOGY",
    "DISS-CH2-CALCULATION-UNIT",
    "DISS-CH2-ALGORITHM",
    "DISS-CH3-EXPERIMENT",
    "DISS-CH3-REFERENCE-VERSIONING",
    "DISS-CH3-LIMITATIONS",
    "DISS-CONCLUSION",
    "DISS-APPENDICES",
}

REQUIRED_FORBIDDEN_IDS = {
    "FC-001",
    "FC-002",
    "FC-003",
    "FC-004",
    "FC-005",
    "FC-006",
    "FC-007",
}

GITIGNORE_PATTERNS = {
    "thesis/source/*.docx",
    "thesis/versions/*.docx",
    "thesis/exports/pdf/*.pdf",
    "thesis/exports/rendered-review/*",
    "!thesis/exports/rendered-review/.gitkeep",
}


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(PROJECT_ROOT))
    except ValueError:
        return str(path)


def as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def load_required_mapping(path: Path) -> tuple[dict[str, Any] | None, list[str]]:
    if not path.exists():
        return None, [f"Missing required file: {rel(path)}"]
    data = load_data(path)
    if not isinstance(data, dict):
        return None, [f"{rel(path)} must contain a mapping"]
    return data, []


def validate_required_paths() -> list[str]:
    errors: list[str] = []
    for path in REQUIRED_DIRS:
        if not path.is_dir():
            errors.append(f"Missing required directory: {rel(path)}")
    for path in REQUIRED_FILES:
        if not path.exists():
            errors.append(f"Missing required file: {rel(path)}")
    return errors


def validate_impact_log() -> list[str]:
    path = DISSERTATION_DIR / "dissertation-impact-log.yml"
    data, errors = load_required_mapping(path)
    if data is None:
        return errors
    impacts = data.get("impacts")
    allowed = {str(item) for item in as_list(data.get("allowed_impact_types"))}
    if not isinstance(impacts, list):
        errors.append(f"{rel(path)} impacts must be a list")
        return errors
    for impact in impacts:
        if not isinstance(impact, dict):
            errors.append(f"{rel(path)} impacts entries must be mappings")
            continue
        impact_type = str(impact.get("impact_type") or "")
        if impact_type and allowed and impact_type not in allowed:
            errors.append(f"{rel(path)} unsupported impact_type={impact_type}")
    return errors


def validate_section_queue() -> list[str]:
    path = DISSERTATION_DIR / "section-update-queue.yml"
    data, errors = load_required_mapping(path)
    if data is None:
        return errors
    updates = data.get("section_updates")
    allowed = {str(item) for item in as_list(data.get("allowed_statuses"))}
    if not isinstance(updates, list):
        errors.append(f"{rel(path)} section_updates must be a list")
        return errors
    for update in updates:
        if not isinstance(update, dict):
            errors.append(f"{rel(path)} section_updates entries must be mappings")
            continue
        status = str(update.get("status") or "")
        accepted_by = str(update.get("accepted_by") or "")
        if status and allowed and status not in allowed:
            errors.append(f"{rel(path)} unsupported status={status}")
        if status == "accepted" and not accepted_by:
            errors.append(f"{rel(path)} accepted update requires accepted_by")
        if accepted_by == "Codex":
            errors.append(f"{rel(path)} accepted_by must not be Codex")
    return errors


def validate_artifact_map() -> list[str]:
    path = DISSERTATION_DIR / "dissertation-artifact-map.yml"
    data, errors = load_required_mapping(path)
    if data is None:
        return errors
    sections = data.get("sections", [])
    if not isinstance(sections, list):
        return [f"{rel(path)} sections must be a list"]
    seen = {
        str(section.get("section_id"))
        for section in sections
        if isinstance(section, dict)
    }
    missing = sorted(REQUIRED_SECTION_IDS - seen)
    for section_id in missing:
        errors.append(f"{rel(path)} missing section_id={section_id}")
    for section in sections:
        if not isinstance(section, dict):
            errors.append(f"{rel(path)} sections entries must be mappings")
            continue
        for field in [
            "section_id",
            "title",
            "docx_target",
            "related_project_modules",
            "related_artifacts",
            "update_policy",
            "notes",
        ]:
            if field not in section:
                errors.append(
                    f"{rel(path)} {section.get('section_id')}: missing {field}"
                )
    return errors


def validate_forbidden_claims() -> list[str]:
    path = DISSERTATION_DIR / "prompt-profiles" / "forbidden-claims.yml"
    data, errors = load_required_mapping(path)
    if data is None:
        return errors
    claims = data.get("forbidden_claims", [])
    if not isinstance(claims, list):
        return [f"{rel(path)} forbidden_claims must be a list"]
    seen = {str(claim.get("id")) for claim in claims if isinstance(claim, dict)}
    for claim_id in sorted(REQUIRED_FORBIDDEN_IDS - seen):
        errors.append(f"{rel(path)} missing forbidden claim {claim_id}")
    for claim in claims:
        if not isinstance(claim, dict):
            errors.append(f"{rel(path)} forbidden_claims entries must be mappings")
            continue
        if not claim.get("forbidden_claim") or not claim.get("allowed_replacement"):
            errors.append(
                f"{rel(path)} {claim.get('id')}: missing claim or replacement"
            )
    return errors


def validate_bibliography_files() -> list[str]:
    errors: list[str] = []
    for path, key in [
        (DISSERTATION_DIR / "bibliography-registry.yml", "sources"),
        (DISSERTATION_DIR / "citation-requests.yml", "citation_requests"),
    ]:
        data, file_errors = load_required_mapping(path)
        errors.extend(file_errors)
        if data is None:
            continue
        if not isinstance(data.get(key), list):
            errors.append(f"{rel(path)} {key} must be a list")
    return errors


def validate_agents_rules() -> list[str]:
    if not AGENTS_PATH.exists():
        return [f"Missing {rel(AGENTS_PATH)}"]
    text = AGENTS_PATH.read_text(encoding="utf-8")
    required = [
        "Dissertation synchronization and prompt generation discipline",
        "Codex не имеет права редактировать DOCX напрямую",
        "Accepted artifacts are protected",
    ]
    return [
        f"AGENTS.md missing dissertation rule: {fragment}"
        for fragment in required
        if fragment not in text
    ]


def validate_gitignore() -> list[str]:
    if not GITIGNORE_PATH.exists():
        return [f"Missing {rel(GITIGNORE_PATH)}"]
    lines = {
        line.strip()
        for line in GITIGNORE_PATH.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    }
    return [
        f".gitignore missing thesis pattern: {pattern}"
        for pattern in sorted(GITIGNORE_PATTERNS - lines)
    ]


def validate_no_docx_or_pdf_created() -> list[str]:
    errors: list[str] = []
    if THESIS_DIR.exists():
        for path in sorted(THESIS_DIR.glob("**/*")):
            if path.suffix.lower() in {".docx", ".pdf"}:
                errors.append(f"Unexpected dissertation binary artifact: {rel(path)}")
    return errors


def validate_acceptance_report() -> list[str]:
    if not ACCEPTANCE_REPORT_PATH.exists():
        return [f"Missing acceptance report: {rel(ACCEPTANCE_REPORT_PATH)}"]
    text = ACCEPTANCE_REPORT_PATH.read_text(encoding="utf-8")
    errors: list[str] = []
    fields: dict[str, str] = {}
    for line in text.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        if key in {"acceptance_decision", "accepted_by", "accepted_at", "comments"}:
            fields[key] = value.strip()

    decision = fields.get("acceptance_decision", "")
    accepted_by = fields.get("accepted_by", "")
    accepted_at = fields.get("accepted_at", "")
    comments = fields.get("comments", "")

    if decision not in {"pending", "accepted"}:
        errors.append("EP-008 acceptance_decision must be pending or accepted")
    if accepted_by == "Codex":
        errors.append("EP-008 accepted_by must not be Codex")
    if decision == "accepted":
        if not accepted_by:
            errors.append("EP-008 accepted acceptance report requires accepted_by")
        if not accepted_at:
            errors.append("EP-008 accepted acceptance report requires accepted_at")
        if not comments:
            errors.append("EP-008 accepted acceptance report requires comments")
    return errors


def validate_sync() -> list[str]:
    errors: list[str] = []
    errors.extend(validate_required_paths())
    errors.extend(validate_impact_log())
    errors.extend(validate_section_queue())
    errors.extend(validate_artifact_map())
    errors.extend(validate_forbidden_claims())
    errors.extend(validate_bibliography_files())
    errors.extend(validate_agents_rules())
    errors.extend(validate_gitignore())
    errors.extend(validate_no_docx_or_pdf_created())
    errors.extend(validate_acceptance_report())
    errors.extend(validate_prompts())
    return errors


def main() -> int:
    errors = validate_sync()
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Dissertation sync validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
