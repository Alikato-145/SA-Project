# Haris Payroll DBML Design

## Objective

สร้าง PostgreSQL schema ในรูปแบบ DBML สำหรับนำเข้า dbdiagram.io โดยครอบคลุม flow ตั้งแต่โครงสร้างองค์กร ข้อมูลพนักงาน การลงเวลา การลา OT เงินเบิกล่วงหน้า เงินกู้ หนี้ค่าอาหาร การคำนวณเงินเดือน สลิป และ audit trail

## Design boundaries

- ใช้ `snake_case` และชื่อ table แบบ plural
- ทุก table ใช้ surrogate primary key ชนิด `bigint`
- ใช้ PostgreSQL-compatible types และ DBML enums
- เก็บเวลาเป็น `timestamptz` และวันที่ธุรกิจเป็น `date`
- จำนวนเงินใช้ `numeric(12,2)` และจำนวนวัน/ชั่วโมงใช้ `numeric(8,2)`
- ข้อมูลย้อนหลังไม่ถูกลบจริง โดย master data สำคัญมี `is_active` หรือ status
- DBML แสดง logical constraints; validation ที่ต้องอาศัยหลาย row หรือเวลาให้ backend/service และ database transaction บังคับ

## Domains

### Organization and identity

- `shops` มีหลาย `branches`
- `branches` มีหลาย `departments` และ schedule ของตนเอง
- `positions` เป็น master data
- `employees` เก็บข้อมูลบุคคลและสถานะการจ้าง
- `user_accounts` แยก authentication ออกจากข้อมูลพนักงาน และหนึ่งพนักงานมี account ได้ไม่เกินหนึ่งบัญชี
- `roles` และ `user_account_roles` รองรับ Employee, Supervisor, Branch Manager, HR และ Owner
- `employment_assignments` เก็บประวัติ branch, department, position, salary และ welfare ด้วย `effective_from`/`effective_to`
- `employee_bank_accounts` แยกข้อมูลธนาคารออกจากบัญชีผู้ใช้

### Attendance and scheduling

- `employee_weekly_holidays` เก็บวันหยุดประจำรายบุคคลแบบมีช่วงเวลาที่มีผล
- `branch_schedules` เก็บเวลาเริ่ม/ปิดมาตรฐานแบบ effective-dated
- `branch_schedule_overrides` override เวลาของวันเฉพาะ
- `holiday_calendars` เป็นวันนักขัตฤกษ์ที่ร้านกำหนดเอง
- `work_day_records` มีหนึ่ง row ต่อพนักงานต่อวัน และเก็บผู้คีย์ข้อมูลแยกจากเจ้าของ record

### Leave

- `leave_types` เป็น master data เพิ่มประเภทได้โดยไม่แก้ schema
- `leave_requests` เก็บคำขอระดับใบและผู้ยื่น
- `leave_request_days` แตกใบลาเป็นรายวัน เพื่อรองรับใบเดียวที่มีทั้งวันลาป่วยแบบได้รับและไม่ได้รับค่าจ้าง
- `leave_quotas` unique ต่อ employee, leave type และปี เก็บ `entitled_days` ที่อัปเกรดกลางปีได้
- `leave_approval_actions` เก็บทุก approval/rejection/type change/override เป็น append-only history

### Overtime

- `overtime_records` unique ต่อพนักงานต่อวัน และต้องได้รับอนุมัติก่อนนำไปคำนวณ
- `overtime_approval_actions` เก็บประวัติการพิจารณาแบบ append-only

### Employee finance

- `advance_requests` เก็บคำขอเบิกล่วงหน้าและผลการอนุมัติ
- `loans` เก็บสัญญาเงินกู้ และ `loan_installments` เก็บงวดรายเดือน
- `debt_types` กำหนดประเภทหนี้แบบเพิ่มได้ และ `debt_transactions` เก็บรายการหนี้รายครั้ง ห้ามรีเซ็ตหรือลบประวัติหลังหักเงินเดือน

### Payroll and outputs

- `payroll_periods` เก็บงวดและสถานะ Draft/Preview/Locked
- `payroll_records` มีหนึ่ง row ต่อพนักงานต่องวด และ snapshot ฐานเงินเดือน/สวัสดิการ/ยอดรวม
- `payroll_items` เก็บรายรับและรายหักแต่ละรายการ พร้อม source reference เพื่อ trace กลับ
- `payroll_adjustments` ใช้แก้ไขหลังงวดถูกล็อกโดยไม่แก้ค่าเดิม
- `payroll_configurations` เก็บอัตราและเพดานแบบ effective-dated แยกตามสาขาได้
- `payslips` ผูกหนึ่งต่อหนึ่งกับ payroll record
- `email_delivery_logs` เก็บทุกครั้งที่ส่งสลิป

### Files and audit

- `attachments` รองรับเอกสารพนักงานและใบลา โดยใช้ optional FK ที่ชัดเจน
- `audit_logs` เก็บ actor, action, table, record, old/new data และเวลา

## Critical constraints

- `work_day_records`: unique `(employee_id, work_date)`
- `leave_quotas`: unique `(employee_id, leave_type_id, quota_year)`
- `leave_request_days`: unique `(leave_request_id, leave_date)` และวันลาของพนักงานต้องไม่ซ้อนกัน โดย backend/database exclusion constraint บังคับเพิ่มเติม
- `overtime_records`: unique `(employee_id, overtime_date)`
- `payroll_records`: unique `(payroll_period_id, employee_id)`
- `payslips`: unique `payroll_record_id`
- active `employment_assignments`, weekly holidays, schedules และ payroll configurations ต้องไม่มีช่วงวันที่ทับซ้อนกัน โดย migration จริงเพิ่ม PostgreSQL exclusion constraints
- การ approve leave, consume quota และสร้าง/update work-day record ต้องอยู่ใน transaction เดียวกัน
- การ lock payroll ต้องตรวจ attendance ครบ, pending approvals, net pay ไม่ติดลบ และ snapshot ค่าที่ใช้คำนวณ

## Intended output

ไฟล์ `haris-payroll-postgresql.dbml` ไฟล์เดียวที่ dbdiagram.io import ได้ พร้อม enums, tables, indexes, references และ notes สำหรับกฎที่ DBML บังคับโดยตรงไม่ได้
