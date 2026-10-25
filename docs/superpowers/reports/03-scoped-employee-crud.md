# Subtask 3 — Branch-scoped employee CRUD

## Delivered

Branch managers can onboard employees into their own branch, edit a current employee's profile/contact fields, and change employment status or terminate employment. Authorization stays in employee/assignment services. Standalone employee creation remains HR/OWNER only. No schema, migration, authentication, or account-administration changes.

## Policy rulings

- Mutation permission uses validated active BRANCH_MANAGER branch grants and the employee's **current** assignment. Supervisor/self grants never confer mutation permission. Historical assignments do not retain edit permission after a transfer.
- Read visibility remains current-assignment based. An employee whose termination ends that assignment before today leaves the manager's list/detail scope. HR/OWNER retain access to history. The success notice is outside the reloaded profile's request state, so mutation confirmation survives a subsequent inaccessible profile.
- Managers cannot include optional `account` or `bank_account` in onboarding; rejection precedes employee insertion. Those onboarding checkboxes are disabled for managers. Existing account, bank, employment-history, and holiday administration controls retain their separate HR/OWNER permission.
- Manager response uses an internal `manager` view mapped at the controller boundary to the existing `EmployeeOwnDto` shape: phone, personal_email, address, hire_date, terminated_at, and team fields. National/passport values and their masked fields are omitted. Supervisor DTO remains sparse. No new public field names were introduced.
- Existing assignment history, salary values, payroll mutability checks, domain audit records, and transaction boundaries are retained. Termination also validates current branch against locked assignment rows in the assignment service.

## Files

Backend:

- `backend/src/features/employee/employee.scope.ts`
- `backend/src/features/employee/employee.service.ts`
- `backend/src/features/employee/employee.mapper.ts`
- `backend/src/features/employee/employee.onboarding.test.ts`
- `backend/src/features/employee/employee.write.test.ts`
- `backend/src/features/employee/employee.read.test.ts`
- `backend/src/features/employment-assignment/employment-assignment.service.ts`
- `backend/src/features/employment-assignment/employment-assignment.service.test.ts`

Frontend:

- `frontend/lib/auth/route-access.ts`
- `frontend/lib/auth/route-access.test.ts`
- `frontend/app/(dashboard)/employees/page.tsx`
- `frontend/features/identity-hr/employees/employee-read-view.tsx`
- `frontend/features/identity-hr/onboarding/onboarding-form.tsx`
- `frontend/e2e/employee-management.e2e.ts`

No submodule pointer updates or task commits were made. AUTH-01 checkpoint changes belong to separate commits and were left untouched.

## RED → GREEN

1. Added branch-manager onboarding and update/termination tests before production changes. The focused employee suite produced **18 pass / 2 fail**: own-branch manager onboarding and updating failed with `FORBIDDEN_SCOPE`, the expected missing capability.
2. Implemented the minimal shared branch-permission helper and service checks. The same focused suite produced **20 pass / 0 fail**. Forbidden branch, account and bank payload tests assert no employee/account/assignment writes; employee/supervisor onboarding is denied.
3. Added a manager `/employees/new` route assertion before the frontend change: **4 pass / 1 fail**, expected true but received false. With route access updated: **5 pass / 0 fail**.
4. Updated the pre-existing manager read-field expectation to the approved contact/date contract, retaining supervisor privacy assertions and adding explicit absence of national-ID masked fields.
5. Added direct assignment-service checks proving manager termination rejects another branch, closes the covered row, and preserves salary; added employee/supervisor update/status denials.

## Validation

Final local checks:

- Backend `bun test`: **469 pass / 28 skip / 0 fail**, 497 tests across 106 files. Skips are the database-dependent tests without TEST_DATABASE_URL; root owns the sequential full database run.
- Backend `bun run typecheck`: passed.
- Frontend `bun test`: **45 pass / 0 fail**.
- Frontend `bun run lint`: passed.
- Frontend `bunx tsc --noEmit`: passed.
- Focused real-browser `employee-management.e2e.ts`: **1 passed (3.3s)** against disposable localhost:18083. It logs in as branch_manager, creates a unique employee through UI, follows the persisted profile, edits phone, reloads and confirms persistence, terminates with confirmation, and checks persisted terminated status. Crafted different-branch and account onboarding requests return403, and the rejected employee does not appear in a subsequent list. Bank/account checkboxes are disabled. The shop selector uses the known DEMO option rather than a fixed option count.

The first browser attempts failed on test selectors (nested-label select lookup and duplicate employee-code text), then passed after selecting accessible comboboxes and the profile definition. Those attempts are not claimed as product failures or completed journeys.

## Review concerns and limits

