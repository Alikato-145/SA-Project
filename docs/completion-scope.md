# ขอบเขตการปิดระบบ — 13 ตุลาคม 2026

ผู้ใช้ยืนยันใน chat สำหรับงาน FLOW-001–060:

- Payroll จบที่ locked snapshots, adjustments, PDF payslip และ CSV exports
- ไม่เพิ่ม paid/failed/reversed, cash disbursement, bank reconciliation หรือ schema ใหม่
- การยื่น/ชำระประกันสังคมจริงอยู่นอก scope; ระบบส่งออก CSV เท่านั้น
- เอกสารรายบุคคลใน flow นี้ใช้ payslip ไม่สร้าง invoice อีกชนิดโดยไม่มี use case แยก
- OT คงสามประเภทตาม schema เดิม: hourly, rest_day, public_holiday
- ผู้ใช้ยืนยัน 14 ตุลาคม: ฐานประกันสังคมใช้ค่าจ้างพื้นฐานรวมรายวันในงวดตาม code เดิม ไม่รวมสวัสดิการ/OT/adjustment เช่น 27 วัน × 100 บาท ใช้ฐาน 2,700 บาท ไม่ใช่เงินเดือนตามสัญญา 2,600 บาท
- ส่ง payslip ด้วย SMTP จริง; ผู้ใช้จะเตรียม connection การทดสอบใช้ local mail sink
- ผู้ใช้ยืนยัน 14 ตุลาคมให้ใส่ SMTP mock placeholders ก่อน และจะเปลี่ยน connection เองภายหลัง; Mailpit เป็นหลักฐานการส่งในรอบนี้ การส่งถึง inbox ภายนอกไม่ใช่สิ่งที่รับรองจากค่า mock
- Browser ทดสอบได้ด้วยบัญชี demo บน localhost ของ stack ทดสอบแยกเท่านั้น
- ไม่เพิ่ม OCR, device clock, direct bank API, native apps หรือ deferred authentication features

บัญชีส่วนกลางไม่จำเป็นต้องผูก employee ส่วนบัญชี employee ต้องเลือก/สร้าง employee
ก่อนให้ self scope ไม่ย้าย account ที่ผูก employee แล้วไปอีกคนโดย ordinary edit
การเปลี่ยน linkage/สิทธิ์ต้องผ่าน authorized service พร้อมเหตุผลและ audit

นิยามเสร็จ: ทุก in-scope task มี implementation/verification ที่ตรง acceptance criteria,
fixtures/tests ผ่านบน stack แยก, browser flow มีหลักฐาน และ docs ตรงกับสิ่งที่ส่งมอบ
UAT ตัวแทนผู้ใช้, production SMTP credentials และ infrastructure/provider settings
ต้องใช้ข้อมูลจริงจากผู้รับผิดชอบ จึงไม่ถือว่าผ่านจาก automated tests เพียงอย่างเดียว

FLOW-048, FLOW-051, FLOW-052 ปิดด้วย scope นี้; FLOW-049–050 ไม่ applicable
เพราะผู้ใช้ยืนยันว่าไม่ทำ disbursement lifecycle
