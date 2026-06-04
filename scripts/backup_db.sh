#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
PROJECT_ROOT=$(CDPATH= cd "$SCRIPT_DIR/.." && pwd)

if [ -f "$PROJECT_ROOT/.env" ]; then
  set -a
  . "$PROJECT_ROOT/.env"
  set +a
fi

POSTGRES_DB=${POSTGRES_DB:-tartip}
POSTGRES_USER=${POSTGRES_USER:-tartip}
BACKUP_DIR=${BACKUP_DIR:-/backups}
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/tartip_${TIMESTAMP}.dump"

cd "$PROJECT_ROOT"

docker compose exec -T postgres pg_dump \
  --format=custom \
  --file="$BACKUP_FILE" \
  --username="$POSTGRES_USER" \
  "$POSTGRES_DB"

printf 'Backup created: %s\n' "$BACKUP_FILE"
