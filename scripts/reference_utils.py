from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


SAFE_STRING_CHARS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-./")


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if value in {"", "null", "None", "~"}:
        return None
    if value == "[]":
        return []
    if value == "{}":
        return {}
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    try:
        return int(value)
    except ValueError:
        return value


def _strip_comment(line: str) -> str:
    in_single = False
    in_double = False
    for index, char in enumerate(line):
        if char == "'" and not in_double:
            in_single = not in_single
        elif char == '"' and not in_single:
            in_double = not in_double
        elif char == "#" and not in_single and not in_double:
            return line[:index]
    return line


def _tokenize_yaml(text: str) -> list[tuple[int, str]]:
    tokens: list[tuple[int, str]] = []
    for raw_line in text.splitlines():
        line = _strip_comment(raw_line).rstrip()
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip(" "))
        tokens.append((indent, line.strip()))
    return tokens


def _split_key_value(content: str) -> tuple[str, str] | None:
    if ":" not in content:
        return None
    key, value = content.split(":", 1)
    return key.strip(), value.strip()


def _parse_yaml_block(tokens: list[tuple[int, str]], index: int, indent: int) -> tuple[Any, int]:
    if index >= len(tokens):
        return None, index
    current_indent, content = tokens[index]
    if current_indent < indent:
        return None, index
    if content == "-" or content.startswith("- "):
        return _parse_yaml_list(tokens, index, current_indent)
    return _parse_yaml_map(tokens, index, current_indent)


def _parse_yaml_map(tokens: list[tuple[int, str]], index: int, indent: int) -> tuple[dict[str, Any], int]:
    result: dict[str, Any] = {}
    while index < len(tokens):
        current_indent, content = tokens[index]
        if current_indent < indent or content == "-" or content.startswith("- "):
            break
        if current_indent > indent:
            index += 1
            continue
        split = _split_key_value(content)
        if split is None:
            index += 1
            continue
        key, raw_value = split
        index += 1
        if raw_value:
            result[key] = parse_scalar(raw_value)
        elif index < len(tokens) and tokens[index][0] > current_indent:
            result[key], index = _parse_yaml_block(tokens, index, tokens[index][0])
        else:
            result[key] = None
    return result, index


def _parse_yaml_list(tokens: list[tuple[int, str]], index: int, indent: int) -> tuple[list[Any], int]:
    result: list[Any] = []
    while index < len(tokens):
        current_indent, content = tokens[index]
        if current_indent != indent or not (content == "-" or content.startswith("- ")):
            break
        item_content = "" if content == "-" else content[2:].strip()
        index += 1
        if not item_content:
            if index < len(tokens) and tokens[index][0] > current_indent:
                item, index = _parse_yaml_block(tokens, index, tokens[index][0])
            else:
                item = None
            result.append(item)
            continue
        split = _split_key_value(item_content)
        if split is None:
            result.append(parse_scalar(item_content))
            continue
        key, raw_value = split
        item = {key: parse_scalar(raw_value) if raw_value else None}
        if index < len(tokens) and tokens[index][0] > current_indent:
            nested, index = _parse_yaml_map(tokens, index, tokens[index][0])
            item.update(nested)
        result.append(item)
    return result, index


def load_yaml_subset(path: Path) -> Any:
    tokens = _tokenize_yaml(path.read_text(encoding="utf-8"))
    if not tokens:
        return {}
    value, _ = _parse_yaml_block(tokens, 0, tokens[0][0])
    return value


def load_data(path: str | Path) -> Any:
    data_path = Path(path)
    text = data_path.read_text(encoding="utf-8")
    if data_path.suffix.lower() == ".json":
        return json.loads(text)
    return load_yaml_subset(data_path)


def normalize_payload(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): normalize_payload(value[key]) for key in sorted(value)}
    if isinstance(value, list):
        return [normalize_payload(item) for item in value]
    return value


def canonical_payload_hash(value: Any) -> str:
    canonical = json.dumps(
        normalize_payload(value),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def records_by_natural_key(data: Any) -> dict[str, dict[str, Any]]:
    records = data.get("records", data) if isinstance(data, dict) else data
    if not isinstance(records, list):
        raise ValueError("Reference release must be a list or contain a records list.")
    result: dict[str, dict[str, Any]] = {}
    for record in records:
        if not isinstance(record, dict):
            raise ValueError("Each reference record must be an object.")
        natural_key = record.get("natural_key") or record.get("id")
        if not natural_key:
            raise ValueError("Each reference record must have natural_key or id.")
        result[str(natural_key)] = record
    return result


def record_payload(record: dict[str, Any]) -> Any:
    if "payload" in record:
        return record["payload"]
    return {key: value for key, value in record.items() if key not in {"id", "natural_key"}}


def format_yaml_scalar(value: Any) -> str:
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, (int, float)):
        return str(value)
    text = str(value)
    if text and all(char in SAFE_STRING_CHARS for char in text):
        return text
    return json.dumps(text, ensure_ascii=False)


def dump_yaml(value: Any, indent: int = 0) -> str:
    spaces = " " * indent
    lines: list[str] = []
    if isinstance(value, dict):
        for key, item in value.items():
            if isinstance(item, (dict, list)):
                lines.append(f"{spaces}{key}:")
                lines.append(dump_yaml(item, indent + 2))
            else:
                lines.append(f"{spaces}{key}: {format_yaml_scalar(item)}")
    elif isinstance(value, list):
        if not value:
            return f"{spaces}[]"
        for item in value:
            if isinstance(item, dict):
                lines.append(f"{spaces}-")
                lines.append(dump_yaml(item, indent + 2))
            elif isinstance(item, list):
                lines.append(f"{spaces}-")
                lines.append(dump_yaml(item, indent + 2))
            else:
                lines.append(f"{spaces}- {format_yaml_scalar(item)}")
    else:
        lines.append(f"{spaces}{format_yaml_scalar(value)}")
    return "\n".join(lines)


def write_yaml(path: str | Path, value: Any) -> None:
    Path(path).write_text(dump_yaml(value) + "\n", encoding="utf-8")
