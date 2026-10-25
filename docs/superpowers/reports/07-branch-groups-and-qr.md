# Task 7 — branch payment preparation and phone PromptPay QR

Implemented on `codex/use-case-delivery`, from backend `1c98720` / frontend `c0975e5`. No commit, push, merge, deployment, production data change, external email, bank API or real transfer was performed. Source is handed back for a fresh root-owned review.

## Delivered behavior

All-scope HR/OWNER can list and prepare payments from a locked payroll period, optionally for one historical branch. Each locked record appears once: social-security membership snapshot has priority, then nonmembers split into cash/transfer. Zero-net records are labelled with no payment obligation or QR. Preparation snapshots full positive exact net, method, historical branch, registered recipient phone and optional bank destination. SS transfers require an active primary bank; nonmember transfers require an explicitly registered PromptPay phone. Contact phone is never a fallback.

Preparation uses the existing payroll-input advisory transaction lock. It reuses existing prepared/paid snapshots without updating or revalidating them against live destinations. It validates the new batch before inserting, and a later failure rolls back all new inserts. Later recipient, bank, branch or membership changes leave the prepared values unchanged. Public JSON exposes only authorized phone, bank metadata and last four digits; ciphertext/full bank numbers are absent. Preparation audits contain record IDs/count, no destination secrets.

The existing payroll workspace shows three groups, branch filtering, missing-destination links to the existing employee screen, explicit unprepared/prepared/zero labels, and recipient/amount beside the QR. QR is available only for prepared nonmember transfers. The authenticated SVG endpoint sets `Cache-Control: private, no-store`. Generating/scanning QR does not mark anything paid; Task 8 owns paid/cancel APIs.

## Schema coordination

The implementer generated only `backend/drizzle/0005_sloppy_rafael_vega.sql` and its Drizzle metadata. Root inspected/applied it only to `haris-payroll-verify` and updated the logical DBML/ORM/design references. Root's before/after files `/private/tmp/haris-task7-locked-before.txt` and `/private/tmp/haris-task7-locked-after.txt` confirm **138 pre-existing locked payroll records and 9,150 payroll items remained byte-for-byte equivalent by their recorded hashes**.

The additive table has positive exact amounts, destination tuple and lifecycle checks, RESTRICT/CASCADE FKs, one active prepared/paid payment per payroll record, branch/status lookup, immutable snapshots and preserved history. A trigger requires full locked payroll net and historical branch, member-specific destination rules, and guards future prepared→paid/cancelled transitions. No lifecycle endpoint exists in this task. The canonical catalog is 39 public tables, 25 enums, six migrations and 39 bigint primary keys.

## Verification and RED → GREEN

| Check | Evidence |
| --- | --- |
| PromptPay core | Three actual assertion failures on stubs (CRC, exact cents/phone TLV, invalid inputs), then 3 passed/14 assertions; extended to 5 passed/21 assertions with the author's published CRC vector and independent PNG decoding at one cent and maximum amount |
| Payment use cases | Four actual assertion failures on stubs (partition/zero, finance denial, missing destination, repeat/frozen snapshot), then 4 passed/12 assertions |
| Frontend API | Real request-path/method assertion failed on stub, then 1 passed/2 assertions |
| Actual PostgreSQL | Concurrent prepare, deliberate failure after insert, batch validation, idempotency, frozen phone/bank/branch/member facts, safe DTO, SQL guards, paid/cancelled QR denial and preserved cancelled/reprepared history; 1 passed/30 assertions (`/private/tmp/haris-task7-focused-db.log`) |
| Catalog regression | First full DB run 528 passed/2 failed/0 skipped: only stale expected 38 tables/24 enums/five migrations and 38 PKs. Updated expectations to the reviewed additive schema and added payment-guard catalog evidence; final full suite below |
| Browser | HR prepares branch 1; OWNER prepares branch 2, reloads/reopens same period; eight records partitioned once, six active prepared payments, two zero rows, zero paid rows. Employee/supervisor/branch manager each receive 403 for list, prepare and QR direct URLs |
| Mobile boundary | Maximum amount made the amount+QR action row overflow at 390px (real failing browser assertion). Added wrapping only to that action row; the same browser scenario passes without horizontal overflow |
| Quality | Full frontend unit suite 48 passed/0 failed/162 assertions across 17 files; lint and frontend/backend types pass; diff checks clean. Narrow design detector returns `[]` |

