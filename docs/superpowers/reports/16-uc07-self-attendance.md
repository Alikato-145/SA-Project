# 16 — UC07 employee own manual attendance

Implemented and frozen for independent spec/quality review on 26 October 2026. This report covers Task 1 only. Root owns review, checkpoint commits, shared guide/main ledger and final 20-use-case regression/integration. No commit, push, merge, deployment, schema or automation change was performed by this task.

## Requirement and root cause

Binding source: `docs/superpowers/specs/2026-10-26-use-case-20-alignment-design.md`, UC07 and global constraints; `.superpowers/sdd/2026-10-26-use-case-20-alignment/task-1-brief.md`.

The attendance route excluded EMPLOYEE, its page offered only the staff employee picker, and attendance runtime exclusively used shared `manage` authorization. That shared rule correctly denies self grants across other features; changing it globally would expand unrelated permissions.

## Implementation

- Attendance-local authorization first preserves existing staff `manage` access. Only a denied manage attempt can fall back to the authenticated employee association plus a valid active EMPLOYEE/self grant. Shared employee operation-context policy remains unchanged.
- Own create/correction uses dated assignment branch validation, current effective schedule, derived Bangkok lateness and deductible status. Self worked/late entries require clock-in; self absence requires no clock timestamps. Ordinary self entries cannot override public/weekly/closed-day rules.
- Self correction checks the OLD row is manual and ordinary present/late/absent, rejects leave/import/holiday rows, requires a new trimmed 5–1,000 character reason with a letter or digit, and preserves branch/date/source/creator. Creation source remains manual. `entry_source` is explicitly rejected by create/correct request validation.
- Existing transaction, payroll serialization/input locks, employee/date uniqueness and domain audit record actor plus old/new facts. Locked corrections are checked before attendance validation. No new attendance approval system or clock integration.
- Existing attendance page uses the established EmployeeContextPicker: employees see their linked identity and dated branch, no arbitrary picker; staff retain their scoped picker/actions. Self holiday choices are removed, derived late minutes stay read-only through status changes, and correction reason has matching length guidance. Existing layout/components retained.

Changed application/test files (7): backend attendance.runtime.service.ts, attendance.routes.ts, new attendance.self.integration.test.ts; frontend attendance/page.tsx, route-access.ts, route-access.test.ts, new attendance-self.e2e.ts. All other feature permissions, schema/migrations and academic/user-dirty files were preserved.

## Observed RED and corrections

Commands run from repository root unless a package is specified:

```sh
docker compose --env-file .env.example -p haris-payroll-verify -f compose.yaml -f compose.verify.yaml exec -T backend sh -ec 'TEST_DATABASE_URL="$DATABASE_URL" bun test src/features/attendance/attendance.self.integration.test.ts'
```

Observed intended RED: **0 pass / 4 fail**, own create expected200 received403 `FORBIDDEN_SCOPE`. Before that, two fixture setup errors (duplicate linked employee; missing payroll-period creator) were repaired; the latter raw log and a truthful note about the first overwritten raw log remain in local task evidence. These are fixture errors, not feature RED.

From frontend:

```sh
bun test lib/auth/route-access.test.ts
E2E_BASE_URL=http://localhost:18083 bun run test:e2e e2e/attendance-self.e2e.ts --workers=1 --retries=0
```

Observed unit RED: **3 pass / 3 fail**, EMPLOYEE attendance excluded. Actual browser RED: **1 fail**, employee could not open attendance. After implementation, a first browser attempt created/persisted successfully then timed out because the test used an exact label selector for a select containing option text; changed to its stable `select[name=recordId]`. The failed log, screenshots and trace are retained locally. A subsequent targeted interaction assertion exposed status-change code making derived minutes editable; observed readonly RED, then fixed the existing handler for self mode. Initial frontend lint caught the new auth effect referencing a state setter before its declaration plus an effect dependency; moved the effect after state declarations and stabilized applyClock with useCallback. Final checks below passed. No failures were hidden or retried automatically.

## GREEN verification

All database/browser work targeted **haris-payroll-verify** only: HTTP18083, PostgreSQL55440, Mailpit18025. No production/external delivery.

