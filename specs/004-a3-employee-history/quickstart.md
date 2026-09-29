# A3 Validation Quickstart

## Preconditions

1. Use an isolated, migrated PostgreSQL database and valid A1 auth/audit configuration.
2. Register the A3 route bundle in a test-only Elysia composition with a current-actor adapter. Do not edit the shared `app.ts` as part of A3.
3. Seed two shops, two branches, two departments, matching shop positions, and test actors for Employee, Supervisor, Branch Manager, HR, and Owner.
4. Supply the confirmed bank encryption key/version configuration before running bank and full onboarding scenarios.

## Scenario 1 — Scope and private fields

Create employees assigned to separate departments and branches. List/detail as each role. Verify self/department/branch/all visibility and hidden-detail not-found behavior. Team responses must omit compensation, full identity values, and bank data.

## Scenario 2 — Identity and status

Create an employee with national ID or passport ID, then test duplicate code, duplicate each identity type, and missing identity. Change to terminated with a valid date; reject a date before hire. Verify historical employee detail remains available and account login status is unchanged.

## Scenario 3 — Assignment history

Create a first assignment and a change on date D. Verify the former row ends on D minus one day, the next starts on D, and a lookup before/on D resolves the correct organization and exact salary/welfare strings. Reject a one-day overlap, reversed range, inactive organization, mismatched department, and mismatched position shop.

## Scenario 4 — Bank privacy and primary lifecycle

Add two accounts, switch primary, and deactivate primary with a replacement or an explicit no-primary choice. Verify one active primary at most, ciphertext differs from plaintext, only last four digits appear in responses/audit, and a failed audit rolls back the switch. Run only after key policy is confirmed.

## Scenario 5 — Weekly holidays

Create weekdays 0 and 6, close and replace one period, and verify historical date lookup. Reject -1, 7, reversed dates, and overlapping same-weekday periods.

## Scenario 6 — Atomic onboarding

Submit employee, first assignment, optional bank, holidays, and account in one request. Verify one public audit outcome and a one-time temporary password only in the successful response. Force failure in each component and verify no partial rows remain.

## Verification commands

Run from `backend/`:

```sh
bun run typecheck
bun test
```

Run database suites one file per Bun process with an isolated database and an explicit integration flag. Record commands, counts, and any limitations in the A3 handoff.

## 2026-09-23 US1 verification record

- `bun test src/features/employee/employee.read.test.ts`: 6 pass, 0 fail. This includes a 1,000-row **in-memory** paging test, not the database-backed SC-006 performance claim.
- `bun test src/core/audit/a3-transport-audit.plugin.test.ts src/features/employee/employee.scope.test.ts src/features/employee/employee.validation.test.ts`: 12 pass, 0 fail.
- `bun run typecheck`: pass.
- `bun test` full backend, two consecutive reruns: 250 pass, 18 PostgreSQL-gated skip, 0 fail each. First full run had 4 failures in `auth.plugin.test.ts` returning 401; the same file alone passed 6/6 and both following full runs passed 250/250. Treat this as a transient suite interaction requiring further investigation if it recurs, not as a verified product regression.
- `DATABASE_URL` was unset, so no A3 PostgreSQL integration or database-backed 1,000-row performance result is claimed. Production `app.ts` composition remains Person C's handoff.


## 2026-09-27 final A3 verification record

- Focused A3 plus affected A1 regression suite: 44 pass, 0 fail.
- `bun run typecheck`: pass.
- `bun test`: 329 pass, 21 PostgreSQL-gated skip, 0 fail, 1,355 assertions across 70 files.
- All six database integration files were then run in separate Bun processes against an isolated migrated PostgreSQL 16 database (`haris_payroll_a3_verify` on local port 55433): 16 pass, 0 skip, 0 fail in total. The leave and overtime database contracts used isolated employee/account/leave-type fixtures. The temporary PostgreSQL service was stopped after verification; its volume remains recoverable.
- `createA3EmployeeRoutes` is the independently composable route bundle for Person C. Shared `src/app.ts` was not edited.
- The 1,000-row employee paging check remains an in-memory performance test; no database-backed SC-006 performance claim is made.
- Schema-owner follow-up: DBML defaults `employee_bank_accounts.is_primary` to `false`, while Drizzle/migration defaults it to `true`. A3 always sends an explicit boolean to persistence and intentionally made no schema or migration change. The schema owner must choose and align the canonical default later.
