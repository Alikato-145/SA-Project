# Haris Payroll Product Backlog

รายการนี้คือสิ่งที่ต้องพัฒนาต่อจากฐาน PostgreSQL เพื่อให้ Haris Payroll กลายเป็นเว็บใช้งานจริง เพื่อนสามารถเลือก task ตาม ID ได้ แต่ต้องทำ dependency ให้เสร็จก่อน

## Assignment rules

- หนึ่งคนรับหนึ่ง task หรือหนึ่งกลุ่มไฟล์ ห้ามแก้ไฟล์เดียวกันพร้อมกัน
- ก่อนเริ่ม ให้สร้าง `specs/<task-id>-<short-name>/spec.md` จาก `docs/task-spec-guideline.md`
- Backend ต้องใช้ flow `route → controller → service → repository → database`
- Authorization และ transaction อยู่ใน service/backend ไม่พึ่งการซ่อนปุ่มใน frontend
- ห้ามแก้ Drizzle schema หรือ migration ระหว่างทำ feature โดยไม่แยก task และคุยกับ schema owner
- ทุก task ต้องส่ง changed files, commands/tests ที่รัน และ known limitations ตอน handoff

## Phase 1 — Shared backend and frontend foundation

- [ ] T001 Finalize PostgreSQL infrastructure validation and handoff in `specs/001-align-postgresql-infrastructure/tasks.md` and `specs/001-align-postgresql-infrastructure/quickstart.md`
- [ ] T002 [P] Implement typed application errors and the Elysia error boundary in `backend/src/core/errors/` and `backend/src/app.ts`
- [ ] T003 [P] Implement transaction/unit-of-work support for services in `backend/src/core/db/transaction.ts`
- [ ] T004 Implement password hashing, session/token policy, and authenticated actor types in `backend/src/core/auth/`
- [ ] T005 Implement reusable role-scope authorization checks for self, department, branch, and all scopes in `backend/src/core/auth/authorization.ts`
- [ ] T006 [P] Define stable API response/error contracts in `backend/src/shared/http/` and frontend API client behavior in `frontend/lib/api/`
- [ ] T007 [P] Add backend test helpers and isolated PostgreSQL fixtures in `backend/src/test/`
- [ ] T008 [P] Build the authenticated frontend shell, navigation, loading, forbidden, and error states in `frontend/app/(dashboard)/` and `frontend/components/`

**Foundation gate:** login-capable routes can identify an actor, enforce scope, use transactions, and return stable errors.

## Phase 2 — Authentication and account administration (MVP Slice 1)

- [ ] T009 [AUTH] Implement account lookup and credential persistence in `backend/src/features/user-account/user-account.repository.ts`
- [ ] T010 [AUTH] Implement login, logout, current-user, lockout, and failed-attempt rules in `backend/src/features/user-account/user-account.service.ts`
- [ ] T011 [AUTH] Add authentication DTOs, schemas, mapper, controller, and routes in `backend/src/features/user-account/`
- [ ] T012 [AUTH] Implement scoped role assignment and scope-combination validation in `backend/src/features/role/` and `backend/src/features/user-account/`
- [ ] T013 [P] [AUTH] Build login and account/role administration pages in `frontend/app/login/` and `frontend/app/(dashboard)/accounts/`
- [ ] T014 [AUTH] Add authentication, lockout, role-scope, and unauthorized-access tests in `backend/src/features/user-account/*.test.ts`

**Independent test:** a user can log in, `/me` returns safe account data, invalid scope assignments fail, and protected routes reject unauthorized actors.

## Phase 3 — Organization master data (MVP Slice 2)

- [ ] T015 [P] [ORG] Implement shop and branch repositories/services in `backend/src/features/shop/` and `backend/src/features/branch/`
- [ ] T016 [P] [ORG] Implement department and position repositories/services in `backend/src/features/department/` and `backend/src/features/position/`
- [ ] T017 [ORG] Add organization DTOs, mappers, controllers, routes, validation, and inactive-record behavior in `backend/src/features/{shop,branch,department,position}/`
- [ ] T018 [P] [ORG] Build organization administration screens in `frontend/app/(dashboard)/organization/`
- [ ] T019 [ORG] Add organization uniqueness, inactive-master, and branch/department consistency tests in `backend/src/features/{shop,branch,department,position}/*.test.ts`

**Independent test:** HR can manage organization masters without deleting records referenced by history.

## Phase 4 — Employee and employment history (MVP Slice 3)

