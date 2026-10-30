#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
# This wrapper must finish bootstrap before Playwright loads test modules.
export HTTP_PORT="${HTTP_PORT:-${VERIFY_HTTP_PORT:-18083}}"
export POSTGRES_PORT="${POSTGRES_PORT:-${VERIFY_POSTGRES_PORT:-55440}}"
export VERIFY_MAIL_PORT="${VERIFY_MAIL_PORT:-18025}"
# Let Playwright choose its worker color policy without conflicting caller flags.
unset FORCE_COLOR NO_COLOR
compose() { docker compose --env-file .env.example -p haris-payroll-verify -f compose.yaml -f compose.verify.yaml "$@"; }
run_id="$(date -u +%Y%m%dT%H%M%SZ)-$$"
evidence="$(pwd)/docs/superpowers/reports/full-uat-evidence/$run_id"
container_dir="/tmp/haris-full-uat-$run_id"
mkdir -p "$evidence/fixtures" "$evidence/payslips" "$evidence/reports"
compose exec -T -e RELEASE_DISPOSABLE_DB=1 -e UAT_FIXTURE_DIR="$container_dir" -e PAYSLIP_FIXTURE_DIR="$container_dir/payslips" backend sh -ec '
  export TEST_DATABASE_URL="$DATABASE_URL"
  bun run scripts/full-uat-fixtures.ts
  bun run src/features/payslip/payslip.test-support.ts
' > "$evidence/fixtures.log" 2>&1
compose cp "backend:$container_dir/." "$evidence/fixtures" >> "$evidence/fixtures.log" 2>&1
export UAT_SCOPE_FIXTURE_FILE="$evidence/fixtures/scope.json"
export PAYMENT_FIXTURE_FILE="$evidence/fixtures/payments.json"
export PAYMENT_CATEGORY_FIXTURE_FILE="$evidence/fixtures/payment-categories.json"
export PAYMENT_LIFECYCLE_FIXTURE_FILE="$evidence/fixtures/lifecycle.json"
export PAYABLE_REPORT_FIXTURE_FILE="$evidence/fixtures/reports.json"
export PAYSLIP_FIXTURE_FILE="$evidence/fixtures/payslips/fixture.json"
export PAYABLE_REPORT_EVIDENCE_DIR="$evidence/reports"
export PAYSLIP_EVIDENCE_DIR="$evidence/payslips"
export E2E_EVIDENCE_DIR="$evidence"
export E2E_LOGIN_PACING_FILE="$evidence/last-login"
export PLAYWRIGHT_HTML_OUTPUT_DIR="$evidence/playwright-report"
export E2E_BASE_URL="http://localhost:$HTTP_PORT"
printf '%s\n' "$evidence" > docs/superpowers/reports/full-uat-evidence/latest-run.txt
printf 'Fresh fixtures and evidence: %s\n' "$evidence"
cd frontend
# Preserve the full invocation log, including failures; retries stay disabled.
set +e
bun run test:e2e --output="$evidence/test-results" "$@" > "$evidence/browser.log" 2>&1
result=$?
cat "$evidence/browser.log"
exit "$result"
