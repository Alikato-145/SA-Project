# Branch Payment Groups and PromptPay QR Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox syntax for tracking.

**Goal:** HR/OWNER prepare frozen payroll payments by branch, view the three exclusive groups and generate phone-based PromptPay QR for nonmember transfers.

**Architecture:** Add the proposed payroll_payments under the payroll feature, with a dedicated feature-prefixed payment service/repository/transport/mapper. Reuse locked payroll facts and authorized employee/bank services. Prepare first; QR reads only frozen payment values. Task8 adds paid/cancel APIs to this same model.

**Tech Stack:** Bun/Elysia/Drizzle/PostgreSQL16, Next.js16/React19; local QR renderer and dev-only independent decoder if dependencies are needed.

**Spec:** `docs/superpowers/specs/2026-10-25-use-case-delivery-design.md`; primary technical references `docs/superpowers/plans/promptpay-primary-reference-notes.md`; preparation boundary `docs/superpowers/plans/delivery-follow-up-notes.md`.

## Global Constraints

- Accounting uses HR; only all-scope HR/OWNER prepare/read payment groups or QR. No employee/supervisor/manager finance permission.
- Locked payroll only; strictlypositive full net per employee, exact decimals. Zero net creates noQR/payment obligation and has no outstanding balance.
- Group priority: social-security member snapshot first; remaining employees split cash/transfer. No duplicate/missing employees.
- Freeze branch from locked payroll assignment, channel, recipient phone and bank destination/amount at preparation. Never join live destination into an old QR.
- QR generation/scanning never marks paid. No bank API, external QR service, actual money transfers or external email.
- One migration owner, additive migration, root SQL/reference review and disposable application only.

## Review Focus

- A later live phone/account/branch change must leave prepared recipient and amount unchanged.
- Two concurrent prepare calls must return one active payment per payroll record.
- Missing destination in one new row must not leave a partially prepared new batch.
- SS membership grouping must use frozen membership, not any contribution amount or current assignment flag.
- The actual displayed QR must decode to frozen phone/amount and a valid checksum, including cents and maximum representable amount.

### Task 1: Preparation, exclusive grouping and QR vertical slice

**Files:**
- Create payroll-owned `payroll-payment.schema.ts`, `payroll-payment.types.ts`, `payroll-payment.repository.ts`, `payroll-payment.service.ts`, `payroll-payment.controller.ts`, `payroll-payment.routes.ts`, `payroll-payment.mapper.ts` and focused tests; a small `payroll-payment.promptpay.ts` owns pure exact-string encoding/CRC.
- Modify export-only `backend/src/db/schema.ts`, shared enums/relations, `backend/src/app.ts` composition and error catalog. Add minimal internal employee/bank service capabilities needed to read destination under a supplied transaction, never foreign repositories.
- Create `frontend/components/payroll-payments.tsx`, API module under `frontend/lib/payroll/`, real `frontend/e2e/payroll-payments.e2e.ts`; integrate into existing payroll workspace using its selected period/branch instead of another unrelated shop selector where possible.
- Next serialized migration adds payroll_payments/status enum; root updates logical references and applies to disposable DB.

