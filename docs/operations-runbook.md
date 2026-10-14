# Haris Payroll — operator runbook

Updated 14 October 2026. Scope ends at locked payroll, adjustments, PDF and CSV.
A CSV download is not a payment or a social-security submission.

## Verification without touching existing development data

Requirements: Docker Compose, Bun, Node.js and Playwright Chromium/WebKit (`cd frontend && bun x playwright install chromium webkit`).
Run `sh scripts/verify.sh` from the root. It uses project `haris-payroll-verify`,
HTTP 18083, PostgreSQL 55440, and a Mailpit inbox at http://localhost:18025.
Database and document volumes are separate from development. Demo credentials
are for these disposable localhost stacks only. Do not seed production.

The fixture runs twice to check idempotence. Backend tests run one process per
file so a file closing its pool does not break another file. All database gates
are enabled; a skipped database test fails this check. Browser tests create
fresh synthetic organization data and assert payroll totals, permissions,
PDF bytes, SMTP acceptance, reports and downloads. Mailpit acceptance does not
prove external inbox delivery. Reports/screenshots are under frontend/playwright-report.

After the root verification, run the WebKit payroll/mobile checks separately:

```sh
cd frontend
E2E_BASE_URL=http://localhost:18083 PLAYWRIGHT_HTML_OUTPUT_DIR=playwright-report-webkit \
bun run test:e2e --browser=webkit --output=test-results-webkit --grep 'fresh organization|mobile keyboard|organization duplicate'
```

The GitHub workflow runs on push, pull requests and manual dispatch. Private
submodules require a `SUBMODULES_TOKEN` repository secret with read access to both
submodule repositories; the default GitHub token only covers its own repository.
The workflow stores failure screenshots/traces and separate WebKit artifacts.

## Fresh production deployment

1. Clone root with recursive submodules at the approved release revisions.
2. Supply `.env.production` from `.env.production.example`: unique database/JWT
   secrets, exact HTTPS origin, bank keyring and SMTP settings. Keep the keyring
   in a separate protected secret store; backups alone cannot decrypt accounts.
3. Put HTTPS termination in front of the gateway. Production cookies are Secure.
4. Run `docker compose --env-file .env.production -f compose.production.yaml up --build -d --wait`.
   Production startup applies the existing reviewed SQL through `db:migrate:production` (Drizzle ORM migrator), so development migration CLI packages are not in the runtime image. Do not run db:push or regenerate schema.
5. Verify `/api/health/ready` through the gateway or `/health/ready` inside backend,
   login/logout, own-only access, a synthetic file, and a designated SMTP test
   recipient before inviting users. Create a private password file (chmod 600) in a protected location and run
   `INITIAL_OWNER_USERNAME=<name> INITIAL_OWNER_PASSWORD_FILE=<path> bun run scripts/bootstrap-owner.ts`
   inside the backend with that file mounted read-only. This creates the canonical
   role catalog and first Owner in one audited transaction only when no accounts
   exist. It never prints the password and cannot be used to elevate an existing
   database. Delete the temporary password file after secure delivery. Never seed
   demo accounts in production.
6. Record exact root/backend/frontend commits, operator, date and acceptance.
   Publish submodules first, then the root revision containing both exact pointers.
   A source push is not production deployment or human UAT acceptance.

`/health/live` checks the process; `/health/ready` checks PostgreSQL and returns
503 without a connection string on failure. Gateway `/healthz` checks Nginx only.
Nginx resolves Docker upstream addresses again after container replacement.
Login requests are limited per client IP to 10/minute with a burst of 20; excess
requests return HTTP 429 and the stable RATE_LIMITED error. Users sharing an IP
share this allowance. Keep this limit enabled during release checks.
Backend logs emit JSON with request ID, route pattern, status and duration;
request bodies, query strings, passwords, tokens and bank numbers are omitted.
Use `docker compose ... logs --tail 100 backend` and correlate request IDs with
Audit. Set alerts in the deployment provider for unhealthy containers, repeated
5xx, database/disk capacity, failed SMTP attempts and pending attempts.
Provider monitoring/retention is still awaiting actual hosting settings.

## Backup and restore

