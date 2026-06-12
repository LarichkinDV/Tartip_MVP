from __future__ import annotations

import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT_ROOT / "scripts" / "sync_accepted_packet.py"
PACKET = "EP-100-SAMPLE"
NEXT_PACKET = "EP-101-NEXT"


def run_sync(root: Path, packet: str = PACKET, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            packet,
            *args,
            "--project-root",
            str(root),
        ],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def write_fixture(
    root: Path,
    *,
    decision: str = "accepted",
    accepted_by: str = "Дмитрий",
    accepted_at: str = "2026-06-12",
    packet_status: str = "ready_for_acceptance",
    include_report: bool = True,
    include_in_accepted_packets: bool = False,
) -> None:
    (root / "docs" / "acceptance").mkdir(parents=True)
    (root / "docs" / "grace").mkdir(parents=True)
    (root / "docs" / "other").mkdir(parents=True)
    if include_report:
        (root / "docs" / "acceptance" / f"{PACKET}.acceptance.md").write_text(
            "\n".join(
                [
                    f"# Acceptance Report - {PACKET}",
                    "",
                    "## User-owned решение",
                    "",
                    "```yaml",
                    f"acceptance_decision: {decision}",
                    f"accepted_by: {accepted_by}",
                    f"accepted_at: {accepted_at}",
                    "comments: User accepted the packet.",
                    "```",
                    "",
                ]
            ),
            encoding="utf-8",
        )
    (root / "docs" / "acceptance" / "EP-099-PREVIOUS.acceptance.md").write_text(
        "acceptance_decision: accepted\n"
        "accepted_by: Дмитрий\n"
        "accepted_at: 2026-06-11\n"
        "comments: Previous packet.\n",
        encoding="utf-8",
    )
    (root / "docs" / "grace" / "execution-packets.xml").write_text(
        f"""<ExecutionPackets version="1.0">
  <Packet id="EP-099-PREVIOUS" status="accepted">
    <Name>Previous</Name>
  </Packet>
  <Packet id="{PACKET}" status="{packet_status}">
    <Name>Sample</Name>
    <ExpectedArtifacts>
      <Artifact>docs/acceptance/{PACKET}.acceptance.md</Artifact>
      <Artifact>docs/other/sample.md</Artifact>
    </ExpectedArtifacts>
    <AcceptanceCriteria>
      <Criterion id="AC-001">Sample criterion.</Criterion>
    </AcceptanceCriteria>
  </Packet>
</ExecutionPackets>
""",
        encoding="utf-8",
    )
    accepted_packets = "    - EP-099-PREVIOUS\n"
    if include_in_accepted_packets:
        accepted_packets += f"    - {PACKET}\n"
    (root / "docs" / "project-state.yml").write_text(
        "project_state:\n"
        "  schema_version: 1\n"
        "  updated_at: 2026-06-12\n"
        "  state_mode: ready_for_acceptance\n"
        f"  active_execution_packet: {PACKET}\n"
        "  last_accepted_execution_packet: EP-099-PREVIOUS\n"
        "  last_completed_execution_packet: EP-099-PREVIOUS\n"
        f"  next_recommended_packet: {NEXT_PACKET}\n"
        "  deferred_follow_up_packets: []\n"
        "  accepted_packets:\n"
        f"{accepted_packets}"
        "  monthly_scopes: []\n",
        encoding="utf-8",
    )
    (root / "docs" / "project-plan.md").write_text(
        "# Project Plan\n\n"
        "Current execution packet: `EP-100-SAMPLE`.\n\n"
        "```yaml\n"
        "project_state: ready_for_acceptance\n"
        "active_execution_packet: EP-100-SAMPLE\n"
        "last_accepted_execution_packet: EP-099-PREVIOUS\n"
        "last_completed_execution_packet: EP-099-PREVIOUS\n"
        f"next_recommended_packet: {NEXT_PACKET}\n"
        "```\n\n"
        "```yaml\n"
        "post_acceptance_baseline:\n"
        "  accepted_packets:\n"
        "    - EP-099-PREVIOUS\n"
        "```\n\n"
        "| Packet | Name | Status |\n"
        "|---|---|---|\n"
        "| EP-100-SAMPLE | Sample | ready_for_acceptance |\n",
        encoding="utf-8",
    )
    (root / "docs" / "status-report.md").write_text(
        "# Status Report\n\n"
        "## 2. Текущий Execution Packet\n\n"
        "`EP-100-SAMPLE`\n\n"
        "```yaml\n"
        "project_state: ready_for_acceptance\n"
        "active_execution_packet: EP-100-SAMPLE\n"
        "last_accepted_execution_packet: EP-099-PREVIOUS\n"
        "last_completed_execution_packet: EP-099-PREVIOUS\n"
        f"next_recommended_packet: {NEXT_PACKET}\n"
        "```\n\n"
        "```yaml\n"
        "post_acceptance_baseline:\n"
        "  accepted_packets:\n"
        "    - EP-099-PREVIOUS\n"
        "```\n",
        encoding="utf-8",
    )
    (root / "docs" / "artifact-registry.yml").write_text(
        "registry_version: 1\n"
        "artifacts:\n"
        "  -\n"
        "    artifact_id: ART-ACCEPTANCE-EP-099-PREVIOUS\n"
        "    path: docs/acceptance/EP-099-PREVIOUS.acceptance.md\n"
        "    status: active\n"
        "    protection:\n"
        "      protection_status: protected\n"
        "      source_category: source_acceptance\n"
        "      change_requires_user_approval: true\n",
        encoding="utf-8",
    )
    (root / "docs" / "other" / "sample.md").write_text("sample\n", encoding="utf-8")


