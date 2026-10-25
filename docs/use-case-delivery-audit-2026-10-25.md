# ผลตรวจความพร้อมส่งมอบ Use Case ของ Haris Payroll

## อัปเดตหลัง delivery — 25 ตุลาคม 2026

Task11 implementation พร้อม independent review: browser UAT ครบทุกไฟล์ตามค่า default ผ่าน **49/49,0fail,0skip** ในการรันเดียว10.9นาที บนข้อมูลสมมติชุดใหม่; backend guardedDB **538/0skip/0fail**, frontend unit52/lint/types/build ผ่าน ไม่มีการเปลี่ยน production protection หรือ schema ใน Task11

Login ทั้ง5roleและ Login/UC1–16 ที่ต้องมี UI action ถูก map แยกตาม actor ใน [actor matrix](superpowers/use-case-actor-matrix.md): HR/OWNER/manager CRUDตามscope, HR/OWNERเปิด-ปรับ-ล็อกงวด/เตรียมกลุ่ม-ยืนยันจ่าย/สลิป-อีเมล-PDF, employeeยื่นลา/กู้/advanceจริงพร้อมreloadและdirectscope denials Advanceทดสอบวันที่25October2026 มี25วันทำงานผ่านเกณฑ์จริง

หลักฐานและรอบผิดพลาดก่อนหน้าเก็บใน [รายงาน Task11](superpowers/reports/11-full-use-case-uat.md); [BP/คู่มือตามบทบาท](superpowers/use-case-delivery-handover.md) แยกขั้นตอนในเว็บกับการจ่ายเงินจริงภายนอกภายในแต่ละขั้น [schema summary](superpowers/use-case-schema-summary.md) ใช้อธิบายERDเฉพาะusecaseโดยไม่ลดโมเดลฐานข้อมูลจริง เอกสาร academicเดิมไม่ได้ถูกเขียนทับ

ข้อจำกัดยังคงอยู่: Mailpitพิสูจน์เฉพาะSMTP/กล่องรับภายในและattachmentตรงกัน ไม่รับรองinboxภายนอก; QR/CSVเป็นการเตรียมจ่าย ไม่ใช่bankexecution/หลักฐานโอน; creditor summaryคือเงินเดือนที่ร้านต้องจ่าย การตรวจรับผู้ใช้จริงและfresh Task11/whole-branch reviewยังเป็นgateแยก Rootเป็นผู้ปิดงานและautomationหลังผ่านทุกgate

## Baseline audit ก่อน implementation — เก็บประวัติเดิม

ข้อความและตารางต่อไปนี้เป็นผลตรวจครั้งแรกก่อนเติมdelivery มิใช่สถานะปัจจุบัน ใช้คู่กับอัปเดตและหลักฐานด้านบน

วันที่ตรวจ 25 ตุลาคม 2026 เปรียบเทียบกับ Use Case Diagram ล่าสุดที่ผู้ใช้ให้มา 16 รายการ และเพิ่ม Login เป็นรายการตรวจอีกหนึ่งรายการ ตรวจ source ปัจจุบันทั้ง frontend และ backend รวมถึง route access, API, service, persistence queries และชุดทดสอบที่มีอยู่

**ข้อสรุป: ยังส่งมอบโดยอ้างว่าทำได้ครบทุก Use Case และทุก role ตามภาพไม่ได้** มีทั้งฟังก์ชันที่ยังไม่มี ฟังก์ชันที่ทำงานคนละความหมาย และสิทธิ์ที่ไม่ตรงกับ actor ในภาพ ผลนี้เป็นการตรวจ source ร่วมกับการรัน unit tests และ static checks ไม่ใช่ผล UAT บนเว็บกับฐานข้อมูลจริง

อัปเดตภายหลังการยืนยันข้อกำหนด: ฝ่ายบัญชีใช้ HR เดิม และสรุปเจ้าหนี้หมายถึงยอดเงินเดือนที่ร้านต้องจ่ายทั้งรวม/รายบุคคล ขณะนี้เปิดชุดทดสอบแยกและรัน database suite 477 ผ่านโดยไม่ข้าม พร้อม browser 8 scenarios ผ่านแล้ว แต่พบ AUTH-01 ว่า token ที่คัดลอกไว้ยังใช้ได้หลัง Logout รายละเอียดอยู่ใน [ผล Subtask 2](superpowers/plans/2026-10-25-login-verification-results.md) ตัวเลขและข้อจำกัดด้าน runtime ในส่วนผล audit ด้านล่างเป็นผลรอบแรกก่อนเปิด Docker ไม่ใช่ผลล่าสุด

