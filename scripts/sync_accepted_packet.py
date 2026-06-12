#!/usr/bin/env python3
from __future__ import annotations

import argparse
import difflib
import os
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from reference_utils import dump_yaml, load_data


DEFAULT_PROJECT_ROOT = Path(__file__).resolve().parents[1]
USER_OWNED_FIELDS = {
    "acceptance_decision",
    "accepted_by",
    "accepted_at",
    "comments",
    "checked_by",
    "answered_by",
    "decided_by",
    "resolved_by",
    "resolution",
}
SYNC_REL_PATHS = {
    "docs/grace/execution-packets.xml",
    "docs/project-state.yml",
    "docs/project-plan.md",
    "docs/status-report.md",
    "docs/artifact-registry.yml",
    "docs/acceptance-dashboard.md",
    "docs/acceptance-dashboard.yml",
    "docs/user-action-dashboard.md",
    "docs/user-action-dashboard.yml",
    "docs/user-review-workbench.md",
    "docs/user-review-workbench.yml",
    "docs/verification-dashboard.md",
    "docs/verification-dashboard.yml",
}


@dataclass(frozen=True)
class Change:
    path: Path
    old_text: str
    new_text: str
    reason: str

    @property
    def changed(self) -> bool:
        return self.old_text != self.new_text


class SyncError(RuntimeError):
    pass


class CliError(RuntimeError):
    pass