**Interfaces and schema:**
- Service methods `listPaymentGroups({actor,requestId,periodId,branchId?})`, `preparePayrollPayments({actor,requestId,periodId,branchId?})`, `getPromptpayQr({actor,requestId,paymentId})` return domain data, not HTTP/DTOs. Controllers invoke safe mappers/renderers.
- GET `/api/v1/payroll/periods/:period_id/payments` optionalbranch_id; POST same path plus `/prepare`; GET `/api/v1/payroll/payments/:payment_id/qr`. Follow existing route ID/response conventions. Mutation origin checks and backend finance authority required. QR response private/no-store, authorized SVG/PNG; no ciphertext/full bank number in JSON/audit.
- Existing employee service exposes getPaymentDestination({actor,requestId,employeeId}); add an internal transactional payment-read capability if needed to share the destination row lock with edits. Existing bank service may expose an authorized transaction-aware primary account domain snapshot. Keep controllers out of cross-feature orchestration.
- payroll_payments required: bigintid; payroll_record_id FK; branch_id_snapshot FK; payment_method existingenum; amount numeric12,2 >0; status payroll_payment_status prepared/paid/cancelled DEFAULTprepared; prepared_by_user_account_id FK andprepared_at; created_at/updated_at.
- Nullable: employee_bank_account_id FK; promptpay_phone_snapshot varchar10; bank_code_snapshot; account_holder_name_snapshot; account_number_ciphertext_snapshot; account_number_last4_snapshot. Cipher envelope already embeds key version. All FKs RESTRICT/CASCADE, no hard deletion.
- Lifecycle fields for Task8: paid_by_user_account_id/paid_at/reference_no; cancelled_by_user_account_id/cancelled_at/cancellation_reason. DB checks require matching actor/time/status; cancellation requires nonempty reason. Prepared has neither paid nor cancellation metadata; paid has no cancellation metadata; cancelled has no paid metadata. Snapshots remain immutable; do not add paid/cancel endpoints yet.
- Partial unique index payroll_record_id WHERE status IN(prepared,paid). Preserve cancelled history. Add period lookup index through payroll_record and branch/status index as needed; no group-total table.
- Cash has no destination snapshot. NonSStransfer requires explicitly registered phone; bank snapshot optional when present. SStransfer requires active-primary bank snapshot and has noQR. Validate complete bank tuple/canonical phone and one usable transfer destination. No automatic contactphone fallback.
- Preparation holds the existing payroll-input serialization through transaction, validates all new rows before writes, skips/reuses existing active snapshots idempotently. A batch containing a missing new destination returns actionable employee-specific errors and inserts no new payments. Group list may show unprepared preview clearly, using live channel only until prepared; after prepare use snapshots exclusively.
- Derive membership from immutable payroll_record snapshot, branch from its stored assignment; names for display may be current but are not recipient identity verification. Group partitions cover each locked record once, with zero-net rows labeled separately.
- Encode PromptPay mobile TLV from canonical snapshot phone and exact amount string; no floating-point payroll arithmetic. BOTtag29/AID A000000677010111/phonesubtag01, THB764, amount54, countryTH, CRC63. Research note has primary links. Use local `qrcode` rendering; `jsQR` dev-only independent decode is acceptable. Verify package/lockfile and container install if adding dependency; no public payload service.

- [x] Read AGENTS/Next docs and Task6 final interfaces. Write failing tests for partition3groups/zero, own-role denial, missingdestinations, immutable snapshots and duplicateprepare. Add exact-cent payload tests and independent CRC vector from the primary upstream references. Capture realRED.
- [x] Generate migration with partialunique/status/destination constraints and snapshot immutability protection; hand SQL to root beforeapply. No independent migration. Root verifies existing locked payroll/items unchanged.
- [x] Implement service/repository transaction and safe mapper/transport. Use service access for foreign features. Test real concurrent prepare gives one active row and a deliberate failure rolls back all new rows. Repeatedprepare after live recipient edit returns original snapshot.
- [x] Implement branch groups and clear prepare/QR controls in existing payroll UI. Show recipient phone/amount alongside QR and distinguish prepared from paid. Hide QR for SS/cash/zero/cancelled/paid, enforce same restriction backend. Register missing destinations through existing employee screen, not a generic bank-form rewrite.
- [x] Real browser HR and OWNER: mixed group fixtures in two branches, prepare, reload, change live recipient/contact then confirm oldQR unchanged. Extract actual rendered QR pixels to canvas and decode with independentdecoder; assert frozen recipient/amount/CRC. Verify employee/supervisor/manager denied via direct API, including QRURL. No bank app transfer or external account interaction.
- [x] Run focused/full migratedDB and frontend unit/lint/types sequentially with browser after root apply/ownership coordination. Report `docs/superpowers/reports/07-branch-groups-and-qr.md` with RED/GREEN, actual decode proof, source references, screenshots and limits. Fresh review before scoped commit; no rootgitlink/push/deploy.
