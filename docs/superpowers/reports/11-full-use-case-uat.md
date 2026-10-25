# Task11 — Full use-case actor UAT

สถานะ: **Task11 implementation/verification พร้อม fresh review** — final complete browser invocation ผ่าน **49/49,0fail,0skip,10.9min,exit0** วันที่25October2026; ต้องผ่าน fresh Task11 review และ whole-branch review โดย root แยกกัน ยังไม่อ้างปิดโครงการทั้งหมด

## สิ่งที่เปลี่ยน

- เพิ่ม shared successful-login pacing ที่ทุก helper, API login setup และ independent browser context เรียกใช้ ระยะ 6200ms ใช้ timestamp file ร่วมกันแม้ Playwright เปลี่ยน worker ไม่มี auth response retry ไม่แก้ nginx, authentication policy หรือ production limiter workers1/retries0 คงเดิม
- เพิ่ม `scripts/full-uat.sh` เป็น browser entrypoint ที่ `scripts/verify.sh` เรียก สร้าง unique disposable Task7/8/9/10 fixtures ก่อน Playwright module load พร้อม explicit paths, scope fixture และ evidence directory ต่อ run ไม่ reuse immutable payment/payslip history ไม่ reset/delete facts และไม่ skip เมื่อ fixture ขาด
- เติม named single-role UI coverage: Login/session/logout/replay ทั้ง5roles; CRUD employee โดย HR/OWNER/manager; HR/OWNER เปิดงวดและล็อกจริงร่วมกับ adjustment UI; employee ส่งลาและ advance ของตนจริง; concrete other-branch create/edit/terminate และ bank/account-role escalation denial
- ขยาย actual HR/OWNER report CSV downloads ตรวจ original prepared bank destination หลัง live edit พร้อม exact earned-base SS values; คง assertion export ของ original fresh-organization flow
- แยก evidence ของทุก run ออกจาก focused Task2–10 artifacts เดิม ไม่แก้ academic DOCX/builders ไม่เปลี่ยน schema/migration, runtime API/UI, payroll rules, external systems หรือ production data

## Environment และคำสั่ง

ใช้ compose project `haris-payroll-verify` เท่านั้น: web18083, PostgreSQL16 port55440, Mailpit18025 SMTPภายใน `mailpit:1025`; synthetic `example.test` recipients ไม่มี external SMTP, bank API หรือเงินจริง การรัน DB-mutating suites เป็นลำดับไม่ทับกัน Root ไม่ได้รัน DB/browser ระหว่างงานนี้

Public release accounts: `employee`/EMPLOYEE, `supervisor`/SUPERVISOR, `branch_manager`/BRANCH_MANAGER, `hr`/HR, `admin`/OWNER; password `password` เป็น fixtureสาธารณะเท่านั้น ตรวจ grants singleton ผ่าน `/auth/me` ไม่พ่วง OWNER ให้ scoped actor Synthetic linked accounts ใช้ generated temporary password ใน memory ของ test; ไม่บันทึก credentials นั้นในรายงาน

คำสั่งจาก repository root:

```sh
# Complete reproducible environment/check/browser entrypoint:
sh scripts/verify.sh
# Once the disposable stack and release fixture are ready, fresh browser run only:
sh scripts/full-uat.sh
```

`verify.sh` สร้าง/เปิด stack, seed release twice เพื่อเช็ก idempotency, backend types/guardedDB, frontend unit/lint/types แล้วเรียก fresh browser wrapper Runtime build ตรวจแยกด้วย frontend `bun run build` การทดสอบ build กับ browser ใช้ source revision เดียวกัน ไม่มี runtime change เพิ่มหลัง build

## Verification record

