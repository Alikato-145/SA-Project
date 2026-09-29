# A5 Verification and Handoff

Run from each submodule without modifying root submodule pointers:

    cd backend && bun run typecheck && bun test
    cd frontend && bun test && bun run lint && bun run build

Database-gated tests need a dedicated TEST_DATABASE_URL. Already-running shared Compose services are not a disposable test database.

## Results

- Backend typecheck: passed on A5 branch.
- A5 focused matrix/audit/payroll tests: 19 passed, 0 failed.
- Backend suite without TEST_DATABASE_URL: 416 passed, 26 skipped, 0 failed.
- Backend suite with dedicated PostgreSQL 16 and migrated schema: 426 passed, 18 skipped, 0 failed. The remaining 18 require additional fixture IDs or environment prerequisites; they are not reported as passed.
- Frontend on develop: 31 tests passed; lint passed; production build passed (20 static pages generated).
- A5 database-gated owner journey: real login, cookie, /auth/me, employee list/detail, and two-assignment cross-branch history passed; unauthenticated detail returned 401. This is an in-process HTTP integration test, not a browser UI test.
- B5 database-gated two-branch operations → payroll lock journey passed after removing its non-portable /private/tmp credential file write. A pg@9 deprecation warning about concurrent client queries remains and is outside this A5 fix.

## Contract and fixes

- Employee operation-context repository now declares that a dated lookup may return undefined. The service's PAYROLL_ASSIGNMENT_MISSING branch is covered by A5.
- Supervisor, manager, HR, owner, and employee checks use dated assignment context; attendance list visibility changes on the transfer date. Existing payroll tests verify dated salary/welfare and a missing-history gap.
- A1–A3 registries resolve 49 unique public actions with one failure audit each; audit snapshots exclude credentials, identity secrets, and full bank account numbers. A1/A2 malformed long route IDs now use the bounded unknown target, preserving failure auditing.
- B5 integration test no longer persists its disposable password to a host file.

## Person C handoff and limits

- The backend login → employee → history path and the B5 operations → payroll lock path are green on an isolated test database. A4 frontend adapters, route access tests, lint, and build are green.
- A human/browser demo of the complete UI and deployment rehearsal remain Person C release activities; this A5 package does not claim they ran.
- Eighteen database tests still intentionally skip without their feature-specific fixture IDs or flags. The disposable A5 PostgreSQL container was used solely for this verification and should be stopped/removed after checks.
- No schema, migration, or public API change was made. Root submodule pointers and unrelated dirty root files were not staged.
