# Haris Payroll — รายการงานก่อนถือว่าใช้งานครบ

ตรวจวันที่ 13 ตุลาคม 2026 (Asia/Bangkok) จาก working tree ปัจจุบัน

## ข้อสรุป

ระบบมี backend และ tests จำนวนมาก แต่ยังไม่ครบในระดับผู้ใช้ทำงานผ่านเว็บตั้งแต่ต้นจนจบ
การมี API, container healthy หรือ unit tests ผ่าน ยังไม่ใช่หลักฐานว่าใช้งานครบทุก role
ไม่ควรให้เปอร์เซ็นต์ความพร้อมโดยยังไม่มี acceptance matrix ที่ผ่านจริง

รายงานนี้เป็น audit และ backlog ไม่ใช่การประกาศว่าฟังก์ชันทั้งหมดผ่านการตรวจแล้ว
ไม่ได้แก้ข้อมูลจริงหรือกำหนดสิทธิ์ให้บัญชีใด และไม่ได้ทำ browser sign-in รอบนี้

## หลักฐานที่รันใหม่

| การตรวจ | ผล | ขอบเขต |
|---|---|---|
| Backend `bun run typecheck` | ผ่าน | TypeScript |
| Backend `bun test` บน host | 420 pass, 27 skip, 0 fail | Database gates ยังไม่เปิด |
| Backend แยก process ต่อไฟล์ บน PostgreSQL disposable | 445 pass, 0 skip, 0 fail; 95 files | เปิด database gates และ fixture IDs; ไม่ใช้ database ของผู้ใช้ |
| Frontend `bun test` | 40 pass, 0 fail; 13 files | API adapters, helpers, role routing และ checks ที่มีอยู่ |
| Frontend `bun run lint` | ผ่าน | ทั้ง frontend |
| Frontend `tsc --noEmit` | ผ่าน | ทั้ง frontend |
| Frontend `bun run build` | ผ่าน | Production compilation/static generation; ไม่ใช่ deployment rehearsal |
| Browser journey ทั้ง 5 roles | ยังไม่มีผลตรวจครบ | ต้องเพิ่มและรันก่อน acceptance |

Backend checkout: `f8e0ab1a9ad66c19dc5e493bcd44f6ebc3834cc2` พร้อม uncommitted changes
Frontend checkout: `7aac774111928cab2ead8745fb235e43865229ad` พร้อม uncommitted changes
จึงไม่ควรนำหลักฐานนี้ไปอ้างว่ารันบน clean published commit แล้ว

Database validation ใช้ Compose project `haris-payroll-audit` บน PostgreSQL 16,
migrate และ seed ใน database แยก จากนั้นตั้ง `TEST_DATABASE_URL=DATABASE_URL`,
`A2_DATABASE_INTEGRATION=1`, `DATABASE_INTEGRATION=1` และ B1/B2 fixture IDs
แล้วรันแต่ละ `*.test.ts` ใน process แยก ตามข้อจำกัด lifecycle ของ test pool
ลบเฉพาะ audit stack/volumes หลังทดสอบแล้ว Development database เดิมยังอยู่

## P0 — ทำก่อน เพื่อให้ flow เงินเดือนจบได้

