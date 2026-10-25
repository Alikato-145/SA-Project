# Subtask 5 — Employee loan requests

## Delivered

- `/api/v1/loan-requests` create/list, `/:id/approve`, `/:id/reject`; requested terms remain immutable and requester/decision/link fields are server owned.
- Employee own request/list only. Decisions require an active all-scope HR or OWNER grant; branch managers receive no new finance rights. Current employment assignment is checked.
- Approval takes the common payroll-input transaction lock before locking the request row; reuses `LoanService.createLoan`, exact-cent `splitInstallments` and the active `operationTransaction`. Loan, installments, decision and audit share one transaction.
- Approval rejects first due months before the current Bangkok business month (`LOAN_REQUEST_PAST_DUE_MONTH`, 422), and checks the entire installment range against locked payroll. Existing direct HR creation and deduction code remain unchanged.
- Finance page: employee request form, pending/approved/rejected history; HR/OWNER first due month and required rejection note; approved loans retain the existing installment display. Thai error/help copy explains forbidden retroactive schedules.
- Additive generated migration `backend/drizzle/0003_employee_loan_requests.sql`, snapshot and journal; root inspected/applied only on the disposable verification DB and updated DBML/reference parity. Catalog expectation: 38 tables, 23 enums, 4 migrations.

## RED → GREEN evidence

- Initial backend request test failed because `loan-request.service` did not exist; then three behavior tests passed (own scope, finance decision/duplicate prevention, rejection).
- Browser RED: employee Finance page lacked region `คำขอเงินกู้` (15-second visible assertion failure). After form/list implementation, employee submit/reload pending passed.
- Past-month behavioral RED: approval of unlocked `2000-01-01` resolved unexpectedly. GREEN: it rejects with `LOAN_REQUEST_PAST_DUE_MONTH`; current Bangkok month is accepted by the request policy and remains subject to runtime payroll mutability.
- Integration test's initial failure was an assertion mismatch: Drizzle wraps PostgreSQL `23505` in `cause`; correcting the assertion exposed the real rollback behavior. Browser raw API assertions likewise use snake_case, while the frontend API helper converts to camelCase.

## Verification

Run package commands in their package directories. Local verification only: compose project `haris-payroll-verify`, web 18083, PostgreSQL 55440, Mailpit 18025. Container DB URL was reused without printing credentials; no production writes or external email.

- Backend `bun run typecheck`: passed.
- Backend `bun test`: **482 passed, 34 skipped, 0 failed** (516 tests). Database-dependent tests remain opt-in in this no-DB run.
- Focused real DB: `docker compose -p haris-payroll-verify -f compose.yaml -f compose.verify.yaml exec -T backend sh -c 'TEST_DATABASE_URL="$DATABASE_URL" bun test ./src/features/loan/loan-request.database.test.ts ./src/features/loan/loan.test.ts ./src/features/loan/loan-request.test.ts'`: **10 passed, 0 failed, 46 assertions**.
- The DB test proves concurrent HR/OWNER approval yields exactly one loan; 3 installments sum to 100.01; duplicate decision conflicts; own forged submit/read and employee/manager decision fail; OWNER rejection creates no loan; a real installment unique violation rolls back loan and request decision; a locked last installment month rejects the entire schedule.
- Race proof: another connection holds `pg_advisory_xact_lock(72419,5)`, approval remains waiting, that connection inserts/commits a locked final due month, approval resumes and rejects `PAYROLL_PERIOD_LOCKED`, leaving request pending.
- Frontend `bun test`: **46 passed, 0 failed**; `bunx tsc --noEmit`: passed. Lint initially caught three explicit-any annotations in the new E2E assertions; replaced with typed callback shapes; final `bun run lint` and `bunx tsc --noEmit` both passed.
- Final `bun run test:e2e e2e/loan-requests.e2e.ts`: **4 passed**. Employee submits/reloads pending; HR approves and employee reloads matching loan/installments; OWNER rejects and employee reloads note; forged own scope and employee/manager decisions return 403; duplicate approval returns 409. Tests assert 100.01 principal and 33.34/33.34/33.33 installments.

Evidence: `loan-requests-hr.png`, `loan-requests-admin.png`, `loan-requests-employee-approve.png`, `loan-requests-employee-reject.png` in this report directory. Desktop HR capture visually inspected; existing workspace controls/layout retained.

## Boundaries / handoff

No commits, push, merge, deployment or root submodule-pointer changes. Test fixtures are uniquely prefixed and retained only in the disposable verification DB. Root owns full database suite/catalog validation and the fresh review before task-specific commits. No new pending-request payroll blocker is needed: only an approved request creates deductions, and approval always validates mutable months. No additional manager finance permission or accounting role was introduced.

## Root full-DB follow-up

Root's complete migrated-DB run executed 514 tests: 513 passed, 0 skipped, 1 failed (`src/core/db/database.integration.test.ts`, `all domain primary keys use bigint`). The failure was the stale expected row count 37 versus the new 38 tables, not a primary-key type mismatch. Changed that assertion to 38 while retaining `rows.every(({ data_type }) => data_type === "bigint")` unchanged. Focused migrated catalog rerun (`TEST_DATABASE_URL="$DATABASE_URL" bun test ./src/core/db/database.integration.test.ts` inside the verification backend): **9 passed, 0 failed, 21 assertions**. Backend `bun run typecheck`: passed. Source frozen again; no production code changed in this follow-up.

## Root closure

Final full migrated DB514pass/0skip/0fail109files+typecheck (`/private/tmp/haris-task5-final-db.log`). Initialfullrun513pass/1fail due stale expectedPKcount; focusedfix9pass and fullrerun514pass closed it without weakening bigintchecks. Freshreview finalspecPASS/qualityPASS. Checkpoints backend `a9adf81`,frontend `2454245`; no push/merge/deploy/rootgitlinkupdate. Subtask5complete, fullsystemUAT remains separately pending.