def snapshot(root: Path) -> dict[str, str]:
    return {
        str(path.relative_to(root)): path.read_text(encoding="utf-8")
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def test_dry_run_does_not_modify_files(tmp_path: Path) -> None:
    write_fixture(tmp_path)
    before = snapshot(tmp_path)

    result = run_sync(tmp_path, PACKET, "--dry-run")

    assert result.returncode == 0, result.stderr
    assert "Dry run only; no files were modified." in result.stdout
    assert snapshot(tmp_path) == before


def test_requires_explicit_mode(tmp_path: Path) -> None:
    write_fixture(tmp_path)

    result = run_sync(tmp_path, PACKET)

    assert result.returncode == 2
    assert "one of the arguments --dry-run --apply is required" in result.stderr


def test_apply_syncs_accepted_packet(tmp_path: Path) -> None:
    write_fixture(tmp_path)

    result = run_sync(tmp_path, PACKET, "--apply")

    assert result.returncode == 0, result.stderr
    assert f'<Packet id="{PACKET}" status="accepted">' in (
        tmp_path / "docs" / "grace" / "execution-packets.xml"
    ).read_text(encoding="utf-8")
    state = (tmp_path / "docs" / "project-state.yml").read_text(encoding="utf-8")
    assert f"- {PACKET}" in state
    assert "active_execution_packet: none" in state
    assert f"last_accepted_execution_packet: {PACKET}" in state
    assert f"next_recommended_packet: {NEXT_PACKET}" in state
    registry = (tmp_path / "docs" / "artifact-registry.yml").read_text(encoding="utf-8")
    assert f"path: docs/acceptance/{PACKET}.acceptance.md" in registry
    assert "protection_status: protected" in registry


def test_rejects_missing_acceptance_report(tmp_path: Path) -> None:
    write_fixture(tmp_path, include_report=False)

    result = run_sync(tmp_path, PACKET, "--dry-run")

    assert result.returncode == 1
    assert "acceptance report not found" in result.stderr


def test_rejects_pending_acceptance_decision(tmp_path: Path) -> None:
    write_fixture(tmp_path, decision="pending")

    result = run_sync(tmp_path, PACKET, "--dry-run")

    assert result.returncode == 1
    assert "acceptance_decision must be accepted" in result.stderr


def test_rejects_empty_accepted_by(tmp_path: Path) -> None:
    write_fixture(tmp_path, accepted_by="")

    result = run_sync(tmp_path, PACKET, "--dry-run")

    assert result.returncode == 1
    assert "accepted_by is required" in result.stderr


def test_rejects_accepted_by_codex(tmp_path: Path) -> None:
    write_fixture(tmp_path, accepted_by="Codex")

    result = run_sync(tmp_path, PACKET, "--dry-run")

    assert result.returncode == 1
    assert "accepted_by must not be Codex" in result.stderr


def test_rejects_empty_accepted_at(tmp_path: Path) -> None:
    write_fixture(tmp_path, accepted_at="")

    result = run_sync(tmp_path, PACKET, "--dry-run")

    assert result.returncode == 1
    assert "accepted_at is required" in result.stderr


def test_does_not_modify_acceptance_report_user_fields(tmp_path: Path) -> None:
    write_fixture(tmp_path)
    report = tmp_path / "docs" / "acceptance" / f"{PACKET}.acceptance.md"
    before = report.read_text(encoding="utf-8")

    result = run_sync(tmp_path, PACKET, "--apply")

    assert result.returncode == 0, result.stderr
    assert report.read_text(encoding="utf-8") == before


def test_adds_packet_to_accepted_packets(tmp_path: Path) -> None:
    write_fixture(tmp_path)

    result = run_sync(tmp_path, PACKET, "--apply")

    assert result.returncode == 0, result.stderr
    assert f"- {PACKET}" in (
        tmp_path / "docs" / "project-state.yml"
    ).read_text(encoding="utf-8")


def test_sets_execution_packet_status_to_accepted(tmp_path: Path) -> None:
    write_fixture(tmp_path)

    result = run_sync(tmp_path, PACKET, "--apply")

    assert result.returncode == 0, result.stderr
    assert f'<Packet id="{PACKET}" status="accepted">' in (
        tmp_path / "docs" / "grace" / "execution-packets.xml"
    ).read_text(encoding="utf-8")


def test_resets_active_execution_packet_to_none(tmp_path: Path) -> None:
    write_fixture(tmp_path)

    result = run_sync(tmp_path, PACKET, "--apply")

    assert result.returncode == 0, result.stderr
    assert "active_execution_packet: none" in (
        tmp_path / "docs" / "project-state.yml"
    ).read_text(encoding="utf-8")


def test_preserves_next_recommended_packet(tmp_path: Path) -> None:
    write_fixture(tmp_path)

    result = run_sync(tmp_path, PACKET, "--apply")

    assert result.returncode == 0, result.stderr
    assert f"next_recommended_packet: {NEXT_PACKET}" in (
        tmp_path / "docs" / "project-state.yml"
    ).read_text(encoding="utf-8")


def test_removes_next_packet_from_deferred_follow_up_packets(tmp_path: Path) -> None:
    write_fixture(tmp_path)
    state_path = tmp_path / "docs" / "project-state.yml"
    state_path.write_text(
        state_path.read_text(encoding="utf-8").replace(
            "  deferred_follow_up_packets: []\n",
            "  deferred_follow_up_packets:\n"
            "    - packet_id: EP-016-REFERENCE-INTAKE-PREPARATION\n"
            "      reason: Deferred.\n"
            f"    - packet_id: {NEXT_PACKET}\n"
            "      reason: Next after acceptance.\n",
        ),
        encoding="utf-8",
    )

    result = run_sync(tmp_path, PACKET, "--apply")

    assert result.returncode == 0, result.stderr
    state = state_path.read_text(encoding="utf-8")
    assert "packet_id: EP-016-REFERENCE-INTAKE-PREPARATION" in state
    assert f"packet_id: {NEXT_PACKET}" not in state
    assert f"next_recommended_packet: {NEXT_PACKET}" in state


def test_updates_registry_without_style_only_empty_list_churn(tmp_path: Path) -> None:
    write_fixture(tmp_path)
    registry_path = tmp_path / "docs" / "artifact-registry.yml"
    registry_path.write_text(
        "registry_version: 1\n"
        "artifacts:\n"
        "  -\n"
        f"    artifact_id: ART-ACCEPTANCE-{PACKET}\n"
        f"    path: docs/acceptance/{PACKET}.acceptance.md\n"
        "    status: active\n"
        "    depends_on:\n"
        "      []\n"
        "    supersedes:\n"
        "      []\n"
        "    notes: \"Codex status ready_for_acceptance; user decision remains pending.\"\n"
        "    protection:\n"
        "      protection_status: not_protected_pending\n"
        "      source_category: source_acceptance\n"
        "      accepted_in: null\n"
        "      user_decision_source: null\n"
        "      change_requires_user_approval: false\n"
        "      allowed_update_modes:\n"
        "        - execution_packet_change\n"
        "      generator: null\n"
        "      derived_from:\n"
        "        []\n"
        "      regeneration_command: null\n"
        "      protected_since: null\n"
        "  -\n"
        "    artifact_id: ART-ACCEPTANCE-EP-099-PREVIOUS\n"
        "    path: docs/acceptance/EP-099-PREVIOUS.acceptance.md\n"
        "    status: active\n",
        encoding="utf-8",
    )

    result = run_sync(tmp_path, PACKET, "--apply")

    assert result.returncode == 0, result.stderr
    registry = registry_path.read_text(encoding="utf-8")
    assert "depends_on:\n      []" in registry
    assert "supersedes:\n      []" in registry
    assert "derived_from:\n        []" in registry
    assert "protection_status: protected" in registry


def test_idempotent_second_apply_produces_no_changes(tmp_path: Path) -> None:
    write_fixture(tmp_path)
    first = run_sync(tmp_path, PACKET, "--apply")
    assert first.returncode == 0, first.stderr
    before = snapshot(tmp_path)

    second = run_sync(tmp_path, PACKET, "--apply")

    assert second.returncode == 0, second.stderr
    assert "No changes required" in second.stdout
    assert snapshot(tmp_path) == before


def test_historical_accepted_packet_is_noop_while_other_packet_is_active(
    tmp_path: Path,
) -> None:
    write_fixture(tmp_path)
    first = run_sync(tmp_path, PACKET, "--apply")
    assert first.returncode == 0, first.stderr
    state_path = tmp_path / "docs" / "project-state.yml"
    state_path.write_text(
        state_path.read_text(encoding="utf-8")
        .replace("state_mode: accepted_baseline", "state_mode: ready_for_acceptance")
        .replace("active_execution_packet: none", "active_execution_packet: EP-101-NEXT"),
        encoding="utf-8",
    )
    before = snapshot(tmp_path)

    result = run_sync(tmp_path, PACKET, "--dry-run")

    assert result.returncode == 0, result.stderr
    assert "No changes required" in result.stdout
    assert snapshot(tmp_path) == before


def test_rejects_inconsistent_accepted_state(tmp_path: Path) -> None:
    write_fixture(tmp_path, packet_status="accepted", include_in_accepted_packets=False)

    result = run_sync(tmp_path, PACKET, "--dry-run")

    assert result.returncode == 1
    assert "project-state accepted_packets misses it" in result.stderr


def test_does_not_touch_unrelated_acceptance_reports(tmp_path: Path) -> None:
    write_fixture(tmp_path)
    previous_report = tmp_path / "docs" / "acceptance" / "EP-099-PREVIOUS.acceptance.md"
    before = previous_report.read_text(encoding="utf-8")

    result = run_sync(tmp_path, PACKET, "--apply")

    assert result.returncode == 0, result.stderr
    assert previous_report.read_text(encoding="utf-8") == before
