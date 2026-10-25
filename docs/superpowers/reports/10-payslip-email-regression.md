# Task 10 — Payslip/email regression

สถานะ: implementation พร้อม fresh review, 25 October 2026. ทดสอบเฉพาะ payslip/email gate; full actor/use-case UAT เป็น Task 11.

## ผลและ minimal repair

HR (`hr`, grant HR เท่านั้น) และ OWNER (`admin`, grant OWNER เท่านั้น) ใช้แบบฟอร์ม **ออกหรือเปิดสลิป**, **ดาวน์โหลด PDF**, **ส่งสลิป** จริงได้ ทั้งคู่เปิดใหม่หลัง reload ได้ slip ID เดิม, financial totals เดิม, PDF bytes เดิม และ terminal delivery attempt เดิม. SMTP acceptance และ local inbox receipt ตรวจแยกกัน พร้อม attachment ตรงกับ stored/downloaded PDF ทุก byte.

พบ defect จริง: standalone SUPERVISOR/BRANCH_MANAGER ที่เชื่อมกับพนักงานถูก `DashboardAccessGuard` กันออกจาก `/payslips`; `route-access.ts` ไม่รวมสอง role นี้ แม้ backend `ownOrAdmin` และหน้า `PayslipsPage` รองรับ own-only read อยู่แล้ว. Shared caller อีกจุดคือ sidebar navigation ใช้ policy เดียวกัน. Root อนุมัติ scope extension เฉพาะ route policy/test นี้.

แก้ production เพียงหนึ่งบรรทัด: `/payslips` ใช้ `allRoles` ที่มีอยู่แล้ว. เมื่อไม่มี HR/OWNER หน้าเดิมยังใช้ `/mine` และไม่มี generate/send controls. Backend authorization คงเดิม. ไม่เปลี่ยน schema, migration, API contract, mail provider/dependency, payroll facts หรือ delivery history.

## Verification

| Check | คำสั่งจาก package directory | ผล |
|---|---|---|
| Baseline ก่อนแก้ | backend `bun test src/features/payslip/payslip.service.test.ts src/features/payslip/payslip.routes.test.ts src/features/payslip/payslip.document.test.ts` | 9 pass / 0 fail |
| Concrete UI RED | frontend focused browser, standalone supervisor own-slip navigation | HR/OWNER case pass, scoped-own case fail; `RED-supervisor-own-slip-denied.png`, `browser-RED.log` |
| Unit RED → GREEN | frontend `bun test lib/auth/route-access.test.ts` | 5 pass / 1 fail → 6 pass / 0 fail |
| Final actual browser | frontend `E2E_BASE_URL=http://localhost:18083 bun run test:e2e e2e/payslip-delivery.e2e.ts` | **2 pass / 0 fail**, 22.0s |
| Full frontend unit | frontend `bun test` | **51 pass / 0 fail**, 17 files, 172 assertions |
| Frontend required checks | frontend `bun run lint`; `bun run node_modules/typescript/bin/tsc --noEmit` | exit 0 ทั้งคู่ |
| Focused backend/storage | backend `bun test src/features/payslip/payslip.service.test.ts src/features/payslip/payslip.routes.test.ts src/features/payslip/payslip.document.test.ts src/core/storage/document-storage.test.ts` | **10 pass / 0 fail**, 4 files, 32 assertions |
| Backend types | backend `bun run typecheck` | exit 0 |
| Stored facts/files/mail | safe disposable SQL snapshot + local Mailpit readback + SHA256 + bundled PDF text reader | 4 locked records, 4 stored slips, all frozen amounts/item values/hash checks pass |

Browser harness development also exposed three assertion/setup mistakes, corrected before the product repair: Chromium exposed an empty response body for a download (compare saved file with an independent authenticated GET instead), CSV fields were quoted, and auth linkage is `account.employee.id`. These were not production RED evidence. Only the scoped route-policy failure prompted a production edit. Playwright reports a harmless NO_COLOR/FORCE_COLOR warning.

Existing focused service tests exercise SMTP failure as a separate failed attempt, retained earlier attempts, stale pending recovery, rejection of active/terminal recovery, and employee recovery denial. Storage test covers replacement/tampering/traversal. No external failure simulation or production protection changes were needed.

## Actor and persistence evidence

Disposable compose project `haris-payroll-verify`: web18083, PostgreSQL55440, Mailpit18025. Before any send, runtime target was verified as `mailpit:1025`, secure=false, SMTP credentials unset, sender `payroll@example.test`; sanitized `smtp-target.json` retains this. Only synthetic `example.test` recipients were used.

