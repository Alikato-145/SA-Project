# Haris Payroll Use Case Delivery Design

## สถานะและเป้าหมาย

ร่างข้อกำหนด Subtask 1 สำหรับทำ Login และ Use Case 1–16 ให้ทดสอบผ่านหน้าเว็บได้ครบตาม actor ในภาพล่าสุด อ้างอิงผลตรวจใน `docs/use-case-delivery-audit-2026-10-25.md` และ ERD ที่ผู้ใช้ส่งวันที่ 25 ตุลาคม 2026

ผู้ใช้ยืนยันให้ใช้ PromptPay จากเบอร์โทรศัพท์เป็นหลัก ฝ่ายบัญชีใช้สิทธิ์ HR เดิม และรายงานสรุปเจ้าหนี้หมายถึงยอดเงินเดือนที่ร้านต้องจ่ายให้พนักงาน ทั้งแบบรวมทั้งหมดและแยกรายบุคคล เพื่อใช้ข้อมูลชุดเดียวกันออกสลิป การตอบข้อกำหนดนี้ใช้เป็นฐานเดินงานถัดไปได้ โดยยังไม่ถือว่าช่องว่างในผล audit ได้รับการแก้ไขแล้ว

## แนวทาง

ใช้แนวทางต่อยอดระบบเดิมเป็นรายความสามารถ ให้แต่ละ subtask ครบ database/service/API/UI/tests แทนการแยกทำ backend ทั้งหมดแล้วค่อยต่อหน้าเว็บ รักษา Next.js/Bun/Elysia/Drizzle/PostgreSQL 16, feature-first layers และ API conventions เดิม

การเปลี่ยนชื่อ UC ให้ตรงเฉพาะสิ่งที่แอปทำได้ในปัจจุบันจะลดงาน แต่ไม่เติมฟังก์ชันที่ผู้ใช้ต้องส่งมอบ จึงใช้ภาพ Use Case ล่าสุดเป็นเป้าหมายและเพิ่มส่วนที่ขาดเป็นหลัก ไม่ขยายไปสั่งโอนธนาคารอัตโนมัติ

## ข้อกำหนดที่ใช้เป็นฐาน

- Login และ UI submission ต้องตรวจแยกตาม role ไม่ใช้ OWNER ทำแทนทุก actor
- UC1–3: HR และ OWNER จัดการทุกสาขา; BRANCH_MANAGER จัดการเฉพาะสาขาที่ได้รับสิทธิ์ backend ต้องบังคับ scope ด้วย
- UC3 หมายถึงยุติการใช้งาน/สิ้นสุดการจ้างโดยรักษาประวัติ ไม่ hard delete ประวัติเงินเดือน หนี้ หรือการอนุมัติ
- UC5 ต้องเพิ่มรายได้/รายการหักในงวดที่ยังไม่ล็อกได้ และรักษา workflow แก้ผลจากงวดที่ล็อกแล้วไปงวดภายหลัง
- UC7–11 ต้องมีช่องทางจ่าย กลุ่มรายสาขา และการบันทึกผลการจ่าย ไม่ใช้สถานะ locked แทน paid
- UC12–14 มีสลิปรายบุคคล อีเมลสลิป และ PDF สรุปเงินเดือน/สรุปเจ้าหนี้เป็นผลลัพธ์แยกกัน
- UC15 พนักงานยื่นลาเองตามกฎเดิม; UC16 พนักงานยื่น advance และ loan request เองได้
- รักษา decimal money, effective dates, append-only approval/audit, transaction และ immutable locked payroll

## Role contract

