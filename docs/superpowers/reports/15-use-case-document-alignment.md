# ตรวจความสอดคล้อง Use Case กับระบบหลังส่งมอบ

วันที่26ตุลาคม2026; source backendc2a404d/frontende6d6fb6, rootdevelop0b36631. ตรวจ source และเอกสารในเครื่อง ไม่ใช่การรัน browser/UAT ใหม่ ไม่แก้ไฟล์ academic ที่ผู้ใช้แก้ค้าง ไม่แก้โค้ด/commit/push ในงานตรวจนี้

## ข้อสรุป

ระบบสัมพันธ์กับ16Use Casesในภาพเดิมที่ใช้เป็นขอบเขต delivery และมี retained automated browser49scenarios ผ่านตาม actor matrix แต่รายงานวิชาการ `docs/sa-report/README.md` ซึ่งเป็น SOURCE ของ build_report.py ตอนนี้จัดเป็น20Use Casesคนละชุด จึงยังกล่าวว่ารายงานปัจจุบันกับระบบตรงทุกขั้นตอน/ทุกactorไม่ได้ เลขUCตรงกันไม่ได้แปลว่าหน้าที่เดียวกัน

ตัวอย่าง: UC01ภาพเดิม=สร้างพนักงาน แต่ UC01รายงานปัจจุบัน=เข้าสู่ระบบ; UC15ภาพเดิม=ยื่นลา แต่ UC15รายงานปัจจุบัน=คำนวณเงินเดือน. `report-uc-crosswalk.json` ที่มีอยู่ map academicชุดก่อน34รายการ→20รายการ ไม่ใช่16รายการในdelivery→20รายการ จึงไม่แทนตารางเทียบนี้

## ประเด็นที่ต้องปรับก่อนใช้รายงานเป็นเกณฑ์เดโม

| ระดับ | ประเด็น | เอกสาร / หลักฐานโค้ด | วิธีทำให้ตรงกัน |
|---|---|---|---|
| สำคัญ | UC07ให้พนักงานบันทึก/แก้ลงเวลาเอง แต่ EMPLOYEE เข้า attendance ไม่ได้ และ action manage ไม่อนุญาต self grant | reportREADME:679–684; frontend/lib/auth/route-access.ts:56–57; backend/src/features/employee/employee.operation-context.service.ts:12–20 | หากคง behaviorปัจจุบัน ระบุ actor HR/OWNER/BRANCH_MANAGER/SUPERVISOR ตามscope; ถ้าต้องการemployeeclock-in/out ต้องพัฒนาและทดสอบเพิ่ม ไม่ใช่เพียงเพิ่มเมนู |
| สำคัญ | รายงาน20UCไม่มี flowเตรียมจ่าย/เลือกช่องทาง/กลุ่มสาขา/QR/manualconfirm/cancel/history; UC18อธิบายเพียง export | reportREADME:923–943; backend/src/features/payroll/payroll-payment.routes.ts:20–25; frontend/components/payroll-payments.tsx | เพิ่ม usecaseเตรียมและบันทึกการจ่ายเงินเดือน หรือขยายUC18ให้ครอบคลุมจริง พร้อม BP/diagram/CRUD/sequence ที่สัมพันธ์; การโอนเงินจริงยังภายนอกแต่การเตรียมและบันทึกpaidอยู่ในระบบ |
| ต้องแก้เงื่อนไข | UC08บอกโควตาไม่พอให้แก้ก่อนส่ง แต่ submitLeave ไม่ตรวจ quota; approvalตรวจ quotaและallowExceedอาจเป็นลาไม่รับค่าจ้าง | reportREADME:705–708; backend/src/features/leave/leave.service.ts:42–55,95–146 | เขียนว่ารับคำขอpendingแล้วตรวจโควตา/ผลpaid-unpaidตอนอนุมัติ; ถ้าต้องการปฏิเสธตั้งแต่submit ต้องเพิ่มกฎใหม่ให้ชัด |
| ต้องแยกสอง workflow | UC12ระบุกรอกเหตุผลและปฏิเสธต้องมีเหตุผลรวมทั้งadvance/loan แต่ advanceส่งได้เพียงemployee_id/amount; rejectnoteoptional และUIส่งว่างได้ | reportREADME:791–795; backend/src/features/advance/advance.routes.ts:7,13–15; frontend/app/(dashboard)/finance/page.tsx:79 | แยกข้อกำหนดเงินกู้กับเงินทดรอง; หากต้องการเหตุผลบังคับทั้งคู่ ต้องเพิ่มform/API/validationตามข้อกำหนด ไม่อ้างว่ามีแล้ว |
| ต้องเติมactorตามขอบเขต | UC04ระบุแค่HR/OWNER ทั้งที่ระบบและภาพ16เดิมให้managerสร้าง/แก้/ยุติพนักงานในสาขาตนด้วย | reportREADME:613; frontend/lib/auth/route-access.ts:52–55; backend/src/features/employee/employee.scope.ts:53; employee-management.e2e.ts | เพิ่มmanagerเฉพาะงานown-branchCRUD แยกจากbank/account/compensation-history administrationที่ยังสงวนสิทธิ์ |
| ต้องอัปเดตแบบจำลอง | รายงานระบุ36entities/79FKและไม่มีตารางใหม่loan_requests/payroll_payments/revoked_session_tokens ขณะที่DBMLเต็มมี39tables | reportREADME:1014; haris-payroll-postgresql.dbml:106,355,480 | อัปเดตERD/DataDictionary/CRUD/query ที่เกี่ยวข้อง หรือระบุภาพย่ออย่างชัดเจน; อย่าใช้จำนวนเดิมเป็นโมเดลเต็มของเวอร์ชันส่งมอบ |

