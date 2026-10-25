# Task 4 — Current-period payroll adjustments

## Delivered behavior

HR (including accounting for this delivery) and OWNER can request an earning or deduction for an employee assigned to an unlocked payroll period without supplying an older locked payroll record. The current-period form uses the selected period's roster, lists its adjustments and exposes approve/reject actions for pending items. The original locked-record correction form remains available below it.

The existing POST `/api/v1/payroll/adjustments` accepts optional `employee_id` and optional `original_payroll_record_id`, while retaining a required target period. With an original, the employee is inferred or checked against the explicit employee; locked-original, same-shop and later-target checks remain. Without an original, employee and valid target-shop assignment are required. EMPLOYEE, SUPERVISOR and BRANCH_MANAGER cannot request or decide adjustments. Responses include `employee_id` and nullable `original_payroll_record_id`.

Request and approval remain in the shared serialized transactional path. Pending current items block lock; approved items use the direct employee reference in readiness and input projections. Repeated preview does not settle an adjustment; final lock marks it applied and records one source line. Negative-net lock rolls back without applying the deduction. No calculator rounding or social-security calculation was changed.

## Migration and existing history

Generated `backend/drizzle/0002_motionless_piledriver.sql` and its Drizzle snapshot/journal. The generated SQL was corrected to add nullable `employee_id`, backfill it from each original payroll record, then set NOT NULL. The new FK uses RESTRICT/CASCADE. Original record becomes nullable; target/employee/status has an index. `chk_adjustment_origin_or_target` requires a target for origin-free rows while preserving legacy original-backed rows with null targets.

Root inspected and applied only to the disposable verification database. Root reported 64 preexisting adjustments, all with valid original references; after migration all 64 had matching direct employees, with no null or mismatched employee values. Root updated DBML, ORM reference and design-decision parity. Application implementation did not apply the migration independently.

## RED → GREEN evidence

Before implementation, `bun test src/features/payroll/payroll.adjustment.test.ts` failed for the expected missing behavior: response lacked employee, mismatched original employee was accepted, and origin-free request without employee was accepted by the existing harness. Existing legacy cases passed. The first authorization assertion used the wrong expected error identifier (`FORBIDDEN`); corrected it to the existing `FORBIDDEN_SCOPE` contract.

The frontend API contract check first failed because `periodId` was ignored and the list URL lacked `period_id`. After implementation, all four payroll API tests passed with exact decimal payloads preserved.

Final service tests cover current request/approval, missing assignment, missing employee, original mismatch, all three denied roles and existing legacy validations. Real migrated integration covers current request, pending lock blocking, approval, repeated preview, single application, direct employee FK and current deduction resulting in negative net. The first negative-preview persistence assertion incorrectly expected a saved line; corrected to zero because existing blocker behavior intentionally does not persist an invalid preview. No production change was made for that assertion.

## Verification

Run from the appropriate package directory unless otherwise stated:

- Backend `bun run typecheck`: passed.
- Focused backend adjustment/lock/routes/preview checks: passed (21 checks before the final expanded role tests). Final adjustment file: 10 passed, 0 failed.
- Disposable database focused `payroll.projection.integration.test.ts`: 1 passed, 36 assertions.
- Full migrated backend suite via the guarded `bun run test:db` wrapper: **509 passed, 0 skipped, 0 failed, 107 files**. Log: `/private/tmp/haris-task4-full-db.log`.
- Frontend `bun test`: **46 passed, 0 failed**, 16 files, 157 assertions. Log: `/private/tmp/haris-task4-frontend-unit.log`.
- Frontend `bun run lint` and `bunx tsc --noEmit`: passed.
- `bunx playwright test e2e/current-adjustments.e2e.ts`: **3 passed** (10.4 seconds). OWNER and HR each submit through the actual form, observe pending approval, verify readiness/lock blocking, approve through UI, preview twice, lock, reload and verify persistent 125.01 net and applied status. EMPLOYEE submit and approval both return 403.
- `bunx playwright test e2e/flow.e2e.ts --grep 'approved adjustments apply once'`: **1 passed** (3.5 seconds). Existing same-employee locked-source correction, repeated preview, preserved source and negative-net lock rejection remain green.
- `git diff --check` in both submodules: passed.

Disposable full-suite command from root:

```sh
HTTP_PORT=18083 POSTGRES_PORT=55440 docker compose --env-file .env.example -p haris-payroll-verify -f compose.yaml -f compose.verify.yaml exec -T -e RELEASE_DISPOSABLE_DB=1 backend sh -ec 'export TEST_DATABASE_URL="$DATABASE_URL"; bun run test:db'
```

DB and browser checks ran sequentially, never concurrently. Host sandbox connection attempts failed before escalation; container checks and host Playwright succeeded under approved verification access.

## UI proof and harness correction

The first new browser run timed out because its test did not open the parent payroll workbook, which is where the existing page loads `can_mutate` and reveals adjustment controls. Corrected the harness to select the main shop and open its workbook before accessing the current form, including after reload; no timeout increase or application workaround.

Screenshots after locked-result reload (visually inspected OWNER screenshot):

- [OWNER current adjustment and persistent totals](current-adjustments-admin.png)
- [HR current adjustment and persistent totals](current-adjustments-hr.png)

## Limits and unchanged scope

Only disposable synthetic data was written. No production migration, payments, external email, commit, push, merge, deployment or submodule-pointer update was performed. Existing pg single-client concurrent-query deprecation warning appears during projection integration; all assertions pass. Playwright emits the existing NO_COLOR/FORCE_COLOR environment warning. Dedicated simultaneous approve-versus-lock stress testing was not added; both continue to use the existing shared serialization path. Historical nullable-target rows remain readable but cannot be approved without a target, matching the preexisting decision guard.

## Root closure

Fresh independent review: spec compliance PASS, task quality PASS, no actionable findings. Root inspected fullDB509/0skip0fail log and report evidence; SQL/reference parity and64-row backfill verified. Checkpoints backend `c5a735e`,frontend `6b8387b`; no push orrootgitlink update. Subtask4 complete; remaining fullsystemUAT recorded separately.
