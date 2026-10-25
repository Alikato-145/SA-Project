# รายงานส่งมอบ Haris Payroll: Login และ Use Case 1–16

วันที่จัดทำ: 26 ตุลาคม 2026 (Asia/Bangkok)
สถานะความสามารถ: ผ่าน automated UAT และ final review ตามขอบเขตที่ตกลง
รอบทดสอบครบชุดล่าสุด: 25 ตุลาคม 2026, `20261025T131201Z-66768`

## ผลส่งมอบ

ต่อยอดระบบเดิมให้ทำ Login และ UC1–16 ผ่านหน้าเว็บ โดยแยกบัญชี single-role ของ EMPLOYEE, SUPERVISOR, BRANCH_MANAGER, HR และ OWNER ไม่ใช้ OWNER ทดแทน actor อื่น ฝ่ายบัญชีใช้ HR เดิม รายละเอียดทุก actor/ขั้นตอน/การอ่านซ้ำ/กรณีปฏิเสธอยู่ใน [actor matrix](../use-case-actor-matrix.md)

| ขอบเขต | สิ่งที่ตรวจส่งมอบ |
|---|---|
| Login | เข้า/ออกระบบทั้ง5roles; token ที่ logout แล้วใช้ซ้ำไม่ได้ ขณะ session อื่นยังใช้ได้; no-grant/disabled/locked boundaries |
| UC1–3 พนักงาน | HR/OWNER ทุกสาขา; manager เฉพาะสาขาตน สร้าง/แก้/ยุติการจ้างผ่านเว็บ; ไม่ลบประวัติ ไม่ยกระดับ role/bank rights |
| UC4–6 เงินเดือน | HR/OWNER สร้างรอบ เพิ่ม/อนุมัติรายการปรับ preview และ lock; pending/readiness guards; คิดรายการครั้งเดียวและรักษาค่าที่ล็อก |
| UC7–11 จ่ายเงิน | ช่องทาง/เบอร์รับเงินแยกจากเบอร์ติดต่อ; กลุ่มเงินสด/โอน/ประกันสังคมไม่ซ้ำ; freeze ยอด/ปลายทาง/สาขา; QR decode ตรง; manual confirm/cancel/history/ยอดจ่ายและค้าง |
| UC12–14 เอกสาร | HR/OWNER ออกสลิป ส่งอีเมลเข้า local Mailpit และดาวน์โหลด PDF เงินเดือน/เจ้าหนี้; ตัวกรอง/ยอดรวม/รายบุคคลตรง locked payroll; CSV ใช้ frozen bank และ earned SS base |
| UC15 ลา | Employee ยื่นของตน → HR อนุมัติ request เดิม → employee reload เห็น approved/ประวัติ; ขอบเขต supervisor3vs4days/manager ตรวจแยก |
| UC16 กู้/เบิก | Employee ยื่นกู้/เบิกล่วงหน้าของตน; HR อนุมัติ/OWNER ปฏิเสธตามสิทธิ์; loan/installments atomic; actual-date advance eligibility และยอดสุทธิ |
| Supporting scope | Own-only สลิป/PDF สำหรับ employee และ linked scoped roles; direct endpoint denials และ department/branch scope |

## ประเด็น final review ที่แก้ครบ

1. Payment-destination self-read ต้องมี valid active grant ร่วมกับ identity; no-grant/invalid/inactive/last-grant-revoked ถูกปฏิเสธก่อนอ่านปลายทาง โดยไม่เปลี่ยน intentional account-state authentication
2. หน้ายืนยันจ่ายแสดง frozen bank code/holder/last4 และ frozen PromptPay phone แยกกันเมื่อมีทั้งคู่ ไม่ซ่อนบัญชีธนาคารหลังแก้ข้อมูล live
3. Mailpit consumers อ่านพอร์ตที่กำหนดจริง ตรวจ actual messages/message/attachment URLs ที่18025และ18026
4. เชื่อม employee-created leave เดิมไปถึง approval/reload/decision history และแก้ conflicting color flags ใน launcher
5. CI upload เก็บ generated full-UAT evidence ที่ wrapper ใช้จริง; Git ignore หลักฐานดิบ โดยไม่ลบไฟล์ในเครื่อง

[รายงานแก้ละเอียดและ RED→GREEN](13-final-review-repairs.md) · [final review + scoped re-review](12-final-delivery-review.md)

## ผลทดสอบที่ตรวจหลักฐานแล้ว

