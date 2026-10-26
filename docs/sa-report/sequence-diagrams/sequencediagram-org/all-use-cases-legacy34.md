# โค้ด SequenceDiagram.org ทุก Use Case

คัดลอกเนื้อหาภายใน code block ทีละรายการไปใช้ ไม่คัดลอกทุก block รวมกัน

การตรวจสอบมี alt/else แสดงผลด้วย display() และส่งข้อผิดพลาดจาก Service ผ่าน Controller ด้วย error() ไม่มีลูกศรตอบกลับ Actor

## UC01 ตั้งค่าระบบจัดการเงินเดือน

```text
title UC01 ตั้งค่าระบบจัดการเงินเดือน
actor HR
participant PayrollPage
participant PayrollController
participant PayrollService
participant DatabaseInstance
HR->PayrollPage:เลือกค่ากำหนดเงินเดือนและกดบันทึก
PayrollPage->PayrollPage:ตรวจว่าร้าน ชนิดค่า จำนวนเงิน และวันที่ไม่ว่าง และจำนวนเงินเป็นตัวเลข
alt ข้อมูลไม่ถูกต้อง
  PayrollPage->PayrollPage:display("กรุณากรอกข้อมูลให้ครบและใช้รูปแบบที่ถูกต้อง")
else ข้อมูลถูกต้อง
  PayrollPage->PayrollController:ส่งคำขอสร้างค่ากำหนดเงินเดือน
  PayrollController->PayrollController:ตรวจชนิดข้อมูลและพารามิเตอร์คำขอ
  alt ชนิดข้อมูลหรือพารามิเตอร์คำขอไม่ถูกต้อง
    PayrollController->PayrollPage:display("ชนิดข้อมูลหรือพารามิเตอร์คำขอไม่ถูกต้อง")
  else ชนิดข้อมูลและพารามิเตอร์คำขอถูกต้อง
    PayrollController->PayrollService:createPayrollConfiguration(shopId, configKey, amount)
    PayrollService->PayrollService:ตรวจสิทธิ์ของผู้ดำเนินการตามขอบเขต
    alt ไม่มีสิทธิ์
      PayrollService->PayrollController:error("ไม่มีสิทธิ์ดำเนินการนี้")
      PayrollController->PayrollPage:display("ไม่มีสิทธิ์ดำเนินการนี้")
    else มีสิทธิ์
      PayrollService->DatabaseInstance:อ่านค่ากำหนดเดิม
      PayrollService->PayrollService:ตรวจช่วงวันที่มีผลไม่ทับซ้อนกัน
      alt ช่วงวันที่ทับซ้อน
        PayrollService->PayrollController:error("มีค่ากำหนดเงินเดือนครอบคลุมช่วงวันที่นี้แล้ว")
        PayrollController->PayrollPage:display("มีค่ากำหนดเงินเดือนครอบคลุมช่วงวันที่นี้แล้ว")
      else ช่วงวันที่ไม่ทับซ้อน
        PayrollService->DatabaseInstance:บันทึกค่ากำหนด
        PayrollService-->PayrollController:ส่งรายการตั้งค่าเงินเดือนที่บันทึก
        PayrollController->PayrollPage:display(รายการตั้งค่าเงินเดือนที่บันทึก)
      end
    end
  end
end
```

## UC02 ตั้งค่าประเภทการลา

```text
title UC02 ตั้งค่าประเภทการลา
actor HR
participant LeavePage
participant LeaveController
participant LeaveService
participant DatabaseInstance
note over LeavePage:ปัจจุบันดูประเภทการลาได้ แต่ยังไม่มี API เพิ่มหรือแก้ไขประเภทการลา
HR->LeavePage:เปิดดูรายการประเภทการลา
LeavePage->LeaveController:ขอรายการประเภทการลา
LeaveController->LeaveController:ตรวจชนิดข้อมูลและพารามิเตอร์คำขอ
alt ชนิดข้อมูลหรือพารามิเตอร์คำขอไม่ถูกต้อง
  LeaveController->LeavePage:display("ชนิดข้อมูลหรือพารามิเตอร์คำขอไม่ถูกต้อง")
else ชนิดข้อมูลและพารามิเตอร์คำขอถูกต้อง
  LeaveController->LeaveService:listTypes()
  LeaveService->LeaveService:ตรวจสิทธิ์ของผู้ขอดูข้อมูล
  alt ไม่มีสิทธิ์
    LeaveService->LeaveController:error("ไม่มีสิทธิ์ดำเนินการนี้")
    LeaveController->LeavePage:display("ไม่มีสิทธิ์ดำเนินการนี้")
  else มีสิทธิ์
    LeaveService->DatabaseInstance:อ่านประเภทการลา
    LeaveService->LeaveService:คัดเฉพาะประเภทการลาที่เปิดใช้งาน
    LeaveService-->LeaveController:ส่งรายการประเภทการลาปัจจุบัน
    LeaveController->LeavePage:display(รายการประเภทการลาปัจจุบัน)
  end
end
```

## UC03 ตั้งค่าประเภท OT

```text
title UC03 ตั้งค่าประเภท OT
actor Employee
participant OvertimePage
participant OvertimeController
participant OvertimeService
participant DatabaseInstance
note over OvertimePage:ประเภท OT เป็นค่าคงที่ hourly, rest_day, public_holiday; flow นี้แสดงการเลือกประเภทตอนยื่นคำขอ
Employee->OvertimePage:กรอกวัน ประเภท และชั่วโมง OT แล้วกดยื่น
OvertimePage->OvertimePage:ตรวจว่าวัน ประเภท และจำนวนชั่วโมงไม่ว่าง และจำนวนชั่วโมงเป็นตัวเลข
alt ข้อมูลไม่ถูกต้อง
  OvertimePage->OvertimePage:display("กรุณากรอกข้อมูลให้ครบและใช้รูปแบบที่ถูกต้อง")
else ข้อมูลถูกต้อง
  OvertimePage->OvertimeController:ส่งคำขอ OT ที่ระบุประเภท
  OvertimeController->OvertimeController:ตรวจชนิดข้อมูลและพารามิเตอร์คำขอ
  alt ชนิดข้อมูลหรือพารามิเตอร์คำขอไม่ถูกต้อง
    OvertimeController->OvertimePage:display("ชนิดข้อมูลหรือพารามิเตอร์คำขอไม่ถูกต้อง")
  else ชนิดข้อมูลและพารามิเตอร์คำขอถูกต้อง
    OvertimeController->OvertimeService:submitOvertime(employeeId, date, type, hours)
    OvertimeService->OvertimeService:ตรวจสิทธิ์ของผู้ดำเนินการตามขอบเขต
    alt ไม่มีสิทธิ์
      OvertimeService->OvertimeController:error("ไม่มีสิทธิ์ดำเนินการนี้")
      OvertimeController->OvertimePage:display("ไม่มีสิทธิ์ดำเนินการนี้")
    else มีสิทธิ์
      OvertimeService->DatabaseInstance:อ่านข้อมูลพนักงาน
      OvertimeService->OvertimeService:ตรวจประเภท OT และคำขอที่ซ้ำหรือขัดกัน
      alt ประเภทหรือจำนวน OT ไม่ถูกต้อง หรือคำขอซ้ำ
        OvertimeService->OvertimeController:error("ประเภท จำนวน หรือวันที่ OT ไม่ถูกต้อง หรือมีคำขอซ้ำ")
        OvertimeController->OvertimePage:display("ประเภท จำนวน หรือวันที่ OT ไม่ถูกต้อง หรือมีคำขอซ้ำ")
      else ประเภทและจำนวน OT ถูกต้อง และไม่ซ้ำ
        OvertimeService->DatabaseInstance:บันทึกคำขอ OT
        OvertimeService-->OvertimeController:ส่งคำขอ OT สถานะรออนุมัติ
        OvertimeController->OvertimePage:display(คำขอ OT สถานะรออนุมัติ)
      end
    end
  end
end
```

## UC04 สร้างรอบเงินเดือน

```text
title UC04 สร้างรอบเงินเดือน
actor HR
participant PayrollPage
participant PayrollController
participant PayrollService
participant DatabaseInstance
HR->PayrollPage:เลือกร้านและช่วงวันเพื่อสร้างรอบเงินเดือน
PayrollPage->PayrollPage:ตรวจว่าร้าน เดือน ปี และวันเริ่มกับวันสิ้นสุดไม่ว่างและมีรูปแบบถูกต้อง
alt ข้อมูลไม่ถูกต้อง
  PayrollPage->PayrollPage:display("กรุณากรอกข้อมูลให้ครบและใช้รูปแบบที่ถูกต้อง")
else ข้อมูลถูกต้อง
  PayrollPage->PayrollController:ส่งคำขอสร้างรอบเงินเดือน
  PayrollController->PayrollController:ตรวจชนิดข้อมูลและพารามิเตอร์คำขอ
  alt ชนิดข้อมูลหรือพารามิเตอร์คำขอไม่ถูกต้อง
    PayrollController->PayrollPage:display("ชนิดข้อมูลหรือพารามิเตอร์คำขอไม่ถูกต้อง")
  else ชนิดข้อมูลและพารามิเตอร์คำขอถูกต้อง
    PayrollController->PayrollService:createPayrollPeriod(shopId, startDate, endDate)
    PayrollService->PayrollService:ตรวจสิทธิ์ของผู้ดำเนินการตามขอบเขต
    alt ไม่มีสิทธิ์
      PayrollService->PayrollController:error("ไม่มีสิทธิ์ดำเนินการนี้")
      PayrollController->PayrollPage:display("ไม่มีสิทธิ์ดำเนินการนี้")
    else มีสิทธิ์
      PayrollService->DatabaseInstance:อ่านร้านและรอบเดิม
      PayrollService->PayrollService:ตรวจร้าน ช่วงวัน และรอบที่ซ้ำ
      alt ร้านหรือช่วงวันไม่ถูกต้อง
        PayrollService->PayrollController:error("ร้านหรือช่วงวันที่สร้างรอบเงินเดือนไม่ถูกต้อง")
        PayrollController->PayrollPage:display("ร้านหรือช่วงวันที่สร้างรอบเงินเดือนไม่ถูกต้อง")
      else ร้านและช่วงวันถูกต้อง
        alt มีรอบซ้ำหรือช่วงวันที่ทับซ้อน
          PayrollService->PayrollController:error("ไม่สามารถสร้างได้ เนื่องจากมีรอบซ้ำหรือช่วงวันที่ทับซ้อนกับรอบเงินเดือนอื่น")
          PayrollController->PayrollPage:display("ไม่สามารถสร้างได้ เนื่องจากมีรอบซ้ำหรือช่วงวันที่ทับซ้อนกับรอบเงินเดือนอื่น")
        else ไม่มีรอบซ้ำหรือช่วงวันที่ทับซ้อน
          PayrollService->DatabaseInstance:สร้างรอบเงินเดือน
          PayrollService-->PayrollController:ส่งรอบเงินเดือนสถานะฉบับร่าง
          PayrollController->PayrollPage:display(รอบเงินเดือนสถานะฉบับร่าง)
        end
      end
    end
  end
end
```

