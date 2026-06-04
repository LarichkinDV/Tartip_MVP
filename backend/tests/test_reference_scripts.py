import json
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def run_script(*args: str, input_text: str | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args],
        cwd=PROJECT_ROOT,
        input=input_text,
        capture_output=True,
        text=True,
        check=True,
    )


def test_canonical_hash_ignores_json_key_order() -> None:
    first = run_script("scripts/compute_reference_hash.py", "-", input_text='{"b": 2, "a": 1}')
    second = run_script("scripts/compute_reference_hash.py", "-", input_text='{"a":1,"b":2}')

    assert first.stdout.strip() == second.stdout.strip()


def test_compare_reference_fixture_delta_counts() -> None:
    result = run_script("scripts/compare_reference_releases.py", "--fixture")
    payload = json.loads(result.stdout)

    assert payload["logical_objects_v1"] == 10
    assert payload["effective_lookup_v2_count"] == 10
    assert payload["counts"] == {
        "added": 1,
        "changed": 1,
        "deleted": 1,
        "unchanged": 8,
        "new_revision_count": 3,
        "change_set_count": 3,
    }
    assert payload["added_records"] == ["fake-ref-011"]
    assert payload["changed_records"] == ["fake-ref-003"]
    assert payload["deleted_records"] == ["fake-ref-010"]
    assert payload["rule_status_updates"] == [
        {
            "rule_id": "partition_brick_120_reinf",
            "natural_key": "fake-ref-003",
            "dependency_type": "normative_candidate_fixture",
            "new_status": "requires_norm_review",
        }
    ]