Final execution logs:

- `/private/tmp/haris-task7-full-db.log` — full serialized migrated-database regression (530 passed, 0 skipped, 0 failed, 115 files).
- `/private/tmp/haris-task7-browser-final.log` — two real browser tests, actual rendered image decode and authorization.
- `/private/tmp/haris-task7-frontend-tests.log` — 48 passed across all 17 frontend unit files.
- `/private/tmp/haris-task7-frontend-lint.log`, `/private/tmp/haris-task7-frontend-types.log`, `/private/tmp/haris-task7-backend-types.log`.
- `/private/tmp/haris-task7-design-detect.json` — `[]`.

## Independent displayed-image proof

The browser draws the actual authenticated SVG `<img>` onto a same-origin canvas, extracts RGBA pixels and uses separately pinned development-only `jsQR`; it imports neither the production payload builder nor its CRC. It checks recipient/amount and a separately implemented checksum. The HR image remains identical after changing live recipient to `0899999999`, contact phone to `0866666666`, reopening/reloading and repeating preparation.

Decoded recipient is **0812345678**. Exact rendered payloads:

```text
123.45:
00020101021229370016A0000006770101110113006681234567853037645406123.455802TH6304B5E2

9999999999.99:
00020101021229370016A00000067701011101130066812345678530376454139999999999.995802TH6304C7B8
```

These prove encoding/rendering and immutable preparation, not registration ownership, banking-app acceptance, transfer limits or settlement. The UI instructs the operator to verify the bank application's recipient name. No banking application or external payment account was opened.

## Visual evidence

Focused, readable screenshots:

- `docs/superpowers/reports/payment-groups-hr-panel.png`
- `docs/superpowers/reports/payment-groups-owner-panel.png`
- `docs/superpowers/reports/payment-groups-owner-qr-mobile.png`

Full-page originals are `/private/tmp/haris-task7-hr-groups-qr.png`, `/private/tmp/haris-task7-owner-groups-qr.png` and `/private/tmp/haris-task7-owner-groups-qr-mobile.png`. Focused panel captures temporarily hide the fixed application header only during screenshot stitching; product UI is unchanged. Desktop and 390px mobile were visually inspected.

## Primary technical references

Read the Bank of Thailand annex on tag 29, AID, phone subtag, THB, amount, country and CRC; checked the author's encoder and published test vectors. The implementation keeps monetary input as an exact decimal string instead of adopting the upstream number/toFixed amount API.

