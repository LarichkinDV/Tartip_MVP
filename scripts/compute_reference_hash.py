#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from reference_utils import canonical_payload_hash, load_data


def load_payload(path_arg: str) -> object:
    if path_arg == "-":
        return json.loads(sys.stdin.read())
    return load_data(Path(path_arg))


def main() -> int:
    parser = argparse.ArgumentParser(description="Compute a canonical sha256 hash for reference payloads.")
    parser.add_argument("path", help="JSON/YAML payload path, or '-' to read JSON from stdin.")
    args = parser.parse_args()

    payload = load_payload(args.path)
    print(canonical_payload_hash(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
