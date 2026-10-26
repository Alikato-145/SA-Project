# Current20 delivery summary

สถานะ: implementation, disposable-system acceptance และ independent scoped review ผ่านแล้ว; backend/frontend fast-forward และ push develop แล้ว root delivery รวมเอกสารและsubmodule pointersสำหรับdevelopตามคำสั่งผู้ใช้ รายงานนี้ไม่อ้างผล hosted CI ล่วงหน้า

## ผลงาน

ระบบอิงทะเบียนปัจจุบัน [20 use cases](../../sa-report/evidence/use-case-catalog.json) และ [73 actor/action rows](../../sa-report/evidence/current20-actor-matrix.json) แยกจาก delivery16 และ academic34 เดิมโดยมี crosswalk คนละชุด

- UC07: พนักงานบันทึก/แก้ลงเวลา manual ของตนเองได้ภายใต้ EMPLOYEE/self ที่เชื่อมพนักงานจริง ใช้สาขาตามวันที่และเวลาเข้างานตามตาราง ห้ามแก้รายการลา/import/exception/งวดล็อกและข้อมูลผู้อื่น มีเหตุผลแก้ไขและ audit
- UC08: ตรวจ quota ทุกปีที่เกี่ยวข้องก่อนยื่น/แก้ ไม่จองหรือหักจนอนุมัติ การอนุมัติตรวจซ้ำ; allow_exceed ยกเว้นเฉพาะเพดาน โดยต้องมี quota ที่ไม่ถูก freeze
- UC12: เหตุผลคำขอเงินทดรองและเหตุผลปฏิเสธรายการใหม่ต้องไม่ว่าง ยาว1–1000ตัวอักษร เก็บเหตุผลหลัง reload; ประวัติเก่า NULL ยังแสดงตามจริง ไม่แต่งข้อมูลย้อนหลัง
- เพิ่ม UI acceptance สำหรับองค์กร/บัญชี/ประวัติพนักงาน/ตาราง/นโยบาย/หนี้/audit และการปฏิบัติงานตามขอบเขตของผู้อนุมัติ รวมทั้งเปลี่ยนรหัสผ่านจริงของทั้ง5บทบาท
- ปรับรูปเล่มและแบบจำลองให้สัมพันธ์กับ20IDs:39tables/91FK/25enums/7migrations,23sequence+collaboration scenarios,24query mappings,158ภาพที่อ้างอิง พร้อม payment lifecycle และ frozen destinations
- [คู่มือผู้เริ่มต้นทั้ง20UseCases](../../user-guide/README.md) อธิบาย prerequisites, role/scope, เมนู/ฟอร์ม/ปุ่ม, ผลสำเร็จและวิธีแก้กรณีติดเงื่อนไข

## หลักฐานการตรวจ

| Gate | ผล |
|---|---|
| Backend types/full disposable PostgreSQL suite |598ผ่าน/0fail/0skip,123files|
| Frontend unit/lint/types/build |55ผ่าน;ทุกคำสั่งexit0|
| Final unfiltered browser |69ผ่าน/0fail/0skip/0flaky,21.1นาที,1worker/0retry;20261026T052214Z-27083|
| Source freeze |578ไฟล์ก่อน/หลัง full69 ตรงกัน; หลังreviewแก้เฉพาะ1E2E, runtime+อีก577ไฟล์เดิม|
| ดาวน์โหลดและตรวจ bytes |12PDF/4CSV/2Mailpit attachments/2QRpayloadsผ่าน|
| รูปเล่ม |298หน้า ตรวจทุกหน้า;484cached referencesตรง ไม่มีหาย/ผิด; DOCX/PDF hashesในmanifest|

รายละเอียดคำสั่ง/กรณีล้มเหลวและการแก้ fixture/font อยู่ใน [รายงาน19](19-current20-actor-uat.md), [acceptance manifest](../../sa-report/evidence/current20-acceptance-manifest.json) และ [artifact QA](../../sa-report/evidence/current20-artifact-qa.md) ไม่ใช้focusedผ่านบางส่วนแทนผลชุดเต็ม69กรณี ผล64กรณีเดิมเก็บเป็นpre-refinementเท่านั้น

เงินเดือนเจ้าหนี้ใช้ผลล็อกเดียวกับสลิป: รวม31800.00/ตัวกรอง7600.00; bankCSV15200.00ใช้ปลายทางsnapshot; ประกันสังคมใช้earned-base12000/4000และหัก600/200 ไม่ใช่ฐานสัญญา30000.00 สลิปที่ดาวน์โหลดตรงกับbytesที่Mailpitรับทั้งHR/OWNER การจ่ายแยกยอด175.03/จ่าย150.03/ค้าง25.00และรักษารายการยกเลิก QRถอดรหัสและตรวจTLV/CRCแยกกันแล้ว แต่ไม่ใช่หลักฐานว่าโอนสำเร็จ