- [Bank of Thailand Thai QR Payment Standard, annex pp. 14–18](https://www.bot.or.th/content/dam/bot/documents/th/our-roles/payment-systems/about-payment-systems/ThaiQRCode_Payment_Standard.pdf)
- [PromptPay QR author implementation](https://github.com/dtinth/promptpay-qr/blob/master/index.js)
- [PromptPay QR author published tests](https://github.com/dtinth/promptpay-qr/blob/master/index.test.js)
- [Local qrcode renderer documentation](https://github.com/soldair/node-qrcode)
- [Independent jsQR decoder documentation](https://github.com/cozmo/jsQR)
- [EMVCo QR overview](https://www.emvco.com/emv-technologies/qr-codes/)

Pinned packages: backend runtime `qrcode@1.5.4`; backend development `@types/qrcode@1.5.6`, `jsqr@1.4.0`, `pngjs@7.0.0`; frontend development `jsqr@1.4.0`. Both package lockfiles are updated. The separate backend container dependency volume was refreshed with `bun install --frozen-lockfile`.

## Reproduction and limits

Use only the isolated verification stack (web 18083, PostgreSQL 55440, Mailpit 18025). The browser test needs a **fresh** fixture because payment and payroll history are deliberately immutable. From the repository root:

```sh
docker compose -p haris-payroll-verify -f compose.yaml -f compose.verify.yaml exec -T backend bun -e 'import { Pool } from "pg"; import { seedPaymentFixture } from "./src/features/payroll/payroll-payment.test-support"; const p=new Pool({connectionString:process.env.DATABASE_URL});console.log(JSON.stringify(await seedPaymentFixture(p)));await p.end();' > /private/tmp/haris-task7-browser-fixture.json
```

From `frontend/`:

```sh
PAYMENT_FIXTURE_FILE=/private/tmp/haris-task7-browser-fixture.json bunx playwright test e2e/payroll-payments.e2e.ts
bun test
bun run lint
bunx tsc --noEmit
```

From the repository root, after browser completion:

```sh
docker compose -p haris-payroll-verify -f compose.yaml -f compose.verify.yaml exec -T backend sh -c 'RELEASE_DISPOSABLE_DB=1 TEST_DATABASE_URL="$DATABASE_URL" bun run test:db'
```

From `backend/`, run `bun run typecheck`. Disposable tests preserve committed fixture/history rows; they never reset production data. The first browser attempt corrected a test assumption: the existing payroll workspace resets the selected shop on reload, so the test explicitly reopens its period. No product persistence feature was added for that unrelated behavior. Existing production login rate limits remain unchanged. Final focused UAT passed without changing the limiter.

## Fresh review fix 1 — reversed-period preview deadlock

The reviewer identified that `listPaymentGroups` held destination `FOR UPDATE` locks without acquiring the payroll-input advisory lock. The repository orders records by historical branch/code; after two employees swap branches, two periods can visit employee A/B in opposite order. Concurrent previews or preview/preparation could each hold one employee and wait for the other, resulting in PostgreSQL `40P01` and a finance request failure.

Added `payroll-payment.concurrency.integration.test.ts` using two dedicated PostgreSQL connections and actual October/November historical assignments with swapped branches. Dependency decoration pauses only after each real first destination read; a control connection observes overlap with `pg_blocking_pids`, then releases both requests. Before changing production code, **both list/list and list/prepare failed with actual `40P01: deadlock detected`** (`/private/tmp/haris-task7-fix1-red.log`, 0 passed/2 failed). This extends the original same-period concurrency test to opposite historical row orders.

The minimal fix acquires the existing `serializePayrollInputs` advisory lock at the beginning of the preview transaction, before `load` can lock any destination. Preparation retains all existing destination locks and snapshot behavior. This deliberately shares the current global serialization ceiling: simultaneous previews/prepare/input mutations may wait; no new lock abstraction or schema change was added.

After the change, both controlled scenarios complete and list/prepare produces exactly two payments. The amended concurrency tests plus existing payment service, actual DB snapshot/rollback and QR image tests pass **12 tests / 72 assertions, 0 failed**, across four files (`/private/tmp/haris-task7-fix1-green.log`). `bun run typecheck` and `git diff --check` pass (`/private/tmp/haris-task7-fix1-types.log`). The earlier 530-test full-DB and browser evidence above predates this focused fix; this round reran all four relevant payment test files, without unrelated frontend/schema changes. Source is frozen again for root's scoped re-review; no commit or external effects.

Commands, from the repository root and backend package respectively:

```sh
docker compose -p haris-payroll-verify -f compose.yaml -f compose.verify.yaml exec -T backend sh -c 'TEST_DATABASE_URL="$DATABASE_URL" bun test src/features/payroll/payroll-payment.concurrency.integration.test.ts src/features/payroll/payroll-payment.integration.test.ts src/features/payroll/payroll-payment.service.test.ts src/features/payroll/payroll-payment.promptpay.test.ts'
```

```sh
bun run typecheck
git diff --check
```

## Reviewed local checkpoint

Root final post-repair typecheck + full guarded disposable DB: **532 passed, 0 skipped, 0 failed across116files**, exit0 (`/private/tmp/haris-task7-final-db.log`). Scoped re-review marks P2 ADDRESSED, specPASS/qualityApproved. Local commits backend`1c360fa`, frontend`b10451c`; no push, merge, deployment or root gitlink update. Earlier530 count is pre-repair; two new concurrency tests explain532. Frontend unchanged by repair; existing48tests/types/lint and browser2 evidence retained.
