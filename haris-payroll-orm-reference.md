# Haris Payroll — Table & Relationship Reference

เอกสารนี้อธิบาย schema จาก `haris-payroll-postgresql.dbml` เพื่อใช้เป็น reference ตอนเขียน ORM สำหรับ PostgreSQL

## 1. Mental model

ระบบแบ่งข้อมูลเป็น 7 domain:

```text
Organization
  shops → branches → departments
                    ↘ employment_assignments ← positions

Identity & employment
  employees ↔ user_accounts ↔ roles
      └── employment_assignments / bank_accounts / weekly_holidays

Daily operation
  employees → work_day_records
            → leave_requests → leave_request_days
            → overtime_records

Employee finance
  employees → advance_requests
            → loans → loan_installments
            → debt_transactions

Payroll
  shops → payroll_periods → payroll_records → payroll_items
                                     └──────→ payslips → email_delivery_logs

Supporting data
  payroll_configurations / attachments / audit_logs
```

`employees` เป็นศูนย์กลางของข้อมูลเชิงธุรกิจ แต่ `user_accounts` เป็นตัวแทนของผู้กระทำในระบบ เช่น คนคีย์เวลา คนอนุมัติ และคนล็อกงวด ทั้งสองความหมายต้องไม่ปนกัน

## 2. Cardinality notation

- `1:N` — parent หนึ่ง row มี child ได้หลาย row; child เก็บ FK
- `1:0..1` — parent อาจมี child ได้ไม่เกินหนึ่ง row; FK ฝั่ง child ต้อง `unique`
- `N:M` — ใช้ junction table คั่นกลาง
- Optional FK — column เป็น nullable; relation ใน ORM ควรเป็น optional
- Snapshot FK — ชี้ไปยังข้อมูลต้นทางพร้อมเก็บค่าที่ใช้จริงซ้ำไว้ เพื่อรักษาประวัติ

## 3. Organization

### `shops`

ร้านหรือองค์กรระดับบนสุด ใช้รองรับกรณีระบบมีหลายร้านในอนาคต

ฟิลด์สำคัญ:

- `id` — PK
- `code` — business key, unique
- `name`
- `is_active` — ปิดใช้งานโดยไม่ลบข้อมูล

Relationships:

- `shops 1:N branches`
- `shops 1:N positions`
- `shops 1:N holiday_calendars`
- `shops 1:N payroll_configurations`
- `shops 1:N payroll_periods`

ชื่อ relation ใน ORM:

```text
Shop.branches
Shop.positions
Shop.holidays
Shop.payrollConfigurations
Shop.payrollPeriods
```

### `branches`

สาขาของร้าน เช่น ครัวกลางหรือสาขาขาย

ฟิลด์สำคัญ:

- `shop_id` — FK ไป `shops`
- `code` — unique ภายในร้านด้วย `(shop_id, code)`
- `timezone` — ใช้แปลงเวลาเข้าออกและตัดวันทำงาน
- `is_active`

Relationships:

- `branches N:1 shops`
- `branches 1:N departments`
- `branches 1:N employment_assignments`
- `branches 1:N branch_schedules`
- `branches 1:N branch_schedule_overrides`
- `branches 1:N work_day_records`
- `branches 1:N scoped user_account_roles`
- `branches 1:N payroll_configurations` แบบ optional scope

`work_day_records.branch_id` เป็น snapshot ว่าพนักงานทำงานที่สาขาใดในวันนั้น ไม่ควรคำนวณจากสังกัดปัจจุบันย้อนหลัง

### `departments`

แผนกภายในสาขา เช่น ครัวร้อน ครัวเย็น และบริการ

ฟิลด์สำคัญ:

- `branch_id` — FK ไป `branches`
- `code` — unique ภายในสาขา
- `name`
- `is_active`

Relationships:

- `departments N:1 branches`
- `departments 1:N employment_assignments`
- `departments 1:N scoped user_account_roles`