## UC05 เพิ่มพนักงานเข้ารอบเงินเดือน

```text
title UC05 เพิ่มพนักงานเข้ารอบเงินเดือน
actor HR
participant PayrollPage
participant PayrollController
participant PayrollService
participant DatabaseInstance
note over PayrollPage:ระบบเพิ่มพนักงานเข้ารอบโดยคัดประวัติการจ้างอัตโนมัติระหว่าง preview
HR->PayrollPage:เลือกรอบแล้วกดคำนวณตัวอย่างเงินเดือน
PayrollPage->PayrollPage:ตรวจว่าเลือกรอบแล้วและรหัสรอบเป็นตัวเลข
alt ข้อมูลไม่ถูกต้อง
  PayrollPage->PayrollPage:display("กรุณากรอกข้อมูลให้ครบและใช้รูปแบบที่ถูกต้อง")
else ข้อมูลถูกต้อง
  PayrollPage->PayrollController:ส่งคำขอคำนวณตัวอย่างเงินเดือน
  PayrollController->PayrollController:ตรวจชนิดข้อมูลและพารามิเตอร์คำขอ
  alt ชนิดข้อมูลหรือพารามิเตอร์คำขอไม่ถูกต้อง
    PayrollController->PayrollPage:display("ชนิดข้อมูลหรือพารามิเตอร์คำขอไม่ถูกต้อง")
  else ชนิดข้อมูลและพารามิเตอร์คำขอถูกต้อง
    PayrollController->PayrollService:previewPayrollPeriod(periodId)
    PayrollService->PayrollService:ตรวจสิทธิ์ของผู้ดำเนินการตามขอบเขต
    alt ไม่มีสิทธิ์
      PayrollService->PayrollController:error("ไม่มีสิทธิ์ดำเนินการนี้")
      PayrollController->PayrollPage:display("ไม่มีสิทธิ์ดำเนินการนี้")
    else มีสิทธิ์
      PayrollService->DatabaseInstance:อ่านรอบเงินเดือนและสถานะ
      PayrollService->PayrollService:ตรวจสถานะรอบก่อนคำนวณ
      alt สถานะรอบไม่อนุญาตให้คำนวณ
        PayrollService->PayrollController:error("ไม่สามารถคำนวณรอบเงินเดือนในสถานะนี้ได้")
        PayrollController->PayrollPage:display("ไม่สามารถคำนวณรอบเงินเดือนในสถานะนี้ได้")
      else สถานะรอบอนุญาตให้คำนวณ
        PayrollService->DatabaseInstance:อ่านประวัติการจ้างตามช่วงวันที่
        PayrollService->DatabaseInstance:อ่านวันทำงาน คำขอ และค่ากำหนด
        PayrollService->PayrollService:คัดพนักงานและคำนวณผลรายคน
        PayrollService->PayrollService:รวบรวม blocker เมื่อข้อมูลไม่ครบหรือยอดผิดปกติ
        alt พบ blocker
          PayrollService->PayrollController:error("ไม่สามารถคำนวณตัวอย่างได้ กรุณาแก้ข้อมูลที่ขาดหรือยอดผิดปกติ")
          PayrollController->PayrollPage:display("ไม่สามารถคำนวณตัวอย่างได้ กรุณาแก้ข้อมูลที่ขาดหรือยอดผิดปกติ")
        else ไม่พบ blocker
          PayrollService->DatabaseInstance:บันทึกผลเงินเดือนและสถานะ previewed
          PayrollService-->PayrollController:ส่งรายชื่อพนักงานและผลคำนวณตัวอย่าง
          PayrollController->PayrollPage:display(รายชื่อพนักงานและผลคำนวณตัวอย่าง)
        end
      end
    end
  end
end
```

## UC06 คำนวณ OT

```text
title UC06 คำนวณ OT
actor HR
participant PayrollPage
participant PayrollController
participant PayrollService
participant DatabaseInstance
HR->PayrollPage:เลือกรอบเพื่อคำนวณค่า OT ในเงินเดือน
PayrollPage->PayrollPage:ตรวจว่ามีรอบที่เลือกและรหัสรอบเป็นสตริงตัวเลขที่ไม่ว่าง
alt ข้อมูลไม่ถูกต้อง
  PayrollPage->PayrollPage:display("กรุณากรอกข้อมูลให้ครบและใช้รูปแบบที่ถูกต้อง")
else ข้อมูลถูกต้อง
  PayrollPage->PayrollController:ส่งคำขอคำนวณตัวอย่างเงินเดือน
  PayrollController->PayrollController:ตรวจชนิดข้อมูลและพารามิเตอร์คำขอ
  alt ชนิดข้อมูลหรือพารามิเตอร์คำขอไม่ถูกต้อง
    PayrollController->PayrollPage:display("ชนิดข้อมูลหรือพารามิเตอร์คำขอไม่ถูกต้อง")
  else ชนิดข้อมูลและพารามิเตอร์คำขอถูกต้อง
    PayrollController->PayrollService:previewPayrollPeriod(periodId)
    PayrollService->PayrollService:ตรวจสิทธิ์ของผู้ดำเนินการตามขอบเขต
    alt ไม่มีสิทธิ์
      PayrollService->PayrollController:error("ไม่มีสิทธิ์ดำเนินการนี้")
      PayrollController->PayrollPage:display("ไม่มีสิทธิ์ดำเนินการนี้")
    else มีสิทธิ์
      PayrollService->DatabaseInstance:อ่าน OT ที่อนุมัติ
      PayrollService->PayrollService:คำนวณเฉพาะ OT ที่อนุมัติแล้วตามอัตราที่มีผล
      PayrollService->DatabaseInstance:บันทึกผล preview
      PayrollService-->PayrollController:ส่งยอด OT ในตัวอย่างเงินเดือน
      PayrollController->PayrollPage:display(ยอด OT ในตัวอย่างเงินเดือน)
    end
  end
end
```

## UC07 ปิดรอบเงินเดือน

```text
title UC07 ปิดรอบเงินเดือน
actor HR
participant PayrollPage
participant PayrollController
participant PayrollService
participant DatabaseInstance
HR->PayrollPage:เลือกรอบที่ตรวจแล้วและกดล็อกรอบ
PayrollPage->PayrollPage:ตรวจว่ามีรอบที่เลือกและรหัสรอบเป็นสตริงตัวเลขที่ไม่ว่าง
alt ข้อมูลไม่ถูกต้อง
  PayrollPage->PayrollPage:display("กรุณากรอกข้อมูลให้ครบและใช้รูปแบบที่ถูกต้อง")
else ข้อมูลถูกต้อง
  PayrollPage->PayrollController:ส่งคำขอล็อกรอบเงินเดือน
  PayrollController->PayrollController:ตรวจชนิดข้อมูลและพารามิเตอร์คำขอ
  alt ชนิดข้อมูลหรือพารามิเตอร์คำขอไม่ถูกต้อง
    PayrollController->PayrollPage:display("ชนิดข้อมูลหรือพารามิเตอร์คำขอไม่ถูกต้อง")
  else ชนิดข้อมูลและพารามิเตอร์คำขอถูกต้อง
    PayrollController->PayrollService:lockPayrollPeriod(periodId)
    PayrollService->PayrollService:ตรวจสิทธิ์ของผู้ดำเนินการตามขอบเขต
    alt ไม่มีสิทธิ์
      PayrollService->PayrollController:error("ไม่มีสิทธิ์ดำเนินการนี้")
      PayrollController->PayrollPage:display("ไม่มีสิทธิ์ดำเนินการนี้")
    else มีสิทธิ์
      PayrollService->DatabaseInstance:อ่านข้อมูลก่อนล็อก
      PayrollService->PayrollService:ตรวจวันทำงาน คำขอค้าง ยอดสุทธิ และผลรวม
      alt วันทำงานไม่ครบ
        PayrollService->PayrollController:error("ไม่สามารถล็อกรอบได้ เนื่องจากวันทำงานไม่ครบ")
        PayrollController->PayrollPage:display("ไม่สามารถล็อกรอบได้ เนื่องจากวันทำงานไม่ครบ")
      else วันทำงานครบ
        alt มีคำขอรออนุมัติ
          PayrollService->PayrollController:error("ไม่สามารถล็อกรอบได้ เนื่องจากมีคำขอรออนุมัติ")
          PayrollController->PayrollPage:display("ไม่สามารถล็อกรอบได้ เนื่องจากมีคำขอรออนุมัติ")
        else ไม่มีคำขอรออนุมัติ
          alt ยอดสุทธิติดลบหรือผลรวมไม่ถูกต้อง
            PayrollService->PayrollController:error("ไม่สามารถล็อกรอบได้ เนื่องจากยอดสุทธิหรือผลรวมไม่ถูกต้อง")
            PayrollController->PayrollPage:display("ไม่สามารถล็อกรอบได้ เนื่องจากยอดสุทธิหรือผลรวมไม่ถูกต้อง")
          else ยอดสุทธิไม่ติดลบและผลรวมถูกต้อง
            PayrollService->DatabaseInstance:ล็อกรอบและบันทึกค่า
            PayrollService-->PayrollController:ส่งรอบที่ล็อกพร้อมข้อมูลตรวจสอบย้อนหลัง
            PayrollController->PayrollPage:display(รอบที่ล็อกพร้อมข้อมูลตรวจสอบย้อนหลัง)
          end
        end
      end
    end
  end
end
```

