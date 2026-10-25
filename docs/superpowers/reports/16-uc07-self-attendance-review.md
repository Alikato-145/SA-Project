### Spec Compliance

- ✅ **Spec compliant / PASS** สำหรับ Task 1 UC07 ไม่พบ requirement ที่ขาด, extra scope หรือพฤติกรรมที่ขัดกับ binding design
- ⚠️ Final unfiltered 20-use-case/actor acceptance และ integration อยู่นอก Task 1; root ต้องตรวจใน final delivery gate ผลนี้ไม่รับรอง real external delivery/payment

Reviewed 26 October 2026 against the frozen Task 1 handback. Review scope is the seven application/test files identified in `task-1-review-package.md`; surrounding authorization, attendance, schedule, transaction, payroll-lock and employee-context code was read to trace the complete request. Application sources, tests, index and HEAD were not modified.

### Strengths

- **Spec compliance: PASS.** ไม่พบข้อกำหนด UC07 ที่ยังขาดหรือพฤติกรรมที่ขัดกับ binding design ในขอบเขต Task 1
- **Code quality: PASS.** ไม่พบ actionable defect ที่ต้องแก้ก่อน checkpoint การเพิ่มสิทธิ์จำกัดอยู่ใน attendance service และใช้ authorization parser, dated assignment, transaction, payroll lock และ audit เดิม
- **Application findings: none.** ไม่มี application defect ที่ต้องส่งกลับ implementer

### Requirements and authorization traced

อ่าน root `AGENTS.md`, `frontend/AGENTS.md`, Task 1 brief/report/review package และ global + UC07 constraints ใน `2026-10-26-use-case-20-alignment-design.md` ก่อนประเมิน การตรวจใช้หลัก minimal changes จาก ponytail และไม่เปิด subagent เพิ่ม

| ประเด็น | ผลการตรวจและตำแหน่งหลัก |
| --- | --- |
| Real active EMPLOYEE/self authority | `backend/src/features/attendance/attendance.runtime.service.ts:14–22` ใช้ staff `manage` เดิมก่อน และ fallback เฉพาะ `FORBIDDEN_SCOPE` เมื่อ trusted employee identity ตรงกับ target และ `parseActiveGrant` ยืนยัน EMPLOYEE/self ที่มี scope shape ถูกต้อง Shared `manage` ไม่ได้ถูกแก้ Auth boundary โหลด account/grants ปัจจุบันและตัด inactive/malformed roles ก่อนสร้าง trusted actor |
| Own list/context/calendar | เส้นทางเดิมเรียก shared read authorization; own employee association และ valid self grant เป็นเงื่อนไข server-side การ list แบบ branch/global ยังถูกปฏิเสธสำหรับ employee และ rows ถูกกรองด้วย `visibleWorkDays` |
| Historical branch | Runtime validation บรรทัด 37–44 โหลด assignment ตาม work date และเทียบ branch; base create service ตรวจ assignment ซ้ำ การ correction ใช้ employee/date/branch ของ OLD row; request correction ไม่มีช่องเปลี่ยน identity, date หรือ branch |
| Protected OLD records and provenance | Runtime บรรทัด 88–97 ปฏิเสธ OLD row ที่ไม่ใช่ manual present/late/absent ก่อน merge correction จึงเปลี่ยน import/biometric/leave/holiday ให้เป็น ordinary row เพื่อเลี่ยง guard ไม่ได้ Base service/repository ยังกัน leave และ create บังคับ source เป็น manual; route explicitly rejects `entry_source` |
| Schedule and deductions | บรรทัด 37–54 ตรวจ effective schedule/override, public holiday, weekly holiday และ closed day สำหรับ self; require clock-in ของ worked/late และห้าม clock timestamps ของ absence; ตรวจ derived Bangkok late minutes/status และ deductible flag Base record validation ตรวจ work date, clock range และ minutes เพิ่มอีกชั้น Open override ที่สร้างผ่าน schedule service ต้องมี complete hours |
| Locked payroll and atomicity | `runOperation` เปิด transaction และ serialize payroll inputs ก่อนอ่าน/เขียน Runtime ตรวจ input mutability ทั้ง create/correct และ base correction มี guard ซ้ำ จึงไม่เปิดทางแก้ locked inputs ผ่าน self fallback |
| New correction reason and audit | บรรทัด 93–95 อ่านจาก correction command ใหม่ ไม่ยืม OLD note; trim และตรวจ 5–1,000 characters พร้อม letter/digit Audit เดิมอยู่ใน transaction เดียวกัน บันทึก actor, OLD/NEW และ note โดยไม่เปลี่ยน creator/source |
| UI own context and staff regression | `frontend/app/(dashboard)/attendance/page.tsx:24–78,115–128` ใช้ EmployeeContextPicker เดิม, linked self identity, dated branch, limited statuses, read-only derived minutes และ reason guidance Staff retain management picker/statuses/actions และ shared authorization policy ยังเดิม Route access เพิ่มเฉพาะ attendance |

