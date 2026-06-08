#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from reference_utils import load_data


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = [
    PROJECT_ROOT / "docs" / "audit" / "README.md",
    PROJECT_ROOT / "docs" / "audit" / "codex-spec-audit.md",
    PROJECT_ROOT / "docs" / "audit" / "codex-spec-audit.yml",
    PROJECT_ROOT / "docs" / "audit" / "language-policy.md",
    PROJECT_ROOT / "docs" / "audit" / "language-audit-report.md",
    PROJECT_ROOT / "docs" / "audit" / "audit-findings.yml",
    PROJECT_ROOT / "scripts" / "audit_codex_spec.py",
    PROJECT_ROOT / "scripts" / "audit_language_policy.py",
    PROJECT_ROOT / "scripts" / "validate_audit_reports.py",
]
REPORT_FILES = [
    PROJECT_ROOT / "docs" / "audit" / "README.md",
    PROJECT_ROOT / "docs" / "audit" / "codex-spec-audit.md",
    PROJECT_ROOT / "docs" / "audit" / "language-policy.md",
    PROJECT_ROOT / "docs" / "audit" / "language-audit-report.md",
]
FINDINGS_PATH = PROJECT_ROOT / "docs" / "audit" / "audit-findings.yml"
ALLOWED_STATUSES = {
    "open",
    "acknowledged",
    "fixed",
    "accepted_risk",
    "false_positive",
    "blocked",
    "requires_user_approval",
}


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(PROJECT_ROOT))
    except ValueError:
        return str(path)


def as_text(value: Any) -> str:
    return "" if value is None else str(value)


def load_findings() -> list[dict[str, Any]]:
    data = load_data(FINDINGS_PATH)
    findings = data.get("findings", []) if isinstance(data, dict) else []
    if not isinstance(findings, list):
        raise ValueError("docs/audit/audit-findings.yml must contain findings list")
    return [item for item in findings if isinstance(item, dict)]


def validate_required_files() -> list[str]:
    errors: list[str] = []
    for path in REQUIRED_FILES:
        if not path.exists():
            errors.append(f"Missing required audit file: {rel(path)}")
    return errors


def validate_reports_language() -> list[str]:
    errors: list[str] = []
    for path in REPORT_FILES:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        if len(text.strip()) < 80:
            errors.append(f"Audit report is too small: {rel(path)}")
        cyrillic_count = sum("А" <= char <= "я" or char in "Ёё" for char in text)
        if cyrillic_count < 20:
            errors.append(
                f"Audit report does not look Russian enough: {rel(path)}"
            )
    return errors


def validate_findings(findings: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    seen: set[str] = set()
    required_fields = {
        "id",
        "check_id",
        "severity",
        "category",
        "file",
        "issue",
        "recommendation",
        "status",
        "created_at",
        "resolved_by",
        "resolved_at",
        "resolution",
        "preserve_user_resolution",
    }
    for item in findings:
        finding_id = as_text(item.get("id")) or "<missing id>"
        if finding_id in seen:
            errors.append(f"Duplicate finding id: {finding_id}")
        seen.add(finding_id)
        missing = sorted(field for field in required_fields if field not in item)
        if missing:
            errors.append(f"{finding_id}: missing fields: {', '.join(missing)}")
        if item.get("status") not in ALLOWED_STATUSES:
            errors.append(f"{finding_id}: unsupported status={item.get('status')}")
        if item.get("accepted_by") == "Codex":
            errors.append(f"{finding_id}: accepted_by must not be Codex")
        if item.get("preserve_user_resolution") is not True:
            errors.append(f"{finding_id}: preserve_user_resolution must be true")
        if item.get("severity") == "critical" and item.get("status") == "fixed":
            resolved_by = as_text(item.get("resolved_by"))
            resolution = as_text(item.get("resolution"))
            if not resolved_by or resolved_by == "Codex" or not resolution:
                errors.append(
                    f"{finding_id}: critical fixed finding requires non-Codex resolution evidence"
                )
        if item.get("check_id") == "AUD-LANG-001" and item.get("severity") in {
            "critical",
            "high",
        }:
            errors.append(
                f"{finding_id}: AUD-LANG-001 must remain medium/low and must not block make check"
            )
    return errors


def main() -> int:
    errors = validate_required_files()
    if not FINDINGS_PATH.exists():
        errors.append(f"Missing audit findings file: {rel(FINDINGS_PATH)}")
        findings: list[dict[str, Any]] = []
    else:
        try:
            findings = load_findings()
        except ValueError as exc:
            errors.append(str(exc))
            findings = []
    errors.extend(validate_findings(findings))
    errors.extend(validate_reports_language())
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Audit report validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