## UC08 จ่ายเงินเดือนแบ่งเป็นประเภท

```text
title UC08 จ่ายเงินเดือนแบ่งเป็นประเภท
actor HR
participant ReportsPage
participant ReportRoutes
participant ReportService
participant DatabaseInstance
note over ReportsPage:ระบบส่งออก CSV เท่านั้น การจ่ายและยืนยันผลเกิดภายนอกระบบ
HR->ReportsPage:เลือกรอบและขอไฟล์รายการโอนเงิน
ReportsPage->ReportsPage:ตรวจว่ามีรอบที่เลือกและรหัสรอบเป็นสตริงตัวเลขที่ไม่ว่าง
alt ข้อมูลไม่ถูกต้อง
  ReportsPage->ReportsPage:display("กรุณากรอกข้อมูลให้ครบและใช้รูปแบบที่ถูกต้อง")
else ข้อมูลถูกต้อง
  ReportsPage->ReportRoutes:ขอไฟล์ CSV รายการโอนเงิน
  ReportRoutes->ReportRoutes:ตรวจชนิดข้อมูลและพารามิเตอร์คำขอ
  alt ชนิดข้อมูลหรือพารามิเตอร์คำขอไม่ถูกต้อง
    ReportRoutes->ReportsPage:display("ชนิดข้อมูลหรือพารามิเตอร์คำขอไม่ถูกต้อง")
  else ชนิดข้อมูลและพารามิเตอร์คำขอถูกต้อง
    ReportRoutes->ReportService:bankTransfer(periodId)
    ReportService->ReportService:ตรวจสิทธิ์ของผู้ดำเนินการตามขอบเขต
    alt ไม่มีสิทธิ์
      ReportService->ReportRoutes:error("ไม่มีสิทธิ์ดำเนินการนี้")
      ReportRoutes->ReportsPage:display("ไม่มีสิทธิ์ดำเนินการนี้")
    else มีสิทธิ์
      ReportService->DatabaseInstance:อ่านผลเงินเดือน
      ReportService->ReportService:จัดยอดและบัญชีตามผลเงินเดือนที่ล็อก
      ReportService-->ReportRoutes:ส่งไฟล์ CSV สำหรับนำเข้าธนาคาร
      ReportRoutes->ReportsPage:display(ไฟล์ CSV สำหรับนำเข้าธนาคาร)
    end
  end
end
```

## UC09 จ่ายเงินเดือนแบบเงินสด

```text
title UC09 จ่ายเงินเดือนแบบเงินสด
actor HR
participant PayrollPage
participant PayrollController
participant PayrollService
participant DatabaseInstance
note over PayrollPage:ระบบแสดงข้อมูลรอบเงินเดือน ยังไม่มี API บันทึกการจ่ายเงินสด
HR->PayrollPage:เลือกรอบเพื่อดูยอดจ่ายเงินสด
PayrollPage->PayrollPage:ตรวจว่ามีรอบที่เลือกและรหัสรอบเป็นสตริงตัวเลขที่ไม่ว่าง
alt ข้อมูลไม่ถูกต้อง
  PayrollPage->PayrollPage:display("กรุณากรอกข้อมูลให้ครบและใช้รูปแบบที่ถูกต้อง")
else ข้อมูลถูกต้อง
  PayrollPage->PayrollController:ขอรายละเอียดผลเงินเดือนของรอบ
  PayrollController->PayrollController:ตรวจชนิดข้อมูลและพารามิเตอร์คำขอ
  alt ชนิดข้อมูลหรือพารามิเตอร์คำขอไม่ถูกต้อง
    PayrollController->PayrollPage:display("ชนิดข้อมูลหรือพารามิเตอร์คำขอไม่ถูกต้อง")
  else ชนิดข้อมูลและพารามิเตอร์คำขอถูกต้อง
    PayrollController->PayrollService:getPayrollPeriod(periodId)
    PayrollService->PayrollService:ตรวจสิทธิ์ของผู้ดำเนินการตามขอบเขต
    alt ไม่มีสิทธิ์
      PayrollService->PayrollController:error("ไม่มีสิทธิ์ดำเนินการนี้")
      PayrollController->PayrollPage:display("ไม่มีสิทธิ์ดำเนินการนี้")
    else มีสิทธิ์
      PayrollService->DatabaseInstance:อ่านยอดเงินเดือน
      PayrollService->PayrollService:แสดงยอดสุทธิสำหรับนำไปจ่ายภายนอกระบบ
      PayrollService-->PayrollController:ส่งยอดเงินสดที่ต้องจ่าย
      PayrollController->PayrollPage:display(ยอดเงินสดที่ต้องจ่าย)
    end
  end
end
```

## UC10 ประกันสังคม

```text
title UC10 ประกันสังคม
actor HR
participant ReportsPage
participant ReportRoutes
participant ReportService
participant DatabaseInstance
note over ReportsPage:รองรับ CSV ประกันสังคม ยังไม่มีการนำส่งหรือยืนยันชำระในระบบ
HR->ReportsPage:เลือกรอบเพื่อจัดข้อมูลประกันสังคม
ReportsPage->ReportsPage:ตรวจว่ามีรอบที่เลือกและรหัสรอบเป็นสตริงตัวเลขที่ไม่ว่าง
alt ข้อมูลไม่ถูกต้อง
  ReportsPage->ReportsPage:display("กรุณากรอกข้อมูลให้ครบและใช้รูปแบบที่ถูกต้อง")
else ข้อมูลถูกต้อง
  ReportsPage->ReportRoutes:ขอไฟล์ CSV ประกันสังคม
  ReportRoutes->ReportRoutes:ตรวจชนิดข้อมูลและพารามิเตอร์คำขอ
  alt ชนิดข้อมูลหรือพารามิเตอร์คำขอไม่ถูกต้อง
    ReportRoutes->ReportsPage:display("ชนิดข้อมูลหรือพารามิเตอร์คำขอไม่ถูกต้อง")
  else ชนิดข้อมูลและพารามิเตอร์คำขอถูกต้อง
    ReportRoutes->ReportService:socialSecurity(periodId)
    ReportService->ReportService:ตรวจสิทธิ์ของผู้ดำเนินการตามขอบเขต
    alt ไม่มีสิทธิ์
      ReportService->ReportRoutes:error("ไม่มีสิทธิ์ดำเนินการนี้")
      ReportRoutes->ReportsPage:display("ไม่มีสิทธิ์ดำเนินการนี้")
    else มีสิทธิ์
      ReportService->DatabaseInstance:อ่านเงินเดือนฐาน
      ReportService->ReportService:คำนวณจากเงินเดือนฐานโดยไม่รวมสวัสดิการ
      ReportService-->ReportRoutes:ส่งไฟล์ CSV ประกันสังคม
      ReportRoutes->ReportsPage:display(ไฟล์ CSV ประกันสังคม)
    end
  end
end
```

## UC11 จ่ายเงินเดือนแบบโอน

```text
title UC11 จ่ายเงินเดือนแบบโอน
actor HR
participant ReportsPage
participant ReportRoutes
participant ReportService
participant DatabaseInstance
note over ReportsPage:การ export CSV ไม่ได้หมายถึงโอนเงินสำเร็จ
HR->ReportsPage:เลือกรอบเพื่อส่งออกไฟล์โอนเงิน
ReportsPage->ReportsPage:ตรวจว่ามีรอบที่เลือกและรหัสรอบเป็นสตริงตัวเลขที่ไม่ว่าง
alt ข้อมูลไม่ถูกต้อง
  ReportsPage->ReportsPage:display("กรุณากรอกข้อมูลให้ครบและใช้รูปแบบที่ถูกต้อง")
else ข้อมูลถูกต้อง
  ReportsPage->ReportRoutes:ขอไฟล์ CSV สำหรับธนาคาร
  ReportRoutes->ReportRoutes:ตรวจชนิดข้อมูลและพารามิเตอร์คำขอ
  alt ชนิดข้อมูลหรือพารามิเตอร์คำขอไม่ถูกต้อง
    ReportRoutes->ReportsPage:display("ชนิดข้อมูลหรือพารามิเตอร์คำขอไม่ถูกต้อง")
  else ชนิดข้อมูลและพารามิเตอร์คำขอถูกต้อง
    ReportRoutes->ReportService:bankTransfer(periodId)
    ReportService->ReportService:ตรวจสิทธิ์ของผู้ดำเนินการตามขอบเขต
    alt ไม่มีสิทธิ์
      ReportService->ReportRoutes:error("ไม่มีสิทธิ์ดำเนินการนี้")
      ReportRoutes->ReportsPage:display("ไม่มีสิทธิ์ดำเนินการนี้")
    else มีสิทธิ์
      ReportService->DatabaseInstance:อ่านยอดและบัญชี
      ReportService->ReportService:จัดยอดสุทธิและบัญชีของผลที่ล็อก
      ReportService-->ReportRoutes:ส่งไฟล์ CSV สำหรับธนาคาร
      ReportRoutes->ReportsPage:display(ไฟล์ CSV สำหรับธนาคาร)
    end
  end
end
```

## UC12 คำนวณการลาและมาสาย

```text
title UC12 คำนวณการลาและมาสาย
actor HR
participant PayrollPage
participant PayrollController
participant PayrollService
participant DatabaseInstance
HR->PayrollPage:เลือกรอบเพื่อคำนวณวันลาและมาสาย
PayrollPage->PayrollPage:ตรวจว่ามีรอบที่เลือกและรหัสรอบเป็นสตริงตัวเลขที่ไม่ว่าง
alt ข้อมูลไม่ถูกต้อง
  PayrollPage->PayrollPage:display("กรุณากรอกข้อมูลให้ครบและใช้รูปแบบที่ถูกต้อง")
else ข้อมูลถูกต้อง
  PayrollPage->PayrollController:ส่งคำขอคำนวณตัวอย่างเงินเดือน
  PayrollController->PayrollController:ตรวจชนิดข้อมูลและพารามิเตอร์คำขอ
  alt ชนิดข้อมูลหรือพารามิเตอร์คำขอไม่ถูกต้อง
    PayrollController->PayrollPage:display("ชนิดข้อมูลหรือพารามิเตอร์คำขอไม่ถูกต้อง")
  else ชนิดข้อมูลและพารามิเตอร์คำขอถูกต้อง
    PayrollController->PayrollService:previewPayrollPeriod(periodId)
    PayrollService->PayrollService:ตรวจสิทธิ์ของผู้ดำเนินการตามขอบเขต
    alt ไม่มีสิทธิ์
      PayrollService->PayrollController:error("ไม่มีสิทธิ์ดำเนินการนี้")
      PayrollController->PayrollPage:display("ไม่มีสิทธิ์ดำเนินการนี้")
    else มีสิทธิ์
      PayrollService->DatabaseInstance:อ่านเวลาและวันลา
      PayrollService->PayrollService:แยกวันขาดหรือสายที่หักเงินกับวันลาที่ไม่หัก
      PayrollService->DatabaseInstance:บันทึกผล preview
      PayrollService-->PayrollController:ส่งยอดหักและรายการไม่หักแยกกัน
      PayrollController->PayrollPage:display(ยอดหักและรายการไม่หักแยกกัน)
    end
  end
end
```

