# Task11 review — spec compliance and quality

## Spec Compliance

- ✅ Spec compliant สำหรับขอบเขต Task11 และ verification stack ค่า default: เพิ่ม actual UI submissions, reload/persistence และ direct authorization checks โดยไม่แก้ runtime/schema/migrations/dependencies; งาน whole-branch review, commits และปิด automation ยังเป็น gate ของ root ตาม brief ไม่ใช่งานที่รายงานนี้รับรองว่าจบแล้ว
- ✅ Login ใช้ทั้งห้า single-role actors พร้อม reload, logout, copied-token rejection และ independent session (`frontend/e2e/auth-session.e2e.ts:4`); HR/OWNER/manager ทำ employee CRUD ผ่าน UI พร้อม persisted contact/status และ assignment-history observer (`frontend/e2e/employee-management.e2e.ts:5`, `:57`, `:71`); concrete manager cross-branch writes และ account/bank escalation ถูกปฏิเสธ (`frontend/e2e/actor-write-denials.e2e.ts:14`).
- ✅ HR และ OWNER สร้างงวด/ส่งรายการปรับ/อนุมัติ/ล็อกผ่าน UI โดย pending lock ถูกกัน และ repeated previews ไม่เพิ่มรายการซ้ำ (`frontend/e2e/current-adjustments.e2e.ts:14`, `:39`, `:65`, `:79`). Employee ส่ง leave ของตนจน persisted pending และ advance จน HR อนุมัติ/employee reload (`frontend/e2e/employee-self-service.e2e.ts:57`, `:67`, `:94`). Actor matrix แยก 38 rows และระบุ supporting guards อย่างตรงไปตรงมา (`docs/superpowers/use-case-actor-matrix.md:5`, `:43`).
- ✅ เพิ่มการดาวน์โหลด frozen bank/earned-base SS CSV จาก UI ของทั้ง HR/OWNER หลังเปลี่ยน live bank details (`frontend/e2e/payable-reports.e2e.ts:24`); bootstrap สร้าง unique payment/lifecycle/report fixtures ก่อน browser module load และ wrapper คืน browser exit status เดิม (`backend/scripts/full-uat-fixtures.ts:18`, `scripts/full-uat.sh:11`, `:33`).
- ✅ BP/manual ใช้ numbered natural-language steps แยกบทบาท อธิบาย web/manual operations ในแต่ละขั้น, HR grant สำหรับบัญชี, manual payout แล้วจึง app confirmation, salary-payable creditor summary และ locked-value adjustment (`docs/superpowers/use-case-delivery-handover.md:7`, `:36`, `:46`). ไม่มีการแก้ academic report หรือ root gitlinks ใน review package.
- ⚠️ Task gate นี้ไม่ได้รับรองทั้ง branch หรือ real-world actor UAT, bank execution/acceptance และ external inbox delivery; ข้อจำกัดเหล่านี้ถูกระบุชัด (`docs/superpowers/reports/11-full-use-case-uat.md:55`, `:57`, `:74`). Existing untouched approval/eligibility/runtime behavior รับหลักฐานจาก focused Tasks2–10 และ controller's full-suite checks ไม่ได้ตรวจ source ทั้ง repository ซ้ำ.

## Strengths

