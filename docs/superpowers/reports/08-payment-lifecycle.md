# Task 8 — Manual payment lifecycle

Status: DONE_WITH_CONCERNS (execution note only), source frozen for independent spec/quality review. No commit, push, merge, deployment, migration or root gitlink update performed.

Base: backend `1c360fa`, frontend `b10451c`, both existing `codex/use-case-delivery` branches. Existing schema 0005 and the isolated `haris-payroll-verify` stack were consumed. No schema mismatch found.

## Delivered behavior

- HR/OWNER with all-branch authority can confirm a prepared payment or cancel its preparation. EMPLOYEE/SUPERVISOR/BRANCH_MANAGER are denied before lookup.
- Confirmation trims an optional reference (maximum 200 characters; empty becomes null). Cancellation trims a required reason (1–1000 characters). Same normalized retry returns the original row without UPDATE, preserving original actor/time and emitting no second domain transition. Changed details and incompatible transitions return stable `PAYMENT_STATE_CONFLICT` (409).
- Lifecycle transactions acquire `serializePayrollInputs` before a cancelled-inclusive SELECT FOR UPDATE, then perform a conditional prepared-state update and domain audit atomically. Existing active-only list/QR lookup and Task7 lock ordering remain intact. Separate `confirm_attempt` / `cancel_attempt` observations record attempts; canonical `.confirm.succeeded` / `.cancel.succeeded` records occur once per transition.
- Summary returns exact two-decimal strings from integer cents, historical assignment/branch snapshots, one locked record per employee, and zero-net employee counts without payable counts. Cancelled attempts do not inflate paid totals or joins. Safe cancelled history and paid actor/time/reference are mapped only at the controller boundary; ciphertext/full bank account data are excluded.
- Existing payment panel now shows branch/all-branch paid and outstanding totals, an explicit manual verification checkbox with employee/full amount/destination before confirmation, optional reference, cancellation reason, retained history and paid metadata. It explains that QR creation/scanning does not establish successful transfer and cancelling preparation cannot reverse a transfer or invalidate a downloaded QR. Paid/zero/history rows have no decision controls; cancelled preparation can be deliberately re-prepared via the existing prepare action.
- Added one shared Thai error-message mapping for the new conflict code; this small extra file is needed to explain the business reason in the UI.

## Verification

All database checks used only `postgresql://postgres:postgres@localhost:55440/haris_payroll`; website `http://localhost:18083`, local Mailpit unchanged. Production login limits were unchanged. No banking app, transfer or external email was used.

| Check | Command (package directory) | Result |
|---|---|---|
| Backend RED | `TEST_DATABASE_URL=… bun test src/features/payroll/payroll-payment.lifecycle.integration.test.ts` | Failed because `getPaymentSummary` was absent |
| Frontend RED | `bun test lib/payroll/payroll-payment-api.test.ts` | Failed because `confirm` was absent; later conflict-localization RED also captured |
| Browser RED | `E2E_BASE_URL=http://localhost:18083 bun run test:e2e e2e/payroll-payment-lifecycle.e2e.ts` | Missing summary UI before implementation |
| Focused Task7+8 regression | four payment service/integration/concurrency files | 8 passed, 0 failed, 103 assertions before final added assertions |
| Final lifecycle integration | `TEST_DATABASE_URL=… bun test src/features/payroll/payroll-payment.lifecycle.integration.test.ts` | 1 passed, 0 failed, 53 assertions |
| Backend types | `bun run typecheck` | Passed |
| Final guarded full DB suite | `RELEASE_DISPOSABLE_DB=1 DATABASE_URL=… TEST_DATABASE_URL=… bun run test:db` | 533 passed, 0 skipped, 0 failed across 117 files |
| Final frontend suite | `bun test` | 50 passed, 0 failed, 166 assertions across 17 files |
| Frontend lint/types | `bun run lint`; `bun run node_modules/typescript/bin/tsc --noEmit` | Passed |
| Final real browser | focused lifecycle command above | 1 passed, 15.1 seconds |
| UI mechanical detector | `impeccable detect --json frontend/components/payroll-payments.tsx` | `[]` |
| Diff whitespace | `git diff --check` in each submodule | Passed |

Actual migrated DB checks cover pay/pay racing (one transition event), pay/cancel racing (exactly one winner and one event), audit failure after update rolling back status/metadata, repeat decisions preserving original actor/time, changed-details conflicts, validation/404, direct route cookie-origin/ID protection, unauthorized roles, cancelled/paid QR denial, reprepare with a fresh destination and retained cancelled snapshot, and historical branch totals after a later assignment transfer.

Hand-checked exact fixture: branch A `100.01 + 50.02 + 0.00`, branch B `25.00`: 4 employees, 3 payable; initial `175.03 / 0.00 / 175.03`; first payment leaves `75.02`; cancellation leaves `75.02`; reprepare/payment of `50.02` completes branch A and leaves all-branch `25.00`.

Final browser fixture period **415** persisted: payment **257** paid `100.01` by HR account 2 with `hr-receipt`; **258** retained cancelled `50.02` by HR with `HR correction`; **259** retained cancelled `25.00` by OWNER account 1 with `OWNER correction`; replacement **260** paid `50.02` by OWNER. Browser reloads verify history/status, no duplicate confirmation control, branch completion, `175.03 / 150.03 / 25.00`, and direct 403 for all three prohibited roles.

## Evidence

Retained under [payment-lifecycle-evidence](payment-lifecycle-evidence/): RED/final logs, browser fixture persistence JSON and readable panel screenshots:

- [Confirmation desktop](payment-lifecycle-evidence/haris-task8-confirm-desktop.png)
- [Confirmation and wrapped controls at 390px](payment-lifecycle-evidence/haris-task8-confirm-mobile.png)
- [HR paid/cancelled history](payment-lifecycle-evidence/haris-task8-hr-lifecycle.png)
- [OWNER totals/history desktop](payment-lifecycle-evidence/haris-task8-owner-lifecycle.png)
- [OWNER totals/history at 390px](payment-lifecycle-evidence/haris-task8-owner-mobile.png)

Screenshots hide the existing sticky header, skip link and development overlay only during capture, so panel content remains readable. Both mobile captures were checked for horizontal overflow; none occurred.

## Limits and execution notes

- Synthetic local payment decisions only: these records represent manual verification, not bank confirmation. No production build or broad unrelated browser suite was requested/run for this slice.
- Initial sandbox localhost access required escalation. An early browser check then failed because its expected text omitted the existing `฿` formatter; only the test expectation changed. That failed selector-only browser wait overlapped an initial full DB invocation before any browser payment mutation; the final browser and final guarded DB run were completed sequentially, with no overlapping payment-mutating checks.
- Existing Next.js smooth-scroll and Playwright `NO_COLOR`/`FORCE_COLOR` development warnings remain; no runtime/payment errors in the passing focused run. No unresolved product/schema concern identified.

## Reviewed local checkpoint

Independent Task8 spec/quality review approved with no Critical/Important findings; final full-UC UAT remains separate. Local commits backend`2d8f662`, frontend`3837e84`. Root read final durable logs (533DB/0skip0fail,50frontend/166asserts) and inspected mobile confirmation. No schema, push, merge, deploy or root gitlink update. Environment-only color warning stays tracked for finalUAT invocation.
