# Subtask 6 — Payment destinations and effective social-security membership

Implemented on backend `a9adf81` / frontend `2454245`, branch `codex/use-case-delivery`. No commits, push, merge, deployment, root gitlink update, production writes, external email or actual payment.

## Delivered behavior

- Dedicated GET/PUT `/api/v1/employees/:employee_id/payment-destination`. HR/OWNER manage; employee reads own. Manager profile-edit rights do not grant destination writes. API contracts use `payment_method` (`cash`/`transfer`) and nullable `promptpay_phone`, separate from contact `phone`.
- Recipient normalization accepts Thai `0[689]` mobile numbers and `+66` form with spaces, hyphens and parentheses; rejects letters, invalid prefixes/lengths and arbitrary slash stripping. Cash accepts null. Transfer can be registered before later preparation validation. No contact-phone fallback.
- Mutations use existing transaction/domain audit boundaries; audit stores method and recipient-presence facts without recording full recipient phone. New routes join the existing transport audit registry (18 employee actions).
- Assignment onboarding and successor history carry `is_social_security_member`, default true for existing clients. Membership changes close the earlier effective row and create a successor, with membership included in audit facts and UI history.
- Daily payroll projection takes membership from each day's effective assignment. Only covered daily base salary enters the social-security earned base; welfare, OT and adjustments remain excluded. Existing absence/leave policy, rounding, rates and cap remain unchanged.
- New calculated records persist membership/base snapshots; snapshot assignment is the last covered employment assignment even when employment ends before period end. Old locked rows keep a nullable earned-base snapshot and true membership default. The locked-payroll trigger remains unchanged.
- Profile UI has HR/OWNER destination editor and employee own read view. Onboarding/history forms expose membership checkbox. Real browser testing found an uncontrolled-input issue when resaving a canonical-equivalent phone; controlled draft values now display the server's canonical phone immediately.

## Migration and preservation evidence

`backend/drizzle/0004_conscious_toro.sql`, generated snapshot and journal are additive. Existing employees with an active primary bank account backfill to transfer; others and new employees default cash. There is no contact-phone copy. No payroll-row UPDATE or trigger disable is present.

Root inspected and applied only to disposable project `haris-payroll-verify`. Root's pre/post hashes of **135 existing payroll records** (excluding the two added columns) and **8,919 existing payroll items** matched. Root evidence: `/private/tmp/haris-task6-migrate.log` and the corresponding locked-before/locked-after files. Catalog checks now expect 38 tables, 24 enums and 5 serialized migrations.

## Verification

Commands were run in the named package directory unless the command starts with Docker.

| Check | Exact command | Result |
|---|---|---|
| Backend types | `bun run typecheck` | Passed |
| Backend non-DB suite | `bun test` | 486 passed, 35 skipped, 0 failed; skips are DB-gated tests |
| Focused actual DB | `docker compose -p haris-payroll-verify -f compose.yaml -f compose.verify.yaml exec -T backend sh -c 'TEST_DATABASE_URL="$DATABASE_URL" bun test src/features/payroll/payroll.membership.integration.test.ts'` | 1 passed, 11 assertions |
| Full actual DB suite | `docker compose -p haris-payroll-verify -f compose.yaml -f compose.verify.yaml exec -T backend sh -c 'RELEASE_DISPOSABLE_DB=1 TEST_DATABASE_URL="$DATABASE_URL" bun run test:db'` | **519 passed, 0 skipped, 0 failed, 111 files** |
| Frontend units | `bun test` | 47 passed, 160 assertions |
| Frontend types | `bunx tsc --noEmit` | Passed |
| Frontend lint | `bun run lint` | Passed |
| Real browser | `bunx playwright test e2e/payment-destination.e2e.ts` | **2 passed in 9.3s** |
| Diff whitespace | `git diff --check` in backend/frontend | Passed |
| UI mechanical scan | Impeccable detector on the four changed UI surfaces | No findings (`[]`) |

TDD RED evidence: `/tmp/payment-red.log` (missing normalizer/earned-base snapshot), `/tmp/payment-auth-red.log` (missing destination use case), `/tmp/payment-ui-red.log` (missing dedicated client mutation), `/tmp/payment-history-red.log` (missing member default), `/tmp/payment-audit-red.log` (missing route registrations). Subsequent focused tests passed. Browser RED additionally reproduced stale canonical phone display before its fix; final browser run is green. Full DB initially detected stale catalog expectations (23 enums/4 migrations); updating them to the approved 24/5 restored the green suite.

The actual DB integration proves 10 covered days at 1,000/day => **10,000.00 base / 500.00 deduction**, excluding nonmember days paid at 2,000/day. It checks last terminated assignment selection, persisted snapshots, later-assignment independence, immutable locked update rejection, and legacy NULL base/default true. Unit tests also cover all-nonmember zero SS, existing default-member behavior, welfare/OT/adjustment exclusions, and effective successor preservation.