def rel(root: Path, path: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


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


def unified_diff(root: Path, change: Change) -> str:
    return "".join(
        difflib.unified_diff(
            change.old_text.splitlines(keepends=True),
            change.new_text.splitlines(keepends=True),
            fromfile=f"a/{rel(root, change.path)}",
            tofile=f"b/{rel(root, change.path)}",
        )
    )


def yaml_text(value: Any) -> str:
    text = dump_yaml(value) + "\n"
    return re.sub(r"^(\s*[^:\n]+:)\n\s+\[\]$", r"\1 []", text, flags=re.MULTILINE)


def parse_acceptance_report(path: Path) -> dict[str, str]:
    values = {
        "acceptance_decision": "",
        "accepted_by": "",
        "accepted_at": "",
        "comments": "",
    }
    if not path.exists():
        raise SyncError(f"acceptance report not found: {path}")
    for line in path.read_text(encoding="utf-8").splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        if key in values:
            values[key] = value.strip()
    return values


def validate_acceptance_decision(packet_id: str, report: Path) -> dict[str, str]:
    values = parse_acceptance_report(report)
    if values["acceptance_decision"] != "accepted":
        raise SyncError(
            f"{packet_id}: acceptance_decision must be accepted before sync"
        )
    if not values["accepted_by"]:
        raise SyncError(f"{packet_id}: accepted_by is required before sync")
    if values["accepted_by"] == "Codex":
        raise SyncError(f"{packet_id}: accepted_by must not be Codex")
    if not values["accepted_at"]:
        raise SyncError(f"{packet_id}: accepted_at is required before sync")
    return values


def packet_statuses(packets_text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    pattern = re.compile(r'<Packet\s+id="([^"]+)"\s+status="([^"]+)"')
    for packet_id, status in pattern.findall(packets_text):
        result[packet_id] = status
    return result


def packet_expected_artifacts(packets_text: str, packet_id: str) -> set[str]:
    packet_match = re.search(
        rf'(<Packet\s+id="{re.escape(packet_id)}"\s+status="[^"]+".*?</Packet>)',
        packets_text,
        flags=re.DOTALL,
    )
    if not packet_match:
        return set()
    return {
        artifact.strip()
        for artifact in re.findall(
            r"<Artifact>(.*?)</Artifact>", packet_match.group(1), flags=re.DOTALL
        )
        if artifact.strip()
    }


def set_packet_status(packets_text: str, packet_id: str, status: str) -> str:
    pattern = re.compile(
        rf'(<Packet\s+id="{re.escape(packet_id)}"\s+status=")([^"]+)(">)'
    )
    matches = list(pattern.finditer(packets_text))
    if not matches:
        raise SyncError(f"{packet_id}: packet is missing in execution-packets.xml")
    if len(matches) > 1:
        raise SyncError(f"{packet_id}: duplicate packet entries found")
    return pattern.sub(rf"\g<1>{status}\g<3>", packets_text, count=1)


def load_project_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise SyncError("docs/project-state.yml not found")
    data = load_data(path)
    state = data.get("project_state", {}) if isinstance(data, dict) else {}
    if not isinstance(state, dict):
        raise SyncError("docs/project-state.yml must contain project_state mapping")
    return state


def update_project_state(
    state_path: Path,
    packet_id: str,
    next_packet: str,
) -> str:
    data = load_data(state_path)
    if not isinstance(data, dict) or not isinstance(data.get("project_state"), dict):
        raise SyncError("docs/project-state.yml must contain project_state mapping")
    state = data["project_state"]
    accepted_packets = state.get("accepted_packets")
    if not isinstance(accepted_packets, list):
        raise SyncError("docs/project-state.yml accepted_packets must be a list")
    if packet_id not in accepted_packets:
        accepted_packets.append(packet_id)
    state["state_mode"] = "accepted_baseline"
    state["active_execution_packet"] = "none"
    state["last_accepted_execution_packet"] = packet_id
    state["last_completed_execution_packet"] = packet_id
    state["next_recommended_packet"] = next_packet
    deferred = state.get("deferred_follow_up_packets")
    if isinstance(deferred, list):
        state["deferred_follow_up_packets"] = [
            item
            for item in deferred
            if not (
                isinstance(item, dict)
                and str(item.get("packet_id") or "").strip() == next_packet
            )
        ]
    tmp = tempfile.NamedTemporaryFile("w+", encoding="utf-8", delete=False)
    tmp_path = Path(tmp.name)
    try:
        tmp.close()
        tmp_path.write_text(yaml_text(data), encoding="utf-8")
        return tmp_path.read_text(encoding="utf-8")
    finally:
        if tmp_path.exists():
            tmp_path.unlink()


def add_baseline_packet(text: str, packet_id: str) -> str:
    marker = f"    - {packet_id}\n"
    if marker in text:
        return text
    pattern = re.compile(
        r"(post_acceptance_baseline:\n  accepted_packets:\n"
        r"(?:(?:    - [^\n]+\n)+))"
    )
    if pattern.search(text):
        return pattern.sub(lambda match: match.group(1) + marker, text, count=1)
    return text


def update_current_packet_text(text: str, packet_id: str, next_packet: str) -> str:
    replacements = {
        r"project_state: [^\n]+": "project_state: accepted_baseline",
        r"active_execution_packet: [^\n]+": "active_execution_packet: none",
        r"last_accepted_execution_packet: [^\n]+": (
            f"last_accepted_execution_packet: {packet_id}"
        ),
        r"last_completed_execution_packet: [^\n]+": (
            f"last_completed_execution_packet: {packet_id}"
        ),
        r"next_recommended_packet: [^\n]+": (
            f"next_recommended_packet: {next_packet}"
        ),
    }
    updated = text
    updated = re.sub(
        r"Current execution packet: `[^`]+`",
        "Current execution packet: `none`",
        updated,
        count=1,
    )
    updated = re.sub(
        r"(## \d+\. Текущий Execution Packet\n\n)`[^`]+`",
        r"\1`none`",
        updated,
        count=1,
    )
    for pattern, replacement in replacements.items():
        updated = re.sub(pattern, replacement, updated, count=1)
    updated = add_baseline_packet(updated, packet_id)
    updated = re.sub(
        rf"(\| {re.escape(packet_id)} \| [^|\n]+ \| )[^|\n]+(\|)",
        rf"\g<1>accepted\g<2>",
        updated,
    )
    return updated


def protected_acceptance_report_text(
    packet_id: str,
    report_rel_path: str,
) -> str:
    return (
        "    protection:\n"
        "      protection_status: protected\n"
        f"      protection_reason: \"Accepted {packet_id} acceptance report is a historical user decision record.\"\n"
        "      source_category: source_acceptance\n"
        f"      accepted_in: {packet_id}\n"
        f"      user_decision_source: {report_rel_path}\n"
        "      change_requires_user_approval: true\n"
        "      allowed_update_modes:\n"
        "        - approved_change_request_only\n"
        "      generator: null\n"
        "      derived_from:\n"
        "        []\n"
        "      regeneration_command: null\n"
        "      protected_since: null"
    )


def registry_artifact_text(packet_id: str, report_rel_path: str) -> str:
    return (
        "  -\n"
        f"    artifact_id: ART-ACCEPTANCE-{packet_id}\n"
        f"    name: \"{packet_id} acceptance report\"\n"
        "    type: acceptance_report\n"
        f"    path: {report_rel_path}\n"
        "    owner_module: M-PROJECT-PLANNING-AND-ACCEPTANCE\n"
        "    related_packets:\n"
        f"      - {packet_id}\n"
        "    related_requirements:\n"
        "      - REQ-015\n"
        "    status: active\n"
        f"    description: \"Acceptance report for {packet_id}.\"\n"
        "    created_at: null\n"
        "    updated_at: null\n"
        "    verification:\n"
        "      status: pending\n"
        "      scenarios:\n"
        "        []\n"
        "      last_checked_at: null\n"
        "      evidence: null\n"
        "    acceptance:\n"
        "      required: true\n"
        "      owner: \"Дмитрий\"\n"
        "      status: pending\n"
        f"      acceptance_report: {report_rel_path}\n"
        "      accepted_at: null\n"
        "      accepted_by: null\n"
        "      comments: null\n"
        "    depends_on:\n"
        "      []\n"
        "    supersedes:\n"
        "      []\n"
        "    git:\n"
        "      branch: null\n"
        "      commit: null\n"
        "      pull_request: null\n"
        f"    notes: \"{packet_id} accepted by user; protected historical source artifact.\"\n"
        + protected_acceptance_report_text(packet_id, report_rel_path)
    )


def artifact_block_bounds(lines: list[str], report_rel_path: str) -> tuple[int, int] | None:
    path_index = None
    for index, line in enumerate(lines):
        if line.strip() == f"path: {report_rel_path}":
            path_index = index
            break
    if path_index is None:
        return None
    start = path_index
    while start >= 0 and lines[start] != "  -":
        start -= 1
    if start < 0:
        return None
    end = len(lines)
    for index in range(start + 1, len(lines)):
        if lines[index] == "  -":
            end = index
            break
    return start, end


def protection_bounds(block: list[str]) -> tuple[int, int] | None:
    start = None
    for index, line in enumerate(block):
        if line == "    protection:":
            start = index
            break
    if start is None:
        return None
    end = len(block)
    for index in range(start + 1, len(block)):
        if re.match(r"^    [A-Za-z_][A-Za-z0-9_]*:", block[index]):
            end = index
            break
    return start, end


def update_artifact_registry(
    registry_path: Path,
    packet_id: str,
    report_rel_path: str,
) -> tuple[str, str | None]:
    old_text = registry_path.read_text(encoding="utf-8")
    lines = old_text.splitlines()
    bounds = artifact_block_bounds(lines, report_rel_path)
    if bounds is None:
        separator = "" if old_text.endswith("\n") else "\n"
        return (
            old_text + separator + registry_artifact_text(packet_id, report_rel_path) + "\n",
            None,
        )
    start, end = bounds
    block = lines[start:end]
    notes_text = (
        f"    notes: \"{packet_id} accepted by user; protected historical source artifact.\""
    )
    note_replaced = False
    for index, line in enumerate(block):
        if line.startswith("    notes:"):
            block[index] = notes_text
            note_replaced = True
            break
    prot_bounds = protection_bounds(block)
    if prot_bounds is None:
        warning = (
            f"{report_rel_path}: artifact has no protection block; "
            "manual registry protection update is required"
        )
        return old_text, warning
    if not note_replaced:
        block.insert(prot_bounds[0], notes_text)
        prot_bounds = protection_bounds(block)
        if prot_bounds is None:
            return old_text, f"{report_rel_path}: failed to locate protection block"
    prot_start, prot_end = prot_bounds
    protection = protected_acceptance_report_text(packet_id, report_rel_path).splitlines()
    block[prot_start:prot_end] = protection
    new_lines = lines[:start] + block + lines[end:]
    return "\n".join(new_lines) + "\n", None


def validate_consistency(
    packet_id: str,
    statuses: dict[str, str],
    state: dict[str, Any],
) -> None:
    if packet_id not in statuses:
        raise SyncError(f"{packet_id}: packet is missing in execution-packets.xml")
    accepted_packets = state.get("accepted_packets")
    if not isinstance(accepted_packets, list):
        raise SyncError("docs/project-state.yml accepted_packets must be a list")
    in_accepted = packet_id in accepted_packets
    packet_status = statuses[packet_id]
    if packet_status == "accepted" and not in_accepted:
        raise SyncError(
            f"{packet_id}: execution-packets.xml is accepted but "
            "project-state accepted_packets misses it"
        )
    if in_accepted and packet_status != "accepted":
        raise SyncError(
            f"{packet_id}: project-state accepted_packets contains packet but "
            "execution-packets.xml is not accepted"
        )
    active_packet = str(state.get("active_execution_packet") or "").strip()
    active_packet = "" if active_packet in {"", "none", "null", "None"} else active_packet
    if in_accepted and packet_status == "accepted":
        if active_packet == packet_id:
            raise SyncError(f"{packet_id}: accepted packet is still active")
        return
    if state.get("state_mode") == "ready_for_acceptance" and active_packet != packet_id:
        raise SyncError(
            f"{packet_id}: project-state active_execution_packet is "
            f"{active_packet or 'none'}"
        )


def git_changed_paths(root: Path) -> set[str]:
    if not (root / ".git").exists():
        return set()
    result = subprocess.run(
        ["git", "-C", str(root), "status", "--short"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise SyncError("git status --short failed")
    paths: set[str] = set()
    for line in result.stdout.splitlines():
        if not line:
            continue
        raw_path = line[3:].strip()
        if " -> " in raw_path:
            raw_path = raw_path.split(" -> ", 1)[1]
        paths.add(raw_path)
    return paths


def validate_working_tree_for_apply(
    root: Path,
    packet_id: str,
    expected_artifacts: set[str],
    change_paths: set[str],
) -> None:
    changed_paths = git_changed_paths(root)
    if not changed_paths:
        return
    allowed = set(expected_artifacts) | set(SYNC_REL_PATHS) | change_paths
    allowed.add(f"docs/acceptance/{packet_id}.acceptance.md")
    unexpected = sorted(path for path in changed_paths if path not in allowed)
    if unexpected:
        raise SyncError(
            "working tree contains unexpected changes outside sync scope: "
            + ", ".join(unexpected)
        )


def build_changes(root: Path, packet_id: str) -> tuple[list[Change], list[str]]:
    warnings: list[str] = []
    report_path = root / "docs" / "acceptance" / f"{packet_id}.acceptance.md"
    validate_acceptance_decision(packet_id, report_path)

    packets_path = root / "docs" / "grace" / "execution-packets.xml"
    state_path = root / "docs" / "project-state.yml"
    plan_path = root / "docs" / "project-plan.md"
    status_path = root / "docs" / "status-report.md"
    registry_path = root / "docs" / "artifact-registry.yml"

    packets_text = packets_path.read_text(encoding="utf-8")
    statuses = packet_statuses(packets_text)
    state = load_project_state(state_path)
    validate_consistency(packet_id, statuses, state)
    accepted_packets = state.get("accepted_packets", [])
    active_packet = str(state.get("active_execution_packet") or "").strip()
    active_packet = "" if active_packet in {"", "none", "null", "None"} else active_packet
    if statuses.get(packet_id) == "accepted" and packet_id in accepted_packets:
        if not active_packet or active_packet != packet_id:
            return [], []

    next_packet = str(state.get("next_recommended_packet") or "").strip()
    if not next_packet:
        warnings.append("next_recommended_packet is empty; keeping it empty")
    report_rel_path = rel(root, report_path)

    desired_packets = set_packet_status(packets_text, packet_id, "accepted")
    desired_state = update_project_state(state_path, packet_id, next_packet)
    desired_plan = update_current_packet_text(
        plan_path.read_text(encoding="utf-8"),
        packet_id,
        next_packet,
    )
    desired_status = update_current_packet_text(
        status_path.read_text(encoding="utf-8"),
        packet_id,
        next_packet,
    )
    desired_registry, registry_warning = update_artifact_registry(
        registry_path,
        packet_id,
        report_rel_path,
    )
    if registry_warning:
        warnings.append(registry_warning)

    changes = [
        Change(
            packets_path,
            packets_text,
            desired_packets,
            "set execution packet status to accepted",
        ),
        Change(
            state_path,
            state_path.read_text(encoding="utf-8"),
            desired_state,
            "synchronize project-state accepted baseline",
        ),
        Change(
            plan_path,
            plan_path.read_text(encoding="utf-8"),
            desired_plan,
            "synchronize project plan markers",
        ),
        Change(
            status_path,
            status_path.read_text(encoding="utf-8"),
            desired_status,
            "synchronize status report markers",
        ),
        Change(
            registry_path,
            registry_path.read_text(encoding="utf-8"),
            desired_registry,
            "protect accepted acceptance report in artifact registry",
        ),
    ]
    return changes, warnings


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Synchronize project state after a user accepted a packet."
    )
    parser.add_argument("packet_id", help="Execution packet id to synchronize")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true", help="Show planned changes")
    mode.add_argument("--apply", action="store_true", help="Apply planned changes")
    parser.add_argument(
        "--project-root",
        default=str(DEFAULT_PROJECT_ROOT),
        help=argparse.SUPPRESS,
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    try:
        args = parse_args(argv if argv is not None else sys.argv[1:])
    except SystemExit as exc:
        return int(exc.code or 2)
    packet_id = str(args.packet_id).strip()
    if not packet_id.startswith("EP-"):
        print("ERROR: packet_id must start with EP-", file=sys.stderr)
        return 2
    root = Path(args.project_root).resolve()
    try:
        changes, warnings = build_changes(root, packet_id)
        changed = [change for change in changes if change.changed]
        if args.apply:
            packets_text = (root / "docs" / "grace" / "execution-packets.xml").read_text(
                encoding="utf-8"
            )
            expected = packet_expected_artifacts(packets_text, packet_id)
            validate_working_tree_for_apply(
                root,
                packet_id,
                expected,
                {rel(root, change.path) for change in changes},
            )
        mode = "apply" if args.apply else "dry-run"
        print(f"Mode: {mode}")
        for warning in warnings:
            print(f"WARNING: {warning}")
        if not changed:
            print(
                f"Packet {packet_id} is already synchronized as accepted. "
                "No changes required."
            )
            return 0
        print("Planned changes:")
        for change in changed:
            print(f"- {rel(root, change.path)}: {change.reason}")
        print("Affected files:")
        for change in changed:
            print(f"- {rel(root, change.path)}")
        print("Planned diffs:")
        for change in changed:
            print(unified_diff(root, change), end="")
        if not args.apply:
            print("Dry run only; no files were modified.")
            return 0
        for change in changed:
            atomic_write(change.path, change.new_text)
        print("Applied post-acceptance sync:")
        for change in changed:
            print(f"- {rel(root, change.path)}")
        return 0
    except SyncError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    except CliError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