| ID | งาน | สิ่งที่ยืนยัน / เหตุผล | เกณฑ์ตรวจรับ |
|---|---|---|---|
| A01 | เชื่อมหน้าตารางเวลาและวันหยุด | `ScheduleHolidayControls` มีอยู่ แต่ไม่ถูก mount ในหน้าใช้งาน; สาขาใหม่ไม่มี schedule | HR/Owner ตั้งเวลาเริ่ม/เลิก, grace, effective dates, date override และวันหยุดผ่านเว็บได้ โดยใช้ชื่อร้าน/สาขา |
| A02 | รวมขั้นตอนเตรียมร้านและสาขา | ผู้ใช้พบ config missing แล้วจึงพบ schedule missing ทีละด่าน | แสดง readiness checklist ของร้าน/สาขา/งวด รวม config, schedule, assignment, attendance, approvals และ bank data ที่ export ต้องใช้ |
| A03 | ทำ provisioning บัญชีให้ครบ | สร้าง account แล้ว `grants=[]`; Settings สร้าง account ที่ไม่ผูก employee ได้ | แยกบัญชีพนักงานกับบัญชีส่วนกลาง, เลือก/สร้าง employee, กำหนด role/scope; ถ้าไม่ครบต้องบอกว่า account ยังไม่พร้อมใช้งาน ห้ามแจกสิทธิ์อัตโนมัติ |
| A04 | ทำหน้า Settings ให้กำหนดทุก scope ได้ | ฟอร์ม grant ส่ง `department_id: null` เสมอ จึงกำหนด Supervisor scope ไม่ครบ | EMPLOYEE ผูก employee; SUPERVISOR เลือก branch+department; BRANCH_MANAGER เลือก branch; HR/Owner ใช้ all scope ตามสิทธิ์ผู้กำหนด |
| A05 | โหลด payroll ที่บันทึกแล้วเมื่อเลือกงวด | ตารางใช้ `preview.records`; `loadWorkspace` และการเปลี่ยนงวดล้าง preview โดยไม่โหลด `getPeriod`; งวด locked กด preview ไม่ได้ | Preview/lock แล้ว refresh, logout/login หรือเปลี่ยนงวด ยังเห็น records/items ที่ persisted อยู่ รวม Branch Manager read-only |
| A06 | แก้คำอธิบาย payroll blockers | ข้อความ generic/English, employee ID, ไม่ชี้ config key หรือหน้าที่แก้ | ระบุพนักงาน/สาขา/วันที่/ค่าที่ขาด พร้อมลิงก์แก้; แยกยังไม่คำนวณ, ไม่มีพนักงานในช่วงงวด, มี blockers และพร้อมล็อก |
| A07 | ตรวจหน่วยและ effective coverage ของ config | UI readiness เช็กว่ามี key สัก row แต่ไม่เช็ก scope/date ของงวด; input placeholder เดียวใช้กับหลายหน่วย | แสดงหน่วยและตัวอย่างตาม key, validate domain bounds, ตรวจค่าที่มีผลรายวัน/สาขา; ห้ามใส่ค่าเงินเดือนหรืออัตราจริงแทนผู้ใช้โดยเดา |
| A08 | เตรียม demo fixture ที่ใช้เดินงานได้ | seed พื้นฐานและ backend fixtures ไม่ใช่ browser acceptance dataset ที่ครบทุก role | Fixture idempotent มี 2 branches/2 departments, 5 roles, accounts linked, schedules/config/attendance/finance และงวดทดสอบที่ครบ |
| A09 | ทำ journey ตั้งแต่เปิดระบบใหม่ถึง export | ยังไม่มี browser E2E configuration/suite ใน repo ที่ตรวจครบ flow นี้ | Fresh database → ตั้งองค์กร → onboarding → role → attendance → leave/OT/finance → preview → lock → payslip/export จบผ่านเว็บโดยไม่ใช้ SQL เติมข้อมูล |

งาน A01 ตรงกับ T016; A08–A09 ตรงกับ T006–T014 ใน completion plan เดิม
การ refresh รายการสาขาและคำอธิบาย employee scope ที่แก้ใน working tree เป็นเพียงบางส่วนของ A03–A04
ยังไม่ถือว่าปิด provisioning ทั้ง flow

## P1 — ให้ฟังก์ชันใน scope ใช้ได้ครบผ่านเว็บ