## UC13 แก้ไขประเภท OT

```text
title UC13 แก้ไขประเภท OT
actor HR
participant OvertimePage
participant OvertimeController
participant OvertimeService
participant DatabaseInstance
note over OvertimePage:ไม่มี API แก้ประเภท OT เดิม; แสดงทางเลือกปฏิเสธคำขอที่ผิดตามสิทธิ์
HR->OvertimePage:เปิดคำขอ OT ที่ระบุประเภทผิด
OvertimePage->OvertimePage:ตรวจรหัสคำขอ
alt ข้อมูลไม่ถูกต้อง
  OvertimePage->OvertimePage:display("กรุณากรอกข้อมูลให้ครบและใช้รูปแบบที่ถูกต้อง")
else ข้อมูลถูกต้อง
  OvertimePage->OvertimeController:ขอรายการคำขอ OT เพื่อตรวจประเภท
  OvertimeController->OvertimeService:listRequests(employeeId)
  OvertimeService->OvertimeService:ตรวจสิทธิ์ของผู้ดำเนินการตามขอบเขต
  alt ไม่มีสิทธิ์
    OvertimeService->OvertimeController:error("ไม่มีสิทธิ์ดำเนินการนี้")
    OvertimeController->OvertimePage:display("ไม่มีสิทธิ์ดำเนินการนี้")
  else มีสิทธิ์
    OvertimeService->DatabaseInstance:อ่านคำขอและสถานะ
    OvertimeService-->OvertimeController:ส่งรายการคำขอ OT และสถานะ
    OvertimeController->OvertimePage:display(รายการคำขอ OT ให้ตรวจสอบ)
    HR->OvertimePage:เลือกปฏิเสธคำขอที่ผิดประเภท
    OvertimePage->OvertimeController:ส่งคำขอปฏิเสธ OT ที่ผิดประเภท
    OvertimeController->OvertimeService:rejectOvertime(requestId)
    OvertimeService->OvertimeService:ตรวจสิทธิ์ของผู้ดำเนินการตามขอบเขต
    alt ไม่มีสิทธิ์
      OvertimeService->OvertimeController:error("ไม่มีสิทธิ์ดำเนินการนี้")
      OvertimeController->OvertimePage:display("ไม่มีสิทธิ์ดำเนินการนี้")
    else มีสิทธิ์
      OvertimeService->OvertimeService:ตรวจสิทธิ์และสถานะก่อนปฏิเสธ
      alt คำขอไม่ได้อยู่ในสถานะรอพิจารณา
        OvertimeService->OvertimeController:error("ไม่สามารถปฏิเสธคำขอที่พิจารณาแล้ว")
        OvertimeController->OvertimePage:display("ไม่สามารถปฏิเสธคำขอที่พิจารณาแล้ว")
      else คำขออยู่ในสถานะรอพิจารณา
        OvertimeService->DatabaseInstance:บันทึกผลปฏิเสธและประวัติการพิจารณา
        OvertimeService-->OvertimeController:ส่งผลปฏิเสธพร้อมประวัติการพิจารณา
        OvertimeController->OvertimePage:display(ผลปฏิเสธ)
      end
    end
  end
end
```

## UC14 อนุมัติ OT

```text
title UC14 อนุมัติ OT
actor Manager
participant OvertimePage
participant OvertimeController
participant OvertimeService
participant DatabaseInstance
Manager->OvertimePage:เลือกคำขอ OT แล้วกดอนุมัติ
OvertimePage->OvertimePage:ตรวจว่ามีคำขอที่เลือกและรหัสคำขอเป็นสตริงตัวเลขที่ไม่ว่าง
alt ข้อมูลไม่ถูกต้อง
  OvertimePage->OvertimePage:display("กรุณากรอกข้อมูลให้ครบและใช้รูปแบบที่ถูกต้อง")
else ข้อมูลถูกต้อง
  OvertimePage->OvertimeController:ส่งคำขออนุมัติ OT
  OvertimeController->OvertimeController:ตรวจชนิดข้อมูลและพารามิเตอร์คำขอ
  alt ชนิดข้อมูลหรือพารามิเตอร์คำขอไม่ถูกต้อง
    OvertimeController->OvertimePage:display("ชนิดข้อมูลหรือพารามิเตอร์คำขอไม่ถูกต้อง")
  else ชนิดข้อมูลและพารามิเตอร์คำขอถูกต้อง
    OvertimeController->OvertimeService:approveOvertime(requestId)
    OvertimeService->OvertimeService:ตรวจสิทธิ์ของผู้ดำเนินการตามขอบเขต
    alt ไม่มีสิทธิ์
      OvertimeService->OvertimeController:error("ไม่มีสิทธิ์ดำเนินการนี้")
      OvertimeController->OvertimePage:display("ไม่มีสิทธิ์ดำเนินการนี้")
    else มีสิทธิ์
      OvertimeService->DatabaseInstance:อ่านคำขอ OT
      OvertimeService->OvertimeService:ตรวจสิทธิ์ตามสาขาหรือแผนกและสถานะคำขอ
      alt คำขอไม่ได้อยู่ในสถานะรอพิจารณาหรือเงื่อนไข OT ไม่ครบ
        OvertimeService->OvertimeController:error("ไม่สามารถอนุมัติ OT ได้ เนื่องจากสถานะหรือเงื่อนไข OT ไม่ถูกต้อง")
        OvertimeController->OvertimePage:display("ไม่สามารถอนุมัติ OT ได้ เนื่องจากสถานะหรือเงื่อนไข OT ไม่ถูกต้อง")
      else คำขอรอพิจารณาและเงื่อนไข OT ครบ
        OvertimeService->DatabaseInstance:บันทึกผลอนุมัติ
        OvertimeService-->OvertimeController:ส่งผลอนุมัติ OT พร้อมประวัติ
        OvertimeController->OvertimePage:display(ผลอนุมัติ OT พร้อมประวัติ)
      end
    end
  end
end
```

## UC15 กรอกข้อมูลรายรับและรายจ่ายของพนักงาน

```text
title UC15 กรอกข้อมูลรายรับและรายจ่ายของพนักงาน
actor HR
participant FinancePage
participant DebtController
participant DebtService
participant DatabaseInstance
note over FinancePage:flow นี้บันทึกหนี้; เงินกู้และเงินทดรองอยู่ UC26 ยังไม่มีรายรับทั่วไปแบบอิสระ
HR->FinancePage:กรอกธุรกรรมหนี้ของพนักงานแล้วบันทึก
FinancePage->FinancePage:ตรวจว่าพนักงาน ชนิดรายการ จำนวนเงิน และเหตุผลไม่ว่าง และจำนวนเงินเป็นตัวเลข
alt ข้อมูลไม่ถูกต้อง
  FinancePage->FinancePage:display("กรุณากรอกข้อมูลให้ครบและใช้รูปแบบที่ถูกต้อง")
else ข้อมูลถูกต้อง
  FinancePage->DebtController:ส่งคำขอบันทึกธุรกรรมหนี้
  DebtController->DebtController:ตรวจชนิดข้อมูลและพารามิเตอร์คำขอ
  alt ชนิดข้อมูลหรือพารามิเตอร์คำขอไม่ถูกต้อง
    DebtController->FinancePage:display("ชนิดข้อมูลหรือพารามิเตอร์คำขอไม่ถูกต้อง")
  else ชนิดข้อมูลและพารามิเตอร์คำขอถูกต้อง
    DebtController->DebtService:record(employeeId, type, amount)
    DebtService->DebtService:ตรวจสิทธิ์ของผู้ดำเนินการตามขอบเขต
    alt ไม่มีสิทธิ์
      DebtService->DebtController:error("ไม่มีสิทธิ์ดำเนินการนี้")
      DebtController->FinancePage:display("ไม่มีสิทธิ์ดำเนินการนี้")
    else มีสิทธิ์
      DebtService->DatabaseInstance:อ่านข้อมูลพนักงาน
      DebtService->DebtService:ตรวจชนิดธุรกรรมและจำนวนเงิน
      alt ชนิดธุรกรรมหรือจำนวนเงินไม่ถูกต้อง
        DebtService->DebtController:error("ชนิดธุรกรรมหรือจำนวนเงินไม่ถูกต้อง")
        DebtController->FinancePage:display("ชนิดธุรกรรมหรือจำนวนเงินไม่ถูกต้อง")
      else ชนิดธุรกรรมและจำนวนเงินถูกต้อง
        DebtService->DatabaseInstance:บันทึกธุรกรรมหนี้
        DebtService-->DebtController:ส่งธุรกรรมหนี้ใหม่และประวัติ
        DebtController->FinancePage:display(ธุรกรรมหนี้ใหม่และประวัติ)
      end
    end
  end
end
```

## UC16 จ่ายเงินให้พนักงาน