Fixture: shop **1087**, period **467**, employee IDs **845–848**, records **923–926**; each linked scoped/employee account has exactly its named grant, with no OWNER/HR masking.

| Actor | UI outcome | Server-side outcome |
|---|---|---|
| HR | Generated employee A slip **41**, downloaded, sent, reloaded/reopened same slip/history/bytes | Locked totals **12100.37 / 600.00 / 11500.37** |
| OWNER | Independently generated employee B slip **42**, downloaded, sent, reloaded/reopened same slip/history/bytes | Locked totals **4000.25 / 200.00 / 3800.25** |
| Employee A and B | Visible sidebar link → own list → real own PDF download | Own metadata200; other metadata/PDF/deliveries/send403; generation and own-send403 |
| SUPERVISOR | Visible sidebar link → own slip **43** and PDF, no admin controls | Own metadata/PDF200; other metadata/PDF/deliveries/send403; generation/own-send403 |
| BRANCH_MANAGER | Visible sidebar link → own slip **44** and PDF, no admin controls | Same own-only/administrative denials |
| Anonymous | No authenticated session | Download401 |

Final run: HR attempt **48** and OWNER attempt **49** are distinct persisted `sent` rows with provider MessageIDs `payslip-attempt-48@haris-payroll.local` / `payslip-attempt-49@haris-payroll.local`. `mailpit-receipts.json` stores actual local message metadata, recipient, filename/content-type and matching attachment hashes. `delivery-proof.json` records SMTP accepted vs local inbox received separately. There are **10 local sent attempts** retained across browser development/replays; prior attempts were not replaced or deleted. Final actor screenshots show their complete retained history.

All records remain locked and **payment_count=0**: a valid payslip does not require payout and is not payment confirmation. Earnings **19100.65**, deductions **950.00**, net/outstanding **18150.65**, paid **0.00** match hand-specified fixture values, raw stored rows, payslip API and the real `salaryPayable` report projection. Base earnings **12000.00 / 4000.00 / 1000.00 / 2000.00** differ from contracted **30000.00** each; frozen adjustments **100.37 / 0.25 / 0.01 / 0.02** are retained. Social-security export matches frozen earned bases/deductions, including the nonmember snapshot case. Only immutable financial fields are compared across report/payslip; summary PDFs were never parsed to construct slips.

## Retained artifacts and repeat

[Evidence directory](payslip-email-evidence/) contains final browser/unit/type/lint logs; RED/green route-policy logs; HR/OWNER post-reload UI screenshots; employee/scoped own-only screenshots; original/reload/inbox-attachment PDFs; HR/OWNER one-page PDF renders; fixture with report projection; raw exact-decimal source/delivery snapshot; safe Mailpit receipts; `evidence-verification.json`; and SHA256 `source-freeze.json` for all four changed source/test files. HR/OWNER PDF renders and UI panels were inspected: Thai glyphs, amounts, deductions and disclaimer are readable with no clipping or overlap. All four individual PDFs have their exact base/adjustment/deduction/totals verified through PDF text reading.

Fresh fixture command (backend directory): set `RELEASE_DISPOSABLE_DB=1`, explicit `TEST_DATABASE_URL=postgresql://postgres:postgres@127.0.0.1:55440/haris_payroll`, then `bun run src/features/payslip/payslip.test-support.ts`. It creates `/tmp/haris-task10/fixture.json`; pass that file via `PAYSLIP_FIXTURE_FILE` to the focused browser command. The test defaults to the retained fixture for replay against this same disposable stack; a recreated database requires a fresh fixture. An alternate `PAYSLIP_EVIDENCE_DIR` keeps a review replay separate. Fixture setup creates synthetic facts before locking and never disables immutability. The test-only helper is not imported by application composition.

Limits: no external SMTP/deliverability claim, bank transfer, production database, push/merge/deploy or commit. No backend runtime code changed, so the already-reviewed Task 9 full 538-test DB suite was not repeated; no full browser suite/build claim is made. Mobile-specific regression and the full actor/use-case matrix remain Task 11. Source is frozen for independent spec/quality review.

## Reviewed local checkpoint

Fresh spec/quality review approved without Critical/Important findings. Local commits backend`25bdcbd` (test-only fixture), frontend`e82156f` (own-slip route policy and regression). Root read browser2/frontend51/backendfocused10 logs and inspected supervisor own-page screenshot. No backend runtime/schema, external mail, push/merge/deploy or root gitlink update. Full all-UC UAT remains Task11; environmentcolor warning tracked for its harness.
