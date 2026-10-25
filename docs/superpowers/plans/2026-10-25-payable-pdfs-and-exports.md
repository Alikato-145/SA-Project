# Salary Payable PDFs and Exports Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** HR/OWNER download salary and creditor-summary PDFs from locked payroll, with exact person/branch totals, correct SS earned base and frozen bank destinations.

**Architecture:** Add locked-payroll reporting projections and pure PDFKit rendering in reports feature; keep generic operational summary unchanged. Use stored payroll items/records and active payment snapshots, never live bank details or parsed PDFs. Existing payslip source remains locked records/items.

**Tech Stack:** Bun/Elysia/Drizzle/PostgreSQL16, existing PDFKit/NotoSansThai, Next.js16 and Playwright.

**Spec:** docs/superpowers/specs/2026-10-25-use-case-delivery-design.md

## Global Constraints

- Accounting uses HR grant, no ACCOUNTING role.
- Creditor summary = salary payable by restaurant to employees, aggregate + individual; shared locked-payroll data with payslips, not loan/debt summary.
- Manual actual cash/bank/QR transfers only; no bank API integration or external email sends. Mailpit only for email tests.
- Never edit locked payroll values; use a tracked payroll adjustment instead.
- CSV ประกันสังคมใช้ social_security_base_snapshot ที่ตรงกับฐานหักจริง ไม่ใช้ contracted salary แทนเมื่อรายได้รายวันต่างกัน Bank export ใช้ปลายทางที่ freeze สำหรับรายการจ่าย
- Controllers invoke mappers; services return domain/application data, never HTTP responses or response DTOs.
- No schema/migration change expected. No push/merge/deploy/root gitlink updates. Verification only on disposable stack.

## Review Focus

- Effective membership ends midperiod: positive earned base/contribution still appears despite end flag false.
- NULL legacy base derives only frozen base_salary items; explicit0 stays0 and never falls back to monthly contract.
- Cancelled payment attempts do not duplicate employee totals or select stale recipients for a new active attempt.
- Long Thai names/many employees wrap across pages without clipped labels or lost repeated headings/totals.
- Unprepared or phone-only transfers cannot silently produce a misleading complete bank-export file.

---

### Task 1: Locked salary/creditor PDFs plus factual exports

**Files:**
- Modify backend/src/features/reports/report.{types,repository,service,controller,mapper,routes}.ts and focused tests.
- Create backend/src/features/reports/report.document.ts and tests; reuse existing PDFKit/font assets from payslip, no new PDF dependency.
- Modify frontend/app/(dashboard)/reports/page.tsx and minimal report API module if needed.
- Add frontend/e2e/payable-reports.e2e.ts. Report docs/superpowers/reports/09-payable-pdfs-and-exports.md.

**Interfaces:**
- Read Task8 final handback before dispatch; reconcile paid/cancelled summary structures, no simultaneous writer.
- New service `salaryPayable(actor,periodId,requestId,filters:ReportFilters={})` returns locked domain projection with period, branch grouping, employee rows, earnings/deductions/net, paid/outstanding totals, and frozen line items as needed. Query stored employmentAssignmentId for branch/department; active payment status is read-only supplemental fact. Exact amounts with shared decimal utilities.
- GET `/api/v1/reports/salary-summary.pdf` and `/api/v1/reports/creditor-summary.pdf`, queries period_id/optional branch_id/department_id using existing ReportFilters validation. Require HR/OWNER and locked period, deny other roles before reading. Use controller to invoke pure renderer and return application/pdf attachment, private/no-store/nosniff headers. Safe numeric-ID filenames.
- Salary PDF includes report title/period/filter, one row per employee with earned income/deductions/net and branch/grand totals. Creditor PDF includes same factual earnings/deductions/net per employee plus paid/outstanding and aggregate salary payable, clearly labelled “เงินเดือนที่ร้านต้องจ่ายให้พนักงาน”. Include zero-net employees but not outstanding count. Show unprepared separately from prepared/paid; these documents are not transfer evidence. No employee bank account numbers/ciphertext or loan-creditor reinterpretation.
- Existing `/bank-transfer.csv` continues bank format but reads active prepared transfer snapshots only. Paid rows excluded to avoid reissuing confirmed payouts, cash/zero excluded. For positive unprepared records or outstanding phone-only transfers without frozen bank tuple, return actionable validation explaining preparation/QR path, never silently omit and imply complete export. No live primary-bank fallback. Decrypt only within authorized export service; no full bank details in JSON/audit/logs. Existing SS member bank and nonSS phone+bank snapshots both usable.
- Existing `/social-security.csv` header base_salary may remain for compatibility but value is social_security_base_snapshot; NULL legacy uses sum frozen base_salary items. Contribution is frozen social_security item sum. Include covered-base/contribution rows even end-member false; omit explicit0 base and0 contribution when no insured wages. Do not use current assignments, baseSalarySnapshot or current membership to recalculate.
- Both exports accept optional branch/department filters with same validation as PDFs, if adding filters to existing methods preserve old call compatibility.

- [x] Write failing service/repository tests for locked-only PDF projection, HR/OWNER vs three denied roles, branch/department mismatch, positive/deduction/net arithmetic and cancelled-history nonduplication. Capture RED before implementation.
- [x] Write focused SS test: contractual30000, frozen earned base12000, contribution600 yields12000; endflagfalse/base4000/contribution200 remains exported; explicitbase0 never fallback; NULLlegacy frozenbase8000 yields8000 independently of changed live assignment. Run RED then implement factual projection GREEN.
- [x] Write bank-export tests: snapshotold account remains after live-primary edit; paid/cash/zero not exported; cancelledold+newprepared uses only new; missing preparation/phone-only no bank produces actionable error, no partial CSV. Use synthetic encryption fixture, never print full account in logs. Add actual disposable persistence check for snapshot query.
- [x] Implement pure renderers and safe controller routes. Reuse Thai font/decimal formatting; repeat headers and include consistent per-branch/grand totals after pagination. Generic dashboard summary remains available for unlocked preview.
- [x] Add report-page download controls for both PDFs and correct CSV errors using existing selected period/branch. Real browser HR and OWNER download each PDF, verify correct MIME/signature and filters, reload and repeat; deny employee/supervisor/manager direct URLs. Compare person totals with underlying locked rows and individual payslip data, not PDF-derived data.
- [x] Apply pdf skill render/verify workflow to generated PDFs including long-name/multi-page fixture; inspect rendered page images for wrapping/clipping and preserve representative screenshots/PDF evidence. Text extraction alone is insufficient visual QA.
- [x] Sequential backend typecheck + guarded full disposable DB suite; frontend unit/lint/types; focused browser. Record exact pass/skip/fail counts and practical bank/QR limits in report09.
- [x] Freeze source and hand back for fresh spec+quality review before scoped commit. No payslip reconstruction from PDF or external emailing. Task10 only follows reviewed handback.