```text
title UC16 จ่ายเงินให้พนักงาน
actor HR
participant PayrollPage
participant PayrollController
participant PayrollService
participant DatabaseInstance
note over PayrollPage:การจ่ายเงินจริงเป็นขั้นตอนภายนอก ยังไม่มีการบันทึกยืนยันจ่ายในระบบ
HR->PayrollPage:เลือกรอบเพื่อดูยอดจ่ายพนักงาน
PayrollPage->PayrollPage:ตรวจว่ามีรอบที่เลือกและรหัสรอบเป็นสตริงตัวเลขที่ไม่ว่าง
alt ข้อมูลไม่ถูกต้อง
  PayrollPage->PayrollPage:display("กรุณากรอกข้อมูลให้ครบและใช้รูปแบบที่ถูกต้อง")
else ข้อมูลถูกต้อง
  PayrollPage->PayrollController:ขอรายละเอียดผลเงินเดือนของรอบ
  PayrollController->PayrollController:ตรวจชนิดข้อมูลและพารามิเตอร์คำขอ
  alt ชนิดข้อมูลหรือพารามิเตอร์คำขอไม่ถูกต้อง
    PayrollController->PayrollPage:display("ชนิดข้อมูลหรือพารามิเตอร์คำขอไม่ถูกต้อง")
  else ชนิดข้อมูลและพารามิเตอร์คำขอถูกต้อง
    PayrollController->PayrollService:getPayrollPeriod(periodId)
    PayrollService->PayrollService:ตรวจสิทธิ์ของผู้ดำเนินการตามขอบเขต
    alt ไม่มีสิทธิ์
      PayrollService->PayrollController:error("ไม่มีสิทธิ์ดำเนินการนี้")
      PayrollController->PayrollPage:display("ไม่มีสิทธิ์ดำเนินการนี้")
    else มีสิทธิ์
      PayrollService->DatabaseInstance:อ่านผลเงินเดือน
      PayrollService->PayrollService:แสดงยอดที่ล็อกไว้เพื่อจ่ายภายนอกระบบ
      PayrollService-->PayrollController:ส่งยอดเงินเดือนที่ต้องจ่าย
      PayrollController->PayrollPage:display(ยอดเงินเดือนที่ต้องจ่าย)
    end
  end
end
```

## UC17 ส่งสลิปหรือใบแจ้งหนี้รายบุคคล

```text
title UC17 ส่งสลิปหรือใบแจ้งหนี้รายบุคคล
actor HR
participant PayslipsPage
participant PayslipController
participant PayslipService
participant DatabaseInstance
note over PayslipsPage:สร้างข้อมูลสลิปและ mock delivery log ยังไม่มี PDF อีเมลจริง หรือใบแจ้งหนี้
HR->PayslipsPage:เลือกผลเงินเดือนเพื่อสร้างข้อมูลสลิป
PayslipsPage->PayslipsPage:ตรวจรหัสผลเงินเดือน
alt ข้อมูลไม่ถูกต้อง
  PayslipsPage->PayslipsPage:display("กรุณากรอกข้อมูลให้ครบและใช้รูปแบบที่ถูกต้อง")
else ข้อมูลถูกต้อง
  PayslipsPage->PayslipController:ส่งคำขอสร้างข้อมูลสลิป
  PayslipController->PayslipService:generate(recordId)
  PayslipService->PayslipService:ตรวจสิทธิ์ของผู้ดำเนินการตามขอบเขต
  alt ไม่มีสิทธิ์
    PayslipService->PayslipController:error("ไม่มีสิทธิ์ดำเนินการนี้")
    PayslipController->PayslipsPage:display("ไม่มีสิทธิ์ดำเนินการนี้")
  else มีสิทธิ์
    PayslipService->DatabaseInstance:อ่านผลและสลิปเดิม
    PayslipService->PayslipService:ตรวจสิทธิ์ ป้องกันสลิปซ้ำ และยืนยันผู้รับ
    alt มีสลิปของผลเงินเดือนนี้แล้ว
      PayslipService->PayslipController:error("ไม่สามารถสร้างสลิปซ้ำสำหรับผลเงินเดือนเดียวกัน")
      PayslipController->PayslipsPage:display("ไม่สามารถสร้างสลิปซ้ำสำหรับผลเงินเดือนเดียวกัน")
    else ยังไม่มีสลิปของผลเงินเดือนนี้
      alt ผลเงินเดือนยังไม่ล็อกหรือข้อมูลผู้รับไม่ถูกต้อง
        PayslipService->PayslipController:error("ไม่สามารถสร้างสลิปได้ เนื่องจากผลเงินเดือนหรือข้อมูลผู้รับไม่ถูกต้อง")
        PayslipController->PayslipsPage:display("ไม่สามารถสร้างสลิปได้ เนื่องจากผลเงินเดือนหรือข้อมูลผู้รับไม่ถูกต้อง")
      else ผลเงินเดือนล็อกแล้วและข้อมูลผู้รับถูกต้อง
        PayslipService->DatabaseInstance:บันทึกข้อมูลสรุปของสลิป
        PayslipService-->PayslipController:ส่งข้อมูลสลิปที่สร้าง
        PayslipController->PayslipsPage:display(ข้อมูลสลิป)
        HR->PayslipsPage:เลือกบันทึกความพยายามส่งสลิป
        PayslipsPage->PayslipsPage:ตรวจรูปแบบอีเมล
        alt รูปแบบอีเมลไม่ถูกต้อง
          PayslipsPage->PayslipsPage:display("รูปแบบอีเมลไม่ถูกต้อง")
        else รูปแบบอีเมลถูกต้อง
          PayslipsPage->PayslipController:ส่งคำขอบันทึกความพยายามส่ง
          PayslipController->PayslipService:deliver(payslipId, email)
          PayslipService->PayslipService:ตรวจสิทธิ์ของผู้ดำเนินการตามขอบเขต
          alt ไม่มีสิทธิ์
            PayslipService->PayslipController:error("ไม่มีสิทธิ์ดำเนินการนี้")
            PayslipController->PayslipsPage:display("ไม่มีสิทธิ์ดำเนินการนี้")
          else มีสิทธิ์
            PayslipService->PayslipService:ตรวจสิทธิ์และอีเมลผู้รับ
            alt อีเมลไม่ตรงกับผู้รับหรือสลิปไม่พร้อมส่ง
              PayslipService->PayslipController:error("ไม่สามารถบันทึกการส่งได้ เนื่องจากอีเมลผู้รับหรือสถานะสลิปไม่ถูกต้อง")
              PayslipController->PayslipsPage:display("ไม่สามารถบันทึกการส่งได้ เนื่องจากอีเมลผู้รับหรือสถานะสลิปไม่ถูกต้อง")
            else อีเมลตรงกับผู้รับและสลิปพร้อมส่ง
              PayslipService->DatabaseInstance:บันทึกประวัติความพยายามส่ง โดยไม่ส่งอีเมลจริง
              PayslipService-->PayslipController:ส่งผลการบันทึกประวัติการส่ง
              PayslipController->PayslipsPage:display(ประวัติการส่ง)
            end
          end
        end
      end
    end
  end
end
```

## UC18 กรอกข้อมูลลากิจ ลาป่วย และขาดงาน

```text
title UC18 กรอกข้อมูลลากิจ ลาป่วย และขาดงาน
actor HR
participant AttendancePage
participant AttendanceController
participant AttendanceService
participant DatabaseInstance
note over AttendancePage:flow นี้บันทึก attendance/ขาดงาน; การยื่นลาอยู่ UC25
HR->AttendancePage:กรอกข้อมูลวันทำงานหรือการขาดงาน
AttendancePage->AttendancePage:ตรวจว่าพนักงาน วันทำงาน และสถานะไม่ว่าง และวันที่มีรูปแบบถูกต้อง
alt ข้อมูลไม่ถูกต้อง
  AttendancePage->AttendancePage:display("กรุณากรอกข้อมูลให้ครบและใช้รูปแบบที่ถูกต้อง")
else ข้อมูลถูกต้อง
  AttendancePage->AttendanceController:ส่งคำขอสร้างบันทึกวันทำงาน
  AttendanceController->AttendanceController:ตรวจชนิดข้อมูลและพารามิเตอร์คำขอ
  alt ชนิดข้อมูลหรือพารามิเตอร์คำขอไม่ถูกต้อง
    AttendanceController->AttendancePage:display("ชนิดข้อมูลหรือพารามิเตอร์คำขอไม่ถูกต้อง")
  else ชนิดข้อมูลและพารามิเตอร์คำขอถูกต้อง
    AttendanceController->AttendanceService:createManualWorkDay(employeeId, date, status)
    AttendanceService->AttendanceService:ตรวจสิทธิ์ของผู้ดำเนินการตามขอบเขต
    alt ไม่มีสิทธิ์
      AttendanceService->AttendanceController:error("ไม่มีสิทธิ์ดำเนินการนี้")
      AttendanceController->AttendancePage:display("ไม่มีสิทธิ์ดำเนินการนี้")
    else มีสิทธิ์
      AttendanceService->DatabaseInstance:อ่านวันทำงานเดิม
      AttendanceService->AttendanceService:ตรวจวันทำงานซ้ำและสถานะที่บันทึก
      alt มีวันทำงานซ้ำหรือสถานะไม่ถูกต้อง
        AttendanceService->AttendanceController:error("ไม่สามารถบันทึกได้ เนื่องจากมีวันทำงานซ้ำหรือสถานะไม่ถูกต้อง")
        AttendanceController->AttendancePage:display("ไม่สามารถบันทึกได้ เนื่องจากมีวันทำงานซ้ำหรือสถานะไม่ถูกต้อง")
      else วันทำงานไม่ซ้ำและสถานะถูกต้อง
        AttendanceService->DatabaseInstance:บันทึกวันทำงาน
        AttendanceService-->AttendanceController:ส่งบันทึกวันทำงานใหม่
        AttendanceController->AttendancePage:display(บันทึกวันทำงานใหม่)
      end
    end
  end
end
```

## UC19 สร้างพนักงานใหม่