| Check | Command / invocation | Result | Evidence |
|---|---|---|---|
| Pacing RED → GREEN | frontend `bun test e2e/login-pacing.test.ts` | 0pass/1fail → 1pass/0fail; second caller must wait, timestamp survives helper callers | `full-uat-evidence/login-pacing-{red,green}.log` |
| Backend types + complete migrated DB | compose backend `RELEASE_DISPOSABLE_DB=1`, `TEST_DATABASE_URL=$DATABASE_URL`, release twice, `bun run typecheck`, `bun run test:db` | 538pass / 0skip / 0fail,119files | `full-uat-evidence/backend-full-first.log` |
| Frontend complete unit | frontend `bun test` | 52pass / 0fail,18files,173assertions | `full-uat-evidence/frontend-unit-first.log` |
| Frontend lint/types/build | `bun run lint`; `bun run node_modules/typescript/bin/tsc --noEmit`; `bun run build` | exit0 | `frontend-lint-final.log`, `frontend-types-final.log`, `frontend-build-first.log` under evidence |
| Initial targeted12 | four selected E2E files | 8pass/4fail/0skip from test assumptions; wrapper tail then exited127 due operator edit | `20261025T072614Z-37063/playwright-report/`, recovered results and traces |
| Corrected targeted11 | direct denials, CRUD, adjustments, self-service files | 10pass/1fail/0skip; remaining raw DTO casing assertion | `20261025T073035Z-43400/browser.log` |
| Corrected/expanded targeted3 | grep employee own leave, original fresh journey, report downloads | 3pass/0fail/0skip,1.5min | `20261025T073257Z-48598/browser.log` |
| Final entire browser invocation | `sh scripts/full-uat.sh` (no file/grep filter) | **49pass / 0fail / 0skip,10.9min,exit0** | `20261025T073506Z-48849/browser.log` |

Targeted selection12→11 is deliberate: the second targeted pass excludes the5 previously green auth cases and adds4 explicit write-denial cases (12−5+4=11). None were removed from the final default suite. The later3case run verifies the corrected self-service contract plus expanded frozenCSV checks. No targeted results are added together to claim a full pass. Final complete default invocation alone determines full-UAT count.

## Honest failed-run record

Initial test failures were: manager attempted assignment-admin read after valid termination (HR/OWNER-only endpoint); inherited manager DTO mask assertion wrongly applied to HR/OWNER; synthetic leave-type code used disallowed hyphen/lowercase. The second run exposed a further test-only expectation of camelCase/number IDs against public snake_case/string DTOs (frontend performs conversion). Fixed fixtures/assertions to actual contracts and observed GREEN. No application defect was demonstrated and no production fix was introduced.

During initial targeted run the implementer edited the executing wrapper to add a scope-fixture environment variable. Shell file-position drift re-read a partial command at the end and overwrote `browser.log`. Original HTML/trace/screenshots survived. `recovered-report.json` and `recovered-browser-results.txt` explicitly identify reconstruction from HTML, not original stdout. The failing `browser.log` (exit127) is retained. Source/wrapper are frozen during all subsequent invocations. This execution mistake is disclosed separately from product test outcomes.

## Actor evidence and limits

See [actor matrix](../use-case-actor-matrix.md) for each required actor/UI mutation, reload/persistence assertion, direct denial and evidence. [Role-based BP/manual](../use-case-delivery-handover.md) explains web operations and external manual steps inside numbered steps; [schema summary](../use-case-schema-summary.md) explains focused ERD without replacing the complete DBML/Drizzle model. Existing original [audit](../../use-case-delivery-audit-2026-10-25.md) baseline is preserved below its dated update.

Positive advance uses actual Bangkok business date2026-10-25, currentmonth draft payroll, schedule/configuration and all25 attendance days through request date, salary30000 and request100.01. It does not fake clock/date/20day/half-salary rules. Before20 a future invocation asserts legitimate eligibility denial and records `positiveAdvance:false`; that run must not be presented as evidence of positive approval. This delivery's positive approval is proved by the dated final run.