Real browser used HR, OWNER (`admin` fixture), employee and branch-manager accounts on web 18083. It proves recipient `+66 81-234-5678` becomes `0812345678`; changing contact phone to `0899999999` and reloading preserves recipient; invalid transfer phone returns stable `VALIDATION_ERROR`/422; employee own read works, another employee's destination is denied, employee/manager crafted PUT requests return 403, and OWNER saves cash with null phone. OWNER creates a separate future fixture and changes membership through the dated history UI, preserving both original and successor ranges.

Desktop/mobile screenshots inspected:

- [haris-task6-owner-payment.png](haris-task6-owner-payment.png)
- [haris-task6-owner-payment-mobile.png](haris-task6-owner-payment-mobile.png) (390px, no horizontal page overflow)
- [haris-task6-owner-membership.png](haris-task6-owner-membership.png)

Logs: `/tmp/payment-full-db.log`, `/tmp/payment-backend-tests.log`, `/tmp/payment-frontend-tests.log`, `/tmp/payment-ui-types.log`, `/tmp/payment-ui-lint.log`, `/tmp/payment-e2e.log`. Container database URLs were reused without printing credentials. Browser fixture changes exist only in the disposable verification database.

## Boundaries and limitations

Task 7 owns `payroll_payments` preparation, frozen recipient/amount values, validation of missing transfer recipients and QR generation. This task intentionally generates no QR and does not claim any transfer succeeded. Task 8 owns payment lifecycle. Task 9 must preserve NULL legacy earned base and derive any fallback only from frozen `base_salary` payroll items; never use zero or contracted monthly salary as the fallback. No export changes are included here.

Fresh review remains the root controller's next gate. Author verification is complete; no author-side commits were created.

## Review fix round 1 — Concurrent destination audit history (P2)

Finding reproduced before editing production code: two HR saves can read cash/no recipient concurrently; A commits transfer/recipient, then B commits cash/no recipient with a stale cash→cash audit. `/tmp/payment-concurrency-red.log` shows the actual second audit's old state `{payment_method: cash, has_promptpay_phone: false}` instead of A's committed `{payment_method: transfer, has_promptpay_phone: true}`.

Minimal fix: `EmployeePaymentRepositoryPort.findPaymentDestination` accepts an optional `forUpdate` flag. Only the mutation's initial read inside its existing transaction requests `FOR UPDATE`; ordinary GET reads remain unchanged. No schema change, migration, payroll-wide lock or authorization change.

Added `backend/src/features/employee/employee.payment-destination.concurrency.integration.test.ts`: three real PostgreSQL connections, two service transactions, controlled gates and actual `pg_blocking_pids` evidence. A pauses after its initial destination read; B begins concurrently and must wait before reading. An independent ordinary read still returns cash without waiting. After A commits transfer, B reads it, saves cash and commits its real audit row. The test checks B's audit old state equals A's audit new state, both new states, and final persisted destination. Test fixtures and audit rows are confined to the disposable database.

RED command (repository root):

```sh
docker compose -p haris-payroll-verify -f compose.yaml -f compose.verify.yaml exec -T backend sh -c 'TEST_DATABASE_URL="$DATABASE_URL" bun test src/features/employee/employee.payment-destination.concurrency.integration.test.ts'
```

Result before fix: **0 passed / 1 failed**, the expected stale-audit assertion. Same concurrency test plus `employee.payment-destination.test.ts` after fix: **3 passed / 0 failed / 25 assertions** (`/tmp/payment-concurrency-green.log`). A subsequent explicit assertion that B has not read while blocked is included in the final full DB regression run.

Final regression commands/results:

- `cd backend && bun run typecheck`: passed.
- `cd backend && bun test`: **486 passed / 36 DB-gated skips / 0 failed**, 112 files (`/tmp/payment-fix1-unit.log`).
- `docker compose -p haris-payroll-verify -f compose.yaml -f compose.verify.yaml exec -T backend sh -c 'RELEASE_DISPOSABLE_DB=1 TEST_DATABASE_URL="$DATABASE_URL" bun run test:db'`: **520 passed / 0 skipped / 0 failed**, 112 files (`/tmp/payment-fix1-db.log`).
- Backend `git diff --check`: passed.

Only the destination repository/service and the focused concurrency integration test changed for this fix. Frontend/browser/schema are unchanged from the prior verified handback. Source frozen again for scoped independent re-review; no commits.

## Root closure

Scoped independent re-review marks P2 ADDRESSED, specPASS/qualityPASS. Root inspected finalDBlog520pass/0skip/0fail112files and frontend47pass; screenshot copies retained in this reportdirectory. Checkpointsbackend `1c98720`,frontend `c0975e5`; no push/deploy/rootgitlinkupdate. Task6complete. Payment preparation/QR belongsTask7, paid/cancelTask8, exportsTask9; this closure does not claim those features are implemented.