```text
title UC19 สร้างพนักงานใหม่
actor HR
participant NewEmployeePage
participant EmployeeController
participant EmployeeService
participant DatabaseInstance
HR->NewEmployeePage:กรอกข้อมูลพนักงานใหม่และกดบันทึก
NewEmployeePage->NewEmployeePage:ตรวจชื่อ รหัสพนักงาน วันที่เริ่มงาน และค่าจ้างที่ต้องกรอก รวมถึงรูปแบบจำนวนเงิน
alt ข้อมูลไม่ถูกต้อง
  NewEmployeePage->NewEmployeePage:display("กรุณากรอกข้อมูลให้ครบและใช้รูปแบบที่ถูกต้อง")
else ข้อมูลถูกต้อง
  NewEmployeePage->EmployeeController:ส่งคำขอรับพนักงานเข้าระบบ
  EmployeeController->EmployeeController:ตรวจชนิดข้อมูลและพารามิเตอร์คำขอ
  alt ชนิดข้อมูลหรือพารามิเตอร์คำขอไม่ถูกต้อง
    EmployeeController->NewEmployeePage:display("ชนิดข้อมูลหรือพารามิเตอร์คำขอไม่ถูกต้อง")
  else ชนิดข้อมูลและพารามิเตอร์คำขอถูกต้อง
    EmployeeController->EmployeeService:onboardEmployee(employeeData)
    EmployeeService->EmployeeService:ตรวจสิทธิ์ของผู้ดำเนินการตามขอบเขต
    alt ไม่มีสิทธิ์
      EmployeeService->EmployeeController:error("ไม่มีสิทธิ์ดำเนินการนี้")
      EmployeeController->NewEmployeePage:display("ไม่มีสิทธิ์ดำเนินการนี้")
    else มีสิทธิ์
      EmployeeService->DatabaseInstance:อ่านรหัสและสาขา
      EmployeeService->EmployeeService:ตรวจรหัสซ้ำและช่วงการจ้างเริ่มต้น
      alt รหัสพนักงานซ้ำ
        EmployeeService->EmployeeController:error("ไม่สามารถสร้างพนักงานได้ เนื่องจากรหัสพนักงานซ้ำ")
        EmployeeController->NewEmployeePage:display("ไม่สามารถสร้างพนักงานได้ เนื่องจากรหัสพนักงานซ้ำ")
      else รหัสพนักงานไม่ซ้ำ
        alt ข้อมูลสังกัดหรือช่วงการจ้างเริ่มต้นไม่ถูกต้อง
          EmployeeService->EmployeeController:error("ข้อมูลสังกัดหรือช่วงการจ้างเริ่มต้นไม่ถูกต้อง")
          EmployeeController->NewEmployeePage:display("ข้อมูลสังกัดหรือช่วงการจ้างเริ่มต้นไม่ถูกต้อง")
        else ข้อมูลสังกัดและช่วงการจ้างเริ่มต้นถูกต้อง
          EmployeeService->DatabaseInstance:สร้างพนักงานใหม่
          EmployeeService-->EmployeeController:ส่งพนักงานใหม่พร้อมประวัติการจ้างแรก
          EmployeeController->NewEmployeePage:display(พนักงานใหม่พร้อมประวัติการจ้างแรก)
        end
      end
    end
  end
end
```

## UC20a แก้ไขพนักงาน — ข้อมูลทั่วไป

```text
title UC20a แก้ไขพนักงาน — ข้อมูลทั่วไป
actor HR
participant EmployeeDetailPage
participant EmployeeController
participant EmployeeService
participant DatabaseInstance
HR->EmployeeDetailPage:เลือกพนักงานและแก้ข้อมูลทั่วไป
EmployeeDetailPage->EmployeeDetailPage:ตรวจช่องและชนิดข้อมูล
alt ข้อมูลไม่ถูกต้อง
  EmployeeDetailPage->EmployeeDetailPage:display("กรุณากรอกข้อมูลให้ครบและใช้รูปแบบที่ถูกต้อง")
else ข้อมูลถูกต้อง
  EmployeeDetailPage->EmployeeController:ส่งคำขอแก้ข้อมูลพนักงาน
  EmployeeController->EmployeeService:updateEmployee(employeeId, changes)
  EmployeeService->EmployeeService:ตรวจสิทธิ์ของผู้ดำเนินการตามขอบเขต
  alt ไม่มีสิทธิ์
    EmployeeService->EmployeeController:error("ไม่มีสิทธิ์ดำเนินการนี้")
    EmployeeController->EmployeeDetailPage:display("ไม่มีสิทธิ์ดำเนินการนี้")
  else มีสิทธิ์
    EmployeeService->DatabaseInstance:อ่านข้อมูลพนักงานเดิม
    EmployeeService->EmployeeService:ตรวจสิทธิ์และข้อมูลที่เปลี่ยน
    alt ข้อมูลที่แก้ไขไม่ถูกต้องหรือเป็นข้อมูลที่ห้ามเปลี่ยน
      EmployeeService->EmployeeController:error("ไม่สามารถเปลี่ยนข้อมูลพนักงานที่ระบุได้")
      EmployeeController->EmployeeDetailPage:display("ไม่สามารถเปลี่ยนข้อมูลพนักงานที่ระบุได้")
    else ข้อมูลที่แก้ไขถูกต้องและอนุญาตให้เปลี่ยน
      EmployeeService->DatabaseInstance:บันทึกข้อมูลทั่วไปและประวัติการแก้ไข
      EmployeeService-->EmployeeController:ส่งข้อมูลทั่วไปพร้อมประวัติการแก้ไข
      EmployeeController->EmployeeDetailPage:display(ข้อมูลทั่วไปพร้อมประวัติการแก้ไข)
    end
  end
end
```

## UC20b แก้ไขพนักงาน — สังกัดและค่าตอบแทน

```text
title UC20b แก้ไขพนักงาน — สังกัดและค่าตอบแทน
actor HR
participant EmployeeDetailPage
participant EmploymentAssignmentController
participant EmploymentAssignmentService
participant DatabaseInstance
HR->EmployeeDetailPage:เลือกพนักงานและเปลี่ยนสังกัดหรือค่าจ้าง
EmployeeDetailPage->EmployeeDetailPage:ตรวจช่องและชนิดข้อมูล
alt ข้อมูลไม่ถูกต้อง
  EmployeeDetailPage->EmployeeDetailPage:display("กรุณากรอกข้อมูลให้ครบและใช้รูปแบบที่ถูกต้อง")
else ข้อมูลถูกต้อง
  EmployeeDetailPage->EmploymentAssignmentController:ส่งคำขอเพิ่มช่วงการจ้างใหม่
  EmploymentAssignmentController->EmploymentAssignmentService:createAssignment(employeeId, assignment)
  EmploymentAssignmentService->EmploymentAssignmentService:ตรวจสิทธิ์ของผู้ดำเนินการตามขอบเขต
  alt ไม่มีสิทธิ์
    EmploymentAssignmentService->EmploymentAssignmentController:error("ไม่มีสิทธิ์ดำเนินการนี้")
    EmploymentAssignmentController->EmployeeDetailPage:display("ไม่มีสิทธิ์ดำเนินการนี้")
  else มีสิทธิ์
    EmploymentAssignmentService->DatabaseInstance:อ่านช่วงการจ้างเดิม
    EmploymentAssignmentService->EmploymentAssignmentService:ตรวจสิทธิ์และช่วงวันที่ไม่ทับซ้อน
    alt ข้อมูลสังกัดไม่ถูกต้องหรือช่วงวันที่ทับซ้อน
      EmploymentAssignmentService->EmploymentAssignmentController:error("ไม่สามารถเพิ่มประวัติการจ้างได้ เนื่องจากข้อมูลสังกัดหรือช่วงวันที่ไม่ถูกต้อง")
      EmploymentAssignmentController->EmployeeDetailPage:display("ไม่สามารถเพิ่มประวัติการจ้างได้ เนื่องจากข้อมูลสังกัดหรือช่วงวันที่ไม่ถูกต้อง")
    else ข้อมูลสังกัดถูกต้องและช่วงวันที่ไม่ทับซ้อน
      EmploymentAssignmentService->DatabaseInstance:ปิดช่วงเดิมและสร้างช่วงการจ้างใหม่
      EmploymentAssignmentService-->EmploymentAssignmentController:ส่งประวัติการจ้างช่วงใหม่
      EmploymentAssignmentController->EmployeeDetailPage:display(ประวัติการจ้างช่วงใหม่)
    end
  end
end
```

## UC21 ลบพนักงาน

```text
title UC21 ลบพนักงาน
actor HR
participant EmployeeDetailPage
participant EmployeeController
participant EmployeeService
participant DatabaseInstance
note over EmployeeDetailPage:ปิดสถานะพนักงานและเก็บประวัติ ไม่ hard delete
HR->EmployeeDetailPage:เลือกพนักงานแล้วเปลี่ยนสถานะ
EmployeeDetailPage->EmployeeDetailPage:ตรวจว่ามีรหัสพนักงานและสถานะใหม่อยู่ในรูปแบบที่รับได้
alt ข้อมูลไม่ถูกต้อง
  EmployeeDetailPage->EmployeeDetailPage:display("กรุณากรอกข้อมูลให้ครบและใช้รูปแบบที่ถูกต้อง")
else ข้อมูลถูกต้อง
  EmployeeDetailPage->EmployeeController:ส่งคำขอเปลี่ยนสถานะพนักงาน
  EmployeeController->EmployeeController:ตรวจชนิดข้อมูลและพารามิเตอร์คำขอ
  alt ชนิดข้อมูลหรือพารามิเตอร์คำขอไม่ถูกต้อง
    EmployeeController->EmployeeDetailPage:display("ชนิดข้อมูลหรือพารามิเตอร์คำขอไม่ถูกต้อง")
  else ชนิดข้อมูลและพารามิเตอร์คำขอถูกต้อง
    EmployeeController->EmployeeService:changeEmployeeStatus(employeeId, status)
    EmployeeService->EmployeeService:ตรวจสิทธิ์ของผู้ดำเนินการตามขอบเขต
    alt ไม่มีสิทธิ์
      EmployeeService->EmployeeController:error("ไม่มีสิทธิ์ดำเนินการนี้")
      EmployeeController->EmployeeDetailPage:display("ไม่มีสิทธิ์ดำเนินการนี้")
    else มีสิทธิ์
      EmployeeService->DatabaseInstance:อ่านสถานะเดิม
      EmployeeService->EmployeeService:ตรวจว่าการเปลี่ยนสถานะยังรักษาข้อมูลย้อนหลัง
      alt สถานะหรือวันที่สิ้นสุดการจ้างไม่ถูกต้อง
        EmployeeService->EmployeeController:error("ไม่สามารถเปลี่ยนสถานะพนักงานได้ด้วยข้อมูลที่ระบุ")
        EmployeeController->EmployeeDetailPage:display("ไม่สามารถเปลี่ยนสถานะพนักงานได้ด้วยข้อมูลที่ระบุ")
      else สถานะและวันที่สิ้นสุดการจ้างถูกต้อง
        EmployeeService->DatabaseInstance:ปิดสถานะพนักงาน
        EmployeeService-->EmployeeController:ส่งสถานะพนักงานใหม่โดยคงประวัติ
        EmployeeController->EmployeeDetailPage:display(สถานะพนักงานใหม่โดยคงประวัติ)
      end
    end
  end
end
```