| Check | Exact command | Observed result |
|---|---|---|
| Focused API/DB | Docker command above | **5 pass, 0 fail; 57 assertions** |
| Full backend types + migrated DB suite | `docker compose --env-file .env.example -p haris-payroll-verify -f compose.yaml -f compose.verify.yaml exec -T backend sh -ec 'export TEST_DATABASE_URL="$DATABASE_URL" RELEASE_DISPOSABLE_DB=1; bun run typecheck; bun run test:db'` | **545 pass, 0 skip, 0 fail, 120 files**; types exit0 |
| Frontend unit (frontend/) | `bun test` | **54 pass, 0 fail; 175 assertions** |
| Frontend lint (frontend/) | `bun run lint` | exit0, no warnings/errors |
| Frontend types (frontend/) | `bun run node_modules/typescript/bin/tsc --noEmit` | exit0 |
| Frontend build (frontend/) | `bun run build` | exit0, all22 pages generated |
| Final focused browser (frontend/) | `E2E_BASE_URL=http://localhost:18083 E2E_EVIDENCE_DIR=/Users/manus/University/SA-Project/.superpowers/sdd/2026-10-26-use-case-20-alignment/evidence bun run test:e2e e2e/attendance-self.e2e.ts e2e/flow.e2e.ts --grep 'UC07 EMPLOYEE\|schedule changes preserve history' --workers=1 --retries=0` | **2 pass, 0 fail in21.4s**; employee11.4s + existing staff9.4s |
| Whitespace | `git -C backend diff --check` and `git -C frontend diff --check` | exit0 |

The final browser invocation, runnable from frontend/, is:

```sh
E2E_BASE_URL=http://localhost:18083 E2E_EVIDENCE_DIR=/Users/manus/University/SA-Project/.superpowers/sdd/2026-10-26-use-case-20-alignment/evidence bun run test:e2e e2e/attendance-self.e2e.ts e2e/flow.e2e.ts --grep 'UC07 EMPLOYEE|schedule changes preserve history' --workers=1 --retries=0
```
 Application/test sources were frozen throughout each browser invocation. Final backend tests include real application authentication/authorization and PostgreSQL persistence, duplicate conflicts, dated transfer branches, own create/late correction/absence, explicit new correction reasons, inactive/malformed grants, unchanged shared manage denial, other-person list/context/calendar/write403, provenance/status/schedule/deduction rejection, protected old-row preservation, locked create/correct409 and staff import correction/holiday behavior.

## Actual browser persistence and audit

Final scenario uses a fresh EMPLOYEE-only linked account; fixture **employee1334 / account772 / branch1118 / record9444**. UI submitted09:00–18:00, corrected clock-in to09:20, then reloaded and loaded the range again. With09:00 start and5-minute grace the persisted row is **late15 minutes, deductible=true, manual**, with the explicit Thai reason. Browser direct API rejects a forged other employee403 and blank correction reason422. Existing staff schedule-history/calendar/manual-create/clock-correction scenario also passes. Desktop1280×900 and mobile390×844 were inspected; mobile page width does not overflow and the attendance table scrolls within its container.

Independent PostgreSQL read of that exact browser-created row confirms creator772 and unchanged branch/source. Audit has exactly the creation/correction facts for record9444: `attendance.record.create.succeeded` new present; `attendance.record.correct.succeeded` actor772, old present → new late, reason `แก้เวลาเข้าจริงเป็นเก้าโมงยี่สิบ`. See persistence-audit log.

## Evidence and tested source

Durable evidence: [16-uc07-self-attendance-evidence](16-uc07-self-attendance-evidence/), including RED/GREEN/full-check logs, final browser log, actual browser-row/audit read, desktop/mobile PNG and source SHA256 manifest. Local detailed failure artifacts remain under `.superpowers/sdd/2026-10-26-use-case-20-alignment/evidence/` (`task-1-browser-red`, `task-1-browser-first-green-attempt`, `task-1-browser-readonly-red`, setup/lint logs). Traces contain only disposable synthetic fixture credentials and remain local.

Tested base commits (uncommitted task delta): backend `c2a404db6d00df18b0f1a7322e67f15ec9da1d41`; frontend `e6d6fb65b64096840d563e49df29ece981e355af`, both on codex/use-case-alignment-20. Exact seven source/test content hashes are in task-1-tested-source-manifest.json; no final commit/tree SHA exists yet because root owns checkpoints after review.

## Remaining gates and limits

No known UC07 implementation blocker remains. Independent spec/quality review, any resulting bounded fixes, final whole20-use-case actor matrix/browser suite and integration are root-owned and pending. This focused2-test browser run is not claimed as acceptance of the entire20-case delivery. Self service intentionally covers ordinary manual records only; leave/holiday exceptions retain existing staff/approval workflows. All synthetic fixtures/audit facts remain in the disposable database; no historical facts were deleted for cleanup.