| ID | งาน | หลักฐาน/ช่องว่าง | เกณฑ์ตรวจรับ |
|---|---|---|---|
| A10 | Employee ขอเงินทดรองด้วยตนเอง | `/finance` เปิดเฉพาะ HR/Owner | Employee ขอ/ดูของตนเองได้; admin approval แยก; server ปฏิเสธข้อมูลคนอื่น |
| A11 | จัดการประเภทลาและ quota | มี read endpoints; ไม่มี workflow ครบสำหรับตั้งประเภท/จัดสรร quota | HR ตั้งและดู quota รายปี/พนักงานได้, deactivate ประเภทที่มี history อย่างปลอดภัย; แจ้ง quota ไม่พร้อมก่อนอนุมัติ |
| A12 | แสดงประวัติ Leave/OT และทำ corrections ตาม scope | มี history API แต่ไม่ได้เรียกแสดงใน workspaces; OT ยังไม่มี pending edit route | เห็นผู้ตัดสิน เวลา เหตุผล และ corrected leave type; แก้ OT ที่ pending ได้ตาม policy และไม่แก้ decided/locked history |
| A13 | ทำ adjustment ให้ครบ lifecycle | API adapter มี list/decide; หน้า Payroll มีเพียงฟอร์มขอ adjustment | ดู pending/history, เลือก original record/target period, approve/reject, เห็นการ applied โดยไม่แก้ locked record เดิม |
| A14 | เอกสารแนบพนักงาน/การลา | หน้า employee documents ระบุยังไม่เปิดใช้งาน | Upload/list/download ผ่าน authorized storage, size/MIME/hash checks, retention และ audit; ทดสอบข้ามพนักงานและไฟล์ไม่ถูกต้อง |
| A15 | สร้างและดาวน์โหลด PDF payslip จริง | Service ปัจจุบันสร้าง storage key `.json` และ hash ของ JSON summary; ไม่มี PDF download endpoint | เอกสารจาก locked snapshot มี storage จริง, immutable/versioned metadata และ own-only download; voided/tampered/duplicate cases ผ่าน |
| A16 | ส่ง payslip email จริงหรือประกาศโหมดจำลองให้ตรง | `addDelivery` insert `status: sent` โดยไม่มี mail provider call | ถ้าใช้อีเมลจริง ต้องมี provider, failed/sent attempts และ retry policy; ถ้า demo ต้องไม่แสดงว่าจัดส่งจริง |
| A17 | แทนช่อง raw IDs ด้วยตัวเลือกชื่อ | Attendance branch, debt type, adjustment records/periods, payslip record และ export period ยังมีช่อง ID | ไม่ต้องรู้ database IDs; scoped selectors, loading/error/empty states และ pagination ครบ |
| A18 | รายงานตาม product scope | หน้า Reports และ routes ปัจจุบันมี bank-transfer/social-security CSV | เติม attendance/leave/OT/debt/payroll summaries ตามที่ตกลง พร้อม server scopes และยอดตรงกับ locked snapshots |
| A19 | ทำ lifecycle รหัสชั่วคราว/บัญชีไม่มี role ให้ครบ | มี password-change งานล่าสุด แต่ไม่มี acceptance ของทั้ง flow | หลังสร้าง/reset บอกเปลี่ยนรหัสชัด, sessions/revocation ตาม policy, no-role ให้ recovery ที่ทำต่อได้; ไม่มี secrets ใน logs |
| A20 | ปิด UX ที่ทำให้กรอกผิด | month input บาง browser เป็น text, labels/error units และข้อความ English ยังเหลือ | รูปแบบเดือนชัดเจน, Thai date/money/status/error สม่ำเสมอ, validation ก่อน submit, ตัวเลือกชื่อ และ keyboard/mobile ใช้ได้ |

อ้างอิง completion plan T015, T017–T023, T025–T030, T057 และ T059
T022 เรื่อง password change มีงานใน working tree แล้ว จึงต้องตรวจและปิด flow ไม่ใช่สั่งเขียนซ้ำทั้งหมด

## Acceptance tests ที่ต้องมี แม้ unit tests ผ่าน

