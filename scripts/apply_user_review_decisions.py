#!/usr/bin/env python3
from __future__ import annotations

import argparse
import difflib
import hashlib
import os
import sys
import tempfile
from pathlib import Path
from typing import Any

from reference_utils import load_data


PROJECT_ROOT = Path(__file__).resolve().parents[1]
WORKBENCH_PATH = PROJECT_ROOT / "docs" / "user-review-workbench.yml"
DECISION_KEYS = {"acceptance_decision", "accepted_by", "accepted_at", "comments"}
SUPPORTED_NON_ACCEPTANCE_TYPES = {
    "manual_verification",
    "user_action",
    "audit_finding",
    "requires_user_approval",
}


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


def decision_text(path: Path, decision: dict[str, str]) -> str:
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
    return "\n".join(new_lines) + "\n"


def atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=path.parent,
        text=True,
    )
    tmp_path = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as file:
            file.write(text)
        os.replace(tmp_path, path)
    finally:
        if tmp_path.exists():
            tmp_path.unlink()


def unified_diff(path: Path, old_text: str, new_text: str) -> str:
    return "".join(
        difflib.unified_diff(
            old_text.splitlines(keepends=True),
            new_text.splitlines(keepends=True),
            fromfile=f"a/{rel(path)}",
            tofile=f"b/{rel(path)}",
        )
    )


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


def planned_item_change(item: dict[str, Any]) -> tuple[str | None, str, str]:
    item_id = str(item.get("id") or "<missing id>")
    item_type = str(item.get("type") or "")
    if item_type != "acceptance":
        if item_type in SUPPORTED_NON_ACCEPTANCE_TYPES:
            return (
                None,
                f"{item_id}: skipped; {item_type} decisions are warning-only in this version",
                "",
            )
        return None, f"{item_id}: skipped; unsupported item type: {item_type}", ""
    decision, reason = valid_user_decision(item)
    if decision is None:
        return None, f"{item_id}: skipped; {reason}", ""
    target = str(item.get("target_decision_file") or "")
    if not target:
        return None, f"{item_id}: skipped; target_decision_file is missing", ""
    target_path = PROJECT_ROOT / target
    if not target_path.exists():
        return None, f"{item_id}: skipped; target file does not exist: {target}", ""
    expected_checksum = str(item.get("source_checksum_sha256") or "")
    if not expected_checksum:
        return None, f"{item_id}: skipped; source checksum is missing", ""
    current_checksum = checksum(target_path)
    if current_checksum != expected_checksum:
        return None, f"{item_id}: skipped; stale source checksum for {target}", ""
    current_decision = parse_decision(target_path)
    if current_decision.get("acceptance_decision") == "accepted":
        return (
            None,
            f"{item_id}: skipped; acceptance report is already accepted and cannot be overwritten without explicit user approval",
            "",
        )
    old_text = target_path.read_text(encoding="utf-8")
    new_text = decision_text(target_path, decision)
    if old_text == new_text:
        return None, f"{item_id}: skipped; no decision diff for {target}", ""
    return (
        rel(target_path),
        f"{item_id}: planned change for {target}",
        unified_diff(target_path, old_text, new_text),
    )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Safely apply user acceptance decisions from docs/user-review-workbench.yml."
        )
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--dry-run",
        action="store_true",
        help="Show planned changes without writing files. This is the default mode.",
    )
    mode.add_argument(
        "--apply",
        action="store_true",
        help="Apply planned acceptance decisions after all safety checks pass.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])
    apply_changes = bool(args.apply)
    mode = "apply" if apply_changes else "dry-run"
    if not WORKBENCH_PATH.exists():
        print(f"ERROR: missing {rel(WORKBENCH_PATH)}", file=sys.stderr)
        return 1
    workbench = load_workbench()
    items = workbench.get("active_review_items", [])
    planned: list[tuple[str, str]] = []
    affected: list[str] = []
    messages: list[str] = []
    for item in items if isinstance(items, list) else []:
        if not isinstance(item, dict):
            continue
        path, message, diff = planned_item_change(item)
        messages.append(message)
        if path:
            affected.append(path)
            planned.append((path, diff))
    print(f"Mode: {mode}")
    for message in messages:
        prefix = "PLAN" if ": planned " in message else "WARNING"
        print(f"{prefix}: {message}")
    if affected:
        print("Affected files:")
        for path in sorted(set(affected)):
            print(f"- {path}")
        print("Planned diffs:")
        for _path, diff in planned:
            print(diff, end="" if diff.endswith("\n") else "\n")
    else:
        print("No acceptance report changes planned.")
    if apply_changes and planned:
        for path, _diff in planned:
            target_path = PROJECT_ROOT / path
            item = next(
                item
                for item in items
                if isinstance(item, dict)
                and str(item.get("target_decision_file") or "") == path
            )
            decision, _reason = valid_user_decision(item)
            if decision is None:
                raise RuntimeError(f"decision disappeared before apply: {path}")
            atomic_write(target_path, decision_text(target_path, decision))
        print("Applied acceptance reports:")
        for path in sorted(set(affected)):
            print(f"- {path}")
    elif not apply_changes:
        print("Dry run only; no files were modified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
