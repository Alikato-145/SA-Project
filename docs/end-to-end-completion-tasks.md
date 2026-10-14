# Haris Payroll — Backlog ตาม flow ตั้งแต่เปิดระบบจนปิดเงินเดือน

วันที่จัดทำ: 13 ตุลาคม 2026 · อัปเดตสถานะ 14 ตุลาคม 2026

ติ๊ก [x] เฉพาะงาน implementation/verification หรือ scope decision ที่มีหลักฐานแล้ว งาน CI, release, production provider และ human UAT ไม่ถือว่าปิดด้วย localhost tests งาน 049–050 ไม่ applicable ตาม scope ที่ผู้ใช้ยืนยัน

## วิธีใช้

สั่งงานด้วย ID เช่น `ทำ FLOW-006` หรือ `ทำ FLOW-006 ถึง FLOW-007`
แต่ละ task ต้องทำ scope ของตัวเองพร้อม tests/หลักฐานตามเกณฑ์ ไม่ติ๊กเสร็จเพียงเพราะมี code
รายการขาด/ปัญหาด้านล่างเป็น baseline วันที่ 13 ตุลาคม ไม่ใช่สถานะปัจจุบัน ผู้ใช้อนุญาต implementation และ push แล้ว แต่ไม่ได้อนุญาตเปลี่ยน schema ดูผลล่าสุดใน `completion-progress.md` และ `release-verification-2026-10-14.md`

- **BUILD**: ฟังก์ชัน/ทางใช้งานขาดจริง ต้องเติม
- **FIX**: มี code แต่ flow/behavior ยังไม่ครบหรือมีปัญหาที่ตรวจพบ
- **VERIFY**: มี implementation แล้ว ต้องเดินผ่านเว็บและตรวจ integration; แก้เฉพาะถ้าพบ failure
- **DECIDE**: ต้องปิด scope/policy ก่อน dependent tasks; ถ้าอยู่นอก scope ให้ปิดด้วยเอกสาร ไม่เพิ่มฟีเจอร์
- **P0**: ขวาง flow หลัก/การตรวจรับ, **P1**: ให้ scope ปัจจุบันครบ, **P2**: ก่อนใช้เงินจริง

ทุก task ที่แก้ code ต้องรักษา authorization ฝั่ง server, transactions, append-only history,
decimal money และ feature-first architecture ตาม AGENTS.md
Schema/migrations frozen; checklist นี้ไม่ใช่การอนุมัติเปลี่ยน schema

## 0. ตรึง scope และฐานสำหรับทดสอบ

### [x] FLOW-001 — ตรึง acceptance matrix และสถานะงาน [DECIDE · P0]
- **ขาด:** เอกสารหลายชุดมีคำว่า complete ทั้งที่ยังไม่ได้ตรวจ browser flow ครบ
- **ทำ:** จับคู่ use cases ใน spec/SA report กับ API/UI/5 roles, แยก in-scope/deferred, ระบุ task ที่มี code แล้วกับ task ที่ต้องสร้าง
- **ผ่านเมื่อ:** ทุก feature มีเจ้าของ, allowed/denied roles, acceptance case และ dependency; ความต่างของเอกสารมีข้อสรุป
- **ขึ้นกับ:** ไม่มี · อ้างอิง `specs/012-system-completion/tasks.md` และ audit 2026-10-13

### [x] FLOW-002 — Fixture สำหรับเดินทุก role จนถึง payroll [BUILD · P0]
- **ขาด:** seed เริ่มต้นไม่ใช่ acceptance dataset ที่ครบทุก flow และ scenario
- **ทำ:** Fixture idempotent มี 2 ร้าน/สาขาตาม scenarios, 2 แผนก, 5 roles, account-employee links, employment/config/schedule/holiday, leave/OT/finance และงวดทดสอบ
- **ผ่านเมื่อ:** มีทั้งข้อมูลพร้อมคำนวณและข้อมูลผิดเงื่อนไข; dates คงที่, ไม่พึ่งวันที่เครื่อง; ไม่มีข้อมูลส่วนบุคคลจริงหรือแก้ database ผู้ใช้
- **ขึ้นกับ:** FLOW-001; ใช้ schema/API ปัจจุบัน ไม่รอ browser UI ครบ

### [x] FLOW-003 — คำสั่งตรวจและ CI ที่รัน checks ครบ [BUILD · P0]
- **ขาด:** `bun test` ปกติ skip database gates; ไม่มี browser E2E pipeline ที่พิสูจน์ทุก flow
- **ทำ:** Disposable PostgreSQL + migrations/fixtures + isolated DB test processes, frontend tests/lint/typecheck/build; เตรียม browser runner ให้ tasks หลังใช้
- **ผ่านเมื่อ:** Clean checkout รันซ้ำได้, expected DB checks ไม่ skip, exit code ล้มเมื่อ failure และเก็บ test artifacts
- **ขึ้นกับ:** FLOW-002

## 1. เปิดระบบใหม่และเตรียมองค์กร

### [x] FLOW-004 — Fresh-clone/root Compose และ bootstrap Owner [VERIFY · P0]
- **มีแล้ว:** Root Compose, development defaults, migration startup และ seed
- **ตรวจ:** Clone พร้อม submodules, env setup, build/up/wait, migrate ซ้ำ, provision Owner, restart และ volume persistence; ตรวจ config production แยกจาก development
- **ผ่านเมื่อ:** เริ่มจาก database ว่างด้วยคู่มือได้, Owner login ได้, ไม่มีการ reset ข้อมูลโดยไม่ตั้งใจ; root ไม่พึ่ง host Bun เพื่อรัน stack
- **ขึ้นกับ:** FLOW-001

### [x] FLOW-005 — ร้าน → สาขา → แผนก → ตำแหน่ง [VERIFY · P0]
- **มีแล้ว:** Organization API/UI; ยังไม่ได้พิสูจน์ journey ใหม่ครบทุก entity
- **ตรวจ:** Create/list/edit/deactivate, duplicate codes, เลือกร้านแล้วรายการลูกเปลี่ยน, active filters/pagination และป้องกันปิด parent ที่ยังมี dependency
- **ผ่านเมื่อ:** ตั้งองค์กรผ่านเว็บได้ครบ, dropdown เห็นข้อมูลใหม่, IDs ข้ามร้าน/สาขาถูกปฏิเสธ, history ไม่หาย
- **ขึ้นกับ:** FLOW-004

