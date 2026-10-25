# UC08 quota precheck — 26 October 2026

Scope: Task2 of `docs/superpowers/specs/2026-10-26-use-case-20-alignment-design.md`; `.superpowers/sdd/2026-10-26-use-case-20-alignment/task-2-brief.md`. No schema/migration/API-contract change. Task1 attendance changes preserved. All database/browser work used existing disposable **haris-payroll-verify** only (HTTP18083, PostgreSQL55440, Mailpit18025); no production database or external delivery.

## Root cause and implementation

`submitLeave` and `updateLeave` previously checked overlaps/active type, then persisted requests and dates directly. Only `approveLeave` validated quota. A request could therefore be created or edited even when the requested year had no available entitlement.

The service now calls one shared quota guard after the existing employee advisory transaction lock and active-type check, before any request/day/action writes. It counts actual inclusive dates separately by year and reads each quota through the existing `findQuota` transaction method (`SELECT ... FOR UPDATE`). Numeric(8,2) strings are compared in exact integer hundredths of a day. No new reservation, counters, repository methods, schema or dependencies.

Policy, explicitly confirmed by root against existing approval behavior:

- `quotaType=none`: no quota row required.
- A quota-bearing type always requires an existing unfrozen quota row for **each** requested year. Missing rows return `LEAVE_QUOTA_EXCEEDED` (HTTP422); frozen rows return `LEAVE_QUOTA_FROZEN` (HTTP409).
- `allowExceed=false`: used days + requested days must be within that year's entitlement.
- `allowExceed=true`: only the entitlement cap is waived. Missing/frozen quotas still reject. Existing approval behavior consumes available full days and marks excess unpaid/deductible.
- Submission/edit does not reserve or consume quota. Several nonoverlapping pending requests can pass against the same balance; approval must still recheck under its existing transaction/locks. Approval implementation and supervisor3-day/manager-any-day boundaries were unchanged.

The existing leave page now explains these pending-request and excess-policy limits. The frontend API error localizer gained quota-specific Thai reasons so rejection explains the business condition. Other error codes/status mappings are unchanged.

## Observed RED and failures retained

1. Service RED, before production edits: **14 pass / 11 fail**, including insufficient/missing/frozen/exhausted and second-year submit/edit rejection. The existing service proceeded to request/day/action writes rather than reject.
2. Real application/PostgreSQL RED, before production edits: **2 pass / 8 fail**. Invalid submissions returned HTTP200 and pending edits succeeded; excess/approval concurrency characterization cases already passed. Tests use real authenticated EMPLOYEE/OWNER roles and fresh synthetic scoped fixtures; JWT construction avoids irrelevant network login limits in integration tests.
3. First realDB GREEN attempt: **7 pass / 3 fail** because the new tests incorrectly expected HTTP422 for frozen quota; the established boundary returns409. Corrected only test expectations; production policy/status unchanged. Raw log retained as `database-green-initial-status-expectation-failure.log`.
4. First browser run: **1 pass / 1 fail**. Existing approval boundary passed; employee rejection422 was correct but the new UI assertion expected backend English text. Investigation found the frontend deliberately replaces unmapped English errors with a generic Thai message. New localization test observed **11 pass / 1 fail** (generic Thai received instead of business reason), then two Thai mappings were added. Failed browser log, screenshots, trace and HTML report retained under `browser-first-*`; no automatic retry.

Service and integration tests were written and observed failing before the guard. Two initial shell invocations used an incorrect package-relative filename and did not execute intended tests; these were corrected before RED runs. No product changes resulted from those command mistakes.

## Verification commands and results

Commands are from the repository root unless a package is specified. Docker executions target the already-existing named verification backend; its `DATABASE_URL` resolves only the verification Compose network database.

| Check | Command | Result |
|---|---|---|
| Service RED/GREEN (backend/) | `bun test src/features/leave/leave.test.ts` | RED14pass/11fail → GREEN25pass/0fail,57 assertions |
| RealDB RED/GREEN | `docker exec haris-payroll-verify-backend-1 sh -c 'TEST_DATABASE_URL="$DATABASE_URL" RELEASE_DISPOSABLE_DB=1 bun test src/features/leave/leave.quota.integration.test.ts'` | RED2pass/8fail → GREEN10pass/0fail,50 assertions |
| Full backend types + migrated DB suite | `docker exec haris-payroll-verify-backend-1 sh -ec 'bun run typecheck; export TEST_DATABASE_URL="$DATABASE_URL" RELEASE_DISPOSABLE_DB=1; bun run test:db'` | types exit0;568pass/0skip/0fail,121 files |
| Frontend localization RED (frontend/) | `bun test lib/api/client.test.ts` |11pass/1fail |
| Frontend unit final (frontend/) | `bun test` |55pass/0fail,177 assertions,19files |
| Frontend lint final (frontend/) | `bun run lint` |exit0 |
| Frontend types final (frontend/) | `bun run node_modules/typescript/bin/tsc --noEmit` |exit0 |
| Frontend build final (frontend/) | `bun run build` |exit0,22 pages generated |
| Whitespace | `git -C backend diff --check`; `git -C frontend diff --check` |exit0 |