- Full database and broader HR/OWNER browser regressions are handed back to root, with source frozen after the focused pass. Existing HR/OWNER create, onboarding, identity update, termination, transaction rollback, and audit tests pass in the local backend suite.
- Focused browser proof uses termination on today's date; the later-day/missing-current-assignment confirmation behavior follows the existing notice placement and current-scope policy, but was not separately exercised by that browser journey.
- Manager visibility intentionally excludes future-only assignments and ended assignments. No historical-visibility repository query was added.
- No external services, production data, schema or migrations were changed. Unique disposable browser employee fixtures remain in the verification database for root inspection.

## Review round 1 — authorization/transfer concurrency fix

Review findings addressed:

> [P1] Serialize branch authorization with assignment changes

> [P2] Restore consistent advisory-lock-before-row-lock order for termination

The review correctly identified that a transaction alone did not serialize a manager's current-branch authorization with HR assignment transfers, and that the changed termination order could invert the existing global-advisory/assignment-row lock order.

### Changes

- `employee.service.ts` now requires the existing payroll input service's `serialize` capability and calls it at transaction entry before the current-assignment scope read in both profile and status mutations. The transaction keeps that lock through the employee write and commit. This is serialization only: contact editing gains no locked-payroll-period rejection.
- `app.ts` injects the existing `payrollInputs` instance. Read/onboarding/write test harnesses provide the explicit narrowed dependency.
- `employment-assignment.service.ts` includes `serialize` in its payroll service dependency and calls it before `findForTermination` obtains assignment `FOR UPDATE` locks. Direct transactional callers therefore also maintain advisory-lock → assignment-row-lock order. Existing payroll mutability checks still follow authorization.
- Added `backend/src/features/employee/employee.scope-concurrency.integration.test.ts`, plus focused write and assignment-service regression checks. No schema, migration, auth, or frontend changes in this fix round.

### RED → GREEN

Before the production lock changes, focused employee-write/assignment tests produced **12 pass / 4 fail**: both transfer-before-scope tests incorrectly resolved successfully; both direct-termination tests failed the new serialization-before-row-read assertion. After the minimal service/dependency changes, the same focused suite produced **16 pass / 0 fail**.

The new disposable PostgreSQL concurrency suite uses three connections, real employee/assignment repositories, real service transactions, and real advisory/row locks. Promise gates pause the competing operation at a defined point; observed ungranted PostgreSQL advisory locks establish the wait without relying on an arbitrary delay. Five tests passed:

1. Transfer owns the lock before profile authorization: transfer commits; former branch manager is denied and phone/status remain unchanged.
2. Profile scope read owns the lock first: transfer waits; authorized contact write commits before transfer.
3. Transfer owns the lock before non-termination status authorization: former manager is denied with no employee change.
4. Non-termination status scope read owns the lock first: transfer waits; status change commits first, then transfer rechecks employee state and rejects inactive employment with `RESOURCE_NOT_FOUND`.
5. Direct termination waits for the advisory lock while a transfer owns it. A third transaction can still obtain the assignment row with `FOR UPDATE NOWAIT`, proving termination did not retain that row before obtaining the advisory lock. Transfer then commits and former-branch termination is denied without deadlock.

The concurrency fixtures intentionally stub only payroll-period policy and organization validation, which are outside the synchronization assertion and have separate suites. They retain actual persistence, scope reads, transfer services, row updates, advisory locks and transaction boundaries. Unique `RACE-*` fixture employees remain in the disposable database; no production records or application schema were changed.

### Final validation and handback

- Backend `bun run typecheck`: passed.
- Backend full local `bun test`: **471 pass / 33 database skip / 0 fail**, 504 tests across 107 files.
- Focused disposable PostgreSQL concurrency suite: **5 pass / 0 fail**, final run233ms.
- Root's pre-fix broader evidence: full database suite **495 pass / 0 skip / 0 fail**; selected browser regressions **8 passed**. Those are pre-fix evidence, not claimed as rerun after the concurrency fix.
- Source frozen and ownership handed back to root after the final typecheck/unit/concurrency runs. Root owns the fresh full database run and independent fix review. No commits made.

Remaining limitation: the reused serialization mechanism has the existing documented global-lock throughput ceiling. No new locking scheme or schema structure was introduced.

## Root closure

Final migrated disposable database suite502pass/0skip/0fail107files +typecheck. After the fix, selected realbrowser8/8passed25s (managerCRUD,HRsafeDTO,OWNERfullflow,five-role readscope). Fresh scoped re-review marked P1/P2 ADDRESSED, no new actionable defects. Diff checks passed. Checkpoint commits backend `9c7037b`,frontend `adcaf38`; no push/merge/deploy/rootgitlink update. Logs `/private/tmp/haris-task3-final-db.log`, `/private/tmp/haris-task3-final-browser.log`. Full UC×actor UI matrix remains final UAT; this closure does not claim every future payment/report usecase works.
