#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from reference_utils import canonical_payload_hash, load_data, record_payload, records_by_natural_key


PROJECT_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = PROJECT_ROOT / "backend" / "tests" / "fixtures" / "reference"


def compare_values(old: Any, new: Any, field_path: str = "payload") -> list[dict[str, Any]]:
    if old == new:
        return []
    if isinstance(old, dict) and isinstance(new, dict):
        details: list[dict[str, Any]] = []
        for key in sorted(set(old) | set(new)):
            child_path = f"{field_path}.{key}"
            if key not in old:
                details.append(change_detail(child_path, "added", None, new[key]))
            elif key not in new:
                details.append(change_detail(child_path, "deleted", old[key], None))
            else:
                details.extend(compare_values(old[key], new[key], child_path))
        return details
    return [change_detail(field_path, "changed", old, new)]


def change_detail(field_path: str, change_type: str, old: Any, new: Any) -> dict[str, Any]:
    return {
        "field_path": field_path,
        "change_type": change_type,
        "old_value_hash": canonical_payload_hash(old) if old is not None else None,
        "new_value_hash": canonical_payload_hash(new) if new is not None else None,
        "old_value_preview": preview(old),
        "new_value_preview": preview(new),
        "severity": "medium" if change_type == "changed" else "low",
    }


def preview(value: Any) -> str | None:
    if value is None:
        return None
    text = json.dumps(value, ensure_ascii=False, sort_keys=True)
    return text[:120]


def load_dependencies(path: Path | None) -> list[dict[str, Any]]:
    if path is None or not path.exists():
        return []
    data = load_data(path)
    dependencies = data.get("dependencies", []) if isinstance(data, dict) else []
    return dependencies if isinstance(dependencies, list) else []


def compare_releases(old_path: Path, new_path: Path, dependencies_path: Path | None = None) -> dict[str, Any]:
    old_records = records_by_natural_key(load_data(old_path))
    new_records = records_by_natural_key(load_data(new_path))

    old_hashes = {key: canonical_payload_hash(record_payload(record)) for key, record in old_records.items()}
    new_hashes = {key: canonical_payload_hash(record_payload(record)) for key, record in new_records.items()}

    old_keys = set(old_records)
    new_keys = set(new_records)
    added = sorted(new_keys - old_keys)
    deleted = sorted(old_keys - new_keys)
    shared = sorted(old_keys & new_keys)
    changed = sorted(key for key in shared if old_hashes[key] != new_hashes[key])
    unchanged = sorted(key for key in shared if old_hashes[key] == new_hashes[key])

    changed_details = {
        key: compare_values(record_payload(old_records[key]), record_payload(new_records[key]))
        for key in changed
    }

    impacted_rules = []
    changed_or_deleted = set(changed) | set(deleted)
    for dependency in load_dependencies(dependencies_path):
        natural_key = dependency.get("natural_key")
        if natural_key in changed_or_deleted and dependency.get("required_review_on_change", True):
            impacted_rules.append(
                {
                    "rule_id": dependency.get("rule_id"),
                    "natural_key": natural_key,
                    "dependency_type": dependency.get("dependency_type"),
                    "new_status": "requires_norm_review",
                }
            )

    return {
        "old_release_path": str(old_path),
        "new_release_path": str(new_path),
        "logical_objects_v1": len(old_records),
        "effective_lookup_v2_count": len(new_records),
        "added_records": added,
        "changed_records": changed,
        "deleted_records": deleted,
        "unchanged_records": unchanged,
        "counts": {
            "added": len(added),
            "changed": len(changed),
            "deleted": len(deleted),
            "unchanged": len(unchanged),
            "new_revision_count": len(added) + len(changed) + len(deleted),
            "change_set_count": len(added) + len(changed) + len(deleted),
        },
        "changed_details": changed_details,
        "rule_status_updates": impacted_rules,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare two small reference release fixtures.")
    parser.add_argument("--old", type=Path, help="Old release JSON/YAML fixture path.")
    parser.add_argument("--new", type=Path, help="New release JSON/YAML fixture path.")
    parser.add_argument("--dependencies", type=Path, help="Optional rule dependency fixture path.")
    parser.add_argument("--fixture", action="store_true", help="Use bundled fake fixtures.")
    args = parser.parse_args()

    if args.fixture:
        old_path = FIXTURE_DIR / "fake_reference_v1.json"
        new_path = FIXTURE_DIR / "fake_reference_v2.json"
        dependencies_path = FIXTURE_DIR / "fake_reference_dependencies.json"
    else:
        if args.old is None or args.new is None:
            parser.error("--old and --new are required unless --fixture is used")
        old_path = args.old
        new_path = args.new
        dependencies_path = args.dependencies

    print(json.dumps(compare_releases(old_path, new_path, dependencies_path), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