| Actor | สิทธิ์เป้าหมาย |
|---|---|
| EMPLOYEE | ข้อมูล/สลิป/คำขอของตนเท่านั้น ไม่ตัดสินใจคำขอตนเองด้วย EMPLOYEE grant |
| SUPERVISOR | ขอบเขตแผนกและกฎการอนุมัติเดิม ไม่เพิ่มสิทธิ์การเงิน |
| BRANCH_MANAGER | สร้าง/แก้ไข/ยุติพนักงานในสาขาตน โดยไม่ย้ายข้ามสาขาหรือกำหนด role ผ่าน employee form; งานปฏิบัติการเดิมคง scope สาขา |
| HR | Employee admin และงานเงินเดือน/การเงินตามสิทธิ์เดิม |
| OWNER | ทุกสาขาตามสิทธิ์เดิม รวมระบบและการบริหาร role |
| บัญชี | ยืนยัน: บุคลากรบัญชีใช้ HR grant เดิมก่อน โดยระบุ mapping ในรายงานและบัญชีทดสอบ; ไม่เพิ่ม ACCOUNTING role ในงานชุดนี้ |

บัญชีที่มีหลาย grant ใช้สิทธิ์รวมตามระบบเดิม แต่ fixture ตรวจ actor ต้องเป็น single-role เพื่อไม่ให้สิทธิ์ OWNER/HR กลบข้อผิดพลาดของ scoped roles

การสร้าง account ต้องมีขั้นตอนกำหนด role และผูก employee_id ที่ชัดเจน ไม่ถือว่าบัญชีซึ่งยังไม่มี grant ใช้ self-service ได้

## PromptPay และการจ่ายเงิน

- เบอร์ติดต่อ `employees.phone` แยกจาก `employees.promptpay_phone` ซึ่งเป็นเบอร์ที่ผู้ใช้ระบุสำหรับรับ PromptPay
- UI แสดงเบอร์รับเงินและยอดให้ผู้รับผิดชอบตรวจ ก่อนสร้าง QR เบอร์ต้องผ่าน validation/normalization ไม่ใช้เบอร์ติดต่อแทนอัตโนมัติ
- ประเภทจ่ายหลัก `cash` และ `transfer` ส่วน PromptPay QR เป็นวิธีเตรียมจ่ายสำหรับกลุ่ม transfer ที่ BP ระบุ
- สร้าง QR จากเบอร์และยอด snapshot ในรายการจ่าย ไม่ต้องเพิ่ม QR table หรือจัดเก็บรูป QR เป็นหลักฐานการโอน
- บันทึกผลหลังตรวจหลักฐานจากเงินสด/แอปธนาคารภายนอก การสร้างหรือสแกน QR ไม่ยืนยันว่าโอนสำเร็จ
- ไม่มีการเชื่อม API สั่งโอนเงินจริงหรือ bank callback ในขอบเขตนี้

ข้อเสนอการจัดกลุ่มที่ใช้พัฒนาต่อ: กลุ่มมีประกันสังคมก่อน; กลุ่มไม่มีประกันสังคมแบ่ง cash/transfer เพื่อไม่ให้พนักงานหนึ่งคนซ้ำหลายกลุ่ม กลุ่มไม่มีประกันสังคมแบบ transfer จึงมี PromptPay QR กลุ่มอื่นดำเนินการตามช่องทางที่กำหนดโดยไม่สร้าง QR

สถานะพนักงานอยู่ประกันสังคมต้องมี effective date เพื่อคำนวณรายวันได้; การจัดกลุ่มจ่ายใช้สถานะ ณ วันสิ้นงวดเป็นข้อเสนอ หากเปลี่ยนกลางงวด ฐานคำนวณใช้เฉพาะวันและฐานรายได้ที่เข้าเงื่อนไข ไม่ย้อนแก้ประวัติตามสถานะปัจจุบัน

## Schema delta จาก ERD ที่ส่งมา

`payroll_payments` และ `loan_requests` มีในภาพเป็น Proposed Addition แต่ไม่มีใน executable schema ปัจจุบัน ต้องเพิ่มจริงผ่าน migration ที่ได้รับอนุมัติ ไม่เพิ่มชื่อเดียวกันซ้ำอีกตาราง

