### Spec Compliance

- ✅ **Spec compliant — Task 3 / UC12**. ตรวจ brief, implementation report, frozen review package และ global/UC12 binding design เทียบ backend base `a551e05` / frontend base `103f0bb`; ไม่พบ requirement ที่ตกหล่นหรือ scope เพิ่มโดยไม่จำเป็น
- `backend/src/features/advance/advance.service.ts:26` บังคับ string, trim แล้วไม่ว่าง, input ยาวไม่เกิน 1000 ก่อน insert/decision; `advance.routes.ts:7` และ `advance.routes.ts:12` บังคับ request reason/rejection note ที่ API boundary; controller/runtime ส่งต่อ field ครบ (`advance.controller.ts:10`, `advance.runtime.service.ts:20`)
- `frontend/app/(dashboard)/finance/page.tsx:74` ป้องกัน whitespace/overlong ฝั่ง submit, fields มี required/maxlength ที่บรรทัด 96 และ 108; history แสดง saved reason/note และ label NULL อย่างตรงไปตรงมาที่บรรทัด 103–104 โดยไม่มีการแต่งเหตุผลย้อนหลัง
- `backend/drizzle/0006_advance_reason.sql:1` เพิ่มเพียง nullable `advance_requests.reason text`; ไม่มี default, backfill, UPDATE หรือ destructive statement. เปรียบเทียบ semantic JSON ของ 0005→0006 โดยอิสระ: ต่างเฉพาะ snapshot id/prevId และ `public.advance_requests.columns.reason` (`0006_snapshot.json:46`), predecessor ตรง, คง 39 tables / 25 enums. Journal ต่อ idx6/tag0006 (`_journal.json:47`); DBML/ORM/design ใน package ตรงกัน
- หลักฐาน schema-owner ก่อน/หลังตรงกันทั้ง 48 advances, 1015 locked payroll records, 11927 locked items (`18-uc12-advance-reasons-evidence/schema-owner-before.log:1`, `schema-owner-after.log:1`). Final persistence evidence ยืนยัน original advances 48 แถว fingerprint เดิมและ reason NULL ทั้งหมด (`browser-persistence-final.log:4`). Root ยืนยัน actual catalog 39/25/91 ผ่าน read-only query (`schema-owner-catalog-confirmed.log:1`)
- Eligibility/exact-money/pending/scope/lock/transaction paths ใน diff คงเดิม; `advance.integration.test.ts:44` ตรวจ invalid rejection ไม่เปลี่ยน request/audit, `:53` ตรวจ duplicate/concurrent original reason, `:60` ตรวจ legacy NULL, `:65` ตรวจ forged employee/read, `:68` และ `:73` ตรวจ worked-day/half-base/net-pay boundaries. ไม่มี loan implementation delta; browser regression loan เดิมผ่าน (`browser-green.log:13`)
- ⚠️ **ขอบเขตผลตรวจ:** เป็น task gate ของ UC12 เท่านั้น; full 20-use-case actor UAT, final broad review และ integration เป็นงาน root ถัดไปตาม binding design ไม่ถือว่าผ่านจาก browser 7 รายการนี้ การ apply migration จริงอ้างอิงหลักฐาน schema-owner/root ไม่ได้ apply หรือ query ฐานข้อมูลซ้ำโดย reviewer

### Strengths

- `backend/src/features/advance/advance.controller.ts:8` เรียก pure feature mapper ทั้ง single/list; `advance.mapper.ts:2` ใช้ explicit public allowlist จึงไม่เผย actor/time/internal metadata. ตรวจ unchanged `shared/operation-mapper.ts:3` เพื่อยืนยัน snake_case/decimal-string IDs ยังคงผ่าน shared envelope
- `backend/src/features/advance/advance.repository.ts:28` ส่ง insert command เข้า Drizzle โดยตรง จึง persist reason จริง; decision update คง reason เดิมและ pending guard (`:40`). เป็น focused check เพิ่มจาก package เพราะ insert contract เปลี่ยนแต่ implementation body อยู่นอก hunk
- Real PostgreSQL/API/browser tests ตรวจผลลัพธ์และข้อมูลจริง รวม audit rollback, persisted employee/finance reload และ zero POST สำหรับ client validation (`advance.integration.test.ts:42`, `frontend/e2e/advance-reasons.e2e.ts:31`, `:47`, `:56`). Tests ไม่ได้พึ่ง mock เพียงอย่างเดียว
- แยกหลักฐาน main browser **7 passed** (`browser-green.log:17`) กับ final assertion-only **2 passed** (`browser-final.log:11`) ถูกต้อง; manifest สองชุดต่างกันเฉพาะ `frontend/e2e/advance-reasons.e2e.ts`. ไม่ได้อ้างว่า 7 tests ถูก rerun หลังเพิ่ม overlong-note assertion

### Issues

#### Critical (Must Fix)

- ไม่พบ

#### Important (Should Fix)

- ไม่พบ

#### Minor (Nice to Have)

- **Existing dependency warning, non-blocking:** `docs/superpowers/reports/18-uc12-advance-reasons-evidence/database-green.log:42` มี `pg` warning ว่าเรียก query ซ้อนบน active client จะไม่รองรับใน pg9. ผล UC12 ยังผ่าน แต่ output ไม่ pristine และเป็น compatibility debt. ติดตาม query sequencing ของ payroll projection แยกก่อน upgrade pg; ไม่ควรปิด warning หรือขยาย Task 3 ไป refactor projection โดยไม่มี regression scope. Delta นี้ไม่ได้เปลี่ยน projection implementation

### Checks and evidence

- อ่าน frozen package ครั้งเดียวแบบแบ่งช่วง; focused checks เพิ่มเฉพาะความเสี่ยง changed insert contract, public mapper/envelope, changed service call sites และ omitted generated snapshot. ไม่พบ caller ที่ยังส่ง new-write contract เก่าใน backend/frontend source/tests ที่เกี่ยวข้อง
- ตรวจ SHA256 ของ final manifest ทั้ง 20 changed files และ unchanged browser dependencies ตรงกับ working tree; เปรียบเทียบ browser manifest แยก main7/final2. ไม่มี source/index/HEAD mutation และไม่ rerun test suite
- อ่าน RED/failure/GREEN logs ที่เก็บไว้: service RED 6 pass/12 fail; API RED 6 pass/5 fail; browser RED ขาด reason field. Invalid-test-helper และ migration-count assertion failures ถูกเก็บไว้และแก้เฉพาะ test contract ตาม report
- ตรวจ existing GREEN evidence: service/API 29 pass; focused realDB 7 pass; full migratedDB 598 pass/0 skip/0 fail/123 files (`backend-full-database.log:4`); frontend 55 pass (`frontend-unit.log:96`); types/lint/build logs ผ่าน โดย build สร้าง 22 static pages (`frontend-build.log:14`). Final browser 2-run ใช้ workers1/retries0 และ actual Bangkok date 2026-10-26 (`browser-final.log:1`, `:6`)

### Assessment

**Task quality: Approved.** ไม่พบ UC12 defect ที่ต้องแก้ก่อน checkpoint; การเปลี่ยนเป็น vertical minimal delta, คง history/authorization/finance policy และมี persistence/rollback/browser evidence รองรับ. Minor warning เป็น debt ของ path เดิมและไม่กีดขวาง Task 3
