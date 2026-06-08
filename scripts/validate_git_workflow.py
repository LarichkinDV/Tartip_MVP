#!/usr/bin/env python3
from __future__ import annotations

import argparse
import fnmatch
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PACKETS_PATH = PROJECT_ROOT / "docs" / "grace" / "execution-packets.xml"
ACCEPTANCE_DIR = PROJECT_ROOT / "docs" / "acceptance"
BRANCH_RE = re.compile(r"^ep-\d{3}-[a-z0-9][a-z0-9-]*$")
FORBIDDEN_PATTERNS = [
    ".env",
    ".env.*",
    ".venv/*",
    "node_modules/*",
    "*.dump",
    "*.sql",
    "*.backup",
    "backups/*",
    "thesis/source/*.docx",
    "thesis/versions/*.docx",
    "thesis/exports/pdf/*.pdf",
]


@dataclass
class GitStatusEntry:
    index_status: str
    worktree_status: str
    path: str


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(PROJECT_ROOT))
    except ValueError:
        return str(path)


def run_git(args: list[str]) -> tuple[int, str, str]:
    result = subprocess.run(
        ["git", *args],
        cwd=PROJECT_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def current_branch() -> tuple[str, list[str]]:
    code, stdout, stderr = run_git(["branch", "--show-current"])
    if code != 0:
        return "", [f"Не удалось определить текущую ветку: {stderr or stdout}"]
    if not stdout:
        return "", ["Текущая ветка не определена; возможно detached HEAD."]
    return stdout, []


def parse_status_line(line: str) -> GitStatusEntry | None:
    if not line:
        return None
    if line.startswith("?? "):
        return GitStatusEntry("?", "?", line[3:])
    index_status = line[0]
    worktree_status = line[1] if len(line) > 1 else " "
    path = line[3:] if len(line) > 3 else ""
    if " -> " in path:
        path = path.split(" -> ", 1)[1]
    return GitStatusEntry(index_status, worktree_status, path)


def git_status_entries() -> tuple[list[GitStatusEntry], list[str]]:
    code, stdout, stderr = run_git(["status", "--porcelain"])
    if code != 0:
        return [], [f"Не удалось прочитать git status: {stderr or stdout}"]
    entries = [
        entry
        for entry in (parse_status_line(line) for line in stdout.splitlines())
        if entry is not None
    ]
    return entries, []


def packet_id_from_project() -> str:
    project_plan = PROJECT_ROOT / "docs" / "project-plan.md"
    if project_plan.exists():
        text = project_plan.read_text(encoding="utf-8")
        match = re.search(r"`(EP-\d{3}-[A-Z0-9-]+)`", text)
        if match:
            return match.group(1)
    if PACKETS_PATH.exists():
        root = ET.parse(PACKETS_PATH).getroot()
        ready = [
            packet.attrib.get("id", "")
            for packet in root.findall("Packet")
            if packet.attrib.get("status") == "ready_for_acceptance"
        ]
        if ready:
            return sorted(ready)[-1]
    return ""


def packet_number(packet_id: str) -> str:
    match = re.match(r"EP-(\d{3})-", packet_id)
    return match.group(1) if match else ""


def packet_status(packet_id: str) -> str:
    if not PACKETS_PATH.exists() or not packet_id:
        return ""
    root = ET.parse(PACKETS_PATH).getroot()
    for packet in root.findall("Packet"):
        if packet.attrib.get("id") == packet_id:
            return packet.attrib.get("status", "")
    return ""


def parse_acceptance_report(packet_id: str) -> dict[str, str]:
    values = {
        "acceptance_decision": "pending",
        "accepted_by": "",
        "accepted_at": "",
        "comments": "",
    }
    report = ACCEPTANCE_DIR / f"{packet_id}.acceptance.md"
    if not report.exists():
        return values
    for line in report.read_text(encoding="utf-8").splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        if key in values:
            values[key] = value.strip()
    return values


def is_staged_or_untracked(entry: GitStatusEntry) -> bool:
    return entry.index_status == "?" or entry.index_status not in {" ", "?"}


def forbidden_path(path: str) -> bool:
    normalized = path.lstrip("./")
    return any(fnmatch.fnmatch(normalized, pattern) for pattern in FORBIDDEN_PATTERNS)


def detect_forbidden_files(entries: list[GitStatusEntry]) -> list[str]:
    return [
        entry.path
        for entry in entries
        if is_staged_or_untracked(entry) and forbidden_path(entry.path)
    ]


def ep_scope(path: str) -> str:
    if path.startswith("docs/audit/") or path.startswith("scripts/audit_"):
        return "EP-009"
    if path == "scripts/validate_audit_reports.py":
        return "EP-009"
    if path == "docs/git-workflow.md" or path == "scripts/validate_git_workflow.py":
        return "EP-011"
    if path.startswith("docs/dissertation/") or path.startswith("thesis/"):
        return "EP-008"
    if path.startswith("docs/verification-dashboard") or path.startswith(
        "scripts/generate_verification_dashboard.py"
    ):
        return "EP-007"
    if path.startswith("docs/monthly/"):
        return "EP-006"
    if path.startswith("docs/acceptance-dashboard") or path.startswith(
        "docs/user-action-dashboard"
    ):
        return "EP-005"
    if path.startswith("docs/acceptance/EP-011"):
        return "EP-011"
    if path.startswith("docs/acceptance/EP-009"):
        return "EP-009"
    if path.startswith("docs/grace/") or path in {
        "AGENTS.md",
        "Makefile",
        "README.md",
        "CHANGELOG.md",
        "docs/artifact-registry.yml",
        "docs/project-plan.md",
        "docs/status-report.md",
        "docs/traceability-matrix.md",
        "docs/decision-log.md",
    }:
        return "governance"
    return "unknown"


def detect_mixed_ep(entries: list[GitStatusEntry]) -> set[str]:
    scopes = {ep_scope(entry.path) for entry in entries}
    return {scope for scope in scopes if scope != "unknown"}


def branch_expected_for_packet(branch: str, packet_id: str) -> bool:
    number = packet_number(packet_id)
    if not number:
        return False
    return branch.startswith(f"ep-{number}-") and bool(BRANCH_RE.match(branch))


def validate(args: argparse.Namespace) -> tuple[list[str], list[str]]:
    warnings: list[str] = []
    errors: list[str] = []

    branch, branch_errors = current_branch()
    errors.extend(branch_errors)
    entries, status_errors = git_status_entries()
    errors.extend(status_errors)

    packet_id = args.packet_id or packet_id_from_project()
    if packet_id and branch and not branch_expected_for_packet(branch, packet_id):
        if branch == "main":
            warnings.append(
                f"Текущая ветка main не соответствует {packet_id}; это допустимо только как documented exception для pre-existing dirty baseline."
            )
        else:
            warnings.append(
                f"Текущая ветка {branch} не соответствует {packet_id}; ожидается ep-{packet_number(packet_id)}-<short-slug>."
            )
    elif branch and not BRANCH_RE.match(branch) and branch != "main":
        warnings.append(
            f"Имя ветки {branch} не соответствует ep-<number>-<short-slug>."
        )

    forbidden = detect_forbidden_files(entries)
    for path in forbidden:
        errors.append(f"Forbidden file is staged or untracked: {path}")

    scopes = detect_mixed_ep(entries)
    if len(scopes) > 1:
        warnings.append(
            "Working tree contains mixed EP scopes: " + ", ".join(sorted(scopes))
        )

    status = packet_status(packet_id)
    acceptance = parse_acceptance_report(packet_id)
    decision = acceptance.get("acceptance_decision", "pending")
    accepted_by = acceptance.get("accepted_by", "")
    if accepted_by == "Codex":
        errors.append(f"{packet_id}: accepted_by must not be Codex")
    if status != "accepted" or decision != "accepted" or not accepted_by:
        warnings.append(
            f"Merge is forbidden for {packet_id}: packet status={status or '-'}, acceptance_decision={decision}, accepted_by={'set' if accepted_by else 'empty'}."
        )

    if not args.check_passed:
        warnings.append(
            "make check result is not documented for this validator run; merge is not ready."
        )

    if args.strict:
        errors.extend(f"Strict warning: {warning}" for warning in warnings)
    return warnings, errors


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--advisory", action="store_true", help="Do not fail on warnings."
    )
    mode.add_argument("--strict", action="store_true", help="Fail on warnings.")
    parser.add_argument("--packet-id", default="", help="Execution packet id.")
    parser.add_argument(
        "--check-passed",
        action="store_true",
        help="Declare that make check passed in this run.",
    )
    args = parser.parse_args(argv)
    if not args.advisory and not args.strict:
        args.advisory = True
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    warnings, errors = validate(args)
    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    if errors:
        return 1
    print("Git workflow validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