อัปเดต implementation: AUTH-01 แก้แล้วและผ่าน independent review; DB484/0skip/0fail, frontend45, logout browser2, live5role และ backend-restart revocation ผ่าน รายละเอียดล่าสุดใน [progress ledger](superpowers/use-case-delivery-progress.md) และ [รายงาน AUTH-01](superpowers/reports/02-auth-logout-implementation.md) งานสิทธิ์พนักงานตามสาขากำลังดำเนินการ; ตาราง audit ด้านล่างเก็บเป็น baseline ไม่ใช่สถานะงานล่าสุด


## ขอบเขตและ revision

- Root HEAD `174b957dc5f6504b2d64ff21900eeb1ba22b83fd`
- Backend HEAD `4feea540537fcddb5a75b129533a5fbc64cd3072`
- Frontend HEAD `2d799485cf1766a54fffc875ac09b2ebe2773f82`
- ตรวจ working tree ที่มีอยู่ โดยไม่แก้ application source, schema, migration หรือข้อมูลผู้ใช้
- การจัดทำ BP และตาราง mapping ก่อนหน้านี้เป็นการอธิบายกระบวนการตามโจทย์ ไม่ใช่หลักฐาน implementation ผ่านการทดสอบ เอกสารดังกล่าวต้องปรับตามการตัดสินใจเรื่องขอบเขตหลังทราบผลตรวจนี้
- สถานะ “มี” ด้านล่างหมายถึงพบ UI/API/logic ที่รองรับตามความหมายที่ระบุ ยังไม่หมายถึง browser acceptance ผ่านในรอบนี้

## ตารางตรวจครบทุก Use Case