## Schema และข้อมูลเดิม

Schema owner ตรวจและอนุมัติ0006เฉพาะ nullable advance_requests.reason แล้วใช้กับฐานทดสอบเท่านั้น:48รายการเงินทดรองเก่ายังNULLทั้งหมด fingerprintsของ48advances/1015locked payroll records/11927itemsตรงก่อนและหลัง ไม่มีแก้ historical facts หรือฐานจริง รายงาน [16](16-uc07-self-attendance.md), [17](17-uc08-quota-precheck.md), [18](18-uc12-advance-reasons.md) และreviewของแต่ละงานเก็บหลักฐานขอบเขต/ข้อจำกัดไว้

## การตัดสินใจและต้นทุน

| Decision | เหตุผล | ต้นทุน/การควบคุม |
|---|---|---|
| ใช้workspaceเดิม+featurebranches |รักษาเอกสารผู้ใช้ที่ยังไม่commit/dependencies/verification binds|file isolationน้อยลง; single writer, backup, explicit staging|
| เดินหน้าตามconcrete designโดยไม่ถามroutine approvalซ้ำ |ผู้ใช้สั่งแก้และอนุญาตทำต่อ/push developชัดเจน|หากผู้ใช้เปลี่ยนนโยบายอาจต้องแก้ตาม; บันทึกdefaultทุกจุด|
| allow_exceedต้องมีquotaไม่freeze |ตรงกับapprovalเดิมและรักษาข้อมูลสิทธิ์|ต้องตั้งquotaก่อนยื่น แม้นโยบายยอมเกินเพดาน|
| CI timeout25→45นาที |browserอย่างเดียว21.1นาที ยังมีbuild/598DBtests|jobค้างใช้ได้เพิ่ม20นาทีแต่จำกัด45; pushเฉพาะdevelopลดCIซ้ำ|

## ขอบเขตที่ยังต้องตรวจเมื่อใช้งานจริง

ผลนี้เป็นautomated acceptanceบนdisposable stack ไม่แทนhuman UAT/production configuration/ทุกbrowser engine ไม่โอนเงินจริง ไม่ส่งอีเมลภายนอก ไม่deploy บัญชีใช้HRเดิม; โทรศัพท์PromptPayรับเงินแยกจากcontact; QRไม่ทำให้สถานะpaidเอง; externalSMTPต้องตั้งจริงก่อนใช้ การเปลี่ยนรหัสคงsessionปัจจุบันตามนโยบายเดิม ส่วนlogoutเพิกถอนsessionนั้นและปฏิเสธcopiedtoken

Unrelated user filesและประวัติเดิมรักษาไว้; rawcredentials/traces/CSV/mail payloadsไม่publish มีacademicUC08preconditionที่เขียนกว้างแต่alternativeระบุquota_type=noneถูกต้อง และexisting pg parallel-query deprecation warningระดับMinor ไม่ขยายงานเป็นrefactor Automation30นาทีคงPAUSED

## Integration record

Independent Task1–4 reviews PASS/Approved; Task5 initial findings และ final broad reviewทั้ง4จุดแก้ในหนึ่งwave แล้ว [sole scoped re-review](20-current20-scoped-rereview.md) Approved, Task5 SPEC PASS/QUALITY Approved

ก่อนintegration remote developยังอยู่fixedbasesเดิม backend/frontend fast-forwardโดยไม่แก้runtimeเพิ่มและpushสำเร็จ:

- backend: `54f78ea1b3e1e43fe87905f08a89a6db996538a8`
- frontend: `eca9ec9ad337bada1a8d3c8249f6cf0cd5c6376c`
- root: commitที่มีรายงานฉบับนี้และsubmodule pointersข้างต้น; [develop history](https://github.com/Alikato-145/SA-Project/commits/develop) ระบุSHAของrootที่เผยแพร่

ไม่มีforcepush/deploy; ใช้normal fast-forward และตรวจremoteSHAsหลังpush Hosted CIยังไม่ยืนยันในเวลาปิดรายงาน; localverificationผ่านตามหลักฐานข้างต้น

## Post-review bounded fix wave

แก้คู่มือ3จุด: แนบเอกสารเฉพาะคำขอลาก่อนอนุมัติ, สร้างพนักงานก่อน self grant, และตัวเลือกหักค่าจ้างของประเภทลา แก้1E2Eให้ก่อนวันที่20ทดสอบ422/ไม่มีรายการบันทึก แทนบังคับวันที่≥20; วันที่มีสิทธิ์คงpositiveflowsเดิม Focusedbrowser2/2ผ่าน40.9sวันที่26Oct ไม่อ้างว่าเห็นearly-monthbrowserจริง ดู [post-review delta](../../sa-report/evidence/current20-post-review-test-delta.json) และ[scoped re-reviewที่Approved](20-current20-scoped-rereview.md) ไม่เปลี่ยนruntimeหรือปลอมเวลา
