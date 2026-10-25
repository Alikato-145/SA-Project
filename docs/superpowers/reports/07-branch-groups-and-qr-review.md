### Spec Compliance

- ✅ Spec compliant สำหรับ Task 7 ที่ตรวจได้จาก frozen package: ใช้ all-scope HR/OWNER ทุก payment use case, locked payroll และ exact decimal strings, แบ่งกลุ่มโดย membership snapshot ก่อน, ข้าม zero net, เตรียม snapshot แบบ atomic/idempotent และสร้าง QR จาก snapshot เท่านั้น (`backend/src/features/payroll/payroll-payment.service.ts:43`, `:65`, `:72`, `:79`, `:93`; `backend/src/features/payroll/payroll-payment.mapper.ts:3`).
- ✅ Transport, schema และ UI อยู่ในขอบเขต: mutation origin checks และ private/no-store SVG (`backend/src/features/payroll/payroll-payment.routes.ts:18`; `backend/src/features/payroll/payroll-payment.controller.ts:10`), additive schema/lifecycle/partial unique/immutable trigger (`backend/drizzle/0005_sloppy_rafael_vega.sql:1`, `:27`, `:40`, `:42`), ใช้งวดที่เลือกใน payroll workspace (`frontend/app/(dashboard)/payroll/page.tsx:233`) และไม่มี paid/cancel endpoint หรือ external payment service ใน diff.
- ⚠️ Root-owned logical reference updates, migration application และ before/after locked-record hashes อยู่นอก frozen package จึงไม่ตรวจซ้ำใน task-scoped gate นี้; root ต้องคงหลักฐานที่ระบุใน `docs/superpowers/reports/07-branch-groups-and-qr.md` ส่วน Schema coordination. Generated `0005_snapshot.json` ถูกละไว้ใน package; ยังไม่ได้ตรวจ metadata parity โดยอิสระ.

### Strengths

- ใช้ service capability ข้าม feature และ transaction เดียว; ตรวจ destination ทั้ง batch ก่อน insert พร้อม rollback test ที่จงใจล้มหลังเขียนจริง (`backend/src/features/payroll/payroll-payment.service.ts:73`, `:77`, `:89`; `backend/src/features/payroll/payroll-payment.integration.test.ts:36`).
- การเตรียมซ้ำเก็บ snapshot เดิม และ safe mapper ไม่ปล่อย ciphertext/full account number; real DB tests ตรวจทั้ง destination เปลี่ยน, concurrent prepare และ SQL guards (`backend/src/features/payroll/payroll-payment.service.ts:52`, `:79`; `backend/src/features/payroll/payroll-payment.mapper.ts:5`; `backend/src/features/payroll/payroll-payment.integration.test.ts:39`, `:50`).
- Browser check ถอดรหัส pixel จาก SVG ที่แสดงจริงด้วย decoder แยก และตรวจ recipient/amount/checksum หลังแก้ live recipient รวมถึง direct-URL authorization (`frontend/e2e/payroll-payments.e2e.ts:25`, `:39`, `:110`).

### Issues

#### Critical (Must Fix)

- ไม่พบ.

#### Important (Should Fix)

- **[P2] GET list ล็อก employee ตามลำดับที่เปลี่ยนระหว่างงวด ทำให้เกิด deadlock กับ list/prepare ได้** — `backend/src/features/payroll/payroll-payment.service.ts:65` เรียก `load()` ใน transaction โดยไม่เข้า payroll-input serialization แต่ `load()` ที่ `:52` ใช้ `getPaymentDestinationInTransaction` ซึ่งล็อก employee แบบ `FOR UPDATE` (`backend/src/features/employee/employee.service.ts:70`; unchanged persistence capability `backend/src/features/employee/employee.repository.ts:176`). ลำดับแถวเป็น historical branch แล้ว employee code (`backend/src/features/payroll/payroll-payment.repository.ts:33`), ดังนั้นสองงวดที่พนักงาน A/B ย้ายสลับสาขากันจะอ่าน A→B และ B→A. เมื่อสอง request ทำงานพร้อมกัน แต่ละ transaction ถือคนละ employee แล้วรออีกคน เป็น deadlock ที่ PostgreSQL ต้อง abort; list หรือ prepare จะล้มเป็น 500 แม้ข้อมูลถูกต้อง. `serializePayrollInputs` ใน prepare ที่ `:72` ไม่กัน GET ที่ไม่ใช้ lock เดียวกัน. แก้โดยให้ preview อ่านโดยไม่ใช้ update lock หรือกำหนดลำดับ employee lock ที่คงที่/ให้ list ใช้ serialization เดียวกัน แล้วเพิ่ม focused PostgreSQL check สอง locked periods ที่มีลำดับสาขาของพนักงานกลับกัน พร้อม concurrent list/list และ list/prepare. Existing concurrent-prepare test (`backend/src/features/payroll/payroll-payment.integration.test.ts:39`) ใช้เพียงงวดเดียว จึงไม่ครอบคลุม cycle นี้.

#### Minor (Nice to Have)

- **[P3] Browser verification output ยังมี environment warning** — `/private/tmp/haris-task7-browser-final.log:4` มี `NO_COLOR` ถูก `FORCE_COLOR` override. ไม่กระทบผล 2 passed หรือ decode proof แต่ไม่ใช่ pristine output ตาม reviewer rubric; ตั้ง color environment เพียงตัวเดียวใน verification invocation ถัดไป.

### Assessment

**Task quality:** Needs fixes.

