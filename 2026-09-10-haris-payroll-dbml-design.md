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


## 25 October 2026 AUTH-01 delivery extension

User-authorized delivery completion adds persistent current-session logout revocation. Migration `0001_auth_session_revocation` adds `revoked_session_tokens` without rewriting historical business data. Keep fingerprints only and expiry indexing; no in-memory-only blacklist. This technical table may be omitted from the business-focused presentation ERD while remaining in the full DBML and executable schema.

## Delivery extension 25 October 2026 current-period adjustments

`payroll_adjustments.employee_id` is required (employees FK RESTRICT/CASCADE), backfilled from the original payroll record before NOT NULL. Original record is nullable for a current-period request. Existing corrections retain locked-origin/later-target/same-shop rules and must match the direct employee. New requests always specify an unlocked target period and valid employee assignment; legacy origin-linked target-null rows remain unchanged. A database origin-or-target CHECK prevents origin-free targetless rows, and a target/employee/status index supports payroll inputs/readiness. Pending current adjustments block lock; approved items enter preview once and are linked to the applied item only on lock. Exact decimal amounts and approval/audit history are preserved.

This resolves the earlier DBML target-NOT-NULL versus nullable executable schema mismatch without rewriting old target values: the logical reference now explicitly documents the legacy nullable exception. The existing approved correction workflow remains supported. Migration0002 adds/backfills the employee field; no table or enum additions.

## Delivery extension 25 October 2026 employee loan requests

The loan feature owns `loan_requests` with `loan_request_status` pending/approved/rejected, direct employee and requester references, immutable requested principal/count/reason, decision actor/time/note and unique nullable loan linkage. Four foreign keys use RESTRICT/CASCADE. PostgreSQL enforces positive numeric(12,2) principal,1–5 installments, nonempty reason and consistent decision metadata; rejected requests require a note and cannot link a loan. Pending requests cannot contain decision/loan metadata. Existing loans/installments are unchanged.

EMPLOYEE may submit/read own requests; HR/OWNER decide. Approval creates the loan and its installment schedule and links it to the request atomically, with row lock and shared payroll-input serialization; duplicate decisions cannot create another loan. Approver selects the first unlocked due month. Requested principal/count are not silently altered. Migration0003 only adds this enum/table/indexes/constraints; no historical loan values are rewritten.

## Delivery extension 25 October 2026 destinations and social-security snapshots

Employees have payment_method cash/transfer (new defaultcash) and nullable canonical10-digit promptpay_phone, separate from contact phone. Migration0004 initializes existing active-primary-bank employees as transfer, otherscash; recipients remainNULL until explicitly registered. DB phone constraint accepts only0[689] plus8digits. Assignment membership defaultsTRUE for existing all-member payroll behavior and changes through effective-dated successor history.

Payroll records add required is_social_security_member_snapshot defaultTRUE and nullable/nonnegative social_security_base_snapshot. New calculations persist covered daily base earnings, excluding welfare/OT/adjustments. Legacy earned-base staysNULL; reports must derive a fallback from frozen base_salary items, never current monthly salary or0. No old locked payroll rows are updated, and the immutable trigger remains intact. Root pre/post fingerprints of135lockedrecords (excludingonlynewcolumns) and8919items matched exactly on disposable migration. Payment preparation will freeze recipient/amount separately in Task7; generating/scanningQR never marks paid.

## Delivery extension 25 October 2026 prepared payment snapshots

Payroll owns `payroll_payments` and prepared/paid/cancelled status. Required record/branch/channel/positive exact amount/preparer/time, nullable bank FK/phone and complete bank snapshot tuple; encrypted account envelope already embeds key version. Six RESTRICT/CASCADE foreign keys retain source/actor records. A partial UNIQUE index permits only one prepared/paid payment per payroll record while keeping cancelled history; DBML documents this PostgreSQL-only uniqueness rather than incorrectly making all historical record references unique.

Checks enforce canonical phone, complete-or-absent bank tuple, cash without destination, a usable transfer destination and consistent status/decision actor/time/reason. Migration0005 trigger enforces full locked net and frozen assignment branch, member-bank/nonmember-phone transfer requirements, immutable snapshot/preparation fields, no deletes and only prepared→paid/cancelled transitions. Idempotent APIs must return existing rows without a no-op UPDATE. Task7 exposes preparation/groups/QR; Task8 adds lifecycle endpoints, so schema presence does not imply paid confirmation UI is complete.

Root pre/post migration fingerprints matched138locked payroll records and9150items on disposable verificationDB; no historical results changed. Generation/scanning QR never confirms payment or triggers a bank transfer.

## Current 20-use-case alignment 26 October 2026 advance reason

The user-authorized UC12 repair adds only nullable `advance_requests.reason text` in migration0006. New request service/API/UI writes require a trimmed nonblank reason with at most1,000 characters; legacy NULL remains an honest absence of recorded reason. New rejection decisions require a similarly bounded nonblank decision note; existing decisions are not rewritten. No new tables, enums or FKs, no backfill of fictional historic reasons, and no eligibility/loan/payroll rule changes. Root schema-owner review of generated SQL/meta/logical parity and disposable pre/post historic fingerprints is required before applying the migration. Application is authorized only to the existing disposable verification database; no production application, reset or historic payroll mutation.