- [ ] A21 Browser role matrix: Employee own-only; Supervisor department; Manager branch; HR/Owner all-scope ตาม duty; ทั้งอนุญาตและปฏิเสธใน UI/API
- [ ] A22 Identity/HR journey: account ที่มี/ไม่มี employee, ไม่มี role, wrong scope, last Owner, disabled/locked account, reset/change password, session expiry และ logout
- [ ] A23 Effective-date journey: hire กลางเดือน, สาขาย้ายกลางงวด, salary/welfare เปลี่ยน, schedule/config เปลี่ยน, dates ไม่มี overlap และเก็บ historical branch
- [ ] A24 Leave/OT journey: 3 vs 4 วัน, quota, overlap, corrected type, rollback, explicit OT approval ทุกประเภท และ history หลังล็อก
- [ ] A25 Finance/payroll journey: advance วันที่ 19/20, worked days 19/20, half-salary cap, loan installment, food debt reversal, net pay negative, exact decimal/rounding, duplicate records และ locking concurrency
- [ ] A26 Locked-record journey: refresh แล้วอ่านได้, ordinary updates ถูกปฏิเสธ, adjustment ไปงวดถัดไป, payslip/CSV ตรงกับ snapshot และ unauthorized recipient ถูกปฏิเสธ
- [ ] A27 UI resilience: ทุกฟอร์มที่ผู้ใช้ต้องกรอกจริง, list pagination/envelopes, loading/error/empty, retry, rapid selector changes, mobile 360px/desktop 1280px, keyboard/focus/error announcements
- [ ] A28 CI: clean checkout + root/submodule revisions ถูกชุด, disposable PostgreSQL, migrations + fixture setup, process-isolated database tests, frontend tests/build และ browser E2E; เก็บหลักฐานและ fail เมื่อ expected checks ถูก skip

อ้างอิง T007, T013 และ T031–T037; ต้องทดสอบผ่านหน้าจอและข้อมูลจริงใน test database ไม่ใช่ mock API อย่างเดียว

## ก่อนใช้กับข้อมูลเงินจริง

- [ ] A29 Backup/restore, off-host retention, RPO/RTO และ migration/roll-forward rehearsal พร้อมหลักฐาน (T038–T039)
- [ ] A30 Production secrets/JWT/key rotation, TLS, rate limiting, redacted structured logs, readiness/alerts, dependency/image/secret scans (T040–T045)
- [ ] A31 Clean production deployment/restart/persistence rehearsal, configuration ของทุก service และ rollback (T046)
- [ ] A32 คู่มือ/operator runbook/update release checklist + task statuses ตามผลปัจจุบัน + UAT sign-off ตัวแทน 5 roles (T014, T047–T051)

## Scope ที่ต้องตกลงก่อนลงมือ

Completion plan ยังมี T058, T060–T065 ที่ต้องตัดสินใจ/อนุมัติ model ก่อน:

1. OT types เป็น 3 fixed values หรือ configurable
2. ต้องบันทึกจ่ายเงินจริง/เงินสด/ผลโอนและ reversal หรือระบบจบที่ CSV; locked ไม่ได้แปลว่า paid
3. การยื่น/ชำระประกันสังคมจริงอยู่ใน scope หรือจบที่ export
4. คำว่าใบแจ้งหนี้เป็น payslip หรือเอกสารอีกชนิด

Schema/migrations ยัง frozen: ห้ามเริ่มเปลี่ยน disbursement schema โดยถือว่า checklist นี้เป็นการอนุมัติ schema
OCR, เครื่องสแกนเวลา, direct bank API, native apps และ MFA/forgot-password/device management
เป็น scope ที่ defer ไว้ (T052–T056) ไม่ควรนำมาบวกเป็นข้อบังคับใหม่เพื่ออ้างว่า 100%

## ลำดับทำงานและนิยามเสร็จ

1. ปิด A01–A07 เพื่อแก้สิ่งที่ผู้ใช้ติดอยู่และไม่ให้ข้อมูลหายจากหน้า Payroll
2. เตรียม A08 และเดิน A09; เพิ่ม tests ที่พบ failure ก่อนแก้แต่ละจุด
3. ปิด A10–A20 และ scope decisions ที่จำเป็นต่อ use cases ที่ตกลง
4. ผ่าน A21–A28 บน clean published revisions; ไม่ใช้ container healthy หรือจำนวน tests แทน journey evidence
5. ถ้าจะใช้เงินจริง ต้องผ่าน A29–A32 และ UAT ก่อนเปิดใช้

แต่ละรายการจะติ๊กเสร็จได้เมื่อผู้ใช้ทำผ่านเว็บได้, ผลถูกต้องตาม business rules,
server ตรวจ scope, มีหลักฐานจาก test/acceptance ที่เหมาะกับฟังก์ชัน และคู่มือตรงกับระบบ
tests สีเขียวทั้งหมดเป็นเงื่อนไขจำเป็น แต่ไม่ใช่เงื่อนไขเพียงข้อเดียว
