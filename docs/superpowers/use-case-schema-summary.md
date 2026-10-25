# Schema สำหรับอธิบาย Use Case

คำอธิบาย schema หลัง delivery Tasks2–10 สำหรับใช้ประกอบคู่มือและภาพนำเสนอ ไม่ใช่การเปลี่ยน schema; ผลตรวจ UAT แยกอยู่ใน [รายงาน Task11](reports/11-full-use-case-uat.md) โมเดลเต็มอ้างอิง `haris-payroll-postgresql.dbml` และ executable feature schemas; การลดตารางในภาพนำเสนอไม่ตัดตารางออกจากฐานข้อมูลจริง

| ขอบเขตที่อธิบาย | ตารางหลักที่ควรปรากฏ | ความหมายสำคัญ |
|---|---|---|
| Login และสิทธิ์ | user_accounts, roles, user_account_roles | บัญชีและ employee เป็นคนละ entity; scope อยู่ที่ account-role; บัญชีใช้ HR grant |
| UC1–3 ข้อมูลพนักงาน | employees, employment_assignments, branches, departments, positions | ยุติใช้งานแทนลบประวัติ; เปลี่ยนสาขา/ค่าจ้างด้วย effective-dated assignment |
| UC4–6 คำนวณ/ปรับ/ปิดงวด | payroll_periods, payroll_records, payroll_items, payroll_adjustments | ผลรายคนไม่ซ้ำในงวด; ปรับรายได้/หักผ่านอนุมัติ; ล็อกแล้วไม่แก้ตรง |
| UC7–11 ช่องทาง/กลุ่ม/ผลจ่าย | payroll_payments, employee_bank_accounts และ employees/assignment/payroll_records ที่มีอยู่ | เบอร์รับ PromptPay แยกจากเบอร์ติดต่อ; freeze ปลายทาง/ยอด/สาขา; prepared/paid/cancelled; กลุ่ม SS มาก่อน cash/transfer |
| UC12–14 สลิป/อีเมล/สรุป | payslips, email_delivery_logs และ locked payroll_records/items | สลิปรายคนและรายงานสรุปอ่านข้อมูลเดียวกัน; ไม่สร้างสลิปด้วยการแปลงกลับจาก PDF; สรุปเจ้าหนี้คือเงินเดือนที่ร้านต้องจ่าย |
| UC15 ยื่นลา | leave_requests, leave_request_days, leave_types | คำขอเป็นของ employee; วันลาทับซ้อนไม่ได้; approval/quota เป็นรายละเอียดสนับสนุน |
| UC16 ยื่นกู้/เบิกล่วงหน้า | loan_requests, loans, loan_installments, advance_requests | คำขอกู้ approved จึงสร้าง loan/installments ใน transaction; advance มีเงื่อนไขวันและวงเงิน |

หากภาพหลักแน่น สามารถแสดง child tables และตารางสนับสนุนในภาพขยายแยก: revoked_session_tokens, leave_approval_actions, leave_quotas, overtime_records/overtime_approval_actions, work_day_records, payroll_configurations, debt_transactions/debt_types, audit_logs, attachments และตารางตารางทำงาน/วันหยุด ภาพหลักต้องระบุว่าตัดรายละเอียดสนับสนุนเพื่ออธิบาย Use Case ไม่อ้างว่าเป็นฐานข้อมูลทั้งหมด

ความต่างจาก schema ก่อน delivery: persistent logout revocation; current-period adjustment ผูก employee โดย origin ว่างได้; loan_requests; ช่องทางและเบอร์รับเงิน; effective SS membership/earned-base snapshots; payroll_payments พร้อมปลายทางและประวัติสถานะ การออก PDF สรุปไม่จำเป็นต้องมีตาราง PDF แยก เพราะสร้างจากข้อเท็จจริงที่ล็อกแล้ว

ข้อควรแสดงในคำอธิบาย: QR ไม่ใช่หลักฐานจ่ายสำเร็จ, ยกเลิกการเตรียมจ่ายไม่ใช่ย้อนการโอนธนาคาร, กลุ่ม SS สิ้นงวดแยกจากฐานรายได้ที่มีสิทธิ์แต่ละวัน และข้อมูลเก่าต้องไม่เปลี่ยนตามบัญชี/สาขาปัจจุบัน การตรวจ UAT นี้ไม่เปลี่ยน schema/migration; สถานะการ review ขั้นสุดท้ายแยกอยู่ใน progress ledger