### [x] FLOW-006 — หน้าตารางเวลาทำงานสาขา [BUILD · P0]
- **ขาดจริง:** มี branch-schedule API/controls แต่ controls ไม่ได้ mount ในหน้าใช้งาน
- **ทำ:** หน้า/ส่วนงานภาษาไทย เลือกสาขาด้วยชื่อ, ตั้งเวลาเริ่ม/เลิก, late grace, effective range; เปลี่ยน schedule ด้วยประวัติเดิม
- **ผ่านเมื่อ:** สร้าง schedule ของสาขาใหม่ผ่านเว็บแล้ว payroll ใช้ได้; overlap/invalid times/wrong scope มีข้อความแก้ไขได้; ไม่ rewrite ช่วงเก่า
- **ขึ้นกับ:** FLOW-005

### [x] FLOW-007 — วันหยุดนักขัตฤกษ์และ schedule overrides [BUILD · P1]
- **ขาดจริง:** Existing holiday/override APIs ยังไม่มี web path ที่พร้อมใช้
- **ทำ:** จัดการ holiday ตามร้าน, override วันเฉพาะ/ปิดสาขา, active/inactive, แสดง precedence ระหว่าง base schedule กับ override
- **ผ่านเมื่อ:** ผู้ใช้เห็นตารางที่มีผลในวันที่เลือก, payroll/attendance/OT ใช้ตรงกัน, ปิดใช้งานไม่ลบประวัติ
- **ขึ้นกับ:** FLOW-006

### [x] FLOW-008 — ค่าคำนวณและ effective-date validation [FIX · P0]
- **ปัญหา:** Readiness เช็กแค่ว่ามี key สัก row; หน่วยและ placeholder ไม่พอป้องกันกรอกผิด
- **ทำ:** Validations ตาม config key/unit, scope ร้าน/สาขา, effective coverage และ overlap; แสดงตัวอย่างสัดส่วน/บาท/เท่า/วันให้ตรงค่า
- **ผ่านเมื่อ:** แยก ratio กับ cap บาทได้, ค่าผิดวันที่หรือคนละสาขาไม่ถูกนับว่าพร้อม; ไม่มีอัตราจริงที่ agent เดาแทนผู้ใช้
- **ขึ้นกับ:** FLOW-005, FLOW-001 สำหรับ policy bounds

### [x] FLOW-009 — Organization/payroll readiness checklist [BUILD · P0]
- **ขาด:** ผู้ใช้เจอ blockers ทีละข้อหลังลองคำนวณ แทนที่จะรู้สิ่งที่ต้องเตรียมทั้งหมด
- **ทำ:** Checklist ตามร้าน/สาขา/งวด สำหรับ schedule/config/employment/attendance/pending approvals และ bank data สำหรับ export พร้อมลิงก์ไปแก้
- **ผ่านเมื่อ:** แยก not configured, invalid, pending, ready; ตรวจ effective dates ของงวดจริง; readiness ไม่ bypass lock validation
- **ขึ้นกับ:** FLOW-006, FLOW-008; เพิ่มรายการจาก tasks ถัดไปเมื่อ feature พร้อม

## 2. รับพนักงานและเตรียมบัญชีเข้าใช้

### [x] FLOW-010 — Onboarding พนักงานพร้อมข้อมูลการจ้าง [FIX/VERIFY · P0]
- **มีแล้ว:** Atomic onboarding employee/assignment/bank/weekly holidays/optional account
- **ขาด:** สร้าง account ใน onboarding แล้วยังไม่มี grants; success ไม่ทำให้ provisioning ทั้ง flow ชัด
- **ทำ:** ตรวจ onboarding ทั้ง optional cases, validation/scope/rollback; หลังสำเร็จแสดงขั้นตอนกำหนด role และสิ่งที่ยังไม่ครบ
- **ผ่านเมื่อ:** ข้อมูลสำเร็จทั้งหมดหรือ rollback ทั้งชุด; ไม่บอกว่าบัญชีพร้อมใช้เมื่อไม่มี role; พนักงานกลางเดือนเข้า payroll ตรงช่วงจ้าง
- **ขึ้นกับ:** FLOW-005, FLOW-006, FLOW-008

### [x] FLOW-011 — Account-employee linkage และบัญชีที่สร้างมาก่อน [DECIDE/FIX · P0]
- **ปัญหา:** สร้าง standalone account ได้โดยไม่มี employee; ไม่มี self-service ที่ทำให้กรณีบัญชีเดิมชัดเจน
- **ทำ:** แยกบัญชีส่วนกลางจากบัญชีพนักงาน, ตรวจสร้างบัญชีให้ existing employee; ตัดสิน policy ว่าบัญชีเดิมที่ยังไม่ผูกจะ link ได้หรือสร้างใหม่
- **ผ่านเมื่อ:** ถ้าอนุญาต link ต้องมี authorized/audited workflow, one-account-per-employee, ไม่ rebind บัญชีที่มีความสัมพันธ์แล้วโดยเงียบ ๆ; ถ้าไม่อนุญาตมี recovery ชัด
- **ขึ้นกับ:** FLOW-010; policy ที่เปลี่ยน ownership ต้องตกลงก่อน implementation

### [x] FLOW-012 — กำหนด/revoke role และ scope ครบทุกบทบาท [FIX · P0]
- **ปัญหา:** Settings grant ส่ง department เป็น null เสมอ; user เข้าใจว่าสาขาของ employee คือ role scope
- **ทำ:** ใช้ form/validation สอดคล้องกันทั้ง Settings/Account detail; EMPLOYEE=self+employee link, Supervisor=branch+department, Manager=branch, HR/Owner=all ตามสิทธิ์ผู้ให้
- **ผ่านเมื่อ:** Dropdowns scoped/refresh ถูก, เปลี่ยน parent ล้างลูก, last-owner protection และ grant/revoke audit; server ปฏิเสธ combinations ผิด
- **ขึ้นกับ:** FLOW-005, FLOW-011

