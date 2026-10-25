# Current Payroll Adjustments Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox syntax for tracking.

**Goal:** HR/accounting and OWNER can add approved earnings/deductions to an unlocked current payroll period without requiring an older locked record.

**Architecture:** Extend the existing payroll adjustment entity/workflow with a direct employee reference and nullable original record. Preserve locked-origin corrections and the serialized transactional preview/lock application path. Add a current-period UI alongside the existing historical correction form.

**Tech Stack:** Bun/Elysia/Drizzle/PostgreSQL16, Next.js16/React19; exact decimal strings.

**Spec:** `docs/superpowers/specs/2026-10-25-use-case-delivery-design.md`, current-period adjustments and schema delta.

## Global Constraints

- Accounting uses HR grant, no ACCOUNTING role.
- Pending must block payroll lock. Approved adjustments apply once; locked results are immutable.
- Current adjustments require employee/target period/direction/positive amount/reason/requester. Old corrections retain locked original/later target/same shop validation.
- Exact decimal money, backend authorization, transactional state transitions and append-only audit. No actual payments or external email sends.
- One migration owner at a time; additive migration with existing-row backfill, DBML/Drizzle/reference parity. Only disposable verification DB may be migrated.

## Review Focus

- Historical rows must keep their original employee and amount after backfill.
- Mismatched employee_id and original record must never redirect a correction to a different employee.
- Current items for another shop or employee without a valid assignment must be rejected.
- Concurrent approval/lock and repeated preview must neither duplicate nor omit adjustment line items.
- Pending current items must appear in readiness and block locking, including scoped branch roster queries.

### Task 1: Current adjustment vertical slice

**Files:**
- Modify `backend/src/features/payroll/payroll.schema.ts`, `payroll.types.ts`, `payroll.dto.ts`, `payroll.mapper.ts`, `payroll.routes.ts`, `payroll.controller.ts`, `payroll.service.ts`, `payroll.repository.ts` and existing feature tests/support.
- Generate next migration under `backend/drizzle/` after auth revocation0001. Update catalog migration expectation only as required.
- Modify `frontend/lib/payroll/payroll-api.ts`, `frontend/components/payroll-adjustments.tsx`; create `frontend/e2e/current-adjustments.e2e.ts`.
- Update root `haris-payroll-postgresql.dbml`, `haris-payroll-orm-reference.md`, `2026-09-10-haris-payroll-dbml-design.md` in coordination with root.

**Interfaces:**
- Consumes `requestPayrollAdjustment`, `decidePayrollAdjustment`, listAdjustments, payroll readiness/input projections and serialized preview/lock paths.
- Keep existing POST `/api/v1/payroll/adjustments` legacy origin payload valid. Add `employee_id` for origin-free requests; require target period always; when original supplied infer employee or validate matching supplied employee. Responses expose employee_id and nullable original_payroll_record_id. Extend existing list filters to employee/target as needed.
- Persistence: employee_id NOT NULL FK employees RESTRICT/CASCADE; backfill from original payroll record before NOT NULL; original_payroll_record_id nullable. New current items always target non-null. Preserve old target-null data rather than silently changing history. Add target/employee/status index.

- [ ] Read AGENTS, relevant frontend Next docs and exact current types. Add failing tests for current request success/pending blocking/approval/preview/lock single application; cross-shop or missing assignment; employee/supervisor/manager denial; mismatched origin; legacy origin validation preserved. Capture real RED.
- [ ] Generate migration and edit it for safe employee backfill before NOT NULL. Add DB integration coverage for direct employee FK, old rows and approval/application integrity. Do not apply DB migration independently of root or run shared DB tests concurrently.
- [ ] Implement minimal typed service/repository/controller/mapper changes. All input projections/readiness queries currently inner-joining original payroll record must support origin-free items using direct employee_id. Do not change calculator rounding or social-security bases in this task.
- [ ] Run focused tests and backend typecheck; expect zero failures. Existing locked-source correction tests must still pass.
- [ ] Add current-period earnings/deduction form using an employee choice drawn from selected period roster and unlocked period, with amount/reason and pending approval list. Keep existing historical correction form accessible. Add focused frontend contract checks and a real UI journey for each HR/OWNER role.
- [ ] Verify disposable browser request→pending prevents lock→approve→preview repeatedly→lock once→reload persistent totals. Verify deduction producing negative net cannot lock; employee cannot approve or submit payroll adjustments. Include same-employee historical correction regression.
- [ ] Hand schema changes back to root to update reference parity and apply disposable migration; run full migrated DB suite and frontend tests/lint/typecheck sequentially after ownership agreement. Expect zero failures; report any test-harness throttling accurately.
- [ ] Write report `docs/superpowers/reports/04-current-payroll-adjustments.md` with migration/backfill, RED/GREEN evidence, browser proof, exact commands and limitations. No push/merge/deploy or root submodule pointer changes. Commit only this task after independent review.
