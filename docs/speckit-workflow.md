# SpecKit Workflow for Haris Payroll

คู่มือนี้ใช้สำหรับเพื่อนที่ pull repository แล้วรับ work package จาก
`docs/two-week-three-person-plan.md`

## Skill คืออะไรและเรียกอย่างไร

Skill ของโปรเจกต์อยู่ใน `.agents/skills/` และถูก commit ไปกับ repository ดังนั้น
ทุกคนที่เปิด Codex จาก repository root จะใช้ skill ชุดเดียวกัน

เรียก skill โดยพิมพ์ชื่อขึ้นต้นด้วย `$` ในช่องแชต Codex:

```text
$speckit-specify
```

คำสั่ง `$speckit-*` เป็น prompt สำหรับ Codex ไม่ใช่ shell command ห้ามนำไปวางใน
Terminal หาก skill ไม่แสดง ให้ตรวจว่ากำลังเปิด Codex จาก repository root และลอง
พิมพ์ `$` หรือใช้ `/skills` เพื่อดูรายการ skill

## ก่อนเริ่มงานครั้งแรก

รันใน Terminal:

```bash
git pull --recurse-submodules
git submodule update --init --recursive
specify --version
```

จากนั้นอ่าน:

1. `AGENTS.md`
2. `docs/two-week-three-person-plan.md`
3. `docs/haris-payroll-product-backlog.md`
4. เอกสาร domain ที่ task อ้างถึง

เลือก work package เพียงหนึ่งรายการ เช่น `A1`, `B2`, หรือ `C2` และประกาศให้ทีมรู้
ก่อนเริ่ม เพื่อไม่ให้แก้ไฟล์ชนกัน

## ลำดับหลัก

```text
specify
  → clarify (เมื่อจำเป็น)
  → plan
  → tasks
  → analyze
  → implement
  → converge
  → implement อีกครั้งเมื่อ converge เพิ่ม task
```

เรียกทีละ skill และรอให้ขั้นนั้นเสร็จก่อนเสมอ

## Step 1 — สร้าง feature specification

พิมพ์ใน Codex:

```text
$speckit-specify

Implement work package A1 Authentication Foundation from
docs/two-week-three-person-plan.md. Follow AGENTS.md and the PostgreSQL domain
references. Implement only A1. Do not modify database schema or migrations.
```

เปลี่ยน `A1` และคำอธิบายให้ตรงกับ package ที่รับผิดชอบ

ผลที่ต้องได้:

```text
specs/<feature>/spec.md
specs/<feature>/checklists/requirements.md
```

ตรวจว่า spec มี user story, acceptance scenarios, functional requirements,
edge cases และสิ่งที่อยู่นอก scope ครบก่อนทำต่อ

## Step 2 — Clarify เฉพาะเมื่อจำเป็น

ใช้เมื่อ spec ยังมีคำถามที่เปลี่ยน business behavior เช่น ใครอนุมัติได้, ใครเห็นข้อมูล
หรือสถานะเปลี่ยนอย่างไร

```text
$speckit-clarify
```

ตอบคำถามให้ครบแล้วรอให้ Codex เขียนคำตอบกลับเข้า `spec.md`

ข้ามขั้นนี้ได้เมื่อไม่มี `NEEDS CLARIFICATION` และ acceptance criteria ชัดเจนแล้ว

## Step 3 — สร้าง technical plan

```text
$speckit-plan
```

ผลที่ต้องได้อย่างน้อย:

```text
specs/<feature>/plan.md
specs/<feature>/research.md
specs/<feature>/data-model.md
specs/<feature>/quickstart.md
```

ตรวจว่า plan ใช้ architecture ของ backend ตามนี้:

```text
route → controller → service → repository → database
```

Frontend task ต้องอ่าน `frontend/AGENTS.md` ก่อนแก้ไฟล์

## Step 4 — แตกเป็น executable tasks

```text
$speckit-tasks
```

ผลที่ต้องได้:

```text
specs/<feature>/tasks.md
```

