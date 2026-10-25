# Subtask 3 — Scoped employee CRUD review

## Verdicts — after fix round 1

- **Spec compliance: PASS for reviewed Subtask 3 scope.** Both concurrency findings are addressed; no additional actionable regression was found in their fix.
- **Task quality: PASS.** The fix reuses existing service-level serialization, keeps payroll mutability policy separate from contact editing, and adds deterministic real PostgreSQL concurrency evidence.
- **P1: ADDRESSED.** Employee profile/status mutations now obtain transaction advisory serialization before reading current assignment scope.
- **P2: ADDRESSED.** Direct termination now obtains that serialization before assignment row locks, matching transfer order.

The findings below preserve the original review rationale; neither remains open.

## Finding

### [P1] Serialize branch authorization with assignment changes

**Location:** `backend/src/features/employee/employee.service.ts:109–119` and `:152–163` (particularly new guards at lines 111 and 154).

Both methods read the current assignment through `findById`, authorize the manager, and later update the employee by ID only. The repository read has no row lock, and these paths acquire no assignment/payroll mutation lock. Under the default transaction isolation, an HR transfer can close branch A's assignment and insert the current branch B assignment after the manager's read but before the employee update. The branch A manager then successfully edits personal details or changes active/inactive/suspended status despite the employee now belonging to B. Merely wrapping the read/write in a transaction does not prevent this.

Use a shared serialization mechanism with assignment transfers, then read/revalidate current scope while holding it through the employee update; cover both profile and non-termination status operations. A common employee lock requires the transfer path to participate too. Add a controlled two-transaction test that pauses the manager mutation before authorization, commits the transfer, resumes, and verifies denial/no employee change; also cover a transfer racing after the initial read.

Concrete minimal synchronization option: inject the existing payroll input service `serialize` capability into employee service and call it at transaction entry **before** `findById` in both mutations. `createPayrollInputService` exposes `serialize: serializePayrollInputs` (`payroll.service.ts:323`), backed by transaction advisory lock `(72419, 5)` in `payroll.input-lock.repository.ts`. HR `createAssignment` already acquires the same lock through `assertInputsMutable` before changing assignments. Using the service capability preserves cross-feature service dependencies and avoids importing another feature's repository. Re-read current assignment only after acquiring that lock and hold it through commit. Do not add payroll locked-period rejection to contact editing merely to acquire a lock; use `serialize` directly. This retains the existing documented global-lock throughput ceiling.

The termination path does independently read and authorize locked assignment rows in `endAssignmentsForTermination`, so this finding targets profile/non-termination status writes rather than claiming all termination authorization is unprotected.

### [P2] Restore consistent advisory-lock-before-row-lock order for termination

**Location:** `backend/src/features/employment-assignment/employment-assignment.service.ts:23–27`.

This diff moves `findForTermination` (which uses `FOR UPDATE`) ahead of `assertInputsMutable` (which obtains the global advisory lock). A concurrent HR transfer obtains the advisory lock first and then `findLatest`'s assignment row lock. If termination locks the assignment while transfer holds the advisory lock, each waits for the other; PostgreSQL aborts one valid operation as a deadlock. This is newly introduced by the changed ordering.

Acquire the existing payroll service `serialize(executor)` before `findForTermination`, preserving advisory-lock → assignment-row-lock order; then perform locked current-branch authorization and the existing mutability validation. Extend the assignment service dependency from `Pick<PayrollInputService, "assertInputsMutable">` to include `serialize`. Add a controlled transfer/termination concurrency regression proving neither operation deadlocks. Acquiring serialization at employee-service entry alone does not protect other direct callers of this transactional termination method; keep its own lock order safe too.

## Other review conclusions

- Cross-branch onboarding and optional account/bank requests are rejected before employee insertion. Standalone creation and public assignment administration remain HR/OWNER-only.
- Manager contact/date DTO mapping supplies the existing edit form's phone/email/address and omits national/passport identity fields; supervisor mapping remains sparse.
- Current assignment, rather than historical branch membership, controls ordinary sequential mutation permission. Termination keeps assignment rows and salary snapshots, audits truncation, and uses existing payroll mutability checks.
- Success notice survives the subsequent profile reload; documented loss of manager read access after a past termination is consistent with the selected current-assignment visibility policy.
- Frontend profile controls are separate from HR/OWNER bank/account/history controls; onboarding branch choices are restricted and account/bank options disabled for managers.

## Evidence and limits

Read the task brief, global constraints/review focus, frozen review package, actual implementation/repository/transaction code, frontend controls, and implementer report `03-scoped-employee-crud.md`. Reviewed changes against backend `dea8d64` / frontend `6e1b14f` as supplied. Accepted supplied evidence: backend 469 pass / 28 database skip / 0 fail plus typecheck; frontend 45 pass, lint/typecheck; focused real browser manager create/edit/terminate and negative onboarding checks passed.

No tests, database writes, browser journeys, or application changes were performed in this review. Root owns full disposable-database validation. The concurrency finding is established by source/interleaving analysis, not a new live reproduction. Broader HR/OWNER browser journeys, future-dated onboarding, and backdated termination after read-scope loss were not independently exercised.

## Fix round 1 re-review

Scope: original P1/P2 and new breakage in their repair only. Read frozen `task-1-fix-round1-package.md`, appended implementer report, and current service/composition/lock code. No source changes, tests, database operations, or browser journeys were performed for this re-review.

**P1 — ADDRESSED:** `employee.service.ts:111` and `:155` call the required `payroll.serialize(executor)` before `findById`. The same executor/transaction retains serialization through authorization, update, and commit. HR transfer already obtains this advisory lock through `assertInputsMutable` before assignment changes; therefore a transfer preceding the manager read changes the observed branch, while a transfer following it waits until the authorized write commits. `app.ts:235` injects the existing payroll service. Contact updates call serialization directly and do not gain a locked-period policy restriction. The required dependency is explicitly wired in test callers too.

**P2 — ADDRESSED:** `employment-assignment.service.ts:23–24` calls the narrowed payroll dependency's `serialize` before `findForTermination` locks assignment rows. Direct transactional callers therefore preserve advisory → row lock order independently of employee-service orchestration. Reacquiring the same transaction advisory lock through existing mutability validation is safe and keeps policy enforcement intact.

Reviewed the five new PostgreSQL concurrency cases: both orderings for profile/status versus transfer and a direct termination case that observes an advisory wait while a third connection can acquire assignment rows with `FOR UPDATE NOWAIT`. These exercise actual repositories, transactions, assignment transfer service and locks; payroll-period policy/organization validation stubs are clearly bounded. Root reports fresh full database validation **502 pass / 0 skip / 0 fail across 107 files**, plus typecheck; implementer reports focused concurrency **5 pass**, local backend **471 pass / 33 database skip / 0 fail**. These are supplied execution evidence, not reruns by this reviewer.

No new actionable breakage found in the repair. Practical limits remain the existing global-lock throughput ceiling and the original browser/date-policy coverage limits above. This scoped re-review does not claim a repository-wide concurrency audit.