ตอนสร้าง `employment_assignments` ต้อง validate ว่า `department.branch_id` ตรงกับ `branch_id` ใน assignment เพราะ FK ธรรมดายังบังคับเงื่อนไขข้ามสอง column นี้ไม่ได้

### `positions`

ตำแหน่งงาน เช่น พนักงานครัว หัวหน้าแผนก หรือผู้จัดการ

ฟิลด์สำคัญ:

- `shop_id` — ตำแหน่งเป็น master data ระดับร้าน
- `code`, `name`, `is_active`
- unique `(shop_id, code)`

Relationships:

- `positions N:1 shops`
- `positions 1:N employment_assignments`

`positions` ไม่ควรเก็บเงินเดือน เพราะเงินเดือนขึ้นกับพนักงานและช่วงเวลาจริง จึงอยู่ใน `employment_assignments`

## 4. Identity and access control

### `employees`

ข้อมูลตัวบุคคลและสถานะการจ้าง เป็น strong entity หลักของระบบ HR

ฟิลด์สำคัญ:

- `employee_code` — business key, unique
- `national_id` / `passport_id` — อย่างน้อยหนึ่งค่าต้องมี และแต่ละค่าห้ามซ้ำ
- ข้อมูลชื่อ ติดต่อ และที่อยู่
- `hire_date`
- `status`, `terminated_at`

Relationships:

- `employees 1:0..1 user_accounts`
- `employees 1:N employment_assignments`
- `employees 1:N employee_bank_accounts`
- `employees 1:N employee_weekly_holidays`
- `employees 1:N work_day_records`
- `employees 1:N leave_requests`
- `employees 1:N leave_quotas`
- `employees 1:N overtime_records`
- `employees 1:N advance_requests`
- `employees 1:N loans`
- `employees 1:N debt_transactions`
- `employees 1:N payroll_records`
- `employees 1:N attachments`

ORM ควรใช้ `Employee` เป็น aggregate สำหรับข้อมูล HR แต่ไม่ควร eager-load relation ทุกตัวพร้อมกัน เพราะ collection จะโตตามอายุงาน

### `user_accounts`

ข้อมูล authentication แยกออกจาก Employee เพื่อไม่ให้ password และสถานะ login ปนกับข้อมูล HR

ฟิลด์สำคัญ:

- `employee_id` — nullable + unique; account บางประเภท เช่น owner อาจไม่ใช่พนักงาน
- `username`, `password_hash`
- `status`
- `failed_login_attempts`, `locked_until`, `last_login_at`

Relationships:

- `user_accounts 0..1:1 employees`
- `user_accounts N:M roles` ผ่าน `user_account_roles`
- ถูกอ้างเป็น actor ในตารางการสร้าง แก้ไข อนุมัติ คำนวณ และล็อกข้อมูล

ใน ORM แนะนำแยกชื่อ relation ตามหน้าที่ เช่น `submittedLeaveRequests`, `recordedWorkDays`, `approvedLoans` แทนชื่อกว้าง ๆ อย่าง `actions`

### `roles`

Role master สำหรับ `EMPLOYEE`, `SUPERVISOR`, `BRANCH_MANAGER`, `HR`, `OWNER`

ฟิลด์สำคัญ:

- `code` — unique
- `scope` — `self`, `department`, `branch`, `all`
- `is_active`

Relationships:

- `roles N:M user_accounts` ผ่าน `user_account_roles`

`role` บอกประเภทสิทธิ์ ส่วน `branch_id`/`department_id` ใน junction table บอกขอบเขตจริง

### `user_account_roles`

Junction table ระหว่าง account กับ role พร้อม data scope

ฟิลด์สำคัญ:

- `user_account_id`, `role_id`
- `branch_id` — nullable สำหรับ role ระดับ branch
- `department_id` — nullable สำหรับ role ระดับ department
- `granted_by_user_account_id`, `granted_at`

