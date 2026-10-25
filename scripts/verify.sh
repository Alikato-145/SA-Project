#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
export HTTP_PORT="${VERIFY_HTTP_PORT:-18083}"
export POSTGRES_PORT="${VERIFY_POSTGRES_PORT:-55440}"
compose() { docker compose --env-file .env.example -p haris-payroll-verify -f compose.yaml -f compose.verify.yaml "$@"; }

compose config --quiet
bun test scripts/backup-crypto.test.ts
compose up --build -d --wait --wait-timeout 180
compose exec -T -e RELEASE_DISPOSABLE_DB=1 backend sh -ec '
  export TEST_DATABASE_URL="$DATABASE_URL"
  bun run db:seed:release
  bun run db:seed:release
  bun run typecheck
  bun run test:db
'
compose exec -T frontend sh -ec '
  bun test
  bun run lint
  bun run node_modules/typescript/bin/tsc --noEmit
'
printf 'Verification stack is ready at http://localhost:%s; it uses its own database and volumes.\n' "$HTTP_PORT"
if [ "${VERIFY_BROWSER:-1}" = 1 ]; then
  command -v bun >/dev/null || { echo 'Install Bun and Playwright Chromium to run browser verification.' >&2; exit 1; }
  sh scripts/full-uat.sh
fi
