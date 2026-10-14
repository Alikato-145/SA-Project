#!/bin/sh
set -eu
umask 077
cd "$(dirname "$0")/.."
: "${1:?Usage: sh scripts/backup.sh /absolute/new-backup-directory}"
case "$1" in /*) ;; *) echo 'Use an absolute backup path.' >&2; exit 1;; esac
[ ! -e "$1" ] || { echo 'Backup directory already exists.' >&2; exit 1; }
export COMPOSE_FILE="${BACKUP_COMPOSE_FILES:-compose.production.yaml}"
backup_project="${BACKUP_PROJECT:-haris-payroll-production}"
backup_env="${BACKUP_ENV_FILE:-.env.production}"
backup_key="${BACKUP_ENCRYPTION_KEY_FILE:-}"
if [ -n "$backup_key" ]; then
  command -v bun >/dev/null
  [ -f "$backup_key" ] || { echo 'Backup encryption key file is missing.' >&2; exit 1; }
elif [ "${BACKUP_ALLOW_PLAINTEXT:-}" != 1 ]; then
  echo 'Set BACKUP_ENCRYPTION_KEY_FILE; plaintext requires explicit BACKUP_ALLOW_PLAINTEXT=1.' >&2; exit 1
fi
compose() { docker compose --env-file "$backup_env" -p "$backup_project" "$@"; }
mkdir -m 700 "$1"
backup_output="$1"
# Stop application writes so database metadata and immutable files form one checkpoint.
compose stop backend
trap 'compose start backend >/dev/null' EXIT HUP INT TERM
compose exec -T postgres sh -c 'pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" --format=custom --no-owner --no-acl' > "$backup_output/database.dump"
compose run --rm --no-deps -T --user 0 --entrypoint sh backend -c 'tar -C "$DOCUMENT_STORAGE_PATH" -cf - .' > "$backup_output/documents.tar"
(cd "$backup_output" && shasum -a 256 database.dump documents.tar > SHA256SUMS)
printf 'project=%s\ncreated_utc=%s\n' "$backup_project" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" > "$backup_output/manifest.txt"
if [ -n "$backup_key" ]; then
  tar -C "$backup_output" -cf "$backup_output/checkpoint.tar" database.dump documents.tar SHA256SUMS manifest.txt
  bun scripts/backup-crypto.mjs encrypt "$backup_output/checkpoint.tar" "$backup_output/checkpoint.haris" "$backup_key"
  rm "$backup_output/checkpoint.tar" "$backup_output/database.dump" "$backup_output/documents.tar" "$backup_output/SHA256SUMS" "$backup_output/manifest.txt"
fi
printf 'Backup complete: %s (store off-host; keep encryption keys separately).\n' "$backup_output"