- [ ] T020 [EMP] Implement employee repository/service with national-ID/passport validation and soft status changes in `backend/src/features/employee/`
- [ ] T021 [EMP] Implement effective-dated assignment create/transfer/promotion/salary-change use cases in `backend/src/features/employment-assignment/`
- [ ] T022 [P] [EMP] Implement employee bank-account and weekly-holiday use cases in `backend/src/features/employee-bank-account/` and `backend/src/features/employee-weekly-holiday/`
- [ ] T023 [EMP] Add employee, assignment-history, bank-account, and weekly-holiday APIs in `backend/src/features/{employee,employment-assignment,employee-bank-account,employee-weekly-holiday}/`
- [ ] T024 [P] [EMP] Build employee list/detail/edit and employment-history screens in `frontend/app/(dashboard)/employees/`
- [ ] T025 [EMP] Add duplicate identity, overlapping assignment, transfer, compensation-history, and bank-account masking tests in `backend/src/features/employee/*.test.ts` and `backend/src/features/employment-assignment/*.test.ts`

**Independent test:** HR creates an employee, transfers or changes salary through a new effective row, and prior history remains unchanged.

## Phase 5 — Schedules, holidays, and attendance (MVP Slice 4)

- [ ] T026 [P] [ATT] Implement branch schedule and override use cases in `backend/src/features/branch-schedule/`
- [ ] T027 [P] [ATT] Implement holiday-calendar use cases in `backend/src/features/holiday-calendar/`
- [ ] T028 [ATT] Implement work-day record creation/correction with branch snapshots and source tracking in `backend/src/features/attendance/`
- [ ] T029 [ATT] Add schedule, holiday, attendance DTOs/controllers/routes and scoped queries in `backend/src/features/{branch-schedule,holiday-calendar,attendance}/`
- [ ] T030 [P] [ATT] Build schedule calendar, attendance table, and manual-entry screens in `frontend/app/(dashboard)/attendance/`
- [ ] T031 [ATT] Add unique work-day, timezone boundary, schedule override, and historical branch-snapshot tests in `backend/src/features/attendance/*.test.ts`

**Independent test:** a manager records and reviews one work-day per employee/date using the correct historical branch and schedule.

## Phase 6 — Leave workflow

- [ ] T032 [LEAVE] Implement leave types, quotas, requests, and day expansion in `backend/src/features/leave/leave.repository.ts` and `backend/src/features/leave/leave.service.ts`
- [ ] T033 [LEAVE] Implement transactional submit/approve/reject/correct-type flows with append-only approval history in `backend/src/features/leave/leave.service.ts`
- [ ] T034 [LEAVE] Enforce supervisor up-to-three-day and branch-manager approval scope in `backend/src/features/leave/leave.service.ts`
- [ ] T035 [LEAVE] Add leave DTOs, mapper, controller, and routes in `backend/src/features/leave/`
- [ ] T036 [P] [LEAVE] Build employee request, quota, and manager approval screens in `frontend/app/(dashboard)/leave/`
- [ ] T037 [LEAVE] Add overlap, quota, 3-vs-4-day approval, type-correction, and attendance-transaction tests in `backend/src/features/leave/leave.test.ts`

**Independent test:** an employee requests leave and an authorized manager decides it atomically without overlapping days or losing approval history.

## Phase 7 — Overtime workflow

- [ ] T038 [OT] Implement OT request and explicit approval/rejection use cases for rest-day, hourly, and public-holiday OT in `backend/src/features/overtime/`
- [ ] T039 [OT] Add OT DTOs, mapper, controller, routes, and scope enforcement in `backend/src/features/overtime/`
- [ ] T040 [P] [OT] Build employee OT request and manager approval screens in `frontend/app/(dashboard)/overtime/`
- [ ] T041 [OT] Add payable-only-when-approved, approval-history, and OT-type tests in `backend/src/features/overtime/overtime.test.ts`

**Independent test:** late clock-out alone never becomes payable OT; only explicitly approved OT is available to payroll.

## Phase 8 — Advances, loans, and food debt

- [ ] T042 [P] [FIN] Implement advance eligibility and approval use cases in `backend/src/features/advance/`
- [ ] T043 [P] [FIN] Implement loan and installment lifecycle in `backend/src/features/loan/`
- [ ] T044 [P] [FIN] Implement append-only debt charge/adjustment/reversal use cases in `backend/src/features/debt/`
- [ ] T045 [FIN] Add finance DTOs, controllers, routes, authorization, and transaction handling in `backend/src/features/{advance,loan,debt}/`
- [ ] T046 [P] [FIN] Build advance, loan, installment, and debt-ledger screens in `frontend/app/(dashboard)/finance/`
- [ ] T047 [FIN] Add date-20, 20-worked-day, half-salary, negative-net-pay, installment, and append-only debt tests in `backend/src/features/{advance,loan,debt}/*.test.ts`

**Independent test:** approved finance items produce traceable payroll deductions without deleting or resetting financial history.

## Phase 9 — Payroll configuration, calculation, and locking

