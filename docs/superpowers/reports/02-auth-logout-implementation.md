# Subtask 2 — AUTH-01 persistent logout revocation

วันที่ 25 ตุลาคม 2026; implementation ใน backend branch `codex/use-case-delivery` ไม่มี commit/push และไม่มีการเปลี่ยน submodule pointer

## ผลและ root cause

Logout เดิมตรวจ JWT แล้วบันทึก audit ก่อนส่ง cookie tombstone เท่านั้น ไม่มี persisted revocation; `/auth/me`, change-password และ business authenticator จึงยังรับ token ที่คัดลอกไว้ได้

แก้ให้ logout บันทึก SHA-256 fingerprint ของ token ปัจจุบันใน PostgreSQL ก่อนตอบสำเร็จ และตรวจ fingerprint ใน `/auth/me`, change-password, request authenticator และ auth macro ทุกครั้ง ไม่มี in-memory blacklist ใน production, ไม่มีการเก็บ/log raw JWT และไม่ใช้การ disable account แทน logout

เพิ่ม random UUID `jti` ใน JWT ที่ออกใหม่ เพื่อให้ login อิสระของ account เดียวกันในวินาทีเดียวเป็นคนละ token การ logout จึงไม่ตัด session อื่น Existing JWT ที่ยังไม่มี `jti` ยังคงตรวจลายเซ็น/อายุได้และ revoke ด้วย fingerprint ได้ตามเดิม หาก login เก่าบังเอิญใช้ JWT bytes เดียวกัน จะถือเป็น bearer token เดียวกันและถูก revoke พร้อมกัน; session ใหม่ไม่เกิดการชนแบบนี้

พบ edge case เพิ่มระหว่างตรวจ: JOSE ยอมรับ signature ที่เปลี่ยน unused base64url bits แล้วยังแทน signature bytes เดิม การ hash raw spelling อย่างเดียวเปิดทางหลบ blacklist ได้ จึง normalize signature เป็น canonical base64url ก่อนคำนวณ SHA-256 พร้อม regression ที่พิสูจน์ RED ก่อนแก้

## Schema และ migration

เพิ่มใน feature-owned `src/features/user-account/user-account.schema.ts`:

| Field | PostgreSQL |
|---|---|
| `id` | bigint identity primary key |
| `user_account_id` | bigint NOT NULL, FK user_accounts.id, DELETE RESTRICT / UPDATE CASCADE |
| `token_hash` | varchar(64) NOT NULL, lowercase SHA-256 CHECK `^[0-9a-f]{64}$` |
| `expires_at` | timestamp with time zone NOT NULL |
| `revoked_at` | timestamp with time zone NOT NULL DEFAULT now() |

ตาราง `revoked_session_tokens`; unique index `revoked_session_tokens_hash_uidx(token_hash)` และ index `revoked_session_tokens_expiry_idx(expires_at)` ไม่มี enum ใหม่ ไม่มีการแก้ table เดิม

Generated migration: `backend/drizzle/0001_auth_session_revocation.sql` พร้อม `backend/drizzle/meta/0001_snapshot.json` และ `_journal.json` ใช้ `bun run db:generate --name auth_session_revocation` ไม่ใช้ db:push

Catalog expectation เปลี่ยนเฉพาะ table count / bigint PK count จาก 36 เป็น 37 และ migration count จาก 1 เป็น 2; enum count คง 22 และ history protection checks คงเดิม ผู้ implement ไม่ apply migration หรือเชื่อมฐาน production; root เป็นผู้ apply เฉพาะ disposable verification project และจัดการ DBML/reference parity

## RED / GREEN evidence

ก่อน production changes:

- `/private/tmp/auth-logout-red.log`: 21 pass / 3 fail — replay `/auth/me` ไม่ถูกปฏิเสธ, auth macro รับ revoked token และ login สองครั้งในวินาทีเดียวให้ JWT เดียวกัน
- `/private/tmp/auth-request-red.log`: 0 pass / 1 fail — business authenticator resolve สำเร็จทั้งที่ token ถูก revoke
- `/private/tmp/auth-signature-red.log`: 1 pass / 1 fail — equivalent signature spelling ยังไม่ถูกนับว่า revoked หลังเพิ่ม fingerprint persistence แล้ว

หลัง implementation:

- Focused auth/service checks: 25 pass / 0 fail ใน 4 files (ก่อนเพิ่ม session-service checks)
- Session-service checks: 2 pass / 0 fail; database reconnect test skip เมื่อไม่มี TEST_DATABASE_URL
- `bun run typecheck`: exit 0
- `env -u TEST_DATABASE_URL bun test`: **458 pass / 28 skip / 0 fail, 486 tests / 106 files**, exit 0; log `/private/tmp/auth-logout-full-green.log`
- `git diff --check`: exit 0