| รายการ | ผลเทียบกับข้อกำหนด | URL และพฤติกรรมที่มี | สิทธิ์จริง / สิ่งที่ขาด |
|---|---|---|---|
| Login | มีสำหรับ 5 role ที่ระบบรู้จัก | `/login` → session cookie → `/auth/me` | EMPLOYEE, SUPERVISOR, BRANCH_MANAGER, HR, OWNER; ไม่มี ACCOUNTING แยก |
| 1 สร้างพนักงานใหม่ | บางส่วน เพราะ actor ไม่ครบ | `/employees/new` → `POST /api/v1/employees/onboard` | HR และ OWNER ทำได้; BRANCH_MANAGER ไม่ได้ แม้สาขาตนเอง |
| 2 แก้ไขพนักงาน | บางส่วน เพราะ actor ไม่ครบ | `/employees/{id}` → PATCH employee; หน้าประวัติการจ้าง/ธนาคาร/วันหยุดแยก | HR และ OWNER เขียนได้; BRANCH_MANAGER อ่านในสาขาตนเอง แต่แก้ไม่ได้ |
| 3 ลบพนักงาน | บางส่วน ต้องนิยามการลบ | `/employees/{id}` → เปลี่ยนสถานะ → PATCH status | HR/OWNER เปลี่ยน inactive/suspended/terminated ได้; ไม่มี DELETE; BRANCH_MANAGER ไม่ได้ ควรใช้ยุติการใช้งานเพื่อคงประวัติ |
| 4 สร้างรอบเงินเดือน | มีสำหรับ HR/OWNER | `/payroll` → create period → preview | กำหนดเดือนและช่วงวันเต็มเดือน; ยังไม่รองรับ ACCOUNTING เป็น role แยก |
| 5 เพิ่มรายการปรับ | บางส่วน ความหมายต่างจาก BP | `/payroll` → รายการปรับปรุงหลังล็อกรอบ | HR/OWNER ต้องเลือกรายการต้นทางที่ล็อกแล้ว และงวดปลายทางภายหลังในร้านเดียวกัน ไม่ใช่เพิ่มรายได้/เบี้ยขยันทั่วไปในงวดแรก |
| 6 ปิดรอบเงินเดือน | มีในความหมาย lock | `/payroll` → ล็อกรอบ | HR/OWNER; ตรวจ readiness, pending approvals, attendance และยอดสุทธิ; lock ไม่ได้หมายถึงจ่ายเงินแล้ว |
| 7 จ่ายเงินเดือน | ยังไม่มี workflow ตาม BP | ไม่มีปุ่มจ่าย/ยืนยันจ่ายแล้วหรือ payout endpoint | ไม่มี payment reference, รายการชำระจริง หรือสถานะจ่ายครบสาขา; preview/lock/CSV ไม่แทนการจ่าย |
| 8 เลือกช่องทางจ่ายเงิน | ยังไม่มี | ไม่มีช่องเลือกเงินสด/โอน/PromptPay | ไม่มี channel field, API และ UI ที่ครบวงจร |
| 9 แบ่งกลุ่มการจ่ายตามสาขาแบบเงินสด | ยังไม่มี | ไม่มี cash group/export | ไม่มีรายชื่อกลุ่มเงินสด ยอดรวมกลุ่ม และสถานะจ่ายรายสาขา |
| 10 แบ่งกลุ่มการจ่ายตามสาขาแบบเงินโอน | มีเพียงบางส่วน | `/reports` → bank-transfer CSV | HR/OWNER; ส่งออกทั้งร้านตามงวด ไม่ใช้ branch filter ไม่มี branch column/group และไม่มี QR |
| 11 แบ่งกลุ่มการจ่ายตามสาขาแบบเงินประกันสังคม | มีเพียงบางส่วน | `/reports` → social-security CSV | HR/OWNER; เป็นรายงานหักประกันสังคมทั้งร้าน ไม่มี member/non-member classification หรือกลุ่มจ่ายรายสาขา |
| 12 สร้างสลิปเงินเดือน | มีสำหรับ HR/OWNER | `/payslips` → งวดล็อก → ออก/เปิดสลิป → PDF | ต้องมี locked payroll record; สร้างซ้ำคืนฉบับเดิม; employee ดู PDF ของตนได้ |
| 13 ส่งสลิปทางอีเมล | มี source ต้องทดสอบ runtime จริง | `/payslips` → ส่งสลิป → delivery logs | HR/OWNER; ใช้ SMTP จริง ต้องมีค่าตั้งและทดสอบกล่องรับที่ได้รับอนุญาต; sent หมายถึง SMTP ยอมรับ ไม่ใช่ยืนยันเข้ากล่องรับ |
| 14 สร้าง PDF สรุปเงินเดือนและสรุปเจ้าหนี้ | ยังไม่มีตามรูปแบบ/ผลลัพธ์ที่ระบุ | มี summary JSON/CSV และรายละเอียด payroll/debt | ยังไม่มี payroll-summary PDF และ creditor-summary PDF; PDF สลิปรายบุคคลไม่แทนเอกสารสองอย่างนี้ |
| 15 ยื่นคำขอลา | มีสำหรับ employee ของตน | `/leave` → POST leave request → pending/history/attachments | ต้องผูก employee_id และ EMPLOYEE grant; ผู้อนุมัติใช้ scope และกฎ 3 วัน; ต้องทดสอบส่งฟอร์มด้วย employee จริงเพิ่ม |
| 16 ยื่นคำร้องเงินกู้/เบิกล่วงหน้า | มีเฉพาะ advance self-service | `/finance` → ส่งคำขอเงินทดรองจ่าย | employee ขอ advance ได้; loan form/API เป็น HR/OWNER สร้างเงินกู้ที่อนุมัติทันที ยังไม่มี employee loan request |

## สิทธิ์ของ actor ตามภาพเทียบกับระบบ