Relationships:

- `N:1 user_accounts`
- `N:1 roles`
- optional `N:1 branches`
- optional `N:1 departments`
- optional self-domain relation ไป account ผู้ให้สิทธิ์

Validation ที่ service/database trigger ต้องทำ:

```text
scope=self        → branch_id=NULL, department_id=NULL
scope=department  → department_id required
scope=branch      → branch_id required, department_id=NULL
scope=all         → branch_id=NULL, department_id=NULL
```

PostgreSQL `UNIQUE` ที่มี nullable columns ยอมให้ค่า `NULL` ซ้ำได้ จึงควรเพิ่ม partial unique indexes ใน migration จริง หรือ validate ผ่าน service

## 5. Employment and compensation history

### `employment_assignments`

เก็บประวัติสังกัด ตำแหน่ง เงินเดือน และสวัสดิการแบบ effective-dated

ฟิลด์สำคัญ:

- FK: `employee_id`, `branch_id`, `department_id`, `position_id`
- `employment_type`
- `base_salary`, `welfare_amount`
- `effective_from`, `effective_to`
- `is_primary`
- `created_by_user_account_id`

Relationships:

- `N:1 employees`
- `N:1 branches`
- `N:1 departments`
- `N:1 positions`
- optional `N:1 user_accounts` ในฐานะผู้สร้าง
- `1:N payroll_records`

ห้าม update assignment เดิมเมื่อย้ายสาขาหรือขึ้นเงินเดือน ให้ปิด row เดิมด้วย `effective_to` แล้วสร้าง row ใหม่ ช่วงเวลาของ employee เดียวกันต้องไม่ overlap

### `employee_bank_accounts`

บัญชีธนาคารสำหรับรับเงินเดือน แยกเพื่อลดขอบเขตการเข้าถึงข้อมูลอ่อนไหว

ฟิลด์สำคัญ:

- `employee_id`
- `bank_code`, `bank_name`
- `account_holder_name`
- `account_number_ciphertext`, `account_number_last4`
- `is_primary`, `is_active`

Relationships:

- `employee_bank_accounts N:1 employees`

ควรมี business rule ให้พนักงานหนึ่งคนมี active primary account ได้เพียงบัญชีเดียว ผ่าน PostgreSQL partial unique index

## 6. Schedule and attendance

### `employee_weekly_holidays`

วันหยุดประจำสัปดาห์ของพนักงานแบบมีช่วงเวลาที่มีผล

ฟิลด์สำคัญ:

- `employee_id`
- `weekday` — `0..6`
- `effective_from`, `effective_to`

Relationships:

- `N:1 employees`

ใช้ตัดสินว่าการไม่มาทำงานเป็นวันหยุดหรือขาดงาน และใช้เสนอ `overtime_type=rest_day`

### `branch_schedules`

เวลาเริ่มงาน เวลาปิดมาตรฐาน และ grace period ของแต่ละสาขา

ฟิลด์สำคัญ:

- `branch_id`
- `work_start_time`, `standard_close_time`
- `late_grace_minutes`
- `effective_from`, `effective_to`

Relationships:

- `N:1 branches`

ช่วง schedule ของ branch เดียวกันต้องไม่ overlap เพื่อให้เลือกค่า ณ วันทำงานได้เพียง row เดียว

### `branch_schedule_overrides`

เวลาเปิด/ปิดเฉพาะวัน ซึ่ง override `branch_schedules`

ฟิลด์สำคัญ:

- `branch_id`, `schedule_date` — unique คู่กัน
- `work_start_time`, `close_time`, `is_closed`
- `reason`, `created_by_user_account_id`

Relationships:

- `N:1 branches`
- optional `N:1 user_accounts` ผู้สร้าง

เวลาใช้งานจริง:

```text
schedule override ของวันนั้น ?? active branch schedule ของวันนั้น
```

### `holiday_calendars`