## UC22 ค้นหาพนักงาน

```text
title UC22 ค้นหาพนักงาน
actor HR
participant EmployeesPage
participant EmployeeController
participant EmployeeService
participant DatabaseInstance
HR->EmployeesPage:กรอกเงื่อนไขเพื่อค้นหาพนักงาน
EmployeesPage->EmployeesPage:ตรวจว่าตัวกรองค้นหาเป็นข้อความและมีความยาวตามที่ฟอร์มรับได้
alt ข้อมูลไม่ถูกต้อง
  EmployeesPage->EmployeesPage:display("กรุณากรอกข้อมูลให้ครบและใช้รูปแบบที่ถูกต้อง")
else ข้อมูลถูกต้อง
  EmployeesPage->EmployeeController:ส่งคำขอค้นหารายชื่อพนักงาน
  EmployeeController->EmployeeController:ตรวจชนิดข้อมูลและพารามิเตอร์คำขอ
  alt ชนิดข้อมูลหรือพารามิเตอร์คำขอไม่ถูกต้อง
    EmployeeController->EmployeesPage:display("ชนิดข้อมูลหรือพารามิเตอร์คำขอไม่ถูกต้อง")
  else ชนิดข้อมูลและพารามิเตอร์คำขอถูกต้อง
    EmployeeController->EmployeeService:listEmployees(filters)
    EmployeeService->EmployeeService:ตรวจสิทธิ์ของผู้ดำเนินการตามขอบเขต
    alt ไม่มีสิทธิ์
      EmployeeService->EmployeeController:error("ไม่มีสิทธิ์ดำเนินการนี้")
      EmployeeController->EmployeesPage:display("ไม่มีสิทธิ์ดำเนินการนี้")
    else มีสิทธิ์
      EmployeeService->DatabaseInstance:ค้นรายชื่อพนักงาน
      EmployeeService->EmployeeService:จำกัดผลตามสาขาหรือแผนกที่มีสิทธิ์
      EmployeeService-->EmployeeController:ส่งรายชื่อพนักงานที่เข้าถึงได้
      EmployeeController->EmployeesPage:display(รายชื่อพนักงานที่เข้าถึงได้)
    end
  end
end
```

## UC23a แก้ไขประเภทการลาและข้อมูลสาย — ประเภทการลา

```text
title UC23a แก้ไขประเภทการลาและข้อมูลสาย — ประเภทการลา
actor Manager
participant LeavePage
participant LeaveController
participant LeaveService
participant DatabaseInstance
Manager->LeavePage:เลือกคำขอลาและแก้ประเภทก่อนอนุมัติ
LeavePage->LeavePage:ตรวจรหัสและประเภทลา
alt ข้อมูลไม่ถูกต้อง
  LeavePage->LeavePage:display("กรุณากรอกข้อมูลให้ครบและใช้รูปแบบที่ถูกต้อง")
else ข้อมูลถูกต้อง
  LeavePage->LeaveController:ส่งคำขออนุมัติพร้อมประเภทลาสุดท้าย
  LeaveController->LeaveService:approveLeave(requestId, finalLeaveTypeId)
  LeaveService->LeaveService:ตรวจสิทธิ์ของผู้ดำเนินการตามขอบเขต
  alt ไม่มีสิทธิ์
    LeaveService->LeaveController:error("ไม่มีสิทธิ์ดำเนินการนี้")
    LeaveController->LeavePage:display("ไม่มีสิทธิ์ดำเนินการนี้")
  else มีสิทธิ์
    LeaveService->DatabaseInstance:อ่านคำขอและโควตา
    LeaveService->LeaveService:ตรวจสิทธิ์ โควตา และประเภทลาสุดท้าย
    alt ประเภทลาหรือสถานะคำขอไม่ถูกต้อง
      LeaveService->LeaveController:error("ไม่สามารถแก้ประเภทการลาได้ในสถานะนี้")
      LeaveController->LeavePage:display("ไม่สามารถแก้ประเภทการลาได้ในสถานะนี้")
    else ประเภทลาและสถานะคำขอถูกต้อง
      alt จำนวนวันเกินสิทธิ์ผู้อนุมัติหรือโควตาไม่พอ
        LeaveService->LeaveController:error("ไม่สามารถอนุมัติได้ เนื่องจากเกินสิทธิ์ผู้อนุมัติหรือโควตาการลาไม่พอ")
        LeaveController->LeavePage:display("ไม่สามารถอนุมัติได้ เนื่องจากเกินสิทธิ์ผู้อนุมัติหรือโควตาการลาไม่พอ")
      else จำนวนวันอยู่ในสิทธิ์ผู้อนุมัติและโควตาเพียงพอ
        LeaveService->DatabaseInstance:บันทึกผลและประวัติ
        LeaveService-->LeaveController:ส่งผลอนุมัติและประวัติการเปลี่ยนประเภทลา
        LeaveController->LeavePage:display(ผลอนุมัติและประวัติการเปลี่ยนประเภทลา)
      end
    end
  end
end
```

## UC23b แก้ไขประเภทการลาและข้อมูลสาย — ข้อมูลมาสาย

```text
title UC23b แก้ไขประเภทการลาและข้อมูลสาย — ข้อมูลมาสาย
actor Manager
participant AttendancePage
participant AttendanceController
participant AttendanceService
participant DatabaseInstance
Manager->AttendancePage:เลือกวันทำงานที่ต้องแก้ข้อมูลมาสาย
AttendancePage->AttendancePage:ตรวจรหัสและข้อมูลเวลา
alt ข้อมูลไม่ถูกต้อง
  AttendancePage->AttendancePage:display("กรุณากรอกข้อมูลให้ครบและใช้รูปแบบที่ถูกต้อง")
else ข้อมูลถูกต้อง
  AttendancePage->AttendanceController:ส่งคำขอแก้บันทึกวันทำงาน
  AttendanceController->AttendanceService:correctWorkDay(recordId, changes)
  AttendanceService->AttendanceService:ตรวจสิทธิ์ของผู้ดำเนินการตามขอบเขต
  alt ไม่มีสิทธิ์
    AttendanceService->AttendanceController:error("ไม่มีสิทธิ์ดำเนินการนี้")
    AttendanceController->AttendancePage:display("ไม่มีสิทธิ์ดำเนินการนี้")
  else มีสิทธิ์
    AttendanceService->DatabaseInstance:อ่านวันทำงานเดิม
    AttendanceService->AttendanceService:ตรวจสิทธิ์และข้อมูลเวลาที่แก้
    alt ข้อมูลเวลาไม่ถูกต้องหรือวันทำงานอยู่ในรอบที่ล็อกแล้ว
      AttendanceService->AttendanceController:error("ไม่สามารถแก้ข้อมูลมาสายได้ เนื่องจากข้อมูลเวลาไม่ถูกต้องหรือรอบล็อกแล้ว")
      AttendanceController->AttendancePage:display("ไม่สามารถแก้ข้อมูลมาสายได้ เนื่องจากข้อมูลเวลาไม่ถูกต้องหรือรอบล็อกแล้ว")
    else ข้อมูลเวลาถูกต้องและรอบยังไม่ล็อก
      AttendanceService->DatabaseInstance:บันทึกข้อมูลเวลาและประวัติการแก้ไข
      AttendanceService-->AttendanceController:ส่งข้อมูลเวลาที่แก้พร้อมหลักฐาน
      AttendanceController->AttendancePage:display(ข้อมูลเวลาที่แก้พร้อมหลักฐาน)
    end
  end
end
```

## UC24 อนุมัติหรือปฏิเสธการลาภายในแผนก

```text
title UC24 อนุมัติหรือปฏิเสธการลาภายในแผนก
actor Manager
participant LeavePage
participant LeaveController
participant LeaveService
participant DatabaseInstance
note over LeavePage:Supervisor อนุมัติได้ไม่เกิน 3 วัน; Branch Manager อนุมัติได้ทุกระยะภายในสาขา
Manager->LeavePage:เลือกคำขอลาแล้วอนุมัติหรือปฏิเสธ
LeavePage->LeavePage:ตรวจรหัสคำขอและข้อมูลการพิจารณา
alt ข้อมูลไม่ถูกต้อง
  LeavePage->LeavePage:display("กรุณาเลือกคำขอและกรอกข้อมูลให้ถูกต้อง")
else ข้อมูลถูกต้อง
  LeavePage->LeaveController:ส่งคำขอพิจารณาการลา
  LeaveController->LeaveController:ตรวจชนิดข้อมูลและพารามิเตอร์คำขอ
  alt ชนิดข้อมูลหรือพารามิเตอร์คำขอไม่ถูกต้อง
    LeaveController->LeavePage:display("ชนิดข้อมูลหรือพารามิเตอร์คำขอไม่ถูกต้อง")
  else ชนิดข้อมูลและพารามิเตอร์คำขอถูกต้อง
    alt เลือกอนุมัติ
      LeaveController->LeaveService:approveLeave(requestId, finalLeaveTypeId)
    else เลือกปฏิเสธ
      LeaveController->LeaveService:rejectLeave(requestId, remark)
    end
    LeaveService->LeaveService:ตรวจสิทธิ์ตามแผนกหรือสาขา
    alt ไม่มีสิทธิ์
      LeaveService->LeaveController:error("ไม่มีสิทธิ์พิจารณาคำขอลานี้")
      LeaveController->LeavePage:display("ไม่มีสิทธิ์พิจารณาคำขอลานี้")
    else มีสิทธิ์
      LeaveService->DatabaseInstance:อ่านคำขอลาและสถานะ
      LeaveService->LeaveService:ตรวจสถานะคำขอและการล็อกรอบเงินเดือน
      alt คำขอพิจารณาแล้วหรือรอบล็อกแล้ว
        LeaveService->LeaveController:error("ไม่สามารถพิจารณาคำขอนี้ได้ในสถานะปัจจุบัน")
        LeaveController->LeavePage:display("ไม่สามารถพิจารณาคำขอนี้ได้ในสถานะปัจจุบัน")
      else คำขอรอพิจารณาและรอบยังไม่ล็อก
        alt อนุมัติ
          LeaveService->DatabaseInstance:อ่านประเภทการลาและโควตา
          LeaveService->LeaveService:ตรวจประเภทลา จำนวนวันตามสิทธิ์ และโควตา
          alt ประเภทลาไม่ถูกต้อง จำนวนวันเกินสิทธิ์ หรือโควตาไม่พอ
            LeaveService->LeaveController:error("ไม่สามารถอนุมัติได้ กรุณาตรวจประเภทลา จำนวนวัน และโควตา")
            LeaveController->LeavePage:display("ไม่สามารถอนุมัติได้ กรุณาตรวจประเภทลา จำนวนวัน และโควตา")
          else ประเภทลาถูกต้อง จำนวนวันอยู่ในสิทธิ์ และโควตาเพียงพอ
            LeaveService->DatabaseInstance:บันทึกอนุมัติ ใช้โควตา อัปเดตวันทำงาน และเพิ่มประวัติใน transaction
            LeaveService-->LeaveController:ส่งผลอนุมัติและประวัติการพิจารณา
            LeaveController->LeavePage:display(ผลอนุมัติและประวัติการพิจารณา)
          end
        else ปฏิเสธ
          LeaveService->DatabaseInstance:บันทึกปฏิเสธและเพิ่มประวัติ โดยไม่ใช้โควตาหรือแก้วันทำงาน
          LeaveService-->LeaveController:ส่งผลปฏิเสธและประวัติการพิจารณา
          LeaveController->LeavePage:display(ผลปฏิเสธและประวัติการพิจารณา)
        end
      end
    end
  end
end
```