| Actor ในภาพ | Role จริง | ทำได้ปัจจุบัน | ข้อจำกัด |
|---|---|---|---|
| HR | HR scope all | Employee create/edit/status, payroll, adjustments, payslip, email, reports, finance admin | ได้งานมากกว่าที่ผูก HR ไว้ในภาพ; ยังคงไม่มี payout/channel/group/PDF summary |
| บัญชี | ไม่มี ACCOUNTING canonical role | ถ้าบุคลากรฝ่ายบัญชีได้รับ HR grant จะใช้ความสามารถของ HR ได้ | เป็นการ map ตำแหน่งงานกับ role; ยังไม่มี role บัญชีที่แยกหน้าที่ ต้องยืนยันก่อนทำบัญชีทดสอบ ห้ามอ้างว่า login ไม่ได้เพียงเพราะชื่อตำแหน่งบัญชี |
| ผู้จัดการสาขา | BRANCH_MANAGER scope branch | อ่านพนักงานในสาขา, ลงเวลา, พิจารณาคำขอ, payroll read-only | UC1/2/3 ไม่ได้; รายงานและออก/ส่งสลิปไม่เปิดให้ role นี้ |
| เจ้าของร้าน | OWNER scope all | Employee CRUD ในความหมาย status, payroll/lock/adjustment, payslip/email, reports, finance/admin | ขาด workflow เช่นเดียวกับทุก role; สิทธิ์ owner ไม่ทำให้ฟังก์ชันที่ไม่มีทำงานได้ |
| พนักงาน | EMPLOYEE scope self และ employee_id ที่ผูกจริง | ยื่นลา, advance, ดูข้อมูลและสลิปตนเอง | ไม่มี employee loan request; การสร้าง account อย่างเดียวไม่ทำให้ใช้งาน self-service ได้ทันที |

SUPERVISOR เป็น role จริงอีกหนึ่งรายการ แม้ไม่ใช่ actor ในรูปนี้ ต้องรวมในการทดสอบ Login และปฏิเสธการเข้าถึงนอกแผนกด้วย หากบุคคลหนึ่งมีหลาย grants ให้ทดสอบบัญชี single-role แยกก่อน มิฉะนั้น HR/OWNER ที่พ่วงอยู่จะทำให้ดูเหมือน BRANCH_MANAGER ทำงานเขียนได้

## หลักฐานและผลกระทบที่ต้องแก้ก่อนส่งมอบ

### P1 สิทธิ์ผู้จัดการสาขาไม่ตรง Use Case 1–3