วันนักขัตฤกษ์ที่ร้านกำหนดเอง ไม่จำเป็นต้องตรงกับปฏิทินราชการ

ฟิลด์สำคัญ:

- `shop_id`, `holiday_date` — unique คู่กัน
- `name`, `is_active`
- `created_by_user_account_id`

Relationships:

- `N:1 shops`
- optional `N:1 user_accounts`

### `work_day_records`

ข้อเท็จจริงระดับพนักงานต่อวัน เป็นฐานของ attendance และ payroll

ฟิลด์สำคัญ:

- `employee_id`, `work_date` — unique คู่กัน
- `branch_id` — snapshot สาขาที่ทำงานจริง
- `clock_in_at`, `clock_out_at`
- `status`
- `late_minutes`, `is_deductible`
- `entry_source`
- `created_by_user_account_id`

Relationships:

- `N:1 employees` — เจ้าของ attendance
- `N:1 branches` — สาขา ณ วันนั้น
- optional `N:1 user_accounts` — ผู้คีย์
- `1:0..1 leave_request_days`
- `1:N overtime_records` ใน schema; business constraint employee/date จำกัด OT เหลือหนึ่งรายการ

แยกความหมายให้ชัด:

```text
employee_id                    = คนที่มาทำงาน
created_by_user_account_id     = คนที่กรอกข้อมูล
```

## 7. Leave

### `leave_types`

Master data ของประเภทการลา เพื่อเพิ่มลากิจหรือประเภทใหม่ได้โดยไม่แก้ schema

ฟิลด์สำคัญ:

- `code`, `name_th`
- `quota_type`: fixed/by_seniority/none
- `quota_days`
- `is_deductible`
- `requires_document`
- `allow_exceed`
- `is_active`

Relationships:

- `1:N leave_requests` ทั้ง original และ final type
- `1:N leave_request_days`
- `1:N leave_quotas`
- `1:N leave_approval_actions` สำหรับ from/to type

### `leave_requests`

หัวใบคำขอลา เก็บช่วงวันที่ เหตุผล และสถานะ workflow

ฟิลด์สำคัญ:

- `employee_id`
- `original_leave_type_id` — ประเภทที่พนักงานยื่น
- `final_leave_type_id` — ประเภทสุดท้ายหลังผู้อนุมัติแก้; nullable ขณะ pending
- `start_date`, `end_date`, `requested_days`
- `status`, `is_retroactive`
- `submitted_by_user_account_id`, `submitted_at`, `decided_at`

Relationships:

- `N:1 employees`
- `N:1 leave_types` ผ่าน `original_leave_type_id`
- optional `N:1 leave_types` ผ่าน `final_leave_type_id`
- `N:1 user_accounts` ผู้ยื่น
- `1:N leave_request_days`
- `1:N leave_approval_actions`
- `1:N attachments`

ไม่ควรใช้ header row นี้ตัดสินการหักเงิน เพราะหนึ่งใบสามารถมีทั้ง paid และ unpaid days

### `leave_request_days`

รายละเอียดการลารายวัน เป็นตัวแก้กรณีใบลาคร่อมโควตา

ฟิลด์สำคัญ:

- `leave_request_id`, `leave_date` — unique ภายในใบ
- `work_day_record_id` — optional + unique
- `leave_type_id`
- `day_amount` — รองรับครึ่งวัน
- `is_paid`, `is_deductible`
- `quota_consumed`

Relationships:

- `N:1 leave_requests`
- optional `1:1 work_day_records`
- `N:1 leave_types`

ตัวอย่าง: ลาป่วย 5 วัน เหลือสิทธิ์ 2 วัน จะมี 5 rows โดย 2 rows แรก `is_paid=true` และ 3 rows หลัง `is_deductible=true`

### `leave_quotas`

โควตารายปีต่อพนักงานและประเภทการลา

ฟิลด์สำคัญ:

