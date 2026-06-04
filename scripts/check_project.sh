#!/bin/sh
set -eu

cd "$(CDPATH= cd "$(dirname "$0")/.." && pwd)"

if git ls-files --error-unmatch .env >/dev/null 2>&1; then
  printf 'ERROR: .env is tracked by Git. Remove it from the index before committing.\n' >&2
  exit 1
fi

tracked_dumps=$(
  git ls-files \
    | grep -E '(^|/)(backups?|dumps?|exports?)/.*\.(sql|dump|backup|bak)$|(^|/).*(dump|backup).*\.(sql|dump|backup|bak)$' \
    | grep -v -E '\.(age|enc|gpg)$' || true
)

if [ "$tracked_dumps" != "" ]; then
  printf 'ERROR: unencrypted SQL dump-like files are tracked by Git:\n%s\n' "$tracked_dumps" >&2
  exit 1
fi

printf 'Project safety checks passed.\n'