**Reasoning:** ขอบเขตธุรกิจและ snapshot/QR implementation ตรง brief แต่ GET preview เพิ่ม multi-row exclusive locking ที่ไม่อยู่ใน serialization protocol จึงต้องแก้ deadlock ก่อนผ่าน task gate. เป็น static concurrency finding; ไม่ได้อ้างว่าพบ deadlock จากการรันจริง.

### Checks and review limits

- อ่าน frozen package หนึ่งรอบแบบแบ่งช่วง (ช่วง output ที่ถูกตัดอ่านเฉพาะส่วนที่หาย); ไม่รัน git recrawl, ไม่รัน test suite ซ้ำ และไม่เปลี่ยน source/index/HEAD. เขียนเฉพาะ report นี้.
- Named risk: finance helper อาจอนุญาต manager/scoped grants — ตรวจ unchanged `backend/src/features/payroll/payroll.authorization.ts:5`; ต้องเป็น parsed active grant scope `all` และ role HR/OWNER.
- Named risk: transaction capability อาจไม่ล็อกแถวเดียวกับ destination edit และ GET อาจถือ lock ข้าม request — ตรวจ unchanged employee payment persistence `backend/src/features/employee/employee.repository.ts:176`, destination normalization `backend/src/features/employee/employee.payment-destination.ts:8`, employee destination update ในส่วนที่อยู่นอก diff hunk, และ global lock helper `backend/src/features/payroll/payroll.input-lock.repository.ts:5`; ยืนยัน row lock จริงและพบ issue ข้างต้น.
- Named risk: historical branch อาจมาจาก current assignment — ตรวจ focused employment-assignment service/repository และ baseline assignment constraints; ordinary assignment flow ปิด effective range แล้ว insert แถวใหม่ จึงไม่เปลี่ยน branch ของ assignment เดิม. Query ใช้ payroll record's stored assignment; ไม่ใช้ current assignment.
- อ่าน nearest frontend instructions (`frontend/AGENTS.md:1`); ไม่มี `backend/AGENTS.md`. ไม่มีการแก้ frontend code.
- อ่านหลักฐานเดิม: `/private/tmp/haris-task7-full-db.log:1` = 530 pass/0 skip/0 fail/115 files; `/private/tmp/haris-task7-browser-final.log:6` = actual pixel-decoded frozen payloads และ `:10` = 2 passed; frontend tests = 48 pass/0 fail/162 assertions/17 files; lint และ frontend/backend type logs ไม่มี error. ไม่สร้างหลักฐานใหม่แทนชุดเดิม.

### Scoped re-review — fix round 1

- **P2: ADDRESSED.** `backend/src/features/payroll/payroll-payment.service.ts:69` เข้า `serializePayrollInputs(e)` ก่อน `load()` จะถือ employee/destination row locks. List/list และ list/prepare จึงใช้ advisory transaction lock เดียวกันก่อนถือแถว แม้ historical branch ทำให้ลำดับพนักงานสองงวดกลับกัน; วงจรที่รายงานใน initial review ถูกตัดที่ต้น transaction.
- **Spec compliance: ✅; Task quality: Approved สำหรับขอบเขต task หลัง fix.** Frozen fix package เปลี่ยน production เฉพาะ list transaction และเพิ่ม regression test; ไม่พบ Important breakage ใหม่ใน repair diff. การรอ global serialization เป็น ceiling เดิมที่ implementer ระบุไว้ ไม่เปลี่ยน snapshot, authority หรือ QR semantics.
- Regression check ใช้ PostgreSQL connections จริงและ historical assignments ที่สลับสาขา (`backend/src/features/payroll/payroll-payment.concurrency.integration.test.ts:19`, `:30`, `:61`), ควบคุมการซ้อน transaction หลัง first destination read และตรวจ blocking (`:50`, `:73`), แล้ว assert ทั้งสอง operation สำเร็จและ prepare มีสอง payment (`:84`, `:85`). ตรวจแล้วว่าใช้ repository/employee capability จริง ไม่แทนที่ persistence ด้วย mock.
- อ่าน evidence เดิมในรอบแก้: `/private/tmp/haris-task7-fix1-red.log` แสดง 0 pass/2 fail ก่อนแก้; `/private/tmp/haris-task7-fix1-green.log` แสดงสอง reversed-period scenarios ผ่านพร้อม payment/QR tests รวม 12 pass/0 fail/72 assertions/4 files; `/private/tmp/haris-task7-fix1-types.log:1` ไม่มี type error. ไม่ rerun suite หรือขยาย review ไปยัง source เดิม.
- Root ยืนยันเพิ่มเติมว่าตรวจ actual generated metadata (22 columns/6 FKs/5 checks/partial unique) กับ SQL/DBML แล้ว, migration สำเร็จ และ hashes ของ locked records 138 แถว/payroll items 9,150 แถวตรงกัน. ข้อจำกัดการตรวจ root-owned evidence ใน initial verdict จึงปิดโดย root; reviewer ไม่ได้ตรวจซ้ำหรือขยาย scope.
- P3 เรื่อง color environment ยังคงเป็น non-blocking verification hygiene; root เลื่อนไปจัด invocation ใน final UAT โดยไม่ขอ product fix. Initial findings ด้านบนเก็บไว้เป็น review history; current P2/task-quality verdict ใช้ผล scoped re-review นี้.
- อ่าน `fix1-review-package.md` หนึ่งรอบ; ไม่มี source/index/HEAD mutation, ไม่มี schema/frontend changes ใน repair diff, และเขียนเฉพาะ append ของ review report นี้.
