# Payment Lifecycle Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** HR/OWNER record manual full salary payout, cancel preparation and see accurate paid/outstanding totals by branch without changing locked payroll.

**Architecture:** Extend Task7 payroll-payment layers and existing payroll panel; use the existing transaction serialization and immutable payment snapshots. Derive totals from locked records plus active payments; retain cancelled history. No new table or migration expected.

**Tech Stack:** Bun/Elysia/Drizzle/PostgreSQL16; Next.js16/React19; existing exact-decimal utilities and Playwright.

**Spec:** docs/superpowers/specs/2026-10-25-use-case-delivery-design.md

## Global Constraints

- Accounting uses HR grant, no ACCOUNTING role.
- Full UC1–16 and Login, each named actor, UI submission + persisted result + negative authorization checks.
- Manual actual cash/bank/QR transfers only; no bank API integration or external email sends. Mailpit only for email tests.
- เงินและยอด snapshot ใช้ exact decimal; FK และประวัติไม่ใช้ cascade deletion ที่ลบหลักฐาน
- Never edit locked payroll values; use a tracked payroll adjustment instead.
- Employee: own data only. Supervisor: own department. Branch manager: own branch. HR/accounting and owner: all branches, with duties appropriate to the role.
- Root coordinates schema; do not alter migration0005 or schema without reporting a concrete mismatch. Preserve root gitlinks and unrelated work; no push/merge/deploy.

## Review Focus

- A duplicate payout confirmation must return the same result without a second write/audit event or falsely confirming twice.
- Concurrent pay/cancel must settle exactly one transition; no paid row can be cancelled.
- Repreparing after cancellation must retain old evidence and use newly registered recipient; previously downloaded QR cannot be invalidated externally.
- A zero-net employee is visible but never outstanding; cancelled history must not inflate totals or hide outstanding salary.
- Mixed branches and changed live assignments must not move historical payables or widen actor permission.

---

### Task 1: Manual payout, cancellation and branch completion vertical slice

**Files:**
- Modify backend/src/features/payroll/payroll-payment.{types,repository,service,controller,mapper,routes}.ts and focused tests.
- Modify backend/src/core/errors/error-codes.ts only for stable transition errors.
- Modify frontend/components/payroll-payments.tsx and frontend/lib/payroll/payroll-payment-api.ts with focused tests.
- Extend frontend/e2e/payroll-payments.e2e.ts or add frontend/e2e/payroll-payment-lifecycle.e2e.ts.
- Report docs/superpowers/reports/08-payment-lifecycle.md.

**Interfaces:**
- Consume Task7 createPayrollPaymentService, PaymentCommand, PaymentGroupRow, existing prepared/paid/cancelled schema and list/prepare/QR endpoints. Reconcile these names against Task7 reviewed handback before dispatch; never parallel-write Task7.
- Add service `confirmPayrollPayment({actor,requestId,paymentId,referenceNo?})` and `cancelPreparedPayrollPayment({actor,requestId,paymentId,reason})`, returning domain payment data. Service enforces HR/OWNER authority before lookup, then serialized transaction and current-state checks.
- POST `/api/v1/payroll/payments/:payment_id/confirm` with `{reference_no?:string}`; POST `.../:payment_id/cancel` with `{reason:string}`. Cookie-origin protection, numeric-ID validation and controller-only safe mapping follow Task7 routes.
- Confirmation accepts optional trimmed reference up to200 characters, normalizes empty to null. Prepared→paid writes actor/server timestamp/reference atomically. Identical repeat on paid returns existing unchanged; different reference conflicts. Cancelled→paid conflicts. Paid snapshots/timestamp/actor cannot be overwritten.
- Cancellation requires trimmed nonempty reason up to1000 characters. Prepared→cancelled writes actor/server timestamp/reason atomically. Identical repeat on cancelled returns existing unchanged; different reason conflicts. Paid→cancelled conflicts. Repository lifecycle lookup must include cancelled rows, while existing active lookup stays limited to prepared/paid.
- Existing DB trigger permits only prepared→paid/cancelled; idempotency returns existing without UPDATE. Keep frozen destination/amount/branch/creator immutable. Audit one event for actual transition; action-attempt logging may remain separate. Audit includes safe IDs/state/reference/reason, never full bank/cipher/token.
- Add GET `/api/v1/payroll/periods/:period_id/payments/summary` with optional branch_id, returning `{branches:[{branch_id,branch_name,employee_count,payable_count,paid_count,outstanding_count,total_payable,total_paid,total_outstanding,complete}],totals:{...same numeric/count fields}}`. Monetary fields exact two-decimal strings. All locked rows appear once. total_payable=sum positive net; total_paid=sum active paid amounts; total_outstanding=payable-paid; counts ignore zero-net for payable/paid/outstanding; employee_count includes zero-net. complete means outstanding_count=0. Summary uses historical branch snapshots/assignments, never current assignment; cancelled rows never count as paid.
- Include safe per-record payment history in list response or dedicated GET `/api/v1/payroll/payments/:payment_id/history` only if necessary for existing row UI; prefer adding safe cancelled history to period rows. Retain evidence of cancelled reason/actor/time and paid actor/time/reference without full bank details.

- [x] Write failing focused tests: prepared100.01 confirm once/repeat same preserves paid_at/actor/audit count; repeat changed reference conflicts; unauthorized employee/supervisor/manager denied; cancelled cannot confirm; paid cannot cancel; blank/oversize reason/reference validation; missing payment404.
- [x] Capture RED, then implement transaction transitions through repository conditional updates and domain audit within transaction. Use existing serialization lock order. No ordinary UPDATE on idempotent return.
- [x] Write and run actual migrated disposable-DB race tests: simultaneous pay/pay yields one persisted paid row and one transition audit; pay/cancel yields exactly one winner and valid metadata; deliberate audit/write failure rolls whole transition back. Cancel then reprepare creates new ID, retains old snapshot/history and reads fresh destination. Old QR endpoint denies cancelled/paid row.
- [x] Write exact total assertions for two branches: branchA net100.01+50.02+0.00, branchB25.00; initial totals175.03/0.00/175.03 with payable_count3 and employee_count4. Pay100.01 → outstanding75.02; cancel50.02 preparation leaves outstanding75.02; reprepare/pay50.02 → branchA complete, all-branch outstanding25.00. Transfer live assignment afterward and assert old branch totals unchanged.
- [x] Implement summary and safe history, then run focused tests GREEN. No accumulated floating-point money or duplicate joins across cancelled attempts.
- [x] Add UI confirmation showing employee/amount/destination and explicit manual verification before marking paid; display reference input, paid timestamp/state and branch paid/outstanding totals. Use cancellation label “ยกเลิกการเตรียมจ่าย” with reason. Explain generated/scanned QR does not confirm transfer and cancelling preparation cannot reverse a bank transfer or invalidate downloaded QR. No action buttons on zero/paid/cancelled history rows except deliberate reprepare through existing flow.
- [x] Real browser HR and OWNER each confirm/cancel via UI, reload and verify persistence, exact totals, retained cancellation history and no duplicate confirmation. Test direct API denial for employee/supervisor/manager and paid/cancelled QR denial. Use synthetic fixtures only; do not scan in banking app or transfer real funds.
- [x] Sequential verification: backend typecheck + guarded migrated full DB suite; frontend bun test/lint/tsc; focused real browser. Do not run database-mutating suites simultaneously. Retain screenshots and concise logs/counts in report, state limits honestly.
- [x] Freeze source, write task report plus report08 and hand back for fresh spec+quality review. Root commits only scoped files after review gate; no root gitlink updates. Task9 begins only after this gate.