| ตาราง | การเปลี่ยนที่เสนอ |
|---|---|
| employees | เพิ่ม payment_method และ promptpay_phone; รองรับ cash โดยไม่บังคับเบอร์ PromptPay/บัญชีธนาคาร |
| employment_assignments | เพิ่ม is_social_security_member ใช้ effective_from/effective_to เดิม และไม่แก้ย้อนหลังทับแถวเดิม |
| payroll_records | เพิ่ม is_social_security_member_snapshot สำหรับกลุ่มจ่าย และ social_security_base_snapshot เป็นฐานรายได้รายวันที่ใช้หักจริง |
| payroll_payments | สร้างตามภาพ: payroll_record_id, branch_id_snapshot, payment_method, amount, status, paid_at, paid_by_user_account_id, reference_no, snapshots ปลายทาง; เพิ่ม promptpay_phone_snapshot; bank account FK ว่างได้เมื่อไม่ใช้ bank account |
| payroll_adjustments | เพิ่ม employee_id; original_payroll_record_id ว่างได้สำหรับ current-period item; target period ต้องชัด; เมื่อมี original ให้รักษากฎ locked original/later period/same shop เดิม |
| loan_requests | สร้างตามภาพพร้อม requested_by_user_account_id และ optional loan_id ที่ unique; requested fields ไม่ถูกแก้ทับเป็น approved fields โดยไม่มีประวัติ |

เงินและยอด snapshot ใช้ exact decimal; FK และประวัติไม่ใช้ cascade deletion ที่ลบหลักฐาน ต้องแก้ DBML, design reference, Drizzle และ migrations ให้ตรงกันหลังคลาย schema freeze

## กฎ workflow ที่เสนอสำหรับส่วนใหม่

### Employee writes

สร้างในสาขาที่ manager ได้รับสิทธิ์เท่านั้น รวม validation department/position/assignment ผู้จัดการสาขาแก้สิทธิ์ account ไม่ได้ การเปลี่ยนค่าตอบแทนสร้างประวัติตามวันที่มีผล และการย้ายข้ามสาขาใช้ HR/OWNER ไม่ให้อาศัยการแก้ employee เพื่อขยาย scope

ข้อเสนอหลัง builder review: การยุติการจ้างไม่ disable user account อัตโนมัติในงาน UC3 นี้ รักษาพฤติกรรมการแยก employee status จาก account status เดิม HR/OWNER เป็นผู้ระงับ account แยกเมื่อจำเป็น ส่วน manager ไม่ได้สิทธิ์ account admin เพิ่ม ขั้นทดสอบต้องบันทึกผลสองสถานะให้ชัด ไม่อ้างว่า terminate ตัดสิทธิ์ Login ไปด้วย

### Current-period adjustments

รายการใหม่ระบุ employee/target period/direction/positive amount/reason/requester มี approval ก่อนนำไปคิดเงินจริง Pending ต้องแสดงและขัดขวาง lock ตามกฎเดิม Re-preview ไม่สร้างรายการซ้ำ Lock นำรายการไปใช้ครั้งเดียวและผูก applied payroll item งวดล็อกแล้วไม่เปิดให้แก้ตรง ๆ

### Loan requests

EMPLOYEE ส่งได้เฉพาะตน สถานะ pending → approved/rejected ผู้มี finance authority HR/OWNER พิจารณาตามสิทธิ์เดิม เมื่อ approved จึงสร้าง loan และ installments ภายใน transaction เดียว และผูก loan_id กลับคำขอ ป้องกัน approve ซ้ำสร้างหนี้ซ้ำ

ข้อเสนอ: ผู้พิจารณาระบุเดือนเริ่มหักที่ยังไม่ล็อก ไม่สร้างงวดหักย้อนหลัง และใช้ requested amount/count เดิม หากต้องเปลี่ยนสาระสำคัญให้ส่งกลับ/ยื่นใหม่พร้อมประวัติ ไม่แก้คำขอให้ผู้ขอเข้าใจว่าอนุมัติตามยอดเดิม

### Payments

เตรียมได้จาก locked payroll เท่านั้น Freeze รายการจ่ายและปลายทางแยกจากผลคำนวณที่ล็อกแล้ว Snapshot สาขาใช้ประวัติ ณ วันสิ้นงวดตามข้อเสนอข้างต้น การย้ายสาขาทีหลังไม่เปลี่ยนกลุ่มงวดเก่า