### [x] FLOW-013 — Login landing ของบัญชีไม่มี role/ไม่มี employee [FIX · P0]
- **ปัญหา:** Login สำเร็จแต่ sidebar ว่างและแสดง generic forbidden
- **ทำ:** หน้า account-not-ready บอกสิ่งที่ขาดและผู้ที่แก้ได้; redirect ตาม role ที่อนุญาต, recover ไป workspace ที่มีสิทธิ์, logout ได้เสมอ
- **ผ่านเมื่อ:** No-role, no-employee, multiple-role และ unsupported path ไม่พาเข้าทางตัน; ไม่ grant default privileges เพื่อแก้อาการ
- **ขึ้นกับ:** FLOW-012

### [x] FLOW-014 — รหัสชั่วคราวและการดูแลบัญชี [FIX/VERIFY · P1]
- **มีแล้ว:** Login/logout, lockout, reset/unlock/disable, password change บางส่วนใน working tree
- **ตรวจ/ทำ:** Clear password-change prompt/policy, reset/revocation, session expiry, account disable/unlock reasons, temporary password display once; เปลี่ยน role ระหว่าง session
- **ผ่านเมื่อ:** Lifecycle ใช้ผ่านเว็บได้, ไม่แสดง/log secrets ซ้ำ, session/disabled account behavior ตรง policy; เปลี่ยนรหัสไม่กระทบ account อื่น
- **ขึ้นกับ:** FLOW-012, FLOW-013

### [x] FLOW-015 — สิทธิ์หน้า/เมนู/API ทั้ง 5 roles [VERIFY · P0]
- **ยังไม่พิสูจน์ครบ:** มี policy/helpers/tests แต่ไม่ใช่ live route matrix ทุก workflow
- **ตรวจ:** Own employee, department, branch, all-scope; allowed+denied cases, URL/API โดยตรง, roles inactive/revoked และ multiple grants
- **ผ่านเมื่อ:** UI ไม่ชวนทำ action ที่ไม่มีสิทธิ์; backend deny ได้อิสระจาก UI และไม่ leak sensitive fields
- **ขึ้นกับ:** FLOW-012, FLOW-014; ขยาย matrix เมื่อแต่ละ feature พร้อม

## 3. ข้อมูลพนักงานและประวัติการจ้าง

### [x] FLOW-016 — Profile, transfer, promotion, salary/welfare และ termination [VERIFY · P1]
- **มีแล้ว:** Employee/profile/history APIs และหน้าจัดการข้อมูลการจ้าง
- **ตรวจ:** Update profile, successor assignment, transfer กลางงวด, salary/welfare changes, hire/termination dates, overlap และ scope
- **ผ่านเมื่อ:** ปิด row เดิม+สร้าง row ใหม่, compensation history ไม่ถูกเขียนทับ, payroll แบ่งวันที่ใช้ค่าถูก, termination ไม่ลบ history
- **ขึ้นกับ:** FLOW-010, FLOW-015

### [x] FLOW-017 — บัญชีธนาคารพนักงาน [VERIFY · P1]
- **มีแล้ว:** Encrypted bank-account API/UI
- **ตรวจ:** Add/edit/make-primary/deactivate/replacement, absence of primary, masks และ access; bank export แสดงตามสิทธิ์ที่จำเป็น
- **ผ่านเมื่อ:** Primary ไม่ขัดกัน, ไม่มี full account ใน ordinary responses/logs, export อ่านข้อมูลถูกและแจ้ง bank data ที่ขาด
- **ขึ้นกับ:** FLOW-016

### [x] FLOW-018 — วันหยุดประจำสัปดาห์แบบมีประวัติ [VERIFY · P1]
- **มีแล้ว:** List/add/end API และ UI
- **ตรวจ:** ชุดวันหยุด, effective overlaps, เปลี่ยนกลางเดือน, successor และ payroll/OT interpretation
- **ผ่านเมื่อ:** วันเก่ายังอ่านตามประวัติ, ไม่ทำให้การคำนวณย้อนหลังใช้วันหยุดปัจจุบันแทน
- **ขึ้นกับ:** FLOW-016, FLOW-006

### [x] FLOW-019 — Attachment infrastructure และเอกสารพนักงาน [BUILD · P1]
- **ขาดจริง:** หน้า documents ระบุยังไม่เปิดใช้งาน; ไม่มี authorized storage journey ครบ
- **ทำ:** Upload/list/download, storage adapter, size/MIME/hash validation, authorization/audit/redaction, retention; ใช้ schema เดิมก่อนเสนอเปลี่ยน
- **ผ่านเมื่อ:** ไฟล์มี storage จริง, wrong employee/unsafe file/tampering ถูกปฏิเสธ, deactivate ไม่ลบหลักฐานที่ต้องเก็บ
- **ขึ้นกับ:** FLOW-016, FLOW-001 สำหรับ storage/retention policy

## 4. ลงเวลาทำงานรายวัน

### [x] FLOW-020 — Attendance selectors และหน้าทำงานตาม scope [FIX · P1]
- **ปัญหา:** ยังต้องกรอก branch ID; การเลือกพนักงานกับสาขาอาจไม่ตรง historical assignment
- **ทำ:** Named scoped selectors, ใช้ work date หา assignment/branch, reset dependent values, ดูข้อมูลตาม role
- **ผ่านเมื่อ:** เลือกวันที่แล้วสาขาถูก, employee/branch ข้าม scope ถูก deny, stale selection ไม่ส่งข้อมูลผิด
- **ขึ้นกับ:** FLOW-015, FLOW-016, FLOW-006

### [x] FLOW-021 — Attendance status/clock/late/grace integration [VERIFY · P1]
- **ยังไม่พิสูจน์:** Clock fields, late minutes, deductible status ต้องสอดคล้อง schedule/override/timezone และ payroll
- **ตรวจ:** Present/late/absent/weekly/public holiday, grace boundary, clock order, timezone และวันที่ข้ามเที่ยงคืนตาม policy
- **ผ่านเมื่อ:** Late/deduction ที่ payroll ใช้ตรงกับข้อเท็จจริง; ถ้า manual correction ได้ต้องแยกจาก computed values และมีเหตุผล/audit
- **ขึ้นกับ:** FLOW-020, FLOW-007, FLOW-018