Frontend กั้น `/employees/new` ที่ [route-access.ts](../frontend/lib/auth/route-access.ts#L52) และ controls เขียนที่ [employee-read-view.tsx](../frontend/features/identity-hr/employees/employee-read-view.tsx#L69) Backend `canAdministerEmployees` รับเฉพาะ HR/OWNER scope all ที่ [employee.scope.ts](../backend/src/features/employee/employee.scope.ts#L44) และ service เรียกจริงก่อน create/update/status

หากยังส่งภาพเดิม ผู้จัดการสาขาจะทำเดโม UC1–3 ไม่ผ่าน ต้องเลือกว่าจะให้สิทธิ์เขียนเฉพาะสาขาอย่างถูกต้องทั้ง frontend/backend หรือแก้ actor ในเอกสารตามขอบเขตที่ตกลง การให้ HR เพิ่มกับ manager เพื่อข้ามปัญหาเป็นการให้สิทธิ์ทุกสาขา ไม่ใช่การแก้ scoped authorization

### P1 ไม่มีการจ่ายเงิน เลือกช่องทาง และแบ่งกลุ่มเงินสด

[payroll.routes.ts](../backend/src/features/payroll/payroll.routes.ts#L50) มี period/preview/lock/adjustments; [schema.enums.ts](../backend/src/db/schema.enums.ts#L19) กำหนด payroll period จบที่ locked ไม่พบ paid lifecycle หรือ branch payout; [payroll-api.ts](../frontend/lib/payroll/payroll-api.ts#L3) ไม่มี payment/channel binding

UC7–9 และ QR ที่กล่าวใน BP ต้องพัฒนาเพิ่มเติมหากคงข้อกำหนดเดิม แม้ผู้รับผิดชอบโอนเงินจริงนอกเว็บ ขั้นตอนเตรียมกลุ่มและบันทึกผลที่ BP ระบุให้ทำในเว็บก็ยังไม่มี การ settle หนี้/เงินกู้ตอน lock เป็นการบันทึกรายการหัก ไม่ใช่ส่งเงินเดือนให้พนักงาน

### P1 รายงานส่งออกไม่ใช่กลุ่มจ่ายรายสาขา และไม่มี PDF สรุปตาม UC14

[reports/page.tsx](../frontend/app/(dashboard)/reports/page.tsx#L40) ใช้ branch/department เฉพาะ summary แต่ bank/SS download ส่ง `period_id` เท่านั้นที่บรรทัด 48 และอธิบายทั้งร้านที่บรรทัด 54 [report.routes.ts](../backend/src/features/reports/report.routes.ts#L7) มี JSON/CSV ไม่มี summary PDF

[report.service.ts](../backend/src/features/reports/report.service.ts#L51) bank CSV ดึงทุก locked payroll row และปฏิเสธทั้งไฟล์ถ้ามีคนไม่มีบัญชีธนาคาร จึงไม่สามารถผสมเงินสดกับเงินโอนตามกลุ่มใน BP ได้ [report.repository.ts](../backend/src/features/reports/report.repository.ts#L42) ไม่คืน branch field ใน lockedRows และไม่ได้กรอง payment channel/member status

### P1 พนักงานยื่นคำร้องเงินกู้ไม่ได้

[finance/page.tsx](../frontend/app/(dashboard)/finance/page.tsx#L75) แสดง advance request ให้ employee แต่ loan form เปิดเฉพาะ finance admin [loan.runtime.service.ts](../backend/src/features/loan/loan.runtime.service.ts#L11) ตรวจ finance access เฉพาะ HR/OWNER ก่อนส่งให้ [loan.service.ts](../backend/src/features/loan/loan.service.ts#L46) ซึ่งสร้าง loan พร้อม approved actor ทันที

ต้องมี employee request → pending → decision ที่ชัดเจนหากคง UC16 ครบทั้งเงินกู้และเบิกล่วงหน้า การทดสอบ HR สร้างเงินกู้ไม่พิสูจน์ employee self-service

### P1/P2 รายการปรับกับ BP คนละความหมาย

[payroll.service.ts](../backend/src/features/payroll/payroll.service.ts#L258) บังคับ source record locked, target ภายหลัง, same shop, มี employment assignment และต้องอนุมัติก่อน apply; [payroll-adjustments.tsx](../frontend/components/payroll-adjustments.tsx#L35) สอดคล้องกันจริง

ถ้า UC5 หมายถึงแก้ผลเงินเดือนที่ยืนยันไปแล้ว สามารถกำหนด acceptance ตามนี้ได้ ถ้าหมายถึงเพิ่มรายการพิเศษในงวดปัจจุบันหรือเบี้ยขยันทั่วไป ต้องพัฒนาอีก workflow และปรับ BP ที่นำรายการปรับไปวางก่อนปิดรอบแรก

### P2 ฐานประกันสังคมในไฟล์ส่งออกไม่ใช่ฐานที่ใช้คำนวณ

[payroll-calculator.ts](../backend/src/features/payroll/calculation/payroll-calculator.ts#L84) รวม daily base-salary earnings ถูกต้องก่อนคำนวณ deduction แต่ [report.repository.ts](../backend/src/features/reports/report.repository.ts#L43) คืน `baseSalarySnapshot` และ [report.service.ts](../backend/src/features/reports/report.service.ts#L74) ส่งค่านั้นเป็น `base_salary`

กรณีเข้าทำงานบางเดือนหรือค่าจ้างมีผลหลายช่วง ฐานใน CSV อาจไม่ตรงฐานรายได้ที่หักเงินจริง ต้องกำหนดความหมายคอลัมน์และใช้ค่าฐานที่ตรงกับกฎโครงการในการรายงาน ตรวจนี้เป็นความสอดคล้องภายในระบบ ไม่ใช่การรับรองรูปแบบไฟล์สำหรับหน่วยงานภายนอก

### P2 Bank export ไม่ freeze บัญชีปลายทางตามงวด

[report.repository.ts](../backend/src/features/reports/report.repository.ts#L43) join บัญชี primary active ปัจจุบันทุกครั้ง การเปลี่ยนบัญชีหลัง lock ทำให้ export งวดเก่าเปลี่ยนปลายทางได้ แม้ตัว net pay ถูก freeze แล้ว ควรกำหนดและทดสอบนโยบายข้อมูลปลายทางการจ่ายก่อนใช้เงินจริง

### เงื่อนไข Login และ self-service ที่ต้องจัดเตรียม

Canonical role definitions: [role.bootstrap.ts](../backend/src/features/role/role.bootstrap.ts#L9), [authorization.ts](../backend/src/core/auth/authorization.ts#L4), [route-access.ts](../frontend/lib/auth/route-access.ts#L1)

- Login ตรวจ account active, lockout และรหัสผ่านที่ [user-account.service.ts](../backend/src/features/user-account/user-account.service.ts#L212)
- Protected request ตรวจ token แล้วโหลด account/grants ปัจจุบันที่ [request-authenticator.ts](../backend/src/core/auth/request-authenticator.ts#L36)
- Onboarding สร้าง account พร้อม temporary password แต่ `grants: []` ที่ [user-account.admin.service.ts](../backend/src/features/user-account/user-account.admin.service.ts#L84)
- ต้องกำหนด EMPLOYEE role เพิ่มผ่านลิงก์ใน [onboarding-form.tsx](../frontend/features/identity-hr/onboarding/onboarding-form.tsx#L263) จึงใช้งาน self-service; ชุด e2e มีกรณีไม่มีบทบาทแล้วกำหนดภายหลังด้วย
- Employee requests ต้องผูก employee_id จริง และทดสอบด้วยบัญชีของพนักงานเอง ไม่ใช้ admin ส่งแทน

### ข้อจำกัดอื่นที่ควรรู้ก่อนเดโม

- UC3 เป็นการเปลี่ยนสถานะและปิด assignment ไม่ลบประวัติ การเปิด active กลับจาก terminated ล้าง `terminated_at` ใน row ปัจจุบัน แต่ old/new ยังอยู่ใน audit และ assignment เก่ายังปิดอยู่ ต้องกำหนดวิธี rehire ให้สอดคล้อง; ไม่อ้างว่าประวัติหายทั้งหมด [employee.service.ts](../backend/src/features/employee/employee.service.ts#L150)
- Terminate employee ไม่ disable user account อัตโนมัติ หากต้องการตัดการเข้าใช้งานต้องจัดการ account status ตามนโยบายแยก
- Void payslip แล้ว generate เดิมจะคืน voided record ตัวเดิม ไม่มี replacement workflow สำหรับออกใหม่ [payslip.service.ts](../backend/src/features/payslip/payslip.service.ts#L19)
- Supervisor/manager ดู own payslip ได้ใน API หากผูก employee_id แต่ frontend `/payslips` ไม่เปิดให้สอง role นี้ล้วน ๆ ต้องมี EMPLOYEE grant เพิ่มหากต้องใช้ self-service
- SMTP sender เป็น nodemailer จริงที่ [smtp-mailer.ts](../backend/src/core/mail/smtp-mailer.ts#L5) แต่ unit tests inject sender; ห้ามถือว่า unit tests คือส่งเข้า inbox แล้ว ผู้ดูแลกรอก recipient ได้ ต้องตรวจอีเมลกับเจ้าของสลิปก่อนส่ง

## ผลตรวจที่รันรอบนี้

| รายการ | ผล |
|---|---|
| Backend `bun run typecheck` | ผ่าน |
| Backend `env -u TEST_DATABASE_URL bun test` | 452 pass, 27 skip, 0 fail / 103 files |
| Frontend `bun test` | 45 pass, 0 fail / 16 files |
| Frontend `bun run lint` | ผ่าน |
| Frontend `bun run node_modules/typescript/bin/tsc --noEmit` | ผ่าน |
| Playwright `bun run test:e2e --list` | พบ 21 tests ใน 5 files เป็นการนับรายการ ไม่ได้รัน browser |
| Browser/API live verification | ยังไม่ได้รัน: Docker daemon ติดต่อไม่ได้; HTTP localhost:3000 และ auth endpoint ติดต่อไม่ได้ในรอบตรวจ |
| DB integration | 27 รายการข้ามเพราะไม่ได้ตั้ง TEST_DATABASE_URL สำหรับ disposable database; ไม่ใช้ฐานจริงแทน |
| Production build / deploy | ไม่ได้รันในรอบ audit นี้ |

Unit tests ผ่านหมายถึงพฤติกรรมที่มี test รองรับ ไม่ได้พิสูจน์ฟังก์ชันที่ยังไม่มี และผลทดสอบเก่าจากเอกสาร 14 ตุลาคมไม่ใช้แทนผล UAT ปัจจุบัน

## ช่องว่างของ browser tests เดิม

- [scope.e2e.ts](../frontend/e2e/scope.e2e.ts#L16) ทดสอบ login ห้า role และ scoped API reads แต่ไม่มี accounting actor
- [flow.e2e.ts](../frontend/e2e/flow.e2e.ts#L65) golden journey หลักใช้ OWNER; หลายขั้น payroll/lock/generate/email ใช้ `page.request` ไม่ได้กดฟอร์มทุกขั้น
- HR case เน้น safe read DTO ไม่ใช่ CRUD/payroll/payslip/email ครบตลอดเส้นทาง
- Employee leave ใน golden journey เปิดหน้าได้ แต่ไม่ได้ส่งคำขอด้วย employee form
- Employee advance case ตรวจ form/button visible และ cross-employee denial ยังไม่ส่งคำขอผ่านฟอร์มจนสำเร็จ
- Branch manager case ยืนยัน payroll read-only ไม่มีปุ่ม lock ซึ่งเป็นพฤติกรรมจริงแต่ไม่พิสูจน์ CRUD ที่ diagram ต้องการ
- จึงยังไม่มีหลักฐานครบแบบ Use Case × actor × UI submission × persisted result

## Checklist ทดสอบส่งมอบบนเว็บ

ให้เก็บผลต่อหนึ่ง actor ต่อหนึ่ง Use Case เป็น Passed/Failed/Blocked พร้อม screenshot, request/error ID และข้อมูลหลัง reload ไม่ถือว่าแค่เมนูแสดงคือผ่าน

### เตรียมข้อมูลทดสอบ

1. ใช้ disposable verification stack ตาม `scripts/verify.sh` และ fixture ที่จำกัดฐานทดสอบ ไม่ seed หรือรัน destructive integration tests บนฐานใช้งานจริง
2. เตรียม employee A/B, ต่างสาขาอย่างน้อยสองสาขาและต่างแผนก, role single-grant แยก EMPLOYEE/SUPERVISOR/BRANCH_MANAGER/HR/OWNER พร้อมตัดสินใจ accounting-to-role mapping
3. เพิ่ม employee_id link และ EMPLOYEE grant ให้บัญชีที่ใช้ self-service; ตรวจ active/disabled/lockout ตามกรณี
4. เตรียม salary/welfare history, branch schedules, weekly holidays, effective configs, attendance และ approved leave/OT ให้ครบช่วงเดือน
5. เตรียม prior locked month กับ later draft monthสำหรับ UC5; current draft monthอย่างเดียวไม่พอ
6. เตรียมบัญชีธนาคารสำหรับผู้ถูก export, test mailbox ที่อนุญาตให้ส่ง และพื้นที่เก็บ PDF ถาวรสำหรับ stack ทดสอบ

### Login และสิทธิ์

- [ ] Login สำเร็จแยกห้า canonical roles และบัญชีฝ่ายบัญชีตาม mapping ที่ตกลง ตรวจ landing page และเมนู
- [ ] Wrong password, disabled account, temporary lockout และ logout/session หมดอายุให้ผลถูกต้อง
- [ ] บัญชีเพิ่ง onboard แต่ยังไม่มี grant แสดงสถานะไม่มีบทบาท; กำหนดบทบาทแล้วใช้ได้
- [ ] เปิด URL โดยตรง/API ข้ามสิทธิ์ถูกปฏิเสธ รวม own/other employee, department และ branch
- [ ] ไม่ใช้บัญชีที่พ่วง OWNER/HR ไปพิสูจน์สิทธิ์ BRANCH_MANAGER/EMPLOYEE

### Use Case × actor

| UC | Actor ที่ต้องกดทดสอบตาม diagram | เกณฑ์ผลลัพธ์ที่ต้องเห็น | สถานะก่อนแก้ |
|---|---|---|---|
| 1 | HR, ผู้จัดการสาขา, เจ้าของร้าน แยกบัญชี | สร้างข้อมูลและประวัติเริ่มต้นครบ; reload แล้วยังอยู่; ซ้ำถูกปฏิเสธ | Manager blocked |
| 2 | HR, ผู้จัดการสาขา, เจ้าของร้าน | บันทึกผ่านฟอร์ม; read back ถูกต้อง; ประวัติ compensation ไม่ถูกเขียนทับ; scope ไม่ข้ามสาขา | Manager blocked |
| 3 | HR, ผู้จัดการสาขา, เจ้าของร้าน | ยุติการใช้งานตามนิยามที่อนุมัติ; ประวัติเก่าและ audit อยู่; วันสิ้นสุดถูกต้อง | Manager blocked; นิยาม delete ต้องชัด |
| 4 | บัญชี, เจ้าของร้าน | กดสร้างเดือนใหม่จากเว็บ; persisted draft; duplicate/calendar-date validation | Accounting mapping pending |
| 5 | บัญชี, เจ้าของร้าน | เลือกต้นทาง locked กับปลายทางภายหลัง; request → approve → preview → lock; apply ครั้งเดียว | ทดสอบได้เฉพาะขอบเขต adjustment ปัจจุบัน |
| 6 | บัญชี, เจ้าของร้าน | Lock ผ่านเมื่อข้อมูลครบ; pending/incomplete/negative net ถูกกัน; reload locked; แก้ตรง ๆ ไม่ได้ | Accounting mapping pending |
| 7 | บัญชี, เจ้าของร้าน | จ่ายเงินจริงผ่านช่องทางภายนอกที่กำหนด; บันทึกผลในเว็บ; ตรวจและปิดสถานะรายสาขา; ป้องกันบันทึกซ้ำ | Missing |
| 8 | บัญชี, เจ้าของร้าน | เลือกและบันทึก cash/transfer/channel; reload และใช้จัดกลุ่มได้ | Missing |
| 9 | บัญชี, เจ้าของร้าน | เลือกสาขา; รายชื่อเงินสดและยอดรวมถูกต้อง ไม่ปนโอน/สาขาอื่น | Missing |
| 10 | บัญชี, เจ้าของร้าน | เลือกสาขา; เฉพาะกลุ่มโอน; รวมยอดถูกต้อง; QR ตาม BP หากคงข้อกำหนดนั้น | Partial CSV only |
| 11 | บัญชี, เจ้าของร้าน | กลุ่มมี/ไม่มีประกันสังคมแยกถูกต้องตามนิยาม; สาขาและยอดตรง payroll | Partial report only |
| 12 | บัญชี, เจ้าของร้าน | กดออกสลิปจาก locked record; PDF ไทย/ยอดตรง; สร้างซ้ำไม่ซ้ำ; employee A เปิดของ B ไม่ได้ | Accounting mapping pending |
| 13 | บัญชี, เจ้าของร้าน | กดส่งจากเว็บถึง test mailbox ที่อนุญาต; attachment ตรงฉบับ; attempt log; failure ไม่ขึ้นสำเร็จ | SMTP+inbox verification pending |
| 14 | บัญชี, เจ้าของร้าน | ดาวน์โหลด PDF สรุปเงินเดือนและ PDF สรุปเจ้าหนี้; branch/person/ยอดตรง | Missing PDF outputs |
| 15 | พนักงาน | ส่งฟอร์มด้วยตัวเอง → pending → ผู้อนุมัติตัดสิน → employee reload เห็นผล; overlap/quota/attachment ถูกตรวจ | Source ready; actual employee-form UAT pending |
| 16 | พนักงาน | ส่ง advance และ loan แยกกรณี → pending → decision; advance boundary วันที่/วันทำงาน/ครึ่งเงินเดือน/net; loan งวดถูกต้อง | Advance source ready; loan request missing |

### ลำดับงานที่ควรจัดการ

1. ยืนยันขอบเขตและชื่อ actor: accounting map เป็น HR หรือ role แยก; manager CRUD ตามภาพหรือแก้ภาพ; delete คือยุติการใช้งาน; UC5 หมายถึง adjustment แบบใด
2. หากคงภาพและ BP เดิม ให้พัฒนาช่องว่างจริง: payment lifecycle/channel/groups/QR, employee loan request, summary PDFs และ scoped manager writes อย่าขยายสิทธิ์ all-scope เพื่อให้เดโมผ่าน
3. ตรวจและแก้รายงาน SS base กับนโยบาย bank destination snapshot ก่อนทดสอบยอด/การจ่าย
4. เพิ่ม browser cases ที่ submit UI จริงแยกทุก actor รวม employee leave/advance และ HR payroll/payslip ไม่พึ่ง OWNER golden journey อย่างเดียว
5. รัน DB integration กับ disposable database แล้วจึง UAT บนเว็บและเก็บหลักฐาน ไม่มี source changes ที่ทำให้รายการ Missing ผ่านโดยอาศัยการรัน test เดิมเพิ่ม
