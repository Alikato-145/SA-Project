# แหล่งข้อความแผนภาพเชิงแนวคิด

## 1 ลำดับงานเงินเดือนหลังปรับปรุง

```mermaid
flowchart LR
    A[กำหนดสิทธิ์และข้อมูลพนักงาน] --> B[ลงเวลาและรับคำขอ]
    B --> C[อนุมัติลาและ OT]
    C --> D[จัดการเงินทดรอง เงินกู้ และหนี้]
    D --> E[สร้างรอบและคำนวณตัวอย่าง]
    E --> F[ตรวจเงื่อนไขและล็อกรอบ]
    F --> G[จัดการสลิปและส่งออกรายงาน]
    G --> H[ตรวจประวัติการกระทำ]
```

![ลำดับงานเงินเดือนหลังปรับปรุง](figures/concept-01.png)

## 2 การส่งต่อข้อมูลในกระบวนการเดิม

```mermaid
flowchart LR
    S[สาขา] -->|ข้อมูลขาด ลา สาย OT| H[HR]
    H -->|คัดลอกและแก้ Excel| X[ไฟล์เงินเดือน]
    X -->|ยอดและรายการหัก| H
    H -->|ข้อมูลเงินเดือน| I[ทีม IT]
    I -->|สลิปทางอีเมล| E[พนักงาน]
```

![การส่งต่อข้อมูลในกระบวนการเดิม](figures/concept-02.png)

## 3 บทบาทและกลุ่มงานในระบบใหม่

```mermaid
flowchart LR
    E[Employee] --> L[ส่งคำขอลาและ OT]
    E --> P[ดูสลิปตนเอง]
    S[Supervisor] --> A[บันทึกเวลาและพิจารณาคำขอในแผนก]
    M[Branch Manager] --> B[ดูแลข้อมูลและคำขอในสาขา]
    H[HR] --> C[จัดการพนักงานและการเงิน]
    H --> D[คำนวณและล็อกรอบ]
    H --> F[ออกสลิปและรายงาน]
    O[Owner] --> G[ตั้งค่าองค์กรและสิทธิ์]
    O --> D
    L --> D
    A --> D
    B --> D
    C --> D
    D --> F
```

![บทบาทและกลุ่มงานในระบบใหม่](figures/concept-03.png)

## 4 เส้นทางข้อมูลสำหรับคำนวณเงินเดือน

```mermaid
flowchart LR
    S[shops] --> P[payroll_periods]
    E[employees] --> A[employment_assignments]
    E --> W[work_day_records]
    E --> L[leave_requests / leave_request_days]
    E --> O[overtime_records]
    E --> F[advance_requests / loan_installments / debt_transactions]
    P --> R[payroll_records]
    A --> R
    W -. ใช้คำนวณ .-> R
    L -. ใช้คำนวณ .-> R
    O -. ใช้คำนวณ .-> R
    F -. ใช้คำนวณ .-> R
    R --> I[payroll_items]
    R --> SL[payslips]
    SL --> DL[email_delivery_logs]
```

![เส้นทางข้อมูลสำหรับคำนวณเงินเดือน](figures/concept-04.png)

## 5 Class Diagram ของข้อมูลหลัก

```mermaid
classDiagram
    class UserAccount {
      +bigint id
      +string username
      +account_status status
    }
    class AccountRole {
      +bigint user_account_id
      +bigint role_id
      +bigint branch_id
      +bigint department_id
    }
    class Employee {
      +bigint id
      +string employee_code
      +employee_status status
    }
    class EmploymentAssignment {
      +date effective_from
      +date effective_to
      +decimal base_salary
      +decimal welfare_amount
    }
    class WorkDayRecord {
      +date work_date
      +bigint branch_id
      +work_day_status status
    }
    class LeaveRequest {
      +date start_date
      +date end_date
      +leave_request_status status
    }
    class OvertimeRecord {
      +date overtime_date
      +overtime_status status
    }
    class PayrollPeriod {
      +int period_year
      +int period_month
      +payroll_period_status status
    }
    class PayrollRecord {
      +decimal base_salary_snapshot
      +decimal welfare_snapshot
      +decimal net_pay
    }
    class PayrollItem {
      +payroll_item_direction direction
      +decimal amount
    }
    class Payslip {
      +payslip_status status
    }
    UserAccount "1" -- "0..*" AccountRole : มีสิทธิ์
    UserAccount "0..1" -- "0..1" Employee : ผูกกับ
    Employee "1" -- "0..*" EmploymentAssignment : มีประวัติ
    Employee "1" -- "0..*" WorkDayRecord : ลงเวลา
    Employee "1" -- "0..*" LeaveRequest : ขอลา
    Employee "1" -- "0..*" OvertimeRecord : ขอ OT
    Employee "1" -- "0..*" PayrollRecord : รับเงินเดือน
    PayrollPeriod "1" -- "0..*" PayrollRecord : ประกอบด้วย
    PayrollRecord "1" -- "0..*" PayrollItem : แจกแจง
    PayrollRecord "1" -- "0..1" Payslip : ออกสลิป
```