### [x] FLOW-022 — Attendance duplicate/correction/locked protection [VERIFY · P0]
- **มีแล้ว:** Create/correct API และ checks บางส่วน
- **ตรวจ:** Employee+date uniqueness, historical branch snapshot, correction reasons, approved leave interaction, payroll locked dates และ rollback
- **ผ่านเมื่อ:** ไม่ overwrite locked/approved facts ผ่าน ordinary flow, correction มี trace, double submit ไม่สร้างซ้ำ
- **ขึ้นกับ:** FLOW-021

### [x] FLOW-023 — หน้าตรวจวันลงเวลาที่ขาด [BUILD · P0]
- **ขาด:** ผู้ใช้ไม่มี actionable work-date list ที่เติมจน payroll พร้อมได้สะดวก
- **ทำ:** ช่วงวันตาม employment และงวด, missing vs holiday vs leave vs attendance, link ไปวัน/พนักงานที่ต้องแก้; ไม่เติม absent/present อัตโนมัติโดยเดา
- **ผ่านเมื่อ:** HR/Supervisor/Manager เห็นเฉพาะ scope, วันก่อน hire/หลังสิ้นสุดไม่ถูกเรียกให้ลงเวลา, completeness ใช้ logic ตรง payroll
- **ขึ้นกับ:** FLOW-022, FLOW-018, FLOW-009

## 5. การลา

### [x] FLOW-024 — จัดการประเภทการลา [BUILD · P1]
- **ขาดจริง:** มี read types แต่ไม่มี administration lifecycle ครบตาม completion plan
- **ทำ:** HR/Owner list/create/update/deactivate, quota/deduction/document flags, duplicates และ audit
- **ผ่านเมื่อ:** ประเภทที่ถูกอ้างอิงไม่ถูก hard delete, history เก่ายังคงความหมาย, ตัวเลือก active ถูก
- **ขึ้นกับ:** FLOW-001, FLOW-015

### [x] FLOW-025 — จัดสรรและดู leave quota [BUILD · P1]
- **ขาด:** Quota API read/approval internals ไม่ใช่หน้าตั้ง quota สำหรับพนักงานใหม่ครบ flow
- **ทำ:** จัดสรรรายปี/ประเภท/พนักงานตาม policy, แสดง entitled/used/remaining และ annual setup; audit entitlement changes
- **ผ่านเมื่อ:** พนักงานใหม่มี quota ที่ตรวจได้, used ไม่ถูก reset, zero/missing/exhausted quota แจ้งและใช้ policy ที่ตกลง
- **ขึ้นกับ:** FLOW-024, FLOW-010; quota carry-forward ไม่เพิ่มถ้าอยู่นอก scope

### [x] FLOW-026 — ขอ/แก้ใบลาที่ยัง pending [VERIFY · P1]
- **มีแล้ว:** Self/management form, submit/pending edit APIs
- **ตรวจ:** Own-only, overlaps, dates/reason, quota presentation, retroactive policy, changing type/dates, decided/locked request protections
- **ผ่านเมื่อ:** พนักงานไม่ต้องกรอก employee ID, pending edit ถูกต้องและ audit ครบ, wrong scope/invalid range ไม่เปลี่ยน attendance/quota
- **ขึ้นกับ:** FLOW-025, FLOW-015

### [x] FLOW-027 — Approve/reject/correct leave type [VERIFY · P0]
- **มีแล้ว:** Approval API/UI; ต้องพิสูจน์ 3/4-day และ atomic effects ผ่าน journey
- **ตรวจ:** Supervisor ≤3 วัน, Manager ได้ทุกความยาวและ direct approval, HR duties ตาม policy, corrected type, duplicate/concurrent decisions, quota+attendance transaction
- **ผ่านเมื่อ:** 4 วันถูก deny สำหรับ Supervisor, out-of-scope ถูก deny, rollback ไม่กิน quota/แก้ attendance บางส่วน; paid leave ไม่ถูกหักผิด policy
- **ขึ้นกับ:** FLOW-026, FLOW-022

### [x] FLOW-028 — เอกสารใบลาและ decision history [BUILD · P1]
- **ขาด:** หน้าแสดง requiresDocument แต่ไม่มี upload path; history API ไม่ถูกแสดงใน workspace
- **ทำ:** เชื่อม attachment กับคำขอ, required-document policy, append-only action list มีผู้อนุมัติ/เวลา/เหตุผล/old-new leave type
- **ผ่านเมื่อ:** แนบ/ดูไฟล์ตามสิทธิ์, ข้อมูลขาดอธิบายก่อนส่ง/อนุมัติ, history หลัง correction และล็อกยังครบ
- **ขึ้นกับ:** FLOW-019, FLOW-027

## 6. OT

### [x] FLOW-029 — ขอ OT ทุกประเภทและคำนวณหน่วย [VERIFY · P1]
- **มีแล้ว:** Fixed hourly/rest_day/public_holiday submit APIs/forms
- **ตรวจ:** hours/day_units, work date/record link, self/scope, duplicates, rest/public holiday applicability; ตรึง fixed vs configurable types กับ SA report
- **ผ่านเมื่อ:** หน่วยไม่สลับ, late clock-out ไม่กลายเป็น payable OT อัตโนมัติ, invalid type/date ถูกปฏิเสธ
- **ขึ้นกับ:** FLOW-007, FLOW-018, FLOW-021, FLOW-001

### [x] FLOW-030 — แก้ OT ที่ยัง pending [BUILD · P1]
- **ขาดจริง:** OT routes ไม่มี pending correction endpoint และ UI
- **ทำ:** แก้ date/type/amount/reason ตาม policy ก่อน decision/lock; validation, authorization และ old/new audit
- **ผ่านเมื่อ:** Decided/locked OT แก้ไม่ได้, duplicates และ wrong scope ถูก deny, ข้อมูลการตัดสินเก่าไม่หาย
- **ขึ้นกับ:** FLOW-029