### Evidence checked

ตรวจ SHA256 ของไฟล์ทั้งเจ็ดกับ `16-uc07-self-attendance-evidence/task-1-tested-source-manifest.json`: **MATCH ทั้ง 7/7** ฐานที่ handback ระบุคือ backend `c2a404db6d00df18b0f1a7322e67f15ec9da1d41` และ frontend `e6d6fb65b64096840d563e49df29ece981e355af`

อ่าน focused integration test และ browser scenario พร้อม durable evidence: intended RED, focused API/DB GREEN 5 tests, backend suite 545 pass/0 skip/0 fail, frontend 54 pass, lint/types/build exit 0 และ focused browser 2 pass/0 fail โดย worker 1/retry 0 Browser evidence ครอบคลุม EMPLOYEE-only actual create → correction → reload และ existing staff schedule/history/clock-correction flow; persistence/audit evidence อ้าง record 9444 ของ employee 1334/account 772

Focused tests ตรวจ negative scope, missing link/grant, inactive/malformed grants, historical transfer branch, duplicate date, forged source/status, inconsistent clock/deduction, protected OLD rows, fresh reason และ locked create/correct มี assertions ว่า protected rows ไม่เปลี่ยน ไม่ใช่ตรวจเพียง HTTP status

### Issues

#### Critical (Must Fix)

- None.

#### Important (Should Fix)

- None.

#### Minor (Nice to Have)

- **[P3] Test-output noise** — `docs/superpowers/reports/16-uc07-self-attendance-evidence/task-1-browser-final.log:5`: Node เตือนว่า `NO_COLOR` ถูก ignore เพราะตั้ง `FORCE_COLOR` พร้อมกัน เป็น runner-environment noise ไม่กระทบผล 2 passed; หากปรับ test invocation ครั้งถัดไป ให้เลือกตั้ง color flag เพียงตัวเดียว ไม่ต้องรัน suite ซ้ำเพื่อ warning นี้

### Assessment

**Task quality: Approved.** Self policy อยู่ใน owning service, guard OLD row ก่อน merge และใช้ transaction/locks/audit เดิม New tests ตรวจพฤติกรรมกับ PostgreSQL จริงและ browser interaction จริง ไม่พบ application fix ที่ต้อง block checkpoint

### Review limits and next gate

รอบนี้เป็น independent static review และตรวจ consistency ของ frozen sources กับหลักฐานผู้ implement; ไม่ได้รัน suites หรือ browser ซ้ำ เพราะไม่เหลือ concrete uncertainty ที่ต้องใช้ execution เพิ่ม ผล PASS นี้ใช้กับ Task 1 เท่านั้น ไม่รับรอง acceptance ของทั้ง 20 use cases หรือ real external delivery/payment

Root สามารถไป checkpoint Task 1 ต่อได้ Final unfiltered 20-use-case/actor regression, broad final review และ integration/push ยังเป็น gate ของ root ตาม binding design
