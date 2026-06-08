#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from reference_utils import load_data


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DISSERTATION_DIR = PROJECT_ROOT / "docs" / "dissertation"
PROMPT_QUEUE_DIR = DISSERTATION_DIR / "prompt-queue"
FORBIDDEN_CLAIMS_PATH = DISSERTATION_DIR / "prompt-profiles" / "forbidden-claims.yml"
ACCEPTED_PATCH_DIR = DISSERTATION_DIR / "patches" / "accepted"


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(PROJECT_ROOT))
    except ValueError:
        return str(path)


def prompt_files() -> list[Path]:
    if not PROMPT_QUEUE_DIR.exists():
        return []
    return sorted(PROMPT_QUEUE_DIR.glob("**/*.prompt.md"))


def parse_front_matter(path: Path) -> tuple[dict[str, str], str, list[str]]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}, text, [f"{rel(path)}: missing YAML front matter"]
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text, [f"{rel(path)}: unterminated YAML front matter"]
    raw = text[4:end].strip()
    body = text[end + 4 :].lstrip("\n")
    meta: dict[str, str] = {}
    errors: list[str] = []
    for line in raw.splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            errors.append(f"{rel(path)}: invalid front matter line: {line}")
            continue
        key, value = line.split(":", 1)
        cleaned = value.strip()
        if (cleaned.startswith('"') and cleaned.endswith('"')) or (
            cleaned.startswith("'") and cleaned.endswith("'")
        ):
            cleaned = cleaned[1:-1]
        meta[key.strip()] = cleaned
    return meta, body, errors


def load_forbidden_claims() -> list[dict[str, Any]]:
    if not FORBIDDEN_CLAIMS_PATH.exists():
        return []
    data = load_data(FORBIDDEN_CLAIMS_PATH)
    claims = data.get("forbidden_claims", []) if isinstance(data, dict) else []
    return [claim for claim in claims if isinstance(claim, dict)]


def contains_forbidden_claim(text: str, claim: str) -> bool:
    normalized_text = " ".join(text.lower().split())
    normalized_claim = " ".join(claim.lower().split())
    return bool(normalized_claim and normalized_claim in normalized_text)


def patch_is_accepted(value: str) -> bool:
    if not value:
        return False
    path = PROJECT_ROOT / value if not value.startswith("/") else Path(value)
    if not path.exists():
        path = ACCEPTED_PATCH_DIR / value
    return path.exists() and ACCEPTED_PATCH_DIR in path.resolve().parents


def validate_prompt(path: Path, claims: list[dict[str, Any]]) -> list[str]:
    meta, body, errors = parse_front_matter(path)
    prompt_id = meta.get("prompt_id", "")
    prompt_type = meta.get("prompt_type", "")
    status = meta.get("status", "")
    accepted_by = meta.get("accepted_by", "")
    accepted_patch = meta.get("accepted_patch", "") or meta.get("patch_id", "")

    if not prompt_id:
        errors.append(f"{rel(path)}: prompt_id is required")
    if status == "accepted" and not accepted_by:
        errors.append(f"{rel(path)}: status=accepted requires accepted_by")
    if accepted_by == "Codex":
        errors.append(f"{rel(path)}: accepted_by must not be Codex")
    if prompt_type == "docx_update":
        if not patch_is_accepted(accepted_patch):
            errors.append(
                f"{rel(path)}: docx_update prompt requires accepted patch reference"
            )
        if "explicit user request" not in body.lower():
            errors.append(
                f"{rel(path)}: docx_update prompt must require explicit user request"
            )
    body_lower = body.lower()
    if (
        "edit docx directly" in body_lower
        and "do not edit docx directly" not in body_lower
    ):
        errors.append(f"{rel(path)}: direct DOCX editing is not allowed")
    if (
        "редактировать docx напрямую" in body_lower
        and "не редактировать docx напрямую" not in body_lower
    ):
        errors.append(f"{rel(path)}: direct DOCX editing is not allowed")
    for claim in claims:
        forbidden = str(claim.get("forbidden_claim") or "")
        if contains_forbidden_claim(body, forbidden):
            errors.append(
                f"{rel(path)}: contains forbidden claim {claim.get('id')}: {forbidden}"
            )
    return errors


def validate_prompts() -> list[str]:
    errors: list[str] = []
    claims = load_forbidden_claims()
    for path in prompt_files():
        errors.extend(validate_prompt(path, claims))
    return errors


def main() -> int:
    errors = validate_prompts()
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Dissertation prompt validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