No claim of real bank transfer, bank-file acceptance/certification, production SMTP delivery or real-user UAT is made. Mailpit proves local receipt and exact PDF attachment bytes separately from SMTP acceptance. QR decode proves recipient/amount/checksum; scanning/generation never proves paid. Cancelling preparation does not reverse external transfer or revoke downloaded QR/CSV. Salary-creditor PDF means salary payable, not employee debt. Paid rows and locked fiscal facts remain immutable; planned corrections use recorded workflows.

## Final evidence readback

Final run **20261025T073506Z-48849** completed all49cases in one invocation with no retry or skip. [Full log](full-uat-evidence/20261025T073506Z-48849/browser.log), [structured summary](full-uat-evidence/20261025T073506Z-48849/full-browser-summary.json) and [HTML report](full-uat-evidence/20261025T073506Z-48849/playwright-report/index.html) agree:49expected/0unexpected/0flaky/0skipped; errors[]. The sole test process exited0 before any readback query. No application/test/wrapper file changed during it:21source hashes match [before](full-uat-evidence/source-freeze-before-full.json) and [after](full-uat-evidence/20261025T073506Z-48849/source-freeze-after-full.json).

- [Safe raw DB readback](full-uat-evidence/20261025T073506Z-48849/locked-db-readback.json) and [verification](full-uat-evidence/20261025T073506Z-48849/readback-verification.json): all4freshfixture periods locked;9base/linked accounts have exactly one named role; no bank ciphertext/full-account fields included. Report period511 earnings33000.00/deductions1200.00/net31800.00; filtered8000/400/7600. Prepared export kept bank004/last4=1234 after live edit006/last4=9999.
- Payout lifecycle period510: HR confirms100.01 and cancels50.02; after HR reload paid100.01/outstanding75.02. OWNER reprepares/confirms50.02 and cancels25.00; final paid150.03/outstanding25.00 against payable175.03,2paid plus2cancelled historical rows retained. This is a synthetic manual acknowledgement, not actual cash/bank proof.
- Positive final-run self-service: employee1012,leave240,advance77 amount100.01, actual Bangkok2026-10-25/25worked days; own UI submission/reload/HRapproval/employee reload plus otherperson and own-decision denials all passed.
- [Mail/PDF proof](full-uat-evidence/20261025T073506Z-48849/payslips/delivery-proof.json): HR slip49/attempt52 and OWNER slip50/attempt53 both SMTPaccepted and localInboxReceived; each original/reload/Mailpitattachment SHA256 matches stored DB hash. Scoped own slips51/52 also download correctly. These4records total19100.65/950.00/18150.65, paymentcount0, so a slip does not imply payment. Runtime target [sanitized check](full-uat-evidence/20261025T073506Z-48849/smtp-target.json) confirms internal Mailpit1025/securefalse/credentialsUnset.
- Actual saved PDFs:12HR/OWNER all/filtered/reload reports +1individual report-fixture slip +12payslip/download/attachment variants = **25PDF artifacts,33rendered pages**. [Report content checks](full-uat-evidence/20261025T073506Z-48849/report-pdf-verification.json) and [slip checks](full-uat-evidence/20261025T073506Z-48849/payslip-pdf-verification.json) verify exact amounts, employee rows and filters. All report pages inspected as [contact sheet](full-uat-evidence/20261025T073506Z-48849/visual-reports/all-downloaded-pages-contact.png), with readable creditor all/filtered and HR/OWNER slip pages; Thai names, legitimate code wrapping, fiscal columns and disclaimers remain readable with no clipping/overlap. Duplicate slip variants are byte-identical where expected. [Long-name regression](full-uat-evidence/20261025T073506Z-48849/long-pdf-verification.json) reuses reviewed Task9 artifacts (not a newly created browser fixture):70employees,salary9pages/creditor10pages, allrows/repeatedheaders/totals verified and allpage contacts +first/final pages inspected.
- Displayed desktop/mobile QR pixels independently decoded using jsQR; recipient/amount123.45 and maximum9999999999.99 plus CRC checked without production encoder.6prepared/0paid and2zero rows remain distinct. QR/mobile, payment confirmation, actor CRUD, advance, report and slip screenshots are retained in this run directory.