ข้อเสนอขอบเขตแรก: จ่ายเต็ม net pay ต่อพนักงาน ไม่รองรับแบ่งจ่ายบางยอดให้คนเดียวหลายครั้ง ใช้สถานะ prepared/paid/cancelled รักษารายการ cancelled เป็นประวัติ และอนุญาต active payment ต่อ payroll record ได้เพียงหนึ่งรายการด้วย constraint/transaction เมื่อ paid แล้วห้ามกลับเป็น unpaid ผ่าน ordinary update

ยอด net เท่ากับศูนย์แสดงแยกว่าไม่มียอดต้องจ่าย ไม่สร้าง QR จำนวนศูนย์ และไม่นับเป็นผู้ค้างจ่าย ยอดติดลบถูกปฏิเสธตั้งแต่ payroll lock

สถานะครบสาขาคำนวณจากพนักงาน/รายการในงวดและ snapshot สาขา ไม่มีตารางซ้ำสำหรับ group totals เว้นแต่ต้องเก็บเหตุการณ์ยืนยันปิดการจ่ายสาขาแยกในอนาคต การกดยืนยันซ้ำต้อง idempotent และ audit ผู้ทำรายการทุกครั้งที่เปลี่ยนสถานะ

### Reports and payslips

PDF สรุปเงินเดือนใช้ข้อมูล locked payroll และรายการจ่ายที่อ้างอิง ตรวจยอดรวมรายได้/หัก/สุทธิแยกสาขาได้ ไม่ถือว่าสลิปคือหลักฐานโอนเงิน

ยืนยันความหมาย “สรุปเจ้าหนี้”: ยอดเงินเดือนที่ร้านต้องจ่ายให้พนักงาน มีทั้งยอดรวมทั้งหมดและรายละเอียดพนักงานแต่ละคน ใช้ locked payroll เป็นแหล่งข้อมูลหลักเดียวกับสลิป แสดงรายได้ รายการหัก และยอดสุทธิรายคน พร้อมรวมยอดให้ตรงกัน เมื่อมีข้อมูลจ่ายให้แยกยอดจ่าย/ค้างชัดเจนโดยไม่เปลี่ยนผลเงินเดือนที่ล็อกแล้ว รายงานนี้ไม่ใช่สรุปเงินกู้หรือหนี้ที่พนักงานเป็นลูกหนี้ร้าน

การออกสลิปอ่านข้อมูลผลเงินเดือนรายบุคคลจากแหล่งข้อมูลเดียวกับรายงาน ไม่อ่านหรือแปลงกลับจากไฟล์ PDF สรุป เพื่อไม่ให้เกิดการคัดลอก/ปัดเศษ/ตีความข้อมูลซ้ำ

CSV ประกันสังคมใช้ social_security_base_snapshot ที่ตรงกับฐานหักจริง ไม่ใช้ contracted salary แทนเมื่อรายได้รายวันต่างกัน Bank export ใช้ปลายทางที่ freeze สำหรับรายการจ่าย ไม่ join primary account ปัจจุบันมาเปลี่ยนงวดเก่า

สลิป/อีเมลใช้ service และ storage เดิม ตรวจสิทธิ์ owner/HR และ employee self-read ทุกครั้ง ทดสอบ SMTP ด้วย mailbox ที่ได้รับอนุญาตเท่านั้น และแยก SMTP accepted ออกจาก inbox received

## Subtasks และเกณฑ์ตรวจรับ