### [x] FLOW-031 — OT approvals และ append-only history [FIX/VERIFY · P0]
- **มีแล้ว:** Approve/reject/history API; history UI ยังขาด
- **ทำ/ตรวจ:** Scoped decisions, reason, history viewer, double decision, payroll input เฉพาะ approved และ transaction rollback
- **ผ่านเมื่อ:** Pending/rejected OT ไม่ถูกจ่าย, ทุก action อ่าน trace ได้; ทั้ง 3 ประเภทถูกคิดอัตราที่มีผลวันที่ทำงาน
- **ขึ้นกับ:** FLOW-030, FLOW-008

## 7. เงินทดรอง เงินกู้ และหนี้

### [x] FLOW-032 — Employee advance request/list [BUILD · P1]
- **ขาดจริง:** Finance route policy เปิดเฉพาะ HR/Owner จึงไม่มี employee request journey
- **ทำ:** Self-only request/list และสถานะ/เหตุผล; แยกจาก admin approve/loan/debt controls
- **ผ่านเมื่อ:** Employee ขอของตัวเองได้และเข้าของคนอื่นไม่ได้ทั้ง UI/API; ไม่มี admin actions หลุดมา
- **ขึ้นกับ:** FLOW-015, FLOW-016

### [x] FLOW-033 — Advance eligibility และ approval [VERIFY · P0]
- **มีแล้ว:** Eligibility/projection/approval logic และ focused tests
- **ตรวจ:** วันที่ 19/20, worked days 19/20, ไม่เกินครึ่ง base salary, projected net pay ไม่ติดลบ, pending duplicates, rejection note, lock/projection integration
- **ผ่านเมื่อ:** Boundary ทุกคู่มี deterministic fixture; UI บอกเหตุผลชัด, concurrent approve ไม่เกิน cap, final payroll ใช้ approved advance ถูก
- **ขึ้นกับ:** FLOW-032, FLOW-023, FLOW-008

### [x] FLOW-034 — Loan creation/installments/payroll settlement [VERIFY · P1]
- **มีแล้ว:** Loan create/list พร้อม installments; ไม่สรุปว่าต้องมี loan approval เพิ่มเอง
- **ตรวจ:** จำนวนงวดตาม scope, first due month, exact money/rounding, outstanding balance, installment inclusion และ lock settlement ซ้ำ
- **ผ่านเมื่อ:** ยอดงวดรวมตรง principal, หักเดือนถูก, preview ไม่ settle จริง, lock ซ้ำไม่หักซ้ำ, history อ่านได้
- **ขึ้นกับ:** FLOW-016, FLOW-008; final settlement test ขึ้นกับ FLOW-042

### [x] FLOW-035 — Debt-type selector และ policy master data [FIX/DECIDE · P1]
- **ปัญหา:** Finance ต้องกรอก debt_type_id เอง ไม่มี named selector
- **ทำ:** Scoped named choices; ตัดสินว่าประเภทหนี้เป็น fixed seed หรือ HR-managed ก่อนสร้าง administration API
- **ผ่านเมื่อ:** ลงหนี้อาหารได้โดยไม่รู้ ID, inactive/reference history ไม่เสีย; ถ้า fixed คู่มือและ fresh setup มีข้อมูลครบ
- **ขึ้นกับ:** FLOW-001, FLOW-005

### [x] FLOW-036 — Debt ledger/reversal/payroll deduction [VERIFY · P0]
- **มีแล้ว:** Transaction-based debt ledger/reversal API/UI
- **ตรวจ:** Charge/adjustment/reversal reasons, double reversal, settled records, balance and payroll inclusion, locking concurrency
- **ผ่านเมื่อ:** ไม่มี reset/delete history, ยอดคงเหลือตรง transactions, settled debt ไม่ถูกหักซ้ำ และ reversal ไม่ลบรายการเดิม
- **ขึ้นกับ:** FLOW-035; final settlement test ขึ้นกับ FLOW-042

## 8. เปิดงวด คำนวณ ล็อก และปรับปรุง

### [x] FLOW-037 — เปิดงวดเงินเดือนและเลือกเดือนให้เข้าใจง่าย [FIX · P0]
- **ปัญหา:** `type=month` บาง browser เป็น text ไม่มีตัวอย่าง; period errors ไม่ได้ช่วยให้ผู้ใช้แก้ได้ครบ
- **ทำ:** Label/format/example หรือ fallback ที่กรอกได้ชัด, calendar boundaries, shop selection, duplicate period handling
- **ผ่านเมื่อ:** เดือนปกติ/ก.พ. leap year สร้างวันที่ถูก, ค.ศ. ชัด, หนึ่งร้านหนึ่งงวดต่อเดือนไม่ซ้ำ และ role ไม่อนุญาตสร้างไม่ได้
- **ขึ้นกับ:** FLOW-008, FLOW-015

### [x] FLOW-038 — รายชื่อพนักงานที่เข้าเกณฑ์งวด [BUILD/FIX · P0]
- **ปัญหา:** ผู้ใช้ไม่รู้ว่าผูก account/branch แล้วแต่เริ่มจ้างคนละเดือนหรือยังติด input จึงไม่มีเงินเดือน
- **ทำ:** Roster จาก effective employment, แสดงชื่อ/code/branch/date; แยก included, excluded และ blocked พร้อมเหตุผล
- **ผ่านเมื่อ:** hire/termination/transfer กลางงวดถูก, เดือนก่อนจ้างไม่มี payroll โดยมีคำอธิบาย, ไม่ใช้ account-role branch แทน employment snapshot
- **ขึ้นกับ:** FLOW-016, FLOW-037

### [x] FLOW-039 — Payroll blockers เป็น checklist ที่แก้ต่อได้ [FIX · P0]
- **ปัญหา:** Generic English error ไม่ระบุ config ที่ขาด และพบ input blockers ทีละด่าน
- **ทำ:** Structured missing key/date/branch/employee details, Thai messages, links to setup/attendance/approval, readiness ตรง backend lock checks
- **ผ่านเมื่อ:** User แก้ได้โดยไม่อ่าน SQL/code; แยก empty period, not calculated, incomplete calculation และ lock ready ได้
- **ขึ้นกับ:** FLOW-009, FLOW-023, FLOW-038