| การตรวจ | ผล |
|---|---|
| Backend typecheck + migrated disposable PostgreSQL suite | **540 passed / 0 skipped / 0 failed**,119files |
| Frontend unit | **54 passed / 0 failed**,19files,175assertions |
| Frontend lint / TypeScript / production build | ผ่านทั้งหมด |
| Browser ทั้งชุดหลังแก้ | **49 passed / 0 failed / 0 skipped / 0 flaky**,9.9min;1worker,0retries,ไม่มีfile/grepfilter |
| Focused authorization service + Elysia route |4passed,63assertions; มี observed RED ก่อนซ่อม |
| Configured mailbox consumers |2passed ทั้งdefault/override;ไม่มีnetworkในfocusedcheck |
| Wrapper configuration/color/exit status |5passed,38assertions; failureexit17ยังส่งต่อ |
| Final review |SpecPASS / QualityAPPROVED; openCritical0/Important0/Minor0 |

ไม่รวม targeted reruns เป็นผล49 รอบที่ผู้ใช้สั่งหยุดมี27completed/exit143 และเก็บเป็น interrupted เท่านั้น รอบสุดท้ายข้างต้นเป็นหนึ่ง invocation สำเร็จจริง Code/test/harness561paths คงเดิมระหว่าง full run; broad569manifest ต่าง1ไฟล์ที่ root อัปเดตบันทึกการอนุญาต push/merge ซึ่งเปิดเผยแยกใน report13 ไม่มี runtime change หลังตรวจครบ การแก้ workflow/ignore หลังรันจบตรวจ syntax/path แยก ไม่อ้างว่า remote CI ผ่านแล้ว

## เวอร์ชันและ integration

| Repository | เวอร์ชันโค้ดส่งมอบ | เป้าหมาย |
|---|---|---|
| [Backend](https://github.com/Alikato-145/SA-Project-Backend/commit/c2a404db6d00df18b0f1a7322e67f15ec9da1d41) | `c2a404db6d00df18b0f1a7322e67f15ec9da1d41` | `develop`; normal fast-forward/push สำเร็จ |
| [Frontend](https://github.com/Alikato-145/SA-Project-Frontend/commit/e6d6fb65b64096840d563e49df29ece981e355af) | `e6d6fb65b64096840d563e49df29ece981e355af` | `develop`; normal fast-forward/push สำเร็จ |
| Root SA-Project | รายงานฉบับนี้ พร้อม logical schema/reference, verification configuration และ submodule pointers ของสองเวอร์ชันข้างต้น | `develop` ตามคำสั่งผู้ใช้ |

Merge รักษา committed baseline เดิมทั้งหมด ไม่ force push และไม่รวมเอกสาร academic/DOCX/PPTX ที่ผู้ใช้แก้ค้างนอกงานนี้ Root integration อ้างอิงต้นไม้โค้ดเดียวกับที่ผ่าน tests/review ไม่มี deployment หรือ migration บนฐานจริง

## เอกสารและหลักฐาน

- [Progress ราย subtask และเหตุการณ์หยุด/ต่อ](../use-case-delivery-progress.md)
- [ข้อกำหนดและสิทธิ์](../specs/2026-10-25-use-case-delivery-design.md)
- [BP/คู่มือแยกบทบาท](../use-case-delivery-handover.md)
- [Schema เฉพาะ Use Case สำหรับนำเสนอ](../use-case-schema-summary.md)
- [การตัดสินใจและต้นทุน/ข้อจำกัดทั้ง12ข้อ](delivery-decisions-and-limits.md)
- รายงานแต่ละ subtask: reports02–11; final findings/repairs: reports12–13

Logical/executable schema ทั้งชุดมี39tables/25enums และmigration chain0000–0005; roundซ่อมสุดท้ายไม่เพิ่มschema/migration/dependency หลักฐานดิบเก็บในเครื่องใต้ `docs/superpowers/reports/*-evidence/` และ CI artifacts ไม่ push traces/session/fixtures ขนาดใหญ่เข้าGit Compact reports นี้เป็นบันทึกที่ versioned

## ขอบเขตการรับรอง

ทดสอบเฉพาะ disposable verification stack และ local Mailpit ด้วย synthetic data ไม่ใช่ production/real-user UAT การสร้างหรือสแกน QR/ออกสลิปไม่ยืนยันว่าเงินจริงเข้าบัญชี เจ้าหน้าที่ตรวจผลภายนอกแล้วจึงบันทึก paid; ไม่เชื่อม bank API หรือ external SMTP การรับรองไฟล์จากธนาคาร/ประกันสังคม, PromptPay ownership, production operations และความสามารถคืนเงิน/แบ่งจ่าย/OCR/time-clock อยู่นอกขอบเขตตามข้อกำหนดเดิม การรันอัตโนมัติทุก30นาทียังคง PAUSED ตามคำขอก่อนหน้า
