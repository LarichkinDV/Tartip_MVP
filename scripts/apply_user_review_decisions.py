#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import sys
from pathlib import Path
from typing import Any

from reference_utils import load_data


PROJECT_ROOT = Path(__file__).resolve().parents[1]
WORKBENCH_PATH = PROJECT_ROOT / "docs" / "user-review-workbench.yml"
DECISION_KEYS = {"acceptance_decision", "accepted_by", "accepted_at", "comments"}


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(PROJECT_ROOT))
    except ValueError:
        return str(path)


def checksum(path: Path) -> str:
    if not path.exists():
        return ""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_workbench() -> dict[str, Any]:
    data = load_data(WORKBENCH_PATH)
    if not isinstance(data, dict):
        return {}
    root = data.get("user_review_workbench", {})
    return root if isinstance(root, dict) else {}


def parse_decision(path: Path) -> dict[str, str]:
    values = {
        "acceptance_decision": "",
        "accepted_by": "",
        "accepted_at": "",
        "comments": "",
    }
    if not path.exists():
        return values
    for line in path.read_text(encoding="utf-8").splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        if key in values:
            values[key] = value.strip()
    return values


def replace_decision(path: Path, decision: dict[str, str]) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    seen: set[str] = set()
    new_lines: list[str] = []
    for line in lines:
        if ":" not in line:
            new_lines.append(line)
            continue
        key, _ = line.split(":", 1)
        stripped_key = key.strip()
        if stripped_key in DECISION_KEYS:
            new_lines.append(f"{stripped_key}: {decision[stripped_key]}")
            seen.add(stripped_key)
        else:
            new_lines.append(line)
    for key in ["acceptance_decision", "accepted_by", "accepted_at", "comments"]:
        if key not in seen:
            new_lines.append(f"{key}: {decision[key]}")
    path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")


def valid_user_decision(item: dict[str, Any]) -> tuple[dict[str, str] | None, str]:
    decision = item.get("user_decision")
    if not isinstance(decision, dict):
        return None, "user_decision is missing"
    values = {
        "acceptance_decision": str(decision.get("acceptance_decision") or "").strip(),
        "accepted_by": str(decision.get("accepted_by") or "").strip(),
        "accepted_at": str(decision.get("accepted_at") or "").strip(),
        "comments": str(decision.get("comments") or "").strip(),
    }
    if values["acceptance_decision"] in {"", "pending"}:
        return None, "acceptance_decision is empty or pending"
    if values["acceptance_decision"] != "accepted":
        return None, "only acceptance_decision=accepted is supported in this version"
    if not values["accepted_by"]:
        return None, "accepted_by is empty"
    if values["accepted_by"] == "Codex":
        return None, "accepted_by must not be Codex"
    if not values["accepted_at"]:
        return None, "accepted_at is empty"
    if not values["comments"]:
        return None, "comments is empty"
    if item.get("blockers"):
        return None, "active blockers exist"
    return values, ""


def apply_item(item: dict[str, Any]) -> tuple[str | None, str]:
    item_id = str(item.get("id") or "<missing id>")
    if item.get("type") != "acceptance":
        return None, f"{item_id}: skipped; only acceptance items are supported"
    decision, reason = valid_user_decision(item)
    if decision is None:
        return None, f"{item_id}: skipped; {reason}"
    target = str(item.get("target_decision_file") or "")
    if not target:
        return None, f"{item_id}: skipped; target_decision_file is missing"
    target_path = PROJECT_ROOT / target
    if not target_path.exists():
        return None, f"{item_id}: skipped; target file does not exist: {target}"
    expected_checksum = str(item.get("source_checksum_sha256") or "")
    if not expected_checksum:
        return None, f"{item_id}: skipped; source checksum is missing"
    current_checksum = checksum(target_path)
    if current_checksum != expected_checksum:
        return None, f"{item_id}: skipped; stale source checksum for {target}"
    current_decision = parse_decision(target_path)
    if (
        current_decision.get("acceptance_decision") == "accepted"
        and current_decision != decision
    ):
        return (
            None,
            f"{item_id}: skipped; acceptance report is already accepted with another decision",
        )
    replace_decision(target_path, decision)
    return rel(target_path), f"{item_id}: applied to {target}"


def main() -> int:
    if not WORKBENCH_PATH.exists():
        print(f"ERROR: missing {rel(WORKBENCH_PATH)}", file=sys.stderr)
        return 1
    workbench = load_workbench()
    items = workbench.get("active_review_items", [])
    changed: list[str] = []
    messages: list[str] = []
    for item in items if isinstance(items, list) else []:
        if not isinstance(item, dict):
            continue
        path, message = apply_item(item)
        messages.append(message)
        if path:
            changed.append(path)
    for message in messages:
        prefix = "APPLIED" if ": applied " in message else "WARNING"
        print(f"{prefix}: {message}")
    if changed:
        print("Changed acceptance reports:")
        for path in sorted(set(changed)):
            print(f"- {path}")
    else:
        print("No acceptance reports changed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