### [x] FLOW-040 — Daily payroll calculation integration [VERIFY · P0]
- **มีแล้ว:** Decimal calculator และ projection tests
- **ตรวจ:** Daily salary/welfare, absence/late, paid/non-deductible leave, approved OT, weekly/public holidays, advances/installments/debt/adjustments, mid-period history และ rounding
- **ผ่านเมื่อ:** Golden expected totals/items/evidence ตรง business policy, social security ใช้ base salary ไม่รวม welfare, deductions แยก non-deductions, negative net blocks lock
- **ขึ้นกับ:** FLOW-027, FLOW-031, FLOW-033–036, FLOW-038

### [x] FLOW-041 — โหลด persisted payroll และดูรายการหลัง refresh [FIX · P0]
- **บั๊กยืนยัน:** ตารางใช้ preview state; reload/เปลี่ยนงวดไม่เรียก getPeriod records; locked period preview ไม่ได้
- **ทำ:** โหลด detail/records/items เมื่อเลือกงวด, clear stale requests, read-only Manager ตาม scope, loading/error/retry
- **ผ่านเมื่อ:** Preview/lock → refresh/relogin/switch period แล้วเห็นข้อมูลที่ persist อยู่และ evidence; ไม่มีการคำนวณใหม่เพื่ออ่าน locked records
- **ขึ้นกับ:** FLOW-037, FLOW-038; test locked case หลัง FLOW-042

### [x] FLOW-042 — Lock atomicity, snapshots และ concurrency [VERIFY · P0]
- **มีแล้ว:** Lock prerequisites/transaction/snapshot logic
- **ตรวจ:** Attendance complete, no pending decisions, net ≥0, unique employee-period, snapshot config/history/bank evidence ตาม policy, concurrent locks/input changes และ settlement rollback
- **ผ่านเมื่อ:** Fail แล้วไม่มี partial settlement/record, locked values immutable, บันทึก actor/time, second lock ไม่จ่ายหรือหักซ้ำ; UI แสดงผลชัด
- **ขึ้นกับ:** FLOW-039, FLOW-040, FLOW-041

### [x] FLOW-043 — Adjustment ตั้งแต่ request ถึง applied [BUILD/FIX · P1]
- **ขาดจริง:** API list/decide มี แต่หน้า Payroll มีเพียง request form และ raw IDs
- **ทำ:** เลือก original locked record/target period, list pending/history, approve/reject, show application และ old record context
- **ผ่านเมื่อ:** ไม่แก้ original snapshot, target ต้องถูกงวดและไม่ locked, apply ครั้งเดียว, scope/reason/audit ครบ
- **ขึ้นกับ:** FLOW-042, FLOW-041

## 9. Payslip รายงาน และการส่งออก

### [x] FLOW-044 — PDF payslip และ Employee own-only view/download [BUILD · P1]
- **ขาดจริง:** Service สร้าง JSON storage key/hash แต่ไม่มี PDF storage/download journey
- **ทำ:** Versioned immutable PDF จาก locked snapshot, metadata/storage authorization, own list/read/download, HR generate/view/void และ named payroll selector
- **ผ่านเมื่อ:** File มีจริงและยอดตรง, one payslip/record ตาม model, cross-employee/voided/tampered/duplicate cases ถูก deny; ordinary responses ไม่ expose storage secrets
- **ขึ้นกับ:** FLOW-042, FLOW-017, FLOW-019 สำหรับ storage ที่ใช้ร่วมกันได้

### [x] FLOW-045 — Payslip delivery ที่ตรงกับสิ่งที่ส่งจริง [BUILD/DECIDE · P1/P2]
- **ปัญหายืนยัน:** ปัจจุบัน insert email log เป็น sent โดยไม่มี provider call
- **ทำ:** ตกลง demo vs real mail; ถ้า real เชื่อม provider, recipient policy, sent/failed attempts, retry/idempotency; ถ้า demo label ต้องชัดและไม่กล่าวว่าส่งจริง
- **ผ่านเมื่อ:** ทุก attempt มีผลจริง/จำลองที่แยกชัด, failed ไม่ถูกทำเป็น sent, recipient ได้เฉพาะเอกสารที่อนุญาต, ไม่ log secrets
- **ขึ้นกับ:** FLOW-044, FLOW-001 สำหรับ provider/recipient policy

### [ ] FLOW-046 — Bank-transfer และ social-security CSV [FIX/VERIFY · P1]
- **มีแล้ว:** Locked-period CSV endpoints; UI ยังใช้ period ID และเปิดหน้าต่างโดยไม่รู้ว่าดาวน์โหลดสำเร็จ
- **ทำ/ตรวจ:** Named period selector, file error feedback, missing bank/config diagnostics, format/encoding and exact locked totals, permissions
- **ผ่านเมื่อ:** CSV rows/count/totals ตรง snapshots, unlocked/wrong scope ถูกปฏิเสธ, ทดสอบกับ format ที่ผู้รับไฟล์ต้องการ; export ไม่หมายถึง paid/submitted
- **ขึ้นกับ:** FLOW-042, FLOW-017, FLOW-008

### [x] FLOW-047 — Management summaries ตาม scope ที่ตกลง [BUILD · P1]
- **ขาดจริง:** Reports ปัจจุบันมีเพียง 2 CSV ไม่ใช่รายงาน attendance/leave/OT/debt/payroll summaries ครบ
- **ทำ:** Filter ร้าน/สาขา/แผนก/งวดตาม duties, totals/drill-down/export ตาม requirements ที่ตกลงใน FLOW-001
- **ผ่านเมื่อ:** ยอดตรง source/locked records, denied scope ไม่รวมใน aggregates, ประวัติย้อนหลังไม่ใช้ assignment ปัจจุบันแทน
- **ขึ้นกับ:** FLOW-040, FLOW-046, FLOW-015

## 10. จ่ายเงินจริงและการยืนยัน — มี scope gate

### [x] FLOW-048 — ตัดสิน locked vs paid และ disbursement contract [DECIDE · P1 ถ้า in-scope]
- **ขาด:** Completion plan/SA report ระบุ payment workflows แต่ยังไม่มี approved model
- **ทำ:** ตกลงระบบจบที่ CSV หรือ record cash/bank payment, partial/failed/reversed policy, idempotency, amount limits และ append-only model
- **ผ่านเมื่อ:** Product/schema owner อนุมัติข้อสรุป; ถ้านอก scope คู่มือไม่สื่อว่า lock/export คือจ่ายแล้ว
- **ขึ้นกับ:** FLOW-001, FLOW-042; ไม่แก้ schema ก่อน gate นี้