![Class Diagram ของข้อมูลหลัก](figures/concept-05.png)

## 6 สถานะคำขอลาที่เปิดใช้จริง

```mermaid
stateDiagram-v2
    [*] --> pending: ยื่นคำขอลา
    pending --> approved: อนุมัติ
    pending --> rejected: ไม่อนุมัติ
    approved --> [*]
    rejected --> [*]
```

![สถานะคำขอลาที่เปิดใช้จริง](figures/concept-06.png)

## 7 สถานะรอบเงินเดือน

```mermaid
stateDiagram-v2
    [*] --> draft: เปิดรอบ
    draft --> previewed: คำนวณตัวอย่าง
    previewed --> previewed: คำนวณใหม่
    previewed --> locked: ตรวจครบและล็อก
    locked --> [*]
```

![สถานะรอบเงินเดือน](figures/concept-07.png)

## 8 สถานะสลิปเงินเดือน

```mermaid
stateDiagram-v2
    [*] --> generated: ออกจากรายการเงินเดือนที่ล็อกแล้ว
    generated --> generated: เพิ่มประวัติการส่งหนึ่งครั้ง
    generated --> voided: เพิกถอนตามสิทธิ์
    voided --> [*]
```

![สถานะสลิปเงินเดือน](figures/concept-08.png)

## 9 DFD ภาพรวมระบบ

```mermaid
flowchart LR
    E[พนักงาน] -->|ข้อมูลตน คำขอลา/OT| P((Haris Payroll))
    S[หัวหน้า/ผู้จัดการสาขา] -->|บันทึกเวลา ผลอนุมัติ| P
    H[HR/บัญชี] -->|ข้อมูลจ้าง รายการการเงิน คำสั่งคำนวณ| P
    O[เจ้าของร้าน] -->|ข้อมูลตั้งต้น นโยบาย การตรวจผล| P
    P -->|สถานะคำขอ สลิปตนเอง| E
    P -->|รายการในขอบเขตและผลอนุมัติ| S
    P -->|ผลเงินเดือนและ CSV| H
    P -->|ภาพรวมและประวัติการกระทำ| O
```

![DFD ภาพรวมระบบ](figures/concept-09.png)

## 10 DFD กระบวนการเงินเดือน

```mermaid
flowchart LR
    A[ผู้ใช้ที่ผ่านการยืนยันตัวตน] --> P1((1 จัดการองค์กรและพนักงาน))
    A --> P2((2 บันทึกงานและพิจารณาคำขอ))
    A --> P3((3 จัดการรายการการเงิน))
    A --> P4((4 คำนวณและล็อกรอบ))
    A --> P5((5 เตรียมจ่าย บันทึกผลและออกเอกสาร))
    P1 <--> D1[(D1 องค์กร บัญชี ประวัติการจ้างและเพิกถอน session)]
    P2 <--> D2[(D2 เวลา ลา และ OT)]
    P3 <--> D3[(D3 เงินทดรอง คำขอเงินกู้ สัญญาและหนี้)]
    D1 --> P4
    D2 --> P4
    D3 --> P4
    P4 <--> D4[(D4 รอบ ผลล็อก รายการย่อยและ payment snapshots)]
    D4 --> P5
    P5 -->|เตรียม ยืนยัน หรือยกเลิกจ่าย| D4
    P5 <--> D5[(D5 สลิปและประวัติการส่ง)]
    P1 --> D6[(D6 Audit)]
    P2 --> D6
    P3 --> D6
    P4 --> D6
    P5 --> D6
```

![DFD กระบวนการเงินเดือน](figures/concept-10.png)
