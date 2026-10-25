# Task 9 — Locked salary-payable PDFs and factual exports

Status: **DONE_WITH_CONCERNS (execution notes only)**. Source frozen for independent spec/quality review; no unresolved product/schema defect identified. No commit, push, merge, deployment, migration or root gitlink update performed.

Base: backend `2d8f662`, frontend `3837e84`, existing `codex/use-case-delivery` branches. Existing PDFKit and NotoSansThai assets reused; no new dependency or schema changes. Accounting continues to use HR.

## Delivered behavior

- `GET /api/v1/reports/salary-summary.pdf` and `/creditor-summary.pdf` require HR/OWNER with all-branch authority and a locked period. Employee/supervisor/manager are denied before payroll lookup. Both accept period/branch/department filters, validate organizational relations and malformed queries, and use private/no-store/nosniff attachment responses with numeric-ID filenames. Generic report summary/CSV remains previewable for unlocked periods.
- The shared salary-payable application projection reads the stored payroll assignment and immutable earnings/deductions/net, groups by historical branch, and adds active prepared/paid status read-only. Cancelled history cannot multiply rows. Amount totals use the existing integer-cent decimal helpers. Zero-net employees appear but add no positive-payable count or outstanding amount. No bank details/ciphertext enter the safe projection, PDF or public JSON.
- Salary PDF includes per-employee earnings/deductions/net, branch totals and grand totals. Creditor PDF explicitly means “เงินเดือนที่ร้านต้องจ่ายให้พนักงาน”, with paid/outstanding and separate zero/unprepared/prepared/paid labels. This is salary payable, not employee loan debt. Repeated page/table headings, Thai wrapping, totals and page footers survive pagination. Both documents warn that they are not payment evidence.
- Bank CSV now uses active prepared transfer destinations frozen by payment preparation. It excludes paid, cash and zero rows. Any positive unprepared record blocks the whole selected export with a preparation action; any outstanding phone-only transfer blocks it with a QR/cancel-and-reprepare explanation. There is no silent partial CSV or live primary-bank fallback. Decryption remains inside the authorized service only.
- SS CSV retains compatible `base_salary` header but exports covered earned-base snapshot, including former membership with covered wages/contribution. Explicit zero never falls back; only NULL legacy derives from frozen base-salary items. Frozen SS deduction items supply contributions. Zero-base/zero-contribution rows are omitted; current salary/membership do not recalculate history.
- Report page adds both PDF downloads and applies selected filters to all exports. Existing download handling preserves actionable Thai errors. The existing fresh-organization flow explicitly registers transfer/phone against its existing synthetic bank account and prepares payment snapshots before retaining its original bank CSV assertion. One old adjustment selector was scoped to its form because the earlier current-adjustment feature added another amount/reason input.

## Verification

Only the authorized isolated stack was used: PostgreSQL `postgresql://postgres:postgres@localhost:55440/haris_payroll`, website `http://localhost:18083`, local Mailpit `18025`. No production DB, bank API, actual transfer or external email was used; the existing full flow sends only to local Mailpit. Production login throttling was unchanged.

| Check | Package command | Result |
|---|---|---|
| RED fiscal integration | backend: `TEST_DATABASE_URL=… bun test src/features/reports/report.payable.integration.test.ts` | 0 pass / 3 fail for absent payable projection, contractual SS base, missing QR-specific bank handling |
| RED document / pagination / route validation | backend focused tests | Missing renderer, then 27-page footer expansion; malformed query 500 instead of 422; corrected before final validation |
| Early focused fiscal GREEN | same focused integration command | 3 pass / 0 fail / 45 assertions (final full suite additionally includes historical transfer and changed replacement-bank assertions) |
| Backend final types | `bun run typecheck` | Passed |
| Final full guarded DB suite | `RELEASE_DISPOSABLE_DB=1 DATABASE_URL=… TEST_DATABASE_URL=… bun run test:db` | **538 pass / 0 skip / 0 fail / 119 files** |
| Frontend complete suite | `bun test` | **50 pass / 0 fail / 166 assertions / 17 files** |
| Frontend lint and types | `bun run lint`; `bun run node_modules/typescript/bin/tsc --noEmit` | Passed after final test selector change |
| New real report browser scenario | frontend: `E2E_BASE_URL=http://localhost:18083 PAYABLE_REPORT_EVIDENCE_DIR=../docs/superpowers/reports/payable-reports-evidence bun run test:e2e e2e/payable-reports.e2e.ts e2e/flow.e2e.ts --grep 'locked salary PDFs\|fresh organization completes'` | Report scenario **1 pass, 12.5s**; existing flow failed later at an ambiguous adjustment selector; both outcomes retained in combined log |
| Existing fresh-organization regression after selector correction | `E2E_BASE_URL=http://localhost:18083 bun run test:e2e e2e/flow.e2e.ts --grep 'fresh organization completes'` | **1 pass, 20.0s** (20.5s invocation), bank CSV assertion retained |
| PDF visual/content checks | `pdftoppm -scale-to 1300 -png …`; bundled Python pypdf checks | 70 Thai long-name employees: salary **9 pages**, creditor **10 pages**; all 70 rows and repeated headings verified; inspected all-page contact sheets plus readable first/final pages |
| UI detector / whitespace | `impeccable detect --json frontend/app/(dashboard)/reports/page.tsx`; `git diff --check` in both submodules | `[]`; passed |

Successful DB-mutating suites and browser runs were sequential. Full backend validation was followed by frontend checks, then browser checks; a final read-only DB comparison ran after browsers ended. An unnecessary extra sandboxed focused DB invocation was attempted while the browser was running and failed to connect before issuing any query; see execution notes. No successful concurrent DB writer ran.

