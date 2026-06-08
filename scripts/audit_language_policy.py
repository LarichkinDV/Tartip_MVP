#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any

from audit_codex_spec import (
    BLOCKING_STATUSES,
    PROJECT_ROOT,
    finding,
    merge_findings,
)


TODAY = date.today().isoformat()
REPORT_PATH = PROJECT_ROOT / "docs" / "audit" / "language-audit-report.md"
MAX_FINDINGS = 80

READABLE_YAML_KEYS = {
    "title",
    "description",
    "notes",
    "summary",
    "question",
    "recommendation",
    "comments",
}
READABLE_XML_TAGS = {
    "Name",
    "Goal",
    "Item",
    "Expected",
    "Criterion",
}
TECHNICAL_WORDS = {
    "adminer",
    "api",
    "backend",
    "bft",
    "bim",
    "bim5d",
    "calculationunit",
    "changelog",
    "ci",
    "codex",
    "docker",
    "docx",
    "enum",
    "fastapi",
    "frontend",
    "fsnb",
    "gesn",
    "gesnnorm",
    "github",
    "gitignore",
    "grace",
    "json",
    "ksi",
    "llm",
    "make",
    "makefile",
    "markdown",
    "modelelement",
    "node",
    "npm",
    "pdf",
    "postgres",
    "postgresql",
    "pytest",
    "python",
    "react",
    "readme",
    "ruff",
    "sql",
    "sqlalchemy",
    "tartip",
    "typescript",
    "url",
    "vite",
    "workpackage",
    "xml",
    "yaml",
    "yml",
}
ENUM_WORDS = {
    "accepted",
    "active",
    "blocked",
    "candidate",
    "fixed",
    "open",
    "pending",
    "planned",
    "ready",
    "rejected",
    "required",
    "requires",
    "review",
    "status",
    "verified",
}
ENGLISH_WORD_RE = re.compile(r"\b[A-Za-z][A-Za-z'-]*\b")


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(PROJECT_ROOT))
    except ValueError:
        return str(path)


def clean_text(text: str) -> str:
    text = re.sub(r"`[^`]*`", " ", text)
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r"\b[\w.-]+/[\w./-]+\b", " ", text)
    text = re.sub(r"\b[\w.-]+\.(md|yml|yaml|xml|py|ts|tsx|json|toml|txt|sh)\b", " ", text)
    text = re.sub(r"\b[A-Z]{2,}-[0-9A-Z-]+\b", " ", text)
    return text


def unknown_english_words(text: str) -> list[str]:
    words: list[str] = []
    for raw in ENGLISH_WORD_RE.findall(clean_text(text)):
        word = raw.lower().strip("-'")
        if len(word) < 3:
            continue
        if word in TECHNICAL_WORDS or word in ENUM_WORDS:
            continue
        if "_" in word:
            continue
        words.append(raw)
    return words


def should_report(text: str) -> tuple[bool, str]:
    words = unknown_english_words(text)
    has_cyrillic = bool(re.search(r"[А-Яа-яЁё]", text))
    if len(words) >= 6:
        return True, "medium"
    if len(words) >= 4 and not has_cyrillic:
        return True, "medium"
    if len(words) >= 4:
        return True, "low"
    return False, "low"


def language_finding(path: Path, line: int, text: str, severity: str) -> dict[str, Any]:
    digest = hashlib.sha1(f"{rel(path)}:{line}:{text}".encode("utf-8")).hexdigest()[:10]
    return finding(
        f"AUD-LANG-001-{digest}",
        "AUD-LANG-001",
        severity,
        "language_policy",
        rel(path),
        line,
        "Найден вероятный англоязычный пользовательский фрагмент.",
        "Проверить вручную и при необходимости перевести в отдельном follow-up пакете без изменения технических идентификаторов.",
    )


def critical_key_finding(path: Path, line: int, key: str) -> dict[str, Any]:
    digest = hashlib.sha1(f"{rel(path)}:{line}:{key}".encode("utf-8")).hexdigest()[:10]
    return finding(
        f"AUD-LANG-002-{digest}",
        "AUD-LANG-002",
        "critical",
        "language_policy",
        rel(path),
        line,
        f"YAML/XML key выглядит переведенным или содержит кириллицу: {key}.",
        "Восстановить технический ключ без механической русификации.",
    )


def markdown_lines(path: Path) -> list[tuple[int, str]]:
    result: list[tuple[int, str]] = []
    in_code = False
    for index, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        stripped = line.strip()
        if not stripped or stripped.startswith("|---"):
            continue
        result.append((index, stripped))
    return result


def scan_markdown(path: Path) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    for line, text in markdown_lines(path):
        should, severity = should_report(text)
        if should:
            findings.append(language_finding(path, line, text, severity))
    return findings


def scan_yaml(path: Path) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        match = re.match(r"^\s*([^\s:#][^:#]*):\s*(.*)$", line)
        if not match:
            continue
        key = match.group(1).strip()
        value = match.group(2).strip().strip('"')
        if re.search(r"[А-Яа-яЁё]", key):
            findings.append(critical_key_finding(path, line_number, key))
            continue
        if key in READABLE_YAML_KEYS:
            should, severity = should_report(value)
            if should:
                findings.append(language_finding(path, line_number, value, severity))
    return findings


