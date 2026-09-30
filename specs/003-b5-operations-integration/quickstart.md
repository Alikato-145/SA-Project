# B5 Validation Quickstart

Use an isolated migrated PostgreSQL 16 database. From repository root:

```sh
POSTGRES_PORT=55433 docker compose --env-file .env.example -p haris-b5-check up -d --wait postgres
cd backend
bun install --frozen-lockfile
export DATABASE_URL=postgresql://postgres:postgres@127.0.0.1:55433/haris_payroll
export TEST_DATABASE_URL="$DATABASE_URL"
export AUTH_JWT_SECRET=b5-disposable-test-secret-at-least-32-characters
export AUTH_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
export EMPLOYEE_BANK_ENCRYPTION_KEY_VERSION=v1
export EMPLOYEE_BANK_ENCRYPTION_KEYS='{"v1":"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA="}'
bun run db:migrate
bun run typecheck
bun test src/test/b5-operations-journey.test.ts
bun test
```

These auth/encryption values are exclusively for disposable tests. The journey writes its latest temporary account credentials and IDs to `/private/tmp/haris-b5-demo.json`; read that file for a local walkthrough. Before the broad test command, optionally set `B1_TEST_EMPLOYEE_ID` and `B2_TEST_EMPLOYEE_ID` to `employee_id`, `B1_TEST_BRANCH_ID` to `branch_a`, `B2_TEST_ACCOUNT_ID` to `owner_id` and `B2_TEST_LEAVE_TYPE_ID` to `leave_type_id` from that file. This enables the three older attendance/leave/OT database checks. Do not enable these against shared payroll data.

Run the older opt-in database groups in separate processes, with the exports above retained:

```sh
DATABASE_INTEGRATION=1 bun test src/core/db/database.integration.test.ts
DATABASE_INTEGRATION=1 bun test src/features/audit/audit.integration.test.ts
A2_DATABASE_INTEGRATION=1 bun test src/features/shop/shop.write.integration.test.ts
A2_DATABASE_INTEGRATION=1 bun test src/features/department/department.repository.integration.test.ts
A2_DATABASE_INTEGRATION=1 bun test src/features/organization/organization.history.test.ts
A2_DATABASE_INTEGRATION=1 bun test src/features/branch/branch.write.test.ts
A2_DATABASE_INTEGRATION=1 bun test src/features/position/position.read.test.ts
A2_DATABASE_INTEGRATION=1 bun test src/features/position/position.write.test.ts
A2_DATABASE_INTEGRATION=1 bun test src/features/department/department.write.test.ts
cd ../frontend
bun install --frozen-lockfile
bun test
bun run lint
bun run build
```

Backend runtime uses `ADVANCE_REQUEST_DAY=20`, `ADVANCE_MIN_WORKED_DAYS=20` and `ADVANCE_SALARY_RATIO=0.5000` by default; these environment settings may be configured, and are validated. Money and IDs remain decimal strings in public requests. See [contracts](contracts/operations.md), [data model](data-model.md), and [schema owner handoff](schema-owner-handoff.md).

For a browser walkthrough, start backend from its directory with the same environment plus `ELYSIA_HOST=127.0.0.1 ELYSIA_PORT=3001 bun run dev`. In another terminal, start frontend with `BACKEND_ORIGIN=http://127.0.0.1:3001 bun run dev --hostname 127.0.0.1 --port 3000`. Sign in at `http://127.0.0.1:3000/login` using the temporary owner account from the fixture file. Open attendance, leave, overtime and finance from navigation and use its employee/branch/shop IDs. Review transferred attendance, leave quota/history, all OT types and finance settlements. The current fixture month is locked; use the following month for a schedule successor and manual work-day save/read-back. Role/session failures and locked corrections are asserted in the HTTP journey.

The real-database journey prepares unique disposable data and validates exact payroll totals, transaction rollback, two-branch history and denied corrections in seconds. Advance submission runs in that journey on/after day 26 so its recorded-days fixture can satisfy the configured default; focused tests cover eligibility on other dates. Payroll projection/locking regressions also run whenever TEST_DATABASE_URL is set. Skipped tests are reported separately in [validation](validation.md).

Stop only the validation servers and project after verification:

```sh
POSTGRES_PORT=55433 docker compose --env-file .env.example -p haris-b5-check stop postgres
```

Fixtures remain in the isolated test volume because audit/approval/debt history is append-only. No schema generation, normal development data change, or submodule pointer update is part of B5.