`sh scripts/backup.sh /absolute/new-backup-directory` stops backend writes,
captures a PostgreSQL custom dump and immutable documents, writes SHA256 sums,
then starts backend again even if backup fails. The short write outage is
intentional so DB/file pointers have a consistent checkpoint. Files are private
(umask 077). Set BACKUP_ENCRYPTION_KEY_FILE to a mode-600 file containing 32 random
bytes encoded as 64 hex characters. The script streams the checkpoint through
AES-256-GCM into checkpoint.haris and removes its staging plaintext after success.
An authenticated restore publishes plaintext only after the authentication tag
passes; wrong keys and tampering are rejected. Keep the key off-host separately
from backups. If an interrupted backup leaves private staging files, remove them
after inspecting the failure. Plaintext testing requires explicit
BACKUP_ALLOW_PLAINTEXT=1. Copy the encrypted checkpoint off-host. Never commit backups.
Agree retention, encryption provider, RPO and RTO with the data owner before
scheduling production backups; these settings have not been invented here.
Suggested acceptance targets: daily encrypted backups, a backup before every
upgrade, and a monthly restore rehearsal; owner approval is still required.

For the disposable fixture:

```sh
BACKUP_COMPOSE_FILES=compose.yaml:compose.verify.yaml \
BACKUP_PROJECT=haris-payroll-verify BACKUP_ENV_FILE=.env.example \
BACKUP_ENCRYPTION_KEY_FILE=/absolute/private-backup-key \
HTTP_PORT=18083 POSTGRES_PORT=55440 \
sh scripts/backup.sh /private/tmp/haris-payroll-backup-new
BACKUP_ENCRYPTION_KEY_FILE=/absolute/private-backup-key \
RESTORE_DISPOSABLE_DB=1 sh scripts/restore-verification.sh /private/tmp/haris-payroll-backup-new
```

Restore is restricted to project names starting `haris-payroll-restore`. It
verifies archive checksums/traversal before restoring at HTTP 18084/PG 55441.
It does not reset development or production. Set RESTORE_ENV_FILE to a protected
verification env containing the original bank keyring for a real backup.
Restore must not send real emails; leave SMTP unset. After restore run:

```sh
docker compose --env-file .env.example -p haris-payroll-restore -f compose.yaml \
  exec -T backend bun run scripts/verify-documents.ts
```

This verifies SHA256 for every stored document, decryptability of bank records
without printing bank numbers, and history/record counts. Legacy `.json` payslip
metadata is reported separately; an authorized admin can open/generate that
record once to upgrade it to an audited PDF. Missing/tampered PDF files are
errors, not silently regenerated evidence. Review locked totals and own-only
PDF download in the restored browser too.

For an upgrade failure, keep the previous images/revisions and backup. Restore
into an isolated database first, validate the checkpoint, then choose approved
roll-forward or outage recovery. Do not reverse migrations against historical
payroll without the schema owner's review. No schema migration was added here.

## SMTP and document failures

Configure SMTP_HOST, SMTP_PORT, SMTP_SECURE, SMTP_USER, SMTP_PASSWORD and SMTP_FROM.
The example env files deliberately contain mock `smtp.example.invalid` credentials
at the user's request. They cannot deliver external email. Replace them when the
provider is ready; startup remains available and failed delivery attempts are logged.
`compose.verify.yaml` overrides host/port/from and clears mock authentication for
Mailpit. Its inbox proves local SMTP delivery, not an external mailbox.
Production requires STARTTLS or immediate TLS (465). Do not disable certificate
verification. Every attempt has its own pending/sent/failed log; sent means SMTP
accepted the message, not that the recipient read it. Retrying the same request
ID reuses the recorded terminal attempt. A new explicit retry creates a new log.

A pending attempt after a process crash has an uncertain external outcome.
Check the provider using message ID `payslip-attempt-<attempt-id>@haris-payroll.local`
before resolving it; do not blindly resend. An HR/owner can resolve an attempt pending longer than 10 minutes from the
Payslips delivery history after recording the provider result, reference and
reason. This finalizes the existing attempt without sending another email.
Preserve the audit trail; terminal attempts cannot be edited.

Documents live in the named backend document volume, with immutable keys and
SHA256 validation. Do not delete that volume during upgrades (`down -v` destroys
it). Audit orphan files before cleanup; there is no automatic deletion policy.
The document integrity command deliberately avoids printing personal content.
