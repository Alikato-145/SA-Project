# Payslip and Email Regression Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Prove UC12/13 via actual HR/OWNER UI and employee own-only PDF, preserving individual delivery history using local SMTP only.

**Architecture:** Exercise existing payslip service/storage/mail workflow after payment/report changes. Fix concrete failures minimally in owning layers; no broad rewrite or new mail provider. Tests use synthetic locked records, account-linked employees and Mailpit.

**Tech Stack:** Existing Bun/Elysia/Drizzle, PDFKit, local SMTP/Mailpit and Next.js/Playwright.

**Spec:** docs/superpowers/specs/2026-10-25-use-case-delivery-design.md

## Global Constraints

- Accounting uses HR grant, no ACCOUNTING role.
- A payslip belongs to exactly one payroll record. Email delivery attempts are logged individually. Enforce authorization so one employee cannot view or receive another employee’s payslip.
- การออกสลิปอ่านข้อมูลผลเงินเดือนรายบุคคลจากแหล่งข้อมูลเดียวกับรายงาน ไม่อ่านหรือแปลงกลับจากไฟล์ PDF สรุป
- Manual actual cash/bank/QR transfers only; no bank API integration or external email sends. Mailpit only for email tests.
- Never edit locked payroll values; use a tracked payroll adjustment instead.
- No schema changes expected. No push/merge/deploy/root gitlink updates; no real database or external inbox.

## Review Focus

- Two single-role employees must not download/get/send each other's slips through guessed IDs.
- Reopening a generated slip returns the same record/file; retries must not create duplicate slips.
- SMTP acceptance and inbox receipt are distinct evidence; UI must not claim a bank payment or guaranteed external receipt.
- Reload preserves delivery attempts, including failures, without overwriting terminal attempt history.
- Report/payment state changes must not alter locked totals or imply that a generated slip confirms payout.

---

### Task 1: Actor-specific payslip generation/delivery UAT and minimal repairs

**Files:**
- Add frontend/e2e/payslip-delivery.e2e.ts with synthetic fixture support in existing verification conventions.
- Modify only demonstrated failures in backend/src/features/payslip/, core mail infrastructure or frontend/app/(dashboard)/payslips/page.tsx and frontend/lib/payslip/.
- Report docs/superpowers/reports/10-payslip-email-regression.md.

**Interfaces:**
- Existing POST /api/v1/payslips/payroll-records/:record_id, GET /:id/download, GET /:id, GET /:id/deliveries, POST /:id/deliveries with recipient_email; GET /mine. Read current routes before testing.
- HR and OWNER each use actual form “ออกหรือเปิดสลิป”, PDF download and “ส่งสลิป” form. Employee uses own list/download only. Supervisor/manager may access own employee-linked slips according to existing self-read policy, never administrative generation/delivery.
- Use locked record/items as the sole financial source; compare record/payslip/report projection totals exactly. No extraction of summary PDF to construct slips. A paid row is not prerequisite for valid slip creation; preserve existing locked-only rule.
- Local Mailpit18025 only. Verify isolated compose mailer configuration before sending; synthetic example.test addresses only with locally captured SMTP. Never use external credentials/productionSMTP. Keep recipient addresses and attempt IDs as synthetic evidence; no secrets.

- [x] Read relevant AGENTS/Next docs and current service/storage/mailer behavior. Confirm disposable stack and local SMTP target. Baseline focused existing payslip service/routes/document tests before any code change.
- [x] HR UI generates and downloads slip for linked employeeA; OWNER independently generates/opens employeeB slip. Reopening/reloading each returns same slip ID and exact bytes/financial totals. Compare with underlying locked financial projection including adjustments and SS base changes.
- [x] HR and OWNER each submit local email via UI. Assert distinct persisted attempt/log, SMTP accepted response and matching Mailpit message/recipient/attachment bytes; record acceptance vs local inbox receipt separately. Reload history and verify terminal attempt unchanged. Exercise existing failure/recovery test boundary without sending externally or disabling production protection.
- [x] EmployeeA UI own download works; employeeB guessed A metadata/PDF/deliveries/send requests denied. Supervisor/manager generation and email APIs denied; own-only access stays allowed where linked. Anonymous download401. No OWNER grant masking scoped fixtures.
- [x] If a concrete bug appears, record symptom/root cause and failing regression first (RED), then minimal service/repository/controller/UI fix and GREEN. Follow systematic-debugging and TDD; preserve immutable financial/delivery history.
- [x] Run focused tests plus required backend typecheck/full guarded disposable DB suite only if source changed; frontend unit/lint/types for frontend changes. Run new actual browser cases and retain readable panel screenshots/download/message evidence. Avoid parallel database mutators and production Login limiter changes.
- [x] Write report10 and task report with actual actor outcomes/counts and limits. Freeze source for fresh spec+quality review; root scoped commit only after review. If no implementation changes were needed, report tested behavior without inventing fixes. Full UC UAT remains Task11.