ข้อควรทำให้ชัดเพิ่ม: UC17 actor employee หมายถึงอ่าน/ดาวน์โหลดของตน ไม่ใช่ออก/ส่งสลิปแทนHR; UC19ต้องระบุหน้าที่ของแต่ละrole เพราะ /dashboard เป็นพื้นที่ลิงก์งาน ส่วน financial reports /reports เปิดเฉพาะHR/OWNER ไม่ใช่ทุกroleส่งออกข้อมูลการเงินได้; HRจัดการroleOWNERไม่ได้ตามcanAdministerRole

## ตารางตรวจ20Use Casesปัจจุบัน

คำว่า “สัมพันธ์” ในตารางนี้หมายถึงพบ implementation/behaviorที่รองรับเป้าหมายจาก source และหลักฐานเดิม ไม่ใช่ UATใหม่ครบทุกalternativeของ20UC

| UCในรายงานปัจจุบัน | ผลตรวจเทียบความหมาย |
|---|---|
|01เข้าสู่ระบบ/รหัสผ่าน|สัมพันธ์; retained5role session tests และ password flows; no-grant account-stateต้องแยกจากself-serviceauthority|
|02โครงสร้างองค์กร|สัมพันธ์; organizationCRUD/archive และscopeในimplementationเดิม|
|03บัญชี/สิทธิ์|สัมพันธ์; ต้องคงข้อจำกัดHRมอบOWNERไม่ได้และตรวจrole/scope|
|04ข้อมูล/ประวัติพนักงาน|สัมพันธ์แต่actorไม่ครบ: managerownbranchCRUDไม่มีในตารางacademic|
|05ตาราง/วันหยุดสาขา|สัมพันธ์; effectivehistoryและlocked-dateguards; managerมีบางสิทธิ์เพิ่มจากactorที่ระบุ|
|06นโยบายเงินเดือน/การลา|สัมพันธ์; configuration/leaveadministration/quotaมีworkflow ไม่ใช่แก้frozenhistory|
|07บันทึก/แก้ลงเวลา|actorEMPLOYEEไม่ตรงสิทธิ์จริง ต้องแก้เอกสารหรือเพิ่มfeature|
|08ยื่นลา|ฟังก์ชันมีจริง แต่จังหวะตรวจquota/allowExceedในข้อความไม่ตรง|
|09พิจารณาลา|สัมพันธ์; supervisor3วัน/managerdirectapproval/history; HR/OWNERอนุมัติได้ด้วยตามสิทธิ์|
|10ยื่น/แก้OT|สัมพันธ์; pendingeditและapprovedimmutable; ใช้จำนวนชั่วโมง/จำนวนวันตามชนิด ไม่ใช่สมมติว่ามีstart/endOTทุกแบบ|
|11พิจารณาOT|สัมพันธ์; authorization/pending/locked-date/history|
|12เงินทดรอง/เงินกู้|มีทั้งสองจริง; เงื่อนไขreason/requiredrejectionnoteต้องแยกตามข้างต้น|
|13หนี้/รายการปรับ|สัมพันธ์; append-onlydebtและapprovedadjustment/current/locked-origin|
|14เปิดงวด|สัมพันธ์; HR/OWNERUIสร้างรอบและข้อมูลassignment|
|15คำนวณ/ตรวจเงินเดือน|สัมพันธ์; dailyrates/earnedSS/preview; retainedhistory/calculationchecks|
|16readiness/lock|สัมพันธ์; missingattendance/pending/negative guards และimmutablelockedvalues|
|17ออก/ส่ง/รับสลิป|สัมพันธ์เมื่อแบ่งHR/OWNERgenerate-send กับemployeeown-downloadชัด|
|18รายงาน/ไฟล์จ่าย|exportsมีจริง แต่ไม่ครอบคลุมpaymentworkflowใหม่ในรายงาน|
|19ภาพรวม/รายงานตามสิทธิ์|สัมพันธ์แบบกระจายหน้า; /dashboardเป็นnavigation ไม่ใช่financialdashboardทุกrole ต้องระบุrole/actionให้แน่นอน|
|20ประวัติการดำเนินงาน|สัมพันธ์; /auditและbackendauditserviceสำหรับHR/OWNER พร้อมfilters/pagination|