## Review handback

No unresolved product defect was demonstrated in Task11; failed runs were harness/fixture/assertion issues listed above. Only the existing harmless Playwright NO_COLOR/FORCE_COLOR development warning remains. Backend538, frontend52 and production build were completed before the final browser run; later changes were test-only, so no fictitious repeated full-backend/build claim is made. No schema/migration/runtime API/UI changes were introduced in this task.

Source and task evidence are frozen for root's independent Task11 review. Root owns subsequent whole-branch review, local commits, whole-project completion and heartbeat shutdown. No commit, push, merge, deploy, root gitlink change or automation update was performed by this implementer.

## Task11 fix round1/5 — configurable verification ports

Root's fresh review identified one Important/P2 finding: `VERIFY_HTTP_PORT=18084 sh scripts/verify.sh` starts the verification stack on18084, but the new browser wrapper overwrote inherited HTTP/PG/mail settings and always targeted18083. This could fail or test a different local stack. Confirmed by running the real wrappers in an isolated temporary repository with Docker/Bun external commands stubbed; no database, browser or network was used for this repair.

Minimal repair changes only `scripts/full-uat.sh`: select `HTTP_PORT` from inherited value, then `VERIFY_HTTP_PORT`, then18083; PostgreSQL follows inherited `POSTGRES_PORT`, then `VERIFY_POSTGRES_PORT`, then55440. Preserve `VERIFY_MAIL_PORT` or default18025. Derive `E2E_BASE_URL` from selectedHTTPport. Existing fixture/bootstrap commands, production configs, application behavior and browser assertions stay unchanged.

Covering file **`scripts/full-uat.test.ts`** exercises actual shell execution, not source-text matching. Five scenarios cover default18083, actual `verify.sh` override18084 with matching stack/browser settings, standalone VERIFY overrides, inheritedHTTP/PG precedence and preservation of mailport, and propagation of browser exit17 through `verify.sh`. Stub binaries exist only in temporary directories and cannot call real Docker/Bun. Each test removes its own temporary evidence and leaves the prior full-UAT artifacts untouched.

Exact commands from repository root:

```sh
bun test scripts/full-uat.test.ts > docs/superpowers/reports/full-uat-evidence/wrapper-config-fix1-red-confirmed.log 2>&1
# Observed before wrapper change: 2pass / 3fail,20assertions; override URLs incorrectly18083.
bun test scripts/full-uat.test.ts > docs/superpowers/reports/full-uat-evidence/wrapper-config-fix1-green.log 2>&1
# After repair: 5pass / 0fail,33assertions,exit0,1.434s.
sh -n scripts/full-uat.sh
sh -n scripts/verify.sh
# Both syntax checks exit0.
```

The first harness draft also expected a resolved mail default from `verify.sh`'s early stub compose call, where that variable is unset because Compose normally supplies its default. The exit-propagation scenario now sets its mailport explicitly; the first 1pass/4fail log remains as `wrapper-config-fix1-red.log`. The confirmed RED is2pass/3fail from the actual port defect alone. No failure or prior log was erased.

**Evidence timing:** full browser49pass/0fail/0skip and backend538/frontend52/build above were run **before this config-only repair**, on default18083. They were not rerun after the repair; no application/schema/production configuration changed and the focused real-shell tests prove default/custom port wiring. The historical21file manifest remains unchanged as evidence of that browser invocation, and is **not** claimed to equal current source. [New22file freeze](full-uat-evidence/source-freeze-after-config-fix1.json) and [comparison](full-uat-evidence/config-fix1-freeze-verification.json) show20previous files unchanged, only wrapper changed, plus one new root test. [Exact wrapper diff](full-uat-evidence/wrapper-config-fix1.diff) is retained.

Source is frozen again for scoped re-review of this one finding. Minor same-request leave approved/reload coverage and the color-environment warning remain deferred to root's separate final review; neither was changed in this fix round. No commits/gitlinks/automation or external actions performed.
