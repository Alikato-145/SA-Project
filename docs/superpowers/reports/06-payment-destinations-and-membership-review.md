# Subtask 6 — Independent review

Reviewed the frozen Task 1 package against the brief and the plan's Global Constraints/Review Focus, with backend baseline `a9adf81` and frontend baseline `2454245`. Inspected the corresponding implementation for authorization, destination/contact separation, assignment history, daily membership calculation, persistence, migration safety, controller/mapper boundaries and UI integration. No source changes, test reruns, database operations or browser runs were performed.

## Verdict

**Final after Fix 1: Spec PASS; Quality PASS. P2 ADDRESSED; no open actionable findings.** The initial finding and its resolution are retained below. No P0/P1 findings. Task 7 preparation/recipient snapshots/QR and Task 9 exports remain outside this review.

## Finding

### [P2] Lock the destination before reading its audit old values

Location: `backend/src/features/employee/employee.service.ts:90–95`; persistence read at `backend/src/features/employee/employee.repository.ts:176–177`.

The new mutation reads `current` with an ordinary SELECT and only acquires a row lock when UPDATE executes. The transaction wrapper uses the normal database isolation and does not serialize these destination writes. Two HR/OWNER saves can therefore both read the same old value before either updates. For example, starting from cash/no recipient, A saves transfer/recipient and B saves cash/no recipient: after A commits, B overwrites it but records cash → cash in its audit instead of transfer → cash. This makes the sensitive-change history inaccurate even though each mutation and its audit insert commit atomically. It violates the project requirement to record old/new values for sensitive changes.

Minimal fix: provide a repository read with `FOR UPDATE` for the mutation's initial SELECT and use it within the existing transaction; retain the ordinary read for GET. Add a focused concurrent-save check proving the second committed audit sees the first committed destination as its old state. No schema change or payroll-wide lock is needed.

## Requirements confirmed

- Dedicated destination DTO/controller/mapper/service/repository path; HR/OWNER writes and self/admin reads enforced server-side. Generic manager identity updates do not accept payment fields; frontend controls use the separate finance permission.
- Contact phone is independent. Normalization accepts canonical Thai mobile and separated +66 input, rejects malformed values, and cash permits null. Missing transfer recipients remain allowed for Task 7 preparation validation.
- Membership defaults preserve prior clients and is stored on effective assignment successors. Daily payroll uses each dated assignment's membership, includes only base-salary items in the covered base, and persists the exact base and final assignment membership snapshot. Existing calculation/absence/leave rules are retained.
- Additive migration backfills employee method from active primary bank existence; does not copy contact phone, update old payroll rows, disable the immutable trigger, or fabricate a legacy earned base. Mapper preserves legacy NULL.
- Root's reported schema coordination and disposable-only application are accepted. Reported pre/post hashes cover 135 existing records and 8,919 items unchanged. Reported verification: full DB 519 pass/0 skip/0 fail, backend types and non-DB 486 pass/35 skip, frontend 47 tests plus lint/types, and two browser cases. These results were not independently rerun, as instructed.

Review limitations: static review plus supplied verification evidence; no independent concurrency execution. No additional actionable privacy, payroll calculation, legacy-data or scope-expansion defect identified.

## Scoped re-review — Fix 1

**P2 ADDRESSED.** Reviewed `.superpowers/sdd/2026-10-25-payment-destinations-and-membership/task-1-fix1-package.md` and the appended implementation report. Scope was the original race and any breakage introduced by its repair. No tests, source edits, database operations or browser runs were performed.

The repository's optional `forUpdate` argument defaults to false. Only the mutation's initial destination read passes true, selecting with `FOR UPDATE` inside the existing transaction. The employee row therefore remains locked through its UPDATE, audit insertion and commit; another destination save cannot capture old state until the preceding transaction commits. The regular GET retains its ordinary nonblocking SELECT. Authorization, destination normalization, public contract, migration and payroll calculation are unchanged. No new actionable issue found in this repair.

The added real PostgreSQL regression uses separate service connections, controlled gates and `pg_blocking_pids` to establish overlapping writes. It asserts B has not read while blocked, verifies an ordinary GET remains nonblocking, and checks B's audit old state equals A's committed new state. This directly covers the reported failure rather than only checking a repository mock. Accepted reported RED stale-audit failure and GREEN results: focused 3 passed/25 assertions, backend typecheck passed, non-DB suite 486 passed/36 DB-gated skips/0 failed, full DB suite **520 passed/0 skipped/0 failed across 112 files** (`/tmp/payment-fix1-db.log`). These results were not rerun.

Final spec/quality verdict applies to Subtask 6 only; future payment preparation must independently coordinate any recipient snapshot read with destination edits, as part of Task 7.
