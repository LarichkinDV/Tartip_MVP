#!/usr/bin/env python3
from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any

from reference_utils import load_data


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DISSERTATION_DIR = PROJECT_ROOT / "docs" / "dissertation"
IMPACT_LOG_PATH = DISSERTATION_DIR / "dissertation-impact-log.yml"
SECTION_QUEUE_PATH = DISSERTATION_DIR / "section-update-queue.yml"
ARTIFACT_MAP_PATH = DISSERTATION_DIR / "dissertation-artifact-map.yml"
PROMPT_DIR = DISSERTATION_DIR / "prompt-queue" / "pending"


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


def load_mapping(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise ValueError(f"Missing required source: {rel(path)}")
    data = load_data(path)
    if not isinstance(data, dict):
        raise ValueError(f"{rel(path)} must contain a mapping")
    return data


def sections_by_id(data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    sections = data.get("sections", [])
    if not isinstance(sections, list):
        raise ValueError("dissertation-artifact-map.yml sections must be a list")
    result: dict[str, dict[str, Any]] = {}
    for section in sections:
        if isinstance(section, dict) and section.get("section_id"):
            result[str(section["section_id"])] = section
    return result


def impacts_by_packet(data: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    impacts = data.get("impacts", [])
    if not isinstance(impacts, list):
        raise ValueError("dissertation-impact-log.yml impacts must be a list")
    result: dict[str, list[dict[str, Any]]] = {}
    for impact in impacts:
        if isinstance(impact, dict):
            packet_id = str(impact.get("source_packet") or "")
            if packet_id:
                result.setdefault(packet_id, []).append(impact)
    return result


def prompt_id_for(update: dict[str, Any]) -> str:
    existing = str(update.get("prompt_id") or "").strip()
    if existing:
        return existing
    update_id = str(update.get("update_id") or "UNSPECIFIED").strip()
    return f"DP-{update_id}"


def prompt_path(prompt_id: str) -> Path:
    safe = "".join(
        char if char.isalnum() or char in "-_" else "-" for char in prompt_id
    )
    return PROMPT_DIR / f"{safe}.prompt.md"


def front_matter(update: dict[str, Any], prompt_id: str) -> dict[str, str]:
    return {
        "prompt_id": prompt_id,
        "prompt_type": "section_update",
        "status": "pending",
        "section_id": str(update.get("section_id") or ""),
        "source_packet": str(update.get("source_packet") or ""),
        "update_id": str(update.get("update_id") or ""),
        "patch_id": str(update.get("patch_id") or ""),
        "accepted_patch": "",
        "accepted_by": "",
        "created_at": date.today().isoformat(),
    }


def format_front_matter(values: dict[str, str]) -> str:
    lines = ["---"]
    for key, value in values.items():
        escaped = value.replace('"', '\\"')
        lines.append(f'{key}: "{escaped}"')
    lines.append("---")
    return "\n".join(lines)


def build_prompt(
    update: dict[str, Any],
    section: dict[str, Any] | None,
    impact_items: list[dict[str, Any]],
) -> str:
    prompt_id = prompt_id_for(update)
    section_title = section.get("title") if section else "unknown section"
    related_artifacts = as_list(section.get("related_artifacts") if section else [])
    impacts = impact_items or []
    impact_summary = "; ".join(
        str(item.get("summary") or item.get("impact_type") or "impact")
        for item in impacts
        if isinstance(item, dict)
    )
    if not impact_summary:
        impact_summary = "TODO: describe dissertation impact before patch generation."
    artifacts_text = (
        "\n".join(f"- {artifact}" for artifact in related_artifacts) or "- none"
    )
    return "\n".join(
        [
            format_front_matter(front_matter(update, prompt_id)),
            "",
            f"# Dissertation Section Update Prompt — {prompt_id}",
            "",
            "Подготовь markdown patch для диссертации. Не редактируй DOCX напрямую.",
            "",
            "## Контекст",
            "",
            f"- Section ID: {update.get('section_id') or ''}",
            f"- Section title: {section_title}",
            f"- Source packet: {update.get('source_packet') or ''}",
            f"- Update reason: {update.get('reason') or 'TODO: describe reason.'}",
            f"- Required action: {update.get('required_action') or 'TODO: describe action.'}",
            "",
            "## Impact Summary",
            "",
            impact_summary,
            "",
            "## Related Tartip Artifacts",
            "",
            artifacts_text,
            "",
            "## Hard Constraints",
            "",
            "- DOCX update is forbidden in this prompt.",
            "- Prepare only a markdown patch proposal.",
            "- Do not add bibliography entries without citation request.",
            "- Do not present Codex or GRACE as scientific results.",
            "- Do not claim direct GESN selection by BIM element.",
            "- Do not strengthen experiment conclusions beyond the control fragment.",
            "",
            "## Required Output",
            "",
            "Return a markdown patch and a short list of assumptions. If data is insufficient, return TODO items instead of inventing content.",
            "",
        ]
    )


def eligible_updates(queue: dict[str, Any]) -> list[dict[str, Any]]:
    updates = queue.get("section_updates", [])
    if not isinstance(updates, list):
        raise ValueError("section-update-queue.yml section_updates must be a list")
    result: list[dict[str, Any]] = []
    for update in updates:
        if not isinstance(update, dict):
            continue
        status = str(update.get("status") or "pending")
        if status in {"pending", "requires_review"}:
            result.append(update)
    return result


def main() -> int:
    impact_log = load_mapping(IMPACT_LOG_PATH)
    queue = load_mapping(SECTION_QUEUE_PATH)
    artifact_map = load_mapping(ARTIFACT_MAP_PATH)
    sections = sections_by_id(artifact_map)
    impacts = impacts_by_packet(impact_log)
    PROMPT_DIR.mkdir(parents=True, exist_ok=True)

    created: list[Path] = []
    for update in eligible_updates(queue):
        prompt_id = prompt_id_for(update)
        path = prompt_path(prompt_id)
        if path.exists():
            continue
        source_packet = str(update.get("source_packet") or "")
        section_id = str(update.get("section_id") or "")
        text = build_prompt(
            update, sections.get(section_id), impacts.get(source_packet, [])
        )
        path.write_text(text, encoding="utf-8")
        created.append(path)

    if not created:
        print("No dissertation section updates require prompt generation.")
        return 0
    for path in created:
        print(f"Generated dissertation prompt: {rel(path)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
