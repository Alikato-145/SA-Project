#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
: "${1:?Usage: RESTORE_DISPOSABLE_DB=1 sh scripts/restore-verification.sh /absolute/backup-directory}"
[ "${RESTORE_DISPOSABLE_DB:-}" = 1 ] || { echo 'Restore is restricted to a disposable verification project.' >&2; exit 1; }
restore_project="${RESTORE_PROJECT:-haris-payroll-restore}"
case "$restore_project" in haris-payroll-restore*) ;; *) echo 'RESTORE_PROJECT must start with haris-payroll-restore.' >&2; exit 1;; esac
restore_input="$1"
restore_stage=""
trap '[ -z "$restore_stage" ] || rm -rf "$restore_stage"' EXIT HUP INT TERM
if [ -f "$restore_input/checkpoint.haris" ]; then
  : "${BACKUP_ENCRYPTION_KEY_FILE:?Encrypted restore requires BACKUP_ENCRYPTION_KEY_FILE}"
  umask 077
  restore_stage="$(mktemp -d "${TMPDIR:-/tmp}/haris-restore.XXXXXXXX")"
  bun scripts/backup-crypto.mjs decrypt "$restore_input/checkpoint.haris" "$restore_stage/checkpoint.tar" "$BACKUP_ENCRYPTION_KEY_FILE"
  if tar -tf "$restore_stage/checkpoint.tar" | rg '(^/|(^|/)\.\.(/|$))'; then echo 'Unsafe checkpoint archive.' >&2; exit 1; fi
  tar -C "$restore_stage" -xf "$restore_stage/checkpoint.tar"
  restore_input="$restore_stage"
fi
[ -f "$restore_input/SHA256SUMS" ] && [ -f "$restore_input/database.dump" ] && [ -f "$restore_input/documents.tar" ]
(cd "$restore_input" && shasum -a 256 -c SHA256SUMS)
# Do not extract archives containing absolute paths or parent traversal.
if tar -tf "$restore_input/documents.tar" | rg '(^/|(^|/)\.\.(/|$))'; then echo 'Unsafe document archive.' >&2; exit 1; fi
export COMPOSE_FILE=compose.yaml
export HTTP_PORT="${RESTORE_HTTP_PORT:-18084}"
export POSTGRES_PORT="${RESTORE_POSTGRES_PORT:-55441}"
restore_env="${RESTORE_ENV_FILE:-.env.example}"
# A restored checkpoint may contain real recipients; never inherit SMTP credentials.
export SMTP_HOST= SMTP_USER= SMTP_PASSWORD= SMTP_FROM=
compose() { docker compose --env-file "$restore_env" -p "$restore_project" "$@"; }
compose stop backend
compose up -d --wait postgres
compose exec -T postgres sh -c 'pg_restore -U "$POSTGRES_USER" -d "$POSTGRES_DB" --clean --if-exists --no-owner --no-acl --exit-on-error' < "$restore_input/database.dump"
compose run --rm --no-deps -T --user 0 --entrypoint sh backend -c 'mkdir -p "$DOCUMENT_STORAGE_PATH"; tar -C "$DOCUMENT_STORAGE_PATH" -xf -; chown -R bun:bun "$DOCUMENT_STORAGE_PATH"' < "$restore_input/documents.tar"
compose up --build -d --wait --wait-timeout 180
printf 'Restored isolated stack: http://localhost:%s (SMTP is not configured).\n' "$HTTP_PORT"