## Crosswalk ภาพ16รายการเดิมกับรายงาน20รายการ

| ภาพเดิมที่ส่งในแชท | รายงานปัจจุบัน | สิ่งที่ต้องระวัง |
|---|---|---|
|Loginแยกจากภาพ|UC01|เลขUC01ไม่ได้หมายถึงสร้างพนักงานอีกแล้ว|
|UC1สร้าง/UC2แก้/UC3ลบพนักงาน|UC04|ลบคือยุติการจ้างเก็บประวัติ; เพิ่มmanagerownbranchactor|
|UC4สร้างรอบ|UC14|ชื่อ/เลขเปลี่ยนแต่เป้าหมายตรง|
|UC5รายการปรับ|UC13|รวมกับdebt; currentperiod/lockedcorrectionต้องระบุ|
|UC6ปิดรอบ|UC15–16|แยกpreview/readiness/lock|
|UC7จ่าย/UC8ช่องทาง/UC9–11กลุ่มสาขา|ยังไม่มีflowครอบคลุมใน20UC|UC18exportsไม่ใช่paymentlifecycle; ต้องเพิ่ม/ขยายusecase|
|UC12สลิป/UC13อีเมล|UC17|employeeอ่านของตน ส่วนHR/OWNERออก/ส่ง|
|UC14PDFเงินเดือน/เจ้าหนี้|UC18|ระบุสองPDFและเจ้าหนี้=salarypayable;ไม่ใช่employee-debt|
|UC15ยื่นลา|UC08และUC09approval|quota timingต้องตรงbehavior|
|UC16กู้/เบิก|UC12|reason/decisionnoteคนละcontractในสองworkflow|

## ข้อจำกัดการตรวจ

ใช้Markdownต้นทางที่build_report.pyอ่าน, catalog/crosswalk และsourceที่mergeแล้ว ไม่ได้เปิด/แก้binaryDOCXหรือrenderภาพทุกdiagram; จึงไม่รับรองว่าbinaryDOCXล่าสุดเหมือนMarkdownทุกบรรทัด ไม่รันชุด540/54/49ซ้ำเพราะไม่มีimplementationเปลี่ยน รายงานทดสอบเดิมอ้างอิงภาพ16รายการและsupportingregressions; ไม่ยกระดับเป็นใบรับรอง20UCใหม่โดยอาศัยเลข49อย่างเดียว

ข้อเสนอแนะ: เลือกcatalog20เป็นทะเบียนหลักเมื่อใช้รายงานacademicปัจจุบัน แล้วsync actor/mainflow/alternatives/BP/ERD/diagrams/testmatrixตามข้อแตกต่างข้างต้น โดยรักษาcrosswalk16→20เพื่ออธิบายงานส่งมอบเดิม ไม่เปลี่ยนโค้ดให้ตรงประโยคที่ยังไม่ยืนยันนโยบายโดยอัตโนมัติ