Final focused browser command (frontend/), with application/scripts frozen throughout both invocations, fresh scoped fixtures, workers1/retries0 and production login limiter unchanged:

```sh
env -u NO_COLOR -u FORCE_COLOR E2E_BASE_URL=http://localhost:18083 E2E_EVIDENCE_DIR=/Users/manus/University/SA-Project/docs/superpowers/reports/17-uc08-quota-precheck-evidence PLAYWRIGHT_HTML_OUTPUT_DIR=/Users/manus/University/SA-Project/docs/superpowers/reports/17-uc08-quota-precheck-evidence/browser-html bun run test:e2e e2e/leave-quota.e2e.ts e2e/approval.e2e.ts --workers=1 --retries=0 --output=/Users/manus/University/SA-Project/docs/superpowers/reports/17-uc08-quota-precheck-evidence/browser-artifacts
```

Final focused browser result: **2 pass / 0 fail in32.6s** (existing approval17.1s, new employee quota15.0s). Both browser invocations cleared `NO_COLOR` and `FORCE_COLOR` at entry; final log contains no color-conflict warning. Sources stayed frozen during the entire invocation.

## Actual browser persistence and visual QA

Fresh EMPLOYEE-only fixture: **employee1400/account803/type293/year2038/request297**. The UI rejected a2-day request against1day entitlement with the Thai business reason, API listing remained empty, then accepted1day. Reload recovered the pending request. A2-day edit returned422, left the submitted history unchanged, and reload still returned exactly one original1-day request. The employee quota remained0.00 before approval. Owner UI approved the same request; employee reload showed approved and used_days1.00.

Independent PostgreSQL reads confirm exactly one request for employee1400, request297 approved for2038-02-01, one paid/non-deductible day with quota_consumed1.00, quota entitled/used1.00, and exactly submitted(actor803)/approved(actor1) approval actions. Audit contains only successful submit/approve records for that request, with the same actors. See `browser-persistence-confirmed.log`. Two preliminary read-only evidence queries compared varchar audit record_id with an integer and failed at that final statement; earlier result sets were returned. Their logs are retained, and the corrected full query exited0. No database mutation was performed by those queries.

The rejection and reloaded pending screenshots were visually inspected: business reason and pending-policy guidance are readable, standard page controls/layout remain intact. This is desktop1280×900 copy/workflow QA; no claim of new mobile-design validation.

## Focused coverage

RealDB tests assert zero persisted request/day/action rows on invalid submit; exact before/after request/day/action snapshots on invalid pending date/type edits; missing/insufficient second-year rejection followed by valid cross-year edit; quota-free submission; explicit excess paid/unpaid approval outcomes; unchanged quota after pending requests; concurrent nonoverlap requests without reservations and serialized approvals with one success/one quota rejection. Tests leave append-only synthetic history in disposable DB, never delete historical facts for cleanup.

Unit tests independently check fractional boundaries (3.29−0.30 cannot cover3days;3.30−0.30 can), quota locking before writes, no-quota and excess policy and existing approval guards. Existing focused browser approval scenario exercises supervisor3days with corrected type, supervisor4days403, and manager direct4days with quota consumption/history.

## Evidence and limits

Ignored local evidence directory: `docs/superpowers/reports/17-uc08-quota-precheck-evidence/`. Contains preserved RED/failure/GREEN/full-check logs, browser screenshots/traces and source manifest (`tested-source-sha256.json`, seven changed Task2 source/test files plus the unchanged approval scenario). Disposable trace files may contain synthetic credentials and remain local. Tested bases: backend `a352f25eff692bebbe69e43308f80f6aceccd76b`; frontend `22771e7e8ad20cbbeb5578ff3353e66df92bc260`.

Independent review and the whole20-use-case actor/browser matrix remain root-owned gates. This Task2 focused run does not certify all20 use cases, real bank settlement or external email. No commits/push/merge or automation changes performed by Task2 writer.
