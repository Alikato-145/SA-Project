# Task 2 UC08 — independent spec and quality review

## Spec Compliance

- ✅ **Spec compliant — Task 2 scope.** ตรวจ frozen review package เทียบ task-2-brief และ UC08/global design โดยใช้ backend base `a352f25eff692bebbe69e43308f80f6aceccd76b`, frontend base `22771e7e8ad20cbbeb5578ff3353e66df92bc260` และ root ruling: `allow_exceed` ยกเว้นเฉพาะ entitlement cap; missing/frozen ยัง reject และ `quotaType=none` ไม่ต้องมี quota row.
- Guard อยู่ใน service หลัง employee lock/active-type validation และก่อน request/day/action writes ทั้ง submit และ pending edit (`backend/src/features/leave/leave.service.ts:46`, `:53`, `:67`, `:74`). แบ่งจำนวนวันตามปีและเปรียบเทียบ integer hundredths จาก numeric(8,2) โดยไม่ consume/reserve (`leave.service.ts:182`, `:189`, `:195`). ช่วงค่าที่ schema อนุญาตเป็น nonnegative numeric(8,2) อยู่ใน safe integer range หลังคูณ100 (`backend/src/features/leave/leave.schema.ts:166`, `:183`).
- Missing/frozen ถูกตรวจเสมอก่อนเงื่อนไข allowExceed; no-quota return ก่อนอ่าน quota (`leave.service.ts:183`, `:196`). ไม่มี schema/migration/API-contract/repository/approval-policy delta ใน package.
- Invalid submissions ตรวจ DB ว่า request/day/action ว่าง; invalid cross-year/date/type edits ตรวจ persisted snapshots ก่อน/หลังเท่ากัน (`backend/src/features/leave/leave.quota.integration.test.ts:66`, `:69`, `:89`). Tests ครอบคลุม fractional boundary, no-quota และ explicit excess (`backend/src/features/leave/leave.test.ts:96`, `:101`, `:108`; integration test `:104`).
- UI บอกว่า pending ไม่จอง/ตัดสิทธิ์และอาจอนุมัติไม่ได้ภายหลัง พร้อม excess-policy limitation; Thai quota reasons ใช้ stable error codes (`frontend/app/(dashboard)/leave/page.tsx:98`; `frontend/lib/api/client.ts:72`). Actual EMPLOYEE-only browser scenario ตรวจ rejection → valid submit/reload → invalid edit rollback → owner approval (`frontend/e2e/leave-quota.e2e.ts:40`, `:49`, `:63`, `:70`, `:86`).
- ⚠️ Full20UC actor/browser matrix, academic-document synchronization, final whole-branch review และ integration เป็น root-owned gates ตาม design; focused Task2 evidence ไม่ได้แทน acceptance เหล่านั้น.

## Strengths

- แก้ root cause ด้วย private service guard ร่วมเพียงจุดเดียว ไม่เพิ่ม reservation state, dependency หรือ abstraction. ใช้ `LeaveSession.findQuota` เดิมที่อ่าน quota ด้วย `FOR UPDATE` ภายใน transaction (`backend/src/features/leave/leave.repository.ts:85`, `:90`, `:149`).
- Concurrent integration scenario ตรวจสอง pending requests ใช้ balance เดียวกันโดยไม่ reserve และ approval ที่แข่งกันเหลือเพียงหนึ่ง approved อีกหนึ่ง pending พร้อมหนึ่ง approval action/used_days ที่ถูกต้อง (`backend/src/features/leave/leave.quota.integration.test.ts:115`).
- มี persisted evidence จริงนอก mocked service: PostgreSQL request297/employee1400 เหลือหนึ่งวัน approved, quota consumed/used1.00, submitted actor803 และ approved actor1, audit เฉพาะ successful submit/approve (`docs/superpowers/reports/17-uc08-quota-precheck-evidence/browser-persistence-confirmed.log:1`).

## Issues

- **Critical:** ไม่พบ.
- **Important:** ไม่พบ.
- **Minor:** ไม่พบ actionable defect ใน delta นี้.

## Focused checks and evidence

- อ่าน diff package โดยไม่รัน Git commands หรือแก้ source/index/HEAD. Diff service hunks ตัดกลาง submit/update functions จึงอ่าน complete surrounding service flow เพิ่มเพื่อยืนยัน call ordering และ unchanged approval path; ไม่ขยายไป review feature อื่น.
- Named risk — transaction/lock semantics: ตรวจ `leave.repository.ts:85`, `:90`, `:149`; employee advisory transaction lock และ quota `SELECT FOR UPDATE` อยู่ใน session transaction จริง. Named risk — quota arithmetic assumptions: ตรวจ `leave.schema.ts:166`, `:183`; persisted values เป็น nonnegative numeric(8,2).
- Named risk — approval recheck/type correction/locked-input preservation: ตรวจ unchanged `leave.service.ts:87`, `:102`, `:116`, `:142`, `:145` และ runtime wrapper `backend/src/features/leave/leave.runtime.service.ts:44`. Approval ยังคงตรวจสิทธิ์, supervisor3-day limit, payroll mutability, final type, quota missing/frozen/cap และ consume ใน transaction เดิม; submit runtime ยังตรวจ locked inputs. Existing browser approval boundary ผ่านใน `browser.log:5`.
- Named risk — stable status/UI localization: ตรวจ unchanged `backend/src/core/errors/error-codes.ts:129` ว่า exceeded=422 และ frozen=409; frontend mappings/tests ตรงกัน (`frontend/lib/api/client.test.ts:150`). เปิดดู rejection/reloaded-pending screenshots ที่เก็บไว้แล้ว: Thai business reason และ pending-policy copy อ่านได้ที่ desktop1280px. ไม่อ้าง mobile validation.
- ตรวจ source SHA256 แบบ read-only เทียบ `tested-source-sha256.json`: ตรงทั้ง7ไฟล์ Task2 และ unchanged `frontend/e2e/approval.e2e.ts` รวม8ไฟล์. ไม่พบ source drift จาก tested manifest.
- อ่าน preserved RED/GREEN logs: service14pass/11fail →25pass/0fail; realDB2pass/8fail →10pass/0fail (`service-red.log`, `service-green.log`, `database-red.log`, `database-green.log` ใน evidence directory เดียวกัน). Initial status-expectation/browser-localization failures ถูกเก็บและอธิบายไว้ ไม่ใช่ final run ที่ถูกซ่อน.
- อ่าน final logs: backend types + migrated DB568pass/0skip/0fail (`backend-full.log:1`); frontend55pass/0fail, lint/types/build ผ่าน; focused browser2pass workers1/retries0 (`browser.log:1`, `:9`). ไม่พบ warning ใน final logs ที่ตรวจ. ไม่รัน suites ซ้ำ เพราะไม่มี concrete uncertainty ที่ existing run ไม่ตอบ.

## Assessment

**Task quality: Approved.**

การตรวจพบว่า Task2 ตรงตาม spec และ explicit allow_exceed ruling, วาง quota check ก่อน persistence ภายใต้ transaction/locks เดิม และมี focused unit/realDB/browser persistence evidence รองรับ. Approval recheck/consumption และ historical facts ถูกเก็บตาม workflow เดิม; scope ของ verdict นี้จำกัดเฉพาะ Task2 frozen delta.