def scan_xml(path: Path) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    tag_pattern = re.compile(r"<([A-Za-z][A-Za-z0-9_-]*)[^>]*>(.*?)</\1>")
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        for tag, value in tag_pattern.findall(line):
            if re.search(r"[А-Яа-яЁё]", tag):
                findings.append(critical_key_finding(path, line_number, tag))
                continue
            if tag in READABLE_XML_TAGS:
                should, severity = should_report(value)
                if should:
                    findings.append(language_finding(path, line_number, value, severity))
    return findings


def iter_scan_paths() -> list[Path]:
    paths: list[Path] = []
    for root_path in [PROJECT_ROOT / "README.md", PROJECT_ROOT / "CHANGELOG.md"]:
        if root_path.exists():
            paths.append(root_path)
    docs_dir = PROJECT_ROOT / "docs"
    if docs_dir.exists():
        for path in sorted(docs_dir.rglob("*")):
            if path.is_file() and path.suffix.lower() in {".md", ".yml", ".yaml", ".xml"}:
                paths.append(path)
    return paths


def scan_language() -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    for path in iter_scan_paths():
        suffix = path.suffix.lower()
        if suffix == ".md":
            findings.extend(scan_markdown(path))
        elif suffix in {".yml", ".yaml"}:
            findings.extend(scan_yaml(path))
        elif suffix == ".xml":
            findings.extend(scan_xml(path))
        if len(findings) >= MAX_FINDINGS:
            break
    return findings[:MAX_FINDINGS]


def severity_counts(findings: list[dict[str, Any]]) -> dict[str, int]:
    return {
        severity: sum(item.get("severity") == severity for item in findings)
        for severity in ["critical", "high", "medium", "low"]
    }


def active_language_findings(findings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        item
        for item in findings
        if str(item.get("check_id", "")).startswith("AUD-LANG-")
        and item.get("status") in BLOCKING_STATUSES
    ]


def write_report(findings: list[dict[str, Any]]) -> None:
    language = active_language_findings(findings)
    counts = severity_counts(language)
    lines = [
        "# Language Audit Report",
        "",
        f"Дата обновления: {TODAY}",
        "",
        "## 1. Что проверяется",
        "",
        "- Markdown-файлы в `docs/`, `README.md` и `CHANGELOG.md`.",
        "- Человекочитаемые поля YAML/XML: `title`, `description`, `notes`, `summary`, `question`, `recommendation`, `comments`, а также основные XML-теги GRACE.",
        "",
        "## 2. Что не проверяется",
        "",
        "- Кодовые блоки.",
        "- Inline code.",
        "- URL, пути файлов, команды, enum-статусы и технические идентификаторы.",
        "",
        "## 3. Допустимые англоязычные исключения",
        "",
        "- Имена файлов, директорий, классов, функций, переменных, API endpoints и библиотек.",
        "- `YAML`, `XML`, `JSON` keys и enum values.",
        "- Термины вроде `FastAPI`, `React`, `Vite`, `pytest`, `Docker`, `Codex`, `GRACE`.",
        "",
        "## 4. Найденные англоязычные пользовательские фрагменты",
        "",
        "| ID | Severity | File | Line | Issue |",
        "|---|---|---|---:|---|",
    ]
    if language:
        for item in language:
            lines.append(
                f"| {item.get('id')} | {item.get('severity')} | {item.get('file')} | {item.get('line') or '-'} | {item.get('issue')} |"
            )
    else:
        lines.append("| - | - | - | - | - |")
    lines.extend(
        [
            "",
            "## 5. Рекомендации",
            "",
            "- Переводить пользовательский текст отдельными follow-up пакетами.",
            "- Не переводить технические идентификаторы и ключи структурированных файлов.",
            "- Сохранять пользовательские статусы findings.",
            "",
            "## 6. Открытые language findings",
            "",
            f"- critical: {counts['critical']}",
            f"- high: {counts['high']}",
            f"- medium: {counts['medium']}",
            f"- low: {counts['low']}",
            "",
            "## 7. Что не переводилось автоматически",
            "",
            "- Existing README, CHANGELOG, dashboards, GRACE и dissertation документы не русифицировались массово.",
            "- Скрипт только создает findings и рекомендации.",
            "",
            "## 8. Почему технические идентификаторы не переводятся",
            "",
            "Технические идентификаторы являются частью контрактов, путей, API, схем, enum-статусов и кода. Их механический перевод ломает совместимость и проверяемость проекта.",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    generated = scan_language()
    findings = merge_findings(generated)
    write_report(findings)
    critical = [
        item
        for item in active_language_findings(findings)
        if item.get("severity") == "critical"
    ]
    print(f"Language audit complete: {len(generated)} generated findings.")
    if critical:
        for item in critical:
            print(f"CRITICAL: {item.get('id')}: {item.get('issue')}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
