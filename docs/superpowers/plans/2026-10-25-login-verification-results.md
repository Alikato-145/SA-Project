# Subtask 2 Login Verification Results

วันที่ 25 ตุลาคม 2026

## ข้อกำหนดที่ยืนยันแล้ว

- ฝ่ายบัญชีใช้ HR grant เดิม ไม่มี ACCOUNTING role ใหม่
- รายงานสรุปเจ้าหนี้คือยอดเงินเดือนที่ร้านต้องจ่ายให้พนักงาน ทั้งยอดรวมและรายบุคคล ใช้ผลเงินเดือนชุดเดียวกับสลิป ไม่แปลง PDF กลับเป็นข้อมูล
- PromptPay ใช้เบอร์โทรศัพท์รับเงินเป็นหลัก ตาม design ที่อัปเดตแล้ว

## สถานะ

Subtask 1: ยืนยันข้อกำหนดธุรกิจและจัดทำ design แล้ว

Subtask 2: ชุดทดสอบแยกพร้อมใช้งาน; Login ห้า role และ browser scenarios ที่เลือกผ่าน แต่พบข้อจำกัดการเพิกถอน token หลัง Logout จึงบันทึกเป็น finding ที่ต้องจัดการก่อนรับรอง session handling ครบ ยังไม่อ้างว่าผ่านทุกเงื่อนไขความปลอดภัยหรือทุก Use Case ของโครงการ

## Runtime และขอบเขตข้อมูล

เปิด Docker Desktop ที่ติดตั้งอยู่และใช้ project `haris-payroll-verify` เดิมเท่านั้น ไม่ stop/reset project อื่น ไม่เปลี่ยน application source, schema หรือ migrations

- Web: `http://localhost:18083`
- PostgreSQL host port: `55440`
- Mailpit: `http://localhost:18025`; อีเมลทดสอบเข้า local sink ไม่ได้ส่งออกไปผู้รับภายนอก
- Fixture: เดือนกันยายน 2026; สองสาขา แยกแผนกและพนักงาน ใช้ guarded release fixture
- รัน fixture สองครั้งสำเร็จโดย script เดิม ไม่ใช้ฐานพัฒนา/production แทน
- `/login` HTTP 200, `/healthz` HTTP 200, `/api/v1/auth/me` ไม่มี cookie HTTP 401
- มี project อื่นเริ่มตาม restart policy ของ Docker หลังเปิด daemon; ไม่ได้สั่งจัดการ project นั้น

## ผลตรวจที่รันจริง

| Check | ผล |
|---|---|
| Backend auth/lockout/authorization focused checks | 34 pass / 0 fail / 4 files |
| Frontend auth API/route policy focused checks | 9 pass / 0 fail / 2 files |
| `VERIFY_BROWSER=0 sh scripts/verify.sh` | exit 0 |
| Backend disposable database suite ผ่าน script ข้างต้น | 477 pass / 0 skip / 0 fail / 103 files |
| Frontend unit suite ผ่าน verification container | 45 pass / 0 fail / 16 files |
| Backend typecheck, frontend lint/TypeScript | ผ่านใน verification script |
| Chromium browser scenarios ที่เลือก | 8 pass / 0 fail; 24.3 seconds |
| Live single-role Login/me check ห้า account | ผ่าน role code/scope ตรงและมี grant เดียวทุกบัญชี; employee มี employee link |
| Logout cookie expiration | HTTP 200 และ Set-Cookie หมดอายุครบห้าบัญชี |
| Replay token เดิมหลัง Logout | **ไม่ผ่าน: /auth/me ยัง HTTP 200 ครบห้าบัญชี ขณะที่คาดว่าจะเป็น 401 หากมี server-side revocation** |

จำนวน focused tests เป็นส่วนย่อยที่ซ้ำอยู่ใน full suites ไม่ให้นำจำนวนมาบวกแล้วอ้างว่าเป็น unique tests เพิ่ม

## Browser scenarios ที่ผ่าน

1. `fresh organization completes onboarding, evidence, approval, OT, payroll, PDF, SMTP and exports` — มี account ไม่มี grant และกำหนด EMPLOYEE ภายหลังใน journey นี้ หลายขั้นธุรกิจใช้ page.request จึงไม่ใช่หลักฐานกดทุกปุ่มของทุก UC
2. `new account receives named branch scope, changes password and loses access when disabled`
3. `mobile keyboard navigation, error recovery and logout keep session state honest`
4. Employee login + own scope และปฏิเสธข้อมูลคนอื่น
5. Supervisor login + department scope และปฏิเสธนอกขอบเขต
6. Branch manager login + branch scope และปฏิเสธนอกขอบเขต
7. HR login + all scope — ใช้แทน actor ฝ่ายบัญชีตามข้อกำหนดที่ยืนยันแล้ว
8. Owner login + all scope

## บัญชีทดสอบและ grant ที่ตรวจจาก API จริง

| Username fixture | Role | Scope | Grant count |
|---|---|---|---|
| employee | EMPLOYEE | self | 1 |
| supervisor | SUPERVISOR | department | 1 |
| branch_manager | BRANCH_MANAGER | branch | 1 |
| hr | HR | all | 1 |
| admin | OWNER | all | 1 |

ไม่มีการใช้ HR/OWNER grant ที่พ่วงกับ scoped account ไปพิสูจน์สิทธิ์ของ manager/employee ในตารางนี้ ไม่บันทึก cookie, JWT, password จริง หรือข้อมูลบัญชีธนาคารลงรายงาน

## Finding AUTH-01 Logout ไม่เพิกถอน JWT เดิม