ทุก task ควรมี ID, path ของไฟล์, dependency และวิธีตรวจรับ ห้ามเริ่ม implement หาก
task ยังใช้คำกว้าง เช่น “ทำ backend” หรือ “ทำ UI” โดยไม่ระบุผลลัพธ์

## Step 5 — ตรวจความสอดคล้องก่อนลงมือ

```text
$speckit-analyze
```

ควรใช้เสมอกับ authentication, authorization, leave, finance และ payroll

หาก report พบ CRITICAL/HIGH ให้แก้ `spec.md`, `plan.md` หรือ `tasks.md` ก่อน
ห้ามเริ่ม implement แล้วหวังแก้ความหมายทีหลัง

สำหรับ CRUD เล็กที่ไม่มี business decision สามารถข้ามขั้นนี้เพื่อประหยัดเวลาได้

## Step 6 — Implement

```text
$speckit-implement
```

ปล่อยให้ Codex ทำตาม `tasks.md` ตาม dependency อย่าส่ง feature ใหม่แทรกระหว่างรัน
หากต้องหยุด ให้บอกให้หยุดที่ task ID ปัจจุบันและบันทึกสถานะก่อน

หลัง implement ให้รันใน Terminal ตาม package ที่แก้

Backend:

```bash
cd backend
bun run typecheck
bun test
```

Frontend:

```bash
cd frontend
bun run lint
bun run build
```

Full stack:

```bash
docker compose up --build -d
docker compose ps
curl --fail http://127.0.0.1/healthz
```

## Step 7 — ตรวจหางานที่ยังสร้างไม่ครบ

หลัง implement และ tests รอบแรก ใช้:

```text
$speckit-converge
```

Skill นี้เปรียบเทียบ code กับ spec/plan/tasks และเพิ่มเฉพาะงานที่ยังขาดลงใน
`tasks.md`

หากมี task ใหม่ ให้รัน:

```text
$speckit-implement
```

ซ้ำอีกครั้ง แล้วรัน package checks ใหม่

## Optional skills

### Requirements checklist

ใช้เมื่ออยากให้คนอื่นตรวจคุณภาพ requirement ก่อน implement:

```text
$speckit-checklist
```

### Convert tasks to GitHub issues

ใช้หลัง `$speckit-tasks` เมื่อตกลงว่าจะบริหารงานผ่าน GitHub Issues:

```text
$speckit-taskstoissues
```

คำสั่งนี้สร้าง external state จึงต้องตกลงกับทีมก่อน ไม่ต้องใช้สำหรับ sprint นี้หาก
ทีมแบ่งงานผ่านเอกสารใน repository อยู่แล้ว

## Fast path สำหรับ sprint สองสัปดาห์

ใช้ชุดนี้เป็นค่าเริ่มต้น:

```text
$speckit-specify
$speckit-plan
$speckit-tasks
$speckit-implement
$speckit-converge
```

เพิ่ม `$speckit-clarify` เมื่อมี business decision ไม่ชัด และเพิ่ม
`$speckit-analyze` สำหรับ auth/leave/finance/payroll

## Copy-paste prompt สำหรับเริ่มงาน

```text
$speckit-specify

I am responsible for work package <PACKAGE_ID> from
docs/two-week-three-person-plan.md. Create a specification only for that package.
Follow AGENTS.md, preserve historical payroll data, enforce authorization on the
backend, and do not modify schema or migrations. Keep the implementation suitable
for the two-week demo scope: manual attendance, CSV exports, local attachments,
and a mock email adapter are acceptable. Exclude unrelated work packages.
```

## ก่อน handoff

- ทุก checkbox ใน `tasks.md` ที่ทำเสร็จต้องเป็น `[X]`
- Commit ใน `backend/` และ `frontend/` แยกตาม submodule
- ส่ง commit SHA, changed files, tests run, results และ limitations ให้ coordinator
- Feature owner ห้ามอัปเดต root submodule pointer เอง
- Coordinator รวม PR, อัปเดต pointers และรัน Compose validation รอบสุดท้าย
