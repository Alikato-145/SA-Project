# Completion progress

Updated 14 October 2026. Approved scope is in completion-scope.md; the original
acceptance criteria remain in end-to-end-completion-tasks.md. A source publication
is not production deployment or human UAT sign-off.

## Verification evidence

- Latest candidate: 477 backend pass / 0 skip / 0 fail, 45 frontend pass,
  lint/typecheck and 21 Chromium cases passed through `sh scripts/verify.sh`.
  Exact revisions/results are in release-verification-2026-10-14.md.
- WebKit: the full fresh payroll journey, mobile keyboard/error/logout and organization lifecycle journeys
  passed (3 cases, including organization pagination/archival). This exercises the Safari browser engine, not a user's Safari
  profile or certification on every physical device.
- Browser coverage includes organization create/edit/search, duplicate codes,
  20-row pagination, child-first archival, onboarding, scoped account grants,
  no-role recovery, password change/disable and concurrent employee linkage.
- Role recovery cancels stale auth requests and waits for a hydrated granted-role
  navigation in E2E; this fixes the WebKit Linux CI reload/navigation race.
- Five-role live scope matrix: employee, supervisor, branch manager, HR and owner;
  own/department/branch/all queries and bank authorization across three employees.
- Supervisor UI approves three days with a corrected leave type; four-day decision
  is denied. Manager UI directly approves four days. Quotas and append-only actions
  retain original/corrected types. Evidence is own-only; invalid/oversized files fail.
- Historical September transfer and salary/weekly-holiday change: base earnings
  3700, approved OT 75/400/400, net 4575 with SS=0; old assignments retained.
- Real bank UI add/edit/make-primary/replacement/deactivation and cancelled
  no-primary confirmation passed. Ordinary responses and audit snapshots are masked.
- Loan UI: 100.01 / 3 produces 33.34, 33.34, 33.33. Debt reversal preserves ledger.
- Golden September payroll: earnings 2916.25, deductions 163.34, net 2752.91.
  October: base earnings 2700, SS 135, approved adjustment applied once, net 2901.66;
  both periods lock and September remains unchanged.
- Thai PDF rendered/visually checked; UI/API downloads, file hash, own-only access,
  legacy upgrade/idempotence/conflict and voided/cross-employee guards have checks.
- SMTP adapter is tested with Mailpit. Attempts record actual pending/sent/failed
  outcomes; stale pending resolution requires documented provider evidence and
  cannot resend or edit terminal attempts. External SMTP remains unverified.
- Reports: filters, aggregates, 26-row pagination, dated transfer scope and CSV;
  payroll export uses locked values, blocks missing primary bank, escapes CSV formulas.
- Encrypted checkpoint restored into a separate stack: 45 document hashes and 66
  bank accounts verified; checked historical row counts matched the checkpoint.
  Restored role/persisted-payroll browser checks: 11 pass; restored PDF check: 1 pass,
  same hash/net, storage key hidden and unauthenticated download denied.
- Production rehearsal uses synthetic secrets and localhost TLS; startup, secure
  cookies, CSRF, persistence, restart and database outage recovery were checked.
  Production-only migration runner applies the existing SQL to an empty disposable
  database and runs again: 36 tables, one migration journal row, no schema changes.
- Security fixes remove development packages from the backend production image and
  npm/corepack from the frontend runtime, patch Alpine and update gateway stable.
  Docker Scout is authorized for metadata only; findings are in security-verification-2026-10-14.md.

All data is synthetic and all stacks use separate databases/volumes. Development
records were not reset. Browser fixtures use APIs for bulk setup/operations as well
as actual forms; passing them does not imply every action has been exercised via UI.

## Task status

| Tasks | Current status |
|---|---|
| 001–002 | Scope and deterministic disposable fixtures established |
| 003 | Local full verification and push/PR CI implemented; remote CI result must be recorded separately |
| 004–005 | Root/production bootstrap and organization lifecycle verified; published clean checkout is healthy and five baseline browser cases passed |
| 006–009 | Schedule/holiday/config successors and combined dated readiness implemented and checked |
| 010–015 | Onboarding/account lifecycle/linkage, named scopes/no-role recovery and five-role authorization checked |
| 016–023 | Employment history, bank/documents, weekly holidays, attendance clocks/calendar/corrections and lock guards checked |
| 024–031 | Leave administration/quota/document/approval/history and all OT types/pending edit checked |
| 032–036 | Self-only advance, deterministic eligibility boundaries, exact loan installments and debt ledger checked |
| 037–043 | Month/roster/blockers, daily calculation, persisted records, atomic lock and once-only adjustments checked |
| 044–047 | Immutable PDF, mock/local SMTP, CSV and management reports implemented and checked |
| 048,051,052 | Closed by approved CSV/PDF scope |
| 049–050 | Not applicable: disbursement lifecycle excluded by the user |
| 053–056 | Audit viewer/redaction, role/browser journeys and focused WebKit/mobile recovery checked; physical-device/human UAT remains |
| 057 | Encrypted backup and isolated restore checked; off-host destination/retention/RPO/RTO require infrastructure owner settings |
| 058 | Application runtime hardening/scanning completed; unresolved vendor image findings remain explicitly tracked |
| 059 | Local production TLS/restart/outage rehearsal checked; real provider alerts/settings remain |
| 060 | Guides/evidence and matched Git publication prepared; human five-role acceptance remains unsigned |

## Remaining before real production use

1. Review unresolved vendor OS/image CVEs and choose approved patched images or
   documented risk acceptance. No blanket security exception was granted.
2. Configure the real HTTPS host, protected production secrets, provider monitoring
   and encrypted off-host backup destination/retention; agree RPO/RTO.
3. Replace mock SMTP settings and test a specifically authorized external recipient.
4. Obtain the final remote CI result; published clean-checkout verification passed.
5. Have representatives of all five roles run the UAT checklist and sign acceptance.

Social security policy was confirmed by the user: summed daily base earnings,
excluding welfare, OT and adjustments. No contracted-monthly-salary substitution.