- Source freeze ตรงกันทั้ง 21 files ก่อน/หลัง full browser invocation; summary มี total/expected 49, unexpected/flaky/skipped 0, errors empty และ stdout ลงท้าย `49 passed (10.9m)` จริง (`docs/superpowers/reports/full-uat-evidence/source-freeze-before-full.json:1`, `docs/superpowers/reports/full-uat-evidence/20261025T073506Z-48849/full-browser-summary.json:1`, `docs/superpowers/reports/full-uat-evidence/20261025T073506Z-48849/browser.log:1`). ไม่มีการนำ targeted runs มารวมเป็น full-green result.
- Successful-login pacing อยู่เฉพาะ test harness ใช้ timestamp ร่วมกันแม้เปลี่ยน worker และไม่มี blanket retry หรือ production limiter change (`frontend/e2e/login-pacing.ts:3`, `:5`). Wrapper รักษา log/evidence ต่อ run และ failure exit status (`scripts/full-uat.sh:7`, `:31`).
- Report แยก failed targeted runs และ wrapper-edit exit127 อย่างเปิดเผย ไม่อ้างว่าการกู้ HTML คือ original stdout (`docs/superpowers/reports/11-full-use-case-uat.md:43`). Readback ยืนยัน locked totals, retained cancellations และ attachment/stored PDF hash equality; report contact sheet แสดง all/filtered/reload pages โดยไม่เห็น clipping/overlap ในขนาดภาพรวม (`docs/superpowers/reports/full-uat-evidence/20261025T073506Z-48849/readback-verification.json:1`, `docs/superpowers/reports/full-uat-evidence/20261025T073506Z-48849/visual-reports/all-downloaded-pages-contact.png`).

## Issues

### Critical (Must Fix)

- ไม่มี.

### Important (Should Fix)

- **[P2] รักษา configured verification HTTP port เมื่อเรียก browser wrapper — `scripts/full-uat.sh:5`, `:27`.** `scripts/verify.sh:4` ยังคงรองรับ `VERIFY_HTTP_PORT` และใช้ค่านั้นเปิด stack แต่ wrapper บังคับ `HTTP_PORT=18083` และ `E2E_BASE_URL=http://localhost:18083`. ดังนั้น `VERIFY_HTTP_PORT=18084 sh scripts/verify.sh` เปิดเว็บที่ 18084 แล้ว browser ไป 18083 ทำให้ verification ที่เคยรองรับ fail หรือทดสอบ stale stack ที่เปิดค้างผิดตัว แม้ fixtures เพิ่งสร้างใน compose project ปัจจุบัน. ให้ wrapper สืบทอด `HTTP_PORT`/`VERIFY_HTTP_PORT` โดยมี 18083 เป็น default แล้วสร้าง base URL จากค่าที่เลือก; เพิ่ม focused assertion สำหรับ non-default HTTP port โดยไม่ต้องรัน full suite ซ้ำเพื่อพิสูจน์การส่งต่อค่า.

### Minor (Nice to Have)

- **UC15 ยังไม่มี same-request final employee reload — `frontend/e2e/employee-self-service.e2e.ts:70`, `:74`; `docs/superpowers/use-case-actor-matrix.md:43`.** Own employee UI request ถูกตรวจถึง pending แล้ว test ไป finance; `approval.e2e.ts:36` อนุมัติคนละ request ที่ admin สร้าง. Submission/persistence และ approval boundaries มีหลักฐานแล้วตาม task contract และ matrix ระบุข้อเท็จจริงนี้ถูกต้อง จึงไม่ใช่ core actor coverage failure. การให้ approver ตัดสิน `leave.id` แล้ว employee reload เห็น approved จะเชื่อม user journey ได้ครบขึ้น โดยเฉพาะถ้าจะใช้ baseline audit's end-to-end checklist เป็น acceptance เพิ่มเติม.
- **Existing color environment warning ทำให้ log ยังไม่สะอาด — `docs/superpowers/reports/full-uat-evidence/20261025T073506Z-48849/browser.log:5`.** `NO_COLOR` ถูก ignore เพราะมี `FORCE_COLOR`; ไม่กระทบ assertions หรือผล 49 passes และไม่มีหลักฐานว่าเป็น regression ของ Task11. ควรเลือกตั้งเพียงตัวเดียวใน harness environment เมื่อสะดวก.

## Checks and scope