ระดับ: ต้องจัดการก่อนรับรอง server-side logout/session revocation

การทำซ้ำกับบัญชี fixture ที่ได้รับอนุญาต:

1. Login สำเร็จและเก็บ session cookie ไว้ในหน่วยความจำของ verification probe
2. GET `/api/v1/auth/me` ด้วย cookie นั้น ได้ 200
3. POST `/api/v1/auth/logout` ด้วย Origin และ JSON Content-Type ตาม frontend contract ได้ 200 และ cookie tombstone
4. ส่ง GET `/api/v1/auth/me` โดยแนบ cookie ก่อน Logout ที่คัดลอกเก็บไว้ ได้ **200** แม้ browser ปกติล้าง cookie ไปแล้ว
5. ไม่แนบ cookie ได้ 401 ตามปกติ และ browser logout test ผ่าน เพราะ browser ใช้ cookie jar ที่ถูกล้างแล้ว

ยืนยันครบทั้งห้า role โดยไม่พิมพ์ token ออกมา Script จะ exit 1 เมื่อพบ replay หลัง Logout สำเร็จ

สาเหตุจาก executable source:

- `backend/src/features/user-account/user-account.service.ts:324` logout verify claims แล้วบันทึก observed read ไม่มีการ revoke token หรือแก้ session state
- `backend/src/features/user-account/user-account.routes.ts:73` ส่ง cookie tombstone ให้ browser
- `backend/src/core/auth/session-token.ts:51` verify ตรวจลายเซ็น/claims/เวลาหมดอายุ โดยไม่มี persisted session revocation
- `backend/src/core/auth/request-authenticator.ts:36` ตรวจ token และ active account/grants ปัจจุบัน การ disable account จึงตัดสิทธิ์ได้ แต่การ logout อย่างเดียวไม่เปลี่ยน account state
- `/auth/me` เรียก token verification และ account projection เช่นกัน

ผลกระทบ: token ที่ถูกคัดลอกก่อน Logout ยังนำกลับมาใช้ได้ขณะ token ไม่หมดอายุและ account ยังใช้งานได้ ไม่ใช่การเปิดเผย token ผ่านหน้าเว็บ และไม่ใช่การกล่าวว่า login/logout UI ไม่ทำงาน

งานแก้ควรมี failing regression สำหรับ `/auth/me` และ business API หลัง logout โดยใช้ cookie เดิม, concurrent sessions ตามนโยบายที่เลือก และ persistence หลัง restart ห้ามใช้ in-memory blacklist อย่างเดียวเป็นคำตอบสุดท้าย ควรกำหนด persisted session strategy ให้สอดคล้องกับ schema owner ก่อน migration และทดสอบ disable/password changes ร่วมด้วย ไม่แก้โดยลดความคาดหวังของ probe ให้รับ HTTP 200

## คำสั่งทำซ้ำ

จาก repo root:

```sh
VERIFY_BROWSER=0 sh scripts/verify.sh
```

จาก frontend:

```sh
E2E_BASE_URL=http://localhost:18083 bun run test:e2e --grep 'enforces own|new account receives|mobile keyboard|fresh organization'
```

Live actor/replay probe สำหรับรอบนี้อยู่ที่ `tmp/use-case-delivery/check-login-actors.ts` และใช้เฉพาะ synthetic fixture ของ localhost โครงสร้าง DTO อ้างอิง `data.account.employee.id`; Logout ใช้ JSON Content-Type เดียวกับ frontend

## หลักฐานในเครื่อง

- `/private/tmp/haris-subtask2-stack.log`
- `/private/tmp/haris-subtask2-browser.log`
- `/private/tmp/haris-subtask2-auth.log`
- `/private/tmp/haris-subtask2-auth-ui.log`
- `/private/tmp/haris-subtask2-actors.log` — expected failure AUTH-01
- Browser report: `frontend/playwright-report/index.html`; report นี้ใช้สำหรับ 8 scenarios ที่เลือกรอบนี้

## งานถัดไป

- ระบุ AUTH-01 ในแผนก่อนปิด Subtask 2 แบบสมบูรณ์ และเลือก persisted session invalidation strategy ตามนโยบาย logout
- เตรียม scoped employee write implementation สำหรับ Subtask 3 ตาม design โดยไม่ให้ HR grant แก่ manager เพื่อข้าม scope
- ภาพ ERD แบบย่อยังใช้ entity หลักที่ตกลงกันได้ รายละเอียด infrastructure session หากเพิ่มภายหลังแยกอยู่ใน schema เต็มได้

## Final verification after AUTH-01 fix — 25 October 2026

AUTH-01 fixed; fresh independent review found no actionable issues. Disposable migrated DB suite **484 pass / 0 skip / 0 fail,106 files** and backend typecheck passed. Frontend45 tests, lint and typecheck passed. Five single-role live probes rejected logged-out tokens with401. Real backend restart preserved revocation401 and the independent session remained200. DBML and schema reference documents include the additive session table.

Permanent AUTH-01 browser regressions:2 passed. Full browser run:22 passed/1 failed due production nginx Login rate limiting (10r/m,burst20), not wrong credentials or authorization. That failed branch-manager scope test subsequently passed individually1/1 after rate recovery. This is aggregate coverage, not a claim of one all-green23-case run. Test pacing remains tracked for final UAT. Logs: `/private/tmp/haris-auth01-db-green.log`, `/private/tmp/haris-auth01-browser-final.log`, `/private/tmp/haris-auth01-browser-rate-recheck.log`, `/private/tmp/haris-auth01-restart.log`.