- unique `(employee_id, leave_type_id, quota_year)`
- `entitled_days`
- `used_days`
- `last_recalculated_at`
- `frozen_at` — ปีเก่าที่ปิดแล้ว

Relationships:

- `N:1 employees`
- `N:1 leave_types`

การ approve leave, เพิ่ม `used_days` และสร้าง/link `work_day_records` ต้องทำใน database transaction เดียว และ lock quota row ป้องกัน concurrent approvals

### `leave_approval_actions`

Append-only history ของทุก action ต่อใบลา

ฟิลด์สำคัญ:

- `leave_request_id`
- `actor_user_account_id`
- `action`
- `from_leave_type_id`, `to_leave_type_id`
- `remark`, `acted_at`

Relationships:

- `N:1 leave_requests`
- `N:1 user_accounts` ผู้กระทำ
- optional `N:1 leave_types` ทั้งก่อนและหลังเปลี่ยน

อย่า update action เก่าเมื่อมีการ override ให้ append row ใหม่เสมอ

## 8. Overtime

### `overtime_records`

คำขอหรือรายการ OT ของพนักงาน ต้องอนุมัติก่อนเข้า payroll

ฟิลด์สำคัญ:

- unique `(employee_id, overtime_date)` ป้องกัน OT ซ้อนสองประเภท
- `work_day_record_id` — optional
- `overtime_type`
- `hours` สำหรับ hourly OT
- `day_units` สำหรับ rest-day/public-holiday OT
- `status`, `reason`
- `requested_by_user_account_id`

Relationships:

- `N:1 employees`
- optional `N:1 work_day_records`
- `N:1 user_accounts` ผู้บันทึก
- `1:N overtime_approval_actions`

Service ต้อง validate ตาม type:

```text
hourly                 → hours required, day_units NULL
rest_day/public_holiday → day_units required, hours NULL
```

### `overtime_approval_actions`

Append-only approval history ของ OT

Relationships:

- `N:1 overtime_records`
- `N:1 user_accounts` ผู้อนุมัติหรือปฏิเสธ

เก็บ `action`, `remark`, `acted_at` เพื่อ audit workflow

## 9. Advance, loan, and debt

### `advance_requests`

คำขอเบิกเงินล่วงหน้ารายเดือน

ฟิลด์สำคัญ:

- unique `(employee_id, request_month)` — เดือนละครั้ง
- `request_month` ต้องเก็บเป็นวันแรกของเดือน
- `amount`, `status`
- `requested_by_user_account_id`
- `decided_by_user_account_id`, `decided_at`, `decision_note`

Relationships:

- `N:1 employees`
- `N:1 user_accounts` ผู้ยื่น
- optional `N:1 user_accounts` ผู้ตัดสิน

เงื่อนไขวันที่ 20, ทำงานครบ 20 วัน, ไม่เกินครึ่งเงินเดือน และ net pay ไม่ติดลบเป็น cross-table validation ที่ service ต้องตรวจ

### `loans`

สัญญาเงินกู้ของพนักงาน

ฟิลด์สำคัญ:

- `employee_id`
- `principal_amount`
- `installment_count` — 1 ถึง 5
- `status`
- `approved_by_user_account_id`, `approved_at`
- `closed_at`

Relationships:

- `N:1 employees`
- `N:1 user_accounts` ผู้อนุมัติ
- `1:N loan_installments`

ยอดคงเหลือควร derive จาก principal และ installments ที่ deducted หรือเก็บเป็น cached value พร้อม reconciliation ไม่ควรเป็นแหล่งข้อมูลจริงเพียงจุดเดียว

### `loan_installments`

ตารางงวดชำระของ loan

ฟิลด์สำคัญ:

- unique `(loan_id, installment_no)`
- `due_period_start`
- `amount`, `status`
- `payroll_record_id`, `deducted_at`

Relationships:

- `N:1 loans`
- optional `N:1 payroll_records` งวดที่หักจริง