28 skips คือ opt-in disposable database tests เดิม 27 tests และ AUTH-01 reconnect test ใหม่ 1 test ไม่ได้อ้างว่า local round นี้พิสูจน์ database integration ผ่านแล้ว

Root รายงานหลัง apply disposable migration: live replay probe ครบห้า role ได้ 401 และ permanent browser regressions 2 tests ผ่าน (logout replay + independent session/business route) ส่วน full migrated database suite, browser regression ทั้งหมด และ process-restart probe ให้ root บันทึกผลจากการรันจริงเพิ่มเติม

## Test coverage ที่เพิ่ม

- Logout ซ้ำเป็น idempotent, token เดิมอ่าน actor/change password ไม่ได้ และ password ไม่เปลี่ยน
- Auth macro กับ business authenticator ปฏิเสธ revoked cookie แม้ account ยัง active
- Independent same-second logins ใช้งานแยกกัน
- Session service เก็บเฉพาะ fingerprint/account/expiry และ service instance ใหม่เห็น revocation เดิม
- Equivalent base64url signature spellings ใช้หลบ revocation ไม่ได้
- Opt-in DB integration ใช้ explicit TEST_DATABASE_URL ผ่าน connection ของ test เอง: concurrent duplicate revocation สร้างหนึ่ง row, ปิด connection แรกแล้วสร้าง repository/service/authenticator ใหม่, replay ถูกปฏิเสธ, independent session ยังผ่าน, disable account ตัด independent session ด้วย
- Existing lockout, disablement, role reload และ password checks ยังคงผ่านใน full suite

## Changed files

Backend implementation/composition:

- `src/app.ts`
- `src/core/auth/auth.plugin.ts`
- `src/core/auth/auth.types.ts`
- `src/core/auth/request-authenticator.ts`
- `src/core/auth/session-jwt-codec.ts`
- `src/core/auth/session-token.ts`
- `src/features/user-account/user-account.repository.ts`
- `src/features/user-account/user-account.schema.ts`
- `src/features/user-account/user-account.service.ts`
- `src/features/user-account/user-account.session-service.ts` (new)

Tests:

- `src/core/auth/auth.plugin.test.ts`
- `src/core/auth/request-authenticator.test.ts` (new)
- `src/core/auth/session-token.test.ts`
- `src/core/db/database.integration.test.ts`
- `src/features/user-account/user-account.service.test.ts`
- `src/features/user-account/user-account.session-service.test.ts` (new)
- `src/features/user-account/user-account.session.integration.test.ts` (new)

Migration artifacts: `drizzle/0001_auth_session_revocation.sql`, `drizzle/meta/0001_snapshot.json`, `drizzle/meta/_journal.json`

## ข้อจำกัดที่เกี่ยวข้อง

ต้อง migrate ก่อนนำ backend version นี้ขึ้น runtime เพราะ authenticated requests ตรวจ persisted revocation โดยไม่ fallback ให้ผ่านเมื่อ storage หาย การเชื่อมต่อ revocation storage ล้มเหลวจึง fail closed

ยังไม่มี cleanup job ลบ fingerprint หลัง token หมดอายุ; index expiry เตรียมให้ retention maintenance ภายหลัง ข้อมูลที่ค้างไม่มี raw JWT และไม่ทำให้ expired token กลับมาใช้ได้ ไม่เพิ่ม session admin/global logout หรือเปลี่ยน password-session policy นอกขอบเขต AUTH-01

## Final verification after AUTH-01 fix — 25 October 2026

AUTH-01 fixed; fresh independent review found no actionable issues. Disposable migrated DB suite **484 pass / 0 skip / 0 fail,106 files** and backend typecheck passed. Frontend45 tests, lint and typecheck passed. Five single-role live probes rejected logged-out tokens with401. Real backend restart preserved revocation401 and the independent session remained200. DBML and schema reference documents include the additive session table.

Permanent AUTH-01 browser regressions:2 passed. Full browser run:22 passed/1 failed due production nginx Login rate limiting (10r/m,burst20), not wrong credentials or authorization. That failed branch-manager scope test subsequently passed individually1/1 after rate recovery. This is aggregate coverage, not a claim of one all-green23-case run. Test pacing remains tracked for final UAT. Logs: `/private/tmp/haris-auth01-db-green.log`, `/private/tmp/haris-auth01-browser-final.log`, `/private/tmp/haris-auth01-browser-rate-recheck.log`, `/private/tmp/haris-auth01-restart.log`.