### [ ] FLOW-049 — บันทึกจ่ายเงินสดและ reversal [BUILD · CONDITIONAL]
- **ขาด:** ไม่มี payment lifecycle จริงใน code ปัจจุบัน; ทำเฉพาะ FLOW-048 อนุมัติ
- **ทำ:** HR/Owner เลือก locked employee record, amount/reference/evidence, record paid/reversal append-only ตาม approved contract
- **ผ่านเมื่อ:** Duplicate/overpayment/unlocked/wrong-scope ถูก deny, reversal ไม่ rewrite payroll และ audit ครบ
- **ขึ้นกับ:** FLOW-048, FLOW-019; schema change ต้องได้รับอนุมัติแยก

### [ ] FLOW-050 — Bank batch reconciliation และผลโอน [BUILD · CONDITIONAL]
- **ขาด:** CSV export ไม่ได้ติดตามว่าจ่ายสำเร็จ/ล้มเหลว
- **ทำ:** Batch/row-to-record mapping, confirm paid/failed, retry history และ reconciliation ตาม model; ไม่ทำ direct bank API ที่ defer ไว้
- **ผ่านเมื่อ:** ยอดส่งออก/สำเร็จ/ล้มเหลวตรง locked net, repeated confirmation ไม่จ่ายซ้ำ, failures และ reversals trace ได้
- **ขึ้นกับ:** FLOW-048, FLOW-046; schema gate เหมือน FLOW-049

### [x] FLOW-051 — Scope การยื่น/ชำระประกันสังคม [DECIDE/CONDITIONAL BUILD]
- **ขาด:** ยังต้องยืนยันว่าจบที่ CSV หรือมี submission/payment acknowledgment
- **ทำ:** ตรึง scope; ถ้าต้องมีจริงออกแบบ evidence/status/history/roles แล้ว implement หลังอนุมัติ; ถ้าไม่มีแก้คำอธิบายใน SA/คู่มือ
- **ผ่านเมื่อ:** Exported/submitted/accepted/paid ไม่ถูกใช้แทนกันโดยไม่มีหลักฐาน
- **ขึ้นกับ:** FLOW-001, FLOW-046

### [x] FLOW-052 — ตัดสินคำว่าใบแจ้งหนี้รายบุคคล [DECIDE/CONDITIONAL BUILD]
- **ขาด:** SA use case อาจใช้คำไม่ตรง payslip หรือหมายถึงเอกสารคนละชนิด
- **ทำ:** ยืนยันเอกสาร เจ้าของ ผู้รับ fields/lifecycle/retention; ถ้าเป็น payslip แก้ terminology; ถ้าแยกต้อง approved spec ก่อนสร้าง
- **ผ่านเมื่อ:** Scope ไม่ขัดกับคู่มือ/API และไม่สร้าง invoice feature จากการเดาความหมาย
- **ขึ้นกับ:** FLOW-001, FLOW-044

## 11. Audit และการตรวจย้อนหลัง

### [x] FLOW-053 — Audit viewer และครบทุก sensitive action [VERIFY · P1]
- **มีแล้ว:** Audit APIs/viewer, append-only/redaction checks
- **ตรวจ:** Search/filter/actor/target/time/request ID, role changes/reset, employment/bank, approval/correction, finance, preview/lock/adjustment, payslip/export และ payment ถ้า in-scope
- **ผ่านเมื่อ:** หา incident ผ่านเว็บได้, success/failure/rollback มี trace ตาม policy, ไม่มี passwords/tokens/full bank details; update/delete audit ถูก deny
- **ขึ้นกับ:** FLOW-015; final matrix หลัง feature tasks ที่เกี่ยวข้อง

## 12. เดินทุก flow ผ่าน browser

### [x] FLOW-054 — Browser authorization matrix และ account journeys [BUILD · P0]
- **ขาดจริง:** Tests ปัจจุบันไม่ใช่ live browser journey ของทุก role
- **ทำ:** Login/logout/landing/change password/session expiry/role change/no-role + route/action allow/deny ทั้ง 5 roles รวม direct API requests
- **ผ่านเมื่อ:** ใช้ FLOW-002 fixture, tests rerun ได้, backend deny ข้าม employee/department/branch; screenshots/traces เมื่อ fail
- **ขึ้นกับ:** FLOW-003, FLOW-014, FLOW-015

### [x] FLOW-055 — Browser journey ตั้งแต่ตั้งร้านจนถึง export [BUILD · P0]
- **ขาด:** ยังไม่มีหลักฐานปิดงานจาก fresh state ผ่าน UI โดยไม่ใช้ SQL เติมข้อมูลระหว่างทาง
- **ทำ:** Organization → onboarding/grants → schedule/config → attendance → leave/OT → finance → preview/blocker recovery → lock → adjustment → payslip/export; payment เพิ่มเฉพาะ approved scope
- **ผ่านเมื่อ:** Owner/HR/Manager/Supervisor/Employee ทำหน้าที่จริงครบ, cross-role effects ตรง, refresh/relogin ไม่เสีย state, expected totals ยืนยันด้วย golden fixture
- **ขึ้นกับ:** FLOW-005–047 ตาม flow; ใช้ FLOW-048–052 เฉพาะที่อนุมัติ

### [x] FLOW-056 — Failure paths, contract/pagination และ mobile/a11y [BUILD/FIX · P1]
- **ขาด:** Happy-path/API tests ไม่พิสูจน์ UI recovery และ selector behaviors ทั้งระบบ
- **ทำ:** Network/server errors, partial list loads, empty vs unauthorized, pagination/envelopes, double submit/stale requests, 360px/1280px, Safari month field, keyboard/focus/error announcements
- **ผ่านเมื่อ:** ผู้ใช้แก้/ลองใหม่โดยไม่เดา IDs, ไม่มี stale state ส่งข้อมูลผิด, sensitive actions ไม่เกิดซ้ำ, form/status copy ชัด; regressions มี runnable checks
- **ขึ้นกับ:** FLOW-054, FLOW-055

## 13. เปิดใช้งานจริงและส่งมอบ