## UC25 ยื่นคำร้องขอลา

```text
title UC25 ยื่นคำร้องขอลา
actor Employee
participant LeavePage
participant LeaveController
participant LeaveService
participant DatabaseInstance
Employee->LeavePage:กรอกประเภท วัน และเหตุผลแล้วกดยื่นลา
LeavePage->LeavePage:ตรวจประเภทลา วันที่เริ่ม วันสิ้นสุด และเหตุผลว่าไม่ว่างและวันที่มีรูปแบบถูกต้อง
alt ข้อมูลไม่ถูกต้อง
  LeavePage->LeavePage:display("กรุณากรอกข้อมูลให้ครบและใช้รูปแบบที่ถูกต้อง")
else ข้อมูลถูกต้อง
  LeavePage->LeaveController:ส่งคำขอยื่นการลา
  LeaveController->LeaveController:ตรวจชนิดข้อมูลและพารามิเตอร์คำขอ
  alt ชนิดข้อมูลหรือพารามิเตอร์คำขอไม่ถูกต้อง
    LeaveController->LeavePage:display("ชนิดข้อมูลหรือพารามิเตอร์คำขอไม่ถูกต้อง")
  else ชนิดข้อมูลและพารามิเตอร์คำขอถูกต้อง
    LeaveController->LeaveService:submitLeave(employeeId, dates, leaveType)
    LeaveService->LeaveService:ตรวจสิทธิ์ของผู้ดำเนินการตามขอบเขต
    alt ไม่มีสิทธิ์
      LeaveService->LeaveController:error("ไม่มีสิทธิ์ดำเนินการนี้")
      LeaveController->LeavePage:display("ไม่มีสิทธิ์ดำเนินการนี้")
    else มีสิทธิ์
      LeaveService->DatabaseInstance:อ่านประเภทและโควตา
      LeaveService->LeaveService:ตรวจวันทับซ้อน จำนวนวัน และโควตา
      alt วันลาทับซ้อนหรือจำนวนวันไม่ถูกต้อง
        LeaveService->LeaveController:error("ไม่สามารถยื่นลาได้ เนื่องจากช่วงวันทับซ้อนหรือจำนวนวันไม่ถูกต้อง")
        LeaveController->LeavePage:display("ไม่สามารถยื่นลาได้ เนื่องจากช่วงวันทับซ้อนหรือจำนวนวันไม่ถูกต้อง")
      else วันลาไม่ทับซ้อนและจำนวนวันถูกต้อง
        alt โควตาการลาไม่เพียงพอ
          LeaveService->LeaveController:error("ไม่สามารถยื่นลาได้ เนื่องจากโควตาการลาไม่เพียงพอ")
          LeaveController->LeavePage:display("ไม่สามารถยื่นลาได้ เนื่องจากโควตาการลาไม่เพียงพอ")
        else โควตาการลาเพียงพอ
          LeaveService->DatabaseInstance:บันทึกคำขอลา
          LeaveService-->LeaveController:ส่งคำขอลาสถานะรอพิจารณา
          LeaveController->LeavePage:display(คำขอลาสถานะรอพิจารณา)
        end
      end
    end
  end
end
```

## UC26a ยื่นคำร้องเงินกู้หรือเบิกล่วงหน้า — เงินทดรอง

```text
title UC26a ยื่นคำร้องเงินกู้หรือเบิกล่วงหน้า — เงินทดรอง
actor HR
participant FinancePage
participant AdvanceController
participant AdvanceService
participant DatabaseInstance
note over FinancePage:เงินกู้สร้างโดย HR/Owner; เงินทดรองมีเกณฑ์วันที่ 20 วันทำงาน 20 วัน และครึ่งฐานเงินเดือน
HR->FinancePage:กรอกจำนวนเงินทดรองแล้วกดยื่น
FinancePage->FinancePage:ตรวจช่องที่ต้องกรอกและชนิดข้อมูลเบื้องต้น
alt ข้อมูลไม่ถูกต้อง
  FinancePage->FinancePage:display("กรุณากรอกข้อมูลให้ครบและใช้รูปแบบที่ถูกต้อง")
else ข้อมูลถูกต้อง
  FinancePage->AdvanceController:ส่งคำขอเงินทดรอง
  AdvanceController->AdvanceService:submitAdvance(employeeId, amount)
  AdvanceService->AdvanceService:ตรวจสิทธิ์ของผู้ดำเนินการตามขอบเขต
  alt ไม่มีสิทธิ์
    AdvanceService->AdvanceController:error("ไม่มีสิทธิ์ดำเนินการนี้")
    AdvanceController->FinancePage:display("ไม่มีสิทธิ์ดำเนินการนี้")
  else มีสิทธิ์
    AdvanceService->DatabaseInstance:อ่านเงินเดือนฐานและจำนวนวันทำงาน
    AdvanceService->AdvanceService:ตรวจสิทธิ์ วันที่ยื่น วันทำงาน และวงเงิน
    alt วันที่ยื่นหรือวันทำงานไม่ผ่านเกณฑ์ที่กำหนด
      AdvanceService->AdvanceController:error("ยังไม่ผ่านเกณฑ์วันที่ยื่นหรือจำนวนวันทำงานสำหรับเงินทดรอง")
      AdvanceController->FinancePage:display("ยังไม่ผ่านเกณฑ์วันที่ยื่นหรือจำนวนวันทำงานสำหรับเงินทดรอง")
    else วันที่ยื่นและวันทำงานผ่านเกณฑ์
      alt จำนวนเงินไม่ถูกต้องหรือเกินวงเงิน
        AdvanceService->AdvanceController:error("จำนวนเงินทดรองไม่ถูกต้องหรือเกินวงเงินที่กำหนด")
        AdvanceController->FinancePage:display("จำนวนเงินทดรองไม่ถูกต้องหรือเกินวงเงินที่กำหนด")
      else จำนวนเงินถูกต้องและไม่เกินวงเงิน
        AdvanceService->DatabaseInstance:บันทึกคำขอเงินทดรอง
        AdvanceService-->AdvanceController:ส่งคำขอเงินทดรองใหม่
        AdvanceController->FinancePage:display(คำขอเงินทดรองใหม่)
      end
    end
  end
end
```

## UC26b ยื่นคำร้องเงินกู้หรือเบิกล่วงหน้า — เงินกู้

```text
title UC26b ยื่นคำร้องเงินกู้หรือเบิกล่วงหน้า — เงินกู้
actor HR
participant FinancePage
participant LoanController
participant LoanService
participant DatabaseInstance
note over FinancePage:เงินกู้สร้างโดย HR/Owner; เงินทดรองมีเกณฑ์วันที่ 20 วันทำงาน 20 วัน และครึ่งฐานเงินเดือน
HR->FinancePage:กรอกเงินกู้และจำนวนงวดแล้วกดยื่น
FinancePage->FinancePage:ตรวจช่องที่ต้องกรอกและชนิดข้อมูลเบื้องต้น
alt ข้อมูลไม่ถูกต้อง
  FinancePage->FinancePage:display("กรุณากรอกข้อมูลให้ครบและใช้รูปแบบที่ถูกต้อง")
else ข้อมูลถูกต้อง
  FinancePage->LoanController:ส่งคำขอเงินกู้
  LoanController->LoanService:createLoan(employeeId, amount, installments)
  LoanService->LoanService:ตรวจสิทธิ์ของผู้ดำเนินการตามขอบเขต
  alt ไม่มีสิทธิ์
    LoanService->LoanController:error("ไม่มีสิทธิ์ดำเนินการนี้")
    LoanController->FinancePage:display("ไม่มีสิทธิ์ดำเนินการนี้")
  else มีสิทธิ์
    LoanService->DatabaseInstance:อ่านข้อมูลพนักงานและหนี้เดิม
    LoanService->LoanService:ตรวจสิทธิ์ วงเงิน และจำนวนงวด
    alt จำนวนเงินหรือจำนวนงวดไม่ถูกต้อง
      LoanService->LoanController:error("จำนวนเงินกู้หรือจำนวนงวดหักชำระไม่ถูกต้อง")
      LoanController->FinancePage:display("จำนวนเงินกู้หรือจำนวนงวดหักชำระไม่ถูกต้อง")
    else จำนวนเงินและจำนวนงวดถูกต้อง
      LoanService->DatabaseInstance:บันทึกเงินกู้
      LoanService-->LoanController:ส่งเงินกู้พร้อมตารางหักชำระ
      LoanController->FinancePage:display(เงินกู้พร้อมตารางหักชำระ)
    end
  end
end
```