เมื่อ payroll ถูก lock จึงเปลี่ยน installment เป็น `deducted`; การ preview ไม่ควรเปลี่ยนสถานะจริง

### `debt_types`

ประเภทหนี้แบบเพิ่มได้ เช่น ค่าอาหาร ค่าอุปกรณ์ หรือค่าเสียหาย

ฟิลด์สำคัญ:

- `code` — unique
- `name_th`, `description`, `is_active`

Relationships:

- `1:N debt_transactions`

### `debt_transactions`

Ledger ของหนี้พนักงาน เก็บรายการเพิ่ม ปรับ และย้อนรายการโดยไม่ลบประวัติ

ฟิลด์สำคัญ:

- `employee_id`, `debt_type_id`
- `transaction_kind`: charge/adjustment/reversal
- `transaction_date`, `description`, `amount`
- `original_transaction_id` — self FK สำหรับ reversal
- `recorded_by_user_account_id`
- `settled_in_payroll_record_id`, `settled_at`

Relationships:

- `N:1 employees`
- `N:1 debt_types`
- optional self `N:1 debt_transactions` ผ่าน `original_transaction_id`
- `N:1 user_accounts` ผู้บันทึก
- optional `N:1 payroll_records` ที่นำรายการไปหัก

`amount` เป็นค่าบวกเสมอ ส่วนเครื่องหมายทางบัญชี derive จาก `transaction_kind` ช่วยลดความสับสนระหว่าง negative amount กับ reversal

## 10. Payroll

### `payroll_configurations`

ค่าคอนฟิกการคำนวณแบบ effective-dated เช่นอัตราสาย ขาด OT ประกันสังคม และจำนวนวันหาร

ฟิลด์สำคัญ:

- `shop_id`
- `branch_id` — nullable; NULL หมายถึงค่า default ระดับร้าน
- `config_key`, `numeric_value`, `unit`
- `effective_from`, `effective_to`
- `created_by_user_account_id`

Relationships:

- `N:1 shops`
- optional `N:1 branches`
- `N:1 user_accounts` ผู้ตั้งค่า
- `1:N payroll_items` ที่อ้างอัตรานี้

ลำดับเลือก config:

```text
active branch-specific value ?? active shop-wide value
```

ช่วงวันที่ของ `shop + branch + config_key` ต้องไม่ overlap

### `payroll_periods`

หัวงวดเงินเดือนของร้าน

ฟิลด์สำคัญ:

- unique `(shop_id, period_year, period_month)`
- `start_date`, `end_date`
- `status`: draft/previewed/locked
- `created_by_user_account_id`
- `locked_by_user_account_id`, `locked_at`

Relationships:

- `N:1 shops`
- `N:1 user_accounts` ผู้สร้าง
- optional `N:1 user_accounts` ผู้ล็อก
- `1:N payroll_records`
- `1:N payroll_adjustments` ที่นำไปใช้ในงวดนี้

หลัง `locked` ห้ามแก้ record/item เดิม ให้ใช้ `payroll_adjustments`

### `payroll_records`

ผลคำนวณหนึ่งพนักงานในหนึ่งงวด

ฟิลด์สำคัญ:

- unique `(payroll_period_id, employee_id)`
- `employment_assignment_id`
- `base_salary_snapshot`, `welfare_snapshot`
- `total_earnings`, `total_deductions`, `net_pay`
- `status`, `calculated_at`, `calculated_by_user_account_id`

Relationships:

- `N:1 payroll_periods`
- `N:1 employees`
- `N:1 employment_assignments`
- optional `N:1 user_accounts` ผู้คำนวณ
- `1:N payroll_items`
- `1:N loan_installments` ที่ถูกหักใน record นี้
- `1:N debt_transactions` ที่ถูก settle ใน record นี้
- `1:N payroll_adjustments` ในฐานะ original record
- `1:1 payslips`