Focused DB tests cover locked-only vs preview, HR/OWNER and three denied roles, filter mismatch, immutable-assignment transfer history, exact totals, cancelled-old/new-active join behavior, prepared replacement bank tuple after later live edit, paid/cash/zero exclusion, actionable unprepared and phone-only errors, SS 30000 contractual vs 12000/600 earned, former-member 4000/200, explicit zero, and NULL legacy 8000/400 after current salary changes.

Real HR and OWNER UI each downloaded salary and creditor PDFs for all branches, selected branch+department, and after reload: **12 actual saved PDF downloads**, correct MIME/signature and query filters. Desktop and 390px screenshots were inspected with no horizontal overflow. The direct URLs for both PDFs and both CSVs returned 403 for EMPLOYEE/SUPERVISOR/BRANCH_MANAGER. Browser also verified unprepared/phone-only CSV error recovery text. Offline content verification confirms the filtered documents contain only the two selected-branch employees and the correct 8000 / 400 / 7600 totals.

Final browser fixture **period 462**, shop **1084**, branches **864/865**, retained in `browser-fixture.json`. Independent raw stored rows total earnings **33000.00**, deductions **1200.00**, net **31800.00**. Record **912**, employee **838**, individual payslip **39** all share **12000.00 / 600.00 / 11400.00**. Comparisons use locked DB rows, frozen items and individual payslip API data; summary PDFs are never used to construct payslips. The browser prepared this fixture only after downloading its unprepared-status documents, so later prepared status naturally differs from the document-time status while fiscal amounts remain identical.

## Durable evidence

All evidence lives in [payable-reports-evidence](payable-reports-evidence/), including:

- RED/final logs: `backend-red.log`, `document-red.log`, `pagination-red.log`, `route-validation-red.log`, `browser-red.log`, `backend-full-final.log`, `backend-types-final.log`, `frontend-full-final.log`, `frontend-lint-final.log`, `frontend-types-final.log`, `browser-combined-attempt.log`, `flow-browser-final.log`.
- [Salary long-name fixture PDF](payable-reports-evidence/long-thai-salary.pdf), [creditor long-name fixture PDF](payable-reports-evidence/long-thai-creditor.pdf), contact sheets and all page PNGs. Creditor page 10 deliberately contains grand totals, not an accidental blank footer page.
- Actual HR/OWNER all/filtered/reload PDFs (`hr-*.pdf`, `admin-*.pdf`), individual payslip PDF, latest rendered browser creditor pages, desktop/mobile report screenshots.
- `locked-source-verification.json` (safe raw frozen facts), `pdf-content-verification.json` (all 12 actual PDF filters/totals and payslip comparison), `browser-fixture.json`, and `source-freeze.json` (SHA256 of every changed submodule source/test file).

To reproduce long-name artifacts: backend `REPORT_ARTIFACT_DIR=../docs/superpowers/reports/payable-reports-evidence bun test src/features/reports/report.document.test.ts`, then render the PDFs with Poppler. Browser fixture creation uses `seedReportFixture` from `report.test-support.ts` against the explicit disposable URL; set its second employee's registered PromptPay phone to the synthetic `0812345678`, save returned metadata to `/private/tmp/haris-task9-browser-fixture.json` (or set `PAYABLE_REPORT_FIXTURE_FILE`), then run the focused scenario against a fresh fixture. This setup is test-only and never imported by application composition.

## Limits and execution notes

- Bank CSV is a prepared **outstanding bank-transfer** instruction file, not bank acceptance/certification or payment execution. Mixed phone-only/bank groups may require selecting a bank-ready branch/department or using QR; no complete export is implied when blocked. Cancelling preparation/repreparing is deliberate and retains history. Already downloaded bank files cannot be revoked by this application.
- Paid/outstanding is supplemental payment state at the read query; PDF is not a lasting bank confirmation. Salary values remain locked. Schema/trigger immutability was never weakened.
- No production build or broad unrelated browser suite was run for this slice; final cross-use-case UAT remains a separate delivery gate.
- Initial localhost sandbox calls were refused; authorized escalated calls used only the disposable stack. An extra non-escalated focused DB command during final browser work failed with `ECONNREFUSED` before any query, retained as `sandbox-connection-attempt.log`; it did not change data. This is an execution-discipline concern, not a failed product test or concurrent database mutation.
- The first passing-browser attempt's `%PDF-` assertion read Playwright's empty fetch-response body even though an independent local API request returned a valid 11813-byte PDF. The scenario now checks the actual saved browser download bytes; production code was not changed for this test artifact. A test-only ES2017 bigint-literal type error was fixed by using `BigInt(...)` constructors; final types passed.
- The existing fresh flow's first final run failed **after** retained bank-export assertions because unscoped adjustment amount/reason selectors matched the earlier current-adjustment UI. The narrow form-scoped correction passed the targeted rerun. Existing Playwright NO_COLOR/FORCE_COLOR development warning remains. No unresolved runtime/schema defect identified.

Source remains frozen for root's fresh review. Task 10 must follow approved handback.

## Reviewed local checkpoint

Fresh Task9 spec/quality review approved, no Critical/Important findings. Local commits backend`1cf39ab`, frontend`8840416`; root read final logs and inspected PDF images. No schema/dependency, push/merge/deploy or root gitlink update. Color warning remains tracked for finalUAT. Browser results remain separate report scenario and corrected existing-flow pass; full-suite UAT is still pending.