- อ่าน frozen review package เป็นแหล่ง diff เพียงชุดเดียว; บาง tool output ถูกตัด จึงอ่านเฉพาะช่วงที่ไม่แสดง ไม่เรียก git/reconstruct diff และไม่ crawl repository.
- Named focused check: ความเสี่ยง HTTP-port contract เปลี่ยนเมื่อ `verify.sh` delegate ไป wrapper — อ่าน `scripts/verify.sh:4`, `:27` เทียบ wrapper exports/base URL; ไม่ต้องเริ่ม stack เพื่อยืนยันค่าคงที่นี้.
- Named focused check: UC15 pending/approved journey อาจเป็นหลักฐานคนละ request — อ่าน remainder ของ `approval.e2e.ts` เพราะ diff hunk จบกลาง test; ยืนยัน admin-created request IDs และ UI supervisor/manager decisions พร้อม quotas/history (`frontend/e2e/approval.e2e.ts:36`, `:55`, `:78`).
- ตรวจ existing full-run summary, log tail, before/after source-hash equality, safe DB readback และ report-page contact sheet. ไม่ rerun tests/suites; backend538/0skip/0fail, frontend52/173 และ lint/types/build ใช้ actual completed runs ที่ controller ตรวจแล้ว. ไม่แก้ source/index/HEAD; เขียนเฉพาะ review report นี้.

## Assessment

**Spec verdict: Approved สำหรับ task scope ค่า default.**

**Code quality verdict: Needs fixes.**

**Reasoning:** Actual UI actor/persistence/denial coverage และ retained evidence มีน้ำหนักรองรับผล final49; ไม่มี Critical finding หรือ runtime payroll defect ใน task diff. ต้องรักษา existing configurable verification HTTP port ก่อนรับ wrapper เป็น entrypoint ทดแทน เพราะขณะนี้ non-default invocation สามารถชี้ browser ผิด stack.

## Fix round1 — scoped re-review

- **Spec verdict: ✅ Approved. Code quality verdict: ✅ Approved. Open Important/P2: addressed.** `scripts/full-uat.sh:5` สืบทอด `HTTP_PORT` ก่อน fallback ไป `VERIFY_HTTP_PORT`/18083 และ `:29` สร้าง browser URL จากค่าที่เลือกจริง; PostgreSQL/mail settings ถูกส่งต่อด้วย จึงแก้ stack/browser mismatch โดยไม่เปลี่ยน bootstrap, evidence naming หรือ failure exit propagation.
- **Focused regression coverage เพียงพอ:** `scripts/full-uat.test.ts:7` ครอบคลุม default, `verify.sh` custom ports, standalone VERIFY overrides, inherited-port precedence และ browser exit17. ทดสอบ actual copied wrappers ใน isolated temporary directories แล้ว stub เฉพาะ external Docker/Bun (`:19`, `:20`, `:25`); assertions ตรวจ compose calls ทุกครั้งและ browser invocation เดียว (`:28`, `:29`, `:32`). ไม่มี runtime/schema/dependency change หรือ Important regression ใหม่ใน fix diff.
- **Existing evidence ตรวจแล้ว:** `wrapper-config-fix1-red-confirmed.log` ลงท้าย 2pass/3fail/20assertions; `wrapper-config-fix1-green.log:10` ลงท้าย 5pass/0fail/33assertions. Source manifests เปรียบเทียบได้ 22files: 20files เดิมไม่เปลี่ยน, แก้เฉพาะ wrapper และเพิ่ม root regression test หนึ่งไฟล์ (`docs/superpowers/reports/full-uat-evidence/source-freeze-after-config-fix1.json:1`). Shell syntax checks exit0 ตาม controller evidence; reviewer ไม่ rerun checks/suites.
- **Evidence timing ถูกต้อง:** Full49 และ backend/frontend/build checks เป็นผลก่อน config-only repair ตามที่ updated handback/report ระบุ ไม่ใช้ historical21file freeze อ้างว่าตรง current source. หลัง repair ใช้ focused wrapper tests และ new22file freeze; ไม่ต้อง rerun browser หรือ package suites เพื่อยืนยัน port wiring นี้.
- **Scope:** อ่านเฉพาะ frozen fix1 diff, updated handback/report และ named focused evidence; ไม่เปิด review ทั้ง task/branch ซ้ำ ไม่แก้ source/index/HEAD. Minor same-request leave approval/reload และ existing color-warning ยังคงเป็น final-review ledger items; ไม่ขัดขวาง Task11 approval.