`employment_assignment_id` ใช้ trace ต้นทาง ส่วน `base_salary_snapshot` และ `welfare_snapshot` เป็นค่าหลักสำหรับการแสดงย้อนหลัง แม้ assignment ถูกปิดในอนาคต

### `payroll_items`

รายละเอียด line item ของรายรับและรายหัก

ฟิลด์สำคัญ:

- `payroll_record_id`
- `item_type`, `direction`
- `description`, `quantity`, `rate`, `amount`
- `payroll_configuration_id`
- `source_table`, `source_id`
- `occurred_on`

Relationships:

- `N:1 payroll_records`
- optional `N:1 payroll_configurations`
- `1:0..1 payroll_adjustments` ผ่าน `applied_payroll_item_id`

`source_table/source_id` เป็น polymorphic reference เช่น:

```text
source_table='overtime_records', source_id=125
source_table='advance_requests', source_id=41
source_table='loan_installments', source_id=84
```

ORM ทั่วไปสร้าง FK relation ให้ polymorphic pair นี้ไม่ได้ ควรมี `PayrollSourceResolver` ใน service layer และ validate table whitelist เอง

### `payroll_adjustments`

รายการแก้ไขสำหรับข้อมูลที่เกี่ยวข้องกับ payroll ที่ถูกล็อกแล้ว

ฟิลด์สำคัญ:

- `original_payroll_record_id`
- `applied_payroll_period_id` — nullable จนกว่าจะเลือกงวดชดเชย
- `direction`, `amount`, `reason`, `status`
- ผู้ขอและผู้อนุมัติ
- `applied_payroll_item_id` — optional + unique

Relationships:

- `N:1 payroll_records` ต้นฉบับ
- optional `N:1 payroll_periods` งวดที่นำไปใช้
- `N:1 user_accounts` ผู้ขอ
- optional `N:1 user_accounts` ผู้อนุมัติ
- optional `1:1 payroll_items` ที่สร้างจาก adjustment

### `payslips`

Metadata ของไฟล์สลิปที่สร้างจาก payroll record

ฟิลด์สำคัญ:

- `payroll_record_id` — unique ทำให้เป็น 1:1
- `file_storage_key`, `file_sha256`
- `status`, `generated_at`
- ผู้สร้างและผู้ void

Relationships:

- `1:1 payroll_records`
- optional `N:1 user_accounts` ผู้สร้าง/ผู้ void
- `1:N email_delivery_logs`

ไม่ควรเก็บ binary PDF ใน row; เก็บ object-storage key และ hash สำหรับตรวจความถูกต้อง

### `email_delivery_logs`

ประวัติการส่งสลิปทุกครั้ง รวม retry

ฟิลด์สำคัญ:

- `payslip_id`
- `recipient_email` — snapshot ปลายทางจริงในครั้งนั้น
- `status`, `provider_message_id`
- `attempted_at`, `sent_at`, `error_message`

Relationships:

- `N:1 payslips`

หนึ่ง payslip มีหลาย logs ได้ เพราะการส่งครั้งแรกอาจล้มเหลวแล้ว retry

## 11. Files and audit

### `attachments`

Metadata ของไฟล์เอกสารพนักงานหรือเอกสารประกอบใบลา

ฟิลด์สำคัญ:

- `employee_id` หรือ `leave_request_id` ต้องมีเพียงหนึ่งค่า
- `file_name`, `storage_key`, `mime_type`, `file_size_bytes`, `file_sha256`
- `uploaded_by_user_account_id`, `uploaded_at`

Relationships:

- optional `N:1 employees`
- optional `N:1 leave_requests`
- `N:1 user_accounts` ผู้อัปโหลด

รูปแบบนี้เป็น exclusive ownership ไม่ใช่ polymorphic string และมี check constraint บังคับว่า owner ต้องมีหนึ่งประเภทพอดี

### `audit_logs`