- [ ] T048 [PAY] Implement effective-dated payroll configuration and period lifecycle in `backend/src/features/payroll/payroll.repository.ts` and `backend/src/features/payroll/payroll.service.ts`
- [ ] T049 [PAY] Implement decimal-safe daily payroll calculation and a single rounding policy in `backend/src/features/payroll/calculation/`
- [ ] T050 [PAY] Implement payroll preview using assignment, attendance, leave, OT, advances, loans, debts, and social-security inputs in `backend/src/features/payroll/calculation/`
- [ ] T051 [PAY] Implement payroll lock preconditions and immutable input snapshots transactionally in `backend/src/features/payroll/payroll.service.ts`
- [ ] T052 [PAY] Implement tracked post-lock payroll adjustments in `backend/src/features/payroll/payroll.service.ts`
- [ ] T053 [PAY] Add payroll DTOs, mapper, controller, routes, and scoped period/record queries in `backend/src/features/payroll/`
- [ ] T054 [P] [PAY] Build payroll configuration, period, preview, detail, lock, and adjustment screens in `frontend/app/(dashboard)/payroll/`
- [ ] T055 [PAY] Add calculation, rounding, duplicate-record, incomplete-attendance, pending-approval, negative-net-pay, lock, and adjustment tests in `backend/src/features/payroll/*.test.ts`

**Independent test:** HR previews and locks a complete payroll period; locked facts cannot be edited and corrections use adjustments.

## Phase 10 — Payslips and delivery

- [ ] T056 [SLIP] Implement one-payslip-per-payroll-record generation and voiding in `backend/src/features/payslip/`
- [ ] T057 [SLIP] Implement own-payslip authorization and secure download/view response in `backend/src/features/payslip/`
- [ ] T058 [SLIP] Implement email delivery attempts and append-only delivery logs behind a replaceable mail adapter in `backend/src/features/payslip/`
- [ ] T059 [P] [SLIP] Build employee payslip list/detail and HR delivery-status screens in `frontend/app/(dashboard)/payslips/`
- [ ] T060 [SLIP] Add cross-employee denial, one-to-one, voided-slip, and delivery-log tests in `backend/src/features/payslip/payslip.test.ts`

**Independent test:** an employee can access only their own payslip and every delivery attempt is recorded.

## Phase 11 — Exports, reports, attachments, and audit

- [ ] T061 [P] [REPORT] Implement bank-transfer export from locked payroll records in `backend/src/features/reports/bank-transfer/`
- [ ] T062 [P] [REPORT] Implement social-security export using base salary only in `backend/src/features/reports/social-security/`
- [ ] T063 [P] [REPORT] Implement scoped attendance, leave, OT, debt, and payroll reports in `backend/src/features/reports/`
- [ ] T064 [P] [REPORT] Implement attachment metadata/storage abstraction and authorization in `backend/src/features/attachment/`
- [ ] T065 [REPORT] Implement sensitive-change audit writes and scoped audit queries in `backend/src/features/audit/`
- [ ] T066 [REPORT] Add report/export DTOs, controllers, routes, and safe streaming behavior in `backend/src/features/reports/`
- [ ] T067 [P] [REPORT] Build report filters, export actions, attachment UI, and audit viewer in `frontend/app/(dashboard)/reports/` and `frontend/app/(dashboard)/audit/`
- [ ] T068 [REPORT] Add export totals, social-security basis, authorization, attachment, and secret-redaction tests in `backend/src/features/{reports,attachment,audit}/*.test.ts`

**Independent test:** accounting exports locked payroll totals and authorized users can trace sensitive changes without exposing secrets.

## Phase 12 — Release readiness

- [ ] T069 [P] Add frontend form, loading, empty, validation, and error-state tests in `frontend/`
- [ ] T070 [P] Add API contract and end-to-end tests for the critical employee-to-payroll journey in `backend/src/test/e2e/`
- [ ] T071 Perform authorization matrix testing for employee, supervisor, branch manager, HR/accounting, and owner roles in `backend/src/test/e2e/authorization.test.ts`
- [ ] T072 [P] Add database backup/restore and migration rollback operational documentation in `docs/operations/`
- [ ] T073 [P] Add production observability, health, structured logging, and secret-redaction checks in `backend/src/core/` and `docs/operations/`
- [ ] T074 Run accessibility, responsive-layout, lint, and production-build checks in `frontend/` and record results in `docs/release-checklist.md`
- [ ] T075 Run clean development and production deployment rehearsals and record release evidence in `docs/release-checklist.md`

## Dependency order

```text
Foundation
  → Authentication
  → Organization
  → Employee history
  → Attendance
  → Leave + Overtime
  → Advances + Loans + Debt
  → Payroll
  → Payslips
  → Reports
  → Release readiness
```

After Foundation, frontend shell work can proceed in parallel. Within each feature,
backend service/API must define the contract before its frontend task integrates it.

## Suggested first team allocation

- Developer A: T002–T005 backend foundation/auth primitives.
- Developer B: T006 and T008 frontend shell/API client.
- Developer C: T009–T014 authentication feature.
- Developer D: T015–T019 organization master data.
- Schema/migration owner: reviews any discovered schema mismatch; feature owners do not edit migrations directly.

The first usable demo is T001–T025: login, organization setup, and employee management with preserved employment history.