### [ ] FLOW-057 — Backup/restore และ migration recovery [BUILD/VERIFY · P2]
- **ยังไม่พิสูจน์:** Automated backup/off-host retention/restore และ upgrade recovery ที่รันซ้ำได้
- **ทำ:** Backup policy, encrypted retention, restore บน isolated stack, RPO/RTO, forward migration/roll-forward/rollback runbook
- **ผ่านเมื่อ:** Restored rows/history/locked payroll/attachments ตาม policy ใช้ได้, rehearsal มีหลักฐานและไม่แตะข้อมูล production
- **ขึ้นกับ:** FLOW-042, FLOW-019, FLOW-001 retention decision

### [ ] FLOW-058 — Production secrets และ security hardening [BUILD/VERIFY · P2]
- **มีบางส่วน:** JWT/bank encryption, lockout/CSRF/server scopes; production readiness ยังไม่ครบ
- **ทำ:** JWT/key rotation/re-encryption rehearsal, TLS/cookies/origins, rate limits, dependency/image/secret/header checks, audit/payroll/attachment retention
- **ผ่านเมื่อ:** ใช้ secrets จริงที่ต่างจาก demo, rotation ยังอ่าน historical bank data ได้, throttling และ redaction ทำงาน; findings มีผลแก้/เจ้าของ
- **ขึ้นกับ:** FLOW-014, FLOW-017, FLOW-053

### [ ] FLOW-059 — Production deployment/monitoring/restart rehearsal [BUILD/VERIFY · P2]
- **ยังไม่พิสูจน์:** Build ผ่านไม่เท่ากับ deploy ผ่านพร้อม config และ persistence ทุก service
- **ทำ:** Structured redacted logs/request IDs, liveness/readiness, metrics/alerts; clean production Compose deployment, proxy/runtime config, restart/recovery และ service failures
- **ผ่านเมื่อ:** ขั้นตอนคู่มือรันบน clean versions ได้,เว็บ/API/storage/mail ถ้าใช้จริงทำงาน, restart ไม่ทำข้อมูลหาย; operator ตรวจ failures ได้
- **ขึ้นกับ:** FLOW-057, FLOW-058, FLOW-045 ตาม mail scope

### [ ] FLOW-060 — UAT, คู่มือ และเผยแพร่ revisions ที่ตรงกัน [VERIFY/DOCS · P0/P2]
- **ขาด:** ยังไม่มี sign-off ทุก role พร้อมหลักฐาน flow ครบและ status docs ที่ตรง implementation
- **ทำ:** UAT ตัวแทน 5 roles, known limits/operator runbook, acceptance evidence, update tasks/release checklist, ตรวจ root/submodule commits ให้เป็นชุดเดียวกันก่อนเผยแพร่
- **ผ่านเมื่อ:** แต่ละ in-scope task มีผลตรวจจริง, failures ปิดหรือมี scope exception ที่อนุมัติ, fresh-clone release rehearsal ผ่าน; การ update submodule pointers ทำเมื่อได้รับคำสั่งใน release task
- **ขึ้นกับ:** FLOW-053–056; ใช้เงินจริงต้อง FLOW-057–059 และ approved conditional features ผ่านด้วย

## ลำดับเริ่มที่แนะนำ

1. FLOW-001–003 เพื่อกำหนดเกณฑ์และ fixture ที่ใช้พิสูจน์งาน
2. ปิดสิ่งที่ผู้ใช้ติดอยู่: FLOW-006, FLOW-008, FLOW-009, FLOW-012–013, FLOW-037–039, FLOW-041
3. เดิน Employee/Attendance/Leave/OT/Finance และ Payroll ตาม dependencies
4. PDF/exports/adjustment/report/audit และ conditional payment scope
5. Browser tests/UAT แล้ว production operations ถ้าจะใช้เงินจริง

สามารถทำ bug fix เร่งด่วนอย่าง FLOW-006 หรือ FLOW-041 ก่อน FLOW-001–003 ได้
แต่ต้องกลับมาเพิ่ม fixture/acceptance checks ก่อนถือว่าปิด release

## สิ่งที่ไม่รวมอัตโนมัติ

OCR, เครื่องสแกนเวลา, direct bank API, native mobile, MFA, forgot-password email และ
session-device management ยังเป็นงาน deferred ตาม completion plan เดิม
งานเหล่านี้เริ่มเมื่อผู้ใช้เปลี่ยน scope ชัดเจน ไม่เอามาอ้างว่าเป็นช่องว่างบังคับใหม่

## หลักฐานล่าสุดและนิยามเสร็จ

Audit 13 ต.ค. 2026: backend PostgreSQL checks แยก process 445 pass/0 skip/0 fail,
frontend 40 pass, typecheck/lint/build ผ่าน; browser matrix และ complete acceptance journey
ยังไม่มีหลักฐานผ่านครบ งานที่มี implementation จึงระบุ VERIFY ไม่ใช่สั่ง rewrite

ทุก task ต้องจบด้วย: behavior ที่ผู้ใช้ทำได้จริง, server-side authorization,
history/transactions ถูกต้อง, runnable checks ตามความเสี่ยง, และหลักฐานจาก current revisions
ไม่ใช้จำนวน tests หรือ container healthy เพียงอย่างเดียวเป็นนิยามว่า feature เสร็จ

เอกสารประกอบ: `docs/release-readiness-audit-2026-10-13.md`,
`specs/012-system-completion/tasks.md`, `docs/release-checklist.md`
FLOW IDs เป็น task breakdown ใหม่ตาม journey ไม่แทน/เปลี่ยนเลข Txxx เดิมโดยอัตโนมัติ

## ผลหลังเผยแพร่ 14 ตุลาคม 2026

Implementation/automated verification ของ FLOW-001–045 และ 047–056 ผ่านตามหลักฐานใน `release-verification-2026-10-14.md` (049–050 ไม่ applicable) รวม WebKit Linux CI หลังแก้ auth navigation race. FLOW-046 ยังรอผู้รับบัญชีตรวจ format CSV จริงใน UAT; FLOW-057–060 ยังมี off-host/provider policy, vendor CVE review, hosting/alerts และ human sign-off ตาม `uat-checklist.md`. ไม่ถือว่าการ push คือ deploy หรือยอมรับ CVE.
