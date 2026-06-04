#!/bin/sh
set -eu

if [ "${1:-}" = "" ]; then
  printf 'Usage: BACKUP_FILE=backups/tartip_YYYYMMDD_HHMMSS.dump make restore\n' >&2
  exit 2
fi

if [ "${CONFIRM_RESTORE:-}" != "1" ]; then
  printf 'Refusing to restore without CONFIRM_RESTORE=1.\n' >&2
  exit 2
fi

SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
PROJECT_ROOT=$(CDPATH= cd "$SCRIPT_DIR/.." && pwd)

if [ -f "$PROJECT_ROOT/.env" ]; then
  set -a
  . "$PROJECT_ROOT/.env"
  set +a
fi

POSTGRES_DB=${POSTGRES_DB:-tartip}
POSTGRES_USER=${POSTGRES_USER:-tartip}
BACKUP_FILE=$1

cd "$PROJECT_ROOT"

if [ ! -f "$BACKUP_FILE" ]; then
  printf 'Backup file not found: %s\n' "$BACKUP_FILE" >&2
  exit 1
fi

docker compose cp "$BACKUP_FILE" postgres:/tmp/tartip_restore.dump
docker compose exec -T postgres pg_restore \
  --clean \
  --if-exists \
  --username="$POSTGRES_USER" \
  --dbname="$POSTGRES_DB" \
  /tmp/tartip_restore.dump

printf 'Database restored from: %s\n' "$BACKUP_FILE"
