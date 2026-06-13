#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DISCLAIMER = (
    "Настоящий документ является внутренней проектной policy note. Он не является "
    "юридическим заключением, договором, пользовательским соглашением, политикой "
    "обработки персональных данных или согласием Заказчика. Документ не применяется "
    "во внешней договорной работе без отдельной юридической проверки и утверждения."
)
LEGAL_DIR = Path("docs/legal")
NOTE_PATHS = [
    LEGAL_DIR / "ip-and-deliverables-policy-note.md",
    LEGAL_DIR / "customer-data-boundary-policy-note.md",
    LEGAL_DIR / "data-contribution-policy-note.md",
    LEGAL_DIR / "anonymization-and-aggregation-policy-note.md",
    LEGAL_DIR / "code-license-and-data-use-boundary-note.md",
]
FORBIDDEN_PHRASES = [
    "настоящая политика регулирует",
    "пользователь соглашается",
    "Заказчик предоставляет право",
    "данные могут использоваться",
    "достаточно для договорной работы",
    "юридически значимый порядок",
]
DEFAULT_OFF_FLAGS = [
    "telemetry_enabled=false",
    "dataset_contribution_enabled=false",
    "external_upload_enabled=false",
    "ai_training_allowed=false",
    "commercial_use_allowed=false",
]
MANDATORY_DATA_CONTRIBUTION_TEXT = (
    "Данные Заказчика по умолчанию остаются в локальном контуре Заказчика. "
    "Передача данных за пределы локального контура отключена по умолчанию. "
    "Лицензия на программный код, модульная архитектура или возможность последующего "
    "тиражирования не означают согласие Заказчика на передачу, обезличивание, "
    "агрегацию, обучение моделей или коммерческое использование данных. Любая "
    "передача обезличенных или агрегированных данных возможна только при наличии "
    "отдельного согласия, договора или иного применимого правового основания."
)
REIDENTIFICATION_WARNING = (
    "Даже обезличенная единичная закупочная запись может быть небезопасной, если "
    "сохраняет точную дату, город, материал, цену и уникальный контекст сделки."
)
OBVIOUS_INN_PATTERN = re.compile(
    r"\b(?:ИНН|inn)\s*[:№#-]?\s*\d{10}(?:\d{2})?\b",
    flags=re.IGNORECASE,
)


def rel(root: Path, path: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def without_code_blocks(text: str) -> str:
    return re.sub(r"```.*?```", "", text, flags=re.DOTALL)


def contains_casefold(text: str, needle: str) -> bool:
    return needle.casefold() in text.casefold()


def validate_project(root: Path) -> list[str]:
    errors: list[str] = []
    note_texts: dict[Path, str] = {}

    readme_path = root / LEGAL_DIR / "README.md"
    if not readme_path.exists():
        errors.append(f"missing required file: {rel(root, readme_path)}")

    for relative_path in NOTE_PATHS:
        path = root / relative_path
        if not path.exists():
            errors.append(f"missing required file: {relative_path}")
            continue
        text = path.read_text(encoding="utf-8")
        note_texts[relative_path] = text
        if not text.startswith(DISCLAIMER):
            errors.append(f"{relative_path}: missing required disclaimer at file start")
        if "требует юридической проверки" not in text:
            errors.append(f"{relative_path}: missing legal review warning")

        visible_text = without_code_blocks(text)
        for phrase in FORBIDDEN_PHRASES:
            if contains_casefold(visible_text, phrase):
                errors.append(f"{relative_path}: forbidden legal-confidence phrase: {phrase}")
        if OBVIOUS_INN_PATTERN.search(visible_text):
            errors.append(f"{relative_path}: obvious INN-like value must not be present")

    code_note = note_texts.get(LEGAL_DIR / "code-license-and-data-use-boundary-note.md", "")
    for flag in DEFAULT_OFF_FLAGS:
        if flag not in code_note:
            errors.append(
                f"{LEGAL_DIR / 'code-license-and-data-use-boundary-note.md'}: missing default-off flag: {flag}"
            )

    customer_boundary = note_texts.get(
        LEGAL_DIR / "customer-data-boundary-policy-note.md", ""
    )
    if "Передача данных за пределы локального контура отключена по умолчанию" not in customer_boundary:
        errors.append(
            f"{LEGAL_DIR / 'customer-data-boundary-policy-note.md'}: missing default-off external transfer boundary"
        )
    if "не означает автоматический сбор" not in customer_boundary:
        errors.append(
            f"{LEGAL_DIR / 'customer-data-boundary-policy-note.md'}: missing ban on automatic data collection or transfer"
        )

    contribution_note = note_texts.get(LEGAL_DIR / "data-contribution-policy-note.md", "")
    if MANDATORY_DATA_CONTRIBUTION_TEXT not in contribution_note:
        errors.append(
            f"{LEGAL_DIR / 'data-contribution-policy-note.md'}: missing mandatory data contribution boundary wording"
        )

    anonymization_note = note_texts.get(
        LEGAL_DIR / "anonymization-and-aggregation-policy-note.md", ""
    )
    if REIDENTIFICATION_WARNING not in anonymization_note:
        errors.append(
            f"{LEGAL_DIR / 'anonymization-and-aggregation-policy-note.md'}: missing re-identification warning"
        )
    if "re-identification risk check" not in anonymization_note:
        errors.append(
            f"{LEGAL_DIR / 'anonymization-and-aggregation-policy-note.md'}: missing re-identification risk check"
        )

    return errors


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate internal legal/data boundary policy notes."
    )
    parser.add_argument(
        "--project-root",
        default=str(PROJECT_ROOT),
        help=argparse.SUPPRESS,
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])
    root = Path(args.project_root).resolve()
    errors = validate_project(root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Legal data boundary notes validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

