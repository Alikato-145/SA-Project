# Employee Loan Requests Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox syntax for tracking.

**Goal:** Employee submits an own loan request; HR/OWNER approves or rejects it through the web, with approval creating exactly one loan and its installments.

**Architecture:** Add request workflow in the existing loan feature, reusing the existing exact-cent installment splitter and operation transaction context. Preserve direct HR loan creation and existing deduction logic. Keep transport DTO mapping in controller/mapper and database queries in repositories.

**Tech Stack:** Bun/Elysia/Drizzle/PostgreSQL16, Next.js16/React19.

**Spec:** `docs/superpowers/specs/2026-10-25-use-case-delivery-design.md`, loan requests / UC16.

## Global Constraints

- Employee own data only; HR/accounting and OWNER finance decisions, no new manager finance right.
- Request pending → approved/rejected; no editing requested principal/count into different approved values.
- Approval and loan/installment creation must be one transaction with duplicate decisions prevented. Loan principal uses exact decimals, installment count1–5 per existing contract.
- Approver chooses a first due month that is not locked; do not insert historical deduction schedules into locked payroll.
- Additive migration, one schema owner at a time, DBML/Drizzle/reference parity; disposable DB only. No pushes, external emails or money transfers.

## Review Focus

- Employee cannot forge employee_id to submit/read another person's request.
- Two concurrent approve calls must not create two loans or duplicate installments.
- Failure creating an installment rolls back request decision and loan together.
- Requested principal split must sum exactly, including100.01 split3 and minimum-cent boundaries.
- A payroll lock racing approval must not create installments that bypass the common payroll-input lock.

### Task 1: Employee request / finance decision vertical slice

**Files:**
- Extend owning `backend/src/features/loan/loan.schema.ts`, repository/service/runtime/controller/routes/mapper/dto and tests. Add feature-prefixed request-service/repository files only if they keep existing files readable.
- Update `backend/src/app.ts` composition, feature schema exports/relations and shared error registry only as necessary.
- Generate next serialized additive migration and catalog expectations.
- Extend `frontend/app/(dashboard)/finance/page.tsx` with a loan request form/list and finance decision form; use existing API helpers, styles and employee picker.
- Create `frontend/e2e/loan-requests.e2e.ts`; update root DBML and reference notes with root coordination.

**Interfaces:**
- New `/api/v1/loan-requests` POST/GET and `/:id/approve`, `/:id/reject` POST (use existing transport/response conventions).
- Request body employee_id, principal_amount, installment_count, reason. Request owns server-set requested_by_user_account_id, requested_at and pending status.
- Approval body first_due_month (YYYY-MM-01), not earlier than the current Bangkok business month at approval and unlocked for the full installment range; rejection body decision_note required. Requested data immutable after insert; decision actor/time recorded.
- Table loan_requests: bigintPK, employee_id FK, principal_amount numeric12,2 positive, installment_count smallint1–5, reason, pending/approved/rejected status, requester/time, decision actor/time/note, nullable loan_id UNIQUE FK. Reuse an existing suitable request enum only if domain meaning matches; otherwise create named enum through normal shared schema enums.
- Existing LoanService.createLoan and splitInstallments are reused through services, never import a different feature repository. `operationTransaction` already joins active AsyncLocalStorage transaction; verify this invariant in approval rollback test.

- [ ] Read AGENTS and Next docs; inspect existing operation-runtime and loan contracts. Write failing own-request/other-employee denial, HR approval/rejection, duplicate decision, rollback and locked due-month tests, capture genuine RED.
- [ ] Add schema/migration with request constraints/indexes and unique loan link. Coordinate with root before apply; preserve old loans and history.
- [ ] Implement request list/create and row-locked decision workflow; finance authorization and employee assignment checks server-side. Acquire payroll input serialization before decision/loan writes and validate the complete installment date range with existing mutability service. Reject second decision with stable conflict or idempotently return original result; never create another loan.
- [ ] Run focused backend tests and typecheck; expect zero failures, exact installment sums and old loan deduction tests unchanged.
- [ ] Add employee own request UI; finance sees scoped employee requests and approval month/rejection reason controls. Employee must not see decision buttons or direct HR loan creation. Explain pending/approved/rejected clearly in Thai and show created loan installments after approval.
- [ ] Real browser: employee submit→reload pending; HR approve→employee reload loan/installments; separate OWNER rejection journey; forged otheremployee submission403 and employee approval403. Verify duplicate approval creates one loan only and exact principal/count retained.
- [ ] Hand back to root for DBML parity, disposable migration and fullDB tests in sequence. Run frontend unit/lint/typecheck; no full sharedDB or browser jobs concurrently.
- [ ] Report `docs/superpowers/reports/05-employee-loan-requests.md` with RED/GREEN, transaction proof, UI evidence and limitations. Root commissions fresh review before task-specific commit. No root gitlink updates.