Audit trail ระดับระบบสำหรับ create/update/approve/calculate/lock และเหตุการณ์สำคัญ

ฟิลด์สำคัญ:

- `actor_user_account_id` — nullable สำหรับ scheduled job/system action
- `action`
- `table_name`, `record_id`
- `old_data`, `new_data` แบบ `jsonb`
- `reason`, `occurred_at`, `request_id`

Relationships:

- optional `N:1 user_accounts`
- ไม่มี physical FK จาก `table_name/record_id` เพราะเป็น polymorphic audit target

Audit log ควร append-only และไม่ expose ข้อมูลลับ เช่น `password_hash` หรือเลขบัญชีที่ถอดรหัสแล้วใน JSON

## 12. Recommended ORM relationship names

ตารางต่อไปนี้มีหลาย FK ไป target เดียวกัน ต้องตั้งชื่อ relation ชัดเจนเพื่อไม่ให้ ORM สร้างชื่อชนกัน:

```text
LeaveRequest.originalLeaveType
LeaveRequest.finalLeaveType
LeaveApprovalAction.fromLeaveType
LeaveApprovalAction.toLeaveType

PayrollPeriod.createdBy
PayrollPeriod.lockedBy

PayrollAdjustment.requestedBy
PayrollAdjustment.approvedBy

Payslip.generatedBy
Payslip.voidedBy

AdvanceRequest.requestedBy
AdvanceRequest.decidedBy
```

## 13. Delete behavior

- `cascade` ใช้เฉพาะ child ที่ไม่มีความหมายเมื่อ parent หาย เช่น `user_account_roles` และ `leave_request_days`
- `restrict` ใช้กับ business/history data เช่น employee, payroll, loan, approval และ payslip
- `set null` ใช้กับ actor metadata หรือ optional link ที่ไม่ควรทำให้ transaction history หาย
- ในระบบจริงควรหลีกเลี่ยงการลบ `employees`, `user_accounts`, master data และ transaction rows; ใช้ status/soft delete ตาม requirement

## 14. ORM implementation order

ลำดับสร้าง model/migration ที่ dependency ไม่ย้อนกันมากเกินไป:

1. Enums
2. `shops`, `branches`, `departments`, `positions`
3. `employees`, `roles`, `user_accounts`, `user_account_roles`
4. `employment_assignments`, bank accounts, schedules, holidays
5. `work_day_records`
6. Leave tables
7. OT tables
8. `advance_requests`, `loans`, `loan_installments`, `debt_types`, `debt_transactions`
9. Payroll configuration, period, record และ items
10. Payroll adjustments, payslips และ email logs
11. Attachments และ audit logs

`loan_installments` และ `debt_transactions` มี optional FK ไป `payroll_records` จึงอาจต้องสร้าง FK เหล่านี้ใน migration หลังสร้าง payroll tables แล้ว แม้ ORM model จะประกาศ relation ไว้ตั้งแต่ต้นได้

## 15. Constraints that ORM relations alone cannot guarantee

ต้องทำเพิ่มใน migration หรือ service layer:

- ช่วง `employment_assignments` ของ employee เดียวกันห้าม overlap
- branch schedule/config effective periods ห้าม overlap
- พนักงานมี active primary bank account ได้เพียงหนึ่งบัญชี
- scoped role ต้องมี branch/department ตรงกับ `role.scope`
- ใบลาที่ approved ของพนักงานเดียวกันห้ามซ้อนวัน
- leave quota update ต้องใช้ row lock/transaction
- `overtime_records` ต้องมี `hours` หรือ `day_units` ให้ตรงกับ type
- payroll preview ห้ามเปลี่ยนสถานะ loan/debt; เปลี่ยนเฉพาะตอน lock สำเร็จ
- total ใน `payroll_records` ต้อง reconcile กับผลรวม `payroll_items`
- `source_table/source_id` และ `audit_logs.table_name/record_id` ไม่มี physical FK
