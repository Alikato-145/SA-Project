# Delivery decisions and limits

บันทึกการตัดสินใจระหว่างงานสำหรับตรวจส่งมอบ Task11 และ final review ผ่านแล้ว รวม scoped re-review หลังแก้ I1–I3/M1–M2; รายงาน14 สรุปเวอร์ชันส่งมอบ คงหลักฐานรายละเอียดไว้ใน SDD ledgers และรายงานแต่ละ subtask

| งาน | การตัดสินใจที่ใช้ | ผล/ต้นทุนหากต้องเปลี่ยนภายหลัง |
|---|---|---|
| Scoped employee CRUD | ผู้จัดการสร้าง initial assignment เฉพาะสาขาตน; ไม่รับ bank/account payload; ใช้ assignment ปัจจุบันตัดสิน scope | หากต้องให้ผู้จัดการทำงานการเงิน/บัญชี ต้องออกแบบสิทธิ์และตรวจใหม่; ไม่ขยายโดยอาศัย CRUD |
| การเดินงาน | ทำตาม design ที่ผู้ใช้อนุมัติต่อได้โดยไม่ขอยืนยันแผนย่อยซ้ำ แต่ต้องมี fresh review ก่อนปิดงาน | หากรายละเอียดไม่ตรงความต้องการ แก้เป็น local commits ย้อนตรวจได้; ไม่ถือว่าอนุญาต push/merge/deploy |
| Current adjustments | backfill employee จาก source เดิมก่อนบังคับค่า; origin ว่างได้สำหรับรายการใหม่; รักษา legacy target-null; ไม่สร้างผลเงินเดือนเก่าปลอม | migration ต้องตรวจ parity และประวัติ; หาก target validation เปลี่ยน ต้องทบทวน legacy read และ approval |
| Membership/SS history | ไม่ปิด trigger ล็อกเงินเดือน; legacy earned-base เป็น NULL และอ่าน frozen base items; สมาชิกเดิม default true ตามพฤติกรรมคำนวณเดิม | ไม่สามารถอนุมานสถานะสมาชิกเก่าที่ไม่เคยจัดเก็บ; เปลี่ยนนโยบายย้อนหลังต้องมีหลักฐาน/adjustment ไม่เขียนทับ locked facts |
| Recipient audit | mutation ล็อก employee row เพื่อให้ old/new audit ถูกต้อง; GET ปกติไม่ล็อก; preparation ใช้ transactional capability | concurrent mutation อาจรอ row เดียวกัน; งานข้ามหลายแถวต้องคง lock order ที่ทดสอบไว้ |
| QR dependency | ต้องเตรียมและ freeze ปลายทางก่อนสร้าง QR; paid/cancel ใช้ payment model เดียวกันในงานถัดไป | เปลี่ยนเบอร์ภายหลังไม่เปลี่ยน QR เดิม; ต้องยกเลิกการเตรียมและเตรียมใหม่โดยเก็บประวัติ |
| Payment idempotency | retry รายละเอียดเดิมคืนข้อมูลเดิม ไม่มี domain transition ซ้ำ; ไม่ทับผู้ทำ/เวลาของครั้งแรก | reference/reason ที่ต่างกันต้องเป็น conflict; ถ้าต้องแก้ paid metadata ต้องมี workflow แยก |
| Bank CSV | ส่งออกเฉพาะ outstanding prepared bank transfers; paid/cash/zero ไม่ส่งออก; unprepared/phone-only ปฏิเสธพร้อมทางแก้ ไม่ตัดออกเงียบ ๆ | กลุ่มผสมอาจต้องเลือกตัวกรองหรือใช้ QR; ไม่ใช่ bank-certified format/คำสั่งโอนอัตโนมัติ และไฟล์ที่ดาวน์โหลดไปแล้วเพิกถอนภายนอกไม่ได้ |
| Payslip regression scope | เมื่อพฤติกรรมเดิมถูกต้อง ให้เพิ่ม tests/evidence โดยไม่สร้าง product changes ที่ไม่จำเป็น | regression gate ไม่ทดแทน UAT ทุก Use Case/actor |
| Scoped own payslip | เพิ่มเฉพาะสิทธิ์เปิดหน้า/เมนูสลิปของตนให้ supervisor/manager; คง own-only backend และ HR/OWNER-only generation/email | ต้องตรวจ policy และ UI หากเพิ่ม role ใหม่; ไม่ให้สิทธิ์การเงินหรือสลิปของผู้ใต้บังคับบัญชาโดยปริยาย |
| Final UAT ownership | implementer ทำ harness/matrix/UI gaps/docs; root ตรวจ task และ whole branch ก่อนปิด heartbeat; full-suite counts ต้องมาจากหนึ่ง run จริง | พบ failure ต้องเก็บหลักฐานและรันใหม่หลังแก้; selective reruns ไม่อาจใช้แทนผลรวมทั้งชุด |
| ขอบเขต final review | รับข้อยกเว้น 6 เรื่องตาม review12: ธนาคารจริง/ยืนยันเจ้าของ PromptPay, การรับรองไฟล์ภายนอก, external SMTP, production performance/retention/rollout-backup, แบ่งจ่าย/คืนเงิน/ยกเลิก QR ที่ดาวน์โหลด และ clock/OCR | หากต้องใช้ ต้องเพิ่ม integration, operations, certification และ UAT แยก; ไม่ใช้ข้อยกเว้นนี้ตัดช่องสิทธิ์หรือปัญหาหน้ายืนยันจ่าย/พอร์ต Mailpit ออกจากงาน |

การจ่ายเงินจริงทำภายนอกระบบ และเจ้าหน้าที่บันทึกผลหลังตรวจสอบ การสร้าง/สแกน QR หรือออกสลิป/PDF ไม่ยืนยันการโอนสำเร็จ การยกเลิกการเตรียมจ่ายไม่ย้อนการโอนหรือทำให้ QR ที่เคยดาวน์โหลดหมดอายุ อีเมลทดสอบส่งเข้า Mailpit เท่านั้น; ไม่รับรองการส่งถึง external inbox

ต้นทางของ Ruling แต่ละข้อ: `.superpowers/sdd/*/progress.md` (12 รายการ รวมขอบเขต final review) พร้อมรายละเอียดใน reports02–10 คง recovery artifacts ไว้สำหรับตรวจย้อนหลัง; ผลสุดท้ายอ้างอิง reports12–14

ผู้ใช้อนุญาต push และ merge เข้า develop หลังรายงาน/ทดสอบผ่านเมื่อกลับมาทำงานต่อวันที่ 25 ตุลาคม 2026; ไม่ได้อนุญาต production deployment หรือธุรกรรมจริง การรันอัตโนมัติยังพักไว้ตามคำขอครั้งก่อน หลักฐานดิบขนาดใหญ่เก็บในเครื่องและ CI artifacts; รายงานสรุปและ source ที่เกี่ยวข้องเท่านั้นจะเข้าสู่ Git