| งาน | ผลส่งมอบที่ตรวจรับได้ | ขึ้นกับ |
|---|---|---|
| 1 ข้อกำหนดและสิทธิ์ | แบบนี้ผ่าน builder review, ประเด็นธุรกิจได้รับคำตอบ และ schema delta ได้รับอนุมัติก่อนเปลี่ยน schema | — |
| 2 Stack ทดสอบและ Login | บัญชี single-role/ข้อมูลสองสาขา; Login/logout/disabled/lockout/no-grant และ own/other ผ่าน; ไม่ใช้ฐานจริง | 1 สำหรับเกณฑ์บทบาท |
| 3 Employee scoped CRUD | UC1–3 ผ่าน HR/OWNER/manager และ manager ข้ามสาขาไม่ได้ผ่าน UI/API | 1, 2 |
| 4 Current adjustments | เพิ่ม/อนุมัติ/preview/lock ครั้งเดียวได้ และ old adjustment ไม่ถอยหลัง | 1, 2 |
| 5 Employee loan request | Employee submit → HR/OWNER decide → loan/installments atomic; duplicate decision ไม่สร้างหนี้ซ้ำ | 1, 2 |
| 6 Payment destination/history | ช่องทาง/เบอร์/ประกันสังคม effective-dated และ snapshots ไม่เปลี่ยนงวดเก่า | 1, 2, schema delta |
| 7 Branch groups/QR | สามกลุ่มไม่ซ้ำไม่ตกหล่น; QR decode แล้วเบอร์/ยอดตรงกับ snapshot | 6 |
| 8 Record payout | จ่าย/ตรวจ/ยืนยันรายคน; ป้องกันซ้ำ; สรุปค้าง/ครบสาขา; audit และ rollback ถูกต้อง | 7 |
| 9 Summary PDFs/exports | PDF เงินเดือนและเจ้าหนี้ตามนิยาม; branch filter/SS base/payment snapshots ถูกต้อง | 4, 6, 8 |
| 10 Payslip/email regression | ทุก actor ที่กำหนดกด UI ได้; own-only PDF; delivery logs; authorized test inbox | 2, 6, 8 ตามกฎข้อมูลที่เกี่ยวข้อง |
| 11 Handover UAT/docs | Login + UC1–16 × actor ผ่าน UI จริง, persistence หลัง reload, denial cases; BP/ERD/คู่มือตรง behavior | 3–10 |

แต่ละงานมี unit/service boundary checks และ browser test ของตัวเอง ไม่รอเริ่มทดสอบครั้งแรกในงาน 11 การมีปุ่มหรือ API test ผ่านอย่างเดียวไม่ใช่เกณฑ์จบ UI Use Case

## การตัดสินใจที่ยืนยันแล้ว

1. ฝ่ายบัญชีใช้ HR grant เดิม ไม่เพิ่ม ACCOUNTING role
2. สรุปเจ้าหนี้เป็นยอดเงินเดือนที่ร้านต้องจ่าย ทั้งยอดรวมและรายบุคคล ใช้ข้อมูลชุดเดียวกับสลิป
3. PromptPay ใช้เบอร์โทรศัพท์ผู้รับเงินเป็นหลัก แยกจากเบอร์ติดต่อ และ snapshot ตามรายการจ่าย

ก่อนเปลี่ยน schema ให้ส่ง delta นี้ให้ schema owner ตรวจตาม project guide และบันทึกการปรับ DBML/Drizzle/migration ให้ตรงกัน Subtask 2 ใช้ schema เดิม จึงไม่ต้องรอ migration ใหม่

ข้อเสนอทางเทคนิคที่ระบุเป็นค่าเริ่มต้นให้ใช้ต่อได้ในการจัดทำแผน โดยบันทึกความต่างเมื่อ implementation จำเป็นต้องปรับ

## สถานะงาน

- [x] ตรวจ source และช่องว่างเทียบ Login/UC1–16
- [x] บันทึกขอบเขต PromptPay จากเบอร์โทรศัพท์
- [x] จัดทำ role contract, schema delta, workflow และเกณฑ์ตรวจรับราย subtask
- [x] Builder review และแก้ประเด็นที่ทำให้ implementation เดาต่างกัน: ระบุข้อเสนอเรื่อง account status หลัง terminate แยกจาก employee status
- [x] ผู้ใช้ยืนยันข้อกำหนดธุรกิจที่เปิดอยู่: HR สำหรับบัญชี และเจ้าหนี้เงินเดือนรวม/รายบุคคล; เดินงานถัดไปตามบริบทที่อนุญาตแล้ว
- [x] จัดทำ implementation plan สำหรับ Subtask 2 แยกจาก subsystem ที่ต้องเปลี่ยน schema
